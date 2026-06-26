---
name: ppspy
description: Search and analyze Shopify stores, Facebook ads, ad monitoring, and sales tracking using PPSPY e-commerce intelligence API. Find winning products, spy on competitors, monitor ad campaigns, and track real-time sales.
version: 1.0.0
metadata:
  openclaw:
    requires:
      env:
        - PPSPY_API_KEY
      bins:
        - npm
    install:
      command: npm
      args:
        - install
        - -g
        - "ppspy-mcp-server@1.0.1"
    primaryEnv: PPSPY_API_KEY
    emoji: "🔍"
    homepage: https://www.ppspy.com
    mcpServers:
      ppspy:
        command: ppspy-mcp-server
        env:
          PPSPY_API_KEY: "{{PPSPY_API_KEY}}"
---

# PPSPY - E-commerce Intelligence

Search and analyze Shopify stores, Facebook ads, ad monitoring, and sales tracking.

## Setup

1. Visit the official website at [ppspy.com](https://www.ppspy.com/) to view real-time dashboard data and product UI.
2. Visit the direct API site at [api.ppspy.com](https://api.ppspy.com/) to get your API key and manage billing/recharge.
3. Set the environment variable: `PPSPY_API_KEY`

## Available Tools (58 total)

### Shopify Stores (5 tools)
- `ppspy_shopify_store_list` — Search and filter Shopify stores by region, language, revenue, traffic, theme
- `ppspy_shopify_store_details` — Get detailed information for a specific Shopify store
- `ppspy_shopify_store_traffic_list` — Search Shopify stores with traffic data
- `ppspy_shopify_single_product_store_list` — Search single-product Shopify stores
- `ppspy_shopify_theme_store_list` — Search Shopify stores by theme

### Shopify Products (2 tools)
- `ppspy_shopify_product_list` — Search and filter Shopify products by price, sales, category, revenue
- `ppspy_shopify_bestselling_product_list` — Get bestselling products for a specific store

### Ad Library - Ads (2 tools)
- `ppspy_advertisement_list` — Search Facebook ads with advanced filters: keyword, audience reach, spend, status
- `ppspy_advertisement_details` — Get detailed information for a specific advertisement

### Ad Library - Stores (8 tools)
- `ppspy_ad_store_list` — Search ad library stores with advanced filters
- `ppspy_ad_store_details` — Get detailed information for a specific ad store
- `ppspy_ad_store_landing_page_stats` — Get landing page statistics
- `ppspy_ad_store_advertising_trends` — Get advertising trends over time
- `ppspy_ad_store_placement_analysis` — Get ad placement analysis (day/time breakdown)
- `ppspy_ad_store_content_most_used` — Get most used ad copy content
- `ppspy_ad_store_content_longest_run` — Get longest running ad content
- `ppspy_ad_store_advertiser_list` — Get advertisers associated with a store

### Ad Library - Products (2 tools)
- `ppspy_ad_product_list` — Search ad library products with advanced filters
- `ppspy_ad_product_details` — Get detailed information for a specific ad product

### Ad Monitoring (24 tools)
- `ppspy_ad_monitor_create_group` — Create monitoring group
- `ppspy_ad_monitor_group_list` — List all monitoring groups
- `ppspy_ad_monitor_edit_group` — Edit group name
- `ppspy_ad_monitor_delete_group` — Delete group
- `ppspy_ad_monitor_advertiser_search` — Search Facebook advertisers by name
- `ppspy_ad_monitor_create_task` — Create monitoring task(s)
- `ppspy_ad_monitor_task_list` — List monitoring tasks
- `ppspy_ad_monitor_task_set_group` — Assign task to group
- `ppspy_ad_monitor_task_cancel` — Cancel monitoring task
- `ppspy_ad_monitor_task_details` — Get task details
- `ppspy_ad_monitor_task_real_time_overview` — Real-time overview stats
- `ppspy_ad_monitor_task_daily_overview` — Daily overview
- `ppspy_ad_monitor_task_running_overview` — Dashboard stats for running tasks
- `ppspy_ad_monitor_task_landing_page_overview` — Landing page overview
- `ppspy_ad_monitor_task_landing_page_list` — Landing page list with filters
- `ppspy_ad_monitor_task_latest_ad_product` — Latest advertised products
- `ppspy_ad_monitor_task_ad_product_overview` — Product overview by ad count
- `ppspy_ad_monitor_task_ad_product_list` — Product list with filters
- `ppspy_ad_monitor_task_ad_count_stats` — Ad count statistics over time
- `ppspy_ad_monitor_task_ad_deep_analysis` — Ad placement analysis
- `ppspy_ad_monitor_task_ad_content_most_used` — Most used ad copy
- `ppspy_ad_monitor_task_ad_content_longest_run` — Longest running ad content
- `ppspy_ad_monitor_task_ad_list` — Ad list with extensive filters
- `ppspy_ad_monitor_task_ad_details` — Detailed info for a specific monitored ad

### Sales Monitoring (12 tools)
- `ppspy_sales_monitor_create_group` — Create sales monitoring group
- `ppspy_sales_monitor_group_list` — List all sales monitoring groups
- `ppspy_sales_monitor_edit_group` — Edit group name
- `ppspy_sales_monitor_delete_group` — Delete group
- `ppspy_sales_monitor_create_task` — Create sales monitoring task(s), batch up to 50 URLs
- `ppspy_sales_monitor_task_list` — List sales monitoring tasks
- `ppspy_sales_monitor_task_details` — Detailed task info with daily/hourly stats
- `ppspy_sales_monitor_task_real_time_sales` — Real-time individual sales records
- `ppspy_sales_monitor_task_update` — Update task metadata (notes, group)
- `ppspy_sales_monitor_task_stop` — Stop a monitoring task
- `ppspy_sales_monitor_task_delete` — Delete stopped task(s)
- `ppspy_sales_monitor_task_overview` — Aggregated sales overview

### Supplement (3 tools)
- `ppspy_product_category_list` — Get product categories
- `ppspy_ad_filter_options` — Get ad filter options (button types/texts)
- `ppspy_shopify_theme_list` — Get Shopify themes

## Usage Examples

- "Search for Shopify stores with the highest monthly revenue"
- "Find Facebook ads about pet products running for over 30 days"
- "Show me the bestselling products for this Shopify store"
- "Get ad trends for this store over the last 3 months"
- "Create an ad monitoring task for this Facebook advertiser"
- "What are the real-time sales for this store today?"
- "Search for ad products in the beauty category with high audience reach"
- "Show me the most used ad copy for this store"

## Credits

Each API call consumes credits from your PPSPY account:
- **Shopify Store/Product Search**: 1 credit per record
- **Ad Library Search (Ads/Stores/Products)**: 2 credits per record
- **Ad Monitoring / Sales Monitoring**: 1 monitoring quota per task
- **Detail/Analysis/Supplement APIs**: Free
