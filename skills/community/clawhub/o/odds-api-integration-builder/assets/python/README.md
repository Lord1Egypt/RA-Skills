# odds-api.net Python starter

Requires Python 3.10+. Uses the standard library; no pip packages are needed. Configure your own `ODDS_API_KEY` in the process or agent runtime. No key is included, accepted as a command argument, or written to a file.

```bash
python example.py --help
python example.py catalog --kind sports
python example.py catalog --kind leagues --sport basketball
python example.py catalog --kind bookmakers --country-code US
python example.py events --sport basketball --league NBA --from <UTC_START> --to <UTC_END>
python example.py snapshot --event-id <EVENT_ID> --periods "full time"
```

Replace angle-bracket tokens before running. Discover IDs from current responses. `--help` works offline without a key. UTC event bounds end in `Z` and are converted to Unix seconds by the example.

`odds_client.py` provides a read-only client with bounded retries, cursor pagination, complete snapshot checks, safe error messages, host checks, and redirect refusal. `example.py` prints JSON. Snapshot results retain separate page metadata because sequential pages are not an atomic capture.

The production base is `https://api.odds-api.net/v1`. Set `ODDS_API_BASE_URL` only when intentionally using an explicit loopback `/v1` mock. Keep authenticated calls on the backend.

This starter implements REST. For continuous updates, fetch the initial snapshot, connect to the matching SSE/WebSocket route with its resume token, reconcile ordered deltas idempotently, and reload the snapshot on resync. See the integration skill's streaming reference before implementing that state machine.

Website: [odds-api.net](https://odds-api.net/). Documentation: [API reference](https://odds-api.net/docs). Public developer package: [GitHub](https://github.com/odds-api/odds-api).
