#!/usr/bin/env bash
# 试点演示：cad-file-reader 写状态 → 土建算量读状态（同一 bus）
set -euo pipefail
SKILLBUS_STATE_DIR="${SKILLBUS_STATE_DIR:-$(mktemp -d)/skillbus}"
export SKILLBUS_STATE_DIR
HERE="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
BUS="$(dirname "$HERE")/skillbus.py"
echo "★ 1. cad-file-reader 解析完成后写入契约"
python3 "$BUS" push-project-state --project 示例项目 --building B栋 --floor F2 \
  --skill cad-file-reader --entry-file "$HERE/demo_state.json"
echo
echo "★ 2. 土建算量开工前读取共享状态（不再重复读图）"
python3 "$BUS" get-project-state --project 示例项目 --building B栋 --floor F2
echo
echo "★ 3. 解析契约 schema 元数据"
python3 "$BUS" resolve-contract --contract cad-file-reader/v0
