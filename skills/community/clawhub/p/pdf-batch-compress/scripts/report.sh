#!/bin/bash
# ============================================================
# PDF 压缩报告生成脚本
# 用法: bash report.sh [日志目录]
# 默认日志目录: /tmp/pdf_compress_logs
# ============================================================

LOG_DIR="${1:-/tmp/pdf_compress_logs}"

echo "============================================================"
echo "  PDF 批量压缩报告"
echo "  生成时间: $(date '+%Y-%m-%d %H:%M:%S')"
echo "============================================================"
echo ""

# 查找最新的日志文件
LATEST_GS=$(ls -t "$LOG_DIR"/gs_*.log 2>/dev/null | head -1)
LATEST_PYMU=$(ls -t "$LOG_DIR"/pymupdf_*.log 2>/dev/null | head -1)

if [ -z "$LATEST_GS" ] && [ -z "$LATEST_PYMU" ]; then
    echo "❌ 未找到压缩日志文件"
    echo "   日志目录: $LOG_DIR"
    exit 1
fi

echo "--- Ghostscript 阶段 ---"
if [ -n "$LATEST_GS" ]; then
    echo "日志: $LATEST_GS"
    echo "OK:      $(grep -c '^OK' "$LATEST_GS" 2>/dev/null || echo 0)"
    echo "PARTIAL: $(grep -c '^PARTIAL' "$LATEST_GS" 2>/dev/null || echo 0)"
    echo "FAIL:    $(grep -c '^FAIL' "$LATEST_GS" 2>/dev/null || echo 0)"
    echo "SKIP:    $(grep -c '^SKIP' "$LATEST_GS" 2>/dev/null || echo 0)"
    echo "ERROR:   $(grep -c '^ERROR' "$LATEST_GS" 2>/dev/null || echo 0)"
    echo "节省空间: $(awk -F'|' '/^OK/{s+=$3-$4} /^PARTIAL/{s+=$3-$4} END{printf "%.2f GB\n", s/1024}' "$LATEST_GS" 2>/dev/null)"
else
    echo "无 GS 日志"
fi
echo ""

echo "--- PyMuPDF 阶段 ---"
if [ -n "$LATEST_PYMU" ]; then
    echo "日志: $LATEST_PYMU"
    echo "OK:      $(grep -c '^OK' "$LATEST_PYMU" 2>/dev/null || echo 0)"
    echo "PARTIAL: $(grep -c '^PARTIAL' "$LATEST_PYMU" 2>/dev/null || echo 0)"
    echo "FAIL:    $(grep -c '^FAIL' "$LATEST_PYMU" 2>/dev/null || echo 0)"
    echo "SKIP:    $(grep -c '^SKIP' "$LATEST_PYMU" 2>/dev/null || echo 0)"
    echo "ERROR:   $(grep -c '^ERROR' "$LATEST_PYMU" 2>/dev/null || echo 0)"
    echo "节省空间: $(awk -F'|' '/^OK/{s+=$3-$4} /^PARTIAL/{s+=$3-$4} END{printf "%.2f GB\n", s/1024}' "$LATEST_PYMU" 2>/dev/null)"
else
    echo "无 PyMuPDF 日志"
fi
echo ""

echo "--- 失败文件列表 ---"
if [ -n "$LATEST_GS" ]; then
    echo "[GS FAIL]"
    grep '^FAIL' "$LATEST_GS" 2>/dev/null | awk -F'|' '{printf "  %s (%.1fMB)\n", $2, $3}' | head -20
fi
if [ -n "$LATEST_PYMU" ]; then
    echo "[PyMuPDF FAIL]"
    grep '^FAIL' "$LATEST_PYMU" 2>/dev/null | awk -F'|' '{printf "  %s (%.1fMB)\n", $2, $3}' | head -20
fi
echo ""

echo "--- 部分压缩文件列表 ---"
if [ -n "$LATEST_GS" ]; then
    echo "[GS PARTIAL]"
    grep '^PARTIAL' "$LATEST_GS" 2>/dev/null | awk -F'|' '{printf "  %s (%.1f→%.1fMB)\n", $2, $3, $4}' | head -20
fi
if [ -n "$LATEST_PYMU" ]; then
    echo "[PyMuPDF PARTIAL]"
    grep '^PARTIAL' "$LATEST_PYMU" 2>/dev/null | awk -F'|' '{printf "  %s (%.1f→%.1fMB)\n", $2, $3, $4}' | head -20
fi
echo ""

echo "============================================================"
echo "✅ 报告完成"
echo "============================================================"
