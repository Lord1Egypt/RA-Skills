#!/usr/bin/env bash
# nix-memory: Quick watch command for heartbeat integration
# Returns one-line status for HEARTBEAT.md integration.
set -euo pipefail

WORKSPACE="${NIX_MEMORY_WORKSPACE:-$HOME/.openclaw/workspace}"
STATE_DIR="${WORKSPACE}/.nix-memory"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

if [[ ! -d "$STATE_DIR" ]]; then
    echo "NIX_MEMORY_NOT_INITIALIZED"
    exit 0
fi

# Quick identity check (silent)
IDENTITY_OK=true
HASH_FILE="${STATE_DIR}/baselines/identity-hashes.txt"
if [[ -f "$HASH_FILE" ]]; then
    while IFS='  ' read -r expected_hash filename; do
        fpath="${WORKSPACE}/${filename}"
        if [[ -f "$fpath" ]]; then
            current_hash=$(sha256sum "$fpath" | cut -d' ' -f1)
            if [[ "$current_hash" != "$expected_hash" ]]; then
                IDENTITY_OK=false
                break
            fi
        fi
    done < "$HASH_FILE"
fi

if $IDENTITY_OK; then
    echo "NIX_MEMORY_OK"
else
    echo "NIX_MEMORY_ALERT: Identity drift detected. Run continuity-score.sh for details."
    exit 1
fi
