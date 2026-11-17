# Commerce Flows

Companion to `SKILL.md`. Read this when you are wiring a real backend, or when
you need to reason about what the scaffold actually implements versus what is a
placeholder.

## 1. Catalog flow

What ships:

- `src/data/products.ts` is loaded directly by the pages — no fetch on boot.
- `functions/api/products.ts` is a mock endpoint that returns a small slice of
  the same catalog in the same shape. It exists so swapping to a real API is a
  one-line change in the component, not a shape migration.
- Categories come from the same file and drive: Navbar links, HomePage banners,
  ShopPage tabs, Footer links, and product `category` values.

Upgrade path: point the pages at `/api/products`, add pagination and server-side
filtering, keep the `Product` interface unchanged.

## 2. Cart flow

`src/store/cartStore.ts` (Zustand + `persist`):

- `items: CartItem[]` — keyed by `product.id + selectedSize + selectedColor`, so
  the same product in two sizes is two lines.
- `addItem(product, size, color)` merges an existing line instead of duplicating it.
- `updateQuantity(...)` removes the line when quantity drops to 0.
- `itemCount()` / `total()` are derived, never stored.
- `isOpen` / `toggleCart()` drive the global `CartDrawer`.

The wishlist lives in the same file as a second store (`useWishlistStore`) and is
persisted under `<slug>-wishlist`.

Upgrade path: server-priced carts — send the cart to a `/api/cart` endpoint,
recompute totals server-side, and treat the client total as display-only.

## 3. Checkout flow

Three steps, one component, one `step` state variable:

1. **Shipping** — recipient, phone (`^1[3-9]\d{9}$`), province / city / district
   cascade, detail address, shipping method.
2. **Payment & promo** — promo code against `PROMO_CODES`, payment method
   (WeChat / Alipay / bank card, lucide icons), invoice toggle, order notes.
3. **Review** — address and payment summary with jump-back links, item list,
   terms checkbox, final submit.

Money rules:

- Subtotal comes from `cartStore.total()`.
- Shipping is free once subtotal >= `FREE_SHIPPING_THRESHOLD` (from
  `src/utils/format.ts`), otherwise the selected method's fee.
- Discount is percent or fixed, applied after shipping.
- All display goes through `formatPrice()`.

**The `clearCart()` rule:** the cart is cleared only on the final submit of step
3, once and only once. Clearing earlier (step 1 or 2) destroys the order the
customer is still reviewing.

### Mock mode

Generate an order id (`SL` + `Date.now().toString(36).toUpperCase()`), simulate a
short delay, show the success screen. No external calls.

### Stripe mode

Create a Checkout Session server-side, redirect to Stripe's hosted page, process
the webhook, then update order state. `.env` switches behaviour via
`VITE_PAYMENT_MODE`.

## 4. AI sales concierge flow

Two implementations that must stay in sync:

- Front end: `src/components/AIChatWidget.tsx` — `mockAIResponse()` with >= 8
  keyword scenarios matching **both Chinese and English** keywords, plus a
  default fallback. Replies that recommend products render clickable mini cards.
- Back end: `functions/api/assistant.ts` — the same keyword idea behind an HTTP
  endpoint, as the integration point for a real model.

Suggested live behaviour: ask about occasion, narrow by budget, recommend one
primary product plus one alternative, answer objections briefly, push to
add-to-cart.

## 5. Admin flow

`src/pages/AdminPage.tsx` renders metrics, a recent-orders table with status
pills, top products and a stock overview driven by `product.stock`. Order rows
are mock data in the detected language. Replace with real queries when the
backend exists.
