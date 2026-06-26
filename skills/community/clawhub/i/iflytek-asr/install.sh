#!/bin/bash

echo "🚀 讯飞语音转文本 Skill 安装脚本"
echo ""

# 检查 Python
if ! command -v python3 &> /dev/null; then
    echo "❌ 错误：未找到 Python 3"
    echo "   请先安装 Python 3: https://www.python.org/downloads/"
    exit 1
fi

echo "✅ Python 3 已安装: $(python3 --version)"

# 安装依赖
echo ""
echo "📦 安装 Python 依赖..."
pip3 install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "❌ 依赖安装失败"
    exit 1
fi

echo "✅ 依赖安装完成"

# 配置凭证
echo ""
if [ ! -f .env ]; then
    echo "📝 创建凭证配置文件..."
    cp .env.example .env
    echo "✅ 已创建 .env 文件"
    echo ""
    echo "⚠️  下一步：编辑 .env 文件并填入你的讯飞 API 凭证"
    echo "   1. 访问 https://www.xfyun.cn 获取凭证"
    echo "   2. 编辑 .env 文件: nano .env"
    echo "   3. 运行测试: python3 scripts/speech_to_text.py --help"
else
    echo "✅ .env 文件已存在"
fi

echo ""
echo "🎉 安装完成！"
echo ""
echo "快速开始："
echo "  查看文档: cat QUICKSTART.md"
echo "  测试转录: python3 scripts/speech_to_text.py test.mp3"
