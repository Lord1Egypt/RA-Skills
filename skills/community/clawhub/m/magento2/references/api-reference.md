# Magento 2 REST API — Quick Reference

Base URL pattern: `{MAGENTO_BASE_URL}/rest/V1/{endpoint}`

## Authentication
OAuth 1.0a (HMAC-SHA256). All four tokens required:
- `MAGENTO_CONSUMER_KEY` + `MAGENTO_CONSUMER_SECRET`
- `MAGENTO_ACCESS_TOKEN` + `MAGENTO_ACCESS_TOKEN_SECRET`

Generate in Magento Admin → System → Integrations.

---

## Orders

| Endpoint | Method | Description |
|---|---|---|
| `orders` | GET | Search orders (searchCriteria) |
| `orders/{id}` | GET | Get single order |
| `orders/{id}/cancel` | POST | Cancel order |
| `orders/{id}/comments` | POST | Add status history comment |
| `order/{id}/ship` | POST | Create shipment |
| `order/{id}/invoice` | POST | Create invoice |

**Order statuses:** `pending`, `pending_payment`, `processing`, `complete`, `closed`, `canceled`, `holded`, `payment_review`

---

## Catalog / Products

| Endpoint | Method | Description |
|---|---|---|
| `products` | GET | Search products |
| `products/{sku}` | GET | Get product |
| `products/{sku}` | PUT | Update product |
| `products/{sku}` | DELETE | Delete product |
| `categories` | GET | Get category tree |
| `categories/{id}` | GET | Get single category |

---

## Customers

| Endpoint | Method | Description |
|---|---|---|
| `customers/search` | GET | Search customers |
| `customers/{id}` | GET | Get customer |
| `customers/{id}` | PUT | Update customer |

---

## Inventory / Stock

| Endpoint | Method | Description |
|---|---|---|
| `stockItems/{sku}` | GET | Get stock item |
| `products/{sku}/stockItems/{itemId}` | PUT | Update stock |
| `stockItems` | GET | Search all stock items |

---

## Multi-Source Inventory (MSI)

Requires Magento 2.3+ with Inventory modules enabled.

| Endpoint | Method | Description |
|---|---|---|
| `inventory/sources` | GET | Search sources (searchCriteria) |
| `inventory/sources/{sourceCode}` | GET | Get source details |
| `inventory/sources` | POST | Create source |
| `inventory/sources/{sourceCode}` | PUT | Update source |
| `inventory/source-items` | GET | Search source items (searchCriteria) |
| `inventory/source-items` | POST | Bulk save source items |
| `inventory/source-items-delete` | POST | Bulk delete source items |
| `inventory/stocks` | GET | Search stocks (searchCriteria) |
| `inventory/stocks/{stockId}` | GET | Get stock |
| `inventory/stocks` | POST | Create stock |
| `inventory/stocks/{stockId}` | PUT | Update stock |
| `inventory/stocks/{stockId}` | DELETE | Delete stock |
| `inventory/get-product-salable-quantity/{sku}/{stockId}` | GET | Get salable qty |
| `inventory/is-product-salable/{sku}/{stockId}` | GET | Check if salable |
| `inventory/stock-source-links` | GET | List stock-source links |
| `inventory/stock-source-links` | POST | Assign sources to stock |
| `inventory/stock-source-links-delete` | POST | Unassign sources from stock |

---

## Promotions

| Endpoint | Method | Description |
|---|---|---|
| `salesRules/search` | GET | Search cart price rules |
| `salesRules/{id}` | GET | Get rule |
| `salesRules/{id}` | PUT | Update rule |
| `coupons` | POST | Create coupon |
| `coupons/search` | GET | Search coupons |
| `store/storeConfigs` | GET | Store configurations |
| `cache` | GET | List cache types |
| `cache/clear` | POST | Clear caches |

---

## Search Criteria Pattern

All list endpoints accept query params:

```
searchCriteria[filterGroups][0][filters][0][field]=status
searchCriteria[filterGroups][0][filters][0][value]=pending
searchCriteria[filterGroups][0][filters][0][conditionType]=eq
searchCriteria[pageSize]=20
searchCriteria[currentPage]=1
searchCriteria[sortOrders][0][field]=created_at
searchCriteria[sortOrders][0][direction]=DESC
```

**Condition types:** `eq`, `neq`, `gt`, `gteq`, `lt`, `lteq`, `like`, `in`, `nin`, `null`, `notnull`

---

## Common HTTP Status Codes

| Code | Meaning |
|---|---|
| 200 | OK |
| 400 | Bad request (validation error) |
| 401 | Unauthorized — check OAuth credentials |
| 404 | Entity not found |
| 500 | Internal server error |