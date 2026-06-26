---
name: polymarket-politics-random-1u
description: Build and run a Polymarket politics-market trading skill with the AION SDK. Use when the user wants to search active political markets on Polymarket, randomly choose one market, and place a 1 USD trade through Aionmarket using an API key and optionally a wallet private key for self-custody live trading.
metadata:
  author: "GitHub Copilot"
  version: "1.0.0"
  displayName: "Polymarket Politics Random 1U"
  difficulty: "intermediate"
---

# Polymarket Politics Random 1U

> **This is a template.** The default signal is intentionally simple: search active politics markets, pick one at random, and buy 1 USD of YES. Remix the market filter, sizing rule, side selection, or risk checks while keeping the AION plumbing intact.

Use this skill when the user wants a minimal AION SDK trading template for Polymarket politics markets.

## What This Skill Does

- Uses the documented AION SDK pattern from the building-skills guide.
- Searches active Polymarket markets with politics-related keywords.
- Filters to politics-style markets and randomly selects one candidate.
- Checks market context before trading.
- Defaults to dry-run mode.
- Places a live 1 USD trade only when the operator explicitly enables live execution.

## Inputs To Request From The User

Ask the user for these secrets or environment values before live trading:

1. `AION_API_KEY` for authenticated AION SDK access.
2. `WALLET_PRIVATE_KEY` if the user wants self-custody live trading rather than a managed wallet setup.
3. Optional `WALLET_ADDRESS` if the operator wants personalized context checks.

Do not write secrets into repository files.

## How It Works

1. Initialize the SDK client with the AION API key.
2. Search markets with politics-related queries such as `politics`, `election`, `president`, and `senate`.
3. Keep only active politics candidates.
4. Randomly choose one market.
5. Call market context before trading and skip on warnings.
6. Default to dry-run unless `--live` or `RUN_LIVE=true` is provided.
7. For live execution, submit a 1 USD YES trade with `source` and `skill_slug` attached.

## Files

- [clawhub.json](./clawhub.json)
- [politics_random_1u.py](./politics_random_1u.py)

## Run Examples

Dry-run:

```bash
python politics_random_1u.py
```

Live run:

```bash
python politics_random_1u.py --live
```

## Safety Rules

- Always default to dry-run.
- Always include `source`, `skill_slug`, and human-readable `reasoning`.
- Always pass `venue="polymarket"` on read paths.
- Never hardcode API keys or private keys.
- Treat the random entry logic as a demo template, not a production strategy.