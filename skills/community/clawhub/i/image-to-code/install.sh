#!/bin/bash
# image-to-code 技能安装脚本

echo "🐘 安装 image-to-code 技能..."

# 进入技能目录
cd "$(dirname "$0")"

# 检查 Python
if ! command -v python3 &> /dev/null; then
    echo "❌ 未找到 Python3，请先安装 Python3"
    exit 1
fi

echo "✅ Python 版本：$(python3 --version)"

# 安装依赖
echo "📦 安装依赖..."
pip3 install -r requirements.txt

if [ $? -eq 0 ]; then
    echo "✅ 依赖安装完成"
else
    echo "❌ 依赖安装失败"
    exit 1
fi

# 测试导入
echo "🧪 测试技能..."
python3 -c "from image_to_code import ImageToCodeConverter; print('✅ 技能导入成功')"

echo ""
echo "=========================================="
echo "✅ image-to-code 技能安装完成！"
echo "=========================================="
echo ""
echo "用法:"
echo "  python3 image_to_code.py input.png           # 转换图片"
echo "  python3 image_to_code.py input.png out.txt   # 转换并保存"
echo "  python3 image_to_code.py --help              # 查看帮助"
echo ""
echo "输出格式:"
echo "  文字：\$word->body(\"正文=内容=".$F);"
echo "  公式：\$word->formula(\"LaTeX\");"
echo "  图片：![image]"
echo ""
