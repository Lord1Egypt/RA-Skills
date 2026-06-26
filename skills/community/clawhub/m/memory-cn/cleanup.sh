#!/bin/bash
# 清理垃圾文件
# 检测并删除 memory/ 中的噪音文件（raw 对话、session 元数据等）

set -e

MEMORY_DIR="${1:-$HOME/.openclaw/workspace/memory}"
DRY_RUN="${2:---dry-run}"

echo "🧹 记忆文件垃圾检测"
echo "==================="
echo "目录: $MEMORY_DIR"
echo ""

GARBAGE=()

# 扫描所有 .md 文件
while IFS= read -r filepath; do
    filename=$(basename "$filepath")
    
    # 检测 raw 对话模式（user:/assistant: 开头的行占比 > 50%）
    total_lines=$(wc -l < "$filepath")
    if [ "$total_lines" -gt 5 ]; then
        raw_lines=$(grep -c '^\(user:\|assistant:\|System:\)' "$filepath" 2>/dev/null || true)
        ratio=$((raw_lines * 100 / total_lines))
        
        if [ "$ratio" -gt 50 ]; then
            echo "🗑️ $filepath — raw 对话 ($ratio% 是 user:/assistant: 行)"
            GARBAGE+=("$filepath")
            continue
        fi
    fi
    
    # 检测 session 元数据（包含大量 JSON metadata）
    json_blocks=$(grep -c '```json' "$filepath" 2>/dev/null || true)
    if [ "$json_blocks" -gt 10 ] && [ "$total_lines" -lt 200 ]; then
        echo "🗑️ $filepath — session 元数据 ($json_blocks 个 JSON 块)"
        GARBAGE+=("$filepath")
        continue
    fi
    
    # 检测 exec denied 循环
    exec_denied=$(grep -c 'Exec denied' "$filepath" 2>/dev/null || true)
    if [ "$exec_denied" -gt 5 ]; then
        echo "🗑️ $filepath — exec denied 循环 ($exec_denied 次)"
        GARBAGE+=("$filepath")
        continue
    fi
    
done < <(find "$MEMORY_DIR" -maxdepth 1 -name '*.md' -type f)

echo ""

if [ ${#GARBAGE[@]} -eq 0 ]; then
    echo "✅ 没有发现垃圾文件"
    exit 0
fi

echo "发现 ${#GARBAGE[@]} 个垃圾文件"

if [ "$DRY_RUN" = "--dry-run" ]; then
    echo ""
    echo "这是 dry run 模式。要实际删除，运行:"
    echo "  $0 $MEMORY_DIR --execute"
else
    echo ""
    read -p "确认删除这些文件? (y/N) " confirm
    if [ "$confirm" = "y" ] || [ "$confirm" = "Y" ]; then
        for f in "${GARBAGE[@]}"; do
            rm "$f"
            echo "  ✅ 已删除: $f"
        done
        echo "完成！建议运行 openclaw memory index --force 重建索引"
    else
        echo "已取消"
    fi
fi
