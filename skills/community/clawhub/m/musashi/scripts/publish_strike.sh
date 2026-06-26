#!/usr/bin/env bash
# publish_strike.sh — Publish a STRIKE conviction to 0G Chain
# Usage: ./scripts/publish_strike.sh <token_address> <convergence> <evidence_hash> [chain_id] [agent_id]

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BINARY="$SCRIPT_DIR/musashi-core/musashi-core"

TOKEN="${1:?Usage: publish_strike.sh <token_address> <convergence> <evidence_hash> [chain_id] [agent_id]}"
CONVERGENCE="${2:?Convergence score (3 or 4) required}"
EVIDENCE="${3:?Evidence hash required}"

# Validate env
: "${OG_CHAIN_RPC:?Set OG_CHAIN_RPC}"
: "${OG_CHAIN_PRIVATE_KEY:?Set OG_CHAIN_PRIVATE_KEY}"
: "${CONVICTION_LOG_ADDRESS:?Set CONVICTION_LOG_ADDRESS}"

if [ ! -f "$BINARY" ]; then
    echo "Building musashi-core..."
    cd "$SCRIPT_DIR/musashi-core" && go build -o musashi-core ./cmd/musashi/
fi

CHAIN="${4:-1}"
AGENT_ID="${5:-0}"

exec "$BINARY" strike "$TOKEN" --convergence "$CONVERGENCE" --evidence "$EVIDENCE" --token-chain "$CHAIN" --agent-id "$AGENT_ID"
