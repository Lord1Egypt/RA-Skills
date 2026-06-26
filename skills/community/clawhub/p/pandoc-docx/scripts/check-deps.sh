#!/bin/bash
# check-deps.sh - 检查依赖
# 用途：验证 pandoc 和相关工具是否已安装

set -e

echo "╔══════════════════════════════════════════════════════════╗"
echo "║          pandoc-docx 依赖检查                             ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo ""

# 检测系统
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    SYSTEM="Linux"
    if command -v apt &>/dev/null; then
        PM="apt"
    elif command -v yum &>/dev/null; then
        PM="yum"
    elif command -v pacman &>/dev/null; then
        PM="pacman"
    else
        PM="unknown"
    fi
elif [[ "$OSTYPE" == "darwin"* ]]; then
    SYSTEM="macOS"
    PM="brew"
else
    SYSTEM="unknown"
    PM="unknown"
fi

echo "系统：$SYSTEM"
echo "包管理器：$PM"
echo ""

# 检查状态
ALL_OK=true

# 检查 pandoc（必需）
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "必需依赖"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

if command -v pandoc &>/dev/null; then
    echo "✅ pandoc"
    pandoc --version | head -1
else
    echo "❌ pandoc - 未安装"
    ALL_OK=false
fi

echo ""

# 检查可选依赖
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "可选依赖"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

if command -v libreoffice &>/dev/null; then
    echo "✅ libreoffice"
    libreoffice --version | head -1
else
    echo "⚠️  libreoffice - 未安装（支持 .doc 格式需要）"
fi

if command -v pdftotext &>/dev/null; then
    echo "✅ pdftotext (poppler-utils)"
    pdftotext -v 2>&1 | head -1
else
    echo "⚠️  pdftotext - 未安装（读取 PDF 需要）"
fi

if command -v tex &>/dev/null; then
    echo "✅ texlive（生成 PDF 需要）"
else
    echo "⚠️  texlive - 未安装（生成 PDF 需要）"
fi

echo ""

# 总结
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "总结"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

if [ "$ALL_OK" = true ]; then
    echo "✅ 所有必需依赖已安装"
    echo ""
    echo "🎉 pandoc-docx 已就绪！"
else
    echo "❌ 缺少必需依赖"
    echo ""
    echo "安装命令："
    if [ "$PM" = "apt" ]; then
        echo "  sudo apt install pandoc"
    elif [ "$PM" = "brew" ]; then
        echo "  brew install pandoc"
    elif [ "$PM" = "yum" ]; then
        echo "  sudo yum install pandoc"
    elif [ "$PM" = "pacman" ]; then
        echo "  sudo pacman -S pandoc"
    else
        echo "  请手动安装 pandoc"
    fi
fi

echo ""

# 安装建议
if [ "$ALL_OK" = false ]; then
    echo "💡 提示：安装后重新运行此脚本验证"
    echo "   $0"
    echo ""
fi

# 完整安装命令
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "完整安装（可选）"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

if [ "$PM" = "apt" ]; then
    echo "sudo apt install pandoc libreoffice poppler-utils texlive"
elif [ "$PM" = "brew" ]; then
    echo "brew install pandoc"
    echo "brew install --cask libreoffice"
    echo "brew install poppler"
    echo "brew install --cask mactex"
fi

echo ""
