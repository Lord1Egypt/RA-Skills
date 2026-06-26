#!/bin/bash
# 龙虾记忆大师 - Context 检查脚本
# Created by: 天道桐哥 & AI龙虾元龙

echo "🦞 龙虾记忆大师 - Context 检查"
echo "=============================="

# 检查环境变量中的 context 使用情况
# 实际使用时由 OpenClaw 内部提供

echo "检查记忆系统状态..."

WORKSPACE="${OPENCLAW_WORKSPACE:-/root/.openclaw/workspace}"

# 检查必要文件
files=(
  "MEMORY.md"
  "SESSION-STATE.md"
  "HEARTBEAT.md"
  "memory/working-buffer.md"
)

for file in "${files[@]}"; do
  if [ -f "$WORKSPACE/$file" ]; then
    echo "✅ $file"
  else
    echo "❌ $file (缺失)"
  fi
done

echo "=============================="
echo "检查完成！"
