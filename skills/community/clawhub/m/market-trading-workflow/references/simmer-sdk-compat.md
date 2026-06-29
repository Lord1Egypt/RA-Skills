# Simmer SDK compatibility notes

This reference captures the compatibility pattern learned while validating the market-trading workflow against the installed `simmer-sdk` in this environment.

## Why it matters

Different `simmer-sdk` versions expose different discovery kwargs. The workflow should prefer the smallest stable surface and fall back safely when a newer keyword is unavailable.

## Observed usable patterns

- `SimmerClient.from_env()` works for client creation.
- `client.get_markets(q=..., limit=...)` works reliably on older installs.
- `client.get_market_context(market_id, venue=..., my_probability=...)` is the safest context call shape.
- `client.trade(..., source=..., skill_slug=..., reasoning=..., venue=...)` is the preferred trade path.

## Implementation pattern

1. Build discovery kwargs dynamically.
2. Filter kwargs against the runtime method signature before calling.
3. Prefer `q` + `limit` for discovery compatibility.
4. Pass `venue` explicitly when reading context or placing trades.
5. Default to dry-run / paper mode unless live trading is explicitly requested.

## Practical fallback rule

If a newer discovery filter (for example `tags` or `sort`) is unavailable in the active SDK, fall back to a text query that still finds the intended market.

## Verification recipe

- Confirm the script imports.
- Run a dry-run against a known active market.
- Verify the response includes a pass/trade decision and a context-derived reason.
