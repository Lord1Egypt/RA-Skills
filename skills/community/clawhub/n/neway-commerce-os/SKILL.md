---
name: neway-commerce-os
description: Generate, scaffold, build and verify a React + Vite + Hono commerce storefront from a short product brief — catalog, cart, wishlist, three-step checkout, admin dashboard, AI sales assistant and EdgeOne Pages deployment files. Use when the user wants a complete ecommerce/store website skeleton from one sentence, especially for digital products, creator stores, productized services, multi-product studios or NewayStudio-style product matrices.
description_zh: 用一句话产品创意生成可运行的 React + Vite 全栈电商站点：商品目录、购物车、收藏夹、三步结算、管理后台、AI 导购与 EdgeOne Pages 部署配置。触发场景：生成电商网站、开店站、独立站、创作者商店、数字商品商店、产品矩阵官网。
description_en: Generate a runnable React + Vite full-stack commerce storefront from a one-line product brief — catalog, cart, wishlist, three-step checkout, admin dashboard, AI sales concierge and EdgeOne Pages deployment files.
version: 1.1.0
author: neway
display_name: Neway Commerce OS 电商建站
display_name_en: Neway Commerce OS
agent_created: true
---

# Neway Commerce OS

One prompt in, one runnable storefront out.

This file is the **single source of truth** for generation. `templates/base`,
`scripts/` and `references/` are all downstream of it. If a rule here conflicts
with anything in the template or the scripts, **this file wins** — and the
inconsistency should be reported to the user, not silently resolved.

---

# 0. IRON RULES (highest priority — never violate, never "improve")

These three rules come from the user and apply to every artifact this skill
produces. They are enforced by machine gates (G-01, G-02) — a violation is a
hard failure, not a style preference.

| # | Rule | Concrete meaning |
|---|------|------------------|
| **IR-1** | **Even px, never below 12** | Every `font-size` in `px` must be even **and** ≥ 12. `text-[10px]`, `text-[11px]`, `text-[13px]` are forbidden. Minimum is 12. |
| **IR-2** | **No emoji in UI** | No emoji anywhere in UI source — not in JSX, not in product data, not in mock responses, not as icon substitutes, not in i18n strings, not decoratively. |
| **IR-3** | **lucide line icons only** | All icons come from `lucide-react` (line style, no fill, single colour). Never a filled icon set, never an emoji glyph, and an inline SVG only when lucide genuinely lacks the glyph. |

> IR-2 and IR-3 reinforce each other: an emoji used as an icon violates both.
> Replace `🛒` with `<ShoppingCart />`, `❤️` with `<Heart />`, `✓` with `<Check />`.

---

# 1. HARD GATES (all must pass before delivery)

`scripts/validate_generated_project.py` implements every gate below. Run it on
the generated project. **Exit code 0 is a precondition for delivery; a failing
gate means fixing the output, not the gate.**

```bash
python <skill>/scripts/validate_generated_project.py <project_dir> --lang en --currency CNY
```

| Gate | Rule |
|------|------|
| F-01 | All required files exist (see §3) |
| F-02 | Style file exists (`src/styles.css`) |
| F-03 | Deployment files exist (warn) |
| F-04 | No template leftovers: `AccountPage.tsx`, `AiConcierge.tsx`, `products.json`, `src/lib/api.ts` |
| P-01 | **Zero** `__PLACEHOLDER__` tokens left in any file |
| P-02 | No placeholder copy: `Product One`, `Category A`, `category-a`, `Lorem ipsum`, `TODO:`, `example.com` |
| G-01 | **IR-2**: no emoji in `src/`, `functions/`, `index.html` |
| G-02 | **IR-1**: every `text-[Npx]` is even and ≥ 12 |
| G-03 | Currency consistent: CNY output contains no `$<digit>`, USD output contains no `¥<digit>` |
| D-01 | ≥ 8 products |
| D-02 | Each product's `images[0] !== images[1]` (hover swap must be visible) |
| D-03 | ≥ 5 real categories, no generic `category-a` style keys |
| D-04 | `Product` interface has every required field (§5) |
| D-05 | `PROMO_CODES` exported (warn) |
| S-01 | Cart store contract: `persist`, `addItem`, `removeItem`, `updateQuantity`, `clearCart`, `itemCount`, `total`, `toggleCart` |
| S-02 | `useWishlistStore` exists and is persisted |
| U-01 | `AIChatWidget` is mounted **once** (in App.tsx, not also in a page) |
| U-02 | No `window.location` navigation — SPA routing only |
| U-03 | AI widget has ≥ 8 keyword scenarios |
| U-04 | HomePage / ShopPage / ProductPage / CheckoutPage section coverage (warn) |
| T-01 | Two complete colour palettes (`brand` + `fresh`/`leaf`) |
| T-02 | Palette scale spans 50–900 (warn) |
| T-03 | Component classes defined: `btn-primary`, `btn-outline`, `btn-ghost`, `tag`, `section-title`, `section-subtitle`, `input-field` |
| T-04 | `lucide-react` in `package.json` dependencies |
| L-01 | `index.html` `lang` matches the detected language |
| I-01 | Every local `/images/*` reference resolves to a real file |
| I-02 | Remote images reachable (only with `--check-images`) |

**Build gate** (not covered by the script — run it yourself):

```bash
cd <project_dir> && npm install && npm run build   # tsc --noEmit && vite build
```

Must exit 0 with zero TypeScript errors. A project that does not build is not a
deliverable.

> **Repo hygiene (not an output gate):** `scripts/check_skill_language.py` fails
> if any Chinese text appears in the skill itself. This skill ships to a global
> audience, so everything except `README.cn.md` and the `description_zh` /
> `display_name` frontmatter lines must be English — **commit messages included**.
> A file that genuinely needs CJK data (e.g. a regex that must also match a zh-CN
> build) carries it as a `\uXXXX` escape, never a literal character.

---

# 2. EXECUTION WORKFLOW (follow exactly)

0. **Detect language.** `powershell -Command "Get-Culture | Select-Object -ExpandProperty Name"` on Windows, `locale | grep LANG` elsewhere. `zh*` → Chinese UI and `lang="zh-CN"`. Otherwise → English UI. **If detection fails or is unavailable, default to English — never block on this step.**
1. **Normalize** the prompt into a brief: brand name, product category, tone, hero product, palette hint.
2. **Scaffold** — never copy files by hand:
   ```bash
   python <skill>/scripts/scaffold_project.py "<prompt>" --output <cwd> --brand "<Brand>" [--site-name "<Name>"]
   ```
   This copies `templates/base`, resolves every placeholder, and never deletes an existing directory (a re-run renames the old one to `<slug>.bak-<timestamp>`).
3. **Fill content.** Open every page and component in the scaffold and replace the demo catalog with content that fits the brief: products, categories, brand story, promo codes, AI responses. Keep the structure and conventions — the template is a compliant reference implementation, not a blank page.
4. **Apply conventions** (§6–§11).
5. **Localize money** (§7).
6. **Run the gate:** `validate_generated_project.py`. Fix every FAIL and re-run until clean.
7. **Run the build gate:** `npm install && npm run build`. Fix every error.
8. **Preview:** `npm run dev`, confirm all 7 routes render.
9. **Deliver** with Handoff Notes (§12) plus the gate and build evidence.

> **Fail-stop rule:** if a gate or the build fails, fix the output and re-run.
> Never deliver with a failing gate, never edit the validator to make a failure
> disappear, and never describe a failing project as "ready except for…".

---

# 3. Output location & file structure

Generate into the **current working directory** (or a directory the user names)
as `<slug>/`. Never generate inside the skill directory, never overwrite an
existing project, never modify `templates/base` while generating.

```
<slug>/
├── index.html                  ← lang attr + Google Fonts
├── package.json
├── tailwind.config.js          ← two palettes + font families
├── postcss.config.js
├── vite.config.ts              ← publicDir: 'static'
├── tsconfig.json
├── .env.example
├── .gitignore
├── edgeone.json
├── README.md
├── static/images/              ← bundled demo image pool
├── src/
│   ├── main.tsx
│   ├── App.tsx                 ← 7 routes + global CartDrawer + AIChatWidget
│   ├── styles.css
│   ├── utils/format.ts         ← formatPrice() — the only money formatter
│   ├── components/
│   │   ├── Navbar.tsx
│   │   ├── Footer.tsx
│   │   ├── ProductCard.tsx
│   │   ├── CartDrawer.tsx
│   │   └── AIChatWidget.tsx
│   ├── pages/
│   │   ├── HomePage.tsx
│   │   ├── ShopPage.tsx
│   │   ├── ProductPage.tsx
│   │   ├── CartPage.tsx
│   │   ├── CheckoutPage.tsx
│   │   ├── WishlistPage.tsx
│   │   └── AdminPage.tsx
│   ├── data/products.ts        ← single source of truth (TypeScript, not JSON)
│   ├── store/cartStore.ts      ← cart + wishlist stores, both persisted
│   └── types/index.ts
└── functions/
    ├── api/products.ts
    ├── api/checkout.ts
    ├── api/assistant.ts
    └── node/stripe-webhook.ts
```

**Route table — all 7 must exist and render.**

| Path | Page | Notes |
|------|------|-------|
| `/` | HomePage | |
| `/shop` | ShopPage | category tabs + filter + sort + grid/list |
| `/product/:id` | ProductPage | dynamic slug, 404 state when not found |
| `/cart` | CartPage | full-page fallback |
| `/checkout` | CheckoutPage | three steps |
| `/wishlist` | WishlistPage | reads wishlistStore |
| `/admin` | AdminPage | mock metrics + orders |

---

# 4. Language

**One rule, no exceptions:** every user-facing string is in the detected
language — nav, hero, buttons, placeholders, error messages, checkout steps,
footer, AI greeting / quick replies / mock responses, admin metric labels and
table headers, category names, filter options, **and mock data** (order rows,
customer names, AI replies).

For `en` output, `name` = English and `nameEn` = an optional short subtitle. For
`zh-CN` output, every product sets `name` = Chinese and `nameEn` = the Latin name.

The bundled template ships **en**. When the detected language is `zh-CN`,
translate every string — do not leave English copy in a zh-CN build. Gate L-01
catches the `lang` attribute; the rest is on you.

---

# 5. Product data contract

`src/data/products.ts` is the only product source. `products.json` must not exist.
All money is CNY unless the market says otherwise (§7).

```ts
export interface Product {
  id: string;             // URL-safe slug, used by /product/:id
  name: string;           // primary display name
  nameEn?: string;        // optional secondary line — short subtitle or Latin name
  brand: string;
  category: string;       // must match a Category.key
  price: number;          // current price
  originalPrice?: number; // crossed-out price
  unit?: string;          // e.g. 'item'
  images: string[];       // >= 2 — [0] primary, [1] hover swap (must differ)
  colors: { name: string; hex: string }[];
  sizes: string[];
  description: string;    // full paragraph
  details: string[];      // feature bullets
  highlight: string;      // one-line selling point on the card
  tags: string[];         // must match the shop filter tag list
  material: string;
  fit: string;
  rating: number;         // 0–5
  reviewCount: number;
  stock: number;          // <= 10 renders the low-stock badge
  isNew: boolean;
  isSale: boolean;
}
```

Also export `categories` (each with `key`, `label`, `icon` = a lucide component,
and `image`) and `PROMO_CODES`.

Requirements: **≥ 8 products**, **≥ 5 real categories** (natural names for the
domain — never `category-a`), each category with at least one product.

---

# 6. Images

**Default: the bundled local pool.** `templates/base/static/images/` holds 16
demo photos (apparel, bags, accessories, plus one interior shot for story blocks).
`vite.config.ts` sets `publicDir: 'static'`, so they resolve as
`/images/<file>.jpg` and are copied to `dist/images/` on build.

- Prefer local images: deterministic, offline-safe, immune to proxy/network
  failures. Gate I-01 verifies every local reference exists.
- Use a remote URL only when the brief's domain has no match in the pool. Then
  every URL must return HTTP 200 — verify with `--check-images` and record any
  replacement in the handoff notes.
- Never invent an image path. Never reference `static/images/...` in code —
  always `/images/...`.

---

# 7. Currency

- The symbol lives in **exactly one place**: `src/utils/format.ts`
  (`CURRENCY_SYMBOL`). Components must call `formatPrice()`; hardcoding `¥` or `$`
  in JSX is a gate failure (G-03).
- Default market is CN → CNY (`¥`). For a non-CN market, change `CURRENCY_SYMBOL`
  and `.env`'s `VITE_DEFAULT_CURRENCY`, then run the gate with `--currency USD`.
- The free-shipping threshold lives in `format.ts` as `FREE_SHIPPING_THRESHOLD`
  and must be imported by CartDrawer / ProductPage / CheckoutPage, never re-typed.

---

# 8. Code conventions

**Fonts** — `index.html` must load:
```html
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@300;400;500;700&family=Noto+Serif+SC:wght@400;600;700&family=Playfair+Display:wght@400;700&display=swap" rel="stylesheet">
```
`tailwind.config.js` defines `font-body` (Noto Sans SC + Latin fallback) and
`font-display` (Playfair Display + **Noto Serif SC**, so Chinese headings do not
fall back to sans).

**Icons** — lucide-react only; `size` 12–22 matched to surrounding text; no fill.
See §0 IR-3.

**Typography** — even px only, ≥ 12 (IR-1). Prefer Tailwind's scale (`text-xs`,
`text-sm`, `text-base`) over arbitrary values.

**State** — Zustand + `persist`. Cart key `<slug>-cart`, wishlist key
`<slug>-wishlist`. Wishlist must use the store, never local `useState`.

**Routing** — `react-router-dom` v6. Always `useNavigate()` / `<Link>`; never
`window.location` (gate U-02).

**Animation** — `framer-motion`. Hover lift `{ y: -4, scale: 1.02 }`, page enter
`{ opacity: 0, y: 20 } → { opacity: 1, y: 0 }`, stagger `staggerChildren: 0.08`.
Ease-out, never bounce.

**TypeScript** — `strict: true`, no `any` outside placeholder API handlers, and
`npm run build` must be clean.

**Dependencies** — the stack is fixed. Do not add packages: no component
libraries, no icon sets other than lucide, no axios, no date libraries.

**Visual language** — off-white or near-black backgrounds (never pure `#000` or
`#fff`), soft borders, rounded corners, muted gradients only, generous whitespace.

---

# 9. Quality floor (minimum complexity per screen)

If time is short, build **fewer pages at higher quality** rather than spreading thin.

**HomePage** — hero (overlay text + 2 CTAs), category banner grid (image + label,
hover colour change), new arrivals (4–8 `isNew` products with stagger),
bestsellers (rating ≥ 4.7, 4 products), brand story (two-column text + image),
AI assistant entry section.

**ShopPage** — sticky category tab bar driven by `?category=`, toolbar with
filter toggle / sort dropdown / grid-list toggle, filter panel (tag multi-select +
price slider), responsive grid (2/3/4 cols), empty state.

**ProductPage** — image gallery (`aspect-[4/5]` + thumbnail strip), badges,
name + optional subtitle, 5-level quality bar, rating, price + crossed original,
colour and size selectors, add-to-cart + wishlist, spec rows (fit / material),
description, detail bullets, delivery info, related products (same category, ≤ 4).

**ProductCard** — hover image swap, badges (new / sale / low stock), heart toggle,
quick-add on hover, brand + name + optional nameEn, 5-level quality bar, rating,
highlight line, price + crossed original, colour dots, and a `layout` prop
(`'grid' | 'list'`).

**CartDrawer** — right-side slide-in (`max-w-sm`), backdrop, item rows with
quantity steppers and delete, subtotal, free-shipping hint, checkout + continue
shopping, empty state. Mounted once in `App.tsx`, toggled from the Navbar.

**CheckoutPage** — three steps (shipping → payment & promo → review) with a
numbered stepper: full name, email, country select, city, postal code, street
address; 3 shipping methods with fees; promo code validated against `PROMO_CODES`
with applied/error feedback; payment methods with **lucide icons**; invoice
toggle; order notes; review step with edit links, item list and agreement
checkbox; sticky order summary; success screen with a generated order number.
**`clearCart()` runs only on the final review submit — never earlier.**

**WishlistPage** — reads wishlistStore, empty state, add-all-to-cart.

**AdminPage** — 4 metric cards, recent orders table with status pills, top
products, stock overview driven by `product.stock`.

**AIChatWidget** — FAB → chat panel (`w-96`, `max-h-[600px]`), brand-coloured
header, ≥ 8 keyword scenarios, product card embeds, typing indicator, 4
quick-reply chips. Keywords must be written in the **same language as the UI** —
English keywords for an `en` build, Chinese for a `zh-CN` build.

**Footer** — service banner row (4 lucide icons), four-column link grid,
newsletter block, dynamic copyright year.

---

# 10. Animation & interaction standard

Smooth, restrained, purposeful. Every interactive element has a hover and active
state. No layout shift on hover, no transition longer than 0.8s, no infinite
decorative loops.

---

# 11. Anti-patterns (things that have actually gone wrong here)

- Mounting `AIChatWidget` in both `App.tsx` and a page → two floating buttons.
- Using `window.location.href` for in-app navigation → full reload and lost SPA state.
- Referencing an icon component that was never imported → build failure.
- Reusing the same URL for `images[0]` and `images[1]` → hover swap does nothing.
- Keyword language drifting from the UI language → the AI assistant goes silent.
- Copying the template's demo catalog verbatim → the store sells the wrong
  products, and gates P-02 / D-01 / D-03 fire.
- Deleting or relaxing validator rules instead of fixing the output.

---

# 12. Handoff Notes (the only delivery document)

Deliver in the reply — do not create a second `NEWAY_BRIEF.md` (that duplication
was removed on purpose).

```
## Handoff Notes — <Brand> Store

### Gates
- validate_generated_project.py: PASS (0 errors, 0 warnings)
- npm run build: exit 0 (tsc --noEmit + vite build clean)

### Scaffold status
- [x] 7 routes implemented and rendering
- [x] Product data wired (N products, M categories)
- [x] Cart + wishlist persisted
- [x] Three-step checkout with promo codes
- [x] AI concierge (K scenarios, zh + en keywords)
- [x] Admin dashboard scaffold
- [x] Iron rules verified (no emoji / even px >= 12 / lucide icons)
- [x] Images resolved (local pool or verified remote)

### Production wiring still required
- [ ] Stripe live keys (STRIPE_SECRET_KEY, STRIPE_WEBHOOK_SECRET)
- [ ] AI endpoint (AI_API_BASE, AI_API_KEY, AI_MODEL)
- [ ] Real order persistence
- [ ] VITE_SITE_NAME / VITE_DEFAULT_CURRENCY in EdgeOne env

### Run it
npm install && npm run dev   →  http://localhost:5173
```

---

# 13. References

Read on demand — do not load everything up front.

| File | When to read |
|------|--------------|
| `references/architecture.md` | Explaining the layer model, or extending the scaffold |
| `references/commerce-flows.md` | Wiring a real cart / checkout / payment backend |
| `references/deployment.md` | Deploying to EdgeOne Pages, env vars, webhook setup |
