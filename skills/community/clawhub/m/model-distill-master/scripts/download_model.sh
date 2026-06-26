#!/bin/bash
# 下载gemma-3-4b-it模型脚本
# Usage: bash download_model.sh [output_dir]

set -e

OUTPUT_DIR="${1:-./models}"
MODEL_NAME="gemma-3-4b-it"
MODEL_PATH="$OUTPUT_DIR/$MODEL_NAME"

echo "======================================"
echo "  下载Gemma-3-4B-IT模型"
echo "======================================"

# 创建输出目录
mkdir -p "$OUTPUT_DIR"

# 检查git-lfs
if ! command -v git-lfs &> /dev/null; then
    echo "⚠️  git-lfs未安装，正在安装..."
    # 尝试自动安装
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        apt-get update -qq && apt-get install -y -qq git-lfs || true
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        brew install git-lfs 2>/dev/null || true
    elif [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" ]]; then
        # Windows
        echo "请在Windows上手动安装git-lfs: https://git-lfs.github.com/"
        exit 1
    fi
fi

# 初始化git-lfs
git lfs install

# 检查模型是否已存在
if [ -d "$MODEL_PATH" ]; then
    echo "模型目录已存在: $MODEL_PATH"
    read -p "是否重新下载? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "使用现有模型"
        exit 0
    fi
    rm -rf "$MODEL_PATH"
fi

# 下载模型
echo ""
echo "正在从ModelScope下载模型..."
echo "这通常需要10-30分钟，取决于网络速度"
echo ""

cd "$OUTPUT_DIR"
git clone https://www.modelscope.cn/LLM-Research/gemma-3-4b-it.git

echo ""
echo "✅ 模型下载完成！"
echo "模型位置: $MODEL_PATH"
echo ""

# 验证模型文件
echo "验证模型文件..."
if [ -f "$MODEL_PATH/config.json" ]; then
    echo "✅ config.json 存在"
else
    echo "⚠️  config.json 不存在，可能下载不完整"
fi

if [ -f "$MODEL_PATH/model.safetensors.index.json" ] || [ -f "$MODEL_PATH/pytorch_model.bin" ]; then
    echo "✅ 模型权重文件存在"
else
    echo "⚠️  模型权重文件可能不完整"
fi

echo ""
echo "模型大小:"
du -sh "$MODEL_PATH" 2>/dev/null || echo "无法计算大小"

echo ""
echo "======================================"
echo "  下一步: 测试模型加载"
echo "======================================"
echo ""
echo "运行测试:"
echo "  python3 -c \"from transformers import AutoModel; model = AutoModel.from_pretrained('$MODEL_PATH')\""
