#!/bin/bash

# go-trader Control Script for OpenClaw
# Connects go-trader to Telegram via OpenClaw

COMMAND="\$1"
SUBARG="\$2"

case "$COMMAND" in
    status)
        echo "📊 Trading Status:"
        curl -s localhost:8099/status 2>/dev/null | python3 -m json.tool || echo "❌ go-trader not responding"
        ;;
    health)
        echo "🏥 System Health:"
        curl -s localhost:8099/health 2>/dev/null || echo "❌ go-trader not responding"
        ;;
    logs)
        echo "📋 Recent Trading Logs:"
        journalctl -u go-trader -n 20 --no-pager
        ;;
    emergency_stop)
        echo "🚨 EMERGENCY STOP INITIATED"
        systemctl stop go-trader
        echo "✅ All trading halted"
        ;;
    start)
        echo "▶️ Starting go-trader..."
        systemctl start go-trader
        sleep 2
        curl -s localhost:8099/health
        ;;
    restart)
        echo "🔄 Restarting go-trader..."
        systemctl restart go-trader
        sleep 2
        curl -s localhost:8099/health
        ;;
    *)
        echo "Unknown command: $COMMAND"
        echo "Available: status, health, logs, emergency_stop, start, restart"
        ;;
esac
