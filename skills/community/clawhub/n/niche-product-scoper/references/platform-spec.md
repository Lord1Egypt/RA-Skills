# Platform Specification Reference

Load this file ONLY when the user has confirmed their platform choice (Website or Mini Program).

## For Websites

| Element | Decision |
|---------|----------|
| Pages | Max 5 pages for MVP (landing, app, pricing, about, 404) |
| User auth | Email/password via Supabase, or OAuth (Google/GitHub) |
| Payment | Stripe for subscriptions, LemonSqueezy for digital products |
| Hosting | Vercel (recommended), Netlify, or Cloudflare Pages |
| Domain | Purchase via Cloudflare or Namecheap |
| SEO | Required if organic search is main channel. Include: meta tags, sitemap.xml, robots.txt |
| Mobile | Mobile-first responsive design (60%+ traffic will be mobile) |
| i18n | Chinese only for MVP. Add English only after PMF confirmed |

## For Mini Programs

| Element | Decision |
|---------|----------|
| Pages | Max 5 pages for MVP |
| User auth | wx.login (WeChat built-in auth) — always use this |
| Payment | WeChat Pay (requires merchant account setup) |
| Storage | WeChat Cloud Development for MVP (simplest), or Supabase via API |
| Share | Support forward-to-friend and share-to-moments |
| Template messages | Not in MVP (requires user interaction trigger) |
| Search keywords | Max 10 keywords. Use the opportunity-finder's top keywords |
| Category | Pick the least competitive relevant category in 微信小程序 分类 |

## Legal Requirements (Both Platforms)

- Privacy policy page (required for both)
- Terms of service page
- Data handling disclosure (especially for AI-powered features)
- Cookie consent (websites targeting EU users)
