#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""measure_mixed_para.py — 混写基准的段落级判别力实测（v4.7.0）

对 build_mixed_bench.py 产出的逐段真值基准，跑引擎段落混合分（与 paragraph_report.py
同口径的 blended_paragraph_scores），输出：
  - 段落级 AUROC（全部段落，label=1 为 AI 段）
  - 文档内判定质量：hi/med/lo 与真值的一致率、AI 段召回、人类段误报
  - 按 AI 占比分档的细分
结果落 eval/results/mixed_para_<tag>.json —— 边界矩阵「混写文档」行引用本文件。

用法：python eval/measure_mixed_para.py --bench eval/results/mixed_bench_20261005.json --tag 20261005
"""
import argparse
import json
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "scripts"))

import ai_detector  # noqa: E402


def para_auroc(pairs):
    """秩法 AUROC（与 run_eval.py auroc 同口径，含并列平均秩）。"""
    if not pairs:
        return None
    ranked = sorted(pairs, key=lambda x: x[0])
    n1 = sum(1 for _, l in ranked if l == 1)
    n0 = len(ranked) - n1
    if not n1 or not n0:
        return None
    sum_pos, i = 0.0, 0
    while i < len(ranked):
        j = i
        while j < len(ranked) and ranked[j][0] == ranked[i][0]:
            j += 1
        avg = (i + 1 + j) / 2.0
        sum_pos += sum(avg for k in range(i, j) if ranked[k][1] == 1)
        i = j
    return round((sum_pos - n1 * (n1 + 1) / 2) / (n1 * n0), 4)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--bench", required=True)
    ap.add_argument("--tag", default="run")
    ap.add_argument("--out", default=None)
    a = ap.parse_args()

    docs = json.load(open(a.bench, encoding="utf-8"))
    fc = ai_detector._load_fusion_config() or {}
    thr = fc.get("thresholds", {"medium": 0.35, "high": 0.60})
    tm, th = float(thr["medium"]) * 100, float(thr["high"]) * 100

    all_pairs, per_doc, t0 = [], [], time.time()
    for k, d in enumerate(docs, 1):
        rep = ai_detector.detect(d["text"], lang="zh")
        blend = ai_detector.blended_paragraph_scores(d["text"], rep)
        labels = d["para_labels"]
        # 对齐：paragraph_scores 与 blend 逐段（构造文档不截段，长度应一致）
        n = min(len(blend), len(labels))
        doc_pairs = [(blend[j], labels[j]) for j in range(n)]
        all_pairs += doc_pairs
        hi = sum(1 for s, l in doc_pairs if l == 1 and s >= th)
        hu_wrong = sum(1 for s, l in doc_pairs if l == 0 and s >= tm)
        per_doc.append({"id": d["id"], "pattern": d["pattern"],
                        "ai_fraction": d["actual_ai_fraction"],
                        "n_para": n, "para_auroc": para_auroc(doc_pairs),
                        "ai_para_recall@high": round(hi / max(sum(labels), 1), 3),
                        "hu_para_fp@med": round(hu_wrong / max(n - sum(labels), 1), 3)})
        if k % 10 == 0:
            print("  %d/%d docs (%.0fs)" % (k, len(docs), time.time() - t0), flush=True)

    overall = para_auroc(all_pairs)
    by_frac = {}
    for fr in sorted(set(p["ai_fraction"] for p in per_doc)):
        grp = [p for p in per_doc if p["ai_fraction"] == fr]
        by_frac[fr] = {"docs": len(grp),
                       "mean_para_auroc": round(sum(p["para_auroc"] or 0 for p in grp) / len(grp), 4)}
    ai_rec = round(sum(p["ai_para_recall@high"] * p["n_para"] for p in per_doc) /
                   max(sum(p["n_para"] for p in per_doc if True), 1), 4)
    res = {"tag": a.tag, "bench": os.path.basename(a.bench), "model_fp": _fp(),
           "n_docs": len(docs), "n_paras": len(all_pairs),
           "para_auroc_overall": overall,
           "thresholds": {"medium": round(tm, 1), "high": round(th, 1)},
           "ai_para_recall@high_weighted": ai_rec,
           "hu_para_fp@med_mean": round(sum(p["hu_para_fp@med"] for p in per_doc) / len(per_doc), 4),
           "by_ai_fraction": by_frac, "per_doc": per_doc,
           "note": "文档级混写 AUROC 0.52-0.54（原理性局限）；本表为段落级实测——"
                   "结论若 paragraphs 可用，边界矩阵引导用户用 pp_workflow/paragraph_report 段落归因"}
    out = a.out or os.path.join(HERE, "results", "mixed_para_%s.json" % a.tag)
    json.dump(res, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("段落级 AUROC 总体: %s ｜ n_paras=%d ｜ 耗时 %.0fs" % (overall, len(all_pairs), time.time() - t0))
    print("AI 段召回@high(加权):", res["ai_para_recall@high_weighted"],
          "｜ 人类段误报@med(均值):", res["hu_para_fp@med_mean"])
    print("结果:", out)


def _fp():
    import hashlib
    p = os.path.expanduser("~/.cache/paper-polisher/qwen3-detector/model.int8.onnx")
    if not os.path.isfile(p):
        return "rules"
    h = hashlib.md5()
    with open(p, "rb") as f:
        for c in iter(lambda: f.read(1 << 22), b""):
            h.update(c)
    return h.hexdigest()[:12]


if __name__ == "__main__":
    main()
