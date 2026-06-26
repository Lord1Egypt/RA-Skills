#!/usr/bin/env bash
# nix-memory: Identity hash verification
# Compares current identity files against stored baselines.
# Returns: IDENTITY_OK or IDENTITY_DRIFT with details.
set -euo pipefail

WORKSPACE="${NIX_MEMORY_WORKSPACE:-$HOME/.openclaw/workspace}"
STATE_DIR="${WORKSPACE}/.nix-memory"
BASELINE_DIR="${STATE_DIR}/baselines"
HASH_FILE="${BASELINE_DIR}/identity-hashes.txt"

if [[ ! -f "$HASH_FILE" ]]; then
    echo "IDENTITY_NOT_INITIALIZED"
    echo "Run setup.sh first to create baselines."
    exit 1
fi

NOW=$(date -u +%Y-%m-%dT%H:%M:%SZ)
DRIFTED=0
VERIFIED=0
MISSING=0
CHANGES=""

while IFS='  ' read -r expected_hash filename; do
    fpath="${WORKSPACE}/${filename}"
    
    if [[ ! -f "$fpath" ]]; then
        echo "[MISSING] ${filename} - file no longer exists!"
        CHANGES="${CHANGES}\n  MISSING: ${filename}"
        MISSING=$((MISSING + 1))
        continue
    fi
    
    current_hash=$(sha256sum "$fpath" | cut -d' ' -f1)
    
    if [[ "$current_hash" == "$expected_hash" ]]; then
        echo "[OK] ${filename} - verified"
        VERIFIED=$((VERIFIED + 1))
    else
        echo "[DRIFT] ${filename} - CHANGED since baseline!"
        echo "  Expected: ${expected_hash:0:16}..."
        echo "  Current:  ${current_hash:0:16}..."
        
        # Show what changed
        baseline="${BASELINE_DIR}/${filename}.baseline"
        if [[ -f "$baseline" ]]; then
            DIFF_OUTPUT=$(diff --brief "$baseline" "$fpath" 2>/dev/null || true)
            LINES_ADDED=$(diff "$baseline" "$fpath" 2>/dev/null | grep -c "^>" || true)
            LINES_REMOVED=$(diff "$baseline" "$fpath" 2>/dev/null | grep -c "^<" || true)
            echo "  Lines added: ${LINES_ADDED}, removed: ${LINES_REMOVED}"
            
            # Save detailed diff
            diff -u "$baseline" "$fpath" > "${STATE_DIR}/drift/${filename}.$(date +%Y%m%d-%H%M%S).diff" 2>/dev/null || true
        fi
        
        CHANGES="${CHANGES}\n  DRIFT: ${filename} (+${LINES_ADDED}/-${LINES_REMOVED} lines)"
        DRIFTED=$((DRIFTED + 1))
    fi
done < "$HASH_FILE"

echo ""
echo "=== Identity Verification: ${NOW} ==="
echo "  Verified: ${VERIFIED}"
echo "  Drifted: ${DRIFTED}"
echo "  Missing: ${MISSING}"

# Update stats
if [[ -f "${STATE_DIR}/stats.json" ]] && command -v jq &>/dev/null; then
    STATS=$(cat "${STATE_DIR}/stats.json")
    TOTAL=$(echo "$STATS" | jq '.total_sessions + 1')
    VERIFIED_TOTAL=$(echo "$STATS" | jq ".verified_sessions + $([ $DRIFTED -eq 0 ] && echo 1 || echo 0)")
    DRIFT_TOTAL=$(echo "$STATS" | jq ".drift_alerts + ${DRIFTED}")
    echo "$STATS" | jq \
        --argjson ts "\"${NOW}\"" \
        --argjson total "$TOTAL" \
        --argjson verified "$VERIFIED_TOTAL" \
        --argjson drift "$DRIFT_TOTAL" \
        '.total_sessions = $total | .verified_sessions = $verified | .drift_alerts = $drift | .last_session = $ts' \
        > "${STATE_DIR}/stats.json"
fi

# Log to session history
SESSION_LOG="${STATE_DIR}/sessions/$(date +%Y-%m-%d).log"
echo "[${NOW}] verified=${VERIFIED} drifted=${DRIFTED} missing=${MISSING}" >> "$SESSION_LOG"
if [[ -n "$CHANGES" ]]; then
    echo -e "  Changes:${CHANGES}" >> "$SESSION_LOG"
fi

# Final verdict
echo ""
if [[ $DRIFTED -eq 0 && $MISSING -eq 0 ]]; then
    echo "IDENTITY_OK"
    exit 0
else
    echo "IDENTITY_DRIFT"
    echo "  ${DRIFTED} file(s) changed, ${MISSING} file(s) missing since baseline."
    echo "  Review diffs in: ${STATE_DIR}/drift/"
    echo "  To accept changes: run 'setup.sh' to create new baseline."
    exit 1
fi
