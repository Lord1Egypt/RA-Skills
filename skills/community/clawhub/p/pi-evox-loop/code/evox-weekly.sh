#!/usr/bin/env bash
# EvoX 周常（小流量验证）：度量采集 + 生产会话蒸馏诊断（默认 dry-run，不写库）
# 环境变量（可选，公共仓库已去除硬编码绝对路径）：
#   EVOX_NODE : node 可执行路径，默认自动在 PATH 中查找
#   EVOX_ROOT : 部署根目录，默认 $HOME/pi-evox-lab
set -u
NODE="${EVOX_NODE:-node}"
ROOT="${EVOX_ROOT:-$HOME/pi-evox-lab}"
LOG=$ROOT/exp/metrics/run.log
TS=$(date -u +%Y-%m-%dT%H:%M:%SZ)
echo "===== $TS evox-weekly start =====" >> "$LOG"
"$NODE" "$ROOT/code/metrics_collect.mjs" >> "$LOG" 2>&1 || echo "[warn] metrics failed" >> "$LOG"
echo "--- distill diagnostic (dry-run) ---" >> "$LOG"
"$NODE" "$ROOT/code/distill_sessions.mjs" --days 7 --dry-run >> "$LOG" 2>&1 || echo "[warn] distill diagnostic failed" >> "$LOG"
echo "===== $TS evox-weekly done =====" >> "$LOG"
