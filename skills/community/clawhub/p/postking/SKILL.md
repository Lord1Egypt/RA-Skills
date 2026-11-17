---
name: postking-getting-started
description: First-run flow for PostKing — authenticate, top up credits, onboard a brand from a URL, connect socials, and ship a first post.
license: MIT-0
compatibility: "Works with any MCP-compatible client connected to postking-mcp (local stdio or hosted at https://mcp.postking.app/mcp); the pking CLI is an optional fast path when a shell is available."
metadata:
  icon: https://raw.githubusercontent.com/bitsandtea/postking-skills/main/assets/icons/postking-getting-started.svg
  category: marketing
---

# Getting Started

The full zero-to-first-post path: connect, authenticate, fund the balance, onboard a brand from its website, connect socials, and ship a first scheduled post. This is the first skill to run for any new user or freshly-connected agent.

## When to Use

Use this as the very first skill for any new user or freshly-connected agent session: checking auth state, funding credits, onboarding the first brand, connecting social accounts, or shipping the first post. Also use it any time you hit `UNAUTHORIZED`, `INSUFFICIENT_CREDITS`, or `TRIAL_EXPIRED` from another skill and need to route back through auth/billing.

## When NOT to Use

Not for day-to-day content work once a brand is onboarded and funded — hand off to the `postking-social`/`postking` skill for calendar review, posts, blogs, and repurposing. Not for SEO, campaigns, competitor research, Reddit, or voice/quality passes — those are their own skills (`postking-seo`, `postking-storylines`, `postking-competitor-intel`, `postking-reddit`, `postking-brand-voice`).

## Minimal tool subset

This skill needs 17 tools out of PostKing's 200+, grouped by stage:

**Auth**
- `health` — no-auth status check; always call this first.
- `login_start`, `login_complete` — stdio device-flow authentication.

**Credits & billing**
- `get_credits` — check balance and free-tier status.
- `billing_list_packs` — list one-off credit packs.
- `billing_topup` — buy a pack.
- `billing_wallet` — check the unified credit balance.
- `billing_list_tiers` — list subscription tiers.
- `billing_subscribe` — start a subscription.

**Brand onboarding**
- `onboard_brand` — crawl a website, analyze audience, generate themes.
- `create_brand` — manual brand creation without a website crawl.
- `get_onboarding_status` — poll onboarding progress.
- `list_themes` — review generated content themes.

**Socials**
- `check_social_accounts` — see what's connected.
- `generate_connect_link` — get an OAuth link for a platform.

**First post**
- `generate_post` — draft post variations.
- `approve_post` — lock in a variation and schedule.

(`whoami` and `logout` are also available if you need to confirm identity or sign out, but aren't required for this flow.)

## Prerequisites

None — this is the first skill to run when connecting to PostKing.

## Pacing rules

This is a multi-stage flow. Obey these rules throughout:

1. **One stage per turn.** Run the current stage, present the result, then stop and wait for the user. Don't chain into the next stage in the same turn, even on success.
2. **Never reuse remembered values without confirmation.** Brand names, website URLs, social handles, theme choices, and post topics must be reconfirmed in the current conversation — don't pull them from prior sessions or long-term memory without surfacing the value and asking the user to confirm it.
3. **Fail loudly, never silently retry.** If a stage fails, stop, surface the error verbatim, and ask the user how to proceed.
4. **Zero brands means onboarding is required**, not optional — never skip ahead to other work without a brand.

## Procedure

### Step 1 — Check health first

Call `health`. This requires no authentication and tells you whether you're already logged in and what to do next. Always start here.

- **Remote/OAuth transport** (client connected to `https://mcp.postking.app` via an OAuth-aware host): `health` reports that authentication already happened at the connector. Do not call `login_start` — there's no in-session login step.
- **Local stdio transport**: `health` reports whether a token is stored. If not, continue to Step 2.

### Step 2 — Authenticate (stdio only)

Call `login_start`. It returns a URL and a short code and begins polling on its own — the tool call itself waits for the browser approval step and reports success or timeout; you don't need a separate confirmation turn.

Show the URL and code to the user verbatim (no paraphrasing or redaction) and tell them to open it and approve. Use `login_complete` only if your client's flow separates "start" from "poll" — most stdio clients handle both in one `login_start` call.

### Step 3 — Check credits

Call `get_credits` (`detail: "short"` for just the number, `"full"` for complete billing context).

- Healthy balance → continue to Step 5 (brand onboarding).
- `0`, or a later operation returns `INSUFFICIENT_CREDITS` → go to Step 4.

### Step 4 — Fund the balance

Ask the user once which they prefer: a one-off credit pack (agent-native default, instant off-session charge) or a subscription.

**One-off pack:**
1. `billing_list_packs` — SKUs `agent_4`/`agent_5`/`agent_25`/`agent_50` = $4/160cr, $5/220cr, $25/1200cr, $50/2600cr. The $5 pack covers a full demo run (a week of posts + SEO pipeline + a landing page). Show the options and let the user pick — don't guess.
2. `billing_topup({ packSku: "<chosen>" })`:
   - **`status: "paid"`** (common case, card on file) — instant off-session charge; response includes the new `balance`. Done immediately, do not poll.
   - **`checkoutUrl` returned** (no card on file) — present the URL, have the user complete Stripe Checkout, then poll `billing_wallet` every few seconds (cap ~5 minutes) until `credits` rises by the expected amount. Hosted Checkout sessions expire after ~30 minutes of inactivity — call `billing_topup` again for a fresh URL if that happens.

**Subscription:**
1. `billing_list_tiers` — GROWTH / PRO / ENTERPRISE. Ask which tier.
2. `billing_subscribe({ tier, interval })` (`interval: "month"` or `"year"`) — returns a `checkoutUrl`. Human-completion is the cleanest path: the user completes Checkout, the webhook provisions the account (grants credits, activates the plan).
3. Poll `billing_wallet` (or `get_credits`) every few seconds (cap ~5 minutes) until the subscription is active. The agent spends from the same unified `User.credits` pool either way — there's no separate agent wallet.

### Step 5 — Onboard a brand

- `get_onboarding_status` (or check via `health`/prior context) to see whether a brand already exists. If the user has zero brands, onboarding is required — don't proceed to anything else.
- If zero brands: ask the user two questions in the current conversation, one at a time if the UI supports it — (1) "What's the name of the brand?", (2) "What's the website URL to analyze?" If a plausible value exists from prior context, surface it as a suggestion only ("Last time you mentioned `acme.com` — still right, or different?") and wait for explicit confirmation. Never onboard silently on remembered values.
- `onboard_brand({ websiteUrl, name })` — crawls the site, analyzes audience, generates themes. Typically 30–90s.
- Or `create_brand({ name, description, tone, audience })` for manual setup without a crawl.
- `get_onboarding_status({ brandId })` — poll until analysis/theme generation finishes.
- `list_themes({ brandId })` — surface the generated themes (titles + one-line gloss each) and ask the user whether to keep, edit, or regenerate. Don't proceed silently.
- If the user already has ≥1 brand with none active, don't auto-onboard — ask which existing brand to use, or whether to add a new one.

**Deeper brand & theme editing (optional, outside this skill's minimal subset)** — `get_brand_info` for the full audience/positioning reveal, `edit_theme`/`delete_theme`/`generate_themes` for individual theme edits or regeneration. These are covered in the `postking` skill; use them there once onboarding is complete if the user wants finer control.

### Step 6 — Connect socials

- `check_social_accounts({ brandId })` — see what's connected.
- Ask the user which platform(s) they want connected before running anything — don't pick a default silently.
- `generate_connect_link({ brandId, platform })` — platforms: `linkedin`, `x`, `instagram`, `threads`, `facebook`. Show the URL and ask the user to confirm once they've completed OAuth.

### Step 7 — First post

- Confirm with the user which connected platform and which reviewed theme to use — don't pick silently.
- `generate_post({ brandId, platform, variations: 3 })` — show the variations.
- `approve_post({ postId, variation, schedule })` — locks it in.
- Hand off to the `postking` skill from here for calendar review and everything else day-to-day.

## CLI fast path

If a shell is available, the same flow via `pking` (npm package `postking-cli`):

```
pking me                                          # check auth
pking login-start                                 # print URL+code (device flow)
pking login-finish                                # complete after user approves
pking user credits                                # check balance
pking billing packs                                # list one-off packs
pking billing topup --pack <sku>                   # buy a pack
pking billing tiers                                # list subscription tiers
pking billing subscribe --tier <TIER> [--interval year]
pking onboard <websiteUrl> --name "<Name>"         # crawl + analyze + themes
pking brand create <name> --description "..." --tone "..." --audience "..."   # manual
pking brand themes list                            # review generated themes
pking social check                                 # see connected accounts
pking social connect-platform --platform <linkedin|x|instagram|threads|facebook>
pking posts generate --platform <p> --variations 3
pking posts approve <postId> --variation <n> --schedule <iso>
```

`pking login` (unsplit) blocks for up to 15 minutes polling — prefer `login-start` / `login-finish` in an agent context to avoid timeouts. For new users without an account yet, `pking register-start --email <email>` / `pking register-finish` runs the equivalent magic-link registration flow.

## Expected Output

- Confirmed auth state (already-authenticated via transport, or freshly authenticated via device flow).
- A funded balance — instant charge, completed Checkout, or active subscription.
- A populated brand profile (tone, audience, reviewed themes).
- 1+ connected social platform.
- At least one scheduled post.

## Pitfalls

- `INSUFFICIENT_CREDITS` (HTTP 402) — balance too low. Run Step 4.
- `RATE_LIMITED` — back off using the `retryAfter` value in the error envelope before retrying.
- `UNAUTHORIZED` — the stored token is invalid or expired. Re-run `login_start` (stdio) or reconnect the connector (remote/OAuth transport).
- `TRIAL_EXPIRED` — upgrade via the `checkoutUrl` returned in the error envelope.
- `VALIDATION` — invalid email format or a missing required field.
- `NOT_FOUND` on the onboarding/audience status — analysis hasn't finished yet; wait briefly and retry once on the user's say-so, don't loop silently.
- Stripe Checkout session expired (~30 min inactivity) — call `billing_topup` or `billing_subscribe` again for a fresh `checkoutUrl`.

## Verification

- `health` should return successfully and report the current auth state before doing anything else.
- After onboarding, `get_onboarding_status({ brandId })` should report a terminal (non-running) state.
- `check_social_accounts({ brandId })` should reflect the platform just connected.

## Next steps

Once authenticated, funded, and onboarded:

- `postking` — day-to-day content: posts, content weeks, repurposing, blogs, landing pages, visuals, trends.
- `postking-seo` — SEO / GEO from seed keywords to published articles.
- `postking-storylines` — multi-channel marketing campaigns (Storylines).
- `postking-competitor-intel` — discover, register, and analyze a brand's competitors.
