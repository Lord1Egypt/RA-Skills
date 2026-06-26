#!/bin/bash
# OpenCLAW Native Watchdog - monitors gateway process and restarts if needed
# Runs every 5 minutes via systemd timer

LOGFILE="$HOME/.openclaw/logs/watchdog.log"
MAX_LOG_LINES=1000

# Check if OpenCLAW gateway is running
PID=$(pgrep -f "openclaw-gateway" | head -1)

if [ -z "$PID" ]; then
    echo "$(date -u '+%Y-%m-%d %H:%M:%S') ALERT: Gateway not running, attempting restart" >> "$LOGFILE"
    
    # Try to restart - this assumes OpenCLAW is managed by systemd or similar
    # For now, just log the issue - manual restart may be needed
    echo "$(date -u '+%Y-%m-%d %H:%M:%S') WARN: Auto-restart not implemented for native setup" >> "$LOGFILE"
    
    # Send Telegram alert
    CONFIG="$HOME/.openclaw/openclaw.json"
    BOT_TOKEN=$(jq -r '.channels.telegram.botToken // empty' "$CONFIG" 2>/dev/null)
    [ -z "$BOT_TOKEN" ] && BOT_TOKEN=$(grep -o '"botToken":"[^"]*"' "$CONFIG" | head -1 | cut -d'"' -f4)
    CHAT_ID="8489519499"
    
    if [ -n "$BOT_TOKEN" ] && [ "$BOT_TOKEN" != "null" ]; then
        MSG="🚨 *OpenCLAW Watchdog Alert*

Gateway process not detected at $(date -u '+%H:%M UTC')

Manual restart may be required.
SSH: mark@100.67.51.118"
        
        curl -s -X POST "https://api.telegram.org/bot${BOT_TOKEN}/sendMessage" \
            -d chat_id="$CHAT_ID" \
            -d parse_mode="Markdown" \
            -d text="$MSG" > /dev/null 2>&1
    fi
else
    # Gateway is running, optional health check could go here
    echo "$(date -u '+%Y-%m-%d %H:%M:%S') OK: Gateway running (PID: $PID)" >> "$LOGFILE"
fi

# Trim log file if too large
if [ -f "$LOGFILE" ]; then
    LINES=$(wc -l < "$LOGFILE")
    if [ "$LINES" -gt "$MAX_LOG_LINES" ]; then
        tail -n "$MAX_LOG_LINES" "$LOGFILE" > "$LOGFILE.tmp"
        mv "$LOGFILE.tmp" "$LOGFILE"
    fi
fi
