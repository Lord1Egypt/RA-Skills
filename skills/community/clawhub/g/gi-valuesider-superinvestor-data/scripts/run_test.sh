#!/usr/bin/env bash
# 本地测试：不联网用 sample 数据跑解析器，验证流程
set -e
cd "$(dirname "$0")/.."
GURU=mason-hawkins-longleaf-partners

echo "=== 1. 解析 sample 持仓 ==="
python scripts/parse_fetched_content.py --type portfolio \
  --file test/sample_portfolio.txt \
  --guru-slug "$GURU" \
  --source-url "https://valuesider.com/guru/$GURU/portfolio" \
  | head -40

echo ""
echo "=== 2. 解析 sample 交易活动 ==="
python scripts/parse_fetched_content.py --type activity \
  --file test/sample_activity.txt \
  --guru-slug "$GURU" \
  --source-url "https://valuesider.com/guru/$GURU/portfolio-activity" \
  | head -50

echo ""
echo "=== 测试通过：解析器工作正常 ==="
