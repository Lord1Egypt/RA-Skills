# Commerce Flows

## 1. Catalog flow

User lands on the storefront and sees:
- featured hero
- product matrix
- benefit blocks
- pricing or product cards
- AI concierge prompt

Default catalog behaviors:
- load product list from `/functions/api/products`
- support category chips
- support featured badges
- support multi-product studio presentation

## 2. Cart flow

User actions:
1. add a product to cart
2. adjust quantity
3. remove an item
4. proceed to checkout

Default cart state:
- local state in frontend
- mock subtotal calculation
- upgrade path to server-priced cart logic

## 3. Checkout flow

### Mock mode
- create a fake order id
- simulate payment success
- redirect to account or success state

### Stripe mode
- create checkout session
- redirect to stripe hosted checkout
- process webhook on payment success
- update order status

## 4. AI sales concierge flow

Primary goal: help the visitor choose the right product.

Suggested behaviors:
- ask what the customer wants to achieve
- narrow by budget, use case, or experience level
- recommend one primary product and one alternative
- answer objections briefly
- push to add-to-cart or checkout

## 5. Account flow

Account page may include purchased products, order history, download links, billing status, and upgrade prompts.

## 6. Admin flow

Admin page may include product list, order list, promo controls, feature toggles, payment mode switch, and assistant prompt configuration.

## 7. Webhook flow

Stripe webhook responsibilities:
- verify signature
- parse event type
- update order/payment status
- emit audit log or console trace
- ignore unsupported events safely
