#!/usr/bin/env bash
set -euo pipefail

CONFIG_DIR="$HOME/.keepmyclaw"
CONFIG_FILE="$CONFIG_DIR/config"
PASSPHRASE_FILE="$CONFIG_DIR/passphrase"
OPENCLAW_DIR="$HOME/.openclaw"

if [[ ! -f "$CONFIG_FILE" ]]; then
    echo "Error: Config not found. Run setup.sh first." >&2; exit 1
fi
source "$CONFIG_FILE"

if [[ ! -f "$PASSPHRASE_FILE" ]]; then
    echo "Error: Passphrase not found at $PASSPHRASE_FILE" >&2; exit 1
fi

PASSPHRASE="$(cat "$PASSPHRASE_FILE")"
TMPDIR="$(mktemp -d)"
trap 'rm -rf "$TMPDIR"' EXIT

# Determine backup endpoint
BACKUP_ID="${1:-latest}"
ENDPOINT="${CLAWKEEPER_API_URL}/v1/agents/${CLAWKEEPER_AGENT_NAME}/backups/${BACKUP_ID}"

echo "=== ClawKeeper Restore ==="
echo "Agent: ${CLAWKEEPER_AGENT_NAME}"
echo "Backup: ${BACKUP_ID}"
echo

# Download
ENC_FILE="$TMPDIR/backup.tar.gz.enc"
echo "Downloading..."
HTTP_CODE="$(curl -s -o "$ENC_FILE" -w '%{http_code}' \
    -H "Authorization: Bearer ${CLAWKEEPER_API_KEY}" \
    "$ENDPOINT")"

if [[ "$HTTP_CODE" -lt 200 || "$HTTP_CODE" -ge 300 ]]; then
    echo "✗ Download failed (HTTP ${HTTP_CODE})" >&2
    cat "$ENC_FILE" >&2 2>/dev/null
    exit 1
fi
echo "✓ Downloaded"

# Decrypt
TAR_FILE="$TMPDIR/backup.tar.gz"
echo "Decrypting..."
openssl enc -aes-256-cbc -d -salt -pbkdf2 -iter 100000 \
    -in "$ENC_FILE" -out "$TAR_FILE" -pass "pass:${PASSPHRASE}"
echo "✓ Decrypted"

# Preview contents before restoring
echo
echo "Backup contains:"
tar -tzf "$TAR_FILE" | head -30
TOTAL="$(tar -tzf "$TAR_FILE" | wc -l | tr -d ' ')"
[[ "$TOTAL" -gt 30 ]] && echo "  ... and $((TOTAL - 30)) more files"
echo

# Check if this will overwrite existing data
if [[ -d "$OPENCLAW_DIR/workspace" ]] && [[ "$(ls -A "$OPENCLAW_DIR/workspace" 2>/dev/null)" ]]; then
    echo "⚠ WARNING: $OPENCLAW_DIR already has data."
    echo "  Restore will OVERWRITE existing files (but won't delete extras)."
    if [[ -t 0 ]]; then
        read -rp "Continue? [y/N]: " confirm
        [[ "$confirm" != [yY]* ]] && echo "Aborted." && exit 0
    else
        echo "  (Non-interactive mode — proceeding)"
    fi
    echo
fi

# Extract
echo "Restoring to ${OPENCLAW_DIR}..."
mkdir -p "$OPENCLAW_DIR"
tar -xzf "$TAR_FILE" -C "$OPENCLAW_DIR"
echo "✓ Files restored"

# Post-restore summary
echo
echo "=== Restore complete ==="
echo
echo "What was restored:"
[[ -f "$OPENCLAW_DIR/openclaw.json" ]] && echo "  ✓ openclaw.json (agent config)"
[[ -d "$OPENCLAW_DIR/workspace" ]] && echo "  ✓ workspace/ (agent files, memory, skills, projects)"
[[ -d "$OPENCLAW_DIR/credentials" ]] && echo "  ✓ credentials/ (auth tokens)"
[[ -f "$OPENCLAW_DIR/cron/jobs.json" ]] && echo "  ✓ cron/jobs.json (scheduled jobs)"
[[ -d "$OPENCLAW_DIR/agents" ]] && echo "  ✓ agents/ (multi-agent configs)"
for ws in "$OPENCLAW_DIR"/workspace-*; do
    [[ -d "$ws" ]] && echo "  ✓ $(basename "$ws")/ (additional agent workspace)"
done

echo
echo "=== Next Steps ==="
echo "1. Restart OpenClaw to pick up restored config:"
echo "     openclaw gateway restart"
echo "2. Cron jobs will reload automatically on restart."
echo "3. If you restored credentials, verify they still work"
echo "   (API keys don't expire, but OAuth tokens may need re-auth)."
echo "4. Check your agent is responding:"
echo "     openclaw status"
echo
echo "If something looks wrong, your previous data was NOT deleted —"
echo "only overwritten files were replaced. Extras remain untouched."
