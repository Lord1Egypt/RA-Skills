# odds-api.net JavaScript starter

Requires Node.js 22+. No npm packages are needed. No API keys are included or written by this starter. Configure your own `ODDS_API_KEY` in your process or agent runtime before making authenticated requests.

```bash
node main.mjs --help
node main.mjs catalog --kind sports
node main.mjs catalog --kind leagues --sport basketball
node main.mjs catalog --kind bookmakers --country-code US
node main.mjs events --sport basketball --league NBA --from <UTC_START> --to <UTC_END>
node main.mjs snapshot --event-id <EVENT_ID> --periods "full time"
node stream.mjs --event-id <EVENT_ID> --periods "full time" --seconds 60
```

Replace angle-bracket tokens before execution. UTC timestamps must include seconds and end in `Z`. Discover event IDs instead of reusing an example. `--help` works offline without a key.

`api.mjs` handles authentication, bounded rate-limit retries, safe errors, host checks, and pagination. `discovery.mjs` provides catalogs, bounded event discovery, and complete snapshot pages. `main.mjs` prints JSON including each page's freshness metadata. `stream.mjs` emits snapshot, delta, heartbeat, and resync frames as JSON lines; it is a finite transport consumer, not a cache, notifier, or trading application.

`ODDS_API_BASE_URL` defaults to `https://api.odds-api.net/v1`; an explicit loopback `/v1` URL is allowed for mocked tests. Other hosts and redirects are refused. API keys belong on the backend, never in browser-visible code or URLs.

Sequential snapshot pages are not atomic. For a cache, preserve market identity, process ordered semantic delta batches idempotently, and commit data plus resume tokens together. Reload the snapshot on `resync`.

Website: [odds-api.net](https://odds-api.net/). Documentation: [API reference](https://odds-api.net/docs). Public developer package: [GitHub](https://github.com/odds-api/odds-api).
