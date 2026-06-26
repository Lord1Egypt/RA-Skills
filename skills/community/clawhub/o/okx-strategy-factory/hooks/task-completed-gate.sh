#!/usr/bin/env bash
# TaskCompleted hook — 质量门禁 (multi-strategy)
# Exit 0: 允许完成 | Exit 2: 拒绝，附反馈

set -euo pipefail

TEAMMATE="${CLAUDE_TEAMMATE_NAME:-}"
STRATEGY="${CLAUDE_STRATEGY_NAME:-}"

# 如果未指定策略，尝试从最近修改的 Strategy/*/ 推断
if [[ -z "$STRATEGY" ]]; then
    STRATEGY=$(ls -dt Strategy/*/ 2>/dev/null | head -1 | xargs basename 2>/dev/null || true)
fi

# 仍然为空则放行
if [[ -z "$STRATEGY" ]]; then
    exit 0
fi

if [[ "$TEAMMATE" == "strategy" ]]; then
    V=$(ls -d "Strategy/$STRATEGY/Script/v"*/ 2>/dev/null | sort -V | tail -1)
    [ -z "$V" ] && { echo "FEEDBACK: Strategy/$STRATEGY/Script/ 下无版本目录"; exit 2; }
    for f in config.json risk-profile.json README.md; do
        [ ! -f "$V/$f" ] && { echo "FEEDBACK: 缺少 $V/$f"; exit 2; }
    done
    ls "$V"/strategy.{js,ts,py} &>/dev/null 2>&1 || { echo "FEEDBACK: 缺少策略主文件"; exit 2; }
    for field in max_position_size_pct stop_loss_pct max_drawdown_pct gas_budget_usd slippage_tolerance_pct; do
        grep -q "\"$field\"" "$V/risk-profile.json" || { echo "FEEDBACK: risk-profile.json 缺少字段: $field"; exit 2; }
    done
fi

if [[ "$TEAMMATE" == "backtest" ]]; then
    V=$(ls -d "Strategy/$STRATEGY/Backtest/v"*/ 2>/dev/null | sort -V | tail -1)
    [ -z "$V" ] && { echo "FEEDBACK: Strategy/$STRATEGY/Backtest/ 下无回测输出目录"; exit 2; }
    # 至少有报告文件
    ls "$V"/*.{json,md} &>/dev/null 2>&1 || { echo "FEEDBACK: 回测目录缺少报告文件"; exit 2; }
fi

if [[ "$TEAMMATE" == "publish" ]]; then
    # 检查策略根目录下的 manifest.json
    [ ! -f "$STRATEGY/manifest.json" ] && { echo "FEEDBACK: $STRATEGY/ 缺少 manifest.json"; exit 2; }
fi

exit 0
