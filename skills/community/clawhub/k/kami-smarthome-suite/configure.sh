#!/bin/bash
# ============================================================
# Kami SmartHome Suite - Centralized Configuration (CLI)
# ============================================================
# Unified entry point for configuring all Kami SmartHome skills.
#   bash configure.sh                 # interactive setup
#   bash configure.sh sk_live_xxx     # set API key + distribute
#   bash configure.sh --distribute    # distribute existing config
#   bash configure.sh --show          # show current config
# ============================================================
set -e

SKILL_DIR="$(dirname "$(realpath "$0")")"
PY_SCRIPT="$SKILL_DIR/configure.py"

if [ ! -f "$PY_SCRIPT" ]; then
    echo "[x] configure.py not found in $SKILL_DIR" >&2
    exit 2
fi

if ! command -v python3 &> /dev/null; then
    echo "[x] python3 not found. Install: sudo apt install -y python3" >&2
    exit 2
fi

# Forward args. If the first positional arg looks like a key, pass it as --api-key.
ARGS=()
if [ "${1:-}" != "" ] && [[ "${1}" != --* ]]; then
    ARGS+=("--api-key" "$1")
    shift
fi
ARGS+=("$@")

exec python3 "$PY_SCRIPT" "${ARGS[@]}"
