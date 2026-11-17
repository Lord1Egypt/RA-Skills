#!/bin/sh
# 分析收尾（脚本接管，无 LLM）：校验 → 生成简报 → 发送简报。
# 在 LLM 填完 key_factors 之后运行。
set -eu
SKILL_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$SKILL_ROOT"
python3 scripts/analyze_check.py
python3 scripts/summary.py brief
python3 scripts/notify.py send summary
