import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load your data
df_all_data = pd.read_csv("E-Commerce Public Dataset/all_data.csv")
df_geolocation = pd.read_csv("E-Commerce Public Dataset/geolocation_dataset.csv")
df_category_name = pd.read_csv("E-Commerce Public Dataset/product_category_name_translation.csv")
df_customer = pd.read_csv("E-Commerce Public Dataset/customers_dataset.csv")
df_product = pd.read_csv("E-Commerce Public Dataset/products_dataset.csv")
df_order_review = pd.read_csv("E-Commerce Public Dataset/order_reviews_dataset.csv")
df_order_item = pd.read_csv("E-Commerce Public Dataset/order_items_dataset.csv")
df_order = pd.read_csv("E-Commerce Public Dataset/orders_dataset.csv")
df_seller = pd.read_csv("E-Commerce Public Dataset/sellers_dataset.csv")

# Melakukan join antara df_product dan df_order_item berdasarkan product_id dan order_id
df_product = df_product[['product_id']]
df_order_item = df_order_item[['order_id', 'product_id']]
df_order_review = df_order_review[['order_id', 'review_score', 'review_creation_date']]

# Merge dataframes
df_merged = pd.merge(df_product, df_order_item, on='product_id')
df_final = pd.merge(df_merged, df_order_review, on='order_id')

# Preprocess your data
selected_product_ids = df_final['product_id'].unique()[:112371]
df_final_selected = df_final[df_final['product_id'].isin(selected_product_ids)]

# Sidebar for date range selection
start_date = st.date_input('Select start date', pd.to_datetime('2017-08-01'))
end_date = st.date_input('Select end date', pd.to_datetime('2018-08-31'))

# Convert start_date and end_date to datetime64[ns]
start_date = pd.to_datetime(start_date)
end_date = pd.to_datetime(end_date)

# Filter data based on selected date range
df_final_selected['review_creation_date'] = pd.to_datetime(df_final_selected['review_creation_date'])
df_final_selected = df_final_selected[
    (df_final_selected['review_creation_date'] >= start_date) & (df_final_selected['review_creation_date'] <= end_date)
]
df_final_selected['month_year'] = df_final_selected['review_creation_date'].dt.to_period('M')

# Groupby and calculate summary statistics
summary_df = df_final_selected.groupby('month_year').agg({'review_score': ['count', 'mean']}).reset_index()
summary_df.columns = ['month_year', 'review_count', 'avg_review_score']

# Line chart for Number of Reviews
st.subheader('Number of Reviews Over Time')
st.line_chart(summary_df.set_index('month_year')['review_count'])

# Line chart for Average Review Score
st.subheader('Average Review Score Over Time')
st.line_chart(summary_df.set_index('month_year')['avg_review_score'])

# Display Total Customer and Seller by State
st.title('Distribution of Customers and Sellers by State')

# Bar chart for Total Customer by State
customer_count_by_state = df_customer['customer_state'].value_counts()
st.subheader('Total Customer by State')
st.bar_chart(customer_count_by_state)

# Bar chart for Total Sellers by State
seller_count_by_state = df_seller['seller_state'].value_counts()
st.subheader('Total Sellers by State')
st.bar_chart(seller_count_by_state)
