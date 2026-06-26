#!/bin/bash
# extract_pdf_text.sh - 提取 PDF 文本内容
# 用法：./extract_pdf_text.sh <input.pdf> <output.txt> <paper_dir>

set -e

INPUT_PDF="$1"
OUTPUT_TXT="$2"
PAPER_DIR="$3"

# 日志配置
LOG_FILE="$PAPER_DIR/logs/scripts/extract_pdf_text.log"
LOG_PREFIX="[extract_pdf_text]"

mkdir -p "$(dirname "$LOG_FILE")"

log() {
    echo "[$(date +%H:%M:%S)] $LOG_PREFIX $1" | tee -a "$LOG_FILE"
}

if [[ -z "$INPUT_PDF" || -z "$OUTPUT_TXT" ]]; then
    echo "❌ 用法：$0 <input.pdf> <output.txt> <paper_dir>"
    exit 1
fi

if [[ ! -f "$INPUT_PDF" ]]; then
    log "❌ 文件不存在：$INPUT_PDF"
    exit 1
fi

log "🚀 开始执行 extract_pdf_text.sh"
log "📄 输入 PDF: $INPUT_PDF"
log "📝 输出 TXT: $OUTPUT_TXT"

log "📖 正在提取 PDF 文本..."

# 使用 pdftotext 提取文本（保留布局）
pdftotext -layout "$INPUT_PDF" "$OUTPUT_TXT"

# 统计行数
LINE_COUNT=$(wc -l < "$OUTPUT_TXT")
WORD_COUNT=$(wc -w < "$OUTPUT_TXT")
CHAR_COUNT=$(wc -c < "$OUTPUT_TXT")

log "✅ 文本提取完成"
log "📄 行数：$LINE_COUNT"
log "📝 单词数：$WORD_COUNT"
log "📏 字符数：$CHAR_COUNT"
log "💾 输出：$OUTPUT_TXT"
log "🎉 脚本执行完成"

# 检查是否提取到有效内容
if [[ $LINE_COUNT -lt 10 ]]; then
    echo "⚠️  警告：提取的文本行数过少，可能是扫描版 PDF"
    echo "💡 建议：使用 OCR 工具处理"
fi
