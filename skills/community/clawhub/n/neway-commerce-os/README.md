# Neway Commerce OS

> A WorkBuddy Skill: turn **one line of product idea** into a runnable full-stack
> storefront — and force it through a quality gate before it ships.

> Built for the WorkBuddy Bot. Also works when you feed this Skill to Cursor,
> Claude or GPT.

**English** · [Chinese](README.cn.md)

---

## Quick start

Say this to the bot:

> **"Build a premium fashion storefront selling coats and bags."**

The bot will: detect the language → normalise the brief → scaffold from the
bundled template → fill in content → **run the quality gate** → **run the build**
→ deliver Handoff Notes with evidence.

The bundled template ships an **English fashion store** (outerwear / dress / tops /
knitwear / bags / accessories, 12 products, local image pool). Prices default to
¥ (CNY) — see [Currency](#currency) to switch to USD. Edit the copy and data from
there.

---

## The three iron rules (hard constraints, not suggestions)

| # | Rule | Gate |
|---|------|------|
| IR-1 | Font sizes must be **even** and **≥ 12px** | `G-02` |
| IR-2 | **No emoji** anywhere in UI source | `G-01` |
| IR-3 | Icons are **lucide line style**, always | `T-04` + review |

Violating any of them fails generation. Fix the output — never the gate.

---

## Quality gate

A build that has not passed the gate is not a deliverable.

```bash
python scripts/validate_generated_project.py <project_dir> --lang en --currency CNY
```

29 checks covering: structural completeness, leftover placeholders and placeholder
copy, emoji, font sizes, currency consistency, product/category counts, hover-image
swap, the `Product` interface, store contracts, SPA routing, AI scenario count,
dual palettes, component classes, the `lang` attribute, and image resolution.

Exit code 0 is required. **Fix the output, not the gate.**

Build gate (not covered by the script — run it yourself):

```bash
cd <project_dir> && npm install && npm run build   # tsc --noEmit && vite build
```

---

## Generated project layout

```
site-name/
├── index.html                  <- lang attribute + Google Fonts
├── package.json                <- fixed dependency set (do not add packages)
├── tailwind.config.js          <- two palettes: brand + fresh
├── postcss.config.js
├── vite.config.ts              <- publicDir: 'static'
├── tsconfig.json               <- strict: true
├── .env.example
├── edgeone.json                <- EdgeOne Pages deployment config
├── README.md
├── static/images/              <- 16 bundled demo photos (copied to dist/images/)
├── src/
│   ├── main.tsx
│   ├── App.tsx                 <- 7 routes + global CartDrawer + AIChatWidget
│   ├── styles.css              <- btn-* / tag / section-* / input-field
│   ├── utils/format.ts         <- formatPrice(): the only money formatter
│   ├── components/             <- Navbar / Footer / ProductCard / CartDrawer / AIChatWidget
│   ├── pages/                  <- Home / Shop / Product / Cart / Checkout / Wishlist / Admin
│   ├── data/products.ts        <- single source of truth (TypeScript, not JSON)
│   ├── store/cartStore.ts      <- cart + wishlist, both persisted
│   └── types/index.ts          <- Product / Category / CartItem / PromoCode
└── functions/
    ├── api/{products,checkout,assistant}.ts   <- edge functions
    └── node/stripe-webhook.ts                 <- node function
```

### Routes (all 7 required)

| Path | Page | Notes |
|------|------|-------|
| `/` | HomePage | |
| `/shop` | ShopPage | category tabs + filter + sort + grid/list |
| `/product/:id` | ProductPage | 404 state when not found |
| `/cart` | CartPage | full-page cart |
| `/checkout` | CheckoutPage | three steps |
| `/wishlist` | WishlistPage | persisted wishlist |
| `/admin` | AdminPage | mock dashboard |

---

## Stack

| Layer | Technology |
|-------|------------|
| Frontend | React 18 + TypeScript 5 + Vite 5 + Tailwind CSS 3 |
| Icons | lucide-react (line style, no emoji) |
| Animation | framer-motion |
| State | Zustand + `persist` |
| Routing | react-router-dom v6 |
| Fonts | Inter + Playfair Display, with Noto Sans SC / Noto Serif SC as the CJK fallback |
| API | Hono-style edge functions + node functions |
| Payment | Stripe (mock / live) |
| Deployment | EdgeOne Pages |

---

## Commands

```bash
# Scaffold (never deletes an existing directory — a re-run renames it to <slug>.bak-<timestamp>)
python scripts/scaffold_project.py "<one-line brief>" --output <dir> --brand "<Brand>"

# Quality gate
python scripts/validate_generated_project.py <project_dir> --lang en --currency CNY

# Verify the bundled template itself is still compliant
python scripts/validate_generated_project.py templates/base --template --lang en --currency CNY

# Remote image reachability (off by default; the local pool needs no network)
python scripts/validate_generated_project.py <project_dir> --check-images

# Repo hygiene: fail if any Chinese text sneaked into the skill
python scripts/check_skill_language.py
```

---

## Example prompts

> "Generate a streetwear storefront for a young brand, with new-arrivals and limited
> drops, a dark edgy look, and an AI stylist that helps you put an outfit together."

> "Build an indie creator shop selling templates, presets and ebooks, categorised,
> with a live-updating cart and mock checkout."

> "Make a SaaS product site with three pricing tiers, a feature comparison table and
> an AI sales assistant."

An English brief produces an English build (`lang="en"`); a Chinese brief produces a
Chinese build. Gate `L-01` verifies the language attribute.

---

## Images

The 16 bundled photos live in `templates/base/static/images/`. `vite.config.ts`
sets `static` as the Vite `publicDir`, so code references them as
`/images/<file>.jpg`.

**Local by default**: deterministic, offline-safe, unaffected by proxies. Gate
`I-01` verifies every local reference resolves. Reach for a remote URL only when
the domain has no match in the pool, verify it with `--check-images`, and record
the replacement.

---

## Customising

**Real AI concierge** — the replacement path is documented at the top of
`functions/api/assistant.ts`. Set `AI_API_BASE` / `AI_API_KEY` / `AI_MODEL`.
Keyword scenarios live in `mockAIResponse()` in `AIChatWidget.tsx` — keep them in
the **same language as the UI** (English for an `en` build, Chinese for `zh-CN`).

**Payment** — set `VITE_PAYMENT_MODE=stripe` and provide `STRIPE_SECRET_KEY` plus
`STRIPE_WEBHOOK_SECRET`.

**Currency** — change `CURRENCY_SYMBOL` (and the `toLocaleString` locale) in
`src/utils/format.ts` and `VITE_DEFAULT_CURRENCY` in `.env`, then run the gate with
`--currency USD`.

**New pages** — add to `src/pages/`, register the route in `App.tsx`, and extend
`REQUIRED_FILES` in the validator if the page must always exist.

---

## Notes

- The output is a **scaffold plus a clickable demo**: UI, flows and state are
  complete; payments, AI and order persistence are placeholders.
- Handoff notes must distinguish **scaffold-ready / demo-ready / production-ready**.
  Never call a demo production-ready.
- Each generation is an independent directory and **never modifies an existing
  project**.
- `src/data/products.ts` is the single product source; `products.json` is a
  forbidden leftover.
- All money goes through `formatPrice()`; a hardcoded currency symbol fails the gate.

---

## License

MIT
