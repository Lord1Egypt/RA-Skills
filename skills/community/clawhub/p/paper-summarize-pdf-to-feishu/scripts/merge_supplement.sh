#!/bin/bash
# merge_supplement.sh - 合并补充材料到主论文文档
# 用法：./merge_supplement.sh <paper_dir> <supplement.pdf> <doc_token>

set -e

PAPER_DIR="$1"
SUPPLEMENT_PDF="$2"
DOC_TOKEN="$3"

if [[ -z "$PAPER_DIR" || -z "$SUPPLEMENT_PDF" || -z "$DOC_TOKEN" ]]; then
    echo "❌ 用法：$0 <paper_dir> <supplement.pdf> <doc_token>"
    exit 1
fi

if [[ ! -d "$PAPER_DIR" ]]; then
    echo "❌ 论文目录不存在：$PAPER_DIR"
    exit 1
fi

if [[ ! -f "$SUPPLEMENT_PDF" ]]; then
    echo "❌ 补充材料文件不存在：$SUPPLEMENT_PDF"
    exit 1
fi

echo "📎 正在处理补充材料..."
echo "📂 论文目录：$PAPER_DIR"
echo "📄 补充材料：$SUPPLEMENT_PDF"

# 创建补充材料目录
SUPPLEMENT_DIR="$PAPER_DIR/supplements"
mkdir -p "$SUPPLEMENT_DIR"

# 复制补充材料 PDF
SUPPLEMENT_BASENAME=$(basename "$SUPPLEMENT_PDF")
cp "$SUPPLEMENT_PDF" "$SUPPLEMENT_DIR/$SUPPLEMENT_BASENAME"

# 提取补充材料文本
SUPPLEMENT_TXT="$SUPPLEMENT_DIR/supplement.txt"
echo "📖 正在提取补充材料文本..."
pdftotext -layout "$SUPPLEMENT_PDF" "$SUPPLEMENT_TXT" 2>/dev/null || true

if [[ -f "$SUPPLEMENT_TXT" ]]; then
    LINE_COUNT=$(wc -l < "$SUPPLEMENT_TXT")
    echo "✅ 补充材料文本提取完成 ($LINE_COUNT 行)"
else
    echo "⚠️  无法提取补充材料文本"
fi

# 提取补充材料中的关键信息（Extended Data Figures 等）
echo "🔍 正在定位补充材料中的关键内容..."

# 查找 Extended Data Figure
EXTENDED_FIGS=$(grep -n -i "Extended.*Fig" "$SUPPLEMENT_TXT" 2>/dev/null | head -10 || echo "")
if [[ -n "$EXTENDED_FIGS" ]]; then
    echo "📊 找到 Extended Data Figures:"
    echo "$EXTENDED_FIGS" | head -5
fi

# 查找 Supplementary Table
SUPPL_TABLES=$(grep -n -i "Supplementary.*Table" "$SUPPLEMENT_TXT" 2>/dev/null | head -10 || echo "")
if [[ -n "$SUPPL_TABLES" ]]; then
    echo "📋 找到 Supplementary Tables:"
    echo "$SUPPL_TABLES" | head -5
fi

# 生成补充材料摘要（前 500 行）
SUMMARY_FILE="$SUPPLEMENT_DIR/summary.md"
cat > "$SUMMARY_FILE" << EOF
# 📎 补充材料摘要

**源文件**: $SUPPLEMENT_BASENAME
**提取时间**: $(date -Iseconds)

---

## 关键内容

EOF

# 提取前 100 行作为摘要
head -100 "$SUPPLEMENT_TXT" >> "$SUMMARY_FILE" 2>/dev/null || echo "(无法提取内容)" >> "$SUMMARY_FILE"

echo ""
echo "✅ 补充材料处理完成"
echo "📂 补充材料目录：$SUPPLEMENT_DIR"
echo "📝 摘要文件：$SUMMARY_FILE"

# 输出提示
echo ""
echo "📋 下一步操作:"
echo "1. 使用 feishu_doc action=append 将补充材料追加到飞书文档"
echo "2. 文档 token: $DOC_TOKEN"
echo "3. 建议追加到文档末尾的'📎 补充材料'章节"
