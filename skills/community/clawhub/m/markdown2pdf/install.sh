#!/bin/bash
# markdown2pdf 安装脚本

echo "🚀 安装 markdown2pdf 依赖..."

# 检查 Python
echo "📌 检查 Python..."
python3 --version || {
    echo "❌ Python3 未安装，请先安装 Python 3.10+"
    exit 1
}

# 检查 pip
echo "📌 检查 pip..."
if command -v pip3 &> /dev/null; then
    PIP_CMD="pip3"
elif command -v pip &> /dev/null; then
    PIP_CMD="pip"
elif python3 -m pip &> /dev/null; then
    PIP_CMD="python3 -m pip"
else
    echo "❌ pip 未安装，请安装 pip"
    exit 1
fi

echo "✅ 使用 $PIP_CMD"

# 安装 Python 依赖
echo "📦 安装 Python 依赖..."
$PIP_CMD install markdown pdfkit imgkit

# 检查 wkhtmltopdf
echo "📌 检查 wkhtmltopdf..."
if command -v wkhtmltopdf &> /dev/null; then
    echo "✅ wkhtmltopdf 已安装"
    wkhtmltopdf --version
else
    echo "⚠️  wkhtmltopdf 未安装"
    echo ""
    echo "请手动安装 wkhtmltopdf:"
    echo "  macOS:  brew install wkhtmltopdf"
    echo "  Ubuntu: sudo apt-get install wkhtmltopdf"
    echo "  CentOS: sudo yum install wkhtmltopdf"
    echo "  Windows: 下载 https://wkhtmltopdf.org/downloads.html"
    echo ""
fi

echo ""
echo "✅ 安装完成！"
echo ""
echo "使用方法:"
echo "  python3 src/converter.py <input.md> [-t theme] [-f formats]"
echo ""
echo "示例:"
echo "  python3 src/converter.py test_document.md -t github -f pdf"
echo ""
