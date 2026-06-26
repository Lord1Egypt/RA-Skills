# No.0 Event Schema — `cognitive_file_tampering`

**Schema version**: `1.0`
**Producer**: `no0-core`
**Consumer** (optional): `no0-dlc-internal-control`
**Transport**: filesystem (one JSON file per event under `~/.openclaw/no0/events/`)

Core emits events; DLC (if installed) consumes them. **Core does not depend on DLC** — events unread by any consumer simply stay on disk.

---

## 1. Directory layout

```
~/.openclaw/no0/events/
├── pending/       # Core writes here; DLC reads + moves when handled
└── processed/     # DLC archives handled events under YYYY-MM-DD/
```

Core creates `pending/` on first emission. DLC creates `processed/` on first handling.

## 2. Event filename

```
<ISO8601 UTC timestamp>_<6-char hash>.json
```

Examples:

- `2026-04-19T14:32:17Z_a3f2b1.json`

The hash is `md5(timestamp|file_name|new_hash)[:6]` — enough to disambiguate two tamper events on the same file in the same second without implying cryptographic guarantees.

## 3. Severity gating

Core emits events **only for Level 4 and Level 5**. Levels 1–3 are recorded in `change_log.json` but never written to `pending/`. This keeps the event stream high-signal for DLC's authorization flow.

## 4. JSON schema

```jsonc
{
  "event_id": "2026-04-19T14:32:17Z_a3f2b1",
  "event_type": "cognitive_file_tampering",
  "schema_version": "1.0",

  "timestamp": "2026-04-19T14:32:17Z",          // UTC, seconds precision
  "source": "no0-core",                          // producer identifier
  "severity": "level_4" | "level_5",            // string form
  "severity_numeric": 4 | 5,                     // int form, for ordering

  "target_file": "SOUL.md",                      // cognitive file basename
  "target_path": "/Users/.../SOUL.md",           // absolute path if known; may be ""
  "baseline_hash": "<md5 of prior baseline>",    // may be "" if unknown
  "current_hash":  "<md5 of tampered file>",     // may be "" if unknown

  "rule_hits": ["安全机制绕过", "自动执行外部命令"],  // HIGH_RISK_RULES groups hit
  "diff_summary": {
    "lines_added": 3,
    "lines_removed": 0
  },
  "diff_preview": "--- a\n+++ b\n@@\n+ ... (<= 500 chars)",
  "full_diff_path": "~/.openclaw/no0/change_log.json",  // pointer to full context

  "reason": "Core heartbeat processor's classification reason string",
  "suggested_action": "rollback_to_baseline",

  "dlc_request": {
    "require_authorization": true,               // DLC should gate the user
    "require_mfa": true,                         // Level 5 or critical rule → MFA
    "reason_for_user": "检测到 SOUL.md 被篡改……" // human-readable message
  }
}
```

### Field notes

- `dlc_request` is a **suggestion**. DLC may ignore, downgrade, or escalate.
- `rule_hits` lists `HIGH_RISK_RULES` group names from `heartbeat_processor.py` (e.g. `安全机制绕过`, `自动执行外部命令`, `敏感信息外发`, `破坏性清理与覆盖`, etc.). Medium/low hits are not exported.
- `require_mfa` is `true` when the level is 5 **or** any critical rule group is hit; otherwise `false`.
- `require_authorization` is `true` for all emitted events (Level 4+).
- Empty strings (`""`) are used in place of missing hashes or paths rather than `null`.

## 5. Write semantics

Core writes each event **atomically**:

1. Write to `<event_id>.json.tmp` (via `tempfile.mkstemp`) with `json.dump(..., indent=2, ensure_ascii=False)`.
2. `fh.flush()` + `os.fsync(fh.fileno())`.
3. `os.replace(tmp_path, final_path)`.

DLC is guaranteed never to see a half-written event.

Emission is **fail-soft**: any `Exception` in the emitter is caught and logged to stderr; the Core heartbeat loop never raises due to DLC-facing I/O.

## 6. Consumption semantics (DLC side)

DLC should:

1. Watch `pending/` (FSEvents/inotify/ReadDirectoryChangesW, or poll at 5s).
2. Ignore filenames starting with `.tmp_` (in-progress writes).
3. For each event, apply severity logic:
   - Level 5 or `dlc_request.require_mfa` → HTTP auth + TOTP MFA.
   - Level 4 and only `require_authorization` → HTTP auth without MFA.
4. On resolution, move the event to `processed/<YYYY-MM-DD>/<event_id>.json` and append to `~/.openclaw/no0/dlc/audit.csv`.
5. If the user chooses rollback, DLC shells out to Core: `./no0 rollback <file> <version>`. DLC must **not** import Core modules.

## 7. Versioning

Events carry `schema_version`. DLC should:

- Accept any `major.minor` where `major` matches its supported major.
- Reject with an audit entry (not a crash) if the major differs.

v0.3.0 ships `schema_version: "1.0"`. Future breaking changes bump the major.

## 8. What is **not** in scope for v0.3.0

- DLC → Core reverse events (spec §3.3 — deferred).
- Event aging / cleanup of stale `pending/` items (flag to Sailor).
- Event schema negotiation between major versions.
