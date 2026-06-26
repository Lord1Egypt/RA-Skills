#!/bin/bash
# ingest.sh — 文档入库
# 用法:
#   ./ingest.sh --url "https://..."
#   ./ingest.sh --file /path/to/file.pdf --type paper
#   ./ingest.sh --text "我的笔记内容" --title "笔记标题" --type note

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
KB_ROOT="$(dirname "$SCRIPT_DIR")"
RAW_DIR="$KB_ROOT/raw"
CACHE_DIR="$KB_ROOT/cache"

# 默认值
TYPE="article"
TITLE=""
CONTENT=""
SOURCE_URL=""
SOURCE_FILE=""
DATE=$(date +%Y-%m-%d)

# 解析参数
while [[ $# -gt 0 ]]; do
  case $1 in
    --url)
      SOURCE_URL="$2"
      TITLE="$2"
      shift 2
      ;;
    --file)
      SOURCE_FILE="$2"
      TYPE="$3"
      shift 3
      ;;
    --text)
      CONTENT="$2"
      shift 2
      ;;
    --title)
      TITLE="$2"
      shift 2
      ;;
    --type)
      TYPE="$2"
      shift 2
      ;;
    *)
      echo "未知参数: $1"
      exit 1
      ;;
  esac
done

# 检查必填
if [ -z "$SOURCE_URL" ] && [ -z "$SOURCE_FILE" ] && [ -z "$CONTENT" ]; then
  echo "错误: 必须提供 --url、--file 或 --text"
  echo "用法:"
  echo "  ./ingest.sh --url 'https://...'"
  echo "  ./ingest.sh --text '内容' --title '标题'"
  exit 1
fi

# 确定类型
case $TYPE in
  paper|article|note|code|web) ;;
  *) TYPE="article" ;;
esac

# 创建当日目录
TODAY_DIR="$RAW_DIR/$DATE"
mkdir -p "$TODAY_DIR"

# 生成文件名
if [ -n "$TITLE" ]; then
  # 清理标题为安全文件名
  SAFE_TITLE=$(echo "$TITLE" | sed 's/[^\w\-]/_/g' | cut -c1-50)
  FILENAME="${DATE}_${TYPE}_${SAFE_TITLE}.md"
else
  FILENAME="${DATE}_${TYPE}_$(date +%s).md"
fi

DEST="$TODAY_DIR/$FILENAME"

# 获取内容
echo "📥 入库中..."

if [ -n "$SOURCE_URL" ]; then
  echo "  来源: $SOURCE_URL"
  
  # 用 web_fetch 获取内容（通过 OpenClaw）
  # 注意：这里生成一个采集任务，实际抓取由 OpenClaw 工具完成
  cat > "$DEST" << EOF
---
type: $TYPE
source: url
url: $SOURCE_URL
date: $DATE
title: "$SOURCE_URL"
ingested: $(date -u +%Y-%m-%dT%H:%M:%SZ)
---

# $SOURCE_URL

> 原始内容待抓取

## 元信息

- 类型: $TYPE
- 来源: $SOURCE_URL
- 入库时间: $(date '+%Y-%m-%d %H:%M:%S')
- 状态: pending

## 摘要


## 关键概念


## 原始笔记

EOF

elif [ -n "$SOURCE_FILE" ]; then
  echo "  来源文件: $SOURCE_FILE"
  
  if [ ! -f "$SOURCE_FILE" ]; then
    echo "错误: 文件不存在: $SOURCE_FILE"
    exit 1
  fi
  
  # 复制文件到 raw 目录
  cp "$SOURCE_FILE" "$DEST"
  echo "  已复制到: $DEST"

elif [ -n "$CONTENT" ]; then
  echo "  来源: 文本输入"
  
  cat > "$DEST" << EOF
---
type: $TYPE
source: text
date: $DATE
title: "$TITLE"
ingested: $(date -u +%Y-%m-%dT%H:%M:%SZ)
---

$CONTENT

EOF

fi

echo ""
echo "✅ 入库完成: $DEST"
echo ""
echo "下一步:"
echo "  ./scripts/compile.sh                    # 编译到 wiki"
echo "  ./scripts/compile.sh --incremental      # 仅编译新文档"
