# Journal Template: Timestamp-Based Scan Journal

Forge scan journals use a dual-timestamp naming pattern: the filename carries a compact timestamp (`YYYYMMDDTHHMMSSZ`) while the internal `timestamp` field carries ISO format. Both must reference the same instant.

## Pattern

```bash
TS=$(date -u +%Y%m%dT%H%M%SZ)
JOURNAL_DIR="<hermes-home>/profiles/indigo/commons/journals/ocas-forge/$(date -u +%Y-%m-%d)"
mkdir -p "$JOURNAL_DIR"

cat > "$JOURNAL_DIR/forge-scan-${TS}.json" << 'EOF'
{
  "schema": "forge-journal-v1",
  "run_id": "forge-scan-TS_PLACEHOLDER",
  "timestamp": "TS_ISO",
  "action": {"result": "no_op", "findings": {"unprocessed_proposals": 0, "unprocessed_decisions": 0, "pending_variants": 0}},
  "outcome": "success"
}
EOF

sed -i "s/TS_PLACEHOLDER/${TS}/g" "$JOURNAL_DIR/forge-scan-${TS}.json"
sed -i "s/TS_ISO/$(date -u +%Y-%m-%dT%H:%M:%SZ)/g" "$JOURNAL_DIR/forge-scan-${TS}.json"
```

## Pitfall: Two `$(date)` calls

The `sed` substitution approach uses two separate `$(date)` calls. If the clock rolls over between them (e.g., minute boundary), the filename timestamp and internal timestamp will differ. This happened in dispatch #31 (3-minute discrepancy).

**Fix:** Compose the timestamp into a variable first, then use the variable for both filename and content:

```bash
TS=$(date -u +%Y%m%dT%H%M%SZ)
TS_ISO=$(date -u +%Y-%m-%dT%H:%M:%SZ)
# Use $TS for filename, $TS_ISO for content — but both from the SAME epoch second
```

Or better: derive both formats from a single `date` call using `awk` or parameter expansion.

## No-op vs Success distinction

- **No-op journal**: `action.result == "no_op"` with all finding counts at 0. Written when queue is clean.
- **Action journal**: `action.result` describes what was done (processed proposals, applied fixes).
- Both have `outcome: "success"` — the distinction is in `action`, not `outcome`.