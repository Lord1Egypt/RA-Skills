#!/bin/bash
# doc-edit.sh - 编辑文档
# 用途：对现有文档进行简单编辑（追加、替换、提取）

set -e

FILE="$1"
ACTION="$2"
shift 2 || true

if [ -z "$FILE" ] || [ -z "$ACTION" ]; then
    echo "用法：$0 <文件> <操作> [参数]"
    echo ""
    echo "操作:"
    echo "  append <内容>        追加内容到文档末尾"
    echo "  replace <原> <新>    替换文本内容"
    echo "  extract <章节>       提取特定章节"
    echo "  info                 显示文档信息"
    echo ""
    echo "示例:"
    echo "  $0 ~/report.docx append '## 新增章节'"
    echo "  $0 ~/report.docx replace '旧文本' '新文本'"
    echo "  $0 ~/report.docx extract '摘要'"
    echo "  $0 ~/report.docx info"
    exit 1
fi

if [ ! -f "$FILE" ]; then
    echo "❌ 文件不存在：$FILE"
    exit 1
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

case "$ACTION" in
    append)
        # 追加内容
        CONTENT="$*"
        if [ -z "$CONTENT" ]; then
            echo "❌ 需要指定追加的内容"
            exit 1
        fi
        
        TMPFILE=$(mktemp --suffix=.md)
        
        # 读取原文档
        "$SCRIPT_DIR/doc-read.sh" "$FILE" markdown > "$TMPFILE"
        
        # 追加内容
        echo "" >> "$TMPFILE"
        echo "$CONTENT" >> "$TMPFILE"
        
        # 写回
        "$SCRIPT_DIR/doc-write.sh" "$FILE" "$TMPFILE" markdown
        rm -f "$TMPFILE"
        
        echo "✅ 已追加内容到：$FILE"
        ;;
    
    replace)
        # 替换内容
        if [ -z "$1" ] || [ -z "$2" ]; then
            echo "❌ 需要指定原文本和新文本"
            echo "用法：$0 <文件> replace <原文本> <新文本>"
            exit 1
        fi
        
        PATTERN="$1"
        REPLACEMENT="$2"
        TMPFILE=$(mktemp --suffix=.md)
        
        # 读取→替换→写回
        "$SCRIPT_DIR/doc-read.sh" "$FILE" markdown | sed "s/$PATTERN/$REPLACEMENT/g" > "$TMPFILE"
        "$SCRIPT_DIR/doc-write.sh" "$FILE" "$TMPFILE" markdown
        rm -f "$TMPFILE"
        
        echo "✅ 已替换内容：$FILE"
        ;;
    
    extract)
        # 提取章节
        SECTION="$*"
        if [ -z "$SECTION" ]; then
            echo "❌ 需要指定章节名称"
            exit 1
        fi
        
        "$SCRIPT_DIR/doc-read.sh" "$FILE" markdown | grep -A 100 "^# $SECTION" | head -100
        ;;
    
    info)
        # 显示文档信息
        echo "📄 文档信息：$FILE"
        echo "大小：$(du -h "$FILE" | cut -f1)"
        echo "格式：${FILE##*.}"
        
        if [[ "$OSTYPE" == "linux-gnu"* ]]; then
            echo "创建：$(stat -c %y "$FILE" 2>/dev/null)"
            echo "修改：$(stat -c %y "$FILE" 2>/dev/null)"
        elif [[ "$OSTYPE" == "darwin"* ]]; then
            echo "创建：$(stat -f %Sm "$FILE")"
            echo "修改：$(stat -f %Sm "$FILE")"
        fi
        
        # 内容统计
        echo ""
        echo "内容统计:"
        CONTENT=$("$SCRIPT_DIR/doc-read.sh" "$FILE" plain 2>/dev/null || echo "")
        if [ -n "$CONTENT" ]; then
            echo "  字符数：$(echo "$CONTENT" | wc -c)"
            echo "  单词数：$(echo "$CONTENT" | wc -w)"
            echo "  行数：$(echo "$CONTENT" | wc -l)"
        fi
        ;;
    
    *)
        echo "❌ 未知操作：$ACTION"
        echo "支持的操作：append, replace, extract, info"
        exit 1
        ;;
esac
