---
name: gopromotional-mugday
description: "Track coffee and caffeine: typical caffeine per drink, today's total against a 400 mg (or 200 mg in pregnancy) limit, how much is still in your system, when it drops low enough for sleep, and reusable vs disposable cups. Use when someone logs a coffee or asks about caffeine intake."
license: MIT
metadata: {"openclaw": {"requires": {"bins": ["npx"]}, "homepage": "https://www.gopromotional.co.uk/branded-products/travel-mugs"}}
---

# Mugday

## When to use

- "Log a flat white in my travel mug."
- "How much caffeine have I had today?"
- "If I have a coffee at 4pm, when can I sleep?"
- "How many disposable cups did I use this week?"

## Commands

Run with Node 18+ (no install needed). Add `--json` for machine-readable output.

```bash
npx -y gopromotional-mugday drinks
npx -y gopromotional-mugday add flat-white --reusable
npx -y gopromotional-mugday add "office coffee" --mg 90 --time 2026-10-19T09:00
npx -y gopromotional-mugday today
npx -y gopromotional-mugday in-system
npx -y gopromotional-mugday sleep-ready --threshold 50
npx -y gopromotional-mugday cups
```

Python alternative: `pipx run gopromotional-mugday today` (same commands and the same log file).

## Notes

- The log lives in `~/.gopromotional-mugday.json` (override with `--file` or `GOPROMOTIONAL_MUGDAY_FILE`).
- Caffeine values are typical figures and real drinks vary. Uses a 5-hour half-life. Not medical advice.

## Links

- Website: [branded travel mugs for event marketing](https://www.gopromotional.co.uk/branded-products/travel-mugs)
- Source code: [https://github.com/nbkdevs/GoPromotional](https://github.com/nbkdevs/GoPromotional/tree/main/packages/travel-mugs)
- Licence: MIT
