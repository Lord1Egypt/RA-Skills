#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
calibrate_v3 — v3 融合权重与阈值的数据驱动校准。

对基线语料逐文档计算四个组件分:
  para  = 旧引擎段落均分(0-100, 归一化到0-1)
  surf  = L9 表面统计(0-10 → 0-1)
  spec  = L10 词频谱(0-10 → 0-1)
  cot   = L11 思维链(0-10 → 0-1)
按长度带(short<300/mid/long>800)网格搜索权重(每带独立), 目标=全集AUROC最大。
阈值: 人类得分分布 p95=medium 线, p99=high 线。

输出 references/fusion_config.json, ai_detector 运行时加载。
用法: python calibrate_v3.py [--corpus ...] [--apply]
"""
import os, sys, json, argparse, itertools

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import ai_detector
import layers_surface as LS

OUT = os.path.join(HERE, "..", "references", "fusion_config.json")


def components(text):
    cats = ai_detector.load_patterns("zh")
    paras = ai_detector.split_paragraphs(text)
    if not paras:
        return None
    scores = [ai_detector.score_paragraph(p, "zh", cats).ai_score for p in paras]
    lens = [len(p) for p in paras]
    para = sum(s * l for s, l in zip(scores, lens)) / max(sum(lens), 1) / 100.0
    surf = LS.surface_layer(text)["score"] / 10.0
    spec = LS.spectrum_layer(text)["score"] / 10.0
    cot = LS.cot_layer(text)["score"] / 10.0
    return para, surf, spec, cot


def auroc(pairs):
    pos = [s for s, l in pairs if l == 1]
    neg = [s for s, l in pairs if l == 0]
    if not pos or not neg:
        return 0.0
    # 秩法(并列平均)
    ranked = sorted(pairs, key=lambda x: x[0])
    ranks, i = {}, 0
    while i < len(ranked):
        j = i
        while j < len(ranked) and ranked[j][0] == ranked[i][0]:
            j += 1
        avg = (i + 1 + j) / 2.0
        for k in range(i, j):
            ranks[id(ranked[k])] = avg
        i = j
    n1, n0 = len(pos), len(neg)
    sum_pos = sum(ranks[id(p)] for p in ranked if p[1] == 1)
    return (sum_pos - n1 * (n1 + 1) / 2) / (n1 * n0)


def band_of(length):
    return "short" if length < 300 else ("mid" if length < 800 else "long")


GRID = [0.0, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.5, 0.6]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--corpus", default=os.path.join(HERE, "..", "eval", "corpora_small", "eval_zh.jsonl"))
    ap.add_argument("--split", default="calib", choices=["calib", "test", "all"],
                    help="只用 calib 半校准权重, test 半留给最终评测")
    ap.add_argument("--apply", action="store_true")
    a = ap.parse_args()

    recs = [json.loads(l) for l in open(a.corpus, encoding="utf-8") if l.strip()]
    recs = [r for r in recs if r.get("attack") == "none"]
    from pp_split import filter_split
    recs = filter_split(recs, a.split)
    docs = []
    for r in recs:
        c = components(r["text"])
        if c:
            docs.append({"band": band_of(r["length"]), "label": r["label"],
                         "para": c[0], "surf": c[1], "spec": c[2], "cot": c[3]})
    print("组件计算完成: %d docs" % len(docs))
    from collections import Counter
    print("  长度带分布:", dict(Counter(d["band"] for d in docs)))

    # 每带独立网格搜索 (para权重为主轴, 其余三者归一)
    best = {}
    for band in ("short", "mid", "long"):
        seg = [d for d in docs if d["band"] == band]
        if not seg:
            continue
        best_score, best_w = -1, None
        for wp in [x / 20 for x in range(8, 21)]:  # para 0.4-1.0
            rest = round(1.0 - wp, 2)
            for w1 in [x / 20 for x in range(0, int(rest * 20) + 1)]:
                for w2 in [x / 20 for x in range(0, int(round((rest - w1) * 20)) + 1)]:
                    w3 = round(rest - w1 - w2, 2)
                    if w3 < -1e-9:
                        continue
                    pairs = [(wp * d["para"] + w1 * d["spec"] + w2 * d["surf"] + w3 * d["cot"], d["label"])
                             for d in seg]
                    au = auroc(pairs)
                    if au > best_score:
                        best_score, best_w = au, (wp, w1, w2, w3)
        best[band] = {"weights": {"para": best_w[0], "spectrum": best_w[1],
                                  "surface": best_w[2], "cot": best_w[3]},
                      "band_auroc": round(best_score, 4), "n": len(seg)}
        print("  [%s] AUROC=%.4f  weights=%s (n=%d)" % (band, best_score, best[band]["weights"], len(seg)))

    # 全局阈值: 用各自带权重给全体人类文档打分
    def fuse(d):
        w = best[d["band"]]["weights"]
        return w["para"] * d["para"] + w["spectrum"] * d["spec"] + \
               w["surface"] * d["surf"] + w["cot"] * d["cot"]

    hu_scores = sorted(fuse(d) for d in docs if d["label"] == 0)
    import math
    def pct(p):
        k = min(len(hu_scores) - 1, max(0, math.ceil(p * len(hu_scores)) - 1))
        return round(hu_scores[k], 4)
    thresholds = {"medium": pct(0.95), "high": pct(0.99)}
    print("全局阈值(人类分布): medium(p95)=%.4f high(p99)=%.4f" % (thresholds["medium"], thresholds["high"]))

    overall = auroc([(fuse(d), d["label"]) for d in docs])
    print("融合后全集 AUROC: %.4f" % overall)

    if a.apply:
        json.dump({"version": "1.0", "calibrated": __import__("time").strftime("%Y-%m-%d"),
                   "overall_auroc": round(overall, 4), "bands": best, "thresholds": thresholds},
                  open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print("✅ 已写入 %s" % OUT)


if __name__ == "__main__":
    main()
