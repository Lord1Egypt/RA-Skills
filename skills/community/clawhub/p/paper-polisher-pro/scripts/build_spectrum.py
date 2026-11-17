#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_spectrum — 从评测语料构建 L10 层的 AI-人类 token 频率差谱。

输出 references/token_spectrum_zh.json: {token: lift∈[-1,+1]}
  lift>0 = AI 高频, lift<0 = 人类高频。只保留总频次≥min_count 且 |lift|≥min_lift 的 token。

用法: python build_spectrum.py [--corpus ../eval/corpora_small/eval_zh.jsonl] [--apply]
"""
import os, re, json, argparse
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "references", "token_spectrum_zh.json")


def zh_tokens(text):
    toks = []
    for run in re.findall(r"[\u4e00-\u9fff]+", text):
        if len(run) == 1:
            toks.append(run)
        else:
            toks.extend(run[i:i + 2] for i in range(len(run) - 1))
    toks.extend(w for w in re.findall(r"[a-zA-Z]{2,}", text.lower()))
    toks.extend(re.findall(r"[，。；：！？、]", text))
    return toks


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--corpus", default=os.path.join(HERE, "..", "eval", "corpora_small", "eval_zh.jsonl"))
    ap.add_argument("--split", default="calib", choices=["calib", "test", "all"],
                    help="只用 calib 半构建频谱, test 半留给最终评测(防in-sample过拟合)")
    ap.add_argument("--min-count", type=int, default=8)
    ap.add_argument("--min-lift", type=float, default=0.25)
    ap.add_argument("--apply", action="store_true")
    a = ap.parse_args()

    recs = [json.loads(l) for l in open(a.corpus, encoding="utf-8") if l.strip()]
    recs = [r for r in recs if r.get("attack") == "none"]
    from pp_split import filter_split
    recs = filter_split(recs, a.split)
    ai_cnt, hu_cnt = Counter(), Counter()
    ai_docs = hu_docs = 0
    for r in recs:
        c = Counter(zh_tokens(r["text"]))
        if r["label"] == 1:
            ai_cnt.update(c)
            ai_docs += 1
        else:
            hu_cnt.update(c)
            hu_docs += 1
    print("语料: ai=%d docs, human=%d docs" % (ai_docs, hu_docs))

    spec = {}
    for t, ac in ai_cnt.items():
        hc = hu_cnt.get(t, 0)
        total = ac + hc
        if total < a.min_count:
            continue
        # 归一化为每文档频率再算 lift
        af, hf = ac / ai_docs, hc / hu_docs
        lift = (af - hf) / (af + hf + 1e-9)
        if abs(lift) >= a.min_lift:
            spec[t] = round(lift, 3)
    pos = sum(1 for v in spec.values() if v > 0)
    print("频谱: %d tokens (AI高频 %d / 人类高频 %d)" % (len(spec), pos, len(spec) - pos))
    print("  AI高频Top: ", sorted(((t, v) for t, v in spec.items() if v > 0), key=lambda x: -x[1])[:12])
    print("  人类高频Top:", sorted(((t, v) for t, v in spec.items() if v < 0), key=lambda x: x[1])[:12])

    if a.apply:
        json.dump({"version": "1.0", "built_from": os.path.basename(a.corpus),
                   "ai_docs": ai_docs, "human_docs": hu_docs,
                   "tokens": spec},
                  open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print("✅ 已写入 %s" % OUT)


if __name__ == "__main__":
    main()
