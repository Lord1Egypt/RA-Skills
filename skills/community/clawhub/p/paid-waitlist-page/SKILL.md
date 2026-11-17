---
name: paid-waitlist-page
description: Spin up a hosted waitlist / landing / pre-order page that actually persists signups to a managed database and can take a payment — not just emit HTML. Use when the user wants a waitlist page, landing page, coming-soon page, pre-order or paywall, an email-capture form that saves to a database, a hosted signup form that persists, or "collect emails and charge for early access". One command — live URL + DB behind the form + optional checkout.
license: MIT
compatibility: "Requires the settlemesh CLI (npm i -g settlemesh) and a SETTLE_API_KEY; makes authenticated, metered calls to the SettleMesh platform over the network."
metadata:
  openclaw:
    requires:
      bins: ["settlemesh"]
      env: ["SETTLE_API_KEY"]
    primaryEnv: "SETTLE_API_KEY"
---

# paid-waitlist-page — a signup page that persists and can charge

> **Session (auto — never dead-stop on auth):** before your first `settlemesh` call, run `settlemesh whoami`; if it errors and `SETTLE_API_KEY` is unset, run `settlemesh login` yourself — it opens the browser for a **one-time** human approval, polls until approved, and caches the session. Do NOT stop to ask the user to "log in manually" — drive it. Keep an explicit human confirmation only for spending / credential-lending actions (fail-closed).

Every "landing page generator" hands you an `index.html` and stops — leaving you
the three hard parts: **persist** the signups somewhere, **host** the page on a
real URL, and **charge** for pre-orders. A prompt-only skill can't run a database,
keep the page alive, or move money. **SettleMesh closes all three in one deploy.**

This is a specialization of `ship-paid-app` (the deploy engine) + `charge-my-users`
(end-user billing). Read those for the general case; this is the waitlist recipe.

## Recipe

1. **Generate the page** — a static or Node/Python page with a signup `<form>` that
   POSTs `email` (and whatever else) to your handler. Point the write at the
   managed DB (the runtime DB connection is injected by `--full-stack`).
2. **Deploy full-stack** — creates the managed database + SettleMesh auth + a
   runtime API key, and returns a live URL. The form now persists.
3. **Optionally gate with a price** — add a flat pre-order/paywall checkout.

```bash
# Setup once:
npm install -g settlemesh@latest && settlemesh login   # or SETTLE_API_KEY=sk-settle-...

# Persist-only waitlist (form writes to the managed DB):
settlemesh deploy ./waitlist --name waitlist --full-stack --wait --json

# Paid pre-order / paywall (flat SettleMesh checkout in front of access):
settlemesh deploy ./waitlist --name waitlist --full-stack \
  --with-payment --payment-price-credits 50 --wait --json
```

**Read the live URL from the deploy JSON** (don't guess it). The page is reachable
at `<name>.run.settlemesh.io`; no domain to buy or configure.

## Two ways to monetize

- **`--with-payment --payment-price-credits N`** — one flat SettleMesh checkout
  price for access / the pre-order (minimum 50 credits). Best for "pay $X to
  reserve / unlock early access". This is a paywall, not per-use metering.
- **`X-Settle-Payer` (the `charge-my-users` skill)** — metered, per-action billing
  of the end user instead of a flat gate. Use this when each action (a generation,
  a lookup, a download) should bill the visitor rather than charging once at the door.

## Inspect the stored signups

The full-stack DB is a real managed database — query it with `settlemesh db`
(each command takes the app's `<project-id>` from the deploy output):

```bash
settlemesh db migrate <project-id> --sql \
  "create table if not exists signups(id serial primary key, email text, created_at timestamptz default now())"
settlemesh db query <project-id> --sql "select count(*), max(created_at) from signups" --json
settlemesh db get <project-id> --json          # DB metadata / connection info
```

## Verify it's live

```bash
settlemesh deploy status <app-id>     # build/deploy state
settlemesh deploy url <app-id>        # re-fetch the public URL
```

## Notes

- `--full-stack` = DB + auth + runtime key; the form's write path uses the injected
  DB connection, so signups survive restarts — nothing to wire manually.
- Everything is billed in **Aev** (1 USD = 100 Aev). Deploy and `--with-payment`
  are confirm-gated; check balance with `settlemesh aev balance`.
