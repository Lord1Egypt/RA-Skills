#!/bin/bash
# 知识库图片管理工具

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
KB_MANAGER="$SCRIPT_DIR/kb-manager.py"
IMAGE_MANAGER="$SCRIPT_DIR/image-manager.py"

case "$1" in
    add)
        # KB:业务 Q:问题 A:答案 IMG:图片路径
        if [ $# -lt 7 ]; then
            echo "用法：kb-image.sh add <业务名> <问题> <答案> <图片路径>"
            echo ""
            echo "示例:"
            echo "  kb-image.sh add 技术 '登录报错' '502 错误' '/tmp/error.png'"
            exit 1
        fi
        BUSINESS="$2"
        QUESTION="$3"
        ANSWER="$4"
        IMAGE_PATH="$5"
        
        # 保存图片
        echo "📸 保存图片..."
        SAVE_RESULT=$(python3 "$IMAGE_MANAGER" save "$BUSINESS" "$IMAGE_PATH")
        FILENAME=$(echo "$SAVE_RESULT" | python3 -c "import sys,json; print(json.load(sys.stdin).get('filename',''))")
        
        if [ -z "$FILENAME" ]; then
            echo "❌ 保存图片失败"
            echo "$SAVE_RESULT"
            exit 1
        fi
        
        # 提取 OCR 文字
        echo "🔍 提取 OCR 文字..."
        OCR_RESULT=$(python3 "$IMAGE_MANAGER" ocr "$IMAGE_PATH")
        OCR_TEXT=$(echo "$OCR_RESULT" | python3 -c "import sys,json; print(json.load(sys.stdin).get('text',''))")
        
        # 构建附件信息
        ATTACHMENT="{\"filename\":\"$FILENAME\",\"type\":\"image\",\"path\":\"$IMAGE_PATH\",\"ocr_text\":$(echo "$OCR_TEXT" | python3 -c "import sys,json; print(json.dumps(sys.stdin.read().strip()))" 2>/dev/null || echo '""')}"
        
        # 添加问答（带附件）
        echo "📝 添加问答..."
        python3 "$KB_MANAGER" add "$BUSINESS" "$QUESTION" "$ANSWER" "[]" "$ATTACHMENT"
        ;;
    
    ocr)
        if [ $# -lt 2 ]; then
            echo "用法：kb-image.sh ocr <图片路径>"
            exit 1
        fi
        python3 "$IMAGE_MANAGER" ocr "$2"
        ;;
    
    list)
        BUSINESS="${2:-}"
        if [ -z "$BUSINESS" ]; then
            python3 "$IMAGE_MANAGER" list
        else
            python3 "$IMAGE_MANAGER" list "$BUSINESS"
        fi
        ;;
    
    stats)
        python3 "$IMAGE_MANAGER" stats
        ;;
    
    *)
        echo "知识库图片管理工具"
        echo ""
        echo "用法：kb-image.sh <命令> [参数]"
        echo ""
        echo "命令:"
        echo "  add <业务> <问题> <答案> <图片>  - 添加带图片的问答"
        echo "  ocr <图片>                       - OCR 提取文字"
        echo "  list [业务]                      - 列出图片"
        echo "  stats                            - 统计信息"
        echo ""
        echo "示例:"
        echo "  kb-image.sh add 技术 '502 报错' '检查 Nginx' '/tmp/error.png'"
        echo "  kb-image.sh ocr '/tmp/screenshot.png'"
        echo "  kb-image.sh list 技术"
        echo "  kb-image.sh stats"
        ;;
esac
