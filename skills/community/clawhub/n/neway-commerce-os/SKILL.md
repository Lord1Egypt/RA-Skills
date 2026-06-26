---
name: neway-commerce-os
description: Generate, scaffold, build, and prepare deployment for a reusable react + vite + hono commerce operating system focused on digital products, storefronts, subscriptions, ai-assisted sales, admin dashboards, and international stripe-style payments. use when the user wants a complete website skeleton from a short prompt, especially for ecommerce launches, creator stores, productized services, multi-product studios, or newaystudio-style product matrices with edgeone pages deployment and full-stack edge functions.
agent_created: true
---

# Neway Commerce OS

## Overview

Generate a production-quality React + Vite storefront from a single product brief.
Default output includes: product catalog, cart, product detail, checkout, wishlist, admin dashboard, AI sales concierge, mock-to-live payment switching, and EdgeOne Pages deployment files.

This Skill is the authoritative source for **all code conventions** used across all generated stores.
Every agent invoking this Skill must follow the conventions below — no exceptions, no shortcuts.

---

## Execution Workflow (follow this exactly)

0. **Detect language**: run locale detection (see Convention 0). If zh-* → generate Chinese UI; else → English.
1. **Normalize** the user's prompt into a product brief (brand name, product category, tone, hero product, color palette hint).
2. **Scaffold** the project by copying `templates/base/` into a new directory named `<brand-slug>-store/`.
3. **Wire content**: replace all `__PLACEHOLDERS__`, translate ALL UI strings to the detected language (see Convention 0 translation map), fill in product data (Chinese `name` + English `nameEn` in zh mode), set brand colors in `tailwind.config.js`.
4. **Apply conventions**: enforce every rule in the CODE CONVENTIONS section below.
5. **Verify images**: check every mock image URL returns HTTP 200. Replace any 404 image with a verified Unsplash URL.
6. **Run build validation**: execute `npm run build` and ensure zero TypeScript errors.
7. **Preview**: start the dev server (`npm run dev`) and verify all routes are accessible.
8. **Deliver**: provide the project directory path and a summary of what is scaffolded vs. what still needs production wiring.

---

## Required File Structure

```
<brand-slug>-store/
├── index.html                  ← must contain Google Fonts + correct lang attr
├── package.json                ← must include all required deps (see below)
├── tailwind.config.js          ← must define font-body, font-heading, brand colors
├── vite.config.ts
├── tsconfig.json
├── .env.example
├── .gitignore
├── edgeone.json
├── src/
│   ├── main.tsx
│   ├── App.tsx                 ← route definitions
│   ├── styles.css
│   ├── vite-env.d.ts
│   ├── components/
│   │   ├── Navbar.tsx
│   │   ├── Footer.tsx
│   │   ├── ProductCard.tsx
│   │   ├── CartDrawer.tsx       ← slide-out cart (REQUIRED, not optional)
│   │   └── AIChatWidget.tsx
│   ├── pages/
│   │   ├── HomePage.tsx
│   │   ├── ShopPage.tsx         ← dedicated browse/filter/sort page (REQUIRED)
│   │   ├── ProductPage.tsx      ← /product/:id — MUST exist and be routed
│   │   ├── CartPage.tsx         ← fallback full-page cart
│   │   ├── CheckoutPage.tsx
│   │   ├── WishlistPage.tsx
│   │   └── AdminPage.tsx
│   ├── data/
│   │   └── products.ts         ← typed product records
│   ├── store/
│   │   └── cartStore.ts        ← Zustand with persist middleware
│   └── types/
│       └── index.ts
└── functions/
    ├── api/
    │   ├── products.ts
    │   ├── checkout.ts
    │   └── assistant.ts
    └── node/
        └── stripe-webhook.ts
```

### Route table (all 7 routes MUST be present)

| Path             | Page             | Notes                        |
|------------------|------------------|------------------------------|
| `/`              | HomePage         |                              |
| `/shop`          | ShopPage         | browse + filter + sort       |
| `/product/:id`   | ProductPage      | dynamic slug — MUST be wired |
| `/cart`          | CartPage         |                              |
| `/checkout`      | CheckoutPage     |                              |
| `/wishlist`      | WishlistPage     |                              |
| `/admin`         | AdminPage        |                              |

---

## Required npm Dependencies

```jsonc
// package.json dependencies (exact versions may float, list them all)
{
  "dependencies": {
    "react": "^18.3.1",
    "react-dom": "^18.3.1",
    "react-router-dom": "^6.26.1",
    "zustand": "^4.5.5",
    "framer-motion": "^11.3.19",
    "lucide-react": "^0.400.0",
    "clsx": "^2.1.1"
  },
  "devDependencies": {
    "@types/react": "^18.3.3",
    "@types/react-dom": "^18.3.0",
    "@vitejs/plugin-react": "^4.3.1",
    "typescript": "^5.5.4",
    "vite": "^5.4.2",
    "tailwindcss": "^3.4.0",
    "autoprefixer": "^10.4.19",
    "postcss": "^8.4.38"
  }
}
```

---

## CODE CONVENTIONS (MANDATORY)

These rules apply to every file generated by this Skill.
Any agent invoking this Skill must treat these as hard constraints, not suggestions.

### 0. Language Detection & i18n (HIGHEST PRIORITY)

**Before scaffolding any project, detect the user's system locale and generate the UI in the matching language.**

Detection protocol:
1. Run `powershell -Command "Get-Culture | Select-Object -ExpandProperty Name"` on Windows, or `locale | grep LANG` on macOS/Linux
2. If the locale starts with `zh` (zh-CN, zh-TW, zh-HK, etc.) → **generate ALL user-facing UI strings in Chinese (Simplified)**
3. If the locale is anything else (`en`, `ja`, `ko`, etc.) → generate ALL user-facing UI strings in English

**Translation scope** — every user-facing string MUST be translated:
- Navbar links, search placeholder, mobile menu
- Hero taglines, CTAs, section titles
- Product names (name field = Chinese, nameEn field = original English name)
- Product descriptions, details, tags
- Buttons, forms, placeholders, error messages
- Checkout steps, shipping methods, payment labels
- Footer columns, copyright text
- AI chatbot greetings, suggestions, mock responses
- Admin dashboard metric labels, table headers
- Category labels, filter options, sort dropdown

**Common UI translation map (for reference):**

| English (template base) | 中文 (zh-CN output) |
|------------------------|---------------------|
| Home | 首页 |
| Shop | 商城 / 全部商品 |
| New In | 新品上架 |
| Sale | 特惠 / 折扣 |
| Cart | 购物车 |
| Wishlist | 收藏夹 |
| Search products... | 搜索商品... |
| Add to Cart | 加入购物车 |
| Checkout | 结算 |
| Continue Shopping | 继续购物 |
| Proceed to Checkout | 去结算 |
| Subtotal | 小计 |
| Free Shipping over $X | 满 ¥X 免运费 |
| Shipping Info | 收货信息 |
| Payment & Promo | 支付与优惠 |
| Order Review | 确认订单 |
| Place Order | 提交订单 |
| Related Products | 相关推荐 |
| Category | 分类 |
| Sort by | 排序 |
| Price: Low to High | 价格从低到高 |
| Price: High to Low | 价格从高到低 |
| Rating | 评分 |
| Newest | 最新上架 |
| Filter | 筛选 |
| All | 全部 |
| Quantity | 数量 |
| Size | 规格 |
| Color | 颜色 |
| Remove | 删除 |
| Your cart is empty | 购物车是空的 |
| No products found | 没有找到商品 |
| AI Assistant | AI 购物助手 |
| Ask me anything... | 问我任何问题... |
| Bestsellers | 热销推荐 |
| New Arrivals | 新品上市 |
| Features | 特色服务 |
| Free Shipping | 免费配送 |
| Secure Payment | 安全支付 |
| Easy Returns | 无忧退换 |
| Contact Us | 联系我们 |
| About Us | 关于我们 |
| Privacy Policy | 隐私政策 |
| Terms of Service | 服务条款 |
| Newsletter | 订阅资讯 |
| Subscribe | 订阅 |
| Your email | 您的邮箱 |

**Note:** The above map is a reference baseline. The agent should use its own full translation ability for product descriptions, product names, and longer content — not just the map above.

### 1. Font System

**Default font stack (apply to all generated projects):**

- **Body / UI text** — Noto Sans SC, sourced from Google Fonts
- **Display / heading** — Playfair Display, sourced from Google Fonts
- **Fallback** — `"Helvetica Neue", Arial, sans-serif`

**index.html — required `<link>` tag:**
```html
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@300;400;500;700&family=Playfair+Display:wght@400;700&display=swap" rel="stylesheet">
```

**tailwind.config.js — required font definitions:**
```js
theme: {
  extend: {
    fontFamily: {
      'body': ['Noto Sans SC', 'Inter', 'sans-serif'],
      'display': ['Playfair Display', 'serif'],
    },
  },
},
```

**styles.css — apply body font globally:**
```css
body {
  font-family: 'Noto Sans SC', 'Inter', sans-serif;
}
```

### 2. Icon System

**All icons MUST use `lucide-react` components. Emoji is prohibited in all UI code.**

Rules:
- Import from `lucide-react`: `import { ShoppingCart, Heart, Star } from 'lucide-react'`
- Default icon size: `size={16}` or `size={20}` — match surrounding text size
- Never use emoji characters (🛒 ❤️ ⭐ 🎉 etc.) anywhere in JSX
- Never use emoji in product data strings that appear in the UI
- Never use `<span>` with emoji content as icon substitutes
- SVG inline icons are allowed only if lucide-react lacks the specific glyph

**Common icon mappings:**

| Old emoji | Lucide component  |
|-----------|-------------------|
| 🛒        | `<ShoppingCart>`  |
| ❤️ / 💝   | `<Heart>`         |
| ⭐ / ✨    | `<Star>`          |
| 🎉        | `<Gift>`         |
| 🚚        | `<Truck>`         |
| 📦        | `<PackageCheck>`  |
| 🌿        | `<Leaf>`          |
| ❄️        | `<Snowflake>`     |
| ✈️        | `<Plane>`         |
| 🔄        | `<RefreshCw>`     |
| ✓ / ✅    | `<Check>`         |

### 3. Typography — px Values

**Prohibited font sizes:**
All odd `px` values in `text-[Xpx]` Tailwind classes are forbidden.

Correction table:

| Forbidden | Use instead |
|-----------|-------------|
| `text-[11px]` | `text-[12px]` |
| `text-[13px]` | `text-[14px]` |
| `text-[15px]` | `text-[16px]` |
| `text-[9px]`  | `text-[10px]` |

**Rule:** All pixel font sizes must be even numbers. Use Tailwind's standard scale (`text-xs`, `text-sm`, `text-base`, etc.) wherever possible; only use `text-[Xpx]` when a specific size is needed and it must be even.

### 4. Image Handling

**All mock product images must return HTTP 200.**

Protocol:
1. For every `image` URL in `src/data/products.ts`, verify the URL is reachable.
2. If any image returns 404 or fails to load, replace it with a verified Unsplash photo URL in this format:
   ```
   https://images.unsplash.com/photo-<ID>?w=800&auto=format&fit=crop
   ```
3. Use category-appropriate search terms when selecting replacement images.
4. Document replaced images in the handoff notes.

### 5. Zustand Store

The cart store must use Zustand with the `persist` middleware so the cart survives page refresh:

```ts
import { create } from 'zustand'
import { persist } from 'zustand/middleware'

export const useCartStore = create(
  persist(
    (set, get) => ({
      items: [],
      addItem: (product) => { /* ... */ },
      removeItem: (id) => { /* ... */ },
      updateQty: (id, qty) => { /* ... */ },
      clearCart: () => set({ items: [] }),
      total: () => get().items.reduce((sum, i) => sum + i.price * i.qty, 0),
    }),
    { name: '<brand>-cart' }
  )
)
```

### 6. Routing — ProductPage

The `/product/:id` route is critical. It must:
- be declared in `App.tsx` as `<Route path="/product/:id" element={<ProductPage />} />`
- read the `id` param with `const { id } = useParams()`
- find the product from `products.ts` data by matching slug or id
- render a 404 state if not found (without crashing)

**ProductCard must navigate on click:**
```tsx
import { useNavigate } from 'react-router-dom'
const navigate = useNavigate()
// on card click:
navigate(`/product/${product.id}`)
```

### 7. Tailwind Configuration

```js
// tailwind.config.js
export default {
  content: ['./index.html', './src/**/*.{js,ts,jsx,tsx}'],
  theme: {
    extend: {
      fontFamily: {
        'body': ['Noto Sans SC', '"Helvetica Neue"', 'Arial', 'sans-serif'],
        'display': ['"Playfair Display"', 'serif'],
      },
      colors: {
        // Override with brand-specific palette per project
        brand: {
          50: '#fafafa',
          500: '#18181b',
          900: '#09090b',
        },
      },
    },
  },
  plugins: [],
}
```

### 8. Animation System

Use `framer-motion` for all transitions. Standard presets:

```tsx
// Card hover lift
whileHover={{ y: -4, scale: 1.02 }}
transition={{ duration: 0.2 }}

// Page enter
initial={{ opacity: 0, y: 20 }}
animate={{ opacity: 1, y: 0 }}
transition={{ duration: 0.4 }}

// Stagger children
variants={{ hidden: { opacity: 0 }, visible: { opacity: 1 } }}
transition={{ staggerChildren: 0.08 }}
```

### 9. TypeScript Strict Mode

- `tsconfig.json` must have `"strict": true`
- All product data must be typed — define a `Product` interface in `src/types/index.ts`
- No `any` unless in placeholder API handlers
- Run `tsc --noEmit` before delivery; fix all errors

### 10. Build Validation Gate

Before delivering the project, run:

```bash
npm install
npm run build
```

The build MUST complete without errors. If there are TypeScript errors, fix them before delivery.
A project that does not build is not a deliverable.

---

## QUALITY FLOOR — MANDATORY UX STANDARDS

**CRITICAL: These are NOT suggestions.** Every generated project MUST meet all of the following minimum complexity levels. If time/effort is short, do FEWER pages but make them HIGHER quality rather than spreading thin. The test output standard is the FRAISE store method — match or exceed that quality level.

### Store (Zustand)

The project MUST have TWO separate Zustand stores, both with `persist` middleware:

**1. cartStore — key `'<brand>-cart'`**
- `items`, `addItem` (merge same-product), `removeItem`, `updateQty`, `clearCart`, `total()`, `count()`

**2. wishlistStore — key `'<brand>-wishlist'`**
- `ids: string[]`, `toggle(id)`, `has(id)`
- WishlistPage MUST use this store, NOT local useState

### Color Palette

Every project MUST define **two complete color palettes** (50–950), both semantic:

| Palette | Purpose | Examples |
|---------|---------|----------|
| `brand` | Primary actions, highlights, CTAs | Warm orange `#d4751a`, amber, or deep red |
| `fresh` / `leaf` | Organic/success badges, nature cues | Green `#74ae58`, teal `#4EcDc4` |

The theme colors must feel appropriate for the product category. A fruit store uses warm orange + green; a tech store might use indigo + teal. Never use a single-palette or generic gray-only theme.

### CSS Component Classes (in styles.css @layer components)

Minimum required classes (all MUST be defined and used):

| Class | Purpose |
|-------|---------|
| `btn-primary` | Main CTA button (brand fill, white text, rounded-full, hover lift) |
| `btn-outline` | Secondary button (brand border, brand text, transparent bg) |
| `btn-ghost` | Tertiary link-style button (gray text, hover dark) |
| `tag` | Capsule badge (uppercase, tracking-wider, rounded-full) |
| `section-title` | Page section heading (text-2xl, font-display, font-semibold) |
| `section-subtitle` | Section subtitle (text-sm, text-neutral-500) |

### HomePage — Minimum Complexity

The HomePage MUST contain ALL of the following sections in order:

1. **Hero section** — full-width with overlay text, CTA buttons, brand tagline
2. **Category banner grid** — image + label for each non-"all" category, hover color change
3. **New Arrivals** — grid of `isNew` products (4–8 items), with `framer-motion` fadeUp stagger
4. **Bestsellers** — grid of top-rated products (rating ≥ 4.8), 4+ items
5. **Brand story** — two-column text + image section
6. **AI assistant entry** — call-to-action inviting user to click the AI chat widget

### ShopPage — MUST Exist

A dedicated browse page (`/shop`) with:

1. **Category tab bar** — sticky, horizontal scroll, URL param driven (`?category=xxx`)
2. **Toolbar** — filter toggle (expand/collapse), sort dropdown (default/price↑/price↓/rating/newest), grid/list toggle
3. **Filter panel** — tag multi-select (New/Hot/Sale/Classic/Editor Pick), price range slider
4. **Product grid** — responsive (2/3/4 cols), filtered + sorted results, empty state
5. **Pagination** (optional) — if >20 products, show page controls

### CartDrawer — MUST Exist

A slide-out drawer component (NOT an inline section in Navbar):

1. Right-side overlay + slide-in panel (max-w-sm)
2. Product list: thumbnail + name + size + quantity ± buttons + subtotal + delete
3. Footer: subtotal, shipping note ("Free shipping over $99"), "Checkout" button, "Continue Shopping" button
4. Empty state with link to shop
5. The drawer is mounted globally in App.tsx, toggled from Navbar cart icon

### CheckoutPage — Minimum Complexity

A three-step checkout flow with progress indicator, accessible via `/checkout` from CartDrawer or CartPage "Checkout" buttons:

1. **Step 1 — Shipping Info**
   - Recipient name, phone validation (11-digit `^1[3-9]\d{9}$`)
   - Province / City / District cascade selectors (at least 10 provinces populated)
   - Detail address input
   - Shipping method radio group (3 options: express/standard/economy) with descriptions and pricing
   - Free shipping threshold display (Free over $X)

2. **Step 2 — Payment & Promo**
   - Promo code input with apply button — validate against a local PROMO_CODES map, show discount applied/error message
   - Payment method radio group (WeChat Pay / Alipay / Bank Card) with icons
   - Invoice toggle (checkbox) → expandable invoice title input
   - Order notes textarea

3. **Step 3 — Order Review**
   - Full address summary with "Edit" button to jump back to step 1
   - Shipping & payment method confirmation
   - Product list (thumbnail + name + spec + price × qty)
   - Agreement checkbox or statement (Terms of Service + Privacy Policy)
   - Submit button — only at this point call `clearCart()`

**Critical bug fix required:** Do NOT call `clearCart()` on initial submit — only clear after user confirms in step 3.

**Progress indicator:** 3-step horizontal stepper (numbered circles, step labels, connector lines), current step highlighted in brand color, completed steps show checkmark.

**Sidebar:** Sticky order summary panel (right side on desktop, hidden on mobile) showing:
- Product thumbnails + names + sizes × qty
- Subtotal, shipping cost, promo discount (when applied), grand total
- Security badge + return policy note

**Order confirmation after submission:**
- Success animation (spring scale + rotation)
- Order number generation (`SL` + timestamp base36)
- Item count + total paid
- Estimated delivery (1-3 days)
- "Continue Shopping" and "Back to Home" buttons

### ProductPage — Minimum Complexity

1. **Image gallery** — large main image (aspect-[4/5]) + clickable thumbnail strip below, hover swap
2. **Product info** — tags (NEW/SALE/ORGANIC badges), brand, Chinese + English name, star rating with count, quality bar (5-level progress bar), price (large) + crossed originalPrice, size/color selector, quantity ±, "Add to Cart" primary button, heart favorite button, delivery info list
3. **Description section** — full description text + origin/spec info card
4. **Related products** — same-category items (up to 4), excluding current product

### ProductCard — Minimum Complexity

1. **Image swap on hover** — primary image → secondary image fade transition (opacity 1→0)
2. **Badges** — NEW / SALE / ORGANIC (Leaf icon) / LOW_STOCK
3. **Heart favorite button** — appears on hover, persists if favorited, connects to wishlistStore
4. **Quick-add button** — slides up from bottom on hover, adds to cart
5. **Info area** — brand, Chinese name, English name (smaller, gray), quality bar (5 levels), star rating + count, highlight tagline, price + crossed originalPrice, color dots

### ProductCard Must Support Two Layouts

The component must accept a `layout` prop: `'grid'` | `'list'`

- **Grid**: standard card with vertical image + info below
- **List**: horizontal row with image left + info right

### AIChatWidget — Minimum Complexity

1. Floating FAB button (bottom-right), expands to chat panel (w-96, max-h-[600px])
2. Gradient header (brand → fresh/leaf) with title "AI Assistant" + close button
3. **Minimum 8 keyword scenarios** in mockAIResponse(): gift/budget, new arrivals, sale, bestsellers, premium/luxury, and a default welcome
4. **Product card embeds** — AI responses that mention products MUST include clickable mini product cards (thumbnail + name + price + link)
5. **Typing animation** — 3 bouncing dots while "thinking"
6. **Quick reply chips** — 4 preset questions below the input area

### Footer — Minimum Complexity

1. **Service banner row** — 4 feature icons in a row above the main footer: shipping (Truck), quality (ShieldCheck), sourcing (Globe), support
2. **Four-column link grid** — brand intro + social icons, product series links, shopping guide links, about us links
3. Copyright bar with year dynamically generated (`new Date().getFullYear()`)

### Product Data — Required Fields

Every Product record MUST include ALL of these fields. No field is optional.

```ts
export interface Product {
  id: string;            // URL-safe slug
  name: string;          // Chinese product name
  nameEn: string;        // English product name
  brand: string;
  category: string;
  price: number;         // current price in CNY
  originalPrice?: number; // crossed-out price
  images: string[];      // at least 2 images (primary + secondary for hover swap)
  colors: { name: string; hex: string }[];
  sizes: string[];
  description: string;   // full description paragraph
  details: string[];     // feature list
  tags: string[];        // e.g. ["new", "sale", "organic", "gift", "limited"]
  material?: string;    // material description
  fit?: string;         // fit description
  rating: number;        // 0–5
  reviewCount: number;
  isNew: boolean;
  isSale: boolean;
}
```

### Product Count & Categories

- **Minimum 8 products**, each with verified Unsplash images
- **Minimum 5 categories** (excluding "all"), each with at least 1 product
- Categories must be natural for the product domain (e.g. berries/citrus/tropical/stone/melons/gift for fruit, not generic "category-1")
- Each category needs a Lucide icon reference in the Category interface

### Implementation Quality Rules

1. **Never skip a section to save time.** Every section in the QUALITY FLOOR MUST be implemented.
2. **Open the template's existing page files and REPLACE their content**, do not keep generic template placeholder text.
3. **Clean up unused template files** — delete `AccountPage.tsx`, `AiConcierge.tsx`, `products.json`, `lib/api.ts` after generation.
4. **Fill in `edgeone.json`** with real values, no `__SITE_SLUG__` placeholders.
5. **All mock data** (AdminPage orders, AI responses, etc.) must be English-localized and category-appropriate.
6. **All `__PLACEHOLDER__` tokens must be replaced** in every file.

---

## Product Data (generated as TypeScript, not JSON)

The product data file is `src/data/products.ts` (NOT `.json`). The `products.json` template file must be DELETED after generation.

Product data placement:
- Export a `products: Product[]` array using the Product interface defined in the QUALITY FLOOR section
- Export a `categories` array with `{ key, label }` — use appropriate labels per category
- Export a `PROMO_CODES` map with `{ code, discount, type, description }`

---

## Default Stack

| Layer      | Technology                                          |
|------------|-----------------------------------------------------|
| Frontend   | React 18 + Vite 5 + TypeScript 5 + Tailwind CSS 3   |
| Icons      | lucide-react (NO emoji)                              |
| Animation  | framer-motion                                        |
| State      | Zustand + persist middleware                         |
| Routing    | react-router-dom v6                                  |
| Fonts      | Noto Sans SC (body) + Playfair Display (heading)    |
| API        | Hono (Edge Functions) + Node Functions              |
| Payment    | Stripe (mock dev / live prod)                        |
| Deployment | EdgeOne Pages                                        |

---

## Visual Language Defaults

- Background: near-black or light-neutral — avoid pure `#000` or `#fff`
- Card style: subtle border + shadow, no harsh outlines
- Gradient: muted, not neon — avoid blue-purple AI-gradient clichés
- Motion: smooth ease-out, not bounce
- Image aspect ratio: `aspect-square` or `aspect-[4/5]` for product cards
- Typography hierarchy: heading (`font-display`) for H1/H2, body (`font-body`) for everything else

---

## Handoff Notes Format

After scaffolding, always deliver notes in this format:

```
## Handoff Notes — <Brand> Store

### Scaffold Status
- [x] All 7 routes implemented
- [x] Product data wired (N products)
- [x] Cart with persist middleware
- [x] Mock checkout flow (3-step: address → payment → review)
- [x] AI concierge widget
- [x] Admin dashboard scaffold
- [x] Build passes (tsc + vite build)
- [x] All images verified 200

### Production Wiring Required
- [ ] Connect Stripe live keys (set STRIPE_SECRET_KEY)
- [ ] Wire AI assistant endpoint (set AI_API_KEY, AI_MODEL)
- [ ] Replace mock order IDs with database persistence
- [ ] Set VITE_SITE_NAME, VITE_DEFAULT_CURRENCY in EdgeOne env vars

### Dev Server
npm run dev → http://localhost:5173
```

---

## Quality Checklist (run before delivery)

- [ ] Zero TypeScript errors (`npm run build`)
- [ ] All 7 routes render without crashing
- [ ] `/product/:id` is accessible from ProductCard clicks
- [ ] `/shop` has filter + sort + grid/list toggle
- [ ] CartDrawer is mounted globally and toggled from Navbar
- [ ] CheckoutPage has 3-step flow (address → payment&promo → review) with progress stepper
- [ ] Checkout does NOT call clearCart() until final submission review step
- [ ] Checkout has shipping methods, payment methods, promo code, invoice toggle
- [ ] Cart persists across page refresh (zustand persist)
- [ ] Wishlist persists across page refresh (wishlistStore with persist)
- [ ] No emoji anywhere in JSX or product data display strings
- [ ] No odd-px font size classes (`text-[11px]`, `text-[13px]`, etc.)
- [ ] All images return HTTP 200
- [ ] Noto Sans SC loaded in index.html + tailwind.config.js
- [ ] lucide-react is in package.json dependencies
- [ ] tailwindcss + postcss + autoprefixer are in devDependencies
- [ ] Two complete color palettes defined (brand + fresh, 50-950)
- [ ] No `__PLACEHOLDER__` tokens remain in any file
- [ ] Unused template files deleted (AccountPage, AiConcierge, products.json, lib/api.ts)
- [ ] HomePage has: hero, category banners, new arrivals, bestsellers, brand story, AI entry
- [ ] ProductCard supports both grid and list layouts
- [ ] Product data has all required fields (nameEn, images[], tags[], material, fit, etc.)
- [ ] AIChatWidget has 8+ keyword scenarios with product card embeds
