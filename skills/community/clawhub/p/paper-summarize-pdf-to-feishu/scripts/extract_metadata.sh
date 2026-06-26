#!/bin/bash
# extract_metadata.sh - 提取 PDF 论文元数据
# 用法：./extract_metadata.sh <input.pdf> <output.json> <paper_dir>

set -e

INPUT_PDF="$1"
OUTPUT_JSON="$2"
PAPER_DIR="$3"

# 日志配置
LOG_FILE="$PAPER_DIR/logs/scripts/extract_metadata.log"
LOG_PREFIX="[extract_metadata]"

mkdir -p "$(dirname "$LOG_FILE")"

log() {
    echo "[$(date +%H:%M:%S)] $LOG_PREFIX $1" | tee -a "$LOG_FILE"
}

if [[ -z "$INPUT_PDF" || -z "$OUTPUT_JSON" ]]; then
    echo "❌ 用法：$0 <input.pdf> <output.json> <paper_dir>"
    exit 1
fi

if [[ ! -f "$INPUT_PDF" ]]; then
    log "❌ 文件不存在：$INPUT_PDF"
    exit 1
fi

log "🚀 开始执行 extract_metadata.sh"
log "📄 输入 PDF: $INPUT_PDF"
log "📝 输出 JSON: $OUTPUT_JSON"

log "📄 正在提取 PDF 元数据..."

# 使用 pdfinfo 提取元数据
PDFINFO=$(pdfinfo "$INPUT_PDF" 2>/dev/null)

# 提取各个字段
TITLE=$(echo "$PDFINFO" | grep -i "^Title:" | sed 's/^Title:[[:space:]]*//' | head -1)
AUTHOR=$(echo "$PDFINFO" | grep -i "^Author:" | sed 's/^Author:[[:space:]]*//' | head -1)
SUBJECT=$(echo "$PDFINFO" | grep -i "^Subject:" | sed 's/^Subject:[[:space:]]*//' | head -1)
KEYWORDS=$(echo "$PDFINFO" | grep -i "^Keywords:" | sed 's/^Keywords:[[:space:]]*//' | head -1)
PRODUCER=$(echo "$PDFINFO" | grep -i "^Producer:" | sed 's/^Producer:[[:space:]]*//' | head -1)
CREATEDATE=$(echo "$PDFINFO" | grep -i "^CreationDate:" | sed 's/^CreationDate:[[:space:]]*//' | head -1)
PAGES=$(echo "$PDFINFO" | grep -i "^Pages:" | sed 's/^Pages:[[:space:]]*//' | head -1)

# 尝试从文件名或内容提取 DOI
DOI=""
# 方法 1：从文件名提取（常见格式：10.xxxx_xxxxxx.pdf）
FILENAME=$(basename "$INPUT_PDF")
DOI=$(echo "$FILENAME" | grep -oE '10\.[0-9]{4,}/[^_[:space:]]+' | head -1 || echo "")

# 方法 2：从 PDF 内容提取（如果文件名没有 DOI）
if [[ -z "$DOI" ]]; then
    DOI=$(pdftotext "$INPUT_PDF" - 2>/dev/null | grep -oE '10\.[0-9]{4,}/[^[:space:]]+' | head -1 || echo "")
fi

# 生成 paper_id（使用 DOI 或文件名哈希）
if [[ -n "$DOI" ]]; then
    # DOI 转 paper_id：10.1038/s41591-025-04176-7 → 10_1038_s41591-025-04176-7
    # 替换 / 和 . 为 _
    PAPER_ID=$(echo "$DOI" | sed 's/\//_/g' | sed 's/\./_/g')
else
    # 使用文件名哈希
    PAPER_ID="paper_$(md5sum "$INPUT_PDF" | cut -c1-12)"
fi

# 计算文件哈希
PDF_HASH=$(md5sum "$INPUT_PDF" | cut -d' ' -f1)

# 生成 JSON 输出
cat > "$OUTPUT_JSON" << EOF
{
  "paper_id": "$PAPER_ID",
  "doi": "$DOI",
  "title": "$TITLE",
  "authors": "$AUTHOR",
  "subject": "$SUBJECT",
  "keywords": "$KEYWORDS",
  "producer": "$PRODUCER",
  "created_date": "$CREATEDATE",
  "pages": $PAGES,
  "pdf_hash": "$PDF_HASH",
  "source_file": "$INPUT_PDF",
  "extracted_at": "$(date -Iseconds)"
}
EOF

log "✅ 元数据提取完成"
log "📝 Paper ID: $PAPER_ID"
if [[ -n "$DOI" ]]; then
    log "🔗 DOI: $DOI"
fi
log "📄 页数：$PAGES"
log "💾 输出：$OUTPUT_JSON"
log "🎉 脚本执行完成"
