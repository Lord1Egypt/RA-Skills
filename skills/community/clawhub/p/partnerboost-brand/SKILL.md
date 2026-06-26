---
name: partnerboost-api
description: Call PartnerBoost merchant APIs to manage transactions, performance, billing, partners and more
version: 1.1.1
tags: [partnerboost, api, merchant]
requires:
  env:
    - PARTNERBOOST_API_KEY
---

# PartnerBoost Merchant API

You can call PartnerBoost merchant APIs using curl. All requests require the `X-Api-Key` header for authentication.

Please contact CSM to get the API key.

## Setup

OpenClaw (and compatible clients such as QClaw) decide **where** configuration lives and how secrets are wired. This Skill does not document a canonical config file, layout, or JSON shape—you only need **`PARTNERBOOST_API_KEY`** in the process environment when API calls run. Use your client’s official instructions to supply it.

## Authentication

Every request must include:

```
-H "X-Api-Key: $PARTNERBOOST_API_KEY"
```

## Base URL

```
https://app.partnerboost.com
```

## API Pattern

All WebUI APIs follow this pattern:

- **GET**: `curl -s -H "X-Api-Key: $PARTNERBOOST_API_KEY" "https://app.partnerboost.com/a/{controller}/{action}?param1=value1&param2=value2"`
- **POST**: `curl -s -X POST -H "X-Api-Key: $PARTNERBOOST_API_KEY" -H "Content-Type: application/json" -d '{"key":"value"}' "https://app.partnerboost.com/a/{controller}/{action}"`

## Response Format

All APIs return JSON: `{ "code": 0, "message": "ok", "data": ... }`. Code 0 means success.

Paged responses include: `total_size`, `total_page`, `page_size`, `page_num`, `current_size` in the data.

---

## 1. Transaction (订单)

### 1.1 List Transactions (`list4`)

Query orders with filters and pagination. **`list3` is deprecated**; use **`list4`** (backend: `get_list4`).

Simple range query (GET):

```bash
curl -s -H "X-Api-Key: $PARTNERBOOST_API_KEY" \
  "https://app.partnerboost.com/a/transaction/list4?page_num=1&page_size=20&trans_time_start=1735689600&trans_time_end=1741737600"
```

Filters use **`processTransListParams`** on the server. Common fields (all optional unless noted):

- `page_num` (int): page number, default 1  
- `page_size` (int): page size, default 20 (clamped by server)  
- `trans_time_start`, `trans_time_end` (int): Unix timestamp (seconds), transaction time range  
- `trans_keywords` (string): keyword search (order id, tags, SKU, promo, etc., depending on merchant settings)  
- `trans_tag` (string): tag substring match  
- `trans_status` (array): e.g. `new`, `void`, `paid`, `effective`, `mixed` (SKU-level rollups)  
- `trans_sku_status` (array): SKU-level `paid`, `new`, `void`, `effective`  
- `trans_type` (array): transaction types  
- `trans_client_device` (array): e.g. `mobile`, `pc`, `admin`, `-`  
- `trans_norm_id` (array): norm IDs  
- `partner_channel_id` (array): **channel / medium** filter — numeric site IDs or `PB…` medium codes (server may normalize IDs)  
- `partner_id` (array): partner user IDs  
- `partner_group` (array): partner group IDs  
- `partner_channel_type` (array): `WEBSITE`, `SOCIAL_NETWORK`, `MOBILE`  
- `partner_location` (array): country codes  
- `partner_type` (array): `influencer`, `publisher`  
- `payment_id`, `acc_upload_id`, `performance_bonus_type_id` (int): other filters  
- Plus Amazon / affiliate-related filters: `amazon_shop_country`, `amazon_product_brand`, `affiliate_type` as implemented server-side  

Array parameters are easiest via **POST + JSON** (see **API Pattern**). Example:

```bash
curl -s -X POST -H "X-Api-Key: $PARTNERBOOST_API_KEY" -H "Content-Type: application/json" \
  -d '{"page_num":1,"page_size":20,"trans_time_start":1735689600,"trans_time_end":1741737600,"trans_status":["paid"],"partner_channel_id":["PB00001234"]}' \
  "https://app.partnerboost.com/a/transaction/list4"
```

Default sort is by transaction time / id descending (server-defined).

### 1.2 Transaction Statistics

Get order statistics summary. Uses the **same filter set as 1.1** (`processTransListParams`).

```bash
curl -s -H "X-Api-Key: $PARTNERBOOST_API_KEY" \
  "https://app.partnerboost.com/a/transaction/list_stats?trans_time_start=1735689600&trans_time_end=1741737600"
```

Parameters: same filters as **1.1** (optional). `page_num` / `page_size` are initialized on the server but do not change the aggregated stats shape.

### 1.3 Recent Transactions

Get the latest 10 orders. No parameters needed.

```bash
curl -s -H "X-Api-Key: $PARTNERBOOST_API_KEY" \
  "https://app.partnerboost.com/a/transaction/nearly_list"
```

---

## 2. Performance (业绩)

### 2.1 Performance Charts

Get performance chart data (clicks, orders, commission trends).

```bash
curl -s -H "X-Api-Key: $PARTNERBOOST_API_KEY" \
  "https://app.partnerboost.com/a/performance/charts_v2?start_date=1735689600&end_date=1741737600&group_by=day"
```

Parameters:
- `start_date` (int, required): Unix timestamp (10-digit)
- `end_date` (int, required): Unix timestamp (10-digit)
- `group_by` (string): day, week, or month. Default: day
- `medium_id` (string): filter by media ID
- `channel` (string): filter by channel
- `partner_group_id` (int): filter by partner group

### 2.2 Performance List

Get performance detail list with pagination.

```bash
curl -s -H "X-Api-Key: $PARTNERBOOST_API_KEY" \
  "https://app.partnerboost.com/a/performance/list_v2?start_date=1735689600&end_date=1741737600&page_num=1&page_size=20"
```

Parameters:
- `start_date` (int, required): Unix timestamp (10-digit)
- `end_date` (int, required): Unix timestamp (10-digit)
- `page_num`, `page_size`
- `group_by` (string): day, week, month, medium, or channel
- `medium_id`, `channel`, `partner_group_id` — same as charts
- `sort_type` (string): sort field
- `sort_order` (string): asc or desc

### 2.3 Performance Totals

Get performance summary totals.

```bash
curl -s -H "X-Api-Key: $PARTNERBOOST_API_KEY" \
  "https://app.partnerboost.com/a/performance/charts_total?start_date=1735689600&end_date=1741737600"
```

Parameters:
- `start_date` (int, required): Unix timestamp (10-digit)
- `end_date` (int, required): Unix timestamp (10-digit)
- `medium_id`, `channel`, `partner_group_id`

### 2.4 Search Partner Performance

Search partners by keyword in performance reports.

```bash
curl -s -H "X-Api-Key: $PARTNERBOOST_API_KEY" \
  "https://app.partnerboost.com/a/performance/search_partner?word=keyword"
```

Parameters:
- `word` (string, required): search keyword

---

## 3. Account / Billing (结算)

### 3.1 Billing List

Get billing records with filters.

```bash
curl -s -H "X-Api-Key: $PARTNERBOOST_API_KEY" \
  "https://app.partnerboost.com/a/account/billing_list?page_num=1&page_size=20"
```

Parameters (all optional):
- `page_num`, `page_size`
- `mid` (string): media ID
- `ids` (string): billing IDs, comma-separated
- `time_start` (int): start time, Unix timestamp
- `time_end` (int): end time, Unix timestamp
- `payment_method`, `payment_type`, `status`, `search_word`

### 3.2 Account Info

Get account information including balance.

```bash
curl -s -H "X-Api-Key: $PARTNERBOOST_API_KEY" \
  "https://app.partnerboost.com/a/account/account_info"
```

### 3.3 Current Plan

Get current subscription plan details.

```bash
curl -s -H "X-Api-Key: $PARTNERBOOST_API_KEY" \
  "https://app.partnerboost.com/a/account/current_plan"
```

### 3.4 Prepayment List

Get prepayment records.

```bash
curl -s -H "X-Api-Key: $PARTNERBOOST_API_KEY" \
  "https://app.partnerboost.com/a/account/pre_payment?page_num=1&page_size=20"
```

Parameters (all optional): `page_num`, `page_size`, `mid`, `time_start`, `time_end`