# Deployment

Companion to `SKILL.md`. Read this when taking a generated store to EdgeOne Pages.

## Target

Primary target: **EdgeOne Pages** (static hosting + edge functions + Node functions).

## Build assumptions

- Frontend: `vite build` -> `dist/`
- `static/` is the Vite `publicDir`, so `/images/*.jpg` end up in `dist/images/`
- Edge handlers: `functions/api/`
- Node handler: `functions/node/`
- Build command is `tsc --noEmit && vite build` — a type error fails the deploy,
  which is intentional

## Environment variables

| Variable | Purpose | Default in `.env.example` |
|---|---|---|
| `VITE_SITE_NAME` | Display name | generated site name |
| `VITE_BRAND_NAME` | Brand name | generated brand |
| `VITE_DEFAULT_CURRENCY` | Market currency | `CNY` |
| `VITE_PAYMENT_MODE` | `mock` or `stripe` | `mock` |
| `STRIPE_SECRET_KEY` | Stripe server key | empty |
| `STRIPE_WEBHOOK_SECRET` | Webhook signature secret | empty |
| `AI_API_BASE` / `AI_API_KEY` / `AI_MODEL` | AI concierge provider | empty / empty / `deepseek-chat` |

`CURRENCY_SYMBOL` in `src/utils/format.ts` must agree with
`VITE_DEFAULT_CURRENCY` — the quality gate checks the source, not the env file.

## Local workflow

1. `npm install`
2. `npm run dev` — confirm all 7 routes render
3. Run the quality gate:
   `python <skill>/scripts/validate_generated_project.py <project_dir> --lang zh-CN --currency CNY`
4. `npm run build` — must exit 0
5. `npm run preview` — smoke-test the production bundle

## Production workflow

1. Set the environment variables in EdgeOne Pages
2. Switch `VITE_PAYMENT_MODE=stripe`
3. Configure the webhook endpoint and copy its secret into `STRIPE_WEBHOOK_SECRET`
4. Deploy frontend + function handlers
5. Verify the hosted checkout redirect
6. Send a test webhook and verify receipt
7. Verify order state

## Deployment checklist

- [ ] Quality gate exits 0
- [ ] `npm run build` exits 0
- [ ] Homepage renders
- [ ] Products load
- [ ] Cart updates and persists across refresh
- [ ] Wishlist persists across refresh
- [ ] Checkout reaches the review step and only then clears the cart
- [ ] `/product/:id` works on a hard refresh (SPA fallback configured)
- [ ] Assistant endpoint responds
- [ ] Webhook endpoint exists and rejects unsigned payloads
- [ ] Admin page reachable
- [ ] Environment placeholders replaced with real values

## Reporting

Handoff notes must always separate three states explicitly:

- **scaffold-ready** — structure and conventions in place
- **demo-ready** — runs and is clickable end to end with mock data
- **production-ready** — real payments, real persistence, real AI

Never describe a demo-ready build as production-ready.
