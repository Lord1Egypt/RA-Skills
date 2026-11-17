"""run —— 编排入口。

流水线（顺序即接口约束）：
load → pick_sheet → detect_header → normalize → classify_rows → recognize
→ build_tasks → quality → hours_protection → assess → compute_levels
→ score → selfcheck → branch → report
"""
from __future__ import annotations

import argparse
import copy
import json
import sys
import traceback
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import excel_io as X
import excel_out as EO
import field_recognize as F
import params as P
import quality_stats as S
import report as R
import score as SC

SCORED_FIELDS = {"difficulty", "hours", "money", "risk", "quality", "priority",
                 "urgency", "collab", "reuse", "strategy", "innovation", "skill"}


# ============================================================ 任务构建
def _cell(matrix, r, c):
    if r < 0 or r >= len(matrix):
        return None
    row = matrix[r]
    if c < 0 or c >= len(row):
        return None
    return row[c]


def _col_index(colmap):
    return {c["mapped_to"]: c["col_idx"] - 1 for c in colmap["columns"]}


def _deadline_level(d):
    if not d:
        return None
    days = (d - date.today()).days
    if days <= 3:
        return 5
    if days <= 7:
        return 4
    if days <= 14:
        return 3
    if days <= 30:
        return 2
    return 1


def build_tasks(matrix, header, labels, colmap, sheet, unit_hint_from_header):
    cols = _col_index(colmap)
    n_cols = len(matrix[0]) if matrix else 0

    data_rows = [r for r, lab in sorted(labels.items()) if lab["label"] == "DATA"]
    default_unit = {"factor": P.HOURS_PER_MANDAY, "source": "none",
                    "confidence": 0.0, "note": "无工时列或无数据行"}
    if not data_rows:
        return [], [], default_unit

    # ---------- 难度文本源：任务名 + 描述/备注类文本列
    # 说明：难度关键词只从任务名匹配时命中率极低（实测媒体运维类表仅 6%），
    # 备注/说明列往往才是难度的真实载体。故把「未映射的长文本列」也纳入匹配源。
    # 判定为长文本列：该列数据行中，文本长度 >= 8 的非空值占比 >= 50%。
    mapped_idx = set(cols.values())
    text_cols = []
    for c in range(n_cols):
        if c in mapped_idx:
            continue
        vals = [X.norm_str(_cell(matrix, r, c)) for r in data_rows]
        vals = [v for v in vals if v]
        if not vals:
            continue
        if sum(1 for v in vals if len(v) >= 8) / len(vals) >= 0.5:
            text_cols.append(c)

    # ---------- pass 1：逐行原样抽取
    records = []
    skipped = []
    for r in data_rows:
        name = _cell(matrix, r, cols.get("task_name", -1))
        if X.is_null(name):
            skipped.append({"row_id": r + 1, "reason": "empty_task_name",
                            "raw": [X.norm_str(v) for v in matrix[r][:5]]})
            continue
        records.append({"row": r, "task_name": X.norm_str(name)})

    # ---------- 工时单位判定（三来源）
    hours_col = cols.get("hours")
    unit_resolution = default_unit
    bare_values, anchors = [], []

    if hours_col is not None and hours_col >= 0:
        prelim = []
        for rec in records:
            p = F.parse_hours_cell(_cell(matrix, rec["row"], hours_col), default_factor=None)
            prelim.append(p)
            if p.get("pending") is not None:
                bare_values.append(p["pending"])
            elif p.get("value") is not None:
                bare_values.append(p["value"])

        # 日期锚点：需要起止日期
        sc_col, ec_col = cols.get("start_date"), cols.get("end_date")
        for rec, p in zip(records, prelim):
            if sc_col is None or ec_col is None:
                continue
            s = F.parse_date_value(_cell(matrix, rec["row"], sc_col))
            e = F.parse_date_value(_cell(matrix, rec["row"], ec_col))
            if not (s and e):
                continue
            days = (e - s).days + 1
            if days <= 0:
                continue
            avail = days * P.HOURS_PER_MANDAY * P.WORKDAY_FACTOR
            raw_h = p.get("pending") if p.get("pending") is not None else p.get("value")
            if raw_h:
                anchors.append((raw_h, avail))

        hdr_name = ""
        for c in colmap["columns"]:
            if c["mapped_to"] == "hours":
                hdr_name = c["raw_name"]
                break
        unit_hint = unit_hint_from_header
        for c in colmap["columns"]:
            if c["mapped_to"] == "hours" and c.get("unit_hint"):
                unit_hint = c["unit_hint"]
        unit_resolution = F.resolve_hours_unit(
            hdr_name, unit_hint, sheet.get("col_formats", {}).get(hours_col + 1),
            bare_values, anchors,
        )
        factor = unit_resolution["factor"]
        for rec, p in zip(records, prelim):
            if p.get("pending") is not None:
                rec["hours"] = {"value": round(p["pending"] * factor, 4),
                                "estimated": p["estimated"], "ok": True}
            elif p.get("value") is not None:
                rec["hours"] = {"value": p["value"], "estimated": p["estimated"], "ok": True}
            else:
                rec["hours"] = {"value": None, "estimated": False, "ok": False}

    # ---------- 金额列单位
    money_mult = 1.0
    for c in colmap["columns"]:
        if c["mapped_to"] == "money":
            uh = (c.get("unit_hint") or "") + (c["raw_name"] or "")
            if "亿" in uh:
                money_mult = 1e8
            elif "百万" in uh:
                money_mult = 1e6
            elif "万" in uh:
                money_mult = 1e4
            elif "千" in uh:
                money_mult = 1e3

    # ---------- pass 2：逐字段解析
    tasks_raw = []
    for rec in records:
        r = rec["row"]
        vals = {}

        if hours_col is not None:
            h = rec.get("hours") or {}
            vals["hours"] = {"raw": _cell(matrix, r, hours_col),
                             "parsed": h.get("value"), "level": None,
                             "estimated": h.get("estimated", False), "flags": []}

        if "money" in cols:
            m = F.parse_money_cell(_cell(matrix, r, cols["money"]), money_mult)
            vals["money"] = {"raw": m["raw"], "parsed": m["value"], "level": None,
                             "estimated": False, "flags": (
                                 ["currency_foreign"] if m.get("currency_foreign") else [])}

        # 难度：优先专列，其次任务名/交付物关键词（纯脚本规则，无模型）
        diff_level, diff_est, diff_ev = None, False, []
        if "difficulty" in cols:
            lv, est = F.parse_level_value(_cell(matrix, r, cols["difficulty"]))
            if lv is not None:
                diff_level, diff_est, diff_ev = lv, est, ["表内难度等级列"]
        if diff_level is None:
            # 一级源：任务名（+交付物列）
            src1 = rec["task_name"]
            if "reuse" in cols:
                v = _cell(matrix, r, cols["reuse"])
                if not X.is_null(v):
                    src1 += " " + X.norm_str(v)
            kw_level, hits = F.difficulty_from_keywords(src1)
            if kw_level is not None:
                diff_level, diff_est, diff_ev = kw_level, True, hits
            else:
                # 二级源：描述/备注类长文本列。
                # 必须分源而非拼接：备注越长混入低档词的概率越高，
                # 而「命中多档取最低档」会把任务名的高档判据整体拖低
                # （实测「微信分享统一网关开发」被备注里的「调整」拖成 2 档）。
                src2 = " ".join(X.norm_str(_cell(matrix, r, c))
                                for c in text_cols
                                if not X.is_null(_cell(matrix, r, c)))
                if src2.strip():
                    kw2, hits2 = F.difficulty_from_keywords(src2)
                    if kw2 is not None:
                        diff_level, diff_est, diff_ev = kw2, True, [f"描述:{h}" for h in hits2]
        if diff_level is not None:
            vals["difficulty"] = {"raw": _cell(matrix, r, cols.get("difficulty", -1)),
                                  "parsed": diff_level, "level": diff_level,
                                  "estimated": diff_est,
                                  "flags": ["qualitative"] if diff_est else [],
                                  "evidence": diff_ev}

        if "risk" in cols:
            lv, est = F.parse_level_value(_cell(matrix, r, cols["risk"]))
            if lv is not None:
                vals["risk"] = {"raw": _cell(matrix, r, cols["risk"]), "parsed": lv,
                                "level": lv, "estimated": est, "flags": []}

        # 紧迫性：优先级 > 截止日期
        urg_level, urg_src = None, None
        if "priority" in cols:
            lv, _ = F.parse_level_value(_cell(matrix, r, cols["priority"]), kind="priority")
            if lv is not None:
                urg_level, urg_src = lv, "priority"
        if urg_level is None and "urgency" in cols:
            d = F.parse_date_value(_cell(matrix, r, cols["urgency"]))
            lv = _deadline_level(d)
            if lv is not None:
                urg_level, urg_src = lv, "deadline"
        if urg_level is not None:
            vals["urgency"] = {"raw": _cell(matrix, r, cols.get("priority", cols.get("urgency", -1))),
                               "parsed": urg_level, "level": urg_level,
                               "estimated": False, "flags": [urg_src]}

        if "quality" in cols:
            q = F.parse_quality_level(_cell(matrix, r, cols["quality"]))
            if q is not None:
                vals["quality"] = {"raw": _cell(matrix, r, cols["quality"]), "parsed": q,
                                   "level": q, "estimated": False, "flags": []}

        if "collab" in cols:
            cnt = F.parse_count_value(_cell(matrix, r, cols["collab"]))
            if cnt is not None:
                vals["collab"] = {"raw": _cell(matrix, r, cols["collab"]), "parsed": cnt,
                                  "level": None, "estimated": False, "flags": []}

        # J 复用价值：三档枚举（5/3/1）。只在表里有交付物列时才尝试（无列即不开该维度）
        if "reuse" in cols:
            cell = _cell(matrix, r, cols["reuse"])
            cell_s = "" if X.is_null(cell) else X.norm_str(cell)
            j_level, j_word = F.reuse_from_text((cell_s + " " + rec["task_name"]).strip())
            if j_level is not None:
                vals["reuse"] = {"raw": cell, "parsed": j_level, "level": j_level,
                                 "estimated": True, "flags": ["qualitative"],
                                 "evidence": [f"命中「{j_word}」→{j_level}档"]}

        # 日期
        start = F.parse_date_value(_cell(matrix, r, cols["start_date"])) if "start_date" in cols else None
        end = F.parse_date_value(_cell(matrix, r, cols["end_date"])) if "end_date" in cols else None
        deadline = F.parse_date_value(_cell(matrix, r, cols["urgency"])) if "urgency" in cols else None

        meta = {"start": start.isoformat() if start else None,
                "end": end.isoformat() if end else None,
                "deadline": deadline.isoformat() if deadline else None}
        if start and end and end >= start:
            meta["natural_days"] = (end - start).days + 1

        tasks_raw.append({
            "row": r, "task_name": rec["task_name"], "values": vals, "meta": meta,
            "flags": [], "parent_ref": (
                X.norm_str(_cell(matrix, r, cols["parent"])) if "parent" in cols else None),
        })

    return tasks_raw, skipped, unit_resolution


def aggregate_merged(tasks_raw, colmap, fill_map):
    """按纵向合并锚点聚合：工时/金额求和，等级取最大。"""
    cols = _col_index(colmap)
    tc = cols.get("task_name", -1)

    keyed = {}
    for t in tasks_raw:
        key = t["row"]
        if tc >= 0:
            info = fill_map.get((t["row"], tc))
            if info and info["span_rows"] > 1:
                key = info["anchor"][0]
        keyed.setdefault(key, []).append(t)

    merged = []
    for key in sorted(keyed):
        group = keyed[key]
        if len(group) == 1:
            merged.append(group[0])
            continue
        base = group[0]
        base = {**base, "values": copy.deepcopy(base["values"]), "meta": dict(base["meta"])}
        for dim in list(base["values"].keys()):
            items = [g["values"].get(dim) for g in group if g["values"].get(dim)]
            if not items:
                continue
            if dim in ("hours", "money", "collab"):
                total = sum((i.get("parsed") or 0) for i in items)
                base["values"][dim] = {**items[0], "parsed": round(total, 4),
                                       "raw": "+".join(str(i.get("raw")) for i in items)}
            else:
                best = max(items, key=lambda i: i.get("level") or 0)
                base["values"][dim] = dict(best)
        base["flags"] = list({f for g in group for f in g.get("flags", [])}) + ["merged_group"]
        if base["meta"].get("natural_days"):
            base["meta"]["natural_days"] = max(g["meta"].get("natural_days") or 0 for g in group)
        merged.append(base)
    return merged


def assign_ids(tasks):
    for i, t in enumerate(tasks, 1):
        t["task_id"] = f"T{i:04d}"
    return tasks


def dedupe(tasks):
    seen, out, dups = set(), [], []
    for t in tasks:
        key = (t["task_name"],
               str((t["values"].get("hours") or {}).get("parsed")),
               str((t["values"].get("money") or {}).get("parsed")))
        if key in seen:
            dups.append(t["task_id"])
            continue
        seen.add(key)
        out.append(t)
    return out, dups


# ============================================================ 主流水线
def pipeline(path: Path, baseline_path: Path | None, overrides: list | None = None,
             force_points: bool = False) -> dict:
    bundle = X.load(path)
    pick = X.pick_sheet(bundle, F.probe_row)
    sheet = pick["sheet"]
    header = X.detect_header(sheet, F.probe_row)
    matrix, fill_map = X.apply_merges(sheet)
    blocks = X.detect_blocks(matrix)   # 必须传合并展开后的矩阵

    excluded = []
    default_unit = {"factor": P.HOURS_PER_MANDAY, "source": "none",
                    "confidence": 0.0, "note": "无工时列或无数据行"}

    if len(blocks) >= 2:
        # ---------- 多区块表：每个区块独立识别表头与列，再合并任务
        # 依据：个人月度考核表常见「区块标题 → 独立表头 → 数据」重复结构，
        # 单表头解析会漏掉其余区块的任务，并把月评/计划/意见栏当成任务计入。
        headers, colmap, tasks_raw = None, None, []
        unit_resolution = default_unit
        for bi, blk in enumerate(blocks):
            bh = {"row_index": blk["header_row"], "row_span": 1, "unit_row": None,
                  "unit_hint": None, "confidence": 0.8,
                  "detected_by": "multi_block", "data_start": blk["header_row"] + 1}
            bhds = X.build_headers(matrix, bh)
            blabs_all = X.classify_rows(matrix, bh, bhds)
            blabs = {}
            for r, lab in blabs_all.items():
                if not (blk["header_row"] < r <= blk["end"]):
                    continue
                if lab["label"] != "DATA":
                    continue
                if X.is_non_task_row(matrix[r]):
                    excluded.append({"row_id": r + 1, "reason": "non_task_row",
                                     "raw": [X.norm_str(v) for v in matrix[r][:4]
                                             if not X.is_null(v)]})
                    continue
                blabs[r] = lab
            if not blabs:
                continue
            bsamples = []
            for c in range(len(bhds)):
                vals = [_cell(matrix, r, c) for r in sorted(blabs)[:60]]
                bsamples.append([v for v in vals if not X.is_null(v)][:20])
            bcm = F.recognize(bhds, bsamples)
            if overrides:
                bcm = F.apply_override(bcm, overrides, len(bhds))
            if colmap is None:
                colmap, headers = bcm, bhds
            braw, bskip, bunit = build_tasks(matrix, bh, blabs, bcm, sheet, None)
            if bunit.get("source") != "none":
                unit_resolution = bunit
            for t in braw:
                t["block"] = bi
            tasks_raw.extend(braw)
            excluded.extend(bskip)
        if colmap is None:
            colmap, headers = {"columns": [], "unmapped": []}, []
    else:
        headers = X.build_headers(matrix, header)
        labels = X.classify_rows(matrix, header, headers)

        # 列采样
        data_starts = [r for r, lab in labels.items() if lab["label"] == "DATA"]
        samples = []
        for c in range(len(headers)):
            vals = [_cell(matrix, r, c) for r in data_starts[:60]]
            samples.append([v for v in vals if not X.is_null(v)][:20])

        colmap = F.recognize(headers, samples)
        if overrides:
            colmap = F.apply_override(colmap, overrides, len(headers))

        for r, lab in sorted(labels.items()):
            if lab["label"] != "DATA":
                excluded.append({"row_id": r + 1, "reason": lab.get("reason") or lab["label"],
                                 "raw": [X.norm_str(v) for v in matrix[r][:6] if not X.is_null(v)]})
        for r, lab in sorted(labels.items()):
            if lab["label"] == "DATA" and lab.get("suspicious_total"):
                excluded.append({"row_id": r + 1, "reason": "suspect_total_not_removed",
                                 "raw": [X.norm_str(v) for v in matrix[r][:6] if not X.is_null(v)]})

        tasks_raw, skipped, unit_resolution = build_tasks(
            matrix, header, labels, colmap, sheet, header.get("unit_hint"))
        excluded.extend(skipped)

    tasks = aggregate_merged(tasks_raw, colmap, fill_map)
    tasks = assign_ids(tasks)
    tasks, dup_ids = dedupe(tasks)

    # 层级：可加性自检判容器父任务（父 ≈ Σ子 → 父不计分，防重复计分）
    hierarchy = F.resolve_hierarchy(tasks)

    # 质检（门槛检查在打分之前）
    quality = S.check(bundle, header, colmap, tasks, excluded, len(matrix))

    payload = {
        "meta": {
            "file": Path(bundle["path"]).name,
            "file_format": bundle["format"],
            "encoding": bundle.get("encoding"),
            "sheet": sheet["name"],
            "sheet_candidates": pick["candidates"],
            "batch_id": Path(bundle["path"]).stem,
            "parsed_at": date.today().isoformat(),
            "skill_version": "2.1.0",
        },
        "header": {k: header[k] for k in
                   ("row_index", "row_span", "unit_row", "unit_hint",
                    "confidence", "detected_by", "data_start")},
        "columns": colmap["columns"],
        "unmapped_columns": colmap["unmapped"],
        "arbitration_log": colmap["arbitration_log"],
        "dropped_duplicate_columns": colmap.get("dropped_duplicate_columns", []),
        "quality": quality,
        "caliber_freeze": {
            "hours_per_manday": P.HOURS_PER_MANDAY,
            "workday_factor": P.WORKDAY_FACTOR,
            "week_hours": P.WEEK_HOURS,
            "month_hours": P.MONTH_HOURS,
            "hours_deviation_factor": P.HOURS_DEVIATION_FACTOR,
            "holiday_calendar_applied": P.HOLIDAY_CALENDAR_APPLIED,
        },
        "unit_resolution": {},
        "status": "failed" if quality["blockers"] else "ok",
    }

    if quality["blockers"]:
        payload["blockers"] = quality["blockers"]
        payload["tasks"] = []
        payload["batch_assessment"] = {}
        payload["selfcheck"] = {}
        payload["insurance_note"] = []
        return payload

    # 日期锚点 & 可用工时
    S.compute_avail_hours(tasks)
    date_anchor_available = any(t["meta"].get("avail_hours") for t in tasks)
    hp = S.apply_hours_protection(tasks, colmap)

    # 批次评级（必须在打分之前）
    assessment = S.assess(colmap, tasks, quality)

    # 分档
    band_info = S.compute_levels(tasks, assessment["enabled_dims"])

    # 自检
    checks = S.selfcheck(tasks, assessment)
    checks["hours_protection"] = hp
    checks["banding"] = band_info
    baseline = S.load_baseline(baseline_path) if baseline_path else None
    checks["baseline_compare"] = S.compare_baseline(tasks, baseline, payload["caliber_freeze"])

    # 分支判定（0→4 优先级，命中即停）
    n = len(tasks)
    branch = "A_NORMAL"
    if n < P.MIN_TASKS or assessment["weight_total"] < P.COVERAGE_RANK:
        branch = "C_DESCRIPTIVE"
    else:
        deg = checks["degeneracy"]
        rc = deg.get("rank_consistency_AB")
        if (assessment["n_eff"] < P.N_EFF_MIN
                or (rc is not None and rc > P.RANK_CONSISTENCY_MAX)
                or len(assessment["weight_normalized"]) <= 2):
            branch = "D_DEGENERATE"
        elif (assessment["weight_total"] < P.COVERAGE_NORMAL
              or assessment["max_single_weight"] > P.WEIGHT_CONCENTRATION
              or not date_anchor_available):
            branch = "B_DEGRADED"
    assessment["branch"] = branch

    # 打分（工时防护结果作为 K_偏离 的证据来源传入）
    result = SC.compute(tasks, assessment, hours_protection=hp, force_points=force_points)
    total_in = result["summary"]["n_scored"] + result["summary"]["n_out"]
    out_ratio = result["summary"]["n_out"] / total_in if total_in else 0.0
    if out_ratio > 0.50 and branch != "C_DESCRIPTIVE":
        branch = "C_DESCRIPTIVE"
        assessment["branch"] = branch

    # 合并明细供报告使用
    by_id = {t["task_id"]: t for t in tasks}
    for rec in result["tasks"]:
        src = by_id.get(rec["task_id"], {})
        vals = src.get("values", {})
        # 原表行号/区块：仅用于结果表回溯定位，不参与任何计算
        if src.get("row") is not None:
            rec["row"] = src["row"]
        if src.get("block") is not None:
            rec["block"] = src["block"]
        rec["values"] = vals
        rec["hours_effective"] = (vals.get("hours") or {}).get("effective",
                                   (vals.get("hours") or {}).get("parsed"))
        rec["hours_raw"] = (vals.get("hours") or {}).get("parsed")
        rec["money"] = (vals.get("money") or {}).get("parsed")
        rec["difficulty_level"] = (vals.get("difficulty") or {}).get("level")
        rec["difficulty_evidence"] = (vals.get("difficulty") or {}).get("evidence") or []
        rec["urgency_level"] = (vals.get("urgency") or {}).get("level")
        rec["reuse_level"] = (vals.get("reuse") or {}).get("level")

    payload["tasks"] = result["tasks"]
    payload["frozen_tasks"] = result["frozen_tasks"]
    payload["discounted_tasks"] = result["discounted_tasks"]
    payload["totals"] = result["summary"]
    payload["hierarchy"] = {**hierarchy,
                            "containers_detail": result["container_tasks"]}
    payload["batch_assessment"] = assessment
    payload["selfcheck"] = checks
    payload["unit_resolution"] = {"hours": unit_resolution}
    payload["date_anchor_available"] = date_anchor_available
    payload["a_method"] = {
        "method": "keyword_rule_table",
        "table_size": sum(len(words) for _, words in P.A_KEYWORD_TABLE),
        "exclude_words": len(P.A_EXCLUDE_WORDS),
        "min_hit_rate": P.A_KEYWORD_MIN_HIT_RATE,
        "hit_rate": (assessment["coverage_by_dim"] or {}).get("difficulty"),
        "note": ("A 为关键词规则映射（剥离排除词 → 最长匹配去重 → 取最低档），全程无模型判断；"
                 "命中依据逐条记在任务的 difficulty_evidence 里"),
    }
    diff_col = any(c["mapped_to"] == "difficulty" for c in colmap["columns"])
    payload["difficulty_qualitative"] = (not diff_col) or any(
        "qualitative" in (t["values"].get("difficulty", {}).get("flags") or []) for t in tasks)
    payload["a_estimate"] = checks.get("a_estimate")
    payload["manual_override"] = {
        "used": bool(overrides),
        "applied": list(overrides or []),
        "howto": ("如需人工强制指定列映射（本流程唯一的人工介入点），加参数重跑：\n"
                  "  python run.py 你的文件.xlsx --override 3=hours --override 5=money\n"
                  "列号从 1 开始（对应报告「字段识别明细」的列号），字段名可选："
                  + "、".join(sorted(F.FIELD_SPEC))),
    }
    payload["insurance_note"] = R.build_insurance(payload)
    if force_points and branch in ("C_DESCRIPTIVE", "D_DEGENERATE"):
        payload["insurance_note"].append(
            f"⚠ 已按 --force-points 强制输出工分：本批维度覆盖度仅 "
            f"{assessment['weight_total']:.0f}%、有效自由度 {assessment['n_eff']:.2f}，"
            f"未达分配门槛。工分仅作相对参考，**不建议直接用于价值分配**；"
            f"补齐工时/优先级等字段后重跑可提升可信度。")
    payload["baseline"] = {
        "run_id": payload["meta"]["parsed_at"],
        "n_tasks": n,
        "mean_hours": round(
            sum((t["values"].get("hours") or {}).get("parsed") or 0 for t in tasks) / max(n, 1), 4),
        "caliber_freeze": payload["caliber_freeze"],
        "tier_dist": {dim: ((checks["skew"].get(dim) or {}).get("dist"))
                      for dim in assessment["enabled_dims"]},
    }
    payload["status"] = "ok" if branch == "A_NORMAL" else "degraded"
    return payload


# ============================================================ CLI
def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="工分计算：解析 Excel 任务清单并输出事实清单")
    ap.add_argument("file", help="Excel/CSV 路径")
    ap.add_argument("--out-dir", default=None, help="输出目录（默认与输入同目录）")
    ap.add_argument("--json", default=None, help="中间 JSON 输出路径")
    ap.add_argument("--md", default=None, help="Markdown 报告输出路径")
    ap.add_argument("--xlsx", default=None, help="打分结果 Excel 输出路径")
    ap.add_argument("--baseline", default=None, help="baseline.json 路径（用于环比）")
    ap.add_argument("--override", action="append", default=None, metavar="列号=字段名",
                    help="人工强制指定列映射（唯一人工介入点），可多次，如 --override 3=hours")
    ap.add_argument("--force-points", action="store_true",
                    help="明知覆盖度不足（C/D 分支）也要输出工分（默认不输出，只给排序参考）")
    args = ap.parse_args(argv)

    path = Path(args.file)
    out_dir = Path(args.out_dir) if args.out_dir else path.parent
    out_dir.mkdir(parents=True, exist_ok=True)
    stem = path.stem

    try:
        payload = pipeline(path, Path(args.baseline) if args.baseline else None,
                           args.override, args.force_points)
    except X.ParseError as err:
        fail = {"code": err.code, "msg": err.msg, "echo": err.echo,
                "status": "failed", "meta": {"file": path.name}}
        md = R.render_failure(fail)
        _write(out_dir / f"{stem}.gongfen.md" if not args.md else Path(args.md), md)
        jp = out_dir / f"{stem}.gongfen.json" if not args.json else Path(args.json)
        _write(jp, json.dumps(fail, ensure_ascii=False, indent=2))
        print(md)
        print(f"\n[退出码 1] 中间结果已写入：{jp}")
        return 1
    except Exception as exc:  # 内部异常
        tb = traceback.format_exc()
        print(f"[退出码 3] 内部异常：{type(exc).__name__}: {exc}\n{tb}", file=sys.stderr)
        return 3

    if payload["status"] == "failed":
        md = R.render_failure({
            "code": (payload["blockers"][0]["code"] if payload.get("blockers") else "E_FAILED"),
            "msg": (payload["blockers"][0]["msg"] if payload.get("blockers") else "分析失败"),
            "echo": (payload["blockers"][0]["echo"] if payload.get("blockers") else {}),
        })
        jp = out_dir / f"{stem}.gongfen.json" if not args.json else Path(args.json)
        _write(jp, json.dumps(payload, ensure_ascii=False, indent=2, default=_json_default))
        _write(out_dir / f"{stem}.gongfen.md" if not args.md else Path(args.md), md)
        print(md)
        print(f"\n[退出码 1] 中间结果已写入：{jp}")
        return 1

    md = R.render(payload)
    jp = out_dir / f"{stem}.gongfen.json" if not args.json else Path(args.json)
    mp = out_dir / f"{stem}.gongfen.md" if not args.md else Path(args.md)
    xp = out_dir / f"{stem}.gongfen.xlsx" if not args.xlsx else Path(args.xlsx)
    _write(jp, json.dumps(payload, ensure_ascii=False, indent=2, default=_json_default))
    _write(mp, md)
    if args.baseline is None:
        S.write_baseline(out_dir / "baseline.json", payload["baseline"])
    try:
        EO.write_xlsx(payload, xp)
    except Exception as exc:
        print(f"[退出码 3] Excel 输出失败：{type(exc).__name__}: {exc}", file=sys.stderr)
        print(f"          JSON: {jp}\n          MD  : {mp}")
        return 3
    print(md)
    print(f"\n[退出码 0] XLSX: {xp}\n          JSON: {jp}\n          MD  : {mp}")
    return 0


def _json_default(o):
    try:
        import numpy as np
        if isinstance(o, np.integer):
            return int(o)
        if isinstance(o, np.floating):
            return float(o)
        if isinstance(o, np.bool_):
            return bool(o)
    except Exception:
        pass
    return str(o)


def _write(p: Path, text: str):
    p.write_text(text, encoding="utf-8-sig")


if __name__ == "__main__":
    sys.exit(main())
