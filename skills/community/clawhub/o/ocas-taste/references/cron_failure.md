# Cron Failure Fallback

When a taste cron job runs and the Gmail/Calendar OAuth token is revoked (all refresh attempts return `invalid_grant`):

1. **Don't SILENT-fail.** Always output a report containing: auth failure diagnosis, OAuth re-authorization URL, current taste model state, and any data quality issues.
2. **Check credentials.** All Google credentials are centralized in the agent's credential directory (typically `~/.google_Google services/credentials/`). If refresh fails with `invalid_grant`, full re-auth is required — no retry will help. See `references/api_auth.md` for paths and patterns.
3. **Generate the auth URL** using the re-auth procedure in `infrastructure/google-workspace-auth` skill.
4. **Report existing data quality.** Even when scan fails, analyze existing `signals.jsonl` and `items.jsonl` for: enrichment coverage (target: 90%), signal freshness (fraction within 180-day half-life), calendar noise, duplicate venue names.
5. **Distinguish the failure layer.** Three layers can fail independently — diagnose which one:
   - MCP server unreachable → MCP tools fail; standalone `google_auth.py` still works
   - Invalid/expired token → Both MCP and standalone fail with `invalid_grant`
   - 0-byte token file → MCP standalone silently falls back to wrong account; standalone `google_auth.py` silently skips

## MCP server outage (distinct from token failure)

If MCP tools fail with `"MCP server 'google-workspace' is unreachable after 10 consecutive failures"`:

- **Do not retry MCP tools** — the auto-retry cooldown (~60s) wastes the entire cron window
- **Fall back to standalone scripts immediately.** The `google_auth.py` helper at `<hermes-home>/scripts/google_auth.py` works independently of the MCP server
- Check which layer failed: if `get_gmail_service()` / `get_calendar_service()` succeed but MCP tools fail, the tokens are fine — only the MCP server is down
- If both MCP and standalone fail, the token itself is the problem (see below)
- **Two separate issues may coexist:** MCP server down + token expired. Report both distinctly.

**Standalone fallback pattern:**
```python
import sys
from pathlib import Path
sys.path.insert(0, str(Path('<hermes-home>/scripts')))
from google_auth import get_gmail_service, get_calendar_service

gmail = get_gmail_service()
cal = get_calendar_service()
# Use Gmail/Calendar APIs directly (see references/email_extraction.md for query patterns)
```

## Empty or corrupt token file (distinct from `invalid_grant`)

If the credential file at `~/.google_Google services/credentials/<email>.json` is **0 bytes** (empty/truncated), the failure mode differs from `invalid_grant`:

- `google_auth.py` tries `json.loads(token_path.read_text())` → `JSONDecodeError: Expecting value: line 1 column 1 (char 0)`
- The helper prints `Skipping <email>: cannot read token file` to stderr and falls back to the next account
- The fallback account (typically the agent) has zero consumption emails → all services return 0 messages
- **The scan reports success (exit 0) with 0 extractions — no obvious failure signal**

**Diagnosis:** Before scanning, verify token file integrity:
```bash
wc -c ~/.google_Google services/credentials/*.json
```
Any file that is 0 bytes is corrupt and needs re-authorization.

**Recovery:** Same as `invalid_grant` — re-authorize via:
```bash
python3 <hermes-home>/skills/infrastructure/google-workspace-auth/scripts/google_oauth_init.py
```
⚠️ **Account limitation:** `google_oauth_init.py` hardcodes the agent's email (`<third-party-or-user-email>`) on line 141. It will NOT re-authorize <operator>'s account. For <operator>'s account, either edit line 141 to `'<user-google-email>'` (requires localhost:8000 access), or generate the re-auth URL manually by extracting `client_id`/`client_secret` from `<gworkspace-creds>/credentials/<user-google-email>.json` and constructing the OAuth URL with `login_hint=<user-google-email>` (see SKILL.md gotchas for the PKCE pattern).
The scan report should include the file sizes and flag any 0-byte credential files explicitly.

## Token expiry timezone suffix (distinct from `invalid_grant` and 0-byte)

If the credential file has a valid `expiry` field with a timezone suffix (e.g., `"2026-06-17T17:41:40+00:00"`), `Credentials.from_authorized_user_file()` fails with:
```
Error: unconverted data remains: +00:00
```

This is **not** an `invalid_grant` — the token itself is valid. The Google OAuth library's `strptime` parser simply doesn't handle the `+00:00` suffix.

**Diagnosis:**
```bash
python3 -c "
import json
d = json.load(open('<gworkspace-creds>/credentials/<email>.json'))
print('expiry:', repr(d.get('expiry')))
print('access_token present:', bool(d.get('token')))
"
```

**Fix:** Strip the timezone suffix from the `expiry` field:
```python
import json
from pathlib import Path
for email in ['<user-google-email>', '<agent-email>']:
    p = Path(f'<gworkspace-creds>/credentials/{email}.json')
    if not p.exists():
        continue
    d = json.loads(p.read_text())
    old = d.get('expiry')
    if old and '+' in str(old):
        d['expiry'] = old[:19]
        p.write_text(json.dumps(d, indent=2))
        print(f'{email}: fixed {old} -> {d["expiry"]}')
```

After fixing, the scan should proceed normally. The refreshed token will get a new `expiry` field — check if it includes the suffix again on subsequent runs.