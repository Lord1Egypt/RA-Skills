#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
run_topic_assessment.py — 本地选题评估全流程（无需 coze / 无需 LLM 也能出真实结果）。

把三个真实/确定性环节串起来，产出一份完整的选题评价：
  1. literature_probe.dedup_probe  → 真实 Europe PMC 命中数（Cochrane / PubMed SR-MA）
  2. registry_probe.probe_local    → 真实 ClinicalTrials.gov 已注册试验数
  3. topic_assess.assess            → 确定性 4 维评分(临床/方法/数据/新颖性,0-5) + 裁决
                                      + R1-R6 交叉核查 + PRISMA/AMSTAR-2 预检 + real-gap

临床价值维度属判断项：本地默认中值并标注「需人工/LLM 确认」，可用 --clinical 由
LLM/人工覆盖（对齐用户意图：判断类维度本就该用 LLM/Coze 能力）。

用法：
  python scripts/run_topic_assessment.py "SGLT2 inhibitors heart failure reduced ejection fraction" \
      --topic-en "SGLT2 inhibitors heart failure reduced ejection fraction" \
      --out-json out/assess.json --out-md out/assess.md

依赖：仅标准库 + 同仓 adapters/（literature_probe / registry_probe / topic_assess）。
"""
import argparse
import datetime
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ADAPTERS = os.path.join(os.path.dirname(HERE), "adapters")
sys.path.insert(0, ADAPTERS)

import literature_probe  # noqa: E402
import registry_probe    # noqa: E402
import topic_assess      # noqa: E402


def render_md(topic, a):
    s = a["scores"]
    v = a.get("verdict_raw", a.get("verdict", "n/a"))
    vt = a.get("verdict_note", "")
    et = a.get("evidence_tags", {})
    lines = [
        "# 选题评估（本地确定性 + 真实探针）",
        "",
        "**主题**：%s  " % topic,
        "**评估日期**：%s  " % a.get("assessed_on", ""),
        "**裁决**：**%s** —— %s" % (v, vt),
        "",
        "## 四维评分（各 0–5，总分 %d/20）" % s["total"],
        "",
        "| 维度 | 得分 | 证据来源 | 锚点理由 |",
        "| --- | --- | --- | --- |",
        "| 临床价值 | %d | %s | %s |" % (s["clinical"], et.get("clinical", "—"),
                                          a["score_anchors"].get("clinical", "")),
        "| 方法可行性 | %d | %s | %s |" % (s["feasibility"], et.get("feasibility", "—"),
                                            a["score_anchors"].get("feasibility", "")),
        "| 数据可得性 | %d | %s | %s |" % (s["data"], et.get("data", "—"),
                                          a["score_anchors"].get("data", "")),
        "| 新颖性 | %d | %s | %s |" % (s["novelty"], et.get("novelty", "—"),
                                       a["score_anchors"].get("novelty", "")),
        "",
        "## 真实探针证据",
        "",
        "- Cochrane 系统评价：%s" % a["dedup"].get("cochrane", "未探针"),
        "- PubMed SR/MA（近 5 年）：%s" % a["dedup"].get("pubmed", "未探针"),
        "- 注册库（ClinicalTrials.gov）：%s" % a.get("expected_studies", "未探针"),
        "- 真实缺口判定：%s" % a["gap"].get("label", "—"),
        "",
        "## 交叉核查 R1–R6",
        "",
    ]
    for c in a.get("cross_checks", []):
        flag = "⚠ 触发" if c.get("triggered") else "✓ 通过"
        lines.append("- **%s** %s：%s" % (c["rule"], flag, c.get("note", "")))
    lines += [
        "",
        "## 去重段落",
        "",
        "- 近重复风险：%s" % a["dedup"].get("near_duplicate", ""),
        "- 增量说明：%s" % a["dedup"].get("increment", ""),
        "- PROSPERO：%s" % a["dedup"].get("prospero", ""),
        "",
        "## 合规预检（PRISMA 2020 / AMSTAR-2）",
        "",
        "- 总体风险：%s" % a.get("compliance", {}).get("overall_risk", "—"),
        "- 说明：%s" % a.get("compliance", {}).get("note", ""),
        "",
        "> 本地确定性评估：数据/新颖性/方法可行性由真实探针（Europe PMC + ClinicalTrials.gov）驱动；"
        "临床价值属判断项，默认中值并标注需人工/LLM 确认（可用 --clinical 覆盖）。",
    ]
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser(description="本地选题评估（真实探针 + 确定性 4 维评分）")
    ap.add_argument("--topic", required=True, help="选题（可中文，自动翻译为英文检索词）")
    ap.add_argument("--topic-en", default=None, help="英文检索词（提供则优先用于检索）")
    ap.add_argument("--year-from", type=int, default=None, help="起始年份（PubMed 层）")
    ap.add_argument("--max", type=int, default=8, help="每层返回样本数上限")
    ap.add_argument("--clinical", type=int, default=None,
                    help="LLM/人工覆盖临床价值维度（0-5）；不填则本地默认中值")
    ap.add_argument("--out-json", default=None, help="输出评估 JSON 路径")
    ap.add_argument("--out-md", default=None, help="输出评估 Markdown 报告路径")
    args = ap.parse_args()

    q = args.topic_en or args.topic
    print("[1/3] Europe PMC 去重探针 ...", file=sys.stderr)
    dedup = literature_probe.dedup_probe(q, year_from=args.year_from, max_results=args.max)
    print("[2/3] ClinicalTrials.gov 注册库探针 ...", file=sys.stderr)
    reg = registry_probe.probe_local(q, max_results=5)
    print("[3/3] 本地确定性评估 ...", file=sys.stderr)
    a = topic_assess.assess(args.topic, picos={}, missing=[], dedup=dedup,
                            registry=reg, clinical_override=args.clinical)
    a["probes"] = {
        "cochrane_hits": (dedup.get("layers", {}).get("cochrane", {}) or {}).get("hit_count"),
        "pubmed_hits": (dedup.get("layers", {}).get("pubmed_meta", {}) or {}).get("hit_count"),
        "registry_total": reg.get("total"),
        "registry_sample": reg.get("sample"),
        "cjk_untranslated": dedup.get("cjk_untranslated", False),
    }

    if args.out_json:
        with open(args.out_json, "w", encoding="utf-8") as f:
            json.dump(a, f, ensure_ascii=False, indent=2)
        print("wrote %s" % args.out_json, file=sys.stderr)
    if args.out_md:
        with open(args.out_md, "w", encoding="utf-8") as f:
            f.write(render_md(args.topic, a))
        print("wrote %s" % args.out_md, file=sys.stderr)

    print(json.dumps({
        "topic": args.topic,
        "scores": a["scores"],
        "verdict": a.get("verdict_raw", a.get("verdict")),
        "verdict_note": a.get("verdict_note"),
        "cochrane_hits": a["probes"]["cochrane_hits"],
        "pubmed_hits": a["probes"]["pubmed_hits"],
        "registry_total": a["probes"]["registry_total"],
        "gap": a["gap"].get("label"),
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
