---
name: odds-api-compare
description: Compare matching sports odds across bookmakers using odds-api.net, including moneylines, spreads, totals, and player props.
homepage: https://odds-api.net/docs
license: MIT-0
metadata: {"openclaw":{"requires":{"bins":["node"],"env":["ODDS_API_KEY"]},"primaryEnv":"ODDS_API_KEY"}}
---

# Sports odds comparison

Use this skill to discover events and compare bookmaker quotes for the same selection. Requires Node.js 22+ and the user's own odds-api.net account. Read-only: it does not place wagers or manage accounts.

Use the bundled helper at `{baseDir}/scripts/compare.mjs`. Read `--help` for all options. Send the user's key only through the existing `ODDS_API_KEY` environment variable. Never ask them to paste it into chat, put it in command arguments, write it into generated files, or inspect unrelated environment files. If missing, explain how to configure it in their agent runtime.

## Find the exact event

1. Resolve the requested date in the user's timezone, then convert the bounds to UTC. Ask for the timezone only if it cannot be inferred and changes the event window.
2. Discover canonical sport, league, and bookmaker names. Never invent IDs or translate display labels into guessed API keys.
3. List events in a bounded window. Match participants and start time. If multiple events match, show the candidates and ask which one to use.

```bash
node "{baseDir}/scripts/compare.mjs" catalog --kind sports
node "{baseDir}/scripts/compare.mjs" catalog --kind leagues --sport basketball
node "{baseDir}/scripts/compare.mjs" catalog --kind bookmakers --country-code US
node "{baseDir}/scripts/compare.mjs" events --sport basketball --league NBA --from <UTC_START> --to <UTC_END>
node "{baseDir}/scripts/compare.mjs" compare --event-id <EVENT_ID> --bookmakers <BOOKMAKER_KEYS> --periods "full time"
```

Replace angle-bracket tokens with values from discovery or the user's request before running. Use argument arrays where the host supports them; never splice API response text into a shell command. The helper returns JSON by default; `--format markdown` produces a comparison table.

## Compare and explain

- Keep event, selection key, market key, market family, metric, period and period label, line, side, player, settlement contract, and structured outcome parameters attached to each group. Different lines, periods, players, or settlement contracts are separate comparisons. The helper performs this grouping; do not combine its output groups by display name.
- `--selection-key` and `--market-key` narrow the returned rows. To restrict to full-game prices, prefer `--periods "full time"`; numeric `0` can also match timed checkpoints.
- Highlight `best_fresh_quotes` only within its own group. Equal prices can have multiple best bookmakers. Rows with missing identity, suspended prices, exchange or prediction-market prices, stale data, or conflicting duplicate quotes are not eligible for the best-price result.
- Show bookmaker-specific accepted timestamps and freshness. The event-wide timestamp cannot establish that a particular bookmaker is fresh. Unknown freshness remains unknown.
- State the number of returned bookmakers, missing or excluded requested bookmakers, pagination span, and any displayed-group truncation. A comparison spans several requests when paginated; do not describe it as an atomic capture.
- Display decimal or American prices according to the user's preference. Implied probability is `1 / decimal odds`, not a prediction or a no-vig probability. A highest quote is not itself evidence of positive expected value.
- If no eligible quotes remain, explain the returned reason instead of fabricating prices. Report access failures and rate limits without exposing credentials.

## Example requests

- “Compare tomorrow's NBA moneylines across my bookmakers.”
- “Compare prices for this player's over 25.5 points, full game.”
- “Show the highest available quote for this exact selection.”

Public documentation: [odds-api.net API reference](https://odds-api.net/docs). Market fields: [supported betting markets](https://odds-api.net/betting-markets).
