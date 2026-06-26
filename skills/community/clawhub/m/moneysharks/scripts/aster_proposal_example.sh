#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"

# shellcheck disable=SC1091
source "$SCRIPT_DIR/aster_env.example.sh"

python3 "$SCRIPT_DIR/aster_proposal_runner.py" \
  "$SKILL_DIR/config.example.json" \
  BTCUSDT \
  BUY
