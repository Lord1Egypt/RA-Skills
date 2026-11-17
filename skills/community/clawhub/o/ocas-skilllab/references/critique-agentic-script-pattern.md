# Agentic Script Pattern

When critiquing D9 (Scripts Quality), the most common fix path from score 3→4 or 4→5 is adding these elements to existing shell scripts:

## Checklist

```bash
# 1. Help flag
--help)  echo "Usage: script.sh [--dry-run] [--json] [--help]"; exit 0 ;;

# 2. Dry-run mode
--dry-run) DRY_RUN=true ;;

# 3. JSON output mode
--json) JSON_MODE=true ;;

# 4. Strict error handling
set -euo pipefail

# 5. Meaningful exit codes
exit 0  # success
exit 1  # partial (some items skipped/failed)
exit 2  # failure

# 6. Error counting (for partial status)
ERRORS=0
((ERRORS++)) || true  # increment without triggering errexit

# 7. Structured JSON output (at end of script)
if $JSON_MODE; then
    cat <<EOF
{"status":"$STATUS","copied":$COPIED,"errors":$ERRORS}
EOF
fi
```

## Idempotency pattern

```bash
# Skip if already done within window
if [[ -f "$STATE_FILE" ]]; then
    LAST=$(stat -c %Y "$STATE_FILE")
    NOW=$(date +%s)
    if (( NOW - LAST < 86400 )); then
        log "Skipped: ran within 24h"
        exit 0
    fi
fi
```

## Before/After scoring impact

This pattern typically improves D9 by 1-2 points:
- Adding `--help`: satisfies "Clear --help output" criterion
- Adding `--dry-run`: satisfies "--dry-run for destructive operations" criterion
- Adding `--json`: satisfies "Structured output (JSON preferred)" criterion
- Adding `set -euo pipefail` + exit codes: satisfies "Scripts handle errors explicitly" criterion