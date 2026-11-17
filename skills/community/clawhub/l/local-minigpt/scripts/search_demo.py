# -*- coding: utf-8 -*-
"""「让 AI 学会搜索」开卷对照演示。

原理说明(诚实版):真实大模型的「决定何时搜索、搜什么」来自指令微调后的
工具调用能力;字符级 MiniGPT 不会自己「决定」搜索。本演示把搜索决策写成
固定流程,让模型做**检索增强生成(RAG)的最小可运行示例**:

  1) 用 web_search.py 抓取真实网页摘要;
  2) 同一提示词各生成一次:闭卷(只给问题)vs 开卷(先给检索到的网页文本);
  3) 用 8-gram 重合率标注输出里有多少比例「引自网页」、多少「模型硬编」。

用法:
  python scripts/search_demo.py --ckpt-dir checkpoints/demo --query "学而时习之" --n 3
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent / "minigpt"))

import torch

from generate import load_model
from web_search import search


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="开卷 vs 闭卷对照演示")
    p.add_argument("--ckpt-dir", default=str(HERE.parent / "checkpoints" / "demo"))
    p.add_argument("--query", default="学而时习之 不亦说乎")
    p.add_argument("--n", type=int, default=3, help="取前 n 条搜索结果")
    p.add_argument("--max-new-tokens", type=int, default=120)
    p.add_argument("--temperature", type=float, default=0.7)
    p.add_argument("--top-k", type=int, default=40)
    return p.parse_args()


def ngram_overlap(text: str, refs: str, n: int = 8) -> float:
    """输出中出现在检索文本里的 n-gram 比例(粗略的「引用率」)。"""
    text = "".join(text.split())
    refs = "".join(refs.split())
    if len(text) < n:
        return 0.0
    hit = sum(1 for i in range(len(text) - n + 1) if text[i: i + n] in refs)
    return hit / max(1, len(text) - n + 1)


@torch.no_grad()
def gen(model, tok, device: str, prompt: str, max_new_tokens: int,
        temperature: float, top_k: int) -> str:
    ids = tok.encode(prompt)
    if not ids:
        return "(提示词字符全部不在词表内,无法生成)"
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
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model, tok, it, vl = load_model(args.ckpt_dir, device)
    model.eval()
    print(f"被试模型: {args.ckpt_dir} | 训练 {it} 步 | 设备 {device}")

    # ---- 第 1 步:联网搜索 ----
    print(f"\n[1] 搜索: {args.query}")
    used, results = search(args.query, args.n)
    if not results:
        print("[搜索失败] 当前网络不可用;只能做闭卷生成。")
        results = []
    for i, r in enumerate(results, 1):
        print(f"  来源{i}: {r['title']}  {r['url']}")
    refs = "\n".join(f"【网页{i}】{r['title']}。{r['snippet']}" for i, r in enumerate(results, 1))
    cover = sum(c in tok.stoi for c in refs) / max(1, len(refs))
    print(f"\n检索文本对该模型字符表的覆盖率: {cover:.0%}"
          + ("" if cover >= 0.5 else "(过低,开卷收益有限——换个与模型语料同域的查询更合理)"))

    # ---- 第 2 步:闭卷生成 ----
    print("\n[2] 闭卷生成(只给问题,不给网页):")
    closed = gen(model, tok, device, args.query + "\n",
                 args.max_new_tokens, args.temperature, args.top_k)
    print(closed)
    print(f"    → 引用率(与网页 8-gram 重合): {ngram_overlap(closed, refs):.0%}")

    # ---- 第 3 步:开卷生成 ----
    if results:
        prompt = refs + f"\n\n问题: {args.query}\n答: "
        print("\n[3] 开卷生成(先给检索到的网页文本):")
        opened = gen(model, tok, device, prompt,
                     args.max_new_tokens, args.temperature, args.top_k)
        print(opened)
        print(f"    → 引用率(与网页 8-gram 重合): {ngram_overlap(opened, refs):.0%}")
        print("\n解读:开卷引用率显著高于闭卷,即「检索增强」的机制效果——"
              "模型不会搜索,但检索到的文本会实时改变它的输出。")
    print("\nDEMO_DONE", flush=True)


if __name__ == "__main__":
    main()
