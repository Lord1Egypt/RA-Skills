#!/bin/bash
# huo15-reasonix-bridge: 列 Reasonix 项目会话
# 用法: bash list-sessions.sh <项目根目录>
# 示例: bash list-sessions.sh "/Users/jobzhao/workspace/projects/openclaw/marketing_docs"

PROJECT_ROOT="$1"

if [ -z "$PROJECT_ROOT" ]; then
  echo "用法: $0 <项目根目录>"
  exit 1
fi

# 将路径转为 Reasonix 哈希目录名
HASH_DIR=$(echo "$PROJECT_ROOT" | sed 's|/|-|g')
SESSIONS_DIR="$HOME/.reasonix/projects/$HASH_DIR/sessions"

if [ ! -d "$SESSIONS_DIR" ]; then
  echo "错误: 项目 $PROJECT_ROOT 不存在会话目录"
  echo "路径: $SESSIONS_DIR"
  exit 1
fi

echo "项目: $PROJECT_ROOT"
echo "会话:"
echo "---"

for f in "$SESSIONS_DIR"/*.jsonl; do
  [ -f "$f" ] || continue
  fname=$(basename "$f")
  # 提取会话 ID（去掉 .jsonl 后缀）
  sid="${fname%.jsonl}"
  # 读取文件大小
  size=$(wc -c < "$f" | tr -d ' ')
  # 读取修改时间
  mtime=$(stat -f "%Sm" "$f" 2>/dev/null || stat -c "%y" "$f" 2>/dev/null)
  echo "$sid | $size bytes | $mtime"
done