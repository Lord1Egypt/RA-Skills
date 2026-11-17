---
name: gopromotional-packlist
description: "Create packing checklists from templates (work day, travel, trade show, gym) with per-night quantities, save them as Markdown, tick items off and see what is left. Use when someone is packing for a trip, an exhibition or the gym, or asks what they have forgotten."
license: MIT
metadata: {"openclaw": {"requires": {"bins": ["npx"]}, "homepage": "https://www.gopromotional.co.uk/branded-products/tote-bags"}}
---

# Packlist

## When to use

- "Make me a packing list for 3 nights away."
- "What do I need for a trade show stand?"
- "Tick off the passport." / "What's still left to pack?"

## Commands

Run with Node 18+ (no install needed). Add `--json` for machine-readable output.

```bash
npx -y gopromotional-packlist templates
npx -y gopromotional-packlist new --template travel --nights 3 --extra "Umbrella" --title "Lisbon" --out lisbon.md
npx -y gopromotional-packlist check lisbon.md passport
npx -y gopromotional-packlist add lisbon.md "Sunglasses"
npx -y gopromotional-packlist status lisbon.md
```

Python alternative: `pipx run gopromotional-packlist status lisbon.md` (same commands).

## Notes

- Lists are plain Markdown checkboxes (`- [ ] 4 × T-shirts`), so they can be edited by hand.
- Per-night items get nights + 1 (one spare). Templates can be combined: `--template travel,work-day`.
- Partial names work for `check` when they match exactly one item.

## Links

- Website: [branded tote bags for event marketing](https://www.gopromotional.co.uk/branded-products/tote-bags)
- Source code: [https://github.com/nbkdevs/GoPromotional](https://github.com/nbkdevs/GoPromotional/tree/main/packages/tote-bags)
- Licence: MIT
