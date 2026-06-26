#!/bin/bash
# Nexus Relations Analyzer
# 自動計算檔案間關聯

set -e

INDEX_FILE="memory/index.json"
RELATIONS_FILE="memory/relations.json"

echo "🔗 Nexus 關聯分析系統"
echo "======================"

# 讀取現有索引
if [ ! -f "$INDEX_FILE" ]; then
    echo "❌ 找不到 $INDEX_FILE，先執行 auto-index.sh"
    exit 1
fi

echo "計算關聯中..."

# 簡單實現：基於關鍵詞共現
echo "{"
echo "  \"version\": \"1.0\","
echo "  \"relations\": ["

first=true
file_count=0

# 從 index.json 提取文件列表
for file in $(jq -r '.files[].path' "$INDEX_FILE" 2>/dev/null); do
    file_count=$((file_count + 1))
    kws1=$(jq -r "\"\(.files[] | select(.path == \"$file\") | .keywords | join(\"|\"))\"" "$INDEX_FILE" 2>/dev/null)
    
    for file2 in $(jq -r '.files[].path' "$INDEX_FILE" 2>/dev/null | head -$((file_count - 1))); do
        kws2=$(jq -r "\"\(.files[] | select(.path == \"$file2\") | .keywords | join(\"|\"))\"" "$INDEX_FILE" 2>/dev/null)
        
        # 簡單比較：檢查是否有共同關鍵詞
        common=$(echo "${kws1}|${kws2}" | tr '|' '\n' | sort | uniq -d | head -3)
        
        if [ -n "$common" ]; then
            [ "$first" = true ] && first=false || echo ","
            
            # 計算強度 (基於共同關鍵詞數)
            common_count=$(echo "$common" | wc -l | tr -d ' ')
            strength=$(echo "scale=2; $common_count * 0.3" | bc 2>/dev/null || echo "0.3")
            
            echo "    {"
            echo "      \"file\": \"$file\","
            echo "      \"related_to\": \"$file2\","
            echo "      \"shared_keywords\": [$(jq -R -s 'split("\n") | map(select(length>0))' <<< "$common"),],"
            echo "      \"strength\": $strength,"
            echo "      \"type\": \"keyword\""
            echo -n "    }"
        fi
        
        # 限制關聯數量
        [[ $file_count -gt 5 ]] && break
    done
    [[ $file_count -gt 5 ]] && break
done

echo ""
echo "  ],"
echo "  \"metadata\": {"
echo "    \"total_files\": $file_count,"
echo "    \"scan_time\": \"$(date -Iseconds)\""
echo "  }"
echo "}"

echo "" >&2
echo "✅ 關聯分析完成：$RELATIONS_FILE"
