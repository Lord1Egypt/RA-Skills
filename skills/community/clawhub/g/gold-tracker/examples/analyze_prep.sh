#!/bin/sh
# 分析准备（脚本接管，无 LLM）：采集新闻 → 生成分析骨架。
# 之后由 LLM 只填 key_factors 推理内容，再跑 examples/analyze_finish.sh。
set -eu
SKILL_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$SKILL_ROOT"
python3 scripts/news_collect.py
python3 scripts/analyze_scaffold.py
