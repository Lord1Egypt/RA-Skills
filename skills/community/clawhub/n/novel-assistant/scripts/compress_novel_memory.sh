#!/bin/bash
# 小说记忆文件压缩脚本 (纯Shell版本)
# 
# 功能：
# 1. 合并早期章节概要
# 2. 清理已解决的伏笔
# 3. 控制文件总字数
#
# 使用：
#     ./compress_novel_memory.sh <memory_file.md>
#     ./compress_novel_memory.sh <memory_file.md> --keep-chapters 15

set -e

# 默认保留章节数
KEEP_CHAPTERS=15

# 解析参数
MEMORY_FILE=""
while [[ $# -gt 0 ]]; do
    case $1 in
        --keep-chapters)
            KEEP_CHAPTERS="$2"
            shift 2
            ;;
        *)
            MEMORY_FILE="$1"
            shift
            ;;
    esac
done

# 检查文件
if [[ -z "$MEMORY_FILE" ]] || [[ ! -f "$MEMORY_FILE" ]]; then
    echo "用法：$0 <memory_file.md> [--keep-chapters N]"
    echo ""
    echo "选项："
    echo "  --keep-chapters N  保留最近N章（默认15）"
    exit 1
fi

# 获取文件信息
ORIGINAL_SIZE=$(wc -c < "$MEMORY_FILE")
TITLE=$(grep -oP '(?<=# 《)[^》]+' "$MEMORY_FILE" 2>/dev/null || echo "未知小说")
TOTAL_CHAPTERS=$(grep -c "^### 第" "$MEMORY_FILE" 2>/dev/null || echo "0")

echo "正在压缩《$TITLE》记忆文件..."
echo "  原始大小：$ORIGINAL_SIZE 字节"
echo "  章节数：$TOTAL_CHAPTERS"

# 如果章节数不超过保留数，不压缩
if [[ "$TOTAL_CHAPTERS" -le "$KEEP_CHAPTERS" ]]; then
    echo "  章节数未超过阈值，无需压缩"
    exit 0
fi

# 备份原文件
BACKUP_FILE="${MEMORY_FILE}.bak"
cp "$MEMORY_FILE" "$BACKUP_FILE"
echo "  原文件备份：$BACKUP_FILE"

# 创建临时文件
TEMP_FILE=$(mktemp)
trap "rm -f $TEMP_FILE" EXIT

# 提取各部分
BASIC_SECTION=$(sed -n '/^## 基本信息/,/^## /p' "$MEMORY_FILE" | head -n -1)
WORLD_SECTION=$(sed -n '/^## 世界观/,/^## /p' "$MEMORY_FILE" | head -n -1)
CHARACTERS_SECTION=$(sed -n '/^## 主要人物/,/^## /p' "$MEMORY_FILE" | head -n -1)
RELATION_SECTION=$(sed -n '/^## 人物关系图/,/^## /p' "$MEMORY_FILE" | head -n -1)
OUTLINE_SECTION=$(sed -n '/^## 章节大纲/,/^## /p' "$MEMORY_FILE" | head -n -1)
FORESHADOW_SECTION=$(sed -n '/^## 伏笔追踪/,/^## /p' "$MEMORY_FILE" | head -n -1)
TIMELINE_SECTION=$(sed -n '/^## 时间线/,/^## /p' "$MEMORY_FILE" | head -n -1)

# 提取章节概要
CHAPTER_START=$((TOTAL_CHAPTERS - KEEP_CHAPTERS + 1))

# 构建新文件
{
    echo "# 《$TITLE》记忆文件"
    echo ""
    
    # 基本信息
    if [[ -n "$BASIC_SECTION" ]]; then
        echo "$BASIC_SECTION"
        echo ""
    fi
    
    # 世界观
    if [[ -n "$WORLD_SECTION" ]]; then
        echo "$WORLD_SECTION"
        echo ""
    fi
    
    # 主要人物
    if [[ -n "$CHARACTERS_SECTION" ]]; then
        echo "$CHARACTERS_SECTION"
        echo ""
    fi
    
    # 人物关系图
    if [[ -n "$RELATION_SECTION" ]]; then
        echo "$RELATION_SECTION"
        echo ""
    fi
    
    # 章节大纲
    if [[ -n "$OUTLINE_SECTION" ]]; then
        echo "$OUTLINE_SECTION"
        echo ""
    fi
    
    # 剧情概要
    echo "## 剧情概要"
    echo ""
    
    # 添加早期章节概要
    echo "### 第1-$((CHAPTER_START - 1))章概要"
    echo "[前$((CHAPTER_START - 1))章已压缩，关键剧情见章节大纲]"
    echo ""
    
    # 保留近期章节
    sed -n "/^### 第${CHAPTER_START}章/,/^## /p" "$MEMORY_FILE" | head -n -1
    
    # 伏笔追踪（只保留未解决的）
    if [[ -n "$FORESHADOW_SECTION" ]]; then
        echo ""
        echo "## 伏笔追踪"
        echo "$FORESHADOW_SECTION" | grep -v "^\- \[x\]" || true
        echo ""
    fi
    
    # 时间线
    if [[ -n "$TIMELINE_SECTION" ]]; then
        echo "$TIMELINE_SECTION"
    fi
    
} > "$TEMP_FILE"

# 计算压缩后大小
NEW_SIZE=$(wc -c < "$TEMP_FILE")
COMPRESSION_RATIO=$(echo "scale=1; (1 - $NEW_SIZE / $ORIGINAL_SIZE) * 100" | bc 2>/dev/null || echo "0")

echo "  压缩后大小：$NEW_SIZE 字节"
echo "  压缩率：${COMPRESSION_RATIO}%"
echo "  合并了前 $((CHAPTER_START - 1)) 章为概要"

# 写入新文件
mv "$TEMP_FILE" "$MEMORY_FILE"
echo "  新文件已保存：$MEMORY_FILE"
