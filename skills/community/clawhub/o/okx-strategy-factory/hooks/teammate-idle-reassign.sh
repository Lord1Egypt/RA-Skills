#!/usr/bin/env bash
# TeammateIdle hook — 空闲时检查待办 (multi-strategy)
# Exit 0: 允许空闲 | Exit 2: 分配工作

set -euo pipefail

TEAMMATE="${CLAUDE_TEAMMATE_NAME:-}"

case "$TEAMMATE" in
    backtest)
        # 遍历所有策略，检查未回测的版本
        for strat_dir in Strategy/*/; do
            [ ! -d "$strat_dir" ] && continue
            strat=$(basename "$strat_dir")
            for v in "Strategy/$strat/Script/v"*/; do
                [ ! -d "$v" ] && continue
                ver=$(basename "$v")
                [ ! -d "Strategy/$strat/Backtest/$ver" ] && [ -f "$v/risk-profile.json" ] && {
                    echo "FEEDBACK: $strat/$ver 未回测。请验证 $v"; exit 2; }
            done
        done ;;
esac

exit 0
