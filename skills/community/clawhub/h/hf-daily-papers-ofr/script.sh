#!/bin/bash

# Hugging Face Daily Papers - 自动生成 PDF 推荐报告
# 用法: ./script.sh [--pdf]

# Optional proxy: export HF_DAILY_PAPERS_PROXY if needed.
PROXY="${HF_DAILY_PAPERS_PROXY:-}"
GENERATE_PDF="false"

if [ "$1" = "--pdf" ]; then
    GENERATE_PDF="true"
fi

if [ -n "$PROXY" ]; then
    export HTTP_PROXY="$PROXY"
    export HTTPS_PROXY="$PROXY"
fi

echo "📥 获取 HF Daily Papers..."

# 获取页面
curl -sL "https://huggingface.co/papers" > /tmp/hf_papers.html 2>/dev/null

# 提取论文 ID
paper_ids=$(grep -oE 'href="/papers/[0-9]+\.[0-9]+' /tmp/hf_papers.html | sed 's|href="/papers/||' | sort -u | head -30)

# 获取论文详情
papers_data=$(mktemp)
echo "" > "$papers_data"

while IFS= read -r pid; do
    info=$(curl -s "https://huggingface.co/api/papers/$pid" 2>/dev/null)
    if [ -n "$info" ]; then
        title=$(echo "$info" | grep -oE '"title":"[^"]*"' | head -1 | sed 's/"title":"//g' | sed 's/"$//')
        upvotes=$(echo "$info" | grep -oE '"upvotes":[0-9]+' | grep -oE '[0-9]+')
        if [ -n "$title" ]; then
            echo "${pid}|${title}|${upvotes}" >> "$papers_data"
        fi
    fi
done <<< "$paper_ids"

# 按 upvotes 排序
sort -t'|' -k3 -nr "$papers_data" > "${papers_data}.sorted"
mv "${papers_data}.sorted" "$papers_data"

# 时间戳
output_dir="$(cd "$(dirname "$0")" && pwd)/recommendations"
mkdir -p "$output_dir"

echo ""
echo "✅ Markdown: $output_dir/$(date +%Y-%m-%d).md"

# 如果需要 PDF，调用 Python
if [ "$GENERATE_PDF" = "true" ]; then
    python3 "$output_dir/../generator.py" --pdf
fi

rm -f "$papers_data"
