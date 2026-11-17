# -*- coding: utf-8 -*-
"""模型单元测试:python minigpt/test_model.py"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import torch

from model import GPT, GPTConfig


def main() -> None:
    torch.manual_seed(0)

    # 1. 前向 / 反向 / 生成形状检查
    cfg = GPTConfig(vocab_size=50, block_size=16, n_layer=2, n_head=2,
                    n_embd=32, dropout=0.0)
    model = GPT(cfg)
    x = torch.randint(0, 50, (2, 16))
    y = torch.randint(0, 50, (2, 16))
    logits, loss = model(x, y)
    assert logits.shape == (2, 16, 50), f"logits 形状错误: {logits.shape}"
    assert torch.isfinite(loss), "损失不是有限值"
    loss.backward()
    no_grad = [n for n, p in model.named_parameters()
               if p.requires_grad and p.grad is None]
    assert not no_grad, f"有参数没有梯度: {no_grad}"
    out = model.generate(x[:, :4], max_new_tokens=6, temperature=1.0, top_k=10)
    assert out.shape == (2, 10), f"生成形状错误: {out.shape}"

    # 2. 学习能力冒烟测试:重复序列应能在一个小模型上被快速记住
    torch.manual_seed(1)
    pattern = torch.tensor([list(range(10))])
    data = pattern.repeat(64, 1).reshape(-1)          # 640 个 token 的 0..9 循环
    m = GPT(GPTConfig(vocab_size=10, block_size=8, n_layer=2, n_head=2,
                      n_embd=32, dropout=0.0))
    opt = m.configure_optimizers(lr=1e-2, weight_decay=0.0)
    first = None
    for step in range(120):
        ix = torch.randint(0, len(data) - 9, (8,))
        xb = torch.stack([data[i: i + 8] for i in ix])
        yb = torch.stack([data[i + 1: i + 9] for i in ix])
        _, loss = m(xb, yb)
        if first is None:
            first = loss.item()
        opt.zero_grad(set_to_none=True)
        loss.backward()
        opt.step()
    final = loss.item()
    assert final < first * 0.5, f"损失未明显下降: {first:.3f} -> {final:.3f}"

    print(f"test_model: 全部通过(损失 {first:.3f} -> {final:.3f},"
          f"参数量 {m.num_params():,})")


if __name__ == "__main__":
    main()
