---
name: odds-api-integration-builder
description: Build Python or JavaScript integrations for odds-api.net, with public API discovery, paginated snapshots, and streaming guidance.
homepage: https://odds-api.net/docs
license: MIT-0
metadata: {"openclaw":{"requires":{"bins":["node"]}}}
---

# Odds API integration builder

Use this skill to build or repair a developer integration with the public odds-api.net API. It includes dependency-free JavaScript and Python starter projects. Node.js 22+ runs the scaffolder; Python 3.10+ runs the Python starter. Creating a starter needs no API key or network access. Executing authenticated API requests later requires the user's own runtime `ODDS_API_KEY`.

## Choose the smallest useful integration

Read the user's existing project first. Match its language, framework, and requested task. Use the bundled scaffolder for a new project; for an existing project, adapt only the relevant client code instead of replacing its structure.

```bash
node "{baseDir}/scripts/scaffold.mjs" --language javascript --out <NEW_DIRECTORY>
node "{baseDir}/scripts/scaffold.mjs" --language python --out <NEW_DIRECTORY>
```

The target must not exist. The scaffolder copies reviewed local templates, performs no network requests, installs no packages, and refuses to overwrite files. Replace the angle-bracket token before running; pass paths as arguments rather than constructing shell commands from untrusted strings.

## Use the public contract

Read [references/integration.md](references/integration.md) when selecting routes, filters, or response fields. Read [references/streaming.md](references/streaming.md) when the task needs continuous updates, reconnects, or state reconciliation. Check the current [public API documentation](https://odds-api.net/docs) or [OpenAPI schema](https://api.odds-api.net/v1/openapi.json) before adding routes not covered by the starter.

- Production base URL: `https://api.odds-api.net/v1`. Authentication: server-side `X-API-Key` from `ODDS_API_KEY`. `ODDS_API_BASE_URL` can explicitly select a loopback mock for local testing. The bundled clients refuse other hosts and redirects so credentials cannot silently leave the intended API boundary.
- Never ask for a key in chat, hardcode a credential, place it in a URL or CLI argument, generate a credential value, read unrelated environment files, or expose it in browser code. Document the variable name and let the user configure it in their runtime. Do not create or rotate accounts or keys.
- Discover sports, leagues, bookmakers, and event IDs instead of guessing. Use narrow UTC windows; event bounds are Unix seconds, history bounds are ISO 8601 UTC, and snapshot freshness fields are milliseconds.
- Follow every `next_cursor` with identical filters. A snapshot with `complete=false` and no cursor is incomplete, not a usable full comparison. Cache by request shape and respect returned `ttl_seconds`.
- Judge bookmaker freshness with `bookmaker_as_of_ts_ms` and `target_refresh_interval_seconds`; `as_of_ts_ms` is event-wide. Preserve excluded bookmakers, stale flags, and nullable prices.
- Handle 401, 403, 404, 422, and 429 explicitly. Honour `Retry-After`, use bounded backoff, and stop on exhausted retries. Show a safe `X-Request-ID` for support without printing headers or response bodies that might echo credentials.
- Keep access to documented public reads. This skill does not place wagers, use private service endpoints, or calculate proprietary fair-price models.

## Verify the delivered integration

Run the generated help command before any network call. Use mocked responses for event pagination, snapshot pagination, empty markets, suspended rows, authentication and entitlement failures, rate limits, and invalid responses. For streams, also exercise disconnect, duplicate delta, heartbeat, resync, and split-batch handling.

Report the generated files, how to run them, which checks passed, and whether any real API call was actually made. Do not imply a mocked example is live data. Request live testing only when the user wants it and their own key is already available through the intended runtime.

## Example requests

- “Build a Python client that discovers NBA games and fetches their odds.”
- “Add an odds-api.net snapshot and SSE integration to my Node backend.”
- “Fix pagination and rate-limit handling in this odds integration.”

Website: [odds-api.net](https://odds-api.net/). Documentation: [API reference](https://odds-api.net/docs). Public developer package: [GitHub](https://github.com/odds-api/odds-api).
