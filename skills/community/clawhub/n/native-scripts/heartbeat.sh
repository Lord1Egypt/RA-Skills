#!/bin/bash
# OpenCLAW Daily Heartbeat (Native) - sends status + cost summary to Telegram
# Runs daily at 18:00 UTC (7am NZDT) via systemd timer

CONFIG="$HOME/.openclaw/openclaw.json"
WORKSPACE="$HOME/.openclaw/workspace"

# Get Telegram creds
BOT_TOKEN=$(jq -r '.channels.telegram.botToken // empty' "$CONFIG" 2>/dev/null)
[ -z "$BOT_TOKEN" ] && BOT_TOKEN=$(grep -o '"botToken":"[^"]*"' "$CONFIG" | head -1 | cut -d'"' -f4)
CHAT_ID="8489519499"

# Gateway status - check if OpenCLAW process is running
PID=$(pgrep -f "openclaw-gateway" | head -1)
if [ -n "$PID" ]; then
    STATUS="running"
    HEALTH="healthy"
else
    STATUS="stopped"
    HEALTH="unhealthy"
fi

# Get model from config
MODEL=$(jq -r '.models.defaults.text // "unknown"' "$CONFIG" 2>/dev/null | sed 's|moonshot/||')

# Count sessions
SESSION_DIR="$HOME/.openclaw/agents/main/sessions"
SESSIONS=$(ls -1 "$SESSION_DIR"/*.jsonl 2>/dev/null | wc -l)

# System uptime
UPTIME=$(uptime -p 2>/dev/null || echo "unknown")

# System resources
DISK=$(df -h / | awk 'NR==2{printf "%s/%s (%s)", $3, $2, $5}')
MEM=$(free -m | awk '/Mem:/{used=$3; total=$2; pct=int(used/total*100); printf "%dMi/%.1fGi (%d%%)", used, total/1024, pct}' 2>/dev/null || echo "unknown")

# Watchdog alerts in last 24h
ALERTS=0
if [ -f ~/.openclaw/logs/watchdog.log ]; then
    ALERTS=$(grep "$(date -u -d '1 day ago' +%Y-%m-%d)" ~/.openclaw/logs/watchdog.log 2>/dev/null | wc -l)
fi

# Pending OS updates (requires sudo - skip for now)
UPDATES="check manually"

# Cost data (24h)
COST_24H="$($HOME/openclaw/cost-tracker.sh json 24h 2>/dev/null || echo '{}')"
COST_ALL="$($HOME/openclaw/cost-tracker.sh json all 2>/dev/null || echo '{}')"

COST_24H_TOTAL=$(echo "$COST_24H" | ~/.local/bin/jq -r '.summary.totalCostUSD // 0 | . * 10000 | round / 10000' 2>/dev/null || echo "0")
COST_24H_MSGS=$(echo "$COST_24H" | ~/.local/bin/jq -r '.summary.totalMessages // 0' 2>/dev/null || echo "0")
COST_24H_TOKENS=$(echo "$COST_24H" | ~/.local/bin/jq -r '.summary.totalTokens // 0' 2>/dev/null || echo "0")

COST_ALL_TOTAL=$(echo "$COST_ALL" | ~/.local/bin/jq -r '.summary.totalCostUSD // 0 | . * 10000 | round / 10000' 2>/dev/null || echo "0")
COST_ALL_MSGS=$(echo "$COST_ALL" | ~/.local/bin/jq -r '.summary.totalMessages // 0' 2>/dev/null || echo "0")

# Build message
MSG="🌅 *OpenCLAW Daily Heartbeat (Native)*
$(date -u '+%Y-%m-%d %H:%M UTC') | $(TZ=Pacific/Auckland date '+%H:%M NZDT')

🟢 *Gateway*
Status: ${STATUS} (${HEALTH})
Model: ${MODEL} | Sessions: ${SESSIONS}
Uptime: ${UPTIME}

💰 *Costs (24h)*
Messages: ${COST_24H_MSGS} | Tokens: ${COST_24H_TOKENS}
Spend: \$${COST_24H_TOTAL}

📊 *Costs (all time)*
Messages: ${COST_ALL_MSGS}
Total spend: \$${COST_ALL_TOTAL}

🖥️ *System*
Disk: ${DISK}
Memory: ${MEM}
Watchdog alerts (24h): ${ALERTS}
Pending updates: ${UPDATES}

🔗 SSH: mark@100.67.51.118"

# Send
if [ -n "$BOT_TOKEN" ] && [ "$BOT_TOKEN" != "null" ]; then
    curl -s -X POST "https://api.telegram.org/bot${BOT_TOKEN}/sendMessage" \
        -d chat_id="$CHAT_ID" \
        -d parse_mode="Markdown" \
        -d text="$MSG" > /dev/null 2>&1
    echo "Heartbeat sent at $(date -u)"
else
    echo "Error: No bot token found"
    exit 1
fi
