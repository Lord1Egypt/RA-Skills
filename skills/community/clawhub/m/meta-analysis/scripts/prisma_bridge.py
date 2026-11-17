#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
prisma_bridge.py — ct-literature (.merged.json) → meta-analysis `prisma_flow` params.

This is the *only* sanctioned glue between the two skills' PRISMA representations.
It reads the machine PRISMA screen block that `ct-literature`'s `screen_prisma.py`
writes into `.merged.json`, then produces a request envelope that the
meta-analysis `prisma_flow` task (metagear::plot_PRISMA) can consume directly.

Field mapping (see review_workflow.md §1.x for the full rationale):

  AUTO-FILLED (derivable from ct-literature output, no human judgement):
    screened        <- identified_records   (post-dedup total, all title/abstract screened)
    excluded_title  <- excluded_records      (title/abstract rule-excluded)
    records         <- identified_records + duplicates_removed  (raw pre-dedup DB total)
    duplicates      <- duplicates_removed    (item-1 count; REQUIRES_MANUAL if absent)

  REQUIRES MANUAL (cannot be automated — full-text / eligibility / final inclusion):
    other_sources   hand-search, citation chasing, etc.
    assessed        full-text articles assessed for eligibility
    excluded_elig    full-text exclusions (with reasons)
    included         studies FINALLY included in the meta-analysis
    reports          reports of included studies (optional; only if != included)

CRITICAL SEMANTIC GUARD
-----------------------
ct-literature's `included_records` is the count that *passed the machine
title/abstract screen* — it is NOT the number of studies finally included in the
review. Under no circumstance is it mapped to `included`. It MAY be surfaced as a
*suggestion* for `assessed` (records proceeding to full-text) but must be
confirmed by human review before use. Mapping it directly to `included` would
silently produce a methodologically wrong PRISMA diagram.
"""
import argparse
import json
import os
import sys

# Manual fields the bridge never auto-fills (full-text / eligibility / final).
MANUAL_FIELDS = ("other_sources", "assessed", "excluded_elig", "included", "reports")
# Auto fields derived from the ct-literature prisma block.
AUTO_FROM_STAGE = {
    "screened": "identified_records",
    "excluded_title": "excluded_records",
}

DISCLAIMER = (
    "⚠️ 机器初筛，非人工终审 / MACHINE SCREEN — NOT A SUBSTITUTE FOR HUMAN FINAL REVIEW.\n"
    "   ct-literature 的筛选为规则初筛（无 LLM），其 included_records 仅代表「通过标题/摘要\n"
    "   机器初筛的记录数」，而非「最终纳入 Meta 分析的研究数」。\n"
    "   - 标 [MANUAL] 的字段必须由人工补全后方可出图；\n"
    "   - assessed 的参考值来自机器初筛通过数，须人工确认全文评估数后再用；\n"
    "   - included 绝对不可由机器初筛数直接映射（否则产出方法学错误的流程图）。\n"
    "   This diagram is only as valid as the human-entered full-text / eligibility counts."
)


def _load_prisma(merged_path):
    with open(merged_path, encoding="utf-8") as f:
        data = json.load(f)
    prisma = data.get("prisma")
    if not isinstance(prisma, dict):
        raise SystemExit(
            "[ERROR] %s 不含 `prisma` 块。请先用 ct-literature 的 screen_prisma.py "
            "生成 PRISMA 初筛结果（或加 --prisma 重跑 ct_literature）。" % merged_path)
    return prisma


def _stage_count(prisma, stage_name):
    for s in prisma.get("stages", []):
        if s.get("stage") == stage_name:
            return int(s.get("count", 0))
    return None


def build_params(merged_path, manual=None, design="cinnamonMint"):
    """Return (params, mapping_report) for the meta-analysis prisma_flow task.

    `manual` is a dict of override values for MANUAL_FIELDS (or any field).
    """
    manual = dict(manual or {})
    prisma = _load_prisma(merged_path)

    identified = _stage_count(prisma, "identified_records") or 0
    excluded = _stage_count(prisma, "excluded_records") or 0
    included_machine = _stage_count(prisma, "included_records") or 0
    duplicates = prisma.get("duplicates_removed")

    params = {}
    mapping = {}

    # --- AUTO: derived without human judgement ---
    params["screened"] = identified
    mapping["screened"] = ("AUTO", "ct-literature identified_records (post-dedup total)")

    params["excluded_title"] = excluded
    mapping["excluded_title"] = ("AUTO", "ct-literature excluded_records (title/abstract)")

    if duplicates is not None:
        params["duplicates"] = int(duplicates)
        mapping["duplicates"] = ("AUTO", "ct-literature duplicates_removed (item-1 count)")
        params["records"] = identified + int(duplicates)
        mapping["records"] = ("AUTO", "identified_records + duplicates_removed (raw pre-dedup DB total)")
    else:
        params["duplicates"] = 0
        mapping["duplicates"] = ("MANUAL", "ct-literature 未报告 duplicates_removed；请人工补填")
        params["records"] = identified
        mapping["records"] = ("AUTO", "identified_records（缺 duplicates，尚未加回去，请人工核对 raw 总数）")

    # --- MANUAL: must be supplied by human review ---
    suggested_assessed = included_machine  # machine screen pass → entering full-text
    for fld in MANUAL_FIELDS:
        if fld in manual:
            params[fld] = int(manual[fld])
            mapping[fld] = ("MANUAL", "用户显式提供 (--manual/--set)")
        else:
            params[fld] = 0
            if fld == "assessed":
                mapping[fld] = ("MANUAL", "需人工填入全文评估数；参考值(机器初筛通过)=%d，须确认" % suggested_assessed)
            else:
                mapping[fld] = ("MANUAL", "需人工补全（全文/其他来源/最终纳入）")

    params["design"] = design
    return params, mapping, suggested_assessed


def render_report(params, mapping, suggested_assessed, merged_path):
    lines = []
    lines.append("=== PRISMA 字段桥接报告 / PRISMA field bridge report ===")
    lines.append("source: %s" % merged_path)
    lines.append("")
    lines.append("%-14s %-7s %-9s %s" % ("FIELD", "VALUE", "SOURCE", "NOTE"))
    lines.append("-" * 78)
    order = ["records", "other_sources", "duplicates", "screened", "excluded_title",
             "assessed", "excluded_elig", "included", "reports"]
    for fld in order:
        src, note = mapping.get(fld, ("?", ""))
        lines.append("%-14s %-7s %-9s %s" % (fld, params.get(fld, 0), src, note))
    lines.append("")
    if suggested_assessed:
        lines.append("参考：机器初筛通过数(included_records)=%d，可作为 assessed 初值，须人工确认全文评估数。"
                     % suggested_assessed)
    lines.append("")
    lines.append(DISCLAIMER)
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser(
        description="Bridge ct-literature .merged.json → meta-analysis prisma_flow params.")
    ap.add_argument("--merged", required=True, help="ct-literature .merged.json 路径")
    ap.add_argument("--manual", help="手动字段 JSON 文件，如 {\"assessed\":890,\"included\":42}")
    ap.add_argument("--set", action="append", default=[], metavar="field=value",
                    help="内联覆盖，可重复，如 --set assessed=890 --set included=42")
    ap.add_argument("--design", default="cinnamonMint", help="prisma_flow 配色方案")
    ap.add_argument("--out", default="prisma_flow_request.json",
                    help="输出请求信封 JSON（供 coze 端点 / 本地引擎消费）")
    args = ap.parse_args()

    manual = {}
    if args.manual:
        with open(args.manual, encoding="utf-8") as f:
            manual.update(json.load(f))
    for kv in args.set:
        if "=" not in kv:
            print("[WARN] 忽略非法 --set: %s" % kv); continue
        k, v = kv.split("=", 1)
        try:
            manual[k.strip()] = int(v.strip())
        except ValueError:
            manual[k.strip()] = v.strip()

    params, mapping, suggested = build_params(args.merged, manual=manual, design=args.design)
    envelope = {
        "task": "prisma_flow",
        "data": {},
        "params": params,
        "_bridge": {
            "source": "ct-literature .merged.json",
            "disclaimer": DISCLAIMER,
            "mapping": {k: v[0] for k, v in mapping.items()},
            "suggested_assessed_from_machine_screen": suggested,
        },
    }
    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(envelope, f, ensure_ascii=False, indent=2)

    print(render_report(params, mapping, suggested, args.merged))
    print("\n[OK] 请求信封已写出 -> %s" % args.out)
    # 若有 MANUAL 字段仍为空(0 且未显式提供)，提示用户
    blank = [k for k in MANUAL_FIELDS if params.get(k, 0) == 0 and k not in manual]
    if blank:
        print("[ACTION] 以下字段仍为 0（需人工补全后才能出图）: %s" % ", ".join(blank))


if __name__ == "__main__":
    main()
