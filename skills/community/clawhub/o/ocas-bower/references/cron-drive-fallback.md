# Cron / isolated-context Drive fallback (local SDK)

The MCP `google_workspace` Drive tools (`mcp__google_workspace__list_drive_items`,
`mcp__google_workspace__search_drive_files`) are the documented Bower interface
(see `mcp-drive-tooling.md`). **But in isolated/cron Hermes sessions they are NOT
registered** — the tool registry contains only the standard Hermes tool set. Calling
them returns: `Tool '<name>' does not exist. Available tools: browser_back, ...`.

## When to use this fallback
- A scheduled `bower:scan` / `bower:weekly-deep` cron run.
- Any session where `tool_search` / `tool_describe` for `mcp__google_workspace__*`
  returns "not found" or the call returns "does not exist".

## The local SDK path
- Credential helper: `$HERMES_HOME/../indigo/scripts/google_auth.py`
  exposes `get_service(api_name, api_version, scopes, account=...)`.
- **ALWAYS build the service through `get_service` — do NOT hand-build
  `Credentials` from a cached token file + a separately hardcoded `client_id`.**
  The cached token files (`$HERMES_HOME/../indigo/google_token.json`,
  `<fs-root>/indigo-repo/credentials/google_token.json`) carry a `client_id` that
  does NOT match the <operator> OAuth client (`628032148246-…`). If a script loads
  one of those token files yet constructs
  `Credentials(client_id="628032148246-…", …)`, the token (issued for one
  client) is presented with another client's secrets → `invalid_grant: Bad
  Request`. `get_service` pulls both `client_id` and `client_secret` from its
  own `_CLIENTS[account]` map, so they always match. This mismatch silently
  killed Bower light scans for 16 days (2026-06-29 → 2026-07-14) while the
  deep scan — which already used `get_service` — kept succeeding. If a light
  scan dies with `invalid_grant`, suspect a script that bypasses `get_service`
  first, not a dead refresh token.
- Build the service:
  ```python
  import sys
  from pathlib import Path
  sys.path.insert(0, str(Path("$HERMES_HOME/../indigo/scripts")))
  from google_auth import get_service
  svc = get_service("drive", "v3",
                    ["https://www.googleapis.com/auth/drive"],
                    account="<user-google-email>")
  # raises on dead refresh token (HTTP 400 invalid_grant)
  svc.about().get(fields="user").execute()  # smoke test
  ```
- Run the scan script via `terminal` (cron blocks `execute_code`):
  `python3 $HERMES_HOME/../indigo/commons/data/ocas-bower/run_light_scan.py`
  (NOTE: the script once referenced here, `scripts/bower_drive_sdk_light_scan.py`,
  does NOT exist — do not call it. `run_light_scan.py` uses `get_service`, reads
  the cutoff dynamically from `drive_digest.json` `last_updated`, and honors
  every invariant: structural baseline check, owned-vs-shared split, no deletes.)
  It writes the same artifacts as the MCP path (`light_scan_latest.json`,
  `scan_events.jsonl`, `evidence.jsonl`) plus an Observation Journal under
  `commons/journals/ocas-bower/YYYY-MM-DD/`.

## API call mapping (same semantics as the MCP table)
| Bower step | SDK call |
|------------|----------|
| Root baseline (pageSize=10) | `svc.files().list(q="'root' in parents and trashed=false", pageSize=10, includeItemsFromAllDrives=False, supportsAllDrives=False, fields="nextPageToken, files(id,name,mimeType)")` |
| modifiedTime arrival | `svc.files().list(q=f"modifiedTime > '{CUTOFF}' and trashed=false", corpora="user", includeItemsFromAllDrives=False, orderBy="modifiedTime desc", pageSize=200, fields="nextPageToken, files(...)")` |

## Auth failure -> degraded mode
A revoked/expired refresh token raises `HTTP 400 invalid_grant: Bad Request`
(even when `Credentials.valid` is `True`). This is **permanent** — no retry
recovers it. Handle at the scan entry point:
1. Catch the exception.
2. Write `degraded: google_drive` to `evidence.jsonl` (`not_activity_reason` mandatory).
3. Write an aborted `light_scan` event to `scan_events.jsonl`.
4. Report degraded; do NOT generate proposals; never delete.
5. Tell <operator> to re-authenticate via OAuth consent
   (`access_type=offline&prompt=consent`) for `<user-google-email>`.

First observed 2026-06-29; recurred 2026-07-14 (16 days of silent light-scan
failures). `scripts/bower_drive_sdk_light_scan.py` implements this contract.
