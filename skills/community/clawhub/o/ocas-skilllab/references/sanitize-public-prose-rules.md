# Public-Profile Sanitization Rules

Session logs, deprecated-tool references, and canned AI taglines must not ship
in publishable skills or repos.

## Banned README Taglines

Scan `README.md` and `SKILL.md` for these literal strings.

Replace with a skill-specific description or a neutral placeholder.

| Banned |
|--------|
| Tell it what you need. It does the work. |
| One clear job, done well. |

## Banned Deprecated-Tool References

Do not cite deprecated/removed integrations in public-facing prose.

If the reference is meaningful, rewrite it as architecture guidance.

| Banned |
|--------|
| Elephas |

Replacement example:

See `references/integration-notes.md` for current backend architecture.

## Session-Log Quarantine

Any file whose basename matches one of the following is a session log.

Those files must live under `.archive/session-logs-export/`, not in `references/`.

| Pattern basename/regex |
|------------------------|
| `session-YYYY-MM-DD` |
| `session-YYYYMMDD...` |
| `session_YYYYMMDD...` |
| `dispatch-triggered-scan.md` |
| `token-repair.md` |
| `scan_execution_patterns.md` |
| `taste-scan-env-fix.md` |

## Verification

After sanitizing an `ocas-*` skill, confirm none remain:

```bash
grep -RsnE 'Tell it what you need|One clear job|Elephas' README.md SKILL.md references/ scripts/
find references -maxdepth 2 -type f | grep -Ev 'archive|session-logs-export'
```