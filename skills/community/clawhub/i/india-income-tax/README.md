# india-income-tax 🇮🇳

An AI agent skill that tells you exactly how much income tax you'll pay in India — **new vs old regime, side by side** — for Tax Year 2026-27 (the new Income-tax Act, 2025).

Works with **OpenClaw, Claude Code, Codex, Cursor** and any agent that reads `SKILL.md`.

## What your agent can now answer
- "How much tax on ₹18 lakh salary?"
- "Old or new regime — which saves me more?"
- "How much more do I need in 80C/NPS for the old regime to win?"
- "What will my monthly TDS be?"

## What it handles
- New regime slabs, ₹75,000 standard deduction, ₹60,000 rebate up to ₹12L with marginal relief
- Old regime slabs by age (below 60 / 60–79 / 80+), ₹12,500 rebate
- HRA exemption (incl. the 8 cities now at 50%), 80C, 80CCD(1B), employer NPS, 80D, home-loan interest, professional tax
- Surcharge with marginal relief, 4% cess
- **Break-even deductions** and monthly TDS estimate

Exact arithmetic is done by a tested Python script (no network, no dependencies) — the agent never guesses the numbers.

## Install
```bash
openclaw skills install india-income-tax      # OpenClaw
# or copy this folder into ~/.claude/skills/   # Claude Code
```

## Try it directly
```bash
python3 scripts/tax.py '{"salary": 1800000, "age": 30, "sec_80c": 150000}'
python3 tests/test_tax.py
```

## Not covered
Capital gains at special rates, business/presumptive income, non-residents, HUFs. Estimates only — confirm on incometax.gov.in or with a CA.
