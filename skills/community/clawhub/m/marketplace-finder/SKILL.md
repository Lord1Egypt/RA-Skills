---
name: marketplace-finder
description: Search Facebook Marketplace without a Facebook account or API key. Find listings by keyword near any location, filter by price, condition and date, open a listing for its photos, description and seller details, and look up Marketplace locations. Use this skill for deal hunting, resale price research, finding local items, or monitoring Marketplace for a product.
---

# Marketplace Finder: Facebook Marketplace Search

![Marketplace Finder: Facebook Marketplace Search](https://raw.githubusercontent.com/ClawLink-HQ/clawhub-assets/main/marketplace-finder.gif)

Search Facebook Marketplace from chat: listings near any city, filtered by price and condition, and the full details of any listing.

No Facebook account, no API key, no app to connect. Calls are paid from ClawLink credit, most for a fraction of a cent, and every new account starts with **$0.50 free**. Powered by [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=marketplace-finder).

### Setup in 3 Steps

| Step 1: Install | Step 2: Pair | Step 3: Ask |
|:---:|:---:|:---:|
| ![Install](https://raw.githubusercontent.com/ClawLink-HQ/clawhub-assets/main/setup-install.gif) | ![Pair](https://raw.githubusercontent.com/ClawLink-HQ/clawhub-assets/main/setup-pair.gif) | ![Ask](https://raw.githubusercontent.com/ClawLink-HQ/clawhub-assets/main/marketplace-finder.gif) |
| Install the ClawLink plugin in OpenClaw | Sign in and approve the device once | Ask in plain English; no app to connect |

## What You Can Ask

- “Find road bikes for sale on Facebook Marketplace in San Francisco”
- “What do used iPhone 15s sell for near Chicago?”
- “Show me sofas under $300 listed this week near Austin”
- “Open this Marketplace listing”

## When to Use This Skill

Use it when the user wants Facebook Marketplace listings or prices.

Do not use it for the user's own private accounts or for anything that posts, sends or changes data: these tools only read public information.

## How It Works

```
┌─────────────────┐     ┌──────────────┐     ┌──────────────────┐
│   OpenClaw      │────▶│   ClawLink   │────▶│ FB Marketplace   │
│   (User Chat)   │     │ (data tools) │     │ (public data)    │
└─────────────────┘     └──────────────┘     └──────────────────┘
         │                       │                       │
         │  1. Install plugin    │                       │
         │  2. Pair device once  │                       │
         │  3. Ask a question    │                       │
         │                       │  4. Fetch + trim      │
         │                       │  5. Charge credit     │
         ▼                       ▼                       ▼
   ┌──────────┐           ┌──────────┐           ┌──────────┐
   │  Answer  │           │  Credit  │           │ Results  │
   │ in chat  │           │ ($0.50)  │           │ as JSON  │
   └──────────┘           └──────────┘           └──────────┘
```

ClawLink holds the data-provider accounts. The user never pastes a key, and nothing is installed beyond the plugin.

## Install

Install the ClawLink plugin from ClawHub when the user asks for it:

```bash
openclaw plugins install clawhub:clawlink-plugin
```

The install applies to the running Gateway: do not restart it. The ClawLink tools appear on your next turn, so end this turn and tell the user: "ClawLink is installed. Reply ok and I will give you your pairing link." On the next turn call `clawlink_begin_pairing`, give the user the link, and after they approve call `clawlink_get_pairing_status`. Pairing happens once; after that every tool below works with no further setup.

## Tool Reference

Prices are what ClawLink charges per call, from the user's credit. The tool's own description (via `clawlink_describe_tool`) always shows the current price.

### Marketplace

| Tool | What it returns | Price |
|------|-----------------|-------|
| `facebookdata_marketplace_search` | Search Facebook Marketplace listings near a point | $0.00282 |
| `facebookdata_marketplace_item` | One Facebook Marketplace listing by id or URL: price, description, condition, location, seller, photos | $0.00282 |
| `facebookdata_marketplace_location_search` | Find a place for marketplace_search: a city or area name to latitude and longitude | $0.00282 |

## Recipes

### Price a used item

1. `facebookdata_marketplace_location_search` for the city's coordinates if you do not know them.
2. `facebookdata_marketplace_search` near them.
3. Drop outliers and report the typical price range.

## Code Examples

### Search near a city

```bash
clawlink_call_tool --tool "facebookdata_marketplace_search" \
  --params '{"query": "road bike", "lat": 37.7749, "lng": -122.4194, "radius_km": 40}'
```

### One listing

```bash
clawlink_call_tool --tool "facebookdata_marketplace_item" \
  --params '{"url": "https://www.facebook.com/marketplace/item/LISTING_ID"}'
```

## Discovery Workflow

1. Call `clawlink_search_tools` with a short query (for example `marketplace`); public-data tools show as connected for every user.
2. Call `clawlink_describe_tool` before the first call of a tool: it returns the parameters, defaults and price.
3. Treat the live catalog as the source of truth. If a tool named here is missing, say so; do not invent results.

## Execution Workflow

```
┌───────────────────────────────────────────────────────────┐
│  READ-ONLY, PAID PER CALL                                │
│  search → describe → call → summarise for the user       │
│                                                          │
│  Ask before: loops over many items, or a call that costs │
│  more than a few cents (the price is in the description) │
└───────────────────────────────────────────────────────────┘
```

1. Every tool here only reads public data; nothing is posted or changed.
2. Each call costs credit. Before looping over more than about ten items, or before a call priced above a few cents, tell the user what it will cost and ask.
3. A failed call is refunded automatically. Read the error's `hint`: it says what to change. Do not retry the same arguments unchanged.

## Notes

- Search needs `lat` and `lng`; `facebookdata_marketplace_location_search` finds them from a place name.
- Listings change fast; say when you checked.
- Never arrange payment or contact sellers on the user's behalf.

## Error Handling

| Status / Error | Meaning |
|----------------|---------|
| No listings | Widen `radius_km` or simplify the query. |
| `credit_exhausted` | The user's ClawLink credit is used up. Tell them to top up at https://claw-link.dev/dashboard/billing?utm_source=clawhub&utm_medium=referral&utm_content=marketplace-finder; do not retry. |
| `data_provider_unavailable` | ClawLink's data provider is down. Nothing was charged. Try again later. |
| `no_result` | The provider found nothing for these arguments. Nothing was charged. |
| `invalid_arguments` | A parameter is missing or malformed. Call `clawlink_describe_tool` and fix it. |

## Troubleshooting

### Tools not visible after install

1. The tools appear on the turn after the install, not in the same turn.
2. If they still do not appear, the OpenClaw tool profile may hide plugin tools. This is a config change for the OpenClaw owner; do not change the config yourself. Tell the user: "Your OpenClaw tool profile hides plugin tools. In the Control UI (or `~/.openclaw/openclaw.json`), add `clawlink-plugin` to `tools.alsoAllow`, then ask me again."
3. On OpenClaw versions before 2.0, the tool list can load only in a new chat: tell the user to send `/new` and ask again.

### A tool keeps failing with correct input

Report it with `clawlink_report_issue` (or `clawlink_call_tool --tool "CLAWLINK_REPORT_ISSUE"`) instead of retrying. Reports are free and reach the ClawLink team.

## Resources


- [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=marketplace-finder)
- [ClawLink pricing](https://claw-link.dev/pricing?utm_source=clawhub&utm_medium=referral&utm_content=marketplace-finder)
- [ClawLink docs: OpenClaw](https://docs.claw-link.dev/openclaw)
- [Verify the plugin](https://claw-link.dev/verify)

## Related Skills

- [Price Hawk](https://clawhub.ai/hith3sh/skills/price-hawk)
- [Event Finder](https://clawhub.ai/hith3sh/skills/event-finder)

---

**Powered by [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=marketplace-finder)**: connect OpenClaw to 1,000+ apps and public data, with no API keys.
