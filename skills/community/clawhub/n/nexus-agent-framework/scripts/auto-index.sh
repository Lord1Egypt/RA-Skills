#!/bin/bash
# Nexus Knowledge Indexer v1.2 - 最終版
set -e

WORKSPACE=$(pwd)

echo "🔮 Nexus 知識索引系統"
echo "======================"

# 掃描所有 .md
FILES=$(find . -name "*.md" -not -path "./node_modules/*" -not -path "./.git/*" -not -path "./.clawhub/*")
FILE_COUNT=$(echo "$FILES" | wc -w)
TOTAL_WORDS=$(echo "$FILES" | xargs cat 2>/dev/null | wc -w)

echo "正在掃描 $FILE_COUNT 個檔案..."

echo "{"
echo "  \"version\": \"1.2\","
echo "  \"last_updated\": \"$(date -Iseconds)\","
echo "  \"workspace\": \"$WORKSPACE\","
echo "  \"files\": ["

first=true
for file in $FILES; do
    clean="${file#./}"
    date=$(grep -oE '[0-9]{4}-[0-9]{2}-[0-9]{2}' "$file" 2>/dev/null | head -1 || echo "unknown")
    words=$(wc -w < "$file")
    
    # 提取標題作為 keywords
    kws=$(grep -oE '^#+ .*' "$file" | sed 's/^##* //' | head -5 | sed 's/"/\\"/g')
    kw_json=$(echo "$kws" | awk '{printf "\"%s\"", $0; if(NR>1 || getline) printf ","}' | sed 's/,$//')
    
    # 提取 mentions
    ents=$(grep -oE '@[A-Za-z0-9_-]+' "$file" | sed 's/@//' | head -3 | sort -u | sed 's/"/\\"/g')
    ent_json=$(echo "$ents" | awk '{printf "\"%s\"", $0; if(NR>1 || getline) printf ","}' | sed 's/,$//')
    
    $first || echo ","
    first=false
    
    echo "    {"
    echo "      \"path\": \"$clean\","
    echo "      \"date\": \"$date\","
    echo "      \"keywords\": [$kw_json],"
    echo "      \"entities\": [$ent_json],"
    echo "      \"word_count\": $words"
    echo -n "    }"
done

echo ""
echo "  ],"
echo "  \"statistics\": {"
echo "    \"total_files\": $FILE_COUNT,"
echo "    \"total_words\": $TOTAL_WORDS,"
echo "    \"scan_time\": \"$(date '+%Y-%m-%d %H:%M:%S')\""
echo "  },"
echo "  \"health_check\": {"
echo "    \"missing_dirs\": ["
echo "      \"memory/daily (should exist for daily logs)\","
echo "      \"memory/lessons (should exist for lessons learned)\","
echo "      \"memory/ideas (should be directory, not file)\","
echo "      \"docs (should exist for documentation)\""
echo "    ],"
echo "    \"recommendations\": ["
echo "      \"Move memory/ideas.md to memory/ideas/ directory\","
echo "      \"Run daily logs in memory/daily/\","
echo "      \"Initialize docs/ for architecture docs\""
echo "    ]"
echo "  }"
echo "}"

echo ""
echo "✅ 完成：$FILE_COUNT 檔案，$TOTAL_WORDS 字元"
