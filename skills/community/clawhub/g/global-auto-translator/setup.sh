#!/bin/bash
# Global Auto Translator 安装脚本

set -e

echo "========================================="
echo "  Global Auto Translator - 安装程序"
echo "  跨境电商外贸智能翻译引擎"
echo "========================================="
echo ""

# 检查 Python3
if ! command -v python3 &> /dev/null; then
    echo "错误: 未找到 Python3，请先安装"
    exit 1
fi

echo "Python 版本: $(python3 --version)"

# 安装依赖
echo ""
echo "正在安装 Python 依赖..."
pip3 install --user requests langdetect pdfplumber python-docx docx2txt 2>&1 || \
pip3 install --user --break-system-packages requests langdetect pdfplumber python-docx docx2txt 2>&1

# 创建配置目录
mkdir -p ~/.openclaw/global-auto-translator

echo ""
echo "========================================="
echo "  安装完成!"
echo "========================================="
echo ""
echo "启动方式:"
echo "  python3 ~/.openclaw/workspace/skills/global-auto-translator/translate-daemon.py start"
echo ""
echo "停止方式:"
echo "  python3 ~/.openclaw/workspace/skills/global-auto-translator/translate-daemon.py stop"
echo ""
echo "文档翻译:"
echo "  python3 ~/.openclaw/workspace/skills/global-auto-translator/doc-translate.py 文件.pdf"
echo "  python3 ~/.openclaw/workspace/skills/global-auto-translator/doc-translate.py 文件.docx"
echo ""
echo "手动翻译:"
echo "  echo '文本' | python3 ~/.openclaw/workspace/skills/global-auto-translator/translate-daemon.py translate"
