# Token Repair Patterns

Five distinct failure modes exist — confirmed across 2026-06 through 2026-07-27. Run the combined repair script before every scan.

## Credential File Locations

Token files live under the Google Workspace MCP credentials directory, NOT under the Hermes credentials directory:

- **User account:** `~/.google_workspace_mcp/credentials/mx.indigo.karasu@gmail.com.json`
- **Agent/operator account:** `~/.google_workspace_mcp/credentials/<account-email>.json`
- **Symlinks** at `~/.google_workspace_mcp/credentials/operator_email.json` → operator account, `agent_email.json` → user account (read-only; do not write through symlinks — write to the real file).

The old `<gworkspace-creds>/credentials/` path is a placeholder — use the actual paths above.

## Failure Mode 1: Timezone Suffix in Expiry String

**Symptom:** `ValueError: unconverted data remains: +00:00` when loading token.

**Cause:** Google OAuth library writes `expiry: "2026-06-24T18:37:34+00:00"` but `google.oauth2.credentials.Credentials.from_authorized_user_file()` only accepts `%Y-%m-%dT%H:%M:%S`.

**Fix:** `d['expiry'] = d['expiry'][:19]`

## Failure Mode 2: Expiry as Float (Unix Timestamp)

**Symptom:** `AttributeError: 'float' object has no attribute 'rstrip'` when loading token.

**Cause:** Some token files store `expiry` as a Unix timestamp float instead of an ISO string.

**Fix:** `d['expiry'] = time.strftime('%Y-%m-%dT%H:%M:%S', time.localtime(time.time() + 3600))`

## Failure Mode 3: Microsecond Suffix (`.NNNNNN`)

**Symptom:** `from_authorized_user_file()` crashes with `unconverted data remains: .811606`. NOT matched by the `+`/`Z` check — passes through untouched.

**Fix:** Strip `.NNNNNN` before the `[:19]` truncation. The combined script handles this.

## Failure Mode 4: Numeric-String Expiry (Unix Timestamp as JSON String)

**Symptom:** Crashes with a format mismatch — `json.load` yields `str`, not `int`/`float`, so the float branch doesn't match and the string-suffix branch doesn't catch it.

**Cause:** `expiry: "1784952387"` (quoted integer). The `+`/`Z`/`.` stripping leaves it untouched since it has no suffix or fraction — it's a pure digit string.

**Fix:** Detect a pure-digit string and convert via `time.localtime(int(s))`.

**Confirmed 2026-07-26** (`mx.indigo.karasu@gmail.com.json`).

## Failure Mode 5: Microsecond Fraction + Z Suffix Combo

**Symptom:** `ValueError: unconverted data remains: .151160Z` — or silent crash at `from_authorized_user_file()`.

**Cause:** `expiry: "2026-07-27T18:23:50.151160Z"` — BOTH a microsecond fraction `.151160` AND a `Z` UTC suffix simultaneously. The `Z` stripping and `.` stripping must both fire in sequence.

**Fix:** Strip `Z` first, then strip `.` and everything after. The combined repair script handles this.

**Confirmed 2026-07-27** (`mx.indigo.karasu@gmail.com.json`).

## Combined Repair Script (handles all five modes)

Run this before every Taste scan to ensure tokens are valid.

```bash
python3 -c "
import json, time, re
from pathlib import Path

for email in ['mx.indigo.karasu@gmail.com', '<operator-email>']:
    path = Path(f'~/.google_workspace_mcp/credentials/{email}.json')
    if not path.exists():
        print(f'{email}: NO TOKEN FILE')
        continue
    with open(path) as f:
        d = json.load(f)
    expiry = d.get('expiry')
    changed = False
    if isinstance(expiry, bool):
        pass
    elif isinstance(expiry, (int, float)):
        d['expiry'] = time.strftime('%Y-%m-%dT%H:%M:%S', time.localtime(time.time() + 3600))
        changed = True
    elif isinstance(expiry, str):
        s = expiry.strip()
        if s.endswith('Z'):
            s = s[:-1]
        if '+' in s:
            s = s[:s.index('+')]
        if '.' in s:
            s = s[:s.index('.')]
        if re.fullmatch(r'\d+', s):
            d['expiry'] = time.strftime('%Y-%m-%dT%H:%M:%S', time.localtime(int(s)))
            changed = True
        elif s != expiry.strip():
            d['expiry'] = s
            changed = True
    if changed:
        with open(path, 'w') as f:
            json.dump(d, f, indent=2)
        print(f'{email}: Fixed {repr(expiry)} -> {repr(d[\"expiry\"])}')
    else:
        print(f'{email}: OK ({repr(expiry)})')
"
```

## Mandatory Every-Scan Pattern (Confirmed 2026-06-25)

As of dispatch #68, token repair has been required on **every single Taste scan** without exception. Five consecutive dispatches on 2026-06-25 all required timezone suffix stripping. This is now the expected default.

**Rule:** Always run the combined repair script immediately before `taste_scan.py`, chained in a SINGLE `terminal()` call. Never skip repair, never assume the token is still clean from a prior scan.

## Critical Race Condition: Repair → Refresh → Suffix Returns

**The OAuth library refreshes the token on every `google_auth.py` initialization.** If repair and scan run in separate `terminal()` calls, the scan's auth init triggers a refresh that re-adds the `+00:00` suffix — overwriting your repair. This window is seconds wide.

**Fix:** Chain repair + scan in ONE `terminal()` call:
```bash
python3 -c "<repair script above>" && cd $AGENT_ROOT/commons/data/ocas-taste && /usr/bin/python3 $HERMES_HOME/skills/ocas-taste/scripts/taste_scan.py scan-incremental 24
```
The repair writes the clean token, then the scan reads it in the same process — no refresh cycle can fire between them.

## Re-Run After Repair: Duplicate Signal Risk

When tokens are repaired mid-session and the scan re-processes emails, duplicate signals may appear with different `signal_id` UUIDs and slightly different `event_date` precision (e.g., `2026-06-24T13:13:29` vs `2026-06-24T13:20:44.677614`). The dedup script's `(venue_name, event_date[:10], extraction_source)` key should catch these, but event_date precision differences can fool it.

**Mitigation after token repair:**
1. Record `wc -l signals.jsonl` before the scan
2. Record `wc -l signals.jsonl` after the scan
3. If delta > 0 and the scan was a re-run after repair, check for same-venue + same-day duplicates manually

## Confirmed Incidents

- **2026-07-27:** mx.indigo Mode 5 (`.151160Z` microsecond+fraction+Z combo). Also the operator account, Mode 2 (float). Both repaired in one `terminal()` call. Scan succeeded (3 email signals: U :Dessert Story, Chaat Corner alert, Chaat Corner confirmation).
- **2026-07-26:** mx.indigo Mode 4 (`"1784952387"` numeric string). Latent — scan loaded the operator's token first and succeeded.
- **2026-07-15:** Operator Mode 3 (`.811606` microsecond suffix).
- **2026-07-15:** Operator Mode 4 (`"1784952387"` numeric string). Both in same token file.
- **2026-06-25 dispatch #65:** Both accounts Mode 1 again. Scan + repair in single `terminal()` call succeeded. 1 signal created.
- **2026-06-25 dispatch #62:** Token refresh race confirmed (see below).
- **2026-06-24 (dispatch #53):** Mode 1 on both accounts. Re-run created 2 Lavash/DoorDash signals with different precision. Dedup missed them (different `event_date` string). Manual dedup key caught them.
- **2026-06-24 (dispatch #486):** Mode 1 on both accounts. Fixed, scan created 1 signal (Lavash/DoorDash).
- **2026-06-24 (dispatch #485):** mx.indigo Mode 1, owner Mode 2 (float). Fixed, scan created 1 signal (Lavash/DoorDash).
- **2026-06-23:** Mode 1 on owner token. Fixed, scan created 142 signals.

## Token Refresh Race (Repair → Refresh → Suffix Returns)

**Symptom:** Token repair succeeds (confirmed `expiry: "2026-06-25T03:40:37"`), but the subsequent scan immediately fails with `unconverted data remains: +00:00`.

**Cause:** Between the repair `python3 -c` call and the scan script invocation, the Google OAuth library performs a token refresh. The refresh writes a new `expiry` field with the `+00:00` timezone suffix, overwriting the stripped version. This happens within seconds.

**Fix:** Combine repair and scan in a SINGLE `terminal()` call (see Mandatory Every-Scan Pattern above). The repair and scan run in the same process — no refresh cycle can fire between them. A freshly-repaired token with a future expiry won't trigger a refresh on the same init call anyway.