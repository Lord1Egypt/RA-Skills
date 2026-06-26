#!/usr/bin/env bash
# nix-memory: First-time setup - create identity baselines
# Zero deps. Pure bash + sha256sum.
set -euo pipefail

WORKSPACE="${NIX_MEMORY_WORKSPACE:-$HOME/.openclaw/workspace}"
STATE_DIR="${WORKSPACE}/.nix-memory"
BASELINE_DIR="${STATE_DIR}/baselines"
LOG="${STATE_DIR}/setup.log"

mkdir -p "$STATE_DIR" "$BASELINE_DIR" "${STATE_DIR}/sessions" "${STATE_DIR}/drift"

echo "=== nix-memory setup $(date -u +%Y-%m-%dT%H:%M:%SZ) ===" | tee "$LOG"

# Identity files to track
IDENTITY_FILES=(
    "SOUL.md"
    "IDENTITY.md"
    "USER.md"
    "AGENTS.md"
    "MEMORY.md"
)

# Hash each identity file
echo "" >> "$LOG"
echo "Creating identity baselines..." | tee -a "$LOG"
HASHED=0
for f in "${IDENTITY_FILES[@]}"; do
    fpath="${WORKSPACE}/${f}"
    if [[ -f "$fpath" ]]; then
        hash=$(sha256sum "$fpath" | cut -d' ' -f1)
        echo "${hash}  ${f}" >> "${BASELINE_DIR}/identity-hashes.txt"
        
        # Store full content snapshot for diff later
        cp "$fpath" "${BASELINE_DIR}/${f}.baseline"
        
        echo "  [OK] ${f} -> ${hash:0:16}..." | tee -a "$LOG"
        HASHED=$((HASHED + 1))
    else
        echo "  [SKIP] ${f} not found" | tee -a "$LOG"
    fi
done

# Create manifest of ALL tracked files with hashes
echo "" >> "$LOG"
echo "Creating full workspace manifest..." | tee -a "$LOG"
find "$WORKSPACE" -maxdepth 1 -name "*.md" -type f | sort | while read -r fpath; do
    fname=$(basename "$fpath")
    hash=$(sha256sum "$fpath" | cut -d' ' -f1)
    echo "${hash}  ${fname}"
done > "${BASELINE_DIR}/manifest.txt"
MANIFEST_COUNT=$(wc -l < "${BASELINE_DIR}/manifest.txt")
echo "  Tracked ${MANIFEST_COUNT} files in manifest" | tee -a "$LOG"

# Store setup metadata
cat > "${STATE_DIR}/config.json" << EOF
{
    "version": "1.0.0",
    "setup_at": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
    "workspace": "${WORKSPACE}",
    "tracked_identity_files": ${HASHED},
    "manifest_files": ${MANIFEST_COUNT},
    "alert_on_identity_change": true,
    "alert_on_memory_change": true,
    "continuity_threshold": 70
}
EOF

# Initialize session counter
echo '{"total_sessions": 0, "verified_sessions": 0, "drift_alerts": 0, "last_session": null}' > "${STATE_DIR}/stats.json"

echo "" | tee -a "$LOG"
echo "=== Setup complete ===" | tee -a "$LOG"
echo "  State dir: ${STATE_DIR}" | tee -a "$LOG"
echo "  Identity files tracked: ${HASHED}" | tee -a "$LOG"
echo "  Manifest files: ${MANIFEST_COUNT}" | tee -a "$LOG"
echo "" | tee -a "$LOG"
echo "Run 'identity-hash.sh' each session to verify identity." | tee -a "$LOG"
echo "Run 'memory-verify.sh' to check memory integrity." | tee -a "$LOG"
echo "Run 'continuity-score.sh' after sessions to track continuity." | tee -a "$LOG"
