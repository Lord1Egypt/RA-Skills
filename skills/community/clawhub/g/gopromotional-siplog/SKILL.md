---
name: gopromotional-siplog
description: "Estimate a daily water goal and keep a simple hydration log (add drinks in ml, l, cl or oz; see progress, a 7-day history and streaks). Use when someone wants to track water intake, asks how much water to drink, or logs a drink."
license: MIT
metadata: {"openclaw": {"requires": {"bins": ["npx"]}, "homepage": "https://www.gopromotional.co.uk/branded-products/branded-water-bottles"}}
---

# Siplog

## When to use

- "How much water should I drink? I'm 70 kg and run for 30 minutes."
- "Log 500 ml of water." / "I just had a 33cl bottle."
- "How am I doing on water today?" / "Show my hydration this week."

## Commands

Run with Node 18+ (no install needed). Add `--json` for machine-readable output.

```bash
npx -y gopromotional-siplog goal --weight 70 --activity 30 --hot
npx -y gopromotional-siplog add 500ml
npx -y gopromotional-siplog status
npx -y gopromotional-siplog week
npx -y gopromotional-siplog undo
npx -y gopromotional-siplog set-goal 2500
```

Python alternative: `pipx run gopromotional-siplog status` (same commands and the same log file).

## Notes

- The log lives in `~/.gopromotional-siplog.json` (override with `--file` or `GOPROMOTIONAL_SIPLOG_FILE`).
- The goal is weight x 33 ml + 12 ml per active minute (+500 ml when hot), rounded to 50 ml. It is a general guide, not medical advice.

## Links

- Website: [branded water bottles for event marketing](https://www.gopromotional.co.uk/branded-products/branded-water-bottles)
- Source code: [https://github.com/nbkdevs/GoPromotional](https://github.com/nbkdevs/GoPromotional/tree/main/packages/water-bottles)
- Licence: MIT
