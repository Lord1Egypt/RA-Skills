#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""build_mixed_bench.py — 可控混写文档基准（v4.7.0 混写专项）

目的：混写文档的「文档级 AUROC 0.52-0.54」是原理性局限（文档级平均被稀释/顶起），
但**段落级**归因应当可用——本脚本构造逐段真值已知的混写文档，量化段落级判别力，
把边界矩阵从「定性局限」升级为「定量：文档级弱、段落级可用，用 pp_workflow 段落归因」。

方法学（防审计质疑，逐条声明）：
  - 段落来源：老代留出 test 半人类文档 + 当打代 AI 文档（eval_gen2026 全部为评测集，
    本基准只做评测、不入训练——check_leak 闸可验）
  - 合成模式×AI 占比：interleave（交替）/ ai_lead（AI 开头）/ human_lead（人类开头）
    × AI 段占比 25%/50%/75%，逐段真值由构造记录
  - 段落最短 40 字（过短段无文体分布，引擎本来就按短段弱化）
  - 确定性：seed=47，同参数重跑逐字节同基准

用法：
  python eval/build_mixed_bench.py --n-per-cell 6 --out eval/results/mixed_bench_20261005.json
"""
import argparse
import json
import os
import random
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "scripts"))

MIN_PARA = 40


def load_split_texts(path, label):
    from pp_split import filter_split
    recs = [json.loads(l) for l in open(path, encoding="utf-8") if l.strip()]
    recs = filter_split(recs, "test")
    out = []
    for r in recs:
        if r.get("label") != label or r.get("attack", "none") != "none":
            continue
        for p in (r["text"] or "").split("\n"):
            p = p.strip()
            if len(p) >= MIN_PARA:
                out.append(p)
    return out


def synth(pattern, ai_paras, hu_paras, rng):
    """按模式合成一个混写文档，返回 (text, labels) labels: 1=AI 段 0=人类段。"""
    if pattern == "interleave":
        seq = []
        for i in range(max(len(ai_paras), len(hu_paras))):
            if i < len(hu_paras):
                seq.append((hu_paras[i], 0))
            if i < len(ai_paras):
                seq.append((ai_paras[i], 1))
    elif pattern == "ai_lead":
        seq = [(p, 1) for p in ai_paras] + [(p, 0) for p in hu_paras]
    elif pattern == "human_lead":
        seq = [(p, 0) for p in hu_paras] + [(p, 1) for p in ai_paras]
    else:
        raise ValueError(pattern)
    rng.shuffle(seq)
    return "\n\n".join(p for p, _ in seq), [l for _, l in seq]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n-per-cell", type=int, default=6, help="每单元格（模式×占比）文档数")
    ap.add_argument("--out", default=os.path.join(HERE, "results", "mixed_bench.json"))
    a = ap.parse_args()
    rng = random.Random(47)

    corpora = os.path.join(HERE, "corpora_small")
    hu = load_split_texts(os.path.join(corpora, "eval_zh.jsonl"), 0)
    ai = load_split_texts(os.path.join(corpora, "eval_gen2026.jsonl"), 1)
    print("段落池: 人类 %d / 当打代 AI %d（test 半，≥%d 字）" % (len(hu), len(ai), MIN_PARA))

    docs = []
    for pattern in ("interleave", "ai_lead", "human_lead"):
        for frac in (0.25, 0.5, 0.75):
            for k in range(a.n_per_cell):
                # AI 占比 frac → 段数比（人类段 = AI 段 × (1-frac)/frac，至少 1）
                n_ai = rng.randint(2, 3)
                n_hu = max(1, round(n_ai * (1 - frac) / frac))
                ai_p = rng.sample(ai, min(n_ai, len(ai)))
                hu_p = rng.sample(hu, min(n_hu, len(hu)))
                text, labels = synth(pattern, ai_p, hu_p, rng)
                docs.append({"id": "mix_%s_%d_%d" % (pattern, int(frac * 100), k),
                             "pattern": pattern, "ai_fraction": frac,
                             "text": text, "para_labels": labels})
    # 真实 AI 段占比统计（shuffle 后实际值）
    for d in docs:
        d["actual_ai_fraction"] = round(sum(d["para_labels"]) / len(d["para_labels"]), 3)

    os.makedirs(os.path.dirname(a.out), exist_ok=True)
    json.dump(docs, open(a.out, "w", encoding="utf-8"), ensure_ascii=False)
    fr = sorted(set(d["actual_ai_fraction"] for d in docs))
    print("合成混写文档: %d 篇 → %s" % (len(docs), a.out))
    print("实际 AI 段占比档位:", fr)


if __name__ == "__main__":
    main()
