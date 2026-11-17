# Usage tracking

Reach maintains a per-call append-only log so the agent can answer "how much of source X's quota have I used this month" without re-deriving from journals.

## Files

| Path | Format | Content |
|---|---|---|
| `{agent_root}/commons/data/ocas-reach/usage.jsonl` | JSONL | one row per call: `{ts, source, action, status, http_status, quota?}` |
| `{agent_root}/commons/data/ocas-reach/accounts.json` | JSON | account ledger (see `account_provisioning.md`) |

## Row schema

```json
{"ts": "2026-04-26T18:31:09Z", "source": "alpha_vantage", "action": "global_quote", "status": "success", "http_status": 200}
{"ts": "2026-04-26T18:33:51Z", "source": "alpha_vantage", "action": "global_quote", "status": "quota_blocked", "quota": {"daily_used": 25, "daily_remaining": 0}}
```

Statuses:
- `success` — call returned a valid response from the source
- `http_error` / `network_error` / `source_error` — call attempted but failed; counts toward usage
- `quota_blocked` — orchestrator refused to call because daily/monthly cap is exhausted; **does not count** against the cap (it never reached the source)
- `parse_error` — response received but couldn't decode

## Quota enforcement

Before every call, `reach.py` reads `usage.jsonl`, counts rows for `(source, today)` and `(source, this-month)` excluding `quota_blocked`, and compares against the source's `daily` / `monthly` fields in `sources.yml`. If either limit is at or past zero remaining, the call is refused with a `quota_exhausted` envelope.

To inspect:

```bash
python3 scripts/reach.py usage                  # all-time tally per source
python3 scripts/reach.py usage --month 2026-04  # one month
python3 scripts/reach.py source alpha_vantage   # quota state for one source
```

## What's tracked, what's not

- **Tracked**: every call attempt, regardless of HTTP status.
- **Not tracked**: registry / metadata commands (`sources`, `source <name>`, `usage`) — these don't hit any external source.
- **Not tracked**: calls made by skills *other* than Reach. If `weave` or `vesper` make their own API calls (they do, for Google Contacts / Gmail), those are tracked in those skills' own data dirs, not here.

## Rotation

`usage.jsonl` is append-only and never auto-rotated by the orchestrator. If it grows past ~10 MB, archive the prior month with:

```bash
mv {agent_root}/commons/data/ocas-reach/usage.jsonl \
   {agent_root}/commons/data/ocas-reach/usage-$(date -u +%Y-%m).jsonl
```

The file will be re-created on the next call. Quota counts re-derive from whatever's in the active log, so archiving mid-month resets visible usage — only do it at month boundary or accept the reset.

## Privacy

`usage.jsonl` records the source, action, and status of each call but **not the parameters or the response payload**. Parameters and responses live in journal files at `{agent_root}/commons/journals/ocas-reach/YYYY-MM-DD/`, which have stricter access controls.

When a journal is written, the orchestrator extracts only the response's `meta` / `citation` / `quality` fields (when present) into `result_meta` and discards the bulk payload to keep journals small. The full response is the caller's responsibility — Reach returns it on stdout but does not persist it.
