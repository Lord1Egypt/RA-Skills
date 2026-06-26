# Browser Workflow Guide

## Overview

This skill supports browser automation for Pinduoduo (拼多多) shopping with clear safety boundaries.

## Supported Operations

| Operation | Login Required | Description |
|-----------|----------------|-------------|
| Search | No | Search products with filters |
| 百亿补贴 | No | Browse subsidized deals |
| View Product | No | Read specs, prices, group options |
| Seller Vetting | No | Check ratings, badges, reviews |
| Add to Cart | Yes | Add selected item |
| View Cart | Yes | Review cart contents |
| Initiate Group | Yes | Start 拼团 |
| Join Group | Yes | Join existing 拼团 |
| Apply Coupons | Yes | Check platform/seller coupons |
| Generate Order Preview | Yes | Calculate final price |
| Payment | **Never** | User only |

## Workflow Steps

### 1. Discovery (Public Pages)
```javascript
// Navigate to search or 百亿补贴
browser.navigate("https://mobile.yangkeduo.com/")
browser.click("[data-test='billion-subsidy']")

// Extract deals
snapshot.extract({
  title: ".goods-title",
  currentPrice: ".current-price",
  subsidyPrice: ".subsidy-price",
  groupPrice: ".group-price",
  storeBadge: ".store-badge",
  salesCount: ".sales-count"
})
```

### 2. Product Detail
```javascript
// Open product page
browser.navigate(productUrl)

// Extract details
snapshot.extract({
  title: ".goods-title",
  currentPrice: ".price-current",
  groupPrice: ".price-group",
  groupSize: ".group-size",
  currentGroup: ".current-group-count",
  storeName: ".store-name",
  storeRating: ".store-rating",
  badges: ".service-badges",
  reviews: ".review-item"
})
```

### 3. Cart & Group Operations (Login Required)
```javascript
// Add to cart
browser.click(".add-cart-btn")

// Or initiate/join group
browser.click(".group-buy-btn")
browser.click(".initiate-group") // or .join-group

// View cart
browser.navigate("https://mobile.yangkeduo.com/cart.html")

// Extract cart info
snapshot.extract({
  items: ".cart-item",
  subtotal: ".cart-subtotal",
  coupons: ".available-coupon"
})
```

### 4. Order Preview (Login Required)
```javascript
// Proceed to checkout
browser.click(".checkout-btn")

// Extract order summary
snapshot.extract({
  address: ".delivery-address",
  items: ".order-item",
  groupDiscount: ".group-discount",
  couponDiscount: ".coupon-discount",
  total: ".order-total"
})
```

## Safety Rules

1. **Always announce** before browser actions
2. **Stop at payment** - never proceed to payment
3. **Ask before login** - get explicit consent
4. **Show evidence** - snapshot key information
5. **Handoff clearly** - tell user next manual steps

## Common Selectors

| Element | Selector |
|---------|----------|
| Search box | `.search-input` |
| Search button | `.search-btn` |
| 百亿补贴 tab | `[data-test='billion-subsidy']` |
| Product title | `.goods-title` |
| Current price | `.price-current` |
| Group price | `.price-group` |
| Store badge | `.store-badge` |
| Service badges | `.service-badges` |
| Add to cart | `.add-cart-btn` |
| Group buy | `.group-buy-btn` |
| Initiate group | `.initiate-group` |
| Join group | `.join-group` |
| Coupon input | `.coupon-input` |
| Submit order | `.submit-order-btn` |

## Error Handling

| Scenario | Action |
|----------|--------|
| CAPTCHA | Hand to user |
| Login required | Ask user first |
| Group full | Suggest starting new group |
| Price changed | Alert user before proceeding |
| Coupon invalid | Try alternatives or report |
| Seller rating low | Warn user and ask confirmation |
