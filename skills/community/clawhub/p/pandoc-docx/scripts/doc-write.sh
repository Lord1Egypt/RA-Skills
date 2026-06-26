#!/bin/bash
# doc-write.sh - 写入/创建文档
# 用途：将 Markdown 或其他格式转换为 Word 文档

set -e

OUTPUT="$1"
INPUT="${2:--}"
FORMAT="${3:-markdown}"

# 参数检查
if [ -z "$OUTPUT" ]; then
    echo "用法：$0 <输出文件> <输入文件|-> [输入格式]"
    echo ""
    echo "参数说明："
    echo "  输出文件     - 要创建的文件路径（如 ~/document.docx）"
    echo "  输入文件     - 输入文件路径，使用 - 表示从 stdin 读取"
    echo "  输入格式     - 输入文件格式（默认：markdown）"
    echo ""
    echo "示例："
    echo "  $0 ~/output.docx ~/input.md"
    echo "  $0 ~/output.docx - markdown"
    echo "  echo '# 标题' | $0 ~/output.docx -"
    exit 1
fi

# 获取输出文件扩展名
OUT_EXT="${OUTPUT##*.}"

# 创建临时文件
TMPFILE=$(mktemp)

# 读取输入内容
if [ "$INPUT" = "-" ]; then
    # 从 stdin 读取
    cat > "$TMPFILE"
else
    # 从文件读取
    if [ ! -f "$INPUT" ]; then
        echo "❌ 输入文件不存在：$INPUT" >&2
        rm -f "$TMPFILE"
        exit 1
    fi
    cat "$INPUT" > "$TMPFILE"
fi

# 根据输出格式选择写入方式
case "$OUT_EXT" in
    docx)
        # Word .docx - 使用 pandoc
        if ! command -v pandoc &>/dev/null; then
            echo "❌ 需要安装 pandoc" >&2
            echo "安装：sudo apt install pandoc  或  brew install pandoc" >&2
            rm -f "$TMPFILE"
            exit 1
        fi
        pandoc "$TMPFILE" -f "$FORMAT" -o "$OUTPUT"
        echo "✅ 已创建：$OUTPUT"
        ;;
    
    doc)
        # Word .doc - 先创建 .docx 再转换
        if command -v libreoffice &>/dev/null; then
            TMPDOCX=$(mktemp --suffix=.docx)
            pandoc "$TMPFILE" -f "$FORMAT" -o "$TMPDOCX"
            libreoffice --headless --convert-to doc "$TMPDOCX" --outdir "$(dirname "$OUTPUT")" >/dev/null 2>&1
            mv "$(dirname "$OUTPUT")/$(basename "$TMPDOCX" .docx).doc" "$OUTPUT"
            rm -f "$TMPDOCX"
            echo "✅ 已创建：$OUTPUT"
        else
            echo "❌ 写入 .doc 需要 libreoffice" >&2
            rm -f "$TMPFILE"
            exit 1
        fi
        ;;
    
    md|markdown)
        # Markdown - 直接保存
        mv "$TMPFILE" "$OUTPUT"
        echo "✅ 已保存：$OUTPUT"
        ;;
    
    txt|text)
        # 纯文本 - 直接保存
        mv "$TMPFILE" "$OUTPUT"
        echo "✅ 已保存：$OUTPUT"
        ;;
    
    pdf)
        # PDF - 需要 texlive
        if command -v pandoc &>/dev/null; then
            pandoc "$TMPFILE" -f "$FORMAT" -o "$OUTPUT"
            echo "✅ 已创建：$OUTPUT"
        else
            echo "❌ 需要安装 pandoc" >&2
            rm -f "$TMPFILE"
            exit 1
        fi
        ;;
    
    html|htm)
        # HTML - 使用 pandoc
        if command -v pandoc &>/dev/null; then
            pandoc "$TMPFILE" -f "$FORMAT" -o "$OUTPUT"
            echo "✅ 已创建：$OUTPUT"
        else
            echo "❌ 需要安装 pandoc" >&2
            rm -f "$TMPFILE"
            exit 1
        fi
        ;;
    
    *)
        echo "❌ 不支持的格式：$OUT_EXT" >&2
        echo "支持的格式：docx, doc, md, txt, pdf, html" >&2
        rm -f "$TMPFILE"
        exit 1
        ;;
esac

# 清理临时文件
rm -f "$TMPFILE"
