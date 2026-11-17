# -*- coding: utf-8 -*-
"""加载训练好的检查点,本地生成 / 续写文本。

用法示例:
  python minigpt/generate.py --prompt "子曰:" --max-new-tokens 200
  python minigpt/generate.py --ckpt-dir checkpoints/mine --temperature 0.7
  python minigpt/generate.py            # 不带 --prompt 时进入交互续写模式
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import torch

from model import GPT, GPTConfig
from tokenizer import CharTokenizer

REPO_ROOT = Path(__file__).resolve().parents[1]


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="MiniGPT 生成脚本")
    p.add_argument("--ckpt-dir", default=str(REPO_ROOT / "checkpoints" / "demo"))
    p.add_argument("--prompt", default="", help="续写的开头;留空进入交互模式")
    p.add_argument("--max-new-tokens", type=int, default=200)
    p.add_argument("--temperature", type=float, default=0.8)
    p.add_argument("--top-k", type=int, default=40)
    p.add_argument("--device", default="auto", choices=["auto", "cpu", "cuda"])
    return p.parse_args()


def load_model(ckpt_dir: str, device: str):
    ckpt_dir = Path(ckpt_dir)
    cfg_path = ckpt_dir / "config.json"
    ckpt_path = ckpt_dir / "ckpt.pt"
    if not cfg_path.exists() or not ckpt_path.exists():
        sys.exit(f"[错误] {ckpt_dir} 下缺少 config.json / ckpt.pt,请先运行训练脚本")

    config = GPTConfig.from_dict(json.loads(cfg_path.read_text(encoding="utf-8")))
    tok = CharTokenizer.load(str(ckpt_dir / "tokenizer.json"))
    model = GPT(config).to(device)
    state = torch.load(str(ckpt_path), map_location=device, weights_only=True)
    model.load_state_dict(state["model"])
    model.eval()
    return model, tok, state.get("iter"), state.get("val_loss")


@torch.no_grad()
def stream_generate(model: GPT, tok: CharTokenizer, device: str, prompt: str,
                    max_new_tokens: int, temperature: float, top_k: int) -> None:
    """逐 token 生成并实时打印(本地模型的小乐趣)。"""
    ids = tok.encode(prompt)
    if not ids:
        ids = tok.encode("\n") or [0]
    idx = torch.tensor([ids[-model.config.block_size:]], dtype=torch.long, device=device)
    print(tok.decode(idx[0].tolist()), end="", flush=True)
    for _ in range(max_new_tokens):
        idx_cond = (
            idx if idx.size(1) <= model.config.block_size
            else idx[:, -model.config.block_size:]
        )
        logits, _ = model(idx_cond)
        logits = logits[:, -1, :] / max(temperature, 1e-8)
        if top_k and top_k > 0:
            v, _ = torch.topk(logits, min(top_k, logits.size(-1)))
            logits[logits < v[:, [-1]]] = float("-inf")
        probs = torch.softmax(logits, dim=-1)
        next_id = torch.multinomial(probs, num_samples=1)
        idx = torch.cat([idx, next_id], dim=1)
        print(tok.itos[int(next_id)], end="", flush=True)
    print()


def main() -> None:
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

    args = parse_args()
    device = "cuda" if (args.device == "auto" and torch.cuda.is_available()) else (
        args.device if args.device != "auto" else "cpu"
    )
    model, tok, it, val_loss = load_model(args.ckpt_dir, device)
    info = f"已加载检查点: {args.ckpt_dir}(训练 {it} 步"
    if val_loss is not None:
        info += f",最优验证损失 {val_loss:.4f}"
    print(info + ")")

    if args.prompt:
        stream_generate(model, tok, device, args.prompt,
                        args.max_new_tokens, args.temperature, args.top_k)
        return

    print("进入交互续写模式:输入提示词后回车生成,输入空行或 Ctrl+C 退出。")
    while True:
        try:
            line = input("\n提示词> ")
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if not line.strip():
            break
        stream_generate(model, tok, device, line,
                        args.max_new_tokens, args.temperature, args.top_k)


if __name__ == "__main__":
    main()
