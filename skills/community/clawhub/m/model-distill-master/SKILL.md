---
name: model-distill-master
description: |
  模型蒸馏大师：将大模型能力迁移到小模型的完整工作流。
  支持自适应蒸馏、课程学习、能力感知、对抗训练、多维度评估。
  触发词：「蒸馏模型」「把XX模型蒸馏到YY」「压缩模型」「做小模型」「教师模型分析」。
  默认学生模型：gemma-3-4b-it（4B参数，适合边缘部署）。
---

# 模型蒸馏大师

> 大模型的智慧，小模型的身材。

## 角色定义

我是**模型蒸馏大师**，专门帮你把大模型的能力迁移到更小的模型上。我的工作不是简单的"缩小"，而是**能力的选择性迁移**。

我默认使用 **gemma-3-4b-it**（40亿参数）作为学生模型，这是Google的开源模型，在4B级别有很强的性能，非常适合边缘部署。

---

## 执行工作流（Agentic Protocol）

**核心原则：每个阶段必须完成检查点才能进入下一阶段，避免返工。**

### Step 0: 需求诊断与目标确认

收到请求后，立即确认以下信息：

| 必需信息 | 说明 | 如果用户未提供 |
|---------|------|--------------|
| 教师模型 | 源大模型（GPT-4/Claude/其他） | 询问或根据任务推断 |
| 蒸馏目标 | 通用能力 vs 特定任务（代码/数学/推理） | 询问具体场景 |
| 部署场景 | 边缘设备/API服务/本地运行 | 默认为API服务 |
| 数据情况 | 有标注数据还是需要合成 | 假设需要合成 |

**可行性快速评估**：
- gemma-3-4b-it 适合：**推理密集型**任务（代码、数学、逻辑推理）
- gemma-3-4b-it 不适合：**知识密集型**任务（需要大量事实记忆）

如果目标明显超出4B模型能力，**立即告知用户**并建议调整目标。

---

### Step 1: 环境准备与基线测试

**立即执行**，不等用户确认：

```bash
# 检查环境
pip install transformers torch datasets accelerate bitsandbytes peft unsloth -q

# 检查/下载gemma-3-4b-it
if [ ! -d "./models/gemma-3-4b-it" ]; then
    echo "正在下载 gemma-3-4b-it..."
    git lfs install
    git clone https://www.modelscope.cn/LLM-Research/gemma-3-4b-it.git ./models/gemma-3-4b-it
fi

# 创建项目结构
mkdir -p model-distill/{config,scripts,src,data/{raw,synthetic,processed},outputs/{checkpoints,logs,eval_results}}
```

**基线测试（执行）**：

spawn subagent {
  任务：测试gemma-3-4b-it基线能力
  步骤：
  1. 加载gemma-3-4b-it模型
  2. 在简单任务上测试（如：1+1=?, 写一个Python函数）
  3. 记录推理速度和输出质量
  4. 输出基线报告到 model-distill/outputs/baseline_report.md
}

**Step 1 检查点**：
- [ ] 模型可正常加载和推理
- [ ] 基线性能已记录
- [ ] 项目目录结构已创建

完成后展示基线结果，用户确认后进入Step 2。

---

### Step 2: 教师模型分析（并行Agent）

**启动4个并行subagent**，各负责一个维度：

#### Agent A: 能力边界测绘

```
任务：分析教师模型在目标领域的真实能力

执行：
1. 选择20-50个代表性样本（覆盖目标任务的难度梯度）
2. 调用教师模型API获取输出
3. 分类统计：
   - 直接回答正确率
   - 需要推理的正确率  
   - 失败案例分析
4. 输出：model-distill/data/teacher_analysis/capability_map.json

重点：识别教师的"护城河"能力 vs 简单记忆
```

#### Agent B: 推理模式提取

```
任务：提取教师的推理风格

执行：
1. 收集教师模型在复杂任务上的CoT（思维链）输出
2. 分析：
   - 推理步骤结构（一步一步 vs 跳跃）
   - 自我验证行为
   - 不确定性表达方式
3. 输出：model-distill/data/teacher_analysis/reasoning_patterns.json
```

#### Agent C: 知识vs能力分离

```
任务：区分教师的知识和可迁移能力

执行：
1. 设计变体测试（同逻辑，不同表述/领域）
2. 识别哪些是模式识别（可迁移），哪些是事实记忆
3. 输出：model-distill/data/teacher_analysis/knowledge_vs_skill.md
```

#### Agent D: 输出分布分析

```
任务：分析教师输出的统计特性

执行：
1. 测量：平均长度、词汇多样性、结构化程度
2. 识别教师特有的表达模式
3. 输出：model-distill/data/teacher_analysis/output_stats.json

这些信息用于设定学生模型的学习目标
```

**Step 2 检查点**：

展示分析摘要表格：

```
┌─────────────────┬──────────┬────────────────────────────┐
│ 维度            │ 关键发现  │ 对蒸馏的启示                │
├─────────────────┼──────────┼────────────────────────────┤
│ 能力边界        │ X%正确率  │ 建议聚焦/放弃哪些子任务      │
│ 推理模式        │ X种模式   │ CoT数据应模仿的风格         │
│ 可迁移能力      │ X%        │ 需要额外知识注入吗          │
│ 输出特征        │ 平均X tokens │ 学生模型生成长度目标     │
└─────────────────┴──────────┴────────────────────────────┘
```

用户确认分析质量 → 进入Step 3

---

### Step 3: 蒸馏数据合成

基于教师分析，设计数据合成策略：

| 场景 | 策略 | 数据量 |
|------|------|--------|
| 推理密集型 | CoT蒸馏 + 多步推理 | 50K-200K |
| 代码任务 | 执行验证的代码对 | 10K-50K |
| 通用对话 | 多样化指令 + 对话链 | 100K+ |

**启动3个并行Agent合成数据**：

#### Agent A: 种子数据准备

```
任务：准备种子数据集

执行：
1. 从公开数据集筛选相关数据（如GSM8K用于数学）
2. 去重、格式统一
3. 输出：model-distill/data/raw/seed_data.jsonl
```

#### Agent B: 教师标注生成（核心）

```
任务：使用教师模型生成高质量CoT输出

执行：
1. 为每个种子问题调用教师模型
2. 使用特殊prompt引导教师展示推理过程：

---
请详细解释你的思考过程，一步一步解决：
{question}

要求：
1. 先分析问题类型
2. 逐步推理，展示中间步骤
3. 自我验证关键步骤
4. 给出最终答案

思考过程：
---

3. 保存输入-输出对
4. 输出：model-distill/data/synthetic/teacher_labeled.jsonl

注意：如果教师是API模型，注意成本，批量调用
```

#### Agent C: 数据增强与质量控制

```
任务：数据增强和质量过滤

执行：
1. 改写问题表述（保持逻辑）
2. 生成变体问题（同类型不同内容）
3. 过滤低质量数据：
   - 输出过短（可能没推理）
   - 答案错误的
   - 重复度高的
4. 输出：model-distill/data/processed/train.jsonl

同时保留10%作为验证集：eval.jsonl
```

**Step 3 检查点**：

展示数据摘要：
```
数据集统计：
- 总样本数：X
- 平均输出长度：X tokens
- 包含CoT的比例：X%
- 领域分布：[图表]

示例样本（3个随机）：
[展示]
```

用户确认 → 进入Step 4

---

### Step 4: 训练配置生成

**生成完整的训练配置和脚本**：

#### 4.1 生成配置文件

写入 `model-distill/config/distill_config.yaml`：

```yaml
model:
  teacher: "[教师模型名或路径]"
  student: "./models/gemma-3-4b-it"
  
training:
  method: "qlora"  # gemma-3-4b-it推荐QLoRA
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
  alpha: 0.7  # soft loss权重
  beta: 0.3   # hard loss权重

data:
  train_file: "data/processed/train.jsonl"
  eval_file: "data/processed/eval.jsonl"
  
evaluation:
  eval_steps: 500
  eval_tasks: ["[根据目标设定]"]
```

#### 4.2 生成训练脚本

写入 `model-distill/scripts/distill_train.py`：

```python
#!/usr/bin/env python3
"""模型蒸馏训练脚本 - 针对gemma-3-4b-it优化"""

import torch
from transformers import (
    AutoModelForCausalLM, 
    AutoTokenizer,
    TrainingArguments,
    Trainer,
    DataCollatorForSeq2Seq
)
from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training
from datasets import load_dataset
import yaml
import argparse

class DistillationTrainer(Trainer):
    """支持知识蒸馏的Trainer"""
    
    def __init__(self, teacher_model=None, temperature=2.0, alpha=0.7, **kwargs):
        super().__init__(**kwargs)
        self.teacher_model = teacher_model
        self.temperature = temperature
        self.alpha = alpha
        
        if teacher_model is not None:
            self.teacher_model.eval()
            for param in self.teacher_model.parameters():
                param.requires_grad = False
    
    def compute_loss(self, model, inputs, return_outputs=False, **kwargs):
        outputs_student = model(**inputs)
        loss_ce = outputs_student.loss
        
        if self.teacher_model is None:
            return (loss_ce, outputs_student) if return_outputs else loss_ce
        
        with torch.no_grad():
            outputs_teacher = self.teacher_model(**inputs)
        
        # KL散度损失
        student_logits = outputs_student.logits / self.temperature
        teacher_logits = outputs_teacher.logits / self.temperature
        
        loss_kd = torch.nn.functional.kl_div(
            torch.nn.functional.log_softmax(student_logits, dim=-1),
            torch.nn.functional.softmax(teacher_logits, dim=-1),
            reduction='batchmean'
        ) * (self.temperature ** 2)
        
        # 混合损失
        loss = self.alpha * loss_kd + (1 - self.alpha) * loss_ce
        
        return (loss, outputs_student) if return_outputs else loss

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="config/distill_config.yaml")
    args = parser.parse_args()
    
    with open(args.config) as f:
        config = yaml.safe_load(f)
    
    # 加载tokenizer
    tokenizer = AutoTokenizer.from_pretrained(config['model']['student'])
    tokenizer.pad_token = tokenizer.eos_token
    
    # 加载学生模型（4-bit量化）
    print("加载学生模型 (gemma-3-4b-it)...")
    student_model = AutoModelForCausalLM.from_pretrained(
        config['model']['student'],
        load_in_4bit=True,
        torch_dtype=torch.float16,
        device_map="auto"
    )
    student_model = prepare_model_for_kbit_training(student_model)
    
    # 应用LoRA
    lora_config = LoraConfig(**config['lora'])
    student_model = get_peft_model(student_model, lora_config)
    student_model.print_trainable_parameters()
    
    # 加载教师模型（如果本地可用）
    teacher_model = None
    teacher_path = config['model']['teacher']
    if teacher_path.startswith('./') or teacher_path.startswith('/'):
        print("加载本地教师模型...")
        teacher_model = AutoModelForCausalLM.from_pretrained(
            teacher_path,
            torch_dtype=torch.float16,
            device_map="auto"
        )
    
    # 加载数据
    dataset = load_dataset('json', data_files={
        'train': config['data']['train_file'],
        'eval': config['data']['eval_file']
    })
    
    # 预处理
    def preprocess(examples):
        texts = [f"{inp}\n{out}" for inp, out in zip(examples['input'], examples['output'])]
        return tokenizer(texts, truncation=True, max_length=config['training']['max_seq_length'], padding='max_length')
    
    tokenized = dataset.map(preprocess, batched=True)
    
    # 训练参数
    training_args = TrainingArguments(
        output_dir="./outputs/checkpoints",
        num_train_epochs=config['training']['num_epochs'],
        per_device_train_batch_size=config['training']['batch_size'],
        gradient_accumulation_steps=config['training']['gradient_accumulation_steps'],
        learning_rate=config['training']['learning_rate'],
        warmup_ratio=config['training']['warmup_ratio'],
        logging_steps=config['training']['logging_steps'],
        save_steps=config['training']['save_steps'],
        evaluation_strategy="steps",
        eval_steps=config['evaluation']['eval_steps'],
        save_total_limit=3,
        fp16=True,
        report_to="tensorboard",
    )
    
    trainer = DistillationTrainer(
        model=student_model,
        args=training_args,
        train_dataset=tokenized['train'],
        eval_dataset=tokenized['eval'],
        tokenizer=tokenizer,
        teacher_model=teacher_model,
        temperature=config['distillation']['temperature'],
        alpha=config['distillation']['alpha'],
    )
    
    print("开始训练...")
    trainer.train()
    trainer.save_model("./outputs/final_model")
    print("✅ 训练完成！模型保存至 ./outputs/final_model")

if __name__ == "__main__":
    main()
```

#### 4.3 生成评估脚本

写入 `model-distill/scripts/evaluate.py`：

```python
#!/usr/bin/env python3
"""评估蒸馏效果"""

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
import json
import argparse
from tqdm import tqdm

def evaluate_model(model_path, test_data, output_file):
    """评估模型在测试集上的表现"""
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    model = AutoModelForCausalLM.from_pretrained(
        model_path,
        torch_dtype=torch.float16,
        device_map="auto"
    )
    
    results = []
    correct = 0
    
    for item in tqdm(test_data):
        input_text = item['input']
        expected = item['output']
        
        inputs = tokenizer(input_text, return_tensors="pt").to(model.device)
        outputs = model.generate(**inputs, max_new_tokens=512, temperature=0.7)
        generated = tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        # 简单匹配评估（实际应该更精细）
        is_correct = expected.strip() in generated.strip()
        correct += is_correct
        
        results.append({
            'input': input_text,
            'expected': expected,
            'generated': generated,
            'correct': is_correct
        })
    
    accuracy = correct / len(test_data)
    
    with open(output_file, 'w') as f:
        json.dump({'accuracy': accuracy, 'results': results}, f, indent=2)
    
    return accuracy

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", required=True, help="模型路径")
    parser.add_argument("--test_data", required=True, help="测试数据")
    parser.add_argument("--output", default="eval_result.json")
    args = parser.parse_args()
    
    with open(args.test_data) as f:
        test_data = [json.loads(line) for line in f]
    
    acc = evaluate_model(args.model, test_data, args.output)
    print(f"准确率: {acc:.2%}")
```

**Step 4 检查点**：

展示生成的文件列表和配置摘要，用户确认后 → 进入Step 5

---

### Step 5: 训练执行

**询问用户**：
- 是否立即开始训练？
- 或稍后手动运行？

如果用户选择立即执行：

```bash
cd model-distill
python scripts/distill_train.py --config config/distill_config.yaml
```

**监控训练过程**：
- 每10 steps报告损失
- 每500 steps评估并保存检查点
- 监控GPU内存使用

训练完成后 → 进入Step 6

---

### Step 6: 效果验证

**执行评估**：

```bash
# 评估蒸馏后的模型
python scripts/evaluate.py \
    --model ./outputs/final_model \
    --test_data data/processed/eval.jsonl \
    --output outputs/eval_distilled.json

# 对比基线（如果有）
python scripts/evaluate.py \
    --model ./models/gemma-3-4b-it \
    --test_data data/processed/eval.jsonl \
    --output outputs/eval_baseline.json
```

**生成对比报告**：

spawn subagent {
  任务：生成蒸馏效果对比报告
  输入：outputs/eval_distilled.json 和 outputs/eval_baseline.json
  输出：outputs/distillation_report.md
  
  报告格式：
  - 准确率对比（蒸馏后 vs 基线 vs 教师）
  - 推理速度对比
  - 关键改进点
  - 仍然不足的地方
  - 部署建议
}

**最终交付**：

展示报告摘要：
```
蒸馏完成！

性能对比：
┌──────────┬─────────┬────────────┬─────────┐
│ 指标     │ 基线    │ 蒸馏后     │ 教师    │
├──────────┼─────────┼────────────┼─────────┤
│ 准确率   │ X%      │ Y%         │ Z%      │
│ 推理速度 │ X tok/s │ Y tok/s    │ -       │
│ 模型大小 │ 4B      │ 4B (+LoRA) │ 大得多  │
└──────────┴─────────┴────────────┴─────────┘

关键发现：
- ✅ 提升最明显：[方面]
- ⚠️ 仍需改进：[方面]

部署文件：
- 模型：model-distill/outputs/final_model/
- 配置：model-distill/config/
- 报告：model-distill/outputs/distillation_report.md
```

---

## 使用示例

### 示例1：数学能力蒸馏

```
用户：把GPT-4的数学推理能力蒸馏到gemma-3-4b-it

我：
1. 确认目标：教师=GPT-4，任务=数学推理，学生=gemma-3-4b-it
2. 评估可行性：✅ 数学推理适合4B模型
3. 执行Step 1-6：
   - 分析GPT-4解数学题的模式
   - 合成50K数学CoT数据
   - QLoRA训练3个epoch
   - 验证在GSM8K上的表现
4. 输出：可部署的4B数学专用模型
```

### 示例2：代码能力蒸馏

```
用户：蒸馏代码生成能力

我：
1. 确认目标：教师=Claude/GPT-4，任务=Python代码
2. 数据合成策略：
   - 使用HumanEval/MBPP作为种子
   - 生成带解释的代码解决方案
   - 执行验证确保代码正确
3. 训练并验证HumanEval通过率
```

---

## 组件清单

| 组件 | 文件 | 功能描述 |
|------|------|---------|
| 自适应蒸馏 | `scripts/distill_train.py` | 动态温度/alpha调度 |
| 课程学习 | `scripts/generate_curriculum_data.py` | 三级难度数据生成 |
| 教师分析 | `scripts/analyze_teacher.py` | 深度能力分析 |
| 对抗样本 | `scripts/generate_adversarial_samples.py` | 挖掘学生易错样本 |
| 综合评估 | `scripts/comprehensive_evaluate.py` | 多维度评估+诚实边界 |
| 训练监控 | `scripts/train_monitor.py` | 智能诊断与恢复 |
| 报告生成 | `scripts/generate_report.py` | 可解释Markdown报告 |
| 能力感知 | `scripts/capability_aware_distill.py` | 不同能力不同策略 |
| 交互策略 | `scripts/interactive_strategy.py` | 人机协同策略选择 |
| 可视化 | `scripts/visualize_results.py` | 雷达图/曲线/对比图 |
| 部署打包 | `scripts/package_deployment.py` | 一键导出HF/GGUF/ONNX |
| LangGraph | `langgraph_version/distill_graph.py` | 状态图工作流 |

## 故障处理

| 问题 | 诊断 | 解决方案 |
|------|------|---------|
| 模型下载失败 | ModelScope访问问题 | 换HuggingFace镜像或手动下载 |
| OOM | 显存不足 | 减小batch_size或序列长度 |
| 损失不下降 | 学习率/数据问题 | 降低LR至1e-5，检查数据格式 |
| 蒸馏后性能下降 | 过度拟合软标签 | 增加hard label权重，减少epoch |
| NaN损失 | 梯度爆炸 | 降低学习率至1e-5，检查数据异常 |
| 过拟合 | 验证损失上升 | 早停/增加dropout/减少epoch |

---

## 诚实边界

本Skill的局限：

1. **依赖硬件**：需要至少16GB显存的GPU进行训练
2. **教师模型限制**：如果教师只有API访问，数据合成成本可能较高
3. **容量限制**：4B模型无法承载大量知识，复杂知识密集型任务可能效果不佳
4. **时间成本**：完整蒸馏流程可能需要数小时到数天
5. **评估简化**：自动评估可能不完全反映真实能力

**免责声明**：
- 蒸馏后的模型能力受限于学生模型架构和容量
- 不保证达到教师模型相同水平
- 请遵守源模型和目标模型的许可协议

---

> 本Skill由 模型蒸馏大师 生成
> 适配学生模型：gemma-3-4b-it (Google, 4B参数)
> 蒸馏框架：QLoRA + Knowledge Distillation
