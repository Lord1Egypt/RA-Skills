---
name: worldwide-pricing
description: >-
  Reprice an iOS app, in-app purchase, or subscription across all App Store
  territories using purchasing-power (PPP), Big Mac, or Spotify affordability
  indexes, or a straight conversion, through MetaRun. Trigger phrases:
  "reprice", "PPP pricing", "adjust prices by country", "make it affordable
  in India", "raise the price everywhere", "price my app worldwide".
metadata:
  openclaw:
    homepage: https://metarun.dev/agents
    primaryEnv: METARUN_TOKEN
    envVars:
      - name: METARUN_TOKEN
        required: false
        description: MetaRun personal access token (Settings, MCP). Not needed after `npx metarun login`, which stores it in ~/.metarun/config.json.
    requires:
      anyBins:
        - npx
---

# Worldwide pricing: one base price, 175 defensible local prices

You are repricing through MetaRun. The engine computes per-territory targets
from a base price and a strategy; you stage them through a preview, and
nothing touches Apple until the user confirms.

## Ground rules

- Tools run over MetaRun's MCP server or `npx metarun run <tool> '<json>'`.
  Fetch any schema you have not used this session: `npx metarun tools
  <tool-name> --json`. Never invent parameters.
- **A base price is a decision the user makes.** Never pick one for them, and
  never treat the current price as an implied answer: ask what base price
  (and which territory it is anchored in) before computing.
- Every write is a preview/apply pair with a `confirmToken`. Show the user
  the preview's numbers before applying.

## The mission

### 1. Read the current state

- `apple_list_apps` -> resolve the bundle id.
- App prices: `apple_get_app_pricing`. IAP detail: `apple_get_iap` (the list
  read `apple_list_iaps` does not carry per-territory prices). Subscriptions:
  `apple_list_subscription_groups` then `apple_get_subscription`.

### 2. Compute targets

- `pricing_compute_prices` runs the strategy engine: strategies `direct`,
  `ppp`, `bigmac`, `spotify`, `custom`; optional VAT handling and a minimum
  price floor; results snap to Apple's real price tiers. Reference data:
  `pricing_get_indexes`, `pricing_get_exchange_rates`.
- The result includes a `stagedInput` payload built for the matching preview
  tool. Use it as-is; do not reassemble territory rows by hand.
- Sanity-check the extremes with the user: name the cheapest and most
  expensive territories and any floored or unsnapped rows before staging.

### 3. Stage and apply

- Whole app: `apple_preview_set_app_price` (base price; Apple equalizes the
  rest) or `apple_preview_set_territory_prices` (explicit per-territory
  overrides, max 200 per call). Apply with the matching apply tool and the
  preview's confirmToken.
- IAPs: `apple_preview_set_iap_price` / `apple_apply_set_iap_price`.
- Subscriptions: `apple_preview_set_subscription_price`; note
  `preserveCurrentPrice` grandfathers existing subscribers, and Apple
  schedules live-subscription changes for the earliest allowed date
  (tomorrow) rather than instantly. Territories that already carry a
  scheduled change are SKIPPED with a warning; clear them first with
  `apple_preview_clear_scheduled_subscription_prices` if the user wants the
  new price everywhere.
- Exact price points for one territory: `apple_find_price_points`;
  equalization sets: `apple_get_price_equalizations`.

### 4. Report

Summarize what was applied: how many territories, raised vs lowered, and
that the change is in change history and revertible.

## Beyond this mission

Discover the wider surface (metadata, screenshots, releases, ASO) with
`npx metarun tools <filter>`.
