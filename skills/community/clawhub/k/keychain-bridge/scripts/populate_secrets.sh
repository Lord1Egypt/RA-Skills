#!/bin/bash
# Populate secrets files from keychain before service start.
# Group B: secrets that bash scripts or config files need as files on disk.

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SECRETS_DIR="${SECRETS_DIR:-$HOME/.openclaw/secrets}"
ACCOUNT="${ACCOUNT:-moltbot}"

# --- Group B services (expected on disk) ---
GROUP_B_SERVICES=(
    "arr-api-keys"
    "claude-code-token"
    "clawmarket-wallet-key"
    "gitea-api"
    "google-ai-api-key"
    "ha-token"
    "hooks-token"
    "influxdb-token"
    "openrouter-api-key"
)

mkdir -p "$SECRETS_DIR"

populated=0
failed=0

for svc in "${GROUP_B_SERVICES[@]}"; do
    value=$(python3 "$SCRIPT_DIR/get_secret.py" "$svc" --account "$ACCOUNT" 2>/dev/null)
    if [ -n "$value" ]; then
        echo -n "$value" > "$SECRETS_DIR/$svc"
        chmod 600 "$SECRETS_DIR/$svc"
        populated=$((populated + 1))
    else
        echo "WARNING: $svc not found in keychain" >&2
        failed=$((failed + 1))
    fi
done

echo "Populated $populated secrets ($failed failed) into $SECRETS_DIR"
