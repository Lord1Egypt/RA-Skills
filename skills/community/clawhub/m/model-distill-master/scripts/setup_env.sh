#!/bin/bash
# 模型蒸馏环境设置脚本
# Usage: bash setup_env.sh [project_name]

set -e

PROJECT_NAME="${1:-model-distill}"
PROJECT_DIR="./$PROJECT_NAME"

echo "======================================"
echo "  模型蒸馏环境设置"
echo "======================================"

# 创建项目目录结构
echo "[1/5] 创建项目目录结构..."
mkdir -p "$PROJECT_DIR"/{config,scripts,src,data/{raw,synthetic,processed,teacher_analysis},outputs/{checkpoints,logs,eval_results}}

echo "目录结构:"
echo "$PROJECT_DIR/"
echo "├── config/           # 配置文件"
echo "├── scripts/          # 训练/评估脚本"
echo "├── src/              # Python模块"
echo "├── data/"
echo "│   ├── raw/          # 原始数据"
echo "│   ├── synthetic/    # 合成数据"
echo "│   ├── processed/    # 处理后数据"
echo "│   └── teacher_analysis/  # 教师分析结果"
echo "└── outputs/"
echo "    ├── checkpoints/  # 训练检查点"
echo "    ├── logs/         # 训练日志"
echo "    └── eval_results/ # 评估结果"

# 检查Python环境
echo ""
echo "[2/5] 检查Python环境..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "Python版本: $python_version"

# 安装依赖
echo ""
echo "[3/5] 安装依赖..."
pip install -q transformers torch datasets accelerate bitsandbytes peft unsloth
pip install -q huggingface-hub modelscope
pip install -q pyyaml tqdm jsonlines

echo "✅ 依赖安装完成"

# 检查CUDA
echo ""
echo "[4/5] 检查CUDA可用性..."
python3 -c "import torch; print(f'PyTorch版本: {torch.__version__}'); print(f'CUDA可用: {torch.cuda.is_available()}'); print(f'CUDA版本: {torch.version.cuda if torch.cuda.is_available() else \"N/A\"}')"

# 检查/下载gemma模型
echo ""
echo "[5/5] 检查学生模型 (gemma-3-4b-it)..."
if [ ! -d "./models/gemma-3-4b-it" ]; then
    echo "模型未找到，准备下载..."
    echo "下载源: ModelScope (中国镜像)"

    mkdir -p models
    cd models

    # 安装git-lfs（如未安装）
    if ! command -v git-lfs &> /dev/null; then
        echo "安装git-lfs..."
        # 根据系统安装git-lfs
        if [[ "$OSTYPE" == "linux-gnu"* ]]; then
            apt-get update && apt-get install -y git-lfs 2>/dev/null || echo "请手动安装git-lfs"
        elif [[ "$OSTYPE" == "darwin"* ]]; then
            brew install git-lfs 2>/dev/null || echo "请手动安装git-lfs"
        fi
    fi

    git lfs install
    git clone https://www.modelscope.cn/LLM-Research/gemma-3-4b-it.git
    cd ..

    echo "✅ 模型下载完成"
else
    echo "✅ 模型已存在"
fi

# 复制模板文件
echo ""
echo "复制模板文件到项目目录..."

# 这里可以复制预设的模板文件
cat > "$PROJECT_DIR/config/distill_config.yaml" << 'EOF'
model:
  teacher: "gpt-4"  # 或本地路径
  student: "./models/gemma-3-4b-it"

training:
  method: "qlora"
  num_epochs: 3
  batch_size: 8
  gradient_accumulation_steps: 4
  learning_rate: 2.0e-5
  warmup_ratio: 0.1
  logging_steps: 10
  save_steps: 500
  max_seq_length: 2048

lora:
  r: 64
  lora_alpha: 16
  target_modules: ["q_proj", "v_proj", "k_proj", "o_proj", "gate_proj", "up_proj", "down_proj"]
  lora_dropout: 0.05
  bias: "none"
  task_type: "CAUSAL_LM"

distillation:
  temperature: 2.0
  alpha: 0.7
  beta: 0.3

data:
  train_file: "data/processed/train.jsonl"
  eval_file: "data/processed/eval.jsonl"

evaluation:
  eval_steps: 500
  eval_tasks: ["gsm8k"]
EOF

echo ""
echo "======================================"
echo "  ✅ 环境设置完成！"
echo "======================================"
echo ""
echo "项目位置: $PROJECT_DIR"
echo ""
echo "下一步:"
echo "1. 配置教师模型 (config/distill_config.yaml)"
echo "2. 准备训练数据"
echo "3. 运行蒸馏训练"
echo ""
