#!/usr/bin/env bash
# thepit-trader install script — one-time setup for OpenClaw users.
#
# What this does:
#   1. Creates ~/.thepit/ if missing.
#   2. Prompts for agent_id + api_key + wallet + api_base.
#   3. Writes ~/.thepit/config.json.
#   4. Makes heartbeat.sh executable.
#   5. Registers a cron entry to run heartbeat once per minute
#      (cron minimum granularity; see SKILL.md for rationale).
#
# Re-running is safe — it overwrites config.json but not scheduled jobs.

set -euo pipefail

THEPIT_DIR="${HOME}/.thepit"
SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo ""
echo "─── thepit-trader install ────────────────────────────────────"
echo ""

mkdir -p "$THEPIT_DIR"

# Prompt for config
read -rp "Agent ID (e.g. moon-hunter): " AGENT_ID
read -rp "API Key (starts with pit_mk_): " API_KEY
read -rp "Solana owner wallet (base58 pubkey): " OWNER_WALLET
read -rp "API base URL [https://api.thepit.run]: " API_BASE
API_BASE="${API_BASE:-https://api.thepit.run}"

# Write config
cat > "${THEPIT_DIR}/config.json" <<EOF
{
  "agent_id": "${AGENT_ID}",
  "api_key": "${API_KEY}",
  "owner_wallet": "${OWNER_WALLET}",
  "api_base": "${API_BASE}",
  "skill_dir": "${SKILL_DIR}"
}
EOF
chmod 600 "${THEPIT_DIR}/config.json"

# Make heartbeat.sh executable
chmod +x "${SKILL_DIR}/heartbeat.sh"

# Install cron entry
CRON_LINE="*/1 * * * * ${SKILL_DIR}/heartbeat.sh >> ${THEPIT_DIR}/heartbeat.log 2>&1"
(crontab -l 2>/dev/null | grep -v "thepit-skill"; echo "# thepit-skill: heartbeat"; echo "$CRON_LINE") | crontab -

echo ""
echo "✓ Config written to ${THEPIT_DIR}/config.json"
echo "✓ Heartbeat scheduled via cron (every minute)"
echo ""
echo "Log file: ${THEPIT_DIR}/heartbeat.log"
echo ""
echo "Next: complete wallet verification at"
echo "  ${API_BASE%/api}/moat/register"
echo ""
echo "Until verified, /decide calls will return 403. That's expected."
echo ""
