---
name: polymarket-football-odds
description: Analyze Polymarket football/soccer match URLs and estimate match win/draw probabilities using API-Football/API-SPORTS. Use when the user provides a polymarket.com event or market URL for a soccer match and asks to identify the teams, query API-Football, calculate 1X2 probabilities, compare with Polymarket implied odds, or produce a win-probability summary.
---

# Polymarket Football Odds

## Overview

Use this skill to turn a Polymarket football URL into a football fixture lookup and a probability summary. The bundled TypeScript script extracts the Polymarket slug, fetches Gamma event/market metadata, infers the two teams, matches the fixture in API-Football, calls API-Football predictions, and prints home/draw/away probabilities.

## Quick Start

Require an API-Football/API-SPORTS key in the environment. Do not hardcode the key in files or messages.

```bash
API_FOOTBALL_KEY="..." node --experimental-strip-types scripts/analyze-polymarket-football.ts "https://polymarket.com/event/..."
```

Use `--json` when the caller wants machine-readable output:

```bash
API_FOOTBALL_KEY="..." node --experimental-strip-types scripts/analyze-polymarket-football.ts "https://polymarket.com/event/..." --json
```

## Workflow

1. Run the script with the Polymarket URL. It accepts `/event/{slug}` URLs, `/market/{slug}` URLs, and raw slugs.
2. Check the extracted Polymarket title, teams, and fixture. If the script reports multiple possible fixtures or low confidence, ask the user to confirm the fixture or rerun with `--fixture-id`.
3. Report the API-Football 1X2 probabilities as:
   - home team win probability
   - draw probability
   - away team win probability
   - target-team win probability when the Polymarket market asks about a single team
4. Include caveats: API-Football predictions are model outputs, fixture matching can be ambiguous, and Polymarket prices are market-implied prices rather than true probabilities.

## Options

- `--json`: print structured JSON instead of a human summary.
- `--fixture-id <id>`: bypass fixture matching and call API-Football predictions for a known fixture ID.
- `--date YYYY-MM-DD`: override the date used for fixture search.
- `--days <n>`: search plus/minus `n` days around the Polymarket date or `--date`; default is `1`.
- `--self-test`: run local parser tests without network calls or API keys.

## API Notes

Read `references/api-football-polymarket.md` before changing endpoint behavior. Use official endpoints only:

- Polymarket Gamma is public and used only for market discovery.
- API-Football requires the `x-apisports-key` request header.
- API-Football predictions require a fixture ID, so the script must identify the fixture before calling `/predictions`.

## Failure Handling

If the script cannot confidently identify two teams, do not invent team names. Explain which Polymarket title/outcomes were found and ask the user for the teams or fixture ID.

If API-Football returns no prediction for a fixture, report the fixture match and say prediction coverage is unavailable for that match. Do not substitute bookmaker odds as model probabilities unless the user explicitly asks for an odds-implied calculation.
