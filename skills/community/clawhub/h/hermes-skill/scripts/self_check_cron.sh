#!/bin/bash
# 自进化定时自检脚本
# 每小时运行一次，检查是否需要保存知识、创建技能等

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MEMORY_DIR="$HOME/self-improving"

echo "=== 自检开始: $(date) ==="

# 1. 检查 Nudge 系统
echo "[1/4] 检查 Nudge..."
python3 "$SCRIPT_DIR/nudge_system.py" --check

# 2. 检查记忆统计
echo "[2/4] 检查记忆..."
python3 "$SCRIPT_DIR/memory_tool.py" --stats

# 3. 检查需要评估的 skills
echo "[3/4] 检查技能评估..."
python3 "$SCRIPT_DIR/skill_evaluator.py" --stats

# 4. 清理过期记录
echo "[4/4] 清理过期记录..."
# 清理 30 天前的 nudge log
find "$MEMORY_DIR" -name "*.log" -mtime +30 -delete 2>/dev/null

echo "=== 自检完成: $(date) ==="
