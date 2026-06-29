---
name: government-contracts-federal-awards
description: Government contract & federal award data for AI agents — find US federal contract awards by company or keyword, see who just won government contracts, and surface GovCon sales-intent signals. Use to research government contractors, find procurement opportunities, qualify cash-flush B2G leads, or track competitors' federal wins. Pay-per-call in USDC via x402 — no API key, no signup.
tags: [government-contracts, federal-awards, govcon, procurement, rfp, usaspending, contractors, sales-intent, b2g, public-sector]
author: gocreative
version: 1.0.0
license: MIT
---

# Government Contracts & Federal Awards

> Who's winning US federal contracts — by company or keyword. One install, pay-per-call, no API key.

## When to use this
- Research a **government contractor** or a company's federal awards.
- Find **procurement / contract opportunities** by topic.
- Surface **sales-intent signals** — companies that just won a contract (fresh budget).

## How it's paid (x402)
Plain HTTPS GET. First call returns HTTP 402; your OpenClaw wallet auto-pays the USDC fee (Base) and retries → JSON.

## Tools
| Call | What you get | Price |
|---|---|---|
| `GET https://api.gocreativeai.com/v1/finance/gov-awards/{company}` | Largest US federal contract awards to a recipient | ~$0.05 |
| `GET https://api.gocreativeai.com/v1/leads/federal-contracts/{keyword}` | Recent federal awards by keyword (recipient, amount) | ~$0.05 |
| `GET https://api.gocreativeai.com/v1/signal/govcon-radar/{keyword}` | Companies that **just won** federal contracts — sales-intent | ~$0.05 |

## Why GoCreative
Live US federal procurement data (USAspending), pay-per-call, no signup — the **only native govcon feed for agents**.

*Provider: GoCreative — Agent Compliance & Data API · https://api.gocreativeai.com*
