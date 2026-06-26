# Browser Workflow Guide

## Scope

This skill may use browser automation for JD.com research and cart preparation. It may operate inside a user-owned logged-in browser session after the user logs in manually, but it must stop at the product page or cart page before checkout settlement.

The agent never performs login, CAPTCHA, identity checks, checkout settlement, final order submission, order confirmation, payment, bank, wallet, installment, or payment-provider actions.

## Allowed Operations

| Operation | Login Required | Allowed |
|-----------|----------------|---------|
| Search public result pages | No | Yes |
| Open product pages | No | Yes |
| Read specs, reviews, visible prices, seller badges, and delivery hints | No | Yes |
| Compare candidates | No | Yes |
| Select SKU/options | Sometimes | Yes, after confirmation |
| Add confirmed item to cart | Yes | Yes, after confirmation |
| Review cart contents | Yes | Yes |
| Adjust quantity or remove wrong cart item | Yes | Yes, after confirmation |
| Organize visible cart/product promotions | Yes | Yes, after confirmation |
| Login, CAPTCHA, identity checks | Yes | No |
| Address selection, invoice, checkout settlement, submit order, payment | Yes | No |

## Discovery

```javascript
browser.navigate("https://search.jd.com/Search?keyword=...")

snapshot.extract({
  title: ".p-name",
  price: ".p-price .J_price, .p-price",
  shop: ".p-shop",
  reviewCount: ".p-commit"
})
```

If selectors fail, use visible text and page structure instead of inventing facts. JD page markup changes often; selector examples are hints, not guarantees.

## Product Detail

```javascript
browser.navigate(productUrl)

snapshot.extract({
  title: ".sku-name",
  visiblePrice: ".price, .summary-price",
  promotions: ".prom-words, .J-prom-wrap",
  specs: "#detail .Ptable, .parameter2",
  reviews: ".comment-item"
})
```

Capture:

- Product title and model
- Selected SKU and variant
- Visible public price
- Seller name and seller badge
- Review count and recurring review themes
- Visible promotion or coupon notes
- Delivery cue when visible

## Cart Preparation

Before changing cart state, ask for confirmation:

```text
我准备把这个规格加入购物车：{product} / {sku} / {visiblePrice}。确认继续吗？
```

After confirmation:

```javascript
browser.click(addToCartControl)
browser.navigate("https://cart.jd.com/cart_index/")

snapshot.extract({
  items: ".item-list .item-item",
  subtotal: ".amount .sum",
  promos: ".promotion, .coupon, .cart-gift"
})
```

Cart preparation ends in the cart. Summarize what is ready and tell the user to complete checkout settlement, final confirmation, and payment manually.

Do not click controls whose visible text means:

- 去结算
- 结算
- 提交订单
- 确认订单
- 确认下单
- 立即购买
- 立即支付
- 支付
- 白条支付
- 银行卡
- 钱包

## Stop Rules

Stop browser automation and hand control to the user when any of these appears:

- Login prompt, SMS verification, password field, CAPTCHA, or identity check
- Address selection, invoice details, checkout settlement, final confirmation, submit order, payment, bank, wallet, installment, or payment-provider step
- Any button or link whose visible text means checkout, settlement, final confirmation, order submission, or payment
- A price, seller, SKU, or quantity mismatch that makes the cart uncertain
- A coupon requires entering the checkout/settlement page to verify eligibility

When stopping, summarize the current state and say exactly what the user should verify manually.

## Privacy Handling

- Read only the fields needed for the shopping task.
- Do not store cookies, credentials, account data, payment data, addresses, cart data, or order data outside the active browser session and conversation.
- Redact phone numbers, full names, and full addresses in summaries by default.
- If address or invoice details appear, stop and ask the user to handle that step manually.

## Required Narration

Before actions, say what is happening:

- "我先看搜索结果。"
- "我打开商品详情页核对型号、价格和店铺类型。"
- "我读取评论里的重复问题。"
- "我准备选择这个规格，先请你确认。"
- "我准备加入购物车，先请你确认。"
- "我打开购物车核对商品和数量。"

Never say:

- "我来帮你登录。"
- "我来帮你结算。"
- "我来帮你确认订单。"
- "我来帮你支付。"

## Error Handling

| Scenario | Action |
|----------|--------|
| Login required | Ask the user to log in manually, then continue only after they confirm. |
| CAPTCHA | Stop and let the user handle it. |
| Out of stock | Report and suggest alternatives. |
| Price changed | Alert the user and re-confirm before cart changes. |
| Coupon requires settlement page | Treat it as user-only and stop at cart. |
| Selector does not work | Use visible page evidence; do not fabricate extracted fields. |
