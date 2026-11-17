#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
build_gap_probe.py — 一键产出 meta-analysis 选题「真实缺口」gap 字段。

封装 literature_probe.py 的双探针逻辑：
  1) 窄方向（narrow）：跑 Cochrane + PubMed SR/MA 两次探针，取真实 hit_count；
  2) 宽泛父方向（broad）：仅跑 PubMed SR/MA 探针，取 hit_count；
  3) 算 ratio = 窄.PubMed / 宽.PubMed，按 topic-selection.md 阈值判定缺口。

产出严格对齐 scripts/generate_topic_report.py::build_quick_card 消费的 `gap`
字段结构，可直接：
  - `--out gap.json`        单独输出 gap 字段；
  - `--merge-into input.json` 把 gap 合并进选题 input.json 顶层（喂给报告生成器）。

依赖：仅标准库 + 同目录 literature_probe.py（零第三方依赖，可离线判定）。

用法：
  python adapters/build_gap_probe.py \
      --narrow "PD-1 inhibitors NSCLC second line" \
      --broad "NSCLC immunotherapy" \
      --out gap.json
  # 一键合并进现有选题 input.json：
  python adapters/build_gap_probe.py -n "..." -b "..." --merge-into topic_input.json
"""
import argparse
import json
import os
import sys

# 让脚本在任意 cwd 下都能 import 同目录的 literature_probe
_HERE = os.path.dirname(os.path.abspath(__file__))
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

try:
    from literature_probe import probe
except ImportError as _e:  # 致命：缺依赖探针
    sys.stderr.write("[FATAL] 无法加载 literature_probe.py：%s\n" % _e)
    sys.exit(2)

# gap.verdict -> 中文短标签（与 generate_topic_report.GAP_ZH 保持一致）
GAP_LABEL_ZH = {
    "real_gap": "真实缺口",
    "saturated": "已饱和",
    "caution": "需谨慎",
    "unverified": "未验证",
}


def _judge(broad_topic, narrow_cochrane, narrow_pubmed, broad_pubmed):
    """按 topic-selection.md 阈值判定缺口 verdict。

    返回 (verdict, ratio, summary)。ratio 为 None 表示无法计算对比比。
    判定口径（与契约一致）：
      - ratio < 0.3 且 Cochrane < 10           -> real_gap（真实缺口，✅）
      - ratio >= 0.5 或 Cochrane >= 20         -> saturated（已饱和，🔴）
      - 介于两者之间                           -> caution（⚠️，须差异化）
      - 任一探针命中数为空                       -> unverified（⚠️，未验证）
    """
    if narrow_cochrane is None or narrow_pubmed is None or broad_pubmed is None:
        return "unverified", None, "探针不可用（网络受限或命中数为空），缺口未验证"

    if broad_pubmed <= 0:
        # 宽泛方向本身无命中：窄方向若也极稀疏则疑似真实缺口，否则需人工复核
        if narrow_cochrane < 10:
            summary = ("宽泛父方向「%s」PubMed 无命中，窄方向 Cochrane 仅 %d 篇 → "
                       "疑似极细分缺口，建议人工复核" % (broad_topic, narrow_cochrane))
            return "real_gap", None, summary
        summary = "宽泛父方向 PubMed 无命中，无法计算对比比，建议人工复核"
        return "caution", None, summary

    ratio = narrow_pubmed / float(broad_pubmed)
    inv = max(1, round(broad_pubmed / narrow_pubmed))  # 用于 1/N 表述

    if ratio < 0.3 and narrow_cochrane < 10:
        verdict = "real_gap"
        summary = ("该窄方向 PubMed SR/MA（近 5 年）%d 篇，约为宽泛方向「%s」(%d) 的 1/%d → 真实缺口"
                   % (narrow_pubmed, broad_topic, broad_pubmed, inv))
    elif ratio >= 0.5 or narrow_cochrane >= 20:
        verdict = "saturated"
        summary = ("该窄方向 PubMed SR/MA（近 5 年）%d 篇，占宽泛方向「%s」(%d) 的 %.0f%% → 已饱和，须明确增量"
                   % (narrow_pubmed, broad_topic, broad_pubmed, ratio * 100))
    else:
        verdict = "caution"
        summary = ("该窄方向 PubMed SR/MA（近 5 年）%d 篇，约为宽泛方向「%s」(%d) 的 1/%d → 方向已有覆盖，须差异化"
                   % (narrow_pubmed, broad_topic, broad_pubmed, inv))
    return verdict, ratio, summary


def _ratio_human(ratio):
    if ratio is None:
        return "—"
    if ratio >= 1:
        return "%.2fx" % ratio
    return "1/%d" % max(1, round(1.0 / ratio))


def main():
    ap = argparse.ArgumentParser(
        description="一键产出 meta-analysis 选题真实缺口 gap 字段（窄方向+宽泛父方向双探针）")
    ap.add_argument("-n", "--narrow", required=True, help="窄方向查询（PICO 派生，如 'PD-1 inhibitors NSCLC second line'）")
    ap.add_argument("-b", "--broad", required=True, help="宽泛父方向查询（用于对比比，如 'NSCLC immunotherapy'）")
    ap.add_argument("--review-type", default="systematic-review",
                    choices=["meta-analysis", "systematic-review", "rct"])
    ap.add_argument("--year-from", type=int, help="PubMed 层起始年（默认近 5 年）")
    ap.add_argument("--year-to", type=int, help="PubMed 层截止年")
    ap.add_argument("-o", "--out", help="输出 gap JSON 路径（仅 gap 字段）")
    ap.add_argument("--merge-into", help="把 gap 合并进该选题 input.json（顶层 gap 键）")
    args = ap.parse_args()

    sys.stderr.write("[probe] narrow: %s\n" % args.narrow)
    sys.stderr.write("[probe] broad : %s\n" % args.broad)

    narrow_cochrane = probe(args.narrow, layer="cochrane",
                            year_from=args.year_from, year_to=args.year_to, max_results=1)
    narrow_pubmed = probe(args.narrow, layer="pubmed", review_type=args.review_type,
                          year_from=args.year_from, year_to=args.year_to, max_results=1)
    broad_pubmed = probe(args.broad, layer="pubmed", review_type=args.review_type,
                         year_from=args.year_from, year_to=args.year_to, max_results=1)

    nc = narrow_cochrane.get("hit_count")
    np_ = narrow_pubmed.get("hit_count")
    bp = broad_pubmed.get("hit_count")

    verdict, ratio, summary = _judge(args.broad, nc, np_, bp)
    label = GAP_LABEL_ZH.get(verdict, verdict)

    gap = {
        "probe_used": (nc is not None and np_ is not None and bp is not None),
        "narrow": {"cochrane": nc, "pubmed": np_},
        "broad": {"topic": args.broad, "pubmed": bp},
        "ratio_narrow_over_broad": (round(ratio, 4) if ratio is not None else None),
        "verdict": verdict,
        "label": label,
        "summary": summary,
    }

    sys.stderr.write("[result] %s | ratio=%s | Cochrane(narrow)=%s PubMed(narrow)=%s PubMed(broad)=%s\n"
                     % (label, _ratio_human(ratio), nc, np_, bp))

    payload = json.dumps(gap, ensure_ascii=False, indent=2)

    if args.merge_into:
        with open(args.merge_into, "r", encoding="utf-8") as f:
            data = json.load(f)
        data["gap"] = gap
        with open(args.merge_into, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        sys.stderr.write("[OK] merged gap into %s\n" % args.merge_into)
    elif args.out:
        with open(args.out, "w", encoding="utf-8") as f:
            f.write(payload)
        sys.stderr.write("[OK] wrote gap -> %s\n" % args.out)

    # stdout 始终输出 gap（便于管道 / 复制）
    print(payload)


if __name__ == "__main__":
    main()
