# OAuth Recovery Escalation Patterns

Reference for Sands cron runs when Google Calendar auth fails. Read this before retrying auth more than once.

## Error → Meaning → Action

| Error | Meaning | Action |
|---|---|---|
| `invalid_grant: Bad Request` | Refresh token is **dead** (revoked or expired beyond renewal). Not fixable by retry. | Log `degraded: oauth_stale` in evidence. Set `auth_status: STALE_OAUTH` in config. Report to user — they must re-authorize with `access_type=offline&prompt=consent`. Do NOT retry. |
| `oauth_required` (via MCP) | OAuth token expired but refresh token may still be valid. | Attempt refresh via `google_auth.py`. If refresh succeeds, proceed. If refresh fails with `invalid_grant`, escalate to the row above. |
| `ClosedResourceError` / MCP unreachable | Google Workspace MCP server is not running. | Check `ps aux | grep google-workspace-mcp`. If not running, do NOT spend cycles starting it — it's not part of the standard Hermes install. Fall back to direct `google_auth.py`. If direct auth also fails, log compound failure. |
| `404 Not Found` (calendar) | Calendar ID no longer accessible (e.g., work account removed). | Remove from `primary_calendar_ids` in config. Do not hardcode IDs — always discover via `calendarList().list()`. |

## Compound Failures

When multiple things fail simultaneously, log each one separately in evidence:

- **OAuth stale + MCP unreachable**: Log both `degraded: oauth_stale` AND `degraded: google_workspace_mcp`. The user needs to fix BOTH.
- **OAuth stale + service unreachable**: Wait ~40s cooldown, retry once. If retry also fails, log `degraded: google_calendar_unreachable` AND `degraded: oauth_stale`. Do NOT retry auth in a loop when the service is unreachable.

## Recovery Window

- `invalid_grant` requires user intervention — no automatic recovery is possible.
- `oauth_required` may self-heal if the refresh token is still valid (auto-refresh on next successful MCP connection).
- MCP server issues are environmental — the user must start the server process.

## Last Known Good State

When auth fails, always record in evidence:
1. Which calendars failed and with what error
2. Whether the MCP server was reachable
3. Whether direct `google_auth.py` was attempted
4. The `auth_status` value set in config.json

This helps the next run determine if the situation has changed (e.g., MCP server started working again).

## Stale `auth_status` in config.json

The `auth_status` field in `config.json` is written by previous runs and can be **wrong**. A value of `STALE_OAUTH` means a *previous run* failed — it does not prove the token is currently dead.

**Rule:** Ignore `auth_status` as a pre-flight check. Always attempt the live API call first. Only conclude the token is dead if the live call returns `invalid_grant`. On success, reset `auth_status` to `OK`.

**Pattern that caused 8+ days of false failures (2026-06-04):**
1. Early run hit MCP-unreachable + OAuth error → set `auth_status: STALE_OAUTH`
2. Subsequent runs saw `STALE_OAUTH` and logged `degraded` without attempting the call
3. The token was actually valid the entire time
4. Fix: always try the call, let the API be the source of truth
