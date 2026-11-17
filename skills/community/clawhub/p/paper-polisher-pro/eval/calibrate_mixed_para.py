#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""calibrate_mixed_para.py — 混写文档段落级阈值校准（v4.9.0）

v4.7.0 遗留 backlog：段落归因的 hi/med/lo 分档一直沿用文档级阈值（63.7/74.9），
未按段落分布独立校准。本脚本在混写基准（mixed_bench_20261005.json，333 段逐段真值）
上扫描阈值组合，以 AI 段二分类 F1 最优为选点，输出推荐段落阈值+混淆矩阵。

诚实声明：阈值校准于同基准（n=333，自由参数 2 个）——属「校准集内选点」，
发布口径为 triage 建议阈值；排序质量上限=已实测的段落级 AUROC 0.6883。
若未来有留出混写基准，应在其上复核。

用法：python eval/calibrate_mixed_para.py --bench eval/results/mixed_bench_20261005.json \
        --measure-out eval/results/mixed_para_20261005.json \
        --out references/para_thresholds.json
"""
import argparse
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "scripts"))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--bench", required=True)
    ap.add_argument("--measure-out", required=True,
                    help="measure_mixed_para.py 的输出（含逐段分数缓存 per_doc 无分数，需重算）")
    ap.add_argument("--out", required=True)
    a = ap.parse_args()

    docs = json.load(open(a.bench, encoding="utf-8"))
    # 重算逐段分数（与 measure_mixed_para 同口径；基准 54 篇 CPU 数分钟）
    import ai_detector
    all_pairs = []  # (score, label)
    for k, d in enumerate(docs, 1):
        rep = ai_detector.detect(d["text"], lang="zh")
        blend = ai_detector.blended_paragraph_scores(d["text"], rep)
        labels = d["para_labels"]
        n = min(len(blend), len(labels))
        all_pairs += [(blend[j], labels[j]) for j in range(n)]
        print("  %d/%d" % (k, len(docs)), flush=True)

    # 阈值扫描（v4.9.0 语义修正）：对每个 hi 候选，二分类=「score>=hi 判 AI 段」，
    # 其余段落皆非判——不再把 [med,hi) 中带排除（早期口径把中带剔出二分类，
    # F1=0.85 系口径伪象；triage 语义下中带也是人工复核对象）。
    # med 仅作为「需人工复核带」下界单独报告，不参与 F1。
    best = None
    grid = []
    hi = 50.0
    while hi <= 95.0:
        tp = sum(1 for s, l in all_pairs if l == 1 and s >= hi)
        fp = sum(1 for s, l in all_pairs if l == 0 and s >= hi)
        fn = sum(1 for s, l in all_pairs if l == 1 and s < hi)
        prec = tp / max(tp + fp, 1)
        rec = tp / max(tp + fn, 1)
        f1 = 2 * prec * rec / max(prec + rec, 1e-9)
        grid.append({"para_high": round(hi, 1), "precision": round(prec, 3),
                     "ai_para_coverage": round(rec, 3), "f1": round(f1, 4)})
        if best is None or f1 > best["f1"]:
            best = grid[-1]
        hi += 2.5

    bh = best["para_high"]
    bm = round(bh - 5.0, 1)  # 人工复核带下界（报告用）
    # 混淆矩阵（以 hi 为「判 AI 段」阈值）
    tp = sum(1 for s, l in all_pairs if l == 1 and s >= bh)
    fp = sum(1 for s, l in all_pairs if l == 0 and s >= bh)
    fn = sum(1 for s, l in all_pairs if l == 1 and s < bh)
    tn = sum(1 for s, l in all_pairs if l == 0 and s < bh)

    n_ai = tp + fn
    out = {
        "version": "v4.9.0",
        "bench": os.path.basename(a.bench),
        "n_paragraphs": len(all_pairs),
        "n_ai_paragraphs": n_ai,
        "recommended_high": {"para_high": bh, "precision": best["precision"],
                             "ai_para_coverage": best["ai_para_coverage"], "f1": best["f1"]},
        "review_band": {"para_medium_floor": bm,
                        "ai_para_coverage_ge_floor": round(
                            sum(1 for s, l in all_pairs if l == 1 and s >= bm) / max(n_ai, 1), 3)},
        "confusion_at_high": {"tp": tp, "fp": fp, "fn": fn, "tn": tn},
        "honest_conclusion": ("高置信段落判定（≥%.0f 分）精度 %.2f，但 AI 段覆盖率仅 %.0f%%——"
                              "段落归因的用途=「高置信段实锤 + 剩余段人工复核排序」，"
                              "不是段落级自动判定。文档级 AUROC 0.52-0.54 的原理性局限不变。"
                              "阈值校准于同基准（n=%d 段，单参数），属校准集内选点。"
                              % (bh, best["precision"], 100 * best["ai_para_coverage"], len(all_pairs))),
        "grid_top8": sorted(grid, key=lambda g: -g["f1"])[:8],
    }
    json.dump(out, open(a.out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("高置信阈值: hi=%s (P=%.3f 覆盖=%.3f F1=%.4f) ｜ 复核带下界: %s"
          % (bh, best["precision"], best["ai_para_coverage"], best["f1"], bm))
    print("混淆@high: TP=%d FP=%d FN=%d TN=%d" % (tp, fp, fn, tn))
    print("结论:", out["honest_conclusion"])
    print("结果:", a.out)


if __name__ == "__main__":
    main()
