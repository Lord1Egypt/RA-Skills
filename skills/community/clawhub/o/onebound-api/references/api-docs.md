# Onebound Platform Gateway Reference

## Base URL

All API requests go to:

```
{ONEBOUND_BASE_URL}/v1/{endpoint}
```

## Authentication

Include your platform API key in the request header:

```
Authorization: Bearer {ONEBOUND_API_KEY}
```

## Endpoints

### GET /v1/taobao/item-search

Search Taobao and Tmall products by keyword.

**Common query parameters:**

| Field | Type | Required | Description |
|---|---|---|---|
| q | string | Yes | Search keyword |
| page | integer | No | Page number |
| page_size | integer | No | Number of results to return |
| sort | string | No | Sort mode |
| cat | integer | No | Category ID |

**Response:**

```json
{
  "items": {
    "item": []
  },
  "error_code": "0000",
  "reason": "ok",
  "cost": 0.01,
  "balance": 9.99
}
```

### GET /v1/taobao/item-detail

Fetch Taobao product details by item ID.

**Common query parameters:**

| Field | Type | Required | Description |
|---|---|---|---|
| num_iid | string | Yes | Taobao item ID |
| is_promotion | integer | No | Whether to request promotion data |

**Response:**

```json
{
  "item": {},
  "error_code": "0000",
  "reason": "ok",
  "cost": 0.05,
  "balance": 99.99
}
```

### GET /v1/1688/item-search

Search 1688 products by keyword.

**Common query parameters:**

| Field | Type | Required | Description |
|---|---|---|---|
| q | string | Yes | Search keyword |
| page | integer | No | Page number |
| page_size | integer | No | Number of results to return |
| sort | string | No | Sort mode |
| cat | integer | No | Category ID |

**Response:**

```json
{
  "items": {
    "item": []
  },
  "error_code": "0000",
  "reason": "ok",
  "cost": 0.03,
  "balance": 99.99
}
```

### GET /v1/1688/item-detail

Fetch 1688 product details by item ID.

**Common query parameters:**

| Field | Type | Required | Description |
|---|---|---|---|
| num_iid | string | Yes | 1688 item ID |
| sales_data | integer | No | Whether to include recent sales data |
| agent | integer | No | Whether to include distribution pricing data |

**Response:**

```json
{
  "item": {},
  "error_code": "0000",
  "reason": "ok",
  "cost": 0.05,
  "balance": 99.99
}
```

## Notes

- End users only provide the platform API key.
- Upstream Wanbang authentication and forwarding are handled on the server side.
- The gateway may return `cost` and `balance` when a request succeeds and is billed.

## Error Codes

| HTTP Status | Meaning |
|---|---|
| 200 | Success |
| 400 | Missing or invalid parameters |
| 401 | Invalid or expired API key |
| 402 | Insufficient balance |
| 403 | Insufficient permissions |
| 429 | Rate limit exceeded |
| 500 | Internal server error |
