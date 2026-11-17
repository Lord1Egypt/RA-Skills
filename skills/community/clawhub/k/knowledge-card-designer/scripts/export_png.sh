#!/bin/bash
# 小绿书批量截图脚本
# 自动将HTML转换为PNG图片

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 检查参数
if [ $# -eq 0 ]; then
    echo -e "${RED}错误：请指定HTML文件所在目录${NC}"
    echo "用法: ./export_png.sh <目录路径>"
    echo "示例: ./export_png.sh /path/to/xiaogreenbook_topic"
    exit 1
fi

TARGET_DIR="$1"

if [ ! -d "$TARGET_DIR" ]; then
    echo -e "${RED}错误：目录不存在 $TARGET_DIR${NC}"
    exit 1
fi

cd "$TARGET_DIR" || exit 1

echo -e "${YELLOW}🚀 开始批量截图...${NC}"
echo "目录: $TARGET_DIR"
echo ""

# 检查chrome是否可用
if ! command -v google-chrome &> /dev/null; then
    if ! command -v chromium-browser &> /dev/null; then
        echo -e "${RED}错误：未找到Chrome或Chromium浏览器${NC}"
        exit 1
    else
        CHROME="chromium-browser"
    fi
else
    CHROME="google-chrome"
fi

# 截图计数器
SUCCESS=0
FAILED=0

# 生成横幅封面 (900×383)
if [ -f "cover.html" ]; then
    echo -n "📷 生成横幅封面 (900×383)... "
    if $CHROME --headless --no-sandbox --disable-gpu \
        --screenshot=cover.png \
        --window-size=900,383 \
        --hide-scrollbars \
        --disable-logging \
        file://$(pwd)/cover.html 2>/dev/null; then
        echo -e "${GREEN}✓${NC}"
        ((SUCCESS++))
    else
        echo -e "${RED}✗${NC}"
        ((FAILED++))
    fi
fi

# 生成卡片封面 (1080×1350)
if [ -f "cover_card.html" ]; then
    echo -n "📷 生成卡片封面 (1080×1350)... "
    if $CHROME --headless --no-sandbox --disable-gpu \
        --screenshot=cover_card.png \
        --window-size=1080,1350 \
        --hide-scrollbars \
        --disable-logging \
        file://$(pwd)/cover_card.html 2>/dev/null; then
        echo -e "${GREEN}✓${NC}"
        ((SUCCESS++))
    else
        echo -e "${RED}✗${NC}"
        ((FAILED++))
    fi
fi

# 生成内容卡片 (1080×1350)
for html_file in card*.html; do
    if [ -f "$html_file" ]; then
        png_file="${html_file%.html}.png"
        echo -n "📷 生成 $png_file... "
        if $CHROME --headless --no-sandbox --disable-gpu \
            --screenshot="$png_file" \
            --window-size=1080,1350 \
            --hide-scrollbars \
            --disable-logging \
            "file://$(pwd)/$html_file" 2>/dev/null; then
            echo -e "${GREEN}✓${NC}"
            ((SUCCESS++))
        else
            echo -e "${RED}✗${NC}"
            ((FAILED++))
        fi
    fi
done

echo ""
echo -e "${GREEN}✅ 截图完成！${NC}"
echo "成功: $SUCCESS, 失败: $FAILED"
echo ""
echo "生成文件:"
ls -lh *.png 2>/dev/null || echo "无PNG文件"
