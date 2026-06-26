#!/bin/bash
# PRD 快速导出脚本

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
EXPORT_ENGINE="$SCRIPT_DIR/engines/export_engine.py"

# 默认值
OUTPUT_DIR="./output"
IMAGES_DIR=""

# 解析参数
while [[ $# -gt 0 ]]; do
    case $1 in
        -o|--output)
            OUTPUT_DIR="$2"
            shift 2
            ;;
        -i|--images)
            IMAGES_DIR="$2"
            shift 2
            ;;
        -h|--help)
            echo "用法：./export-prd.sh [选项] <输入文件.md>"
            echo ""
            echo "选项:"
            echo "  -o, --output <目录>    输出目录（默认：./output）"
            echo "  -i, --images <目录>   图片目录"
            echo "  -h, --help            显示帮助"
            exit 0
            ;;
        *)
            INPUT_FILE="$1"
            shift
            ;;
    esac
done

if [ -z "$INPUT_FILE" ]; then
    echo "❌ 错误：请指定输入文件"
    echo "用法：./export-prd.sh <输入文件.md>"
    exit 1
fi

# 创建输出目录
mkdir -p "$OUTPUT_DIR"

# 构建命令
CMD="python3 \"$EXPORT_ENGINE\" \"$INPUT_FILE\" -o \"$OUTPUT_DIR/$(basename "$INPUT_FILE" .md).docx\""

if [ -n "$IMAGES_DIR" ]; then
    CMD="$CMD --images \"$IMAGES_DIR\""
fi

# 执行
echo "📄 导出 PRD..."
echo "   输入：$INPUT_FILE"
echo "   输出：$OUTPUT_DIR"
[ -n "$IMAGES_DIR" ] && echo "   图片：$IMAGES_DIR"
echo ""

eval $CMD

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ 导出完成！"
    ls -lh "$OUTPUT_DIR"/*.docx 2>/dev/null | tail -1
else
    echo ""
    echo "❌ 导出失败"
    exit 1
fi
