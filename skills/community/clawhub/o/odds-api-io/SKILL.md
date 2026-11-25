---
name: odds-api
description: Use the Odds-API.io MCP server to answer questions about sports betting odds, events, results, value bets, arbitrage, dropping odds, closing lines, bet settlement and golf outrights. Covers which tool to call first, how to keep responses small, quotas and error handling.
---

# Odds-API.io agent guide

The `odds-api` MCP server wraps the Odds-API.io v3 REST API: odds from 450+ bookmakers across 34 sports. The API key comes from the `ODDS_API_KEY` environment variable only; never ask the user to paste it into the chat and never repeat it.

## Call order

1. **Slugs first.** `get_sports` gives sport slugs, `get_leagues` gives league slugs. Never guess a slug.
2. **Find the event.** `search_events` (team name, `status=live` for in-play), `get_events` (sport + league + date window) or `get_live_events`. Past matches: `search_historical_events` or `get_historical_events`.
3. **Market names.** `get_markets` lists the exact names per sport. Use `ML`, `Spread`, `Totals`; there is no "Match Winner", "Over/Under" or "Asian Handicap".
4. **Bookmakers.** Odds tools only return bookmakers in the key's selection: check `get_selected_bookmakers`. `get_bookmakers` shows each book's `status` (ok, degraded, down) when one is missing.
5. **Prices.** `get_odds` or `get_multi_odds` (up to 10 events, one request) with `bookmakers` **and** `markets`. For "best price" or "fair price" questions use `get_odds_summary`.

## Keep responses small

- Always pass `markets` to `get_odds`, `get_multi_odds` and `get_historical_odds`.
- List tools accept `fields` (keep only some keys per item) and `maxResults`; `get_events` also takes `limit`/`skip`.
- `get_outright_odds` takes `markets` and `maxRunners`: a full golf field is 150+ runners per market.
- Pass `sport` to `get_dropping_odds`; without it player props dominate.

## Which tool for which job

| Job | Tool |
|---|---|
| Best / average / fair price | `get_odds_summary` (Growth plan and above; lower plans get `demo: true` sample data, say so) |
| Line history for one book | `get_odds_movements` (prematch; a 404 lists what does exist) |
| Value bets / arbitrage / steam | `get_value_bets`, `get_arbitrage_bets`, `get_dropping_odds` |
| Closing line value, backtests | `get_closing_lines` (up to 10 leagues, 366 days, 100 events per page) |
| Did my bet win? | `get_settlements`, `grade_bets` (up to 50 at once) |
| Golf outrights | `list_outrights` then `get_outright_odds` / `get_outright_results` (Outrights add-on) |
| Polymarket / Kalshi ids | `get_mappings` |
| Requests left this hour | `get_usage` |

## Plans and errors

- **403**: the plan or add-on does not include the endpoint (outrights, closing lines, settlement, mappings and dropping odds need a paid plan or add-on). Relay the message, which names what to enable, and do not retry.
- **429**: the hourly limit is spent until the reset time in the message. Do not retry before then; `get_usage` shows the limit.
- **400**: fix the arguments (usually a slug or market name).
- **401**: the key was rejected; the user can check it or pick a plan at https://odds-api.io/pricing?ref=mcp.

## Caching

Prematch odds change every few seconds to minutes; catalogue data (sports, leagues, markets, bookmakers) changes rarely. Reuse catalogue answers within a conversation instead of calling again. Each tool call is one API request (multi-event calls count as one).

## Answer format

- Name the bookmaker and when the price was updated (`updatedAt`).
- Odds are decimal strings. Score periods use `p1..pN`, `ft`, `ot`, `ap` (older keys `period1`, `overtime`, `penalties`, `fulltime` stop on 12 November 2026).
- Value bets: `expectedValue` is bookmaker/fair x 100; edge % = `expectedValue - 100` (103.42 is a 3.42% edge, below 100 is a negative edge). Arbitrage: `profitMargin` is already a percentage (2.48 means 2.48%).
- Prices and expected value are market data, not predictions. Present arbitrage as a calculated margin at the quoted prices: prices move and bookmakers can limit or void bets.
