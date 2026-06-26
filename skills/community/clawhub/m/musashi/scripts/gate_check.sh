#!/usr/bin/env bash
# gate_check.sh — Run MUSASHI gate pipeline on a token
# Usage: ./scripts/gate_check.sh <token_address> [chain_id]

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BINARY="$SCRIPT_DIR/musashi-core/musashi-core"

TOKEN="${1:?Usage: gate_check.sh <token_address> [chain_id]}"
CHAIN="${2:-1}"

if [ ! -f "$BINARY" ]; then
    echo "Building musashi-core..."
    cd "$SCRIPT_DIR/musashi-core" && go build -o musashi-core ./cmd/musashi/
fi

exec "$BINARY" gates "$TOKEN" --chain "$CHAIN" --output json
