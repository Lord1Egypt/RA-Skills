#!/bin/bash
# locate_figures.sh - 定位并截取 PDF 中的 Figure/Table 图片
# 用法：./locate_figures.sh <input.pdf> <input.txt> <output_dir>

# 错误处理和日志
set -e
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PAPER_DIR="$(dirname "$SCRIPT_DIR")"
LOG_FILE="$PAPER_DIR/logs/scripts/locate_figures.log"
LOG_PREFIX="[locate_figures]"

# 确保日志目录存在
mkdir -p "$(dirname "$LOG_FILE")"

# 日志函数
log() {
    echo "[$(date +%H:%M:%S)] $LOG_PREFIX $1" | tee -a "$LOG_FILE"
}

# 错误处理
error_handler() {
    local line_no=$1
    local error_code=$2
    log "❌ 错误发生在第 $line_no 行，错误代码：$error_code"
    log "💡 建议：检查输入文件是否存在，依赖工具是否安装"
    exit $error_code
}

trap 'error_handler $LINENO $?' ERR

# 参数检查
if [[ -z "$INPUT_PDF" || -z "$INPUT_TXT" || -z "$OUTPUT_DIR" ]]; then
    log "❌ 用法：$0 <input.pdf> <input.txt> <output_dir>"
    exit 1
fi

log "🚀 开始执行 locate_figures.sh"
log "📄 输入 PDF: $INPUT_PDF"
log "📝 输入文本：$INPUT_TXT"
log "📂 输出目录：$OUTPUT_DIR"

# 创建输出目录
mkdir -p "$OUTPUT_DIR"

echo "🖼️  正在定位 Figure 和 Table..."

# 获取 PDF 总页数
TOTAL_PAGES=$(pdfinfo "$INPUT_PDF" 2>/dev/null | grep "^Pages:" | awk '{print $2}')
echo "📄 PDF 总页数：$TOTAL_PAGES"

# 从文本中定位 Figure 和 Table 关键字的位置
echo ""
echo "🔍 步骤 1：从文本中定位 Figure 标题..."

# 提取包含 "Fig." 或 "Figure" 的行及其行号（只匹配正文中的 Figure，不匹配引用）
FIG_LINES=$(grep -n -i -E '^(Fig\. [0-9]|Figure [0-9])' "$INPUT_TXT" 2>/dev/null | head -20 || echo "")

if [[ -z "$FIG_LINES" ]]; then
    echo "⚠️  未找到 Figure 标题，尝试更宽松的匹配..."
    FIG_LINES=$(grep -n -i -E '(Fig\.|Figure) [0-9]' "$INPUT_TXT" 2>/dev/null | head -20 || echo "")
fi

FIG_COUNT=$(echo "$FIG_LINES" | grep -c "." 2>/dev/null || echo "0")
echo "📊 找到 $FIG_COUNT 个 Figure"

# 估算每页的行数（用于将行号转换为页码）
TOTAL_LINES=$(wc -l < "$INPUT_TXT")
LINES_PER_PAGE=$((TOTAL_LINES / TOTAL_PAGES + 1))
echo "📊 估算每页行数：$LINES_PER_PAGE"

# 函数：将行号转换为页码
line_to_page() {
    local line_num=$1
    local page=$(( (line_num - 1) / LINES_PER_PAGE + 1 ))
    if [[ $page -lt 1 ]]; then page=1; fi
    if [[ $page -gt $TOTAL_PAGES ]]; then page=$TOTAL_PAGES; fi
    echo $page
}

echo ""
echo "🔍 步骤 2：提取 PDF 嵌入图片（pdfimages）..."

# 使用 pdfimages 提取所有嵌入图片
pdfimages -png "$INPUT_PDF" "$OUTPUT_DIR/embedded_temp" 2>/dev/null || true
EMBEDDED_COUNT=$(ls -1 "$OUTPUT_DIR"/embedded_temp-*.png 2>/dev/null | wc -l || echo "0")
echo "📸 提取了 $EMBEDDED_COUNT 张嵌入图片"

echo ""
echo "🔍 步骤 3：筛选真正的 Figure 图片（>100KB）..."

FIG_INDEX=0
for img in "$OUTPUT_DIR"/embedded_temp-*.png; do
    if [[ -f "$img" ]]; then
        FILE_SIZE=$(stat -c%s "$img" 2>/dev/null || echo "0")
        if [[ $FILE_SIZE -gt 102400 ]]; then  # >100KB
            FIG_INDEX=$((FIG_INDEX + 1))
            cp "$img" "$OUTPUT_DIR/figure_${FIG_INDEX}_embedded.png"
            SIZE_KB=$((FILE_SIZE / 1024))
            echo "  ✅ Figure $FIG_INDEX: ${SIZE_KB}KB"
        fi
    fi
done

EMBEDDED_FIG_COUNT=$FIG_INDEX
echo "📊 筛选出 $EMBEDDED_FIG_COUNT 张 Figure 图片"

echo ""
echo "🔍 步骤 4：验证图片数量和内容（OCR 识别 Figure 标题）..."

VALIDATED_FIG_COUNT=0
for img in "$OUTPUT_DIR"/figure_*_embedded.png; do
    if [[ -f "$img" ]]; then
        # 使用 OCR 识别图片中的 Figure 标题
        OCR_TEXT=$(tesseract "$img" stdout -l eng 2>/dev/null || echo "")
        
        # 检查是否包含 Figure 标题
        if echo "$OCR_TEXT" | grep -qiE "Figure [0-9]|Fig\. [0-9]"; then
            VALIDATED_FIG_COUNT=$((VALIDATED_FIG_COUNT + 1))
            echo "  ✅ $(basename "$img"): 包含 Figure 标题"
        else
            echo "  ⚠️  $(basename "$img"): 未检测到 Figure 标题（保留）"
        fi
    fi
done

echo ""
if [[ $VALIDATED_FIG_COUNT -lt $FIG_COUNT ]]; then
    echo "⚠️  警告：验证通过的 Figure 数量 ($VALIDATED_FIG_COUNT) < 文档中 Figure 数量 ($FIG_COUNT)"
    echo "💡 建议：手动检查未通过验证的图片"
else
    echo "✅ 所有 Figure 图片验证通过"
fi

# 清理临时文件
rm -f "$OUTPUT_DIR"/embedded_temp-*.png 2>/dev/null || true

echo ""
echo "✅ Figure 定位完成"
echo "💾 输出目录：$OUTPUT_DIR"

# 输出结果列表
echo ""
echo "📋 提取结果:"
ls -lh "$OUTPUT_DIR"/*.png 2>/dev/null || echo "  (无图片文件)"
