---
name: metered-data-fetch
description: Call real PAID data APIs — paid web search / scrape / SEO / SERP / finance data for agents, no API key, no BYOK, metered per-call, cost quote up front, first call free. Use when the agent needs live web search, page scraping, SEO/SERP rankings, stock/market data, or an LLM, but you do NOT want to sign up for a separate data-API vendor, hold its key, and eat an opaque monthly bill — one SettleMesh key covers them all, each call quoted and metered in Aev.
license: MIT
compatibility: "Requires the settlemesh CLI (npm i -g settlemesh) and a SETTLE_API_KEY; makes authenticated, metered calls to the SettleMesh platform over the network."
metadata:
  openclaw:
    requires:
      bins: ["settlemesh"]
      env: ["SETTLE_API_KEY"]
    primaryEnv: "SETTLE_API_KEY"
---

# metered-data-fetch — paid data APIs, one key, quote before every call

> **Session (auto — never dead-stop on auth):** before your first `settlemesh` call, run `settlemesh whoami`; if it errors and `SETTLE_API_KEY` is unset, run `settlemesh login` yourself — it opens the browser for a **one-time** human approval, polls until approved, and caches the session. Do NOT stop to ask the user to "log in manually" — drive it. Keep an explicit human confirmation only for spending / credential-lending actions (fail-closed).

Every "give your agent web search / scraping / SEO data" skill ends the same way:
*"get an API key from each data vendor and paste it here."* Now you own an
account per vendor, a key in an env file, and a bill you can't see until the invoice lands.
**SettleMesh replaces all of them with one key and a quote before every call.** You
search a single catalog, read the exact Aev a call will cost, then run it — metered
per-call, no provider signup, no BYOK.

A prompt-only skill can't do this: it can only wrap *a key you already own*, so it
can't quote a price, can't meter per-call, and can't front you a free first try.
Here **the bill follows the work** — quote up front, per-capability metering, and a
free first call to every capability.

## Setup (once)

1. `npm install -g settlemesh@latest`
2. `settlemesh login` (a human approves once in the browser) — or set `SETTLE_API_KEY=sk-settle-...` for headless/CI.

## Discover → inspect → quote → call

Never memorize provider endpoints. **Search the catalog for the task, read the
tool's input schema, quote the exact call, then call it.**

```bash
# 1. Discover the right tool by task (not by provider name):
settlemesh search "web search" --json
settlemesh search "SEO SERP" --json          # SERP/rankings capability id — DISCOVER it, don't hardcode
settlemesh capabilities search "stock price" --json

# 2. Inspect the contract before you spend:
settlemesh tool show web.search --json
settlemesh tool schema web.search            # exact input fields

# 3. Quote — read-only cost ceiling in Aev, no hold, no charge:
settlemesh quote web.search --input '{"q":"SettleMesh"}' --json

# 4. Call it:
settlemesh tool call web.search --input '{"q":"SettleMesh"}' --json
```

Add `--confirm` for costly or side-effecting calls and `--wait` to poll an async job:

```bash
settlemesh tool call web.scrape --input '{"url":"https://example.com"}' --confirm --json
```

Real capability families: **web search + scrape**, **finance/market data**
(`finance.stocks.search` / `.quote` / `.daily`), **SEO/SERP** (DataForSEO-backed —
the id can vary, so find it with `settlemesh search "serp" --json`, don't hardcode),
and **LLMs** (`llm.chat`). One key, one unit, one catalog.

## Notes

- **First call to each official capability is FREE** — no card, and refunded if it
  fails — so an agent can try many distinct data APIs before funding anything. Only
  repeat calls draw down your balance.
- The exact Aev billed is on the **`X-Settle-Charged-Aev`** response header (HTTP
  path); the CLI prints the charge. A failed call never charges you — retries are safe.
- Everything is billed in **Aev** (1 USD = 100 Aev). Check balance with
  `settlemesh aev balance`; itemized charges are in `settlemesh aev ledger --limit 5`.
- **The edge:** a quote before every call, first-call-free per capability, and being
  able to **stack these paid calls directly onto a deployed, end-user-paying app** —
  see `charge-my-users` to make your users' wallets pay for the data your app fetches,
  with your markup.
