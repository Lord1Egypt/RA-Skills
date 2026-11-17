# -*- coding: utf-8 -*-
"""对训练好的 MiniGPT 做「编码能力测试」。

三个任务:
  A. 困惑度:在从未参与训练的留出代码上逐窗口求平均交叉熵
     (对照基线 = 均匀分布 ln(词表大小);困惑度 = exp(交叉熵));
  B. 语法有效率:以 "def " / "class " 起头自由生成 N 段,用 ast.parse 判定——
     同时报告「原始整段合法率」与「存在某个前缀合法率」(更公平,容忍截断);
  C. 补全:取留出代码里真实函数/类的前两行作前缀,生成续写并打印检查。

用法: python scripts/coding_test.py --ckpt-dir checkpoints/code --n-samples 50
"""

from __future__ import annotations

import argparse
import ast
import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent / "minigpt"))

import torch

from generate import load_model

REPO_ROOT = Path(__file__).resolve().parents[1]
PROBE_CHARS = "def class import for while return self None True ():.[]"


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="MiniGPT 编码能力测试")
    p.add_argument("--ckpt-dir", default=str(REPO_ROOT / "checkpoints" / "code"))
    p.add_argument("--heldout", default=str(REPO_ROOT / "data" / "code_heldout.txt"))
    p.add_argument("--n-samples", type=int, default=50)
    p.add_argument("--max-new-tokens", type=int, default=200)
    p.add_argument("--temperature", type=float, default=0.5)
    p.add_argument("--top-k", type=int, default=20)
    p.add_argument("--seed", type=int, default=42)
    return p.parse_args()


@torch.no_grad()
def heldout_loss(model, tok, text: str, device: str, block_size: int) -> float:
    ids = torch.tensor(tok.encode(text), dtype=torch.long)
    n = (len(ids) - 1) // block_size
    losses: list[float] = []
    for k in range(n):
        chunk = ids[k * block_size: (k + 1) * block_size + 1]
        x = chunk[:-1].unsqueeze(0).to(device)
        y = chunk[1:].unsqueeze(0).to(device)
        _, loss = model(x, y)
        losses.append(loss.item())
    return sum(losses) / max(1, len(losses))


@torch.no_grad()
def gen(model, tok, device: str, prompt: str, max_new_tokens: int,
        temperature: float, top_k: int) -> str:
    ids = tok.encode(prompt)
    idx = torch.tensor([ids], dtype=torch.long, device=device)
    out = model.generate(idx, max_new_tokens=max_new_tokens,
                         temperature=temperature, top_k=top_k)
    return tok.decode(out[0].tolist())


def has_parsable_prefix(text: str, max_tries: int = 12) -> bool:
    """整段或去掉末尾若干行后的前缀能否通过 ast.parse(容忍生成被截断)。"""
    lines = text.split("\n")
    cuts = [len(text)] + [len("\n".join(lines[:-k])) for k in range(1, max_tries)]
    for cut in cuts:
        try:
            ast.parse(text[:cut])
            return True
        except (SyntaxError, ValueError):
            continue
    return False


def main() -> None:
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    args = parse_args()
    torch.manual_seed(args.seed)
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model, tok, it, vl = load_model(args.ckpt_dir, device)
    model.eval()
    print(f"checkpoint: {args.ckpt_dir} | 训练 {it} 步 | 设备 {device} | 词表 {tok.vocab_size}")

    held_path = Path(args.heldout)
    held = held_path.read_text(encoding="utf-8") if held_path.exists() else ""

    # ---- 任务 A:留出代码上的交叉熵 ----
    if held:
        cover = sum(c in tok.stoi for c in PROBE_CHARS) / len(PROBE_CHARS)
        if len(tok.encode(held)) < 2 * model.config.block_size or cover < 0.5:
            print(f"\n[A] 无法评估:该模型字符表对代码字符覆盖率仅 {cover:.0%}(它没学过代码)")
        else:
            ce = heldout_loss(model, tok, held, device, model.config.block_size)
            print(f"\n[A] 留出代码交叉熵: {ce:.4f} | 困惑度: {math.exp(ce):.1f} | "
                  f"均匀分布对照: {math.log(tok.vocab_size):.4f}")
    else:
        print("\n[A] 未找到留出文件,跳过")

    # ---- 任务 B:自由生成的语法有效率 ----
    cover = sum(c in tok.stoi for c in PROBE_CHARS) / len(PROBE_CHARS)
    print(f"\n[B] 字符表对代码字符覆盖: {cover:.0%}")
    n_def = args.n_samples // 2
    prompts = ["def "] * n_def + ["class "] * (args.n_samples - n_def)
    raw_ok = prefix_ok = 0
    for pr in prompts:
        text = gen(model, tok, device, pr, args.max_new_tokens,
                   args.temperature, args.top_k)
        try:
            ast.parse(text)
            raw_ok += 1
        except (SyntaxError, ValueError):
            pass
        if has_parsable_prefix(text):
            prefix_ok += 1
    print(f"\n[B] 自由生成 {len(prompts)} 段(每段 {args.max_new_tokens} 字符):")
    print(f"    整段语法合法: {raw_ok}/{len(prompts)} = {raw_ok / len(prompts) * 100:.0f}%")
    print(f"    存在合法前缀: {prefix_ok}/{len(prompts)} = {prefix_ok / len(prompts) * 100:.0f}%")

    # ---- 任务 C:真实代码补全样例 ----
    print("\n[C] 补全样例(前缀取自留出代码):")
    prefixes: list[str] = []
    for pat in ("def ", "class "):
        i = held.find(pat)
        if i >= 0:
            j = held.find("\n", i)
            k = held.find("\n", j + 1)
            prefixes.append(held[i: k if k > 0 else j + 1])
    c_ok = 0
    for pi, pre in enumerate(prefixes[:2], 1):
        out_text = gen(model, tok, device, pre, 160, args.temperature, args.top_k)
        ok = has_parsable_prefix(out_text)
        c_ok += ok
        print(f"--- 补全 {pi}(存在合法前缀: {'是' if ok else '否'})---")
        print(out_text)
    if prefixes:
        print(f"\n补全存在合法前缀: {c_ok}/{min(2, len(prefixes))}")
    print("\nTEST_DONE", flush=True)


if __name__ == "__main__":
    main()
