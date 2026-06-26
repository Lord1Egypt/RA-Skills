#!/bin/bash
# 彩票预测技能 - 自动发布脚本
# 每 30 分钟重试一次，成功后停止

MAX_ATTEMPTS=10
ATTEMPT=1

while [ $ATTEMPT -le $MAX_ATTEMPTS ]; do
  echo "=== 自动发布尝试 $ATTEMPT/$MAX_ATTEMPTS ==="
  echo "时间：$(date '+%Y-%m-%d %H:%M:%S')"
  
  SKILL_PATH="/Users/lic/.openclaw/workspace/skills/lottery-predictor-v2.15"
  
  # 尝试发布
  clawhub publish "$SKILL_PATH" \
    --slug lottery-predictor-v2-15 \
    --name "彩票预测 V2.15" \
    --version 2.15.0 \
    --changelog "初始发布：基于 V2.15 数学模型的彩票预测技能" \
    2>&1 | tee /tmp/publish_attempt_$ATTEMPT.log
  
  # 检查是否成功
  if grep -q "Published" /tmp/publish_attempt_$ATTEMPT.log; then
    echo "✅ 发布成功！"
    echo "✅ 发布成功！" >> /Users/lic/.openclaw/workspace/skills/lottery-predictor-v2.15/PUBLISH_RESULT.md
    exit 0
  else
    echo "❌ 失败，等待 30 分钟后重试..."
    echo "尝试 $ATTEMPT 失败：$(date '+%Y-%m-%d %H:%M:%S')" >> /Users/lic/.openclaw/workspace/skills/lottery-predictor-v2.15/PUBLISH_RESULT.md
    sleep 1800  # 30 分钟
  fi
  
  ATTEMPT=$((ATTEMPT + 1))
done

echo "❌ 已达到最大重试次数，发布失败"
echo "❌ 已达到最大重试次数，发布失败" >> /Users/lic/.openclaw/workspace/skills/lottery-predictor-v2.15/PUBLISH_RESULT.md
