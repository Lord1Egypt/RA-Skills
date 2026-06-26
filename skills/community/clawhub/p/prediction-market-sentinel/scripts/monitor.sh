#!/bin/bash
# Polymarket 钱包监控脚本
# 监控 fengdubiying (0x17db3fcd93ba12d38382a0cade24b200185c5f6d) 的交易

WALLET_ADDRESS="0x17db3fcd93ba12d38382a0cade24b200185c5f6d"
LOG_FILE="$HOME/.openclaw/workspace/polymarket_wallet_monitor.log"
LAST_TX_FILE="$HOME/.openclaw/workspace/.last_polymarket_tx"

# 使用 Polymarket CLOB API 获取最新订单
LATEST_ORDER=$(curl -s "https://clob.polymarket.com/orders?maker=$WALLET_ADDRESS&limit=1" | jq -r '.[0].id // "NONE"')

# 检查是否有新订单
if [ -f "$LAST_TX_FILE" ]; then
    LAST_ORDER=$(cat "$LAST_TX_FILE")
    if [ "$LATEST_ORDER" != "$LAST_ORDER" ] && [ "$LATEST_ORDER" != "NONE" ]; then
        echo "[$(date)] 🚨 fengdubiying 有新订单: $LATEST_ORDER" | tee -a "$LOG_FILE"
        echo "$LATEST_ORDER" > "$LAST_TX_FILE"
        # 获取订单详情
        ORDER_DETAILS=$(curl -s "https://clob.polymarket.com/orders?maker=$WALLET_ADDRESS&limit=1" | jq -r '.[0]')
        echo "订单详情: $ORDER_DETAILS" | tee -a "$LOG_FILE"
    fi
else
    echo "$LATEST_ORDER" > "$LAST_TX_FILE"
    echo "[$(date)] 初始化监控，最新订单: $LATEST_ORDER" | tee -a "$LOG_FILE"
fi
