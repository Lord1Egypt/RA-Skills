# Tech Stack Options Reference

Load this file ONLY when the user needs help choosing between specific technologies.

## Website Stacks

### Stack A: Next.js Full Stack (Recommended Default)

| Layer | Technology | Why |
|-------|-----------|-----|
| Framework | Next.js 14+ (App Router) | SSR, API routes, great DX |
| Styling | Tailwind CSS | Rapid prototyping, no context switching |
| Components | Shadcn/UI (optional) | Pre-built accessible components |
| Database | Supabase (PostgreSQL) | Auth + DB + storage in one |
| Auth | Supabase Auth | Email, OAuth, magic links |
| Payment | Stripe | Industry standard, good docs |
| Hosting | Vercel | Zero-config deploys, edge functions |
| AI | OpenAI API (via API route) | Server-side proxy keeps key safe |

### Stack B: Nuxt Full Stack (Vue developers)

| Layer | Technology | Why |
|-------|-----------|-----|
| Framework | Nuxt 3 | SSR, auto-imports, great for Vue devs |
| Styling | Tailwind CSS | Same as Stack A |
| Database | Supabase | Same as Stack A |
| Auth | Supabase Auth | Same as Stack A |
| Payment | Stripe or LemonSqueezy | Same as Stack A |
| Hosting | Vercel or Cloudflare Pages | Both support Nuxt |

### Stack C: Static + Backend (Simplest)

| Layer | Technology | Why |
|-------|-----------|-----|
| Framework | Vanilla HTML + Alpine.js or HTMX | Zero build step |
| Styling | Tailwind CSS (CDN) | No build needed |
| Backend | Supabase | Handles everything |
| Hosting | Cloudflare Pages or GitHub Pages | Free, fast |

## Mini Program Stacks

### Stack D: Taro (React developers)

| Layer | Technology | Why |
|-------|-----------|-----|
| Framework | Taro 3 (React) | Write React, compile to WeChat |
| UI | NutUI | JD's component library, Taro-native |
| State | Zustand | Simple, no boilerplate |
| Backend | WeChat Cloud or Supabase | Cloud is simpler for MVP |

### Stack E: UniApp (Vue developers)

| Layer | Technology | Why |
|-------|-----------|-----|
| Framework | UniApp (Vue 3) | Cross-platform from Vue |
| UI | uView | Popular UniApp component library |
| State | Pinia | Vue 3 standard |
| Backend | WeChat Cloud or Supabase | Same as Stack D |

## Database Schema Patterns

### Pattern 1: User + Credits (usage-based products)

```
users: id, email, plan (free/pro), credits_remaining, created_at
credits_log: id, user_id, amount, action, created_at
```

### Pattern 2: User + Content (creation tools)

```
users: id, email, plan, created_at
projects: id, user_id, title, data (JSON), created_at, updated_at
```

### Pattern 3: User + Subscriptions (SaaS)

```
users: id, email, created_at
subscriptions: id, user_id, plan, status, stripe_customer_id, current_period_end
```
