#!/bin/bash
# ============================================================
# PDF 批量压缩一键编排脚本
# 用法: bash batch_compress.sh <目录> [阈值MB] [并行数]
# 
# 策略：Ghostscript 优先 → PyMuPDF 兜底
# 压缩后替换原文件，保留原文件名
# ============================================================

set -e

# 参数解析
DIRECTORY="${1:?用法: bash batch_compress.sh <目录> [阈值MB] [并行数]}"
THRESHOLD_MB="${2:-50}"
PARALLEL="${3:-8}"

# 路径配置
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PYTHON="/Users/weidong/.workbuddy/binaries/python/envs/default/bin/python3"
GS_SCRIPT="$SCRIPT_DIR/compress_single_gs.py"
PYMUPDF_SCRIPT="$SCRIPT_DIR/compress_fast.py"

# 日志文件
LOG_DIR="/tmp/pdf_compress_logs"
mkdir -p "$LOG_DIR"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
GS_LOG="$LOG_DIR/gs_${TIMESTAMP}.log"
PYMU_LOG="$LOG_DIR/pymupdf_${TIMESTAMP}.log"
FILE_LIST="$LOG_DIR/file_list_${TIMESTAMP}.txt"
REMAINING_LIST="$LOG_DIR/remaining_${TIMESTAMP}.txt"

# 临时文件
THRESHOLD_BYTES=$((THRESHOLD_MB * 1024 * 1024))
THRESHOLD_FIND="+${THRESHOLD_MB}M"

echo "============================================================"
echo "  PDF 批量压缩工具"
echo "============================================================"
echo "  目录: $DIRECTORY"
echo "  阈值: ${THRESHOLD_MB}MB"
echo "  并行: ${PARALLEL} 进程"
echo "  时间: $(date '+%Y-%m-%d %H:%M:%S')"
echo "============================================================"
echo ""

# 检查依赖
echo "[1/5] 检查依赖..."

# 检查目录
if [ ! -d "$DIRECTORY" ]; then
    echo "  ❌ 目录不存在: $DIRECTORY"
    exit 1
fi
echo "  ✅ 目录可访问"

# 检查 Ghostscript
GS_BIN=""
for gs_path in "/opt/homebrew/bin/gs" "/usr/local/bin/gs" "/usr/bin/gs"; do
    if [ -x "$gs_path" ]; then
        GS_BIN="$gs_path"
        break
    fi
done
if [ -n "$GS_BIN" ]; then
    echo "  ✅ Ghostscript: $($GS_BIN --version)"
else
    echo "  ⚠️  Ghostscript 未安装，将跳过 GS 阶段"
    echo "     安装: brew install ghostscript"
fi

# 检查 Python PDF 库
if [ -x "$PYTHON" ]; then
    PYMU_OK=$($PYTHON -c "import fitz; import pikepdf; print('ok')" 2>/dev/null || echo "fail")
    if [ "$PYMU_OK" = "ok" ]; then
        echo "  ✅ PyMuPDF + pikepdf 可用"
    else
        echo "  ⚠️  PyMuPDF/pikepdf 不可用，将跳过 PyMuPDF 阶段"
        echo "     安装: $PYTHON -m pip install pymupdf pikepdf"
    fi
else
    echo "  ❌ Python 不存在: $PYTHON"
    echo "     请先创建 WorkBuddy Python 环境"
    exit 1
fi

if [ -z "$GS_BIN" ] && [ "$PYMU_OK" != "ok" ]; then
    echo ""
    echo "❌ 没有可用的压缩工具，请先安装依赖"
    exit 1
fi

echo ""

# 查找文件
echo "[2/5] 查找超过 ${THRESHOLD_MB}MB 的 PDF 文件..."
find "$DIRECTORY" -iname "*.pdf" -type f -size "$THRESHOLD_FIND" > "$FILE_LIST" 2>/dev/null
TOTAL_COUNT=$(wc -l < "$FILE_LIST" | tr -d ' ')
echo "  找到 $TOTAL_COUNT 个文件需要压缩"

if [ "$TOTAL_COUNT" -eq 0 ]; then
    echo ""
    echo "✅ 没有需要压缩的文件"
    exit 0
fi

# 显示大小分布
echo ""
echo "  大小分布:"
echo "    ${THRESHOLD_MB}-100MB: $(awk -v t="$THRESHOLD_BYTES" -F'\0' '{if(1) {}}' /dev/null 2>/dev/null; find "$DIRECTORY" -iname "*.pdf" -type f -size "$THRESHOLD_FIND" -size -100M 2>/dev/null | wc -l | tr -d ' ')"
echo "    100-200MB: $(find "$DIRECTORY" -iname "*.pdf" -type f -size +100M -size -200M 2>/dev/null | wc -l | tr -d ' ')"
echo "    200-500MB: $(find "$DIRECTORY" -iname "*.pdf" -type f -size +200M -size -500M 2>/dev/null | wc -l | tr -d ' ')"
echo "    500MB+:    $(find "$DIRECTORY" -iname "*.pdf" -type f -size +500M 2>/dev/null | wc -l | tr -d ' ')"
echo ""

# 阶段1：Ghostscript
if [ -n "$GS_BIN" ]; then
    echo "[3/5] 阶段1: Ghostscript 压缩 (${PARALLEL} 进程并行)..."
    echo "  开始时间: $(date '+%H:%M:%S')"
    
    tr '\n' '\0' < "$FILE_LIST" | xargs -0 -P "$PARALLEL" -I {} \
        "$PYTHON" "$GS_SCRIPT" "{}" "$THRESHOLD_MB" \
        2>&1 >> "$GS_LOG" || true
    
    GS_OK=$(grep -c '^OK' "$GS_LOG" 2>/dev/null || echo 0)
    GS_FAIL=$(grep -c '^FAIL' "$GS_LOG" 2>/dev/null || echo 0)
    GS_PARTIAL=$(grep -c '^PARTIAL' "$GS_LOG" 2>/dev/null || echo 0)
    GS_SKIP=$(grep -c '^SKIP' "$GS_LOG" 2>/dev/null || echo 0)
    
    echo "  完成: OK=$GS_OK, FAIL=$GS_FAIL, PARTIAL=$GS_PARTIAL, SKIP=$GS_SKIP"
    echo "  结束时间: $(date '+%H:%M:%S')"
else
    echo "[3/5] 跳过 Ghostscript 阶段（未安装）"
fi
echo ""

# 阶段2：PyMuPDF 兜底
echo "[4/5] 阶段2: PyMuPDF 兜底压缩 (${PARALLEL} 进程并行)..."
find "$DIRECTORY" -iname "*.pdf" -type f -size "$THRESHOLD_FIND" > "$REMAINING_LIST" 2>/dev/null
REMAINING_COUNT=$(wc -l < "$REMAINING_LIST" | tr -d ' ')
echo "  剩余 $REMAINING_COUNT 个文件需要 PyMuPDF 处理"
echo "  开始时间: $(date '+%H:%M:%S')"

if [ "$REMAINING_COUNT" -gt 0 ]; then
    tr '\n' '\0' < "$REMAINING_LIST" | xargs -0 -P "$PARALLEL" -I {} \
        "$PYTHON" "$PYMUPDF_SCRIPT" "{}" "$THRESHOLD_MB" \
        2>&1 >> "$PYMU_LOG" || true
    
    PY_OK=$(grep -c '^OK' "$PYMU_LOG" 2>/dev/null || echo 0)
    PY_FAIL=$(grep -c '^FAIL' "$PYMU_LOG" 2>/dev/null || echo 0)
    PY_PARTIAL=$(grep -c '^PARTIAL' "$PYMU_LOG" 2>/dev/null || echo 0)
    
    echo "  完成: OK=$PY_OK, FAIL=$PY_FAIL, PARTIAL=$PY_PARTIAL"
else
    echo "  无需处理，所有文件已达标"
fi
echo "  结束时间: $(date '+%H:%M:%S')"
echo ""

# 最终报告
echo "[5/5] 最终报告"
echo "============================================================"

# 最终剩余
FINAL_REMAINING=$(find "$DIRECTORY" -iname "*.pdf" -type f -size "$THRESHOLD_FIND" 2>/dev/null | wc -l | tr -d ' ')
TOTAL_OK=$((GS_OK + PY_OK))
TOTAL_PARTIAL=$((GS_PARTIAL + PY_PARTIAL))
TOTAL_FAIL=$((GS_FAIL + PY_FAIL))
TOTAL_PROCESSED=$((TOTAL_OK + TOTAL_PARTIAL + TOTAL_FAIL + GS_SKIP))
SUCCESS_RATE=$(echo "scale=1; ($TOTAL_OK + $TOTAL_PARTIAL) * 100 / $TOTAL_PROCESSED" | bc 2>/dev/null || echo "N/A")

echo "  原始待压缩: $TOTAL_COUNT 个文件"
echo "  成功压缩(OK): $TOTAL_OK"
echo "  部分压缩(PARTIAL): $TOTAL_PARTIAL"
echo "  失败(FAIL): $TOTAL_FAIL"
echo "  跳过(SKIP): $GS_SKIP"
echo "  成功率: ${SUCCESS_RATE}%"
echo "  剩余超过${THRESHOLD_MB}MB: $FINAL_REMAINING"
echo ""

# 节省空间统计
if [ -f "$GS_LOG" ]; then
    GS_SAVED=$(awk -F'|' '/^OK/{s+=$3-$4} /^PARTIAL/{s+=$3-$4} END{print s}' "$GS_LOG" 2>/dev/null || echo 0)
else
    GS_SAVED=0
fi
if [ -f "$PYMU_LOG" ]; then
    PY_SAVED=$(awk -F'|' '/^OK/{s+=$3-$4} /^PARTIAL/{s+=$3-$4} END{print s}' "$PYMU_LOG" 2>/dev/null || echo 0)
else
    PY_SAVED=0
fi
TOTAL_SAVED=$((GS_SAVED + PY_SAVED))
TOTAL_SAVED_GB=$(echo "scale=2; $TOTAL_SAVED/1024" | bc 2>/dev/null || echo "N/A")

echo "  节省空间:"
echo "    Ghostscript: $(echo "scale=2; $GS_SAVED/1024" | bc 2>/dev/null || echo "0") GB"
echo "    PyMuPDF:     $(echo "scale=2; $PY_SAVED/1024" | bc 2>/dev/null || echo "0") GB"
echo "    总计:        ${TOTAL_SAVED_GB} GB"
echo "============================================================"
echo ""
echo "日志文件:"
echo "  GS日志:    $GS_LOG"
echo "  PyMuPDF日志: $PYMU_LOG"
echo "  文件列表:  $FILE_LIST"
echo ""
echo "✅ 压缩完成!"
