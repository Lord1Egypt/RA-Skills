"""field_recognize —— 别名词典、字段识别、单位归一、层级解析。

识别流程：归一化 → 排除词 → L1 精确 → L2 后缀 → L3 最长包含 → L5 模糊
         → 多维度仲裁 → 内容特征反推（置信度硬上限）
"""
from __future__ import annotations

import re
from collections import Counter
from datetime import date, datetime, timedelta

import params as P
from excel_io import is_null, norm_str, similarity, to_float

# ============================================================ 别名词典
# kind: text / hours / money / level / count / date / priority
FIELD_SPEC = {
    "task_name": {
        "canonical": "任务名称", "kind": "text", "dim": None,
        "aliases": {"任务名称": 1.00, "任务名": 0.98, "任务": 0.90, "事项": 0.86,
                    "工作项": 0.86, "工作内容": 0.82, "工作事项": 0.85,
                    "标题": 0.82, "需求名称": 0.88, "任务描述": 0.78,
                    "task": 0.90, "title": 0.85, "item": 0.80, "subject": 0.80},
        "negative": ["任务类型", "任务状态", "任务数", "任务量", "父任务", "子任务",
                     "任务编号", "任务id", "任务等级", "任务金额"],
    },
    "hours": {
        "canonical": "工时", "kind": "hours", "dim": "hours",
        "aliases": {"工时": 1.00, "实际工时": 1.00, "工时数": 0.95, "耗时": 0.95,
                    "用时": 0.95, "人天": 0.95, "人日": 0.95, "工作日": 0.90,
                    "预计工时": 0.92, "计划工时": 0.92, "工作量": 0.85,
                    "工期": 0.85, "周期": 0.78, "投入": 0.75,
                    "hours": 0.90, "effort": 0.90, "manday": 0.92},
        "negative": ["工时单价", "工时费率", "工时占比"],
    },
    "money": {
        "canonical": "金额", "kind": "money", "dim": "money",
        "aliases": {"收益金额": 1.00, "金额": 0.95, "合同额": 0.95, "合同金额": 0.95,
                    "营收": 0.90, "收入": 0.90, "创收": 0.90, "gmv": 0.85,
                    "成本": 0.80, "节约": 0.85, "降本": 0.85, "预算": 0.80,
                    "报价": 0.80, "产出价值": 0.85, "价值": 0.75,
                    "amount": 0.90, "revenue": 0.90},
        "negative": ["金额占比", "单价", "费率", "权重"],
    },
    "difficulty": {
        "canonical": "难度等级", "kind": "level", "dim": "difficulty",
        "aliases": {"难度等级": 1.00, "难度": 0.98, "复杂程度": 0.95, "复杂度": 0.95,
                    "技术难度": 0.95, "level": 0.85, "等级": 0.75,
                    "任务类型": 0.70, "类型": 0.62, "标签": 0.62, "分类": 0.68},
        "negative": [],
    },
    "risk": {
        "canonical": "风险等级", "kind": "level", "dim": "risk",
        "aliases": {"风险等级": 1.00, "风险": 0.95, "影响范围": 0.95, "是否关键": 0.90,
                    "重要性": 0.82, "不可逆": 0.85, "sla": 0.80, "涉及客户": 0.85},
        "negative": [],
    },
    "priority": {
        "canonical": "优先级", "kind": "priority", "dim": "urgency",
        "aliases": {"优先级": 1.00, "priority": 0.95, "紧急度": 0.90,
                    "重要程度": 0.80, "紧急程度": 0.88},
        "negative": [],
    },
    "quality": {
        "canonical": "验收状态", "kind": "quality", "dim": "quality",
        "aliases": {"验收状态": 1.00, "验收": 0.95, "是否通过": 0.92,
                    "驳回次数": 1.00, "返工次数": 0.95, "返工": 0.90,
                    "完成状态": 0.78, "状态": 0.75, "status": 0.75,
                    "评价": 0.70, "评分": 0.68, "客户反馈": 0.75, "review": 0.72},
        "negative": [],
    },
    "urgency": {
        "canonical": "截止日期", "kind": "date", "dim": "urgency",
        "aliases": {"截止日期": 1.00, "截止时间": 0.98, "交付日期": 0.95,
                    "要求完成时间": 0.95, "deadline": 0.95, "ddl": 0.92,
                    "due date": 0.90, "完成期限": 0.90, "是否加急": 0.75},
        "negative": ["开始", "起始"],
    },
    "start_date": {
        "canonical": "开始日期", "kind": "date", "dim": None,
        "aliases": {"开始日期": 1.00, "起始日期": 0.98, "开始时间": 0.95,
                    "start": 0.90, "start date": 0.90, "开工日期": 0.90},
        "negative": [],
    },
    "end_date": {
        "canonical": "结束日期", "kind": "date", "dim": None,
        "aliases": {"结束日期": 1.00, "完成日期": 0.95, "结束时间": 0.95,
                    "end": 0.88, "end date": 0.88, "完工日期": 0.90},
        "negative": [],
    },
    "collab": {
        "canonical": "协作方", "kind": "count", "dim": "collab",
        "aliases": {"协作方": 1.00, "协作部门": 0.95, "参与人": 0.90,
                    "干系人": 0.90, "相关方": 0.90, "配合人": 0.90,
                    "团队": 0.78, "抄送": 0.70, "participants": 0.85},
        "negative": [],
    },
    "reuse": {
        "canonical": "交付物类型", "kind": "text", "dim": "reuse",
        "aliases": {"交付物类型": 1.00, "交付物": 0.95, "产物": 0.88, "产出": 0.82,
                    "成果": 0.82, "deliverable": 0.85},
        "negative": [],
    },
    "skill": {
        "canonical": "所需技能", "kind": "text", "dim": "skill",
        "aliases": {"所需技能": 1.00, "技能要求": 0.95, "技能": 0.92,
                    "岗位": 0.78, "职级": 0.75, "执行人": 0.82,
                    "负责人": 0.72, "assignee": 0.82, "owner": 0.78, "认证": 0.72},
        "negative": [],
    },
    "strategy": {
        "canonical": "关联目标", "kind": "text", "dim": "strategy",
        "aliases": {"关联目标": 1.00, "所属目标": 0.95, "关联okr": 0.92,
                    "okr": 0.88, "战略": 0.85, "季度重点": 0.85},
        "negative": [],
    },
    "innovation": {
        "canonical": "是否探索", "kind": "level", "dim": "innovation",
        "aliases": {"是否探索": 1.00, "探索": 0.80, "预研": 0.80, "创新度": 0.80},
        "negative": [],
    },
    "parent": {
        "canonical": "父任务", "kind": "text", "dim": None,
        "aliases": {"父任务": 1.00, "上级任务": 0.95, "parent": 0.90,
                    "parent id": 0.88, "wbs": 0.85, "层级": 0.78, "阶段": 0.72},
        "negative": [],
    },
    "role": {
        "canonical": "角色", "kind": "text", "dim": None,
        "aliases": {"参与角色": 0.95, "角色": 0.90, "贡献": 0.78,
                    "主导配合": 0.80, "contribution": 0.78},
        "negative": [],
    },
}

# 需人工确认的维度（错认后果最重且不易被总分暴露）
FORCE_CONFIRM_FIELDS = {"money", "skill", "strategy", "difficulty"}

# 内容仲裁用词表
PROGRESS_WORDS = {"已完成", "进行中", "未开始", "已关闭", "待办", "已交付",
                  "进行", "未启动", "完成", "done", "closed", "open", "todo"}
QUALITY_WORDS = {"通过", "驳回", "返工", "不合格", "合格", "验收", "未通过", "待验收"}
INNOV_WORDS = {"探索", "预研", "试点", "创新", "试验", "研究", "从0"}
PRIORITY_WORDS = {"p0", "p1", "p2", "p3", "紧急", "特急", "高", "中", "低", "一般"}

LEVEL_TEXT = {
    "极高": 5, "很高": 5, "非常高": 5, "非常难": 5, "很难": 5, "复杂": 5, "极复杂": 5,
    "困难": 4, "较难": 4, "较高": 4, "偏难": 4, "难": 4,
    "高": 4, "中": 3, "一般": 3, "普通": 3, "中等": 3, "一般难度": 3, "偏高": 4,
    "较低": 2, "偏易": 2, "简单": 2, "低": 2, "容易": 2, "易": 2,
    "很低": 1, "极低": 1, "非常低": 1, "极简": 1,
}

# 注：A 难度关键词表已迁至 params.A_KEYWORD_TABLE（可配置），此处不再保留旧表，
# 避免两套词表并存导致同一任务在两个位置得出不同档位。

# ============================================================ 别名索引
def _build_index():
    idx = {}
    for field, spec in FIELD_SPEC.items():
        for alias, weight in spec["aliases"].items():
            key = norm_str(alias).lower()
            idx.setdefault(key, []).append((field, weight))
    return idx


ALIAS_INDEX = _build_index()
_ALIAS_LENGTHS = sorted({len(k) for k in ALIAS_INDEX}, reverse=True)


def normalize_header(raw):
    """列名归一化：返回 (归一化名, 单位提示)。"""
    s = norm_str(raw)
    unit_hint = None
    m = re.search(r"\(单位[:：]?\s*([^)]+)\)", s)
    if m:
        unit_hint = m.group(1).strip()
    else:
        m2 = re.search(r"\(([^)]+)\)", s)
        if m2:
            inner = m2.group(1).strip()
            if re.match(r"^(小时|h|人天|人日|工作日|天|元|万元|千元|万|%|个|条)$", inner, re.I):
                unit_hint = inner
    s = re.sub(r"\([^)]*\)", "", s)
    s = re.sub(r"是否|所需|实际|相关|情况|信息|明细|说明|备注", "", s)
    s = re.sub(r"[\s\-_/\\:·．.,，]", "", s).lower()
    return s, unit_hint


def _negatively_excluded(field, norm_header_value, raw_header) -> bool:
    raw_n = norm_str(raw_header).lower()
    for neg in FIELD_SPEC[field].get("negative", []):
        nn = norm_str(neg).lower()
        if nn and (nn in raw_n or nn == norm_header_value):
            return True
    return False


def match_column(raw_header):
    """对单列名做 L1→L5 匹配，返回候选列表 [{field, conf, method}]。"""
    norm, unit_hint = normalize_header(raw_header)
    if not norm:
        return [], unit_hint

    candidates = []
    for field in FIELD_SPEC:
        if _negatively_excluded(field, norm, raw_header):
            continue
        best = None
        for alias, weight in FIELD_SPEC[field]["aliases"].items():
            a = norm_str(alias).lower()
            if not a or a in ("", None):
                continue
            # L1 精确
            if norm == a:
                cand = (weight, "L1_exact")
            # L2 后缀
            elif norm.endswith(a) and len(norm) <= len(a) + 4:
                cand = (weight * 0.95, "L2_suffix")
            # L3 最长包含
            elif a in norm:
                cand = (weight * 0.90, "L3_contains")
            # L5 模糊
            elif len(a) >= 2 and similarity(norm, a) >= P.FUZZY_THRESHOLD:
                cand = (weight * 0.75, "L5_fuzzy")
            else:
                continue
            if best is None or cand[0] > best[0]:
                best = cand
        if best:
            candidates.append({"field": field, "conf": round(best[0], 4), "method": best[1]})

    candidates.sort(key=lambda x: -x["conf"])
    return candidates, unit_hint


def probe_row(row) -> int:
    """供 excel_io 做表头/Sheet 评分：该行命中的字段种类数。"""
    hits = set()
    for v in row:
        if is_null(v) or not isinstance(v, str):
            continue
        cands, _ = match_column(v)
        if cands and cands[0]["conf"] >= P.CONF_MID:
            hits.add(cands[0]["field"])
    return len(hits)


# ============================================================ 内容特征
def looks_numeric(v) -> bool:
    """宽松数值判定：原生数字 / 纯数字文本 / 金额串 / 工时串 均算。"""
    if isinstance(v, (int, float)) and not isinstance(v, bool):
        return True
    if is_null(v):
        return False
    if to_float(v) is not None:
        return True
    s = norm_str(v).replace(",", "")
    if RE_MONEY.match(s) or RE_HOURS.match(s):
        return True
    return False


def to_number_loose(v):
    """把 ¥12,000 / 1.2万 / 8h / 2人天 都取成数字（用于内容特征统计）。"""
    n = to_float(v)
    if n is not None:
        return n
    for parser in (parse_money_cell, parse_hours_cell):
        try:
            r = parser(v)
            if r.get("value") is not None:
                return r["value"]
            if r.get("pending") is not None:
                return r["pending"]
        except Exception:
            continue
    return None


def column_features(values) -> dict:
    vals = [v for v in values if not is_null(v)]
    n = len(vals)
    if n == 0:
        return {"n": 0}
    nums = [to_number_loose(v) for v in vals]
    num_ok = [x for x in nums if x is not None]
    numericish = sum(1 for v in vals if looks_numeric(v))
    dates = [parse_date_value(v) for v in vals]
    date_ok = [d for d in dates if d is not None]
    uniq = len(set(norm_str(v) for v in vals))
    texts = [norm_str(v) for v in vals]
    cjk = sum(1 for t in texts if any("\u4e00" <= ch <= "\u9fff" for ch in t))
    enums = [t.lower() for t in texts]
    return {
        "n": n,
        "uniq_ratio": uniq / n,
        "avg_len": sum(len(t) for t in texts) / n,
        "numeric_rate": numericish / n,
        "num_median": sorted(num_ok)[len(num_ok) // 2] if num_ok else None,
        "num_max": max(num_ok) if num_ok else None,
        "date_rate": len(date_ok) / n,
        "cjk_ratio": cjk / n,
        "enum": uniq <= 8 and uniq / n < 0.35,
        "enum_values": list({t for t in texts})[:10],
        "enum_lower": set(enums),
        "seq_like": _seq_like(num_ok, n),
    }


def _seq_like(num_ok, n) -> bool:
    """序号列特征：全整数、无重复、排序后公差为 1 的等差数列（如 1,2,3...13）。

    用途：拦截「序号/编号」列被内容反推成工时。实测踩坑——考核表序号列 1–13
    被判为工时 ×8 → 8~104 小时，排名直接由行号决定，且不报错。
    """
    if not num_ok or len(num_ok) < n or n < 3:
        return False
    try:
        ints = sorted(round(float(x)) for x in num_ok)
    except (TypeError, ValueError):
        return False
    if any(abs(float(x) - round(float(x))) > 1e-9 for x in num_ok):
        return False          # 含小数 → 不是序号
    if len(set(ints)) != len(ints):
        return False          # 有重复 → 不是序号
    return all(ints[i + 1] - ints[i] == 1 for i in range(len(ints) - 1))


def infer_by_content(features) -> dict | None:
    """一列都没匹上时，用列内容特征反推。置信度上限 0.65 → 必然需人工确认。"""
    if features.get("n", 0) < 2:
        return None
    f = features
    if f["enum"]:
        low = f["enum_lower"]
        if low & PROGRESS_WORDS:
            return {"field": "progress", "conf": 0.90, "method": "content_progress"}
        if low & QUALITY_WORDS:
            return {"field": "quality", "conf": 0.62, "method": "content_quality"}
        if low & INNOV_WORDS:
            return {"field": "innovation", "conf": 0.60, "method": "content_innovation"}
        if low & PRIORITY_WORDS:
            return {"field": "priority", "conf": 0.55, "method": "content_priority"}
        if low & set(LEVEL_TEXT):
            return {"field": "difficulty", "conf": 0.60, "method": "content_level"}
    if f["date_rate"] > 0.85:
        return {"field": "date_generic", "conf": 0.60, "method": "content_date"}
    if f["numeric_rate"] > 0.9 and f["num_median"] is not None:
        if f["num_median"] >= 1000 and (f["num_max"] or 0) >= 1e4:
            return {"field": "money", "conf": 0.50, "method": "content_money"}
        if 1 <= f["num_median"] <= 40 and (f["num_max"] or 0) <= 300:
            # 序号列拦截：1..n 的连续整数（公差 1 等差数列）是序号不是工时。
            # 实测踩坑：考核表「序号」列 1–13 被当成工时 ×8 → 8~104 小时，
            # 排名被行号决定，且不会报错，是最难发现的一类误识别。
            if f.get("seq_like"):
                return {"field": "seq", "conf": 0.55, "method": "content_seq"}
            return {"field": "hours", "conf": 0.50, "method": "content_hours"}
    if f["uniq_ratio"] > 0.95 and 5 <= f["avg_len"] <= 60 and f["cjk_ratio"] > 0.3:
        return {"field": "task_name", "conf": 0.55, "method": "content_taskname"}
    return None


# ============================================================ 仲裁
def arbitrate(candidates, raw_header, features):
    """同一列命中多维度时的仲裁。返回 (field, conf, log_note)。"""
    if not candidates:
        return None, 0.0, None
    if len(candidates) == 1:
        c0 = candidates[0]
        # 单候选也要过内容闸：列名叫「状态」但值是 已完成/进行中，就不是质量结果列。
        # 放过去会让所有已完成任务拿到同一个质量分，E 维退化成常数（静默污染总分）。
        if c0["field"] == "quality" and (features.get("enum_lower") or set()) & PROGRESS_WORDS:
            return None, 0.0, "「状态」枚举为进度词（已完成/进行中），不携带质量信息，E 维不启用"
        return c0["field"], c0["conf"], None

    fields = [c["field"] for c in candidates]
    norm, _ = normalize_header(raw_header)
    note = None
    conf_penalty = 0.6

    # 「等级 / Level」：与风险共现 → risk；否则难度
    if {"difficulty", "risk"} <= set(fields):
        raw_n = norm_str(raw_header).lower()
        if any(w in raw_n for w in ("风险", "安全", "不可逆")):
            picked = "risk"
            note = "列名含风险语义，归 D 风险责任"
        else:
            picked = "difficulty"
            note = "裸「等级」默认难度，置信度 ×0.7，需确认"
            conf_penalty = 0.7
        conf = max(c["conf"] for c in candidates if c["field"] == picked) * conf_penalty
        return picked, round(conf, 4), note

    # 「价值」：数值大 → money；枚举高低 → risk 重要性（不进 money）
    if {"money", "risk"} <= set(fields):
        if features.get("numeric_rate", 0) > 0.7 and (features.get("num_median") or 0) >= 100:
            conf = max(c["conf"] for c in candidates if c["field"] == "money") * 0.9
            return "money", round(conf, 4), "内容为数值且量级大，归金额"
        conf = max(c["conf"] for c in candidates if c["field"] == "risk") * 0.7
        return "risk", round(conf, 4), "内容为等级词，归重要性（不进金额）"

    # 「状态」：进度词 → 不作为质量（丢弃）；验收词 → quality
    if "quality" in fields:
        low = features.get("enum_lower", set())
        if low & PROGRESS_WORDS:
            return None, 0.0, "「状态」枚举为进度词（已完成/进行中），不携带质量信息，E 维不启用"
        if low & QUALITY_WORDS:
            conf = max(c["conf"] for c in candidates if c["field"] == "quality")
            return "quality", round(conf, 4), None

    # 「类型/标签」：创新词 → innovation；否则 difficulty
    if {"difficulty", "innovation"} <= set(fields):
        low = features.get("enum_lower", set())
        if low & INNOV_WORDS:
            picked = "innovation"
            note = "枚举含探索/预研类词，归创新度"
        else:
            picked = "difficulty"
            note = "归难度（任务类型映射）"
        conf = max(c["conf"] for c in candidates if c["field"] == picked) * 0.8
        return picked, round(conf, 4), note

    best = candidates[0]
    return best["field"], round(best["conf"] * 0.6, 4), f"多维度冲突，取最高分 {best['field']}，需确认"


# ============================================================ 字段识别总入口
def recognize(headers, sample_cols) -> dict:
    """headers: list[str]；sample_cols: list[list] 与 headers 等长。"""
    columns, unmapped, arbitration_log = [], [], []

    for idx, raw in enumerate(headers):
        samples = sample_cols[idx] if idx < len(sample_cols) else []
        features = column_features(samples)
        cands, unit_hint = match_column(raw)

        if cands:
            field, conf, note = arbitrate(cands, raw, features)
            if field is None:
                unmapped.append({
                    "col_idx": idx + 1, "raw_name": raw,
                    "reason": "arbitrated_out", "note": note,
                    "sample_values": [norm_str(s) for s in samples[:3]],
                })
                if note:
                    arbitration_log.append({"col_idx": idx + 1, "raw_name": raw,
                                            "candidates": [c["field"] for c in cands],
                                            "picked": None, "rule": note})
                continue
            method = next((c["method"] for c in cands if c["field"] == field), "L1_exact")
            # 内容一致加成 / 矛盾惩罚
            content_factor = 1.0
            spec = FIELD_SPEC.get(field, {})
            if spec.get("kind") == "level" and features.get("enum"):
                content_factor = 1.15
            elif spec.get("kind") in ("hours", "money") and features.get("numeric_rate", 0) < 0.3:
                content_factor = 0.5
            conf = min(conf * content_factor, 1.0)

            if note:
                arbitration_log.append({"col_idx": idx + 1, "raw_name": raw,
                                        "candidates": [c["field"] for c in cands],
                                        "picked": field, "rule": note,
                                        "confidence_after": round(conf, 4)})
            columns.append({
                "col_idx": idx + 1, "raw_name": raw, "norm_name": normalize_header(raw)[0],
                "mapped_to": field, "confidence": round(conf, 4), "method": method,
                "unit_hint": unit_hint,
                "requires_confirm": conf < P.CONF_HIGH or field in FORCE_CONFIRM_FIELDS,
                "sample_values": [norm_str(s) for s in samples[:3]],
            })
        else:
            inferred = infer_by_content(features)
            if inferred:
                conf = min(inferred["conf"], P.CONTENT_INFER_CAP)
                columns.append({
                    "col_idx": idx + 1, "raw_name": raw,
                    "norm_name": normalize_header(raw)[0],
                    "mapped_to": inferred["field"], "confidence": round(conf, 4),
                    "method": inferred["method"], "unit_hint": unit_hint,
                    "requires_confirm": True,
                    "sample_values": [norm_str(s) for s in samples[:3]],
                })
                arbitration_log.append({
                    "col_idx": idx + 1, "raw_name": raw, "candidates": [],
                    "picked": inferred["field"],
                    "rule": f"列名未命中别名，由内容特征反推（上限 {P.CONTENT_INFER_CAP}），必须人工确认",
                })
            else:
                unmapped.append({
                    "col_idx": idx + 1, "raw_name": raw,
                    "reason": "no_alias_match", "note": "列名与内容均无法识别",
                    "sample_values": [norm_str(s) for s in samples[:3]],
                })

    # 同字段重复列：取置信度最高者
    seen = {}
    for col in columns:
        f = col["mapped_to"]
        if f not in seen or col["confidence"] > seen[f]["confidence"]:
            seen[f] = col
    deduped = list(seen.values())
    dropped = [c for c in columns if c not in deduped]

    return {"columns": sorted(deduped, key=lambda x: x["col_idx"]),
            "unmapped": unmapped, "arbitration_log": arbitration_log,
            "dropped_duplicate_columns": [c["raw_name"] for c in dropped]}


# ============================================================ 人工覆写入口
def apply_override(colmap, overrides, n_cols):
    """`--override 列号=字段名`：人工强制指定列映射，优先级高于一切自动识别。

    这是唯一的"人工介入"入口 —— 默认一条命令跑到底、不问任何问题；
    只有当人明确知道第 N 列是什么时才用它，覆盖结果会写进仲裁记录留痕。
    返回新的 colmap（不改原对象）。
    """
    from excel_io import ParseError

    def _echo():
        return {"recognized_columns": colmap.get("columns", []),
                "suggested_columns": ["格式：--override 列号=字段名，字段名可选："
                                      + "、".join(sorted(FIELD_SPEC))]}

    log = []
    cols = {c["col_idx"]: dict(c) for c in colmap["columns"]}
    unmapped = {u["col_idx"]: dict(u) for u in colmap.get("unmapped", [])}

    for spec in overrides or []:
        if "=" not in spec:
            raise ParseError("E_OVERRIDE_FORMAT",
                             f"--override 参数格式应为 列号=字段名，收到「{spec}」",
                             {**_echo(), "hint": "例：--override 3=hours --override 5=money"})
        idx_s, field = spec.split("=", 1)
        field = field.strip()
        try:
            idx = int(idx_s.strip())
        except ValueError:
            raise ParseError("E_OVERRIDE_FORMAT",
                             f"--override 的列号必须是整数，收到「{idx_s}」", _echo())
        if field not in FIELD_SPEC:
            raise ParseError("E_OVERRIDE_FIELD",
                             f"--override 指定了未知字段「{field}」", _echo())
        if idx < 1 or idx > n_cols:
            raise ParseError("E_OVERRIDE_RANGE",
                             f"--override 列号 {idx} 超出范围（本表共 {n_cols} 列）", _echo())

        # 同一字段原有的列让位（一个字段只能有一列）
        for c in list(cols.values()):
            if c["mapped_to"] == field and c["col_idx"] != idx:
                cols.pop(c["col_idx"])
                unmapped[c["col_idx"]] = {
                    "col_idx": c["col_idx"], "raw_name": c["raw_name"],
                    "reason": "superseded_by_override",
                    "note": f"被 --override {idx}={field} 取代",
                    "sample_values": c.get("sample_values", []),
                }
                log.append({"col_idx": c["col_idx"], "raw_name": c["raw_name"],
                            "candidates": [field], "picked": None,
                            "rule": f"被 --override {idx}={field} 取代"})

        old = cols.get(idx) or unmapped.get(idx) or {}
        raw_name = old.get("raw_name")
        cols[idx] = {
            "col_idx": idx, "raw_name": raw_name,
            "norm_name": normalize_header(raw_name)[0] if raw_name else "",
            "mapped_to": field, "confidence": 1.0, "method": "manual_override",
            "unit_hint": old.get("unit_hint"), "requires_confirm": False,
            "sample_values": old.get("sample_values", []),
        }
        unmapped.pop(idx, None)
        log.append({"col_idx": idx, "raw_name": raw_name, "candidates": [field],
                    "picked": field, "rule": "人工 --override 强制指定（置信度置 1.0）"})

    return {
        "columns": sorted(cols.values(), key=lambda x: x["col_idx"]),
        "unmapped": sorted(unmapped.values(), key=lambda x: x["col_idx"]),
        "arbitration_log": list(colmap.get("arbitration_log") or []) + log,
        "dropped_duplicate_columns": colmap.get("dropped_duplicate_columns", []),
    }


# ============================================================ 值解析
UNIT_HOURS = {
    "小时": 1.0, "h": 1.0, "hr": 1.0, "hrs": 1.0, "hour": 1.0, "hours": 1.0,
    "人天": P.HOURS_PER_MANDAY, "人日": P.HOURS_PER_MANDAY, "工作日": P.HOURS_PER_MANDAY,
    "天": P.HOURS_PER_MANDAY, "日": P.HOURS_PER_MANDAY, "d": P.HOURS_PER_MANDAY,
    "day": P.HOURS_PER_MANDAY, "days": P.HOURS_PER_MANDAY, "md": P.HOURS_PER_MANDAY,
    "周": P.WEEK_HOURS, "w": P.WEEK_HOURS, "week": P.WEEK_HOURS,
    "月": P.MONTH_HOURS, "month": P.MONTH_HOURS,
    "分钟": 1 / 60, "min": 1 / 60,
}

RE_HOURS = re.compile(
    r"^[约大约≈~<>≥≤\s]*([\d,]+(?:\.\d+)?)\s*(?:[-~至到]\s*([\d,]+(?:\.\d+)?)\s*)?"
    r"(小时|人天|人日|工作日|分钟|hrs|hr|min|天|日|周|月|h|d|w|m)?\s*[左右]?$",
    re.I,
)
RE_MONEY = re.compile(
    r"^[¥￥$€£]?\s*([\d,]+(?:\.\d+)?)\s*(亿|百万|万|千|[kKwWmM])?\s*元?\s*$"
)
MONEY_MULT = {"亿": 1e8, "百万": 1e6, "万": 1e4, "千": 1e3,
              "k": 1e3, "K": 1e3, "w": 1e4, "W": 1e4, "m": 1e6, "M": 1e6}


def parse_hours_cell(v, default_factor=None):
    """返回 {value, estimated, unit_in_cell, ok}。"""
    out = {"raw": v, "value": None, "estimated": False, "unit_in_cell": None, "ok": False}
    if is_null(v):
        return out
    if isinstance(v, (int, float)):
        factor = default_factor if default_factor is not None else 1.0
        out.update(value=float(v) * factor, ok=True,
                   unit_in_cell=None if default_factor else "assumed")
        return out
    s = norm_str(v).replace(",", "")
    m = RE_HOURS.match(s)
    if not m:
        return out
    try:
        lo = float(m.group(1))
        hi = float(m.group(2)) if m.group(2) else None
        unit = (m.group(3) or "").lower()
    except ValueError:
        return out
    val = (lo + hi) / 2 if hi is not None else lo
    estimated = hi is not None or s[0] in "约大约≈~<>≥≤"
    factor = UNIT_HOURS.get(unit) if unit else None
    if factor is not None:
        out.update(value=val * factor, estimated=estimated, unit_in_cell=unit, ok=True)
    elif default_factor is not None:
        out.update(value=val * default_factor, estimated=estimated, ok=True,
                   unit_in_cell="assumed")
    else:
        out.update(value=None, estimated=estimated, unit_in_cell=None, ok=False,
                   pending=val)
    return out


def parse_money_cell(v, column_mult=1.0):
    out = {"raw": v, "value": None, "estimated": False, "ok": False, "currency_foreign": False}
    if is_null(v):
        return out
    if isinstance(v, (int, float)):
        out.update(value=float(v) * column_mult, ok=True)
        return out
    s = norm_str(v)
    if re.search(r"[$€£]", s):
        out["currency_foreign"] = True
    s2 = s.replace(",", "").replace(" ", "")
    m = RE_MONEY.match(s2)
    if not m:
        return out
    try:
        num = float(m.group(1))
    except ValueError:
        return out
    unit = m.group(2)
    mult = column_mult
    if unit:
        # 列名已含单位则不重复乘，只警告（由上层处理）
        mult = MONEY_MULT.get(unit, 1.0)
    out.update(value=num * mult, ok=True, unit_in_cell=unit)
    return out


DATE_PATTERNS = [
    ("%Y/%m/%d", r"^(\d{4})[/-](\d{1,2})[/-](\d{1,2})$"),
    ("%Y.%m.%d", r"^(\d{4})\.(\d{1,2})\.(\d{1,2})$"),
    ("CN", r"^(\d{4})年(\d{1,2})月(\d{1,2})日?$"),
    ("%Y%m%d", r"^(\d{4})(\d{2})(\d{2})$"),
]


def parse_date_value(v):
    """返回 date 或 None。Excel 序列号仅接受 40000–60000。"""
    if v is None or is_null(v):
        return None
    if isinstance(v, datetime):
        return v.date()
    if isinstance(v, date):
        return v
    if isinstance(v, (int, float)) and not isinstance(v, bool):
        if 40000 <= float(v) <= 60000:
            try:
                return (datetime(1899, 12, 30) + timedelta(days=float(v))).date()
            except Exception:
                return None
        return None
    s = norm_str(v)
    m = re.match(r"^(\d{4})[/-](\d{1,2})[/-](\d{1,2})$", s)
    if m:
        return _mkdate(m.group(1), m.group(2), m.group(3))
    m = re.match(r"^(\d{4})\.(\d{1,2})\.(\d{1,2})$", s)
    if m:
        return _mkdate(m.group(1), m.group(2), m.group(3))
    m = re.match(r"^(\d{4})年(\d{1,2})月(\d{1,2})日?$", s)
    if m:
        return _mkdate(m.group(1), m.group(2), m.group(3))
    m = re.match(r"^(\d{4})(\d{2})(\d{2})$", s)
    if m:
        return _mkdate(m.group(1), m.group(2), m.group(3))
    return None


def _mkdate(y, mo, d):
    try:
        return date(int(y), int(mo), int(d))
    except ValueError:
        return None


def parse_date_range(v):
    """支持 '2026/1/1-2026/1/5' 这类区间，返回 (start, end)。"""
    s = norm_str(v)
    if not s:
        return None, None
    parts = re.split(r"\s*[-~至到]\s*", s)
    if len(parts) == 2:
        a, b = parse_date_value(parts[0]), parse_date_value(parts[1])
        if a and b:
            return (a, b) if a <= b else (b, a)
    d = parse_date_value(s)
    return d, d


def parse_level_value(v, kind="level"):
    """返回 (level 1-5, estimated)。"""
    if is_null(v):
        return None, False
    if isinstance(v, (int, float)) and not isinstance(v, bool):
        x = float(v)
        if 1 <= x <= 5:
            return int(round(x)), False
        if 1 <= x <= 10:
            return int(min(5, max(1, round(x / 2)))), True
        if 1 <= x <= 100:
            return int(min(5, max(1, round(x / 20)))), True
        return None, False
    s = norm_str(v).lower()
    if kind == "priority":
        m = re.match(r"^p([0-3])$", s)
        if m:
            return {0: 5, 1: 4, 2: 3, 3: 2}[int(m.group(1))], False
        if s in ("特急", "紧急", "加急"):
            return 5, False
    if s in LEVEL_TEXT:
        return LEVEL_TEXT[s], False
    m = re.match(r"^([1-5])$", s)
    if m:
        return int(m.group(1)), False
    return None, False


def parse_count_value(v):
    """协作方计数：按顿号/逗号/分号/斜杠/换行分割。"""
    if is_null(v):
        return None
    if isinstance(v, (int, float)) and not isinstance(v, bool):
        return int(v)
    parts = [p.strip() for p in re.split(r"[、,;；/\n]+", norm_str(v)) if p.strip()]
    return len(parts) if parts else None


def parse_quality_level(v):
    """质量优先用次数（客观），其次验收结论。"""
    if is_null(v):
        return None
    num = to_float(v)
    if num is not None:
        n = int(num)
        return {0: 5, 1: 4, 2: 3, 3: 2}.get(n, 1)
    s = norm_str(v)
    if s in ("通过", "合格", "已验收", "验收通过"):
        return 5
    if s in ("驳回", "不合格", "未通过", "待验收"):
        return 2
    lvl, _ = parse_level_value(v)
    return lvl


def resolve_hours_unit(header_norm, unit_hint, col_formats, bare_values, anchors):
    """工时单位三来源：列名/格式 > 日期锚点反算 > 数量级推断。

    返回 {"factor","source","confidence","note"}
    """
    # 1) 列名 / 数字格式
    text = (norm_str(header_norm) or "") + " " + (unit_hint or "")
    # 显式名优先（避免「工时」里的「时」被单字键误命中）
    for kw, factor in (("人天", P.HOURS_PER_MANDAY), ("人日", P.HOURS_PER_MANDAY),
                       ("工作日", P.HOURS_PER_MANDAY), ("工时", 1.0), ("小时", 1.0),
                       ("耗时", 1.0), ("用时", 1.0)):
        if kw in text:
            return {"factor": factor, "source": "col_name", "confidence": 0.95,
                    "note": f"列名含「{kw}」→ 按{'小时' if factor == 1 else '人天'}计"}
    for key, factor in UNIT_HOURS.items():
        if key.isascii():
            if re.search(rf"(?<![a-z]){re.escape(key)}(?![a-z])", text, re.I):
                return {"factor": factor, "source": "col_name", "confidence": 0.95,
                        "note": f"列名/单位为「{key}」"}
        else:
            if key in text:
                return {"factor": factor, "source": "col_name", "confidence": 0.95,
                        "note": f"列名/单位为「{key}」"}
    for fmt in col_formats or []:
        for key, factor in UNIT_HOURS.items():
            if key in str(fmt) and not key.isascii():
                return {"factor": factor, "source": "number_format", "confidence": 0.9,
                        "note": f"单元格格式含「{key}」"}

    # 2) 日期锚点反算
    pairs = [(h, avail) for h, avail in anchors if h and avail and avail > 0]
    if len(pairs) >= 2:
        as_hour = sum(1 for h, a in pairs if abs(h / a - 1) < 0.4)
        as_day = sum(1 for h, a in pairs if abs(h * P.HOURS_PER_MANDAY / a - 1) < 0.4)
        if as_hour > as_day and as_hour >= 2:
            return {"factor": 1.0, "source": "date_anchor", "confidence": 0.8,
                    "note": f"日期锚点反算：{as_hour}/{len(pairs)} 条与「小时」吻合"}
        if as_day > as_hour and as_day >= 2:
            return {"factor": P.HOURS_PER_MANDAY, "source": "date_anchor", "confidence": 0.8,
                    "note": f"日期锚点反算：{as_day}/{len(pairs)} 条与「人天」吻合"}

    # 3) 数量级推断
    nums = [x for x in bare_values if x is not None]
    if nums:
        s = sorted(nums)
        med = s[len(s) // 2]
        mx = s[-1]
        if med <= 3 and mx <= 40:
            return {"factor": P.HOURS_PER_MANDAY, "source": "magnitude", "confidence": 0.5,
                    "note": "数量级推断为人天（中位≤3、最大≤40），必须人工确认"}
        if med >= 8 and mx >= 80:
            return {"factor": 1.0, "source": "magnitude", "confidence": 0.5,
                    "note": "数量级推断为小时（中位≥8、最大≥80），必须人工确认"}

    return {"factor": P.HOURS_PER_MANDAY, "source": "default", "confidence": 0.3,
            "note": "单位无法判定，默认按人天×8，必须人工确认"}


def difficulty_from_keywords(text):
    """A 困难程度：关键词 → 档位（纯脚本，无模型）。

    规则（按序）：
      ⓪ 先剥离排除词（耗时/金额/故障/紧急 等），做正交化，避免与 B/C/D/G 重复计分
      ① 命中词存在子串包含关系时只保留最长者（否则「平台搭建」会被「搭建」拖到 4 档）
      ② 命中多档取最低档（保守：低估可申诉，高估发出去收不回）
    返回 (level | None, 命中依据列表)
    """
    if not text:
        return None, []
    t = norm_str(text).lower()
    for w in P.A_EXCLUDE_WORDS:
        t = t.replace(w.lower(), " ")
    hits = []
    for level, words in P.A_KEYWORD_TABLE:
        for w in words:
            if w.lower() in t:
                hits.append((w, level))
    if not hits:
        return None, []
    # ⓪ 最长匹配去重
    kept = []
    for w, lv in sorted(hits, key=lambda x: (-len(x[0]), x[1])):
        if any(w in k[0] for k in kept):
            continue
        kept.append((w, lv))
    level = min(lv for _, lv in kept)
    return level, [f"{w}→{lv}档" for w, lv in kept]


def reuse_from_text(text):
    """J 复用价值：三档枚举（1/3/5），禁止连续打分。零命中返回 None。"""
    if not text:
        return None, None
    t = norm_str(text).lower()
    for level in (5, 3, 1):
        for w in P.J_TIERS[level]:
            if w.lower() in t:
                return level, w
    return None, None


# ============================================================ 层级解析
def resolve_hierarchy(tasks) -> dict:
    """可加性自检判定容器父任务。"""
    by_name = {}
    for t in tasks:
        by_name.setdefault(t["task_name"], []).append(t)

    children = {}
    for t in tasks:
        pid = t.get("parent_ref")
        if pid:
            children.setdefault(pid, []).append(t)

    containers = []
    for t in tasks:
        kids = children.get(t["task_name"]) or children.get(str(t.get("parent_key") or ""))
        if not kids:
            continue
        parent_h = t["values"].get("hours", {}).get("parsed")
        child_sum = sum(k["values"].get("hours", {}).get("parsed") or 0 for k in kids)
        if parent_h and child_sum:
            if abs(parent_h - child_sum) / parent_h < 0.10:
                t["is_container"] = True
                t["parent_reason"] = f"父工时 {parent_h:.1f} ≈ 子任务之和 {child_sum:.1f}（<10%），判为容器"
                containers.append(t["task_id"])
            elif parent_h > child_sum * 1.1:
                t["is_container"] = False
                t["parent_reason"] = f"父工时 {parent_h:.1f} > 1.1×子之和 {child_sum:.1f}，判为独立任务"
        for k in kids:
            k["parent_id"] = t["task_id"]
    return {"containers": containers,
            "note": "容器父任务不计分，只汇总子任务" if containers else "未检测到容器父任务"}
