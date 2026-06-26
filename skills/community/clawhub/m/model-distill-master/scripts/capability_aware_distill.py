#!/usr/bin/env python3
"""能力感知蒸馏 - 针对不同能力类型应用不同策略"""

import torch
import torch.nn as nn
import torch.nn.functional as F
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple
from enum import Enum
import json


class CapabilityType(Enum):
    REASONING = "reasoning"      # 推理能力
    STYLE = "style"              # 风格/语气
    KNOWLEDGE = "knowledge"      # 知识/事实
    CREATIVE = "creative"        # 创造性生成
    INSTRUCTION = "instruction"  # 指令遵循


@dataclass
class CapabilityConfig:
    """能力特定配置"""
    temperature: float
    alpha: float
    loss_weights: Dict[str, float]
    focus_layers: List[str]
    special_tokens: Optional[List[str]] = None


class CapabilityAwareDistiller:
    """能力感知蒸馏器"""

    # 预定义每种能力的最优配置
    CAPABILITY_PRESETS = {
        CapabilityType.REASONING: CapabilityConfig(
            temperature=2.5,  # 高温软化分布，保留推理路径
            alpha=0.8,        # 侧重软标签
            loss_weights={"soft": 0.8, "hard": 0.15, "attention": 0.05},
            focus_layers=["layer.-2", "layer.-1"],  # 关注深层
            special_tokens=["<think>", "<step>", "<reason>"]
        ),
        CapabilityType.STYLE: CapabilityConfig(
            temperature=1.5,  # 中温保留风格特征
            alpha=0.7,
            loss_weights={"soft": 0.7, "hard": 0.2, "embedding": 0.1},
            focus_layers=["embed", "layer.-1"],
            special_tokens=None
        ),
        CapabilityType.KNOWLEDGE: CapabilityConfig(
            temperature=0.8,  # 低温强调事实准确性
            alpha=0.4,        # 侧重硬标签
            loss_weights={"soft": 0.4, "hard": 0.55, "factual": 0.05},
            focus_layers=["all"],
            special_tokens=None
        ),
        CapabilityType.CREATIVE: CapabilityConfig(
            temperature=2.0,
            alpha=0.75,
            loss_weights={"soft": 0.75, "hard": 0.15, "diversity": 0.1},
            focus_layers=["layer.-3", "layer.-2", "layer.-1"],
            special_tokens=None
        ),
        CapabilityType.INSTRUCTION: CapabilityConfig(
            temperature=1.2,
            alpha=0.6,
            loss_weights={"soft": 0.6, "hard": 0.35, "format": 0.05},
            focus_layers=["layer.-2", "layer.-1"],
            special_tokens=["<instruction>", "<response>"]
        )
    }

    def __init__(self, capability_type: CapabilityType,
                 teacher_model=None, student_model=None,
                 device='cuda'):
        self.capability = capability_type
        self.config = self.CAPABILITY_PRESETS[capability_type]
        self.teacher = teacher_model
        self.student = student_model
        self.device = device

    def compute_loss(self, student_logits, teacher_logits,
                     labels, attention_mask=None,
                     student_hidden=None, teacher_hidden=None) -> Dict[str, torch.Tensor]:
        """计算能力感知的复合损失"""

        T = self.config.temperature
        alpha = self.config.alpha
        weights = self.config.loss_weights

        losses = {}

        # 软标签损失 (KL散度)
        if "soft" in weights:
            soft_loss = self._kl_divergence_loss(
                student_logits, teacher_logits, T
            )
            losses["soft"] = soft_loss * weights["soft"]

        # 硬标签损失 (交叉熵)
        if "hard" in weights:
            hard_loss = F.cross_entropy(
                student_logits.view(-1, student_logits.size(-1)),
                labels.view(-1),
                ignore_index=-100
            )
            losses["hard"] = hard_loss * weights["hard"]

        # 注意力对齐损失 (推理能力特有)
        if "attention" in weights and attention_mask is not None:
            att_loss = self._attention_alignment_loss(
                student_logits, teacher_logits, attention_mask
            )
            losses["attention"] = att_loss * weights["attention"]

        # 隐藏层对齐 (风格迁移)
        if "embedding" in weights and student_hidden is not None:
            emb_loss = self._embedding_alignment_loss(student_hidden, teacher_hidden)
            losses["embedding"] = emb_loss * weights["embedding"]

        # 总损失
        losses["total"] = sum(losses.values())

        return losses

    def _kl_divergence_loss(self, student_logits, teacher_logits, temperature):
        """温度缩放的KL散度"""
        student_probs = F.log_softmax(student_logits / temperature, dim=-1)
        teacher_probs = F.softmax(teacher_logits / temperature, dim=-1)
        kl = F.kl_div(student_probs, teacher_probs, reduction='batchmean')
        return kl * (temperature ** 2)

    def _attention_alignment_loss(self, student_logits, teacher_logits, attention_mask):
        """注意力分布对齐 (简化版)"""
        # 使用logits的熵作为注意力分布的代理
        student_probs = F.softmax(student_logits, dim=-1)
        teacher_probs = F.softmax(teacher_logits, dim=-1)

        # 计算分布差异
        mse = F.mse_loss(student_probs, teacher_probs)
        return mse

    def _embedding_alignment_loss(self, student_hidden, teacher_hidden):
        """隐藏层嵌入对齐"""
        # 投影到相同维度
        if student_hidden.shape[-1] != teacher_hidden.shape[-1]:
            # 使用平均池化匹配维度
            student_hidden = F.normalize(student_hidden.mean(dim=1), dim=-1)
            teacher_hidden = F.normalize(teacher_hidden.mean(dim=1), dim=-1)
        else:
            student_hidden = F.normalize(student_hidden, dim=-1)
            teacher_hidden = F.normalize(teacher_hidden, dim=-1)

        cosine_loss = 1 - F.cosine_similarity(student_hidden, teacher_hidden, dim=-1).mean()
        return cosine_loss

    def get_special_token_mask(self, input_ids, tokenizer) -> torch.Tensor:
        """获取特殊token的mask，用于加权损失"""
        if not self.config.special_tokens:
            return torch.ones_like(input_ids, dtype=torch.float)

        mask = torch.zeros_like(input_ids, dtype=torch.float)
        for token in self.config.special_tokens:
            if hasattr(tokenizer, 'convert_tokens_to_ids'):
                token_id = tokenizer.convert_tokens_to_ids(token)
                mask[input_ids == token_id] = 2.0  # 加权

        # 确保至少有一些权重
        mask[mask == 0] = 1.0
        return mask


class MultiCapabilityDistiller:
    """多能力联合蒸馏"""

    def __init__(self, capabilities: List[CapabilityType], device='cuda'):
        self.capabilities = capabilities
        self.distillers = {
            cap: CapabilityAwareDistiller(cap, device=device)
            for cap in capabilities
        }
        # 能力权重可配置
        self.capability_weights = {cap: 1.0 / len(capabilities) for cap in capabilities}

    def compute_combined_loss(self, batch_data: Dict[str, torch.Tensor],
                              capability_labels: List[CapabilityType]) -> torch.Tensor:
        """计算多能力联合损失"""

        total_loss = 0
        for cap_type in set(capability_labels):
            # 筛选属于该能力的样本
            cap_mask = torch.tensor([l == cap_type for l in capability_labels])
            if not cap_mask.any():
                continue

            # 提取该能力的数据
            cap_data = {k: v[cap_mask] for k, v in batch_data.items()}

            # 使用该能力的蒸馏器计算损失
            distiller = self.distillers[cap_type]
            losses = distiller.compute_loss(
                cap_data['student_logits'],
                cap_data['teacher_logits'],
                cap_data['labels']
            )

            weighted_loss = losses["total"] * self.capability_weights[cap_type]
            total_loss += weighted_loss

        return total_loss


def detect_capability_type(text: str, task_hint: Optional[str] = None) -> CapabilityType:
    """自动检测文本的能力类型"""

    # 关键词映射
    reasoning_keywords = ['推理', '证明', '推导', '因为', '所以', '如果', '那么',
                          'reason', 'prove', 'therefore', 'if', 'then', 'step']
    knowledge_keywords = ['是什么', '定义', '概念', '事实', '知识', 'who', 'what is',
                          'define', 'fact', 'knowledge']
    creative_keywords = ['创作', '生成', '写', '创意', 'write', 'create', 'generate',
                         'story', 'poem', 'creative']
    instruction_keywords = ['指令', '命令', '执行', 'instruction', 'command', 'do']

    text_lower = text.lower()

    # 计数
    scores = {
        CapabilityType.REASONING: sum(1 for k in reasoning_keywords if k in text_lower),
        CapabilityType.KNOWLEDGE: sum(1 for k in knowledge_keywords if k in text_lower),
        CapabilityType.CREATIVE: sum(1 for k in creative_keywords if k in text_lower),
        CapabilityType.INSTRUCTION: sum(1 for k in instruction_keywords if k in text_lower),
    }

    # 任务提示优先
    if task_hint:
        hint_map = {
            'math': CapabilityType.REASONING,
            'code': CapabilityType.REASONING,
            'writing': CapabilityType.CREATIVE,
            'qa': CapabilityType.KNOWLEDGE,
            'chat': CapabilityType.STYLE,
            'instruct': CapabilityType.INSTRUCTION,
        }
        if task_hint.lower() in hint_map:
            return hint_map[task_hint.lower()]

    # 选择最高分
    if max(scores.values()) > 0:
        return max(scores, key=scores.get)

    # 默认
    return CapabilityType.REASONING


def create_capability_dataset(input_file: str, output_file: str):
    """为数据集标注能力类型"""

    with open(input_file, 'r') as f:
        data = [json.loads(line) for line in f]

    labeled_data = []
    for item in data:
        text = item.get('input', '') + ' ' + item.get('instruction', '')
        task = item.get('task_type', '')

        cap_type = detect_capability_type(text, task)
        item['capability_type'] = cap_type.value

        labeled_data.append(item)

    # 统计
    from collections import Counter
    stats = Counter([d['capability_type'] for d in labeled_data])
    print("能力类型分布:")
    for cap, count in stats.items():
        print(f"  {cap}: {count}")

    # 保存
    with open(output_file, 'w') as f:
        for item in labeled_data:
            f.write(json.dumps(item, ensure_ascii=False) + '\n')

    print(f"已保存到: {output_file}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--input", help="输入数据文件")
    parser.add_argument("--output", help="输出文件")
    parser.add_argument("--capability", choices=[c.value for c in CapabilityType],
                        help="指定能力类型进行测试")
    args = parser.parse_args()

    if args.input and args.output:
        create_capability_dataset(args.input, args.output)
    elif args.capability:
        # 测试配置
        cap = CapabilityType(args.capability)
        distiller = CapabilityAwareDistiller(cap)
        print(f"能力类型: {cap.value}")
        print(f"温度: {distiller.config.temperature}")
        print(f"Alpha: {distiller.config.alpha}")
        print(f"损失权重: {distiller.config.loss_weights}")
        print(f"关注层: {distiller.config.focus_layers}")
