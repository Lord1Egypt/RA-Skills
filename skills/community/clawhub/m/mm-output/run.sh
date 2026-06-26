#!/bin/bash
# PosterGen Parser Unit - 功能测试脚本 (直接使用 run.py)

# 路径配置
PDF_PATH="/mnt/tidalfs-bdsz01/usr/tusen/yanzexuan/PosterGen/data/am-ELO_A_Stable_Framework_for_Arena-based_LLM_Evaluation/paper.pdf"
MD_PATH="/mnt/tidalfs-bdsz01/usr/tusen/yanzexuan/postergenparserunit/examples/tusen_1210.md"
OUTPUT_DIR="/mnt/tidalfs-bdsz01/usr/tusen/yanzexuan/postergenparserunit/output2"
POSTER_TEMPLATE="/mnt/tidalfs-bdsz01/usr/tusen/yanzexuan/postergenparserunit/templates/report_web_reduced.txt"

echo "=========================================="
echo "PosterGen Parser Unit - 功能测试"
echo "=========================================="
echo ""

# 同步依赖
echo "[1/9] 同步依赖..."
uv sync
echo ""

# ============ 基础解析测试 ============
echo "[2/9] 测试: PDF -> HTML"
uv run python run.py \
  --pdf_path "$PDF_PATH" \
  --output_dir "$OUTPUT_DIR/pdf_to_html" \
  --output_type html
echo "✓ PDF -> HTML 完成"
echo ""

echo "[3/9] 测试: MD -> HTML (带模板)"
uv run python run.py \
  --md_path "$MD_PATH" \
  --output_dir "$OUTPUT_DIR/md_to_html" \
  --output_type html \
  --template "$POSTER_TEMPLATE"
echo "✓ MD -> HTML 完成"
echo ""

# ============ 图片/Slides 生成测试 ============
echo "[4/9] 测试: MD -> XHS Slides (academic风格)"
uv run python run.py \
  --md_path "$MD_PATH" \
  --output_dir "$OUTPUT_DIR/xhs_slides_academic" \
  --output_type xhs_slides \
  --style academic \
  --slides_length medium
echo "✓ XHS Slides (academic) 完成"
echo ""

echo "[5/9] 测试: MD -> XHS Slides (doraemon风格)"
uv run python run.py \
  --md_path "$MD_PATH" \
  --output_dir "$OUTPUT_DIR/xhs_slides_doraemon" \
  --output_type xhs_slides \
  --style doraemon \
  --slides_length short
echo "✓ XHS Slides (doraemon) 完成"
echo ""

echo "[6/9] 测试: MD -> Slides Image (doraemon风格)"
uv run python run.py \
  --md_path "$MD_PATH" \
  --output_dir "$OUTPUT_DIR/slides_doraemon" \
  --output_type slides_image \
  --style doraemon \
  --slides_length medium
echo "✓ Slides Image (doraemon) 完成"
echo ""

echo "[7/9] 测试: MD -> Poster Image (academic风格, medium密度)"
uv run python run.py \
  --md_path "$MD_PATH" \
  --output_dir "$OUTPUT_DIR/poster_academic" \
  --output_type poster_image \
  --style academic \
  --density medium
echo "✓ Poster Image 完成"
echo ""

echo "[8/9] 测试: MD -> Poster Image (doraemon风格, sparse密度)"
uv run python run.py \
  --md_path "$MD_PATH" \
  --output_dir "$OUTPUT_DIR/poster_doraemon" \
  --output_type poster_image \
  --style doraemon \
  --density sparse
echo "✓ Poster Image (doraemon) 完成"
echo ""

# ============ HTML 转换测试 (mm_output) ============
echo "[9/9] 测试: HTML -> PDF/PNG/DOCX"
HTML_FILE="$OUTPUT_DIR/md_to_html/poster_preview.html"
if [ -f "$HTML_FILE" ]; then
    # HTML -> PDF
    uv run python -m mm_output.cli \
      "$HTML_FILE" \
      --format pdf \
      --output-dir "$OUTPUT_DIR/html_to_pdf"
    echo "  ✓ HTML -> PDF 完成"
    
    # HTML -> PNG
    uv run python -m mm_output.cli \
      "$HTML_FILE" \
      --format png \
      --output-dir "$OUTPUT_DIR/html_to_png"
    echo "  ✓ HTML -> PNG 完成"
    
    # HTML -> DOCX
    uv run python -m mm_output.cli \
      "$HTML_FILE" \
      --format docx \
      --output-dir "$OUTPUT_DIR/html_to_docx"
    echo "  ✓ HTML -> DOCX 完成"
else
    echo "⚠ HTML 文件不存在，跳过转换测试"
fi
echo ""

# 打包输出
echo "=========================================="
echo "打包输出文件..."
echo "=========================================="
prefix="$(basename "$OUTPUT_DIR")"
n=1
while [ -e "${prefix}_$(printf '%03d' "$n").tar.gz" ]; do
  n=$((n+1))
done
outfile="${prefix}_$(printf '%03d' "$n").tar.gz"
tar -czf "$outfile" -C "$(dirname "$OUTPUT_DIR")" "$prefix"
echo "✓ 打包完成: $outfile"
echo ""

# 输出测试摘要
echo "=========================================="
echo "测试完成！输出摘要:"
echo "=========================================="
echo ""
echo "输出目录结构:"
find "$OUTPUT_DIR" -type f \( -name "*.html" -o -name "*.pdf" -o -name "*.png" -o -name "*.jpg" -o -name "*.docx" \) 2>/dev/null | head -30 | while read f; do
    echo "  - ${f#$OUTPUT_DIR/}"
done
echo ""
echo "所有测试完成！"
