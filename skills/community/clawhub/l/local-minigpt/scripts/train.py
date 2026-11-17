# -*- coding: utf-8 -*-
"""训练脚本:在本地语料上训练 MiniGPT。

用法示例:
  python minigpt/train.py                          # 默认小配置,CPU 几分钟
  python minigpt/train.py --max-iters 3000 --n-embd 192
  python minigpt/train.py --data data/my.txt --out-dir checkpoints/mine
"""

from __future__ import annotations

import argparse
import json
import math
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import torch

from model import GPT, GPTConfig
from tokenizer import CharTokenizer

REPO_ROOT = Path(__file__).resolve().parents[1]


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="MiniGPT 训练脚本")
    p.add_argument("--data", default=str(REPO_ROOT / "data" / "train.txt"))
    p.add_argument("--out-dir", default=str(REPO_ROOT / "checkpoints" / "demo"))
    p.add_argument("--n-layer", type=int, default=4)
    p.add_argument("--n-head", type=int, default=4)
    p.add_argument("--n-embd", type=int, default=128)
    p.add_argument("--block-size", type=int, default=128)
    p.add_argument("--dropout", type=float, default=0.1)
    p.add_argument("--batch-size", type=int, default=16)
    p.add_argument("--max-iters", type=int, default=1500)
    p.add_argument("--lr", type=float, default=3e-4)
    p.add_argument("--min-lr-ratio", type=float, default=0.1)
    p.add_argument("--warmup-iters", type=int, default=100)
    p.add_argument("--weight-decay", type=float, default=0.1)
    p.add_argument("--grad-clip", type=float, default=1.0)
    p.add_argument("--val-ratio", type=float, default=0.05)
    p.add_argument("--eval-interval", type=int, default=150)
    p.add_argument("--eval-iters", type=int, default=20)
    p.add_argument("--device", default="auto", choices=["auto", "cpu", "cuda"])
    p.add_argument("--seed", type=int, default=1337)
    p.add_argument("--sample-tokens", type=int, default=160,
                   help="训练结束后自动生成的示例 token 数,0 表示不生成")
    return p.parse_args()


def pick_device(spec: str) -> str:
    if spec != "auto":
        return spec
    return "cuda" if torch.cuda.is_available() else "cpu"


def get_lr(it: int, warmup_iters: int, lr_decay_iters: int, max_lr: float, min_lr: float) -> float:
    """带 warmup 的余弦退火学习率(借鉴 GPT-3 论文的训练策略)。"""
    if it < warmup_iters:
        return max_lr * (it + 1) / max(1, warmup_iters)
    if it > lr_decay_iters:
        return min_lr
    ratio = (it - warmup_iters) / max(1, lr_decay_iters - warmup_iters)
    coeff = 0.5 * (1.0 + math.cos(math.pi * ratio))
    return min_lr + coeff * (max_lr - min_lr)


def get_batch(data: torch.Tensor, block_size: int, batch_size: int, device: str):
    """随机取 batch:x 为长度 block_size 的片段,y 为右移一位的「下一个 token」。"""
    ix = torch.randint(len(data) - block_size - 1, (batch_size,))
    x = torch.stack([data[i: i + block_size] for i in ix])
    y = torch.stack([data[i + 1: i + block_size + 1] for i in ix])
    return x.to(device, non_blocking=True), y.to(device, non_blocking=True)


@torch.no_grad()
def estimate_loss(model, data_splits, block_size, batch_size, device, eval_iters) -> dict:
    model.eval()
    out = {}
    for name, d in data_splits.items():
        losses = torch.zeros(eval_iters)
        for k in range(eval_iters):
            x, y = get_batch(d, block_size, batch_size, device)
            _, loss = model(x, y)
            losses[k] = loss.item()
        out[name] = losses.mean().item()
    model.train()
    return out


def sample_text(model, tok: CharTokenizer, device: str, prompt: str,
                max_new_tokens: int, temperature: float = 0.8, top_k: int = 40) -> str:
    ids = tok.encode(prompt)
    if not ids:
        ids = tok.encode("\n") or [0]
    idx = torch.tensor([ids[-model.config.block_size:]], dtype=torch.long, device=device)
    out = model.generate(idx, max_new_tokens=max_new_tokens,
                         temperature=temperature, top_k=top_k)
    return tok.decode(out[0].tolist())


def main() -> None:
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

    args = parse_args()
    torch.manual_seed(args.seed)

    # ---- 语料 ----
    data_path = Path(args.data)
    if not data_path.exists():
        fallback = REPO_ROOT / "data" / "demo.txt"
        if fallback.exists():
            print(f"[提示] 未找到 {data_path},改用自带示例语料 {fallback}")
            data_path = fallback
        else:
            sys.exit(f"[错误] 找不到语料文件: {data_path}(可先运行 python scripts/fetch_corpus.py)")

    text = data_path.read_text(encoding="utf-8")
    if len(text) < 1000:
        sys.exit("[错误] 语料太短(不足 1000 字符),请提供更长的 txt 文件")
    print(f"语料: {data_path}({len(text):,} 字符)")

    tok = CharTokenizer.from_text(text)
    ids = torch.tensor(tok.encode(text), dtype=torch.long)
    n_val = int(len(ids) * args.val_ratio)
    n_train = len(ids) - n_val
    train_data = ids[:n_train]
    splits = {"train": train_data}
    if n_val > args.block_size + 1:
        splits["val"] = ids[n_train:]
    print(f"词表: {tok.vocab_size} 字符 | 训练片段: {n_train:,}"
          + (f" | 验证片段: {len(splits['val']):,}" if "val" in splits else " | (语料太小,暂不划验证集)"))

    # ---- 模型与优化器 ----
    device = pick_device(args.device)
    print(f"设备: {device} | torch {torch.__version__}")
    config = GPTConfig(
        vocab_size=tok.vocab_size,
        block_size=args.block_size,
        n_layer=args.n_layer,
        n_head=args.n_head,
        n_embd=args.n_embd,
        dropout=args.dropout,
    )
    model = GPT(config).to(device)
    print(f"模型参数量(不含位置嵌入): {model.num_params(non_embedding=True):,}")

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    tok.save(str(out_dir / "tokenizer.json"))
    (out_dir / "config.json").write_text(
        json.dumps(config.to_dict(), ensure_ascii=False, indent=2), encoding="utf-8"
    )

    optimizer = model.configure_optimizers(
        weight_decay=args.weight_decay, lr=args.lr, device_type=device
    )
    min_lr = args.lr * args.min_lr_ratio

    # ---- 训练循环 ----
    best_val = float("inf")
    t_start = time.time()
    tokens_seen = 0
    model.train()
    for it in range(args.max_iters):
        lr = get_lr(it, args.warmup_iters, args.max_iters, args.lr, min_lr)
        for g in optimizer.param_groups:
            g["lr"] = lr

        x, y = get_batch(train_data, args.block_size, args.batch_size, device)
        _, loss = model(x, y)
        optimizer.zero_grad(set_to_none=True)
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), args.grad_clip)
        optimizer.step()
        tokens_seen += x.numel()

        if (it + 1) % 10 == 0 or it == 0:
            speed = tokens_seen / max(1e-6, time.time() - t_start)
            print(f"iter {it + 1:5d}/{args.max_iters} | loss {loss.item():.4f} | "
                  f"lr {lr:.2e} | {speed:,.0f} tok/s", flush=True)

        if (it + 1) % args.eval_interval == 0 or (it + 1) == args.max_iters:
            losses = estimate_loss(model, splits, args.block_size,
                                   args.batch_size, device, args.eval_iters)
            msg = f"[评估] iter {it + 1}: train loss {losses['train']:.4f}"
            if "val" in losses:
                msg += f" | val loss {losses['val']:.4f}"
            print(msg, flush=True)
            if "val" in losses and losses["val"] < best_val:
                best_val = losses["val"]
                torch.save({"model": model.state_dict(), "config": config.to_dict(),
                            "iter": it + 1, "val_loss": best_val},
                           str(out_dir / "ckpt-best.pt"))

    torch.save({"model": model.state_dict(), "optimizer": optimizer.state_dict(),
                "config": config.to_dict(), "iter": args.max_iters,
                "val_loss": best_val if best_val < float("inf") else None},
               str(out_dir / "ckpt.pt"))
    print(f"已保存最终检查点: {out_dir / 'ckpt.pt'}"
          + (f"(最优验证损失 {best_val:.4f})" if best_val < float("inf") else ""))

    # ---- 自动采样,直观看到学习效果 ----
    if args.sample_tokens > 0:
        print("---- 自动采样示例(temperature=0.8, top_k=40)----")
        print(sample_text(model, tok, device, prompt="\n",
                          max_new_tokens=args.sample_tokens))
        print("--------------------------------------------")
    print("TRAIN_DONE", flush=True)


if __name__ == "__main__":
    main()
