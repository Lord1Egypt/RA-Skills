# Public API integration notes

Contract checked against the anonymous public OpenAPI document on 4 November 2026. Recheck current documentation when extending the starter; account plans and endpoint fields can change.

## Included starters

JavaScript requires Node.js 22+ and uses native `fetch`. Python requires 3.10+ and uses the standard library. Neither requires npm or pip packages. Run `node main.mjs --help` or `python example.py --help` without a key. Both clients restrict authenticated requests to the official API or an explicitly selected loopback mock and refuse HTTP redirects.

The generated README has runnable discovery and snapshot commands. Use the `ODDS_API_KEY` variable already configured in the user's process; do not populate a file with a key. Keep all authenticated requests on a backend or agent host.

## Route sequence

| Task | Public route | Important fields |
|---|---|---|
| Sports | `/sports` | `items` is an array of strings |
| Leagues | `/leagues?sport=...` | `items` plus optional `details` |
| Bookmakers | `/bookmakers?country_code=...` | `items[].bookmaker`, `country_codes` |
| Events | `/events` | `sport`, `league`, `start_from`, `start_to`, `limit`, `cursor` |
| Odds | `/events/{event_id}/odds/snapshot` | `items`, `next_cursor`, `complete`, `resume`, bookmaker freshness |
| History | `/events/{event_id}/odds/history` | `selection_key`, bounded `from_ts` and `to_ts`, `series[].bookmaker_name`, `points` |

Event bounds are Unix seconds, not milliseconds. History query bounds are ISO 8601 UTC strings. Snapshot acceptance timestamps are milliseconds. `tick_ts` history samples are event driven; a missing sample is not a price of zero.

The `types`, `market_keys`, `periods`, and `bookmakers` snapshot filters are comma-separated strings. Do not assume `type`, `bet_type`, and `market_key` are interchangeable. The full-time label is a safer filter than numeric period `0` when excluding timed checkpoints.

Follow `next_cursor` without changing filters. Snapshot pages contain whole bookmakers; a soft `limit` is not a strict row count. Explicit bookmaker filters may return a large single response. Do not use a small page length as the completion test. Fail explicitly if a safety cap or nonadvancing cursor prevents completing the request.

## Price identity and freshness

Preserve event ID, selection key, market key, market family, period and label, line, side, metric, player, structured selection parameters, and settlement contract. Two rows with similar names can settle differently. Exchange and prediction-market prices need their own price/liquidity handling; do not silently pool them with sportsbook quotes.

Use `bookmaker_as_of_ts_ms[bookmaker]` for a bookmaker's acceptance time. The event-wide `as_of_ts_ms` can advance because an unrelated bookmaker updated. Retain `stale_bookmakers`, `excluded_bookmakers`, and `target_refresh_interval_seconds`. Treat missing freshness as unknown. Respect `ttl_seconds` when caching and keep the snapshot's opaque `resume` for hot streams.

`odds` is a decimal bookmaker quote. `odds_no_vig` and `fair_odds` are separate nullable price fields. Implied probability `1 / odds` still includes bookmaker margin. Request only the price fields the application needs.

## Failure behavior

Do not retry invalid credentials, denied access, or invalid filters indefinitely. For 429, honour numeric or HTTP-date `Retry-After`; if the wait exceeds the client's bounded retry budget, return a clear retry-later result. Quota exhaustion also requires checking usage; retrying faster cannot fix it. Do not print request headers, a full authenticated URL, raw error response bodies, or the credential.

Read [streaming.md](streaming.md) before implementing a continuous client. Reference: [odds-api.net docs](https://odds-api.net/docs).
