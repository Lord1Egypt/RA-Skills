# -*- coding: utf-8 -*-
"""
MiniGPT —— 从零实现的 Decoder-only Transformer 语言模型。

架构与工程决策主要借鉴以下开源工作:
  * GPT-2 (Radford et al., 2019): 预归一化残差块、可学习绝对位置编码、
    GELU 前馈层、输入输出权重绑定
  * GPT-3 (Brown et al., 2020): AdamW + warmup + 余弦退火的学习率策略
  * minGPT / nanoGPT (Andrej Karpathy): 代码组织方式、参数初始化与优化器分组

仅依赖 PyTorch,可在 CPU / CUDA 上训练与推理。
"""

from __future__ import annotations

import inspect
import math
from dataclasses import asdict, dataclass

import torch
import torch.nn as nn
import torch.nn.functional as F


@dataclass
class GPTConfig:
    """模型结构超参数。"""

    vocab_size: int = 50257        # 词表大小(字符级分词时 = 语料字符数)
    block_size: int = 128          # 上下文长度(一次能看的最大 token 数)
    n_layer: int = 4               # Transformer 残差块层数
    n_head: int = 4                # 注意力头数(需整除 n_embd)
    n_embd: int = 128              # 隐藏维度
    dropout: float = 0.1           # dropout 比例
    bias: bool = False             # Linear/LayerNorm 是否带偏置(GPT-2 为 True;
                                   # 关闭可略减参数量,Palm/nanoGPT 均提供此开关)
    tie_weights: bool = True       # 输入词嵌入与输出投影层共享权重(GPT-2 做法)

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: dict) -> "GPTConfig":
        allowed = set(cls.__dataclass_fields__.keys())
        return cls(**{k: v for k, v in d.items() if k in allowed})


class CausalSelfAttention(nn.Module):
    """多头因果自注意力:每个 token 只能关注自己和之前的 token。

    直接调用 PyTorch 2.x 的 scaled_dot_product_attention(内部自动选择
    FlashAttention/内存高效实现),因果遮罩由 is_causal=True 提供,
    等价于 nanoGPT 中手工构造下三角 mask 的写法。
    """

    def __init__(self, config: GPTConfig):
        super().__init__()
        assert config.n_embd % config.n_head == 0, "n_embd 必须能被 n_head 整除"
        self.n_head = config.n_head
        self.n_embd = config.n_embd
        # 一次性算出 q/k/v(合并投影,与 GPT-2 的 c_attn 相同)
        self.qkv = nn.Linear(config.n_embd, 3 * config.n_embd, bias=config.bias)
        self.c_proj = nn.Linear(config.n_embd, config.n_embd, bias=config.bias)
        self.attn_dropout = config.dropout
        self.resid_drop = nn.Dropout(config.dropout)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        B, T, C = x.shape
        q, k, v = self.qkv(x).split(self.n_embd, dim=2)
        # (B, T, C) -> (B, n_head, T, head_dim)
        q = q.view(B, T, self.n_head, C // self.n_head).transpose(1, 2)
        k = k.view(B, T, self.n_head, C // self.n_head).transpose(1, 2)
        v = v.view(B, T, self.n_head, C // self.n_head).transpose(1, 2)

        y = F.scaled_dot_product_attention(
            q, k, v,
            dropout_p=self.attn_dropout if self.training else 0.0,
            is_causal=True,
        )
        # (B, n_head, T, head_dim) -> (B, T, C)
        y = y.transpose(1, 2).contiguous().view(B, T, C)
        return self.resid_drop(self.c_proj(y))


class MLP(nn.Module):
    """前馈层:Linear -> GELU -> Linear(4 倍扩展,与 GPT-2 一致)。"""

    def __init__(self, config: GPTConfig):
        super().__init__()
        self.c_fc = nn.Linear(config.n_embd, 4 * config.n_embd, bias=config.bias)
        self.c_proj = nn.Linear(4 * config.n_embd, config.n_embd, bias=config.bias)
        self.drop = nn.Dropout(config.dropout)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        # GPT-2 使用 GELU 的 tanh 近似
        return self.drop(self.c_proj(F.gelu(self.c_fc(x), approximate="tanh")))


class Block(nn.Module):
    """预归一化残差块:x = x + Attn(LN(x)); x = x + MLP(LN(x))(GPT-2 结构)。"""

    def __init__(self, config: GPTConfig):
        super().__init__()
        self.ln_1 = nn.LayerNorm(config.n_embd, bias=config.bias)
        self.attn = CausalSelfAttention(config)
        self.ln_2 = nn.LayerNorm(config.n_embd, bias=config.bias)
        self.mlp = MLP(config)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x = x + self.attn(self.ln_1(x))
        x = x + self.mlp(self.ln_2(x))
        return x


class GPT(nn.Module):
    """Decoder-only GPT:词嵌入 + 位置嵌入 -> N 个残差块 -> LN -> 输出投影。"""

    def __init__(self, config: GPTConfig):
        super().__init__()
        assert config.vocab_size > 0 and config.block_size >= 1
        self.config = config

        self.transformer = nn.ModuleDict(
            dict(
                wte=nn.Embedding(config.vocab_size, config.n_embd),   # 词嵌入
                wpe=nn.Embedding(config.block_size, config.n_embd),   # 位置嵌入
                drop=nn.Dropout(config.dropout),
                h=nn.ModuleList([Block(config) for _ in range(config.n_layer)]),
                ln_f=nn.LayerNorm(config.n_embd, bias=config.bias),
            )
        )
        self.lm_head = nn.Linear(config.n_embd, config.vocab_size, bias=False)
        if config.tie_weights:
            self.lm_head.weight = self.transformer.wte.weight

        self.apply(self._init_weights)
        # 残差路径上的投影用 1/sqrt(2*n_layer) 缩放(nanoGPT/GPT-2 初始化技巧),
        # 让残差分支在初始时刻的方差保持在合理范围,训练更稳定
        for name, p in self.named_parameters():
            if name.endswith("c_proj.weight"):
                nn.init.normal_(p, mean=0.0, std=0.02 / math.sqrt(2 * config.n_layer))

    @staticmethod
    def _init_weights(module: nn.Module) -> None:
        if isinstance(module, nn.Linear):
            nn.init.normal_(module.weight, mean=0.0, std=0.02)
            if module.bias is not None:
                nn.init.zeros_(module.bias)
        elif isinstance(module, nn.Embedding):
            nn.init.normal_(module.weight, mean=0.0, std=0.02)

    def num_params(self, non_embedding: bool = True) -> int:
        n = sum(p.numel() for p in self.parameters())
        if non_embedding:
            n -= self.transformer.wpe.weight.numel()
            if not self.config.tie_weights:
                n -= self.transformer.wte.weight.numel()
        return n

    def forward(self, idx: torch.Tensor, targets: torch.Tensor | None = None):
        B, T = idx.shape
        if T > self.config.block_size:
            raise ValueError(f"输入长度 {T} 超过 block_size={self.config.block_size}")

        pos = torch.arange(T, device=idx.device)
        x = self.transformer.wte(idx) + self.transformer.wpe(pos)
        x = self.transformer.drop(x)
        for block in self.transformer.h:
            x = block(x)
        x = self.transformer.ln_f(x)

        if targets is not None:
            # 训练:对每个位置都预测下一个 token
            logits = self.lm_head(x)
            loss = F.cross_entropy(
                logits.reshape(-1, logits.size(-1)), targets.reshape(-1)
            )
        else:
            # 推理:只取最后一个位置,省去不需要的计算
            logits = self.lm_head(x[:, [-1], :])
            loss = None
        return logits, loss

    def configure_optimizers(
        self,
        weight_decay: float = 0.1,
        lr: float = 3e-4,
        betas: tuple[float, float] = (0.9, 0.95),
        eps: float = 1e-8,
        device_type: str = "cpu",
    ) -> torch.optim.AdamW:
        """AdamW,按 nanoGPT 的方式分组:>=2 维参数做权重衰减,其余不衰减。"""
        params = [p for p in self.parameters() if p.requires_grad]
        decay = [p for p in params if p.dim() >= 2]
        no_decay = [p for p in params if p.dim() < 2]
        groups = [
            {"params": decay, "weight_decay": weight_decay},
            {"params": no_decay, "weight_decay": 0.0},
        ]
        use_fused = device_type == "cuda" and "fused" in inspect.signature(
            torch.optim.AdamW
        ).parameters
        extra = {"fused": True} if use_fused else {}
        return torch.optim.AdamW(groups, lr=lr, betas=betas, eps=eps, **extra)

    @torch.no_grad()
    def generate(
        self,
        idx: torch.Tensor,
        max_new_tokens: int,
        temperature: float = 1.0,
        top_k: int | None = None,
    ) -> torch.Tensor:
        """自回归采样:从 idx 开始逐个生成 max_new_tokens 个 token。"""
        self.eval()
        for _ in range(max_new_tokens):
            idx_cond = (
                idx
                if idx.size(1) <= self.config.block_size
                else idx[:, -self.config.block_size:]
            )
            logits, _ = self(idx_cond)
            logits = logits[:, -1, :] / max(temperature, 1e-8)
            if top_k is not None and top_k > 0:
                v, _ = torch.topk(logits, min(top_k, logits.size(-1)))
                logits[logits < v[:, [-1]]] = float("-inf")
            probs = F.softmax(logits, dim=-1)
            idx_next = torch.multinomial(probs, num_samples=1)
            idx = torch.cat((idx, idx_next), dim=1)
        return idx
