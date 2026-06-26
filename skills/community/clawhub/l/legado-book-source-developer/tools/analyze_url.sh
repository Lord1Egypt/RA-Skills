#!/bin/bash
# 通用网站快速分析 - 纯 bash + curl，无需 Python
# Usage: bash analyze_url.sh <url> [--post "body"] [--charset gbk]

set -euo pipefail
URL="${1:?Usage: $0 <url> [--post body] [--charset charset]}"
METHOD="GET"
BODY=""
CHARSET=""
OUTDIR="."

shift
while [[ $# -gt 0 ]]; do
    case "$1" in
        --post) METHOD="POST"; BODY="$2"; shift 2 ;;
        --charset) CHARSET="$2"; shift 2 ;;
        --outdir) OUTDIR="$2"; shift 2 ;;
        *) shift ;;
    esac
done

UA="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

echo "=========================================="
echo "网站分析: $URL"
echo "=========================================="

# Step 1: 检测编码
echo ""
echo "--- 编码检测 ---"
HEADERS=$(curl -sI --max-time 15 -A "$UA" "$URL" 2>/dev/null || true)
CT=$(echo "$HEADERS" | grep -i "content-type" | head -1 || true)
echo "Content-Type: ${CT:-unknown}"

if echo "$CT" | grep -qi "gbk\|gb2312"; then
    [ -z "$CHARSET" ] && CHARSET="gbk"
fi
CHARSET="${CHARSET:-utf-8}"
echo "使用编码: $CHARSET"

# Step 2: 获取HTML
echo ""
echo "--- 获取页面 ---"
SAFENAME=$(echo "$URL" | sed 's|https\?://||;s|[^a-zA-Z0-9]|_|g')
OUTFILE="${OUTDIR}/${SAFENAME}.html"

if [ "$METHOD" = "POST" ]; then
    curl -s --max-time 30 -A "$UA" \
        -H "Content-Type: application/x-www-form-urlencoded" \
        -d "$BODY" \
        "$URL" > "$OUTFILE"
else
    curl -s --max-time 30 -A "$UA" "$URL" > "$OUTFILE"
fi

SIZE=$(wc -c < "$OUTFILE")
LINES=$(wc -l < "$OUTFILE")
echo "HTML已保存: $OUTFILE ($SIZE bytes, $LINES lines)"

# Step 3: 基础分析
echo ""
echo "--- 基础分析 ---"

TITLE=$(grep -oP '<title[^>]*>\K[^<]+' "$OUTFILE" | head -1 || echo "N/A")
echo "标题: $TITLE"

FORMS=$(grep -c '<form' "$OUTFILE" || true)
echo "表单数: $FORMS"

IMGS=$(grep -c '<img' "$OUTFILE" || true)
echo "图片数: $IMGS"

SCRIPTS=$(grep -c '<script' "$OUTFILE" || true)
echo "脚本数: $SCRIPTS"

# Step 4: 搜索表单分析
echo ""
echo "--- 搜索表单 ---"
if [ "$FORMS" -gt 0 ]; then
    grep -oP '<form[^>]*>.*?</form>' "$OUTFILE" 2>/dev/null | head -3 | while read -r form; do
        ACTION=$(echo "$form" | grep -oP 'action="[^"]*"' | head -1 || true)
        METHOD_F=$(echo "$form" | grep -oP 'method="[^"]*"' | head -1 || echo 'method="GET"')
        INPUTS=$(echo "$form" | grep -oP '<input[^>]*>' | head -5 || true)
        echo "  $METHOD_F $ACTION"
        echo "  Inputs: $INPUTS"
    done
else
    echo "  未找到表单，请手动检查 Network 面板"
fi

# Step 5: 常见CSS选择器线索
echo ""
echo "--- CSS选择器线索 ---"
echo "可能的列表容器:"
grep -oP 'class="[^"]*\(list\|result\|book\|item\|search\)[^"]*"' "$OUTFILE" | sort -u | head -10 | sed 's/^/  /'

echo "可能的内容容器:"
grep -oP 'class="[^"]*\(content\|chapter\|text\|article\|body\)[^"]*"' "$OUTFILE" | sort -u | head -10 | sed 's/^/  /'

echo ""
echo "=========================================="
echo "分析完成。请用 web_fetch 或浏览器进一步确认选择器。"
echo "=========================================="
