# -*- coding: utf-8 -*-
"""训练 MiniViT 手写数字识别(MNIST 优先;离线自动改用合成数字)。

用法:
  python vision/train_vit.py                     # 默认 2 epochs,CPU 几分钟
  python vision/train_vit.py --device cuda       # CUDA 版 PyTorch 装好后可用
"""

from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path

import torch
import torch.nn.functional as F

_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE))
REPO_ROOT = _HERE.parent

from data import load_dataset
from vit import ViTConfig, VisionTransformer


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="MiniViT 训练")
    p.add_argument("--epochs", type=int, default=2)
    p.add_argument("--batch-size", type=int, default=128)
    p.add_argument("--lr", type=float, default=1e-3)
    p.add_argument("--weight-decay", type=float, default=0.05)
    p.add_argument("--dataset", default="auto", choices=["auto", "mnist", "synthetic"])
    p.add_argument("--max-train", type=int, default=20000, help="限制训练张数以控制 CPU 时长,0 = 全量")
    p.add_argument("--out", default=str(REPO_ROOT / "checkpoints" / "vit"))
    p.add_argument("--device", default="auto")
    p.add_argument("--seed", type=int, default=42)
    return p.parse_args()


def main() -> None:
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    args = parse_args()
    torch.manual_seed(args.seed)
    device = ("cuda" if torch.cuda.is_available() else "cpu") if args.device == "auto" else args.device

    name, trx, tryy, tex, tey = load_dataset(args.dataset)
    if args.max_train and len(trx) > args.max_train:
        trx, tryy = trx[: args.max_train], tryy[: args.max_train]
    print(f"数据集: {name} | 训练 {len(trx):,} 张 | 测试 {len(tex):,} 张 | 设备 {device}")

    tf = trx.float() / 255
    mean, std = tf.mean().item(), max(tf.std().item(), 1e-6)
    train_x = ((trx.float() / 255 - mean) / std).unsqueeze(1)   # N,1,28,28
    test_x = ((tex.float() / 255 - mean) / std).unsqueeze(1)
    train_y, test_y = tryy.long(), tey.long()
    del tf

    cfg = ViTConfig()
    model = VisionTransformer(cfg).to(device)
    print(f"模型参数量: {sum(p.numel() for p in model.parameters()):,}")

    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)
    opt = torch.optim.AdamW(model.parameters(), lr=args.lr, weight_decay=args.weight_decay)
    steps = (len(train_x) + args.batch_size - 1) // args.batch_size
    sched = torch.optim.lr_scheduler.CosineAnnealingLR(opt, T_max=args.epochs * steps)

    best = 0.0
    for ep in range(1, args.epochs + 1):
        model.train()
        perm = torch.randperm(len(train_x))
        t0, lsum, tot, correct = time.time(), 0.0, 0, 0
        for i in range(0, len(train_x), args.batch_size):
            idx = perm[i: i + args.batch_size]
            x, y = train_x[idx].to(device), train_y[idx].to(device)
            logits = model(x)
            loss = F.cross_entropy(logits, y)
            opt.zero_grad(set_to_none=True)
            loss.backward()
            opt.step()
            sched.step()
            bs = len(idx)
            lsum += loss.item() * bs
            tot += bs
            correct += (logits.argmax(1) == y).sum().item()
        model.eval()
        tcorrect = 0
        with torch.no_grad():
            for i in range(0, len(test_x), 512):
                xb = test_x[i: i + 512].to(device)
                yb = test_y[i: i + 512].to(device)
                tcorrect += (model(xb).argmax(1) == yb).sum().item()
        acc = tcorrect / len(test_x)
        print(f"epoch {ep}/{args.epochs} | loss {lsum / tot:.4f} | "
              f"train acc {correct / tot:.2%} | 测试准确率 {acc:.2%} | {time.time() - t0:.0f}s", flush=True)
        if acc >= best:
            best = acc
            torch.save({"config": cfg.to_dict(), "model": model.state_dict(),
                        "mean": mean, "std": std, "dataset": name,
                        "epoch": ep, "test_acc": acc}, str(out_dir / "ckpt.pt"))
    print(f"BEST_ACC {best:.4f}", flush=True)
    print("VIT_TRAIN_DONE", flush=True)


if __name__ == "__main__":
    main()
