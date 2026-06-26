#!/usr/bin/env bash
set -euo pipefail

KEY=""

if [[ "${1:-}" == "--stdin" ]]; then
  IFS= read -r KEY
else
  # Read securely from TTY to avoid leaking key through process arguments.
  printf "Enter x-api-key: "
  stty -echo
  IFS= read -r KEY
  stty echo
  printf "\n"
fi

if [[ -z "$KEY" ]]; then
  echo "Error: empty x-api-key"
  echo "Usage: $0          # interactive"
  echo "   or: echo '<key>' | $0 --stdin"
  exit 1
fi

CONF_DIR="$HOME/.config/nano-banana2"
CONF_FILE="$CONF_DIR/.env"

mkdir -p "$CONF_DIR"
cat > "$CONF_FILE" <<EOF
X_API_KEY=$KEY
EOF
chmod 600 "$CONF_FILE"

echo "x-api-key saved to $CONF_FILE"
