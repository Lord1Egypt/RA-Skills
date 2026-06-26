#!/usr/bin/env python3
"""
模型蒸馏训练脚本 - 针对 gemma-4-E4B-it 优化
支持：标准KD、QLoRA微调、自适应蒸馏损失

升级特性：
1. 动态 Temperature Schedule - 从高(2.0)到低(0.5)的余弦退火
2. 动态 Alpha Schedule - 从软标签主导(0.9)到硬标签主导(0.5)
3. 支持多种调度策略：cosine, linear, step
"""

import torch
import torch.nn.functional as F
import math
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    TrainingArguments,
    Trainer,
    TrainerCallback,
    DataCollatorForLanguageModeling
)
from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training
from datasets import load_dataset
import yaml
import argparse
import os
from pathlib import Path
from typing import Optional, Literal


class AdaptiveDistillationScheduler:
    """
    自适应蒸馏调度器

    动态调整 temperature 和 alpha，实现更好的蒸馏效果：
    - 前期：高 temperature (2.0) + 高 alpha (0.9) → 学习教师的分布
    - 后期：低 temperature (0.5) + 低 alpha (0.5) → 学习准确率

    支持策略：
    - cosine: 余弦退火，平滑过渡
    - linear: 线性下降
    - step: 阶梯式下降
    """

    def __init__(
        self,
        initial_temp: float = 2.0,
        final_temp: float = 0.5,
        initial_alpha: float = 0.9,
        final_alpha: float = 0.5,
        temp_schedule: Literal["cosine", "linear", "step"] = "cosine",
        alpha_schedule: Literal["cosine", "linear", "step"] = "step",
        warmup_ratio: float = 0.1,
        step_milestones: list = None
    ):
        self.initial_temp = initial_temp
        self.final_temp = final_temp
        self.initial_alpha = initial_alpha
        self.final_alpha = final_alpha
        self.temp_schedule = temp_schedule
        self.alpha_schedule = alpha_schedule
        self.warmup_ratio = warmup_ratio
        self.step_milestones = step_milestones or [0.4, 0.7]  # 默认在40%和70%处阶梯下降

        self.current_temp = initial_temp
        self.current_alpha = initial_alpha
        self.current_step = 0
        self.total_steps = 0

    def set_total_steps(self, total_steps: int):
        """设置总步数"""
        self.total_steps = total_steps

    def get_temperature(self, progress: float) -> float:
        """
        计算当前 temperature

        Args:
            progress: 训练进度 (0.0 - 1.0)

        Returns:
            当前 temperature
        """
        # Warmup 阶段保持初始值
        if progress < self.warmup_ratio:
            return self.initial_temp

        # 归一化进度 (0.0 - 1.0)
        adjusted_progress = (progress - self.warmup_ratio) / (1 - self.warmup_ratio)
        adjusted_progress = max(0.0, min(1.0, adjusted_progress))

        if self.temp_schedule == "cosine":
            # 余弦退火：从 initial 到 final
            return self.final_temp + (self.initial_temp - self.final_temp) * \
                   (1 + math.cos(math.pi * adjusted_progress)) / 2

        elif self.temp_schedule == "linear":
            # 线性下降
            return self.initial_temp + (self.final_temp - self.initial_temp) * adjusted_progress

        elif self.temp_schedule == "step":
            # 阶梯式
            for milestone in self.step_milestones:
                if adjusted_progress >= milestone:
                    return self.final_temp + (self.initial_temp - self.final_temp) * 0.5
            return self.initial_temp

        else:
            return self.initial_temp

    def get_alpha(self, progress: float) -> float:
        """
        计算当前 alpha（软标签权重）

        Args:
            progress: 训练进度 (0.0 - 1.0)

        Returns:
            当前 alpha
        """
        # Warmup 阶段保持初始值
        if progress < self.warmup_ratio:
            return self.initial_alpha

        adjusted_progress = (progress - self.warmup_ratio) / (1 - self.warmup_ratio)
        adjusted_progress = max(0.0, min(1.0, adjusted_progress))

        if self.alpha_schedule == "cosine":
            return self.final_alpha + (self.initial_alpha - self.final_alpha) * \
                   (1 + math.cos(math.pi * adjusted_progress)) / 2

        elif self.alpha_schedule == "linear":
            return self.initial_alpha + (self.final_alpha - self.initial_alpha) * adjusted_progress

        elif self.alpha_schedule == "step":
            # 硬切换：前期软标签，后期硬标签
            threshold = 0.6  # 60% 时切换
            if adjusted_progress >= threshold:
                return self.final_alpha
            else:
                return self.initial_alpha

        else:
            return self.initial_alpha

    def step(self, current_step: int):
        """更新当前步数并计算参数"""
        self.current_step = current_step
        if self.total_steps > 0:
            progress = current_step / self.total_steps
            self.current_temp = self.get_temperature(progress)
            self.current_alpha = self.get_alpha(progress)

    def get_current_params(self) -> tuple:
        """获取当前参数"""
        return self.current_temp, self.current_alpha

    def __repr__(self):
        return f"AdaptiveDistillationScheduler(temp={self.current_temp:.3f}, alpha={self.current_alpha:.3f})"


class DistillationTrainingCallback(TrainerCallback):
    """
    蒸馏训练回调，用于更新 scheduler 和记录参数
    """

    def __init__(self, scheduler: AdaptiveDistillationScheduler, log_every: int = 50):
        self.scheduler = scheduler
        self.log_every = log_every

    def on_step_begin(self, args, state, control, **kwargs):
        """每步开始时更新 scheduler"""
        if state.global_step > 0:
            self.scheduler.step(state.global_step)

    def on_log(self, args, state, control, logs=None, **kwargs):
        """记录时添加当前蒸馏参数"""
        if state.global_step % self.log_every == 0:
            temp, alpha = self.scheduler.get_current_params()
            if logs is not None:
                logs['distill/temperature'] = temp
                logs['distill/alpha'] = alpha
                logs['distill/schedule_progress'] = state.global_step / state.max_steps if state.max_steps > 0 else 0


class DistillationTrainer(Trainer):
    """
    支持知识蒸馏的 Trainer（自适应版本）

    特性：
    1. 支持自适应 temperature 和 alpha
    2. 动态调整蒸馏策略
    3. 详细的损失记录
    """

    def __init__(
        self,
        teacher_model=None,
        scheduler: Optional[AdaptiveDistillationScheduler] = None,
        temperature: float = 2.0,  # 仅在没有 scheduler 时使用
        alpha: float = 0.7,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.teacher_model = teacher_model
        self.scheduler = scheduler
        self.static_temperature = temperature
        self.static_alpha = alpha

        if teacher_model is not None:
            self.teacher_model.eval()
            for param in self.teacher_model.parameters():
                param.requires_grad = False

    def get_distillation_params(self) -> tuple:
        """获取当前蒸馏参数"""
        if self.scheduler is not None:
            return self.scheduler.get_current_params()
        return self.static_temperature, self.static_alpha

    def compute_loss(self, model, inputs, return_outputs=False, **kwargs):
        """计算自适应蒸馏损失"""
        # 学生模型前向
        outputs_student = model(**inputs)
        loss_ce = outputs_student.loss

        if self.teacher_model is None:
            return (loss_ce, outputs_student) if return_outputs else loss_ce

        # 获取当前蒸馏参数
        temperature, alpha = self.get_distillation_params()

        # 教师模型前向（无梯度）
        with torch.no_grad():
            outputs_teacher = self.teacher_model(**inputs)

        # KL散度损失（软标签）
        student_logits = outputs_student.logits / temperature
        teacher_logits = outputs_teacher.logits / temperature

        loss_kd = F.kl_div(
            F.log_softmax(student_logits, dim=-1),
            F.softmax(teacher_logits, dim=-1),
            reduction='batchmean'
        ) * (temperature ** 2)

        # 混合损失：alpha * 软标签 + (1-alpha) * 硬标签
        loss = alpha * loss_kd + (1 - alpha) * loss_ce

        # 记录各个损失（用于日志）
        if return_outputs:
            outputs_student.distill_loss = loss_kd.item()
            outputs_student.ce_loss = loss_ce.item()
            outputs_student.temperature = temperature
            outputs_student.alpha = alpha

        return (loss, outputs_student) if return_outputs else loss


def load_model_and_tokenizer(model_path, use_4bit=False):
    """加载模型和分词器"""
    print(f"加载模型: {model_path}")

    tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    if use_4bit:
        model = AutoModelForCausalLM.from_pretrained(
            model_path,
            load_in_4bit=True,
            torch_dtype=torch.float16,
            device_map="auto",
            trust_remote_code=True
        )
        model = prepare_model_for_kbit_training(model)
    else:
        model = AutoModelForCausalLM.from_pretrained(
            model_path,
            torch_dtype=torch.float16,
            device_map="auto",
            trust_remote_code=True
        )

    return model, tokenizer


def apply_lora(model, lora_config):
    """应用LoRA配置"""
    config = LoraConfig(**lora_config)
    model = get_peft_model(model, config)
    model.print_trainable_parameters()
    return model


def create_scheduler(config: dict, total_steps: int) -> Optional[AdaptiveDistillationScheduler]:
    """
    根据配置创建调度器

    如果配置中启用了 adaptive_distillation，则创建调度器
    否则返回 None，使用固定参数
    """
    distill_config = config.get('distillation', {})

    # 检查是否启用自适应蒸馏
    if not distill_config.get('adaptive', False):
        print("使用固定蒸馏参数")
        print(f"  Temperature: {distill_config.get('temperature', 2.0)}")
        print(f"  Alpha: {distill_config.get('alpha', 0.7)}")
        return None

    # 创建自适应调度器
    scheduler = AdaptiveDistillationScheduler(
        initial_temp=distill_config.get('initial_temperature', 2.0),
        final_temp=distill_config.get('final_temperature', 0.5),
        initial_alpha=distill_config.get('initial_alpha', 0.9),
        final_alpha=distill_config.get('final_alpha', 0.5),
        temp_schedule=distill_config.get('temp_schedule', 'cosine'),
        alpha_schedule=distill_config.get('alpha_schedule', 'step'),
        warmup_ratio=distill_config.get('warmup_ratio', 0.1)
    )
    scheduler.set_total_steps(total_steps)

    print("✅ 启用自适应蒸馏损失")
    print(f"  Temperature: {scheduler.initial_temp} → {scheduler.final_temp} ({scheduler.temp_schedule})")
    print(f"  Alpha: {scheduler.initial_alpha} → {scheduler.final_alpha} ({scheduler.alpha_schedule})")
    print(f"  Warmup: {scheduler.warmup_ratio * 100}%")

    return scheduler


def main():
    parser = argparse.ArgumentParser(description="模型蒸馏训练（自适应版本）")
    parser.add_argument("--config", type=str, default="config/distill_config.yaml",
                        help="配置文件路径")
    parser.add_argument("--output_dir", type=str, default=None,
                        help="输出目录（覆盖配置文件）")
    parser.add_argument("--no-adaptive", action="store_true",
                        help="禁用自适应蒸馏，使用固定参数")
    args = parser.parse_args()

    # 加载配置
    with open(args.config, 'r') as f:
        config = yaml.safe_load(f)

    # 如果命令行禁用自适应，覆盖配置
    if args.no_adaptive:
        config['distillation']['adaptive'] = False

    # 设置输出目录
    output_dir = args.output_dir or config['training'].get('output_dir', './outputs/checkpoints')
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    # 加载学生模型
    print("\n" + "="*50)
    print("🚀 模型蒸馏训练（自适应版本）")
    print("="*50)

    print("\n加载学生模型...")
    use_4bit = config['training'].get('method') == 'qlora'
    student_model, tokenizer = load_model_and_tokenizer(
        config['model']['student'],
        use_4bit=use_4bit
    )

    # 应用LoRA
    if config['training']['method'] in ['lora', 'qlora']:
        print("\n应用LoRA...")
        student_model = apply_lora(student_model, config['lora'])

    # 加载教师模型（如果本地可用）
    teacher_model = None
    teacher_path = config['model']['teacher']
    if teacher_path.startswith('./') or teacher_path.startswith('/'):
        if Path(teacher_path).exists():
            print("\n加载本地教师模型...")
            teacher_model, _ = load_model_and_tokenizer(teacher_path, use_4bit=False)
        else:
            print(f"\n⚠️  教师模型路径不存在: {teacher_path}")
            print("    将使用硬标签训练（标准微调）")

    # 加载数据
    print("\n加载数据集...")
    data_files = {}
    if Path(config['data']['train_file']).exists():
        data_files['train'] = config['data']['train_file']
    if Path(config['data']['eval_file']).exists():
        data_files['eval'] = config['data']['eval_file']

    if not data_files:
        raise ValueError("未找到训练数据，请检查配置文件中的路径")

    dataset = load_dataset('json', data_files=data_files)

    # 数据预处理
    max_length = config['training'].get('max_seq_length', 8192)

    def preprocess_function(examples):
        if 'input' in examples and 'output' in examples:
            texts = [f"{inp}\n{out}" for inp, out in zip(examples['input'], examples['output'])]
        elif 'text' in examples:
            texts = examples['text']
        elif 'instruction' in examples and 'response' in examples:
            texts = [f"{instr}\n{resp}" for instr, resp in zip(examples['instruction'], examples['response'])]
        else:
            raise ValueError("无法识别的数据格式，请确保有 input/output 或 text 字段")

        return tokenizer(texts, truncation=True, max_length=max_length, padding='max_length')

    print("预处理数据...")
    tokenized_dataset = dataset.map(preprocess_function, batched=True, remove_columns=dataset['train'].column_names)

    # 计算总步数
    num_epochs = config['training']['num_epochs']
    batch_size = config['training']['batch_size']
    grad_accum = config['training'].get('gradient_accumulation_steps', 1)
    train_size = len(tokenized_dataset['train'])
    steps_per_epoch = (train_size // (batch_size * grad_accum)) + 1
    total_steps = steps_per_epoch * num_epochs

    print(f"\n训练计划:")
    print(f"  样本数: {train_size}")
    print(f"  Epochs: {num_epochs}")
    print(f"  Batch size: {batch_size}")
    print(f"  总步数: ~{total_steps}")

    # 创建自适应调度器
    print("\n" + "="*50)
    print("🎛️  蒸馏策略配置")
    print("="*50)
    scheduler = create_scheduler(config, total_steps)

    # 训练参数
    training_args = TrainingArguments(
        output_dir=output_dir,
        num_train_epochs=num_epochs,
        per_device_train_batch_size=batch_size,
        gradient_accumulation_steps=grad_accum,
        learning_rate=config['training']['learning_rate'],
        warmup_ratio=config['training'].get('warmup_ratio', 0.1),
        logging_steps=config['training']['logging_steps'],
        save_steps=config['training']['save_steps'],
        evaluation_strategy="steps" if 'eval' in tokenized_dataset else "no",
        eval_steps=config['evaluation'].get('eval_steps', 500) if 'eval' in tokenized_dataset else None,
        save_total_limit=3,
        load_best_model_at_end=True if 'eval' in tokenized_dataset else False,
        fp16=True,
        report_to="tensorboard",
        logging_dir=os.path.join(Path(output_dir).parent, "logs"),
    )

    # 准备回调
    callbacks = []
    if scheduler is not None:
        callbacks.append(DistillationTrainingCallback(scheduler, log_every=50))

    # 初始化Trainer
    trainer = DistillationTrainer(
        model=student_model,
        args=training_args,
        train_dataset=tokenized_dataset['train'],
        eval_dataset=tokenized_dataset.get('eval'),
        tokenizer=tokenizer,
        teacher_model=teacher_model,
        scheduler=scheduler,
        temperature=config['distillation'].get('temperature', 2.0),
        alpha=config['distillation'].get('alpha', 0.7),
        data_collator=DataCollatorForLanguageModeling(tokenizer, mlm=False),
        callbacks=callbacks
    )

    # 开始训练
    print("\n" + "="*50)
    print("🚀 开始训练")
    print("="*50)
    print()

    trainer.train()

    # 保存最终模型
    final_model_dir = os.path.join(Path(output_dir).parent, "final_model")
    trainer.save_model(final_model_dir)
    tokenizer.save_pretrained(final_model_dir)

    print(f"\n✅ 训练完成！模型保存至 {final_model_dir}")

    # 如果使用LoRA，保存合并后的模型
    if config['training']['method'] in ['lora', 'qlora']:
        print("\n提示：使用LoRA训练，推理时需要加载基础模型+LoRA权重")
        print("或使用 `merge_lora.py` 脚本合并权重")

    # 输出最终的蒸馏参数
    if scheduler is not None:
        final_temp, final_alpha = scheduler.get_current_params()
        print(f"\n最终蒸馏参数: temperature={final_temp:.3f}, alpha={final_alpha:.3f}")


if __name__ == "__main__":
    main()
