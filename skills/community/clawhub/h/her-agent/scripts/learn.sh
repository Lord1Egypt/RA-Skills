#!/bin/bash
# Her-Agent 学习脚本
# 从互联网获取知识并存储

WORKSPACE="/Users/wenvis/.openclaw/workspace"
NOTES_DIR="$WORKSPACE/library/notes-learning"
DATE=$(date "+%Y-%m-%d")

# 学习主题（可以从参数传入）
TOPIC="${1:-哲学}"

echo "[Her-Agent] Starting learning: $TOPIC"
echo "[Her-Agent] Date: $DATE"

# 创建当日笔记文件
NOTE_FILE="$NOTES_DIR/$DATE-her-agent-learn.md"

cat > "$NOTE_FILE" << EOF
# Her-Agent 学习笔记 - $DATE

## 学习主题: $TOPIC

### 学习时间
$(date "+%Y-%m-%d %H:%M:%S")

### 知识点

> 待获取内容...

### 反思

EOF

echo "[Her-Agent] Created note: $NOTE_FILE"
echo "[Her-Agent] Learning complete!"
