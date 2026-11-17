#!/usr/bin/env python3
"""Stage 0 step 2 + 3: group the inventory into clusters and derive the report outline.

Grouping runs on three axes, in this order:
  1. business domain (fixed 10-domain taxonomy, decides which chapter a report lands in)
  2. time alignment (can these reports actually be compared side by side)
  3. metric overlap (which numbers must be cross-checked, who is the primary source)

Reports that fit nowhere are written to `unclustered` with a mandatory reason and
still get their own chapter. Nothing is ever dropped.

Usage:
    python cluster_reports.py --inventory report-inventory.json \
        --output-clusters report-clusters.json --output-chapter-plan chapter-plan.json
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from datetime import date, datetime, timezone
from pathlib import Path
from artifact_contract import native_stage_identity,validate_stage_identity

SCHEMA_VERSION = "2.0"

DOMAIN_ORDER = ["transaction", "traffic", "product", "content_live", "advertising",
                "service", "market", "asset", "finance", "unclassified"]

DOMAIN_LABEL = {
    "transaction": "交易与销售",
    "traffic": "流量与转化",
    "product": "商品与供给",
    "content_live": "内容与直播",
    "advertising": "投放与费用",
    "service": "客服与体验",
    "market": "市场大盘与竞争",
    "asset": "会员与私域资产",
    "finance": "成本与利润",
    "unclassified": "未归类",
}

DOMAIN_OWNER = {
    "transaction": "data-analyst",
    "traffic": "data-analyst",
    "product": "platform-ops",
    "content_live": "content-live-growth",
    "advertising": "ad-profit-optimizer",
    "service": "data-analyst",
    "market": "data-analyst",
    "asset": "platform-ops",
    "finance": "ad-profit-optimizer",
    "unclassified": "omni-ecom-team-lead",
}

GRANULARITY_RANK = {"transaction": 0, "daily": 1, "weekly": 2, "monthly": 3,
                    "quarterly": 4, "session": 5, "campaign": 5, "snapshot": 6, "unknown": 9}

DEFAULT_TOLERANCE_PCT = 5.0
OVERLAP_THRESHOLD = 0.8

SECTION_TEMPLATES = {
    "domain_analysis": [
        ("caliber_and_coverage", "口径与覆盖",
         "写明本章用到的报表编号、统计期间、统计粒度、指标定义、分母口径和剔污规则"),
        ("core_metrics", "核心指标",
         "按关键指标给出数值、环比同比和结构化拆解，只描述可核验证据"),
        ("cross_validation", "跨报表交叉验证",
         "逐条列出与印证源的对账结果、差异幅度和处置方式，差异超容差必须升级团长裁决"),
        ("judgment_and_action", "判断与行动",
         "给出经营判断、可执行动作、负责人、T+N、验收指标和停止条件"),
    ],
    "data_overview": [
        ("caliber_and_coverage", "报表清单",
         "逐份列出文件名、报表类型、业务域、平台、时间范围、粒度、记录数、完整度和可用性"),
        ("core_metrics", "归类结果",
         "列出每个归类的成员报表、归并依据、主源与印证源"),
        ("cross_validation", "章节与报表映射",
         "列出每个章节覆盖哪些报表、需要跨报表对比或交叉验证的内容"),
        ("judgment_and_action", "数据限制与补数要求",
         "列出数据不足的报表、对结论的影响范围和需要补充的数据清单"),
    ],
    "independent_observation": [
        ("caliber_and_coverage", "报表与口径",
         "说明这些报表为何无法与任何业务域归并，以及各自的统计口径"),
        ("core_metrics", "单独观察结果",
         "对每份报表单独给出可读取的事实，不做跨报表推断"),
        ("cross_validation", "暂不可交叉验证",
         "写明当前无法交叉验证的原因，以及补齐什么数据后可以归并"),
        ("judgment_and_action", "处置建议",
         "给出保留观察、补数后重跑或人工确认的建议"),
    ],
    "data_gap": [
        ("caliber_and_coverage", "缺口范围",
         "列出数据不足的报表编号、文件名和判定依据"),
        ("core_metrics", "对结论的影响",
         "逐条写明该缺口会让哪些结论失去支撑或降低置信度"),
        ("cross_validation", "可否用替代口径兜底",
         "说明是否存在替代口径或近似指标，以及兜底结论的置信度折损"),
        ("judgment_and_action", "补数要求",
         "写明需要补什么数据、找谁要、什么时间前拿到，拿不到时的降级处理方式"),
    ],
    "synthesis": [
        ("caliber_and_coverage", "口径汇总",
         "汇总全文使用的统一口径、权威来源顺序和已裁决冲突"),
        ("core_metrics", "核心结论",
         "一句话经营结论与核心问题排序"),
        ("cross_validation", "冲突裁决",
         "列出专家冲突、扫描结果、团长复算裁决和未被采纳观点的去向"),
        ("judgment_and_action", "行动清单",
         "按负责人、T+N、预期结果、验收指标、停止条件给出行动清单"),
    ],
}


def now_iso() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


def sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def parse_date(value):
    if not value:
        return None
    s = str(value).strip()
    for fmt in ("%Y-%m-%d", "%Y/%m/%d", "%Y-%m", "%Y/%m", "%Y%m%d", "%Y"):
        try:
            d = datetime.strptime(s, fmt).date()
            return d if fmt != "%Y" and fmt != "%Y-%m" and fmt != "%Y/%m" else d.replace(day=1)
        except ValueError:
            continue
    return None


def time_alignment(reports: list[dict]) -> tuple[dict, dict]:
    spans = []
    for r in reports:
        s, e = parse_date(r["time_scope"].get("start")), parse_date(r["time_scope"].get("end"))
        if s and e:
            spans.append((s, e))
    if not spans:
        return ({"aligned": False, "action": "无可用时间信息，统计期间需人工确认后再做同比",
                 "overlap_ratio": 0.0},
                {"start": None, "end": None, "granularity": "unknown", "aligned": False})
    if len(spans) == 1:
        s, e = spans[0]
        return ({"aligned": True, "action": "单份报表，无跨源对齐问题", "overlap_ratio": 1.0},
                {"start": s.isoformat(), "end": e.isoformat(),
                 "granularity": reports[0]["granularity"], "aligned": True})
    inter_start, inter_end = max(s for s, _ in spans), min(e for _, e in spans)
    union_start, union_end = min(s for s, _ in spans), max(e for _, e in spans)
    inter_days = max(0, (inter_end - inter_start).days)
    min_span = max(1, min((e - s).days for s, e in spans))
    ratio = round(min(1.0, inter_days / min_span), 4) if min_span else 0.0
    aligned = ratio >= OVERLAP_THRESHOLD
    action = ("各报表期间重叠度达标，按同一期间直接对比"
              if aligned else
              f"期间重叠仅 {ratio:.0%}，不做同期同比，改为各报表单列趋势观察，"
              f"必要时统一到最大公约粒度后比较")
    return ({"aligned": aligned, "action": action, "overlap_ratio": ratio},
            {"start": (inter_start if aligned else union_start).isoformat(),
             "end": (inter_end if aligned else union_end).isoformat(),
             "granularity": coarsest_granularity(reports), "aligned": aligned})


def coarsest_granularity(reports: list[dict]) -> str:
    grams = [r["granularity"] for r in reports if r["granularity"] != "unknown"]
    if not grams:
        return "unknown"
    return max(grams, key=lambda g: GRANULARITY_RANK.get(g, 9))


def pick_primary(candidates: list[dict]) -> dict:
    """Primary source = analyzable first, then largest row count, then confidence."""
    rank = {"high": 3, "medium": 2, "low": 1}
    return sorted(
        candidates,
        key=lambda r: (r["verdict"] == "analyzable", r["row_count"],
                       rank.get(r["confidence"], 0)),
        reverse=True,
    )[0]


def build_metrics(reports: list[dict]) -> tuple[list[dict], list[str]]:
    owners: dict[str, list[dict]] = {}
    for r in reports:
        for m in r["metrics"]:
            std = m["standard_name"]
            if m["aggregation"] == "unknown":
                continue
            owners.setdefault(std, []).append(r)
    metrics = []
    overlap = []
    for std, holders in owners.items():
        unit = ""
        for h in holders:
            for m in h["metrics"]:
                if m["standard_name"] == std and m.get("unit"):
                    unit = m["unit"]
                    break
            if unit:
                break
        primary = pick_primary(holders)
        others = [h["report_id"] for h in holders if h["report_id"] != primary["report_id"]]
        if len(holders) >= 2:
            overlap.append(std)
            rule = (f"以 {primary['report_id']} 为主源，用 {'、'.join(others)} 在同期同口径下复算"
                    f"「{std}」，差异超过 {DEFAULT_TOLERANCE_PCT}% 即升级为硬冲突，由团长亲跑数裁决")
        else:
            rule = f"仅 {primary['report_id']} 单源，无跨源印证，结论需标注为单源口径"
        metrics.append({
            "standard_name": std,
            "unit": unit,
            "primary_report_id": primary["report_id"],
            "corroborating_report_ids": others,
            "tolerance_pct": DEFAULT_TOLERANCE_PCT,
            "cross_check_rule": rule,
        })
    return metrics, overlap


def cluster_sufficiency(reports: list[dict]) -> tuple[str, str]:
    verdicts = {r["verdict"] for r in reports}
    if verdicts == {"insufficient"}:
        return "insufficient", "本类全部报表数据不足，只能说明缺口，不得输出经营结论"
    if "analyzable" not in verdicts:
        return "partial", "本类无完整可用报表，结论需标注置信度折损"
    if "partial" in verdicts or "insufficient" in verdicts:
        return "partial", "本类含部分可用报表，缺口部分须在数据缺口章节显式说明"
    return "sufficient", ""


def build_clusters(inventory: dict) -> tuple[list[dict], list[dict]]:
    groups: dict[str, list[dict]] = {}
    unclustered_reports: list[dict] = []
    for r in inventory["reports"]:
        if r["domain"] == "unclassified" or r["report_type"] == "unidentified":
            unclustered_reports.append(r)
            continue
        groups.setdefault(r["domain"], []).append(r)

    clusters = []
    seq = 0
    for domain in DOMAIN_ORDER:
        members = groups.get(domain)
        if not members:
            continue
        seq += 1
        cid = f"C{seq:02d}"
        align, tscope = time_alignment(members)
        metrics, overlap = build_metrics(members)
        suff, reason = cluster_sufficiency(members)
        cluster = {
            "cluster_id": cid,
            "domain": domain,
            "label": DOMAIN_LABEL[domain],
            "members": [m["report_id"] for m in members],
            "merge_basis": {
                "domain": f"全部成员业务域一致，均为「{DOMAIN_LABEL[domain]}」",
                "time_alignment": align,
                "metric_overlap": overlap,
            },
            "time_scope": tscope,
            "metrics": metrics,
            "sufficiency": suff,
        }
        if reason:
            cluster["sufficiency_reason"] = reason
        clusters.append(cluster)

    unclustered = []
    for r in unclustered_reports:
        if r["report_type"] == "unidentified":
            reason = "规则库与模型均未判定出报表类型，无法并入任何业务域"
        else:
            reason = (f"业务域为 unclassified，现有 9 个业务域无法容纳该报表"
                      f"（类型：{r.get('report_type_label', r['report_type'])}）")
        unclustered.append({
            "report_id": r["report_id"],
            "file_name": r["file_name"],
            "reason": reason,
            "planned_placement": "independent_observation_chapter",
        })
    return clusters, unclustered


def gap_entry(r: dict) -> dict:
    reason = r.get("verdict_reason") or "判定为数据不足"
    impact = {
        "insufficient": f"该报表无法支撑任何量化结论，涉及 {r.get('report_type_label', '本')} 的判断必须降级为待验证假设",
        "partial": f"该报表可支撑部分结论，涉及 {r.get('report_type_label', '本')} 的量化判断需标注置信度折损",
    }.get(r["verdict"], "该报表可用性存疑，相关结论需标注置信度")
    remedy = {
        "insufficient": "需重新导出完整期间原始数据，或补充该业务域的替代报表后重跑",
        "partial": "需补齐缺失字段或缺失期间的导出，缺失补齐前结论按局部口径呈现",
    }.get(r["verdict"], "需人工确认数据可用性后重跑")
    return {"report_id": r["report_id"], "file_name": r["file_name"],
            "reason": reason, "impact": impact, "remedy": remedy}


def build_chapter(inventory: dict, clusters: list[dict], unclustered: list[dict]) -> dict:
    reports = {r["report_id"]: r for r in inventory["reports"]}
    chapters = []
    covered: list[str] = []

    def new_chapter(index: int, kind: str, title: str, cluster_ids, report_ids,
                    owner: str, caliber: dict, key_metrics, cross_val, gaps):
        sections = [{"section_key": k, "title": t, "requirement": req}
                    for k, t, req in SECTION_TEMPLATES[kind]]
        ch = {
            "chapter_index": index,
            "chapter_id": f"CH{index:02d}",
            "title": title,
            "chapter_kind": kind,
            "source_cluster_ids": cluster_ids,
            "source_report_ids": report_ids,
            "owner_agent": owner,
            "caliber": caliber,
            "key_metrics": key_metrics,
            "sections": sections,
        }
        if cross_val is not None:
            ch["cross_validation"] = cross_val
        if gaps is not None:
            ch["data_gaps"] = gaps
        return ch

    # CH00 data overview always first
    all_ids = [r["report_id"] for r in inventory["reports"]]
    chapters.append(new_chapter(
        0, "data_overview", "数据概览", [], all_ids, "omni-ecom-team-lead",
        {"metric_definitions": ["逐份报表的原始指标名与标准化指标名对照"],
         "denominator": "不涉及计算，仅说明每份报表的覆盖范围与可用性",
         "exclusion_rules": ["不剔除任何报表，未归类的报表也必须在清单中列出"],
         "time_alignment": "按各报表自身期间分别标注，不做统一对齐"},
        ["report_count", "coverage_rate"], None, None))
    covered.extend(all_ids)

    # domain chapters
    idx = 0
    for c in clusters:
        idx += 1
        members = [reports[rid] for rid in c["members"] if rid in reports]
        key_metrics = [m["standard_name"] for m in c["metrics"][:8]]
        cross_val = []
        for m in c["metrics"]:
            for rid in m["corroborating_report_ids"]:
                cross_val.append({
                    "target_report_id": rid,
                    "metric": m["standard_name"],
                    "rule": m["cross_check_rule"],
                    "tolerance_pct": m["tolerance_pct"],
                    "on_mismatch": "由团长亲跑数裁决，裁决前不得写入最终结论",
                })
        gaps = [gap_entry(r) for r in members if r["verdict"] != "analyzable"]
        caliber = {
            "metric_definitions": [
                f"{m['standard_name']}（{m['unit'] or '无单位'}）：主源 {m['primary_report_id']}"
                + (f"，印证源 {'、'.join(m['corroborating_report_ids'])}"
                   if m["corroborating_report_ids"] else "，无印证源")
                for m in c["metrics"][:10]
            ],
            "denominator": f"以 {c['members'][0]} 的统计口径为准，跨报表对比前先对齐"
                           f"{c['time_scope']['granularity']} 粒度与{c['time_scope']['start']}至{c['time_scope']['end']}期间",
            "exclusion_rules": [
                "先做异常单剔污再归因，剔污前后结论不一致时以剔污后为准",
                "访客口径不得混用：店铺去重访客做分母，SPU 层访客只用于占比",
                "UV 价值与 ROI 必须用搜索渠道口径，不得用全店口径",
            ],
            "time_alignment": c["merge_basis"]["time_alignment"]["action"],
        }
        chapters.append(new_chapter(
            idx, "domain_analysis", f"{c['label']}分析", [c["cluster_id"]],
            list(c["members"]), DOMAIN_OWNER.get(c["domain"], "omni-ecom-team-lead"),
            caliber, key_metrics, cross_val, gaps))
        covered.extend(c["members"])

    # independent observation chapter for unclustered reports
    if unclustered:
        idx += 1
        uids = [u["report_id"] for u in unclustered]
        gaps = [gap_entry(reports[r]) for r in uids if reports[r]["verdict"] != "analyzable"]
        chapters.append(new_chapter(
            idx, "independent_observation", "独立观察：未归类报表", [], uids,
            "omni-ecom-team-lead",
            {"metric_definitions": ["按各报表自身列定义，不做跨报表统一"],
             "denominator": "各报表独立，不设统一分母",
             "exclusion_rules": ["不得与已归类报表做合并计算"],
             "time_alignment": "各报表期间独立标注"},
            [], [], gaps))
        covered.extend(uids)

    # data gap chapter
    gap_reports = [r for r in inventory["reports"] if r["verdict"] != "analyzable"]
    if gap_reports:
        idx += 1
        chapters.append(new_chapter(
            idx, "data_gap", "数据缺口与限制", [],
            [r["report_id"] for r in gap_reports], "omni-ecom-team-lead",
            {"metric_definitions": ["本列缺口涉及的全部指标"],
             "denominator": "不适用，本章说明不可计算的部分",
             "exclusion_rules": ["缺口部分不得用推测值填充"],
             "time_alignment": "按各缺口报表的原始期间标注"},
            [], [], [gap_entry(r) for r in gap_reports]))

    # synthesis chapter
    idx += 1
    chapters.append(new_chapter(
        idx, "synthesis", "综合结论与行动清单", [], [], "omni-ecom-team-lead",
        {"metric_definitions": ["沿用各章节已锁定的指标口径"],
         "denominator": "沿用各章节已锁定的分母口径",
         "exclusion_rules": ["综合章节不得引入前面章节未核验证据的新数字"],
         "time_alignment": "沿用各章节的时间对齐结论"},
        [], [], None))

    total = inventory["report_count"]
    covered_unique = sorted(set(covered))
    plan = {
        **native_stage_identity("chapter_plan", inventory["team_version"]),
        "run_id": inventory["run_id"],
        "client_scope": inventory["client_scope"],
        "team_version": inventory["team_version"],
        "cluster_sha256": "",
        "issued_at": now_iso(),
        "chapters": chapters,
        "coverage_plan": {
            "total_reports": total,
            "covered_report_ids": covered_unique,
            "uncovered_report_ids": sorted(set(all_ids) - set(covered_unique)),
            "coverage_rate": round(len(covered_unique) / total, 4) if total else 0.0,
            "data_overview_chapter_id": "CH00",
            "data_gap_chapter_id": next(
                (c["chapter_id"] for c in chapters if c["chapter_kind"] == "data_gap"), None),
        },
    }
    return plan


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Stage 0 step 2+3: cluster reports and plan chapters")
    ap.add_argument("--inventory", required=True)
    ap.add_argument("--output-clusters", required=True)
    ap.add_argument("--output-chapter-plan", required=True)
    args = ap.parse_args(argv)

    inv_path = Path(args.inventory)
    if not inv_path.exists():
        print(json.dumps({"status": "inventory_missing", "path": str(inv_path)}, ensure_ascii=False))
        return 2
    raw = inv_path.read_bytes()
    inventory = json.loads(raw.decode("utf-8"))
    validate_stage_identity(inventory,"report_inventory",inventory.get("team_version"),
                            inventory.get("run_id"),inventory.get("client_scope"))

    clusters, unclustered = build_clusters(inventory)
    cluster_doc = {
        **native_stage_identity("report_clusters", inventory["team_version"]),
        "run_id": inventory["run_id"],
        "client_scope": inventory["client_scope"],
        "team_version": inventory["team_version"],
        "inventory_sha256": sha256_bytes(raw),
        "issued_at": now_iso(),
        "merge_rules": {
            "domain_axis": "先按 10 个固定业务域归并，业务域决定章节归属",
            "time_axis": f"再算期间重叠度，重叠率 ≥ {OVERLAP_THRESHOLD:.0%} 才允许同期同比，否则单列趋势",
            "metric_axis": "最后取指标交集，交集指标指定主源与印证源，生成交叉验证项",
            "tie_break": "主源优先取 verdict=analyzable，其次记录数最多，再次识别置信度最高",
            "overlap_threshold": OVERLAP_THRESHOLD,
        },
        "cluster_count": len(clusters),
        "clusters": clusters,
        "unclustered": unclustered,
    }
    cpath = Path(args.output_clusters)
    cpath.parent.mkdir(parents=True, exist_ok=True)
    cpath.write_text(json.dumps(cluster_doc, ensure_ascii=False, indent=2), encoding="utf-8")

    plan = build_chapter(inventory, clusters, unclustered)
    plan["cluster_sha256"] = sha256_bytes(cpath.read_bytes())
    ppath = Path(args.output_chapter_plan)
    ppath.parent.mkdir(parents=True, exist_ok=True)
    ppath.write_text(json.dumps(plan, ensure_ascii=False, indent=2), encoding="utf-8")

    print(json.dumps({
        "status": "chapter_plan_ready",
        "cluster_count": len(clusters),
        "unclustered_count": len(unclustered),
        "chapter_count": len(plan["chapters"]),
        "coverage_rate": plan["coverage_plan"]["coverage_rate"],
        "uncovered": plan["coverage_plan"]["uncovered_report_ids"],
        "clusters": str(cpath.resolve()),
        "chapter_plan": str(ppath.resolve()),
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
