# Journal File Path Construction

When writing journal files, they MUST land in the date-subdirectory matching the journal's timestamp, not in the skill's journal root.

## Correct Pattern

```bash
TS=$(date -u +%Y%m%dT%H%M%SZ)
DATE_DIR=$(date -u +%Y-%m-%d)
JOURNAL_DIR="<hermes-home>/profiles/indigo/commons/journals/ocas-forge/${DATE_DIR}"
mkdir -p "$JOURNAL_DIR"
cat > "$JOURNAL_DIR/forge-scan-${TS}.json" << EOF
{"run_id": "forge-scan-${TS}", ...}
EOF
```

## Pitfall: Omitting the date subdirectory

Using the skill root directory instead of the date subdirectory:

```bash
# WRONG — file lands in parent, not date subdir
FORGE_DIR="<hermes-home>/profiles/indigo/commons/journals/ocas-forge"
cat > "$FORGE_DIR/forge-scan-${TS}.json" << EOF
```

This produces `<hermes-home>/profiles/indigo/commons/journals/ocas-forge/forge-scan-20260625T234355Z.json` instead of the correct `<hermes-home>/profiles/indigo/commons/journals/ocas-forge/2026-06-25/forge-scan-20260625T234355Z.json`.

**Why it matters:** The dispatcher scans date subdirectories for new journals. Files in the parent directory are invisible to the dispatcher's date-based mtime comparison, but they DO appear in `ls` output and can confuse manual audits. They also break the convention that all journals live in `YYYY-MM-DD/` subdirectories.

**Recovery:** If you catch the mistake immediately:
```bash
mv <hermes-home>/profiles/indigo/commons/journals/ocas-forge/forge-scan-TS.json \
   <hermes-home>/profiles/indigo/commons/journals/ocas-forge/2026-06-25/forge-scan-TS.json
```

**Prevention:** Always include `/${DATE_DIR}` in the path. The `mkdir -p` call should use the full path including the date subdirectory, not just the skill root.

## Same Pattern Applies to All OCAS Journals

- `ocas-forge` → `.../ocas-forge/YYYY-MM-DD/forge-scan-TS.json`
- `ocas-dispatch` → `.../ocas-dispatch/YYYY-MM-DD/dispatch-wave-TS.json`
- `ocas-mentor` → `.../ocas-mentor/YYYY-MM-DD/mentor-light-TS.json`
- `ocas-praxis` → `.../ocas-praxis/YYYY-MM-DD/praxis-cron-TS.json`
- `ocas-custodian` → `.../ocas-custodian/YYYY-MM-DD/light-scan-YYYY-MM-DDTHHMMSSZ.json`

Confirmed 2026-06-25: Both forge-scan and dispatch-wave journals written to parent directory instead of date subdirectory. Files were manually moved post-creation.