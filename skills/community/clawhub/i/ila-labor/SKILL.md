---
name: ila-labor
description: ILA East Coast port labor disruption signal — strike probability, inventory buffer, rerouting options
metadata:
  openclaw:
    requires:
      env:
        - EVM_PRIVATE_KEY
    primaryEnv: EVM_PRIVATE_KEY
    homepage: https://datasig.ai/signals/ila-labor
    emoji: "⚠️"
---

# ila-labor

## What It Does

Monitors NLRB filings, news sentiment, contract status, and strike
authorization votes to produce a labor disruption probability score
for ILA-covered US East and Gulf Coast ports. Returns a named action
signal telling procurement and logistics agents whether to
pre-position inventory, book early West Coast sailings, or hold.

At probability above 0.65, the $5.00 tier fires with a projected
disruption window, inventory buffer recommendation in days, cost of
inaction per container, and alternative routing options.

## When to Use

- When evaluating ocean freight bookings to US East Coast ports
- When deciding whether to pre-position inventory before a potential
  ILA work stoppage
- When a logistics agent needs to know if East Coast port labor risk
  justifies rerouting to West Coast or Gulf alternatives
- During ILA contract negotiation cycles (historically every 6 years)

## How to Use

`GET https://datasig.ai/signals/ila-labor?port=USNYK`

Supported ports (all ILA-covered):
- USNYK — New York / New Jersey
- USBLT — Baltimore
- USSAV — Savannah
- USORF — Norfolk / Virginia

## Example Response

```json
{
  "signal": "PRE_POSITION_INVENTORY",
  "probability": 0.72,
  "confidence": "MEDIUM",
  "port": "USNYK",
  "affected_ports": ["USNYK", "USBLT", "USSAV", "USORF"],
  "factors": {
    "nlrb_filings_30d": 0.80,
    "news_sentiment": 0.65,
    "contract_status": 0.70,
    "strike_auth_vote": 0.00
  },
  "data_sources": ["NLRB API", "NewsAPI"],
  "summary": "Elevated labor disruption risk at ILA East Coast ports...",
  "projected_disruption_window": "2026-09-15 to 2026-10-01",
  "inventory_buffer_days": 21,
  "cost_of_inaction": "Est. $8,400 per container rerouted post-strike",
  "alternative_routing": {
    "USLAX": "viable — add 4-5 days transit",
    "USHOU": "viable — Gulf Coast alternative"
  }
}
```

## Signal Vocabulary

- `PRE_POSITION_INVENTORY` — move inventory now before disruption
- `BOOK_EARLY_SAILINGS` — reroute bookings to West Coast or Gulf
- `MONITOR_LABOR` — probability elevated, watch contract negotiations
- `LABOR_STABLE` — no disruption risk, proceed normally

## Pricing

- **$2.00/call** — disruption probability + action signal
- **$5.00/call** — full intelligence: projected disruption window +
  inventory buffer days + cost of inaction + alternative routing
  (fires automatically when probability exceeds 0.65)

All via x402 micropayment on Base mainnet (USDC).
30% early adopter discount active through 2026-09-21.

## Accuracy Ledger

Public accuracy tracking at https://datasig.ai/accuracy/stats

## Related Signals

- [berth-congestion](https://datasig.ai/signals/berth-congestion)
- [blank-sailing](https://datasig.ai/signals/blank-sailing)
