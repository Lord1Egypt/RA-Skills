#!/bin/bash
# doc-convert.sh - 格式转换
# 用途：在不同文档格式之间转换（支持批量转换和图片提取）

set -e

INPUT=""
OUTPUT=""
EXTRACT_MEDIA=""
REFERENCE_DOC=""
WRAP_MODE=""

# 解析参数
while [ $# -gt 0 ]; do
    case "$1" in
        -o|--output)
            OUTPUT="$2"
            shift 2
            ;;
        --extract-media)
            EXTRACT_MEDIA="--extract-media=$2"
            shift 2
            ;;
        --reference-doc)
            REFERENCE_DOC="--reference-doc=$2"
            shift 2
            ;;
        --wrap)
            WRAP_MODE="--wrap=$2"
            shift 2
            ;;
        -h|--help)
            echo "用法：$0 <输入文件> -o <输出文件> [选项]"
            echo ""
            echo "选项:"
            echo "  -o, --output <文件>       输出文件路径（必需）"
            echo "  --extract-media <目录>    提取图片到指定目录"
            echo "  --reference-doc <文件>    使用参考文档（保持样式）"
            echo "  --wrap <模式>             文本换行模式 (preserve|auto|none)"
            echo "  -h, --help                显示帮助信息"
            echo ""
            echo "支持的格式:"
            echo "  输入：docx, doc, md, txt, pdf, html"
            echo "  输出：docx, doc, md, txt, pdf, html, epub"
            echo ""
            echo "示例:"
            echo "  $0 input.docx -o output.md"
            echo "  $0 input.md -o output.docx"
            echo "  $0 input.docx -o output.md --extract-media=./images"
            echo "  $0 input.md -o output.docx --reference-doc=template.docx"
            exit 0
            ;;
        *)
            if [ -z "$INPUT" ]; then
                INPUT="$1"
            fi
            shift
            ;;
    esac
done

# 参数验证
if [ -z "$INPUT" ] || [ -z "$OUTPUT" ]; then
    echo "❌ 错误：需要指定输入和输出文件" >&2
    echo "使用 -h 查看帮助" >&2
    exit 1
fi

# 检查输入文件
if [ ! -f "$INPUT" ]; then
    echo "❌ 文件不存在：$INPUT" >&2
    exit 1
fi

# 检查 pandoc
if ! command -v pandoc &>/dev/null; then
    echo "❌ 需要安装 pandoc" >&2
    echo "安装：sudo apt install pandoc  或  brew install pandoc" >&2
    exit 1
fi

# 获取文件扩展名
INPUT_EXT="${INPUT##*.}"
OUTPUT_EXT="${OUTPUT##*.}"

# 特殊处理 .doc 格式
if [ "$INPUT_EXT" = "doc" ]; then
    if command -v libreoffice &>/dev/null; then
        TMPDOCX=$(mktemp --suffix=.docx)
        libreoffice --headless --convert-to docx "$INPUT" --outdir "$(dirname "$TMPDOCX")" >/dev/null 2>&1
        mv "$(dirname "$TMPDOCX")/$(basename "$INPUT" .doc).docx" "$TMPDOCX"
        INPUT="$TMPDOCX"
        trap "rm -f $TMPDOCX" EXIT
    else
        echo "❌ 转换 .doc 需要 libreoffice" >&2
        exit 1
    fi
fi

# 执行转换
pandoc "$INPUT" -o "$OUTPUT" $EXTRACT_MEDIA $REFERENCE_DOC $WRAP_MODE

echo "✅ 转换完成：$INPUT → $OUTPUT"

# 如果有提取媒体，显示信息
if [ -n "$EXTRACT_MEDIA" ]; then
    MEDIA_DIR="${EXTRACT_MEDIA#--extract-media=}"
    if [ -d "$MEDIA_DIR" ]; then
        IMAGE_COUNT=$(find "$MEDIA_DIR" -type f | wc -l)
        echo "📸 已提取 $IMAGE_COUNT 个文件到：$MEDIA_DIR"
    fi
fi
