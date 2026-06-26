# McDonald's MCP quick reference

## Endpoint
- MCP server: `https://mcp.mcd.cn`
- Header: `Authorization: Bearer <TOKEN>`
- Protocol: JSON-RPC over Streamable HTTP
- MCP version: `2025-06-18`

## Initialize

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "initialize",
  "params": {
    "protocolVersion": "2025-06-18",
    "capabilities": {},
    "clientInfo": {"name": "client-name", "version": "0.1.0"}
  }
}
```

Then send:

```json
{"jsonrpc":"2.0","method":"notifications/initialized","params":{}}
```

## Tested ordering flow

### 1) Saved addresses
Tool: `delivery-query-addresses`
Input: `{}`
Important output fields:
- `addressId`
- `contactName`
- `phone`
- `fullAddress`
- `storeCode`
- `storeName`
- `beCode`

### 2) Store menu
Tool: `query-meals`
Input:
```json
{"storeCode":"1400650","beCode":"140065002"}
```
Important output shape:
- `data.categories[]`
- `data.meals[code] = { name, currentPrice }`

### 3) Meal detail
Tool: `query-meal-detail`
Input:
```json
{"code":"9900003001","storeCode":"1400650","beCode":"140065002"}
```
Important note from docs: default combo replacement not supported yet.

### 4) Price check
Tool: `calculate-price`
Input:
```json
{
  "storeCode":"1400650",
  "beCode":"140065002",
  "items":[
    {"productCode":"901000","quantity":1},
    {"productCode":"904105","quantity":1}
  ]
}
```
Important output fields:
- `productOriginalPrice`
- `productPrice`
- `deliveryOriginalPrice`
- `deliveryPrice`
- `packingOriginalPrice`
- `packingPrice`
- `discount`
- `price`
- `productList[]`

All price fields are in 分 unless the server embeds formatted text in the markdown summary.

### 5) Create order
Tool: `create-order`
Input:
```json
{
  "addressId":"1076478540000118049160177611",
  "storeCode":"1400650",
  "beCode":"140065002",
  "items":[
    {"productCode":"901000","quantity":1},
    {"productCode":"904105","quantity":1}
  ]
}
```
Important output fields:
- `orderId`
- `payId`
- `payH5Url`
- `orderDetail.orderStatus`
- `orderDetail.realTotalAmount`
- `orderDetail.orderProductList[]`

### 6) Query order
Tool: `query-order`
Input:
```json
{"orderId":"1030750870000656448787414429"}
```
Important output fields:
- `orderStatus`
- `storeName`
- `orderProductList[]`
- `deliveryInfo.expectDeliveryTime`

## Useful tool names
- `delivery-query-addresses`
- `delivery-create-address`
- `query-store-coupons`
- `query-meals`
- `query-meal-detail`
- `calculate-price`
- `create-order`
- `query-order`
- `available-coupons`
- `auto-bind-coupons`
- `query-my-coupons`
- `query-my-account`
- `mall-points-products`
- `mall-product-detail`
- `mall-create-order`
- `list-nutrition-foods`
- `campaign-calendar`
- `now-time-info`

## Error expectations
- `401`: bad / missing token
- `429`: rate limit

## Practical tips
- Always use real payable totals from `calculate-price`, not menu prices.
- Delivery fee can make cheap items exceed the user’s budget.
- Some discounts appear automatically at pricing time.
- Order creation returns a payment URL; payment is not complete until the user pays.
