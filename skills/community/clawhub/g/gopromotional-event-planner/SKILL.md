---
name: gopromotional-event-planner
description: "Plan an event backwards from its date: countdown, a 12-step planning timeline, giveaway quantities for a stand, and the last safe date to order printed or branded merchandise. Use when someone asks how long until an event, what to do when, how many giveaways to order, or when to place a merch order."
license: MIT
metadata: {"openclaw": {"requires": {"bins": ["npx"]}, "homepage": "https://www.gopromotional.co.uk/"}}
---

# Event Planner

## When to use

- "How many days until our conference on 3 December?"
- "Give me a planning timeline for an event on 2026-12-03."
- "How many giveaways for 500 visitors over 2 days?"
- "When is the latest we can order branded merchandise?"

## Commands

Run with Node 18+ (no install needed). Add `--json` for machine-readable output.

```bash
npx -y gopromotional-event-planner countdown 2026-12-03
npx -y gopromotional-event-planner timeline 2026-12-03
npx -y gopromotional-event-planner giveaways --attendees 500 --days 2
npx -y gopromotional-event-planner order-by 2026-12-03 --production 10 --delivery 3
```

Python alternative: `pipx run gopromotional-event-planner countdown 2026-12-03` (same commands).

## Notes

- Giveaways = attendees x days x uptake (default 0.6) x per-person, plus a 10% buffer, rounded up.
- Order-by counts back working days (Mon-Fri) for production, delivery and a safety margin.
- `--today YYYY-MM-DD` fixes the reference date, which is useful for reproducible answers.

## Links

- Website: [branded merchandise](https://www.gopromotional.co.uk/)
- Source code: [https://github.com/nbkdevs/GoPromotional](https://github.com/nbkdevs/GoPromotional/tree/main/packages/homepage)
- Licence: MIT
