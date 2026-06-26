#!/bin/bash
# doc-read.sh - 读取文档内容
# 用途：将 Word/PDF 等格式转换为 Markdown 或纯文本

set -e

FILE="$1"
FORMAT="${2:-markdown}"

# 参数检查
if [ -z "$FILE" ]; then
    echo "用法：$0 <文件路径> [输出格式]"
    echo ""
    echo "支持的格式："
    echo "  markdown (默认) - 输出 Markdown"
    echo "  plain           - 输出纯文本"
    echo "  html            - 输出 HTML"
    echo ""
    echo "示例："
    echo "  $0 ~/document.docx"
    echo "  $0 ~/document.docx plain"
    exit 1
fi

# 检查文件是否存在
if [ ! -f "$FILE" ]; then
    echo "❌ 文件不存在：$FILE" >&2
    exit 1
fi

# 获取文件扩展名
EXT="${FILE##*.}"

# 根据格式选择读取方式
case "$EXT" in
    docx)
        # Word .docx - 直接使用 pandoc
        if ! command -v pandoc &>/dev/null; then
            echo "❌ 需要安装 pandoc" >&2
            echo "安装：sudo apt install pandoc  或  brew install pandoc" >&2
            exit 1
        fi
        pandoc "$FILE" -t "$FORMAT"
        ;;
    
    doc)
        # Word .doc - 需要先转换为 .docx
        if command -v libreoffice &>/dev/null; then
            TMPDOCX=$(mktemp --suffix=.docx)
            libreoffice --headless --convert-to docx "$FILE" --outdir "$(dirname "$TMPDOCX")" >/dev/null 2>&1
            mv "$(dirname "$TMPDOCX")/$(basename "$FILE" .doc).docx" "$TMPDOCX"
            pandoc "$TMPDOCX" -t "$FORMAT"
            rm -f "$TMPDOCX"
        else
            echo "❌ 读取 .doc 需要 libreoffice" >&2
            echo "安装：sudo apt install libreoffice  或  brew install --cask libreoffice" >&2
            exit 1
        fi
        ;;
    
    md|markdown)
        # Markdown - 直接输出
        cat "$FILE"
        ;;
    
    txt|text)
        # 纯文本 - 直接输出
        cat "$FILE"
        ;;
    
    pdf)
        # PDF - 使用 pdftotext
        if command -v pdftotext &>/dev/null; then
            pdftotext "$FILE" -
        else
            echo "❌ 读取 PDF 需要 pdftotext (poppler-utils)" >&2
            echo "安装：sudo apt install poppler-utils  或  brew install poppler" >&2
            exit 1
        fi
        ;;
    
    html|htm)
        # HTML - 使用 pandoc 转换
        if command -v pandoc &>/dev/null; then
            pandoc "$FILE" -t "$FORMAT"
        else
            echo "❌ 需要安装 pandoc" >&2
            exit 1
        fi
        ;;
    
    *)
        echo "❌ 不支持的格式：$EXT" >&2
        echo "支持的格式：docx, doc, md, txt, pdf, html" >&2
        exit 1
        ;;
esac
