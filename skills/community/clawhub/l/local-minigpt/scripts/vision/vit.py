# -*- coding: utf-8 -*-
"""MiniViT —— 从零实现的 Vision Transformer(借鉴 ViT: Dosovitskiy et al., 2020)。

与 MiniGPT 共用同一种「预归一化 Transformer 块」,区别只有三点:
  1. token 不是字符,而是图像切出来的 4x4 像素块(patch embedding);
  2. 注意力不需要因果遮罩(图像块之间互相都能看);
  3. 输出头不是词表分布,而是类别分布(分类任务,用 [CLS] token)。
"""

from __future__ import annotations

from dataclasses import asdict, dataclass

import torch
import torch.nn as nn
import torch.nn.functional as F


@dataclass
class ViTConfig:
    img_size: int = 28
    patch_size: int = 4
    in_chans: int = 1
    n_classes: int = 10
    n_layer: int = 4
    n_head: int = 4
    n_embd: int = 64
    mlp_ratio: int = 4
    dropout: float = 0.1

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: dict) -> "ViTConfig":
        allowed = set(cls.__dataclass_fields__.keys())
        return cls(**{k: v for k, v in d.items() if k in allowed})


class PatchEmbed(nn.Module):
    """把 B×C×H×W 的图像切成 N 个 patch 并线性映射到 D 维:一个 stride=patch 的卷积即可。"""

    def __init__(self, cfg: ViTConfig):
        super().__init__()
        self.proj = nn.Conv2d(cfg.in_chans, cfg.n_embd,
                              kernel_size=cfg.patch_size, stride=cfg.patch_size)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.proj(x).flatten(2).transpose(1, 2)   # B,N,D


class Block(nn.Module):
    """非因果的预归一化 Transformer 块(与 GPT 块唯一的本质区别:没有因果遮罩)。"""

    def __init__(self, cfg: ViTConfig):
        super().__init__()
        self.n_head = cfg.n_head
        self.ln1 = nn.LayerNorm(cfg.n_embd)
        self.qkv = nn.Linear(cfg.n_embd, 3 * cfg.n_embd)
        self.proj = nn.Linear(cfg.n_embd, cfg.n_embd)
        self.drop = nn.Dropout(cfg.dropout)
        self.ln2 = nn.LayerNorm(cfg.n_embd)
        self.fc1 = nn.Linear(cfg.n_embd, cfg.mlp_ratio * cfg.n_embd)
        self.fc2 = nn.Linear(cfg.mlp_ratio * cfg.n_embd, cfg.n_embd)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        B, N, C = x.shape
        h = self.ln1(x)
        qkv = self.qkv(h).reshape(B, N, 3, self.n_head, C // self.n_head).permute(2, 0, 3, 1, 4)
        q, k, v = qkv[0], qkv[1], qkv[2]
        y = F.scaled_dot_product_attention(q, k, v)      # 无 is_causal:双向注意力
        y = y.transpose(1, 2).reshape(B, N, C)
        x = x + self.drop(self.proj(y))
        x = x + self.drop(self.fc2(F.gelu(self.fc1(self.ln2(x)))))
        return x


class VisionTransformer(nn.Module):
    def __init__(self, cfg: ViTConfig):
        super().__init__()
        assert cfg.img_size % cfg.patch_size == 0
        self.cfg = cfg
        n_patches = (cfg.img_size // cfg.patch_size) ** 2

        self.patch_embed = PatchEmbed(cfg)
        self.cls_token = nn.Parameter(torch.zeros(1, 1, cfg.n_embd))
        self.pos_embed = nn.Parameter(torch.zeros(1, n_patches + 1, cfg.n_embd))
        nn.init.trunc_normal_(self.cls_token, std=0.02)
        nn.init.trunc_normal_(self.pos_embed, std=0.02)
        self.drop = nn.Dropout(cfg.dropout)
        self.blocks = nn.ModuleList([Block(cfg) for _ in range(cfg.n_layer)])
        self.ln_f = nn.LayerNorm(cfg.n_embd)
        self.head = nn.Linear(cfg.n_embd, cfg.n_classes)
        self.apply(self._init_weights)

    @staticmethod
    def _init_weights(m: nn.Module) -> None:
        if isinstance(m, nn.Linear):
            nn.init.normal_(m.weight, mean=0.0, std=0.02)
            if m.bias is not None:
                nn.init.zeros_(m.bias)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        B = x.size(0)
        x = self.patch_embed(x)                          # B,N,D
        cls = self.cls_token.expand(B, -1, -1)
        x = torch.cat([cls, x], dim=1)
        x = x + self.pos_embed[:, : x.size(1)]
        x = self.drop(x)
        for blk in self.blocks:
            x = blk(x)
        x = self.ln_f(x)
        return self.head(x[:, 0])                        # 用 [CLS] token 分类
