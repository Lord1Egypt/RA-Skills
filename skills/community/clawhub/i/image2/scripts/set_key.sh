#!/usr/bin/env bash
set -euo pipefail

CONFIG_DIR="$HOME/.config/image2"
ENV_FILE="$CONFIG_DIR/.env"

usage() {
  cat <<'EOF'
Usage:
  set_key.sh                # interactive input
  set_key.sh --stdin        # read key from stdin
  set_key.sh "<x-api-key>"   # pass as arg (less secure)
EOF
}

KEY=""
MODE="interactive"

if [[ "${1:-}" == "-h" || "${1:-}" == "--help" ]]; then
  usage
  exit 0
fi

if [[ "${1:-}" == "--stdin" ]]; then
  MODE="stdin"
elif [[ -n "${1:-}" ]]; then
  MODE="arg"
  KEY="$1"
fi

if [[ "$MODE" == "interactive" ]]; then
  read -r -s -p "Enter X_API_KEY: " KEY
  echo
elif [[ "$MODE" == "stdin" ]]; then
  IFS= read -r KEY
fi

if [[ -z "$KEY" ]]; then
  echo "Error: empty key" >&2
  exit 1
fi

mkdir -p "$CONFIG_DIR"
cat >"$ENV_FILE" <<EOF
X_API_KEY=$KEY
EOF
chmod 600 "$ENV_FILE"

MASKED="${KEY:0:4}****${KEY: -4}"
echo "Saved X_API_KEY to $ENV_FILE"
echo "Key preview: $MASKED"
