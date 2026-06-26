# 模型蒸馏大师 (Model Distill Master)

一个完整的模型蒸馏工作流 Skill，用于将大模型能力迁移到更小的模型（默认 gemma-3-4b-it）。

## 快速开始

### 1. 安装 Skill

```bash
npx skills add model-distill-master
```

### 2. 使用

在 Claude Code 中输入：

```
蒸馏模型：把 GPT-4 的数学能力迁移到 gemma-3-4b-it
```

或：

```
做小模型：需要一个4B的代码专用模型
```

## 目录结构

```
model-distill-skill/
├── SKILL.md                    # 主 Skill 定义
├── README.md                   # 本文件
├── references/
│   └── methodology.md          # 蒸馏方法论
├── scripts/
│   ├── setup_env.sh            # 环境设置
│   ├── download_model.sh       # 下载 gemma-3-4b-it
│   ├── baseline_test.py        # 基线测试
│   ├── generate_cot_data.py    # CoT 数据生成
│   ├── distill_train.py        # 蒸馏训练
│   ├── merge_lora.py           # 合并 LoRA 权重
│   └── evaluate.py             # 模型评估
└── examples/
    ├── math_distill_example.yaml   # 数学蒸馏示例配置
    └── sample_data.txt             # 示例训练数据格式说明
```

## 工作流说明

### Phase 0: 需求诊断
- 确认教师模型（GPT-4/Claude/开源大模型）
- 确认蒸馏目标（数学/代码/推理/通用）
- 评估 gemma-3-4b-it 的适用性

### Phase 1: 环境准备
- 自动下载 gemma-3-4b-it
- 创建项目目录结构
- 运行基线测试

### Phase 2: 教师模型分析（4个并行 Agent）
- Agent A: 能力边界测绘
- Agent B: 推理模式提取
- Agent C: 知识 vs 能力分离
- Agent D: 输出分布分析

### Phase 3: 数据合成（3个并行 Agent）
- Agent A: 种子数据准备
- Agent B: 教师 CoT 标注生成
- Agent C: 数据增强与质量控制

### Phase 4: 训练配置生成
- 生成 `distill_config.yaml`
- 生成训练脚本
- 生成评估脚本

### Phase 5: 训练执行
- QLoRA 训练
- 实时监控损失曲线
- 自动保存检查点

### Phase 6: 效果验证
- 对比基线模型
- 生成评估报告
- 导出部署配置

## 默认学生模型

**gemma-3-4b-it** (Google)
- 参数量：4B
- 架构：Transformer Decoder
- 特点：
  - 推理友好，适合边缘部署
  - 支持 2048 token 上下文
  - 开源可商用

## 支持的蒸馏策略

| 策略 | 适用场景 | 数据量建议 |
|------|----------|-----------|
| CoT 蒸馏 | 推理密集型（数学/逻辑） | 50K-200K |
| 标准 KD | 通用能力迁移 | 100K+ |
| 任务专用 | 特定能力强化 | 10K-50K |

## 脚本使用说明

### 环境设置

```bash
cd model-distill-skill
bash scripts/setup_env.sh [项目名]
```

### 下载模型

```bash
bash scripts/download_model.sh ./models
```

### 基线测试

```bash
python scripts/baseline_test.py ./models/gemma-3-4b-it ./outputs/baseline.json
```

### 生成 CoT 数据

```bash
python scripts/generate_cot_data.py \
    --input data/raw/questions.jsonl \
    --output data/synthetic/cot_data.jsonl \
    --teacher gpt-4
```

### 训练

```bash
python scripts/distill_train.py --config config/distill_config.yaml
```

### 合并 LoRA

```bash
python scripts/merge_lora.py \
    --lora_path outputs/final_model \
    --output outputs/merged_model
```

### 评估

```bash
python scripts/evaluate.py \
    --model outputs/final_model \
    --baseline ./models/gemma-3-4b-it \
    --test_data data/processed/eval.jsonl \
    --output eval_report.json
```

## 数据格式

训练数据应为 JSONL 格式，每行一个样本：

```json
{"input": "问题内容", "output": "带CoT的详细回答"}
```

示例：

```json
{"input": "15 × 24 = ?", "output": "思考过程：\n1. 24 = 20 + 4\n2. 15 × 20 = 300\n3. 15 × 4 = 60\n4. 300 + 60 = 360\n\n答案：360"}
```

## 配置说明

见 `examples/math_distill_example.yaml`

关键配置项：

```yaml
model:
  teacher: "gpt-4"              # 教师模型
  student: "./models/gemma-3-4b-it"  # 学生模型

training:
  method: "qlora"               # 训练方法: qlora/lora/full
  num_epochs: 3                 # 训练轮数
  batch_size: 8                 # 批次大小
  learning_rate: 2.0e-5         # 学习率

lora:
  r: 64                         # LoRA rank
  lora_alpha: 16                # LoRA alpha

distillation:
  temperature: 2.0              # 蒸馏温度
  alpha: 0.7                    # 软标签权重
```

## 硬件要求

- **最低配置**：16GB GPU（RTX 3090/V100）
- **推荐配置**：24GB GPU（RTX 4090/A10）
- **磁盘空间**：~20GB（模型 + 数据 + 检查点）

## 故障排除

| 问题 | 解决方案 |
|------|----------|
| OOM | 减小 `batch_size` 或 `max_seq_length` |
| 模型下载失败 | 使用 HuggingFace 镜像或手动下载 |
| 损失不下降 | 降低学习率，检查数据格式 |
| 蒸馏后性能下降 | 增加软标签权重(alpha)，延长训练时间 |

## 许可证

MIT License

## 参考

- [知识蒸馏原始论文](https://arxiv.org/abs/1503.02531)
- [DistilBERT](https://arxiv.org/abs/1910.01108)
- [Gemma 模型文档](https://ai.google.dev/gemma)
