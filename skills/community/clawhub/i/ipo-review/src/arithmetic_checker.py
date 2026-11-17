from __future__ import annotations

import re
from collections import defaultdict

from .models import Evidence, Issue

NUM_RE = re.compile(r"-?\d+(?:,\d{3})*(?:\.\d+)?")
FORMULA_KEYWORDS = (
    "加：", "减：", "加:", "减:", "期初", "期末", "年初", "年末", "本期增加", "本期减少",
    "本期计提", "本期转回", "本期核销", "本期摊销", "本期转入", "本期转出",
    "转入其他收益", "其他收益", "账面余额", "坏账准备", "账面价值", "递延收益",
    "政府补助", "利息费用", "利息收入", "汇兑损益",
)
ROLL_FORWARD_KEYWORDS = ("期初", "期末", "年初", "年末", "本期增加", "本期减少", "本期计提", "本期转回", "本期核销", "本期摊销", "本期转入", "本期转出", "递延收益", "政府补助")
BOOK_VALUE_KEYWORDS = ("账面余额", "坏账准备", "账面价值")


def check_arithmetic(evidence: list[Evidence], tolerance: dict) -> tuple[list[Issue], list[dict]]:
    issues: list[Issue] = []
    warnings: list[dict] = []
    groups: dict[tuple[str, str, str, str], list[Evidence]] = defaultdict(list)
    tables: dict[tuple[str, str, str], list[Evidence]] = defaultdict(list)
    for ev in evidence:
        if ev.kind != "table":
            continue
        tables[(ev.doc_id, ev.filename, ev.table_no)].append(ev)
        if _is_amount_column(ev):
            groups[(ev.doc_id, ev.filename, ev.table_no, ev.col_name)].append(ev)

    for (doc_id, filename, table_no), cells in tables.items():
        confidence = max(c.table_structure_confidence for c in cells) if cells else 0.0
        rule_type, complexity = _table_rule_type(cells)
        if cells and confidence < 0.85:
            warnings.append(_skip(filename, table_no, "", "detail_range_uncertain", "表格结构置信度不足", "", confidence, table_no, "detail_range_uncertain", "unknown", "uncertain"))
        elif rule_type != "simple_sum":
            warnings.append(_skip(filename, table_no, "", "formula_table_not_supported", "识别为公式型或滚动类表格，未按简单合计校验", "", confidence, table_no, rule_type, complexity, "uncertain"))

    for (_doc_id, filename, table_no, col_name), cells in groups.items():
        cells = sorted(cells, key=lambda x: x.row_index)
        all_table_cells = tables.get((_doc_id, filename, table_no), cells)
        table_rule_type, table_complexity = _table_rule_type(all_table_cells)
        max_confidence = max(c.table_structure_confidence for c in cells) if cells else 0.0
        if not cells or max_confidence < 0.85:
            continue
        if table_rule_type != "simple_sum":
            continue
        total_cells = [c for c in cells if _is_total_row(c.row_name)]
        if len(total_cells) != 1:
            if total_cells:
                warnings.append(_skip(filename, table_no, col_name, "detail_range_uncertain", "存在多个合计/小计行，明细范围不唯一", ",".join(c.row_name for c in total_cells[:10]), max_confidence, table_no, "detail_range_uncertain", "unknown", "uncertain"))
            continue
        for total in total_cells:
            previous_totals = [c.row_index for c in cells if c.row_index < total.row_index and _is_total_row(c.row_name)]
            start_row = max(previous_totals) if previous_totals else 0
            detail_cells = [c for c in cells if start_row < c.row_index < total.row_index and not _is_total_row(c.row_name)]
            if _detail_range_uncertain(detail_cells):
                warnings.append(_skip(filename, table_no, col_name, "detail_range_uncertain", "明细中存在其中项、小计、父子层级或范围不明确项目", ",".join(c.row_name for c in detail_cells[:20]), max_confidence, total.position, "detail_range_uncertain", "unknown", "uncertain"))
                continue
            detail_nums = [_number(c.text) for c in detail_cells]
            detail_nums = [x for x in detail_nums if x is not None]
            displayed_total = _number(total.text)
            if displayed_total is None or len(detail_nums) < 2:
                warnings.append(_skip(filename, table_no, col_name, "detail_range_uncertain", "合计行明细范围不足或不明确", ",".join(c.row_name for c in detail_cells), max_confidence, total.position, "detail_range_uncertain", "unknown", "uncertain"))
                continue
            if len(detail_nums) > 30:
                warnings.append(_skip(filename, table_no, col_name, "detail_range_uncertain", "合计行明细范围过大，疑似跨分组", ",".join(c.row_name for c in detail_cells[:20]), max_confidence, total.position, "detail_range_uncertain", "unknown", "cross_page_risk"))
                continue
            detail_sum = sum(detail_nums)
            if _has_parent_child_risk(detail_cells, detail_sum, displayed_total):
                warnings.append(_skip(filename, table_no, col_name, "detail_range_uncertain", "疑似父级子级重复计入或sum约等于2倍合计", ",".join(c.row_name for c in detail_cells), max_confidence, total.position, "detail_range_uncertain", "unknown", "duplicated_hierarchy"))
                continue
            # 偏离率护栏：真实勾稽差错通常是少数项目漏记或端数（小幅偏离）；
            # 明细求和与合计偏离超过50%，几乎都是明细范围跨分组、表头错位或漏行造成的伪差异，
            # 不作为勾稽问题，转入arithmetic_skips待人工核对表格结构。
            if displayed_total and not (0.5 <= abs(detail_sum / displayed_total) <= 1.5):
                warnings.append(_skip(filename, table_no, col_name, "detail_range_uncertain", "明细求和与合计偏离过大，疑似明细范围跨分组或漏行", ",".join(c.row_name for c in detail_cells[:20]), max_confidence, total.position, "detail_range_uncertain", "unknown", "cross_page_risk"))
                continue
            allowed = max(tolerance.get("amount_default_abs", 0.01), 0.01 * max(1, len(detail_nums)))
            if abs(detail_sum - displayed_total) <= allowed:
                continue
            deviation_ratio = abs(detail_sum - displayed_total) / abs(displayed_total) if displayed_total else None
            issues.append(Issue(
                issue_id=f"AR{len(issues)+1:05d}",
                level="C",
                category="数学勾稽错误",
                round="",
                files=[filename],
                item=f"{table_no}/{col_name}/{total.row_name}",
                conclusion=f"同一表格同一金额列中，{total.row_name} 与上方明细求和不一致。",
                source_1=f"明细求和={detail_sum}",
                source_2=f"披露合计={displayed_total}",
                diff_amount=displayed_total - detail_sum,
                diff_ratio=deviation_ratio,
                caliber_analysis=f"仅对金额列执行：{table_no} {col_name}；纳入行：{', '.join(c.row_name for c in detail_cells[:20])}；偏离率：{deviation_ratio:.2%}；结构置信度：{max(c.table_structure_confidence for c in cells):.2f}。",
                evidence_pages=[f"{filename} {total.position}"],
                evidence_ids=[total.evidence_id] + [c.evidence_id for c in detail_cells[:10]],
                secondary_verified=False,
                basis="该表识别为简单合计表，明细范围清晰，未识别到加减公式或期初期末滚动结构。",
                suggestion="人工核对合计行对应明细范围，确认是否存在小计、跨页、隐藏行或单位不一致。",
                extraction_confidence=0.72,
                judgement_confidence=0.62,
                need_manual_review=True,
                status="LOW_CONFIDENCE_CONFLICT",
                review_priority="key",
                display_default=True,
                count_in_exception_total=True,
                arithmetic_rule_type="simple_sum",
                arithmetic_confidence=0.85,
                formula_complexity="simple",
                detail_range_status="clear",
            ))
    return issues, warnings


def _is_amount_column(ev: Evidence) -> bool:
    text = f"{ev.col_name} {ev.row_name} {ev.text}"
    if re.search(r"占比|比例|百分|%|率|序号|编号|No\.", text, re.I):
        return False
    if ev.unit in {"%", "百分点", "倍"}:
        return False
    return _number(ev.text) is not None


def _is_total_row(row_name: str) -> bool:
    if not any(k in row_name for k in ["合计", "小计", "总计"]):
        return False
    if re.search(r"[①②③④⑤⑥⑦⑧⑨⑩]|\+|-|＝|=|（.*[+加减].*）|\(.*[+加减].*\)", row_name):
        return False
    return True


def _number(text: str) -> float | None:
    cleaned = str(text).strip()
    if cleaned in {"", "-", "—", "不适用"}:
        return None
    match = NUM_RE.search(cleaned)
    if not match:
        return None
    raw = match.group(0).replace(",", "")
    if raw.isdigit() and 1900 <= int(raw) <= 2035:
        return None
    return float(raw)


def _has_parent_child_risk(detail_cells: list[Evidence], detail_sum: float, displayed_total: float) -> bool:
    if displayed_total and 1.7 <= abs(detail_sum / displayed_total) <= 2.3:
        return True
    values = [(c.row_name, _number(c.text)) for c in detail_cells]
    nums = [(name, val) for name, val in values if val is not None]
    for name, val in nums:
        others = [v for n, v in nums if n != name]
        if len(others) >= 2 and abs(sum(others) - displayed_total) <= max(0.01, abs(displayed_total) * 0.001):
            return True
        if others and abs((sum(others) - val)) <= max(0.01, abs(val) * 0.001):
            return True
    return False


def _table_rule_type(cells: list[Evidence]) -> tuple[str, str]:
    blob = " ".join(f"{c.row_name} {c.col_name} {c.text}" for c in cells)
    if ("期后累计回款金额" in blob or "期后回款金额" in blob) and not any(k in blob for k in ("加：", "减：", "期初", "期末", "本期增加", "本期减少", "本期计提", "本期转回")):
        return "simple_sum", "simple"
    if any(k in blob for k in BOOK_VALUE_KEYWORDS):
        return "book_value_formula", "formula"
    if any(k in blob for k in ROLL_FORWARD_KEYWORDS):
        return "roll_forward", "complex"
    if any(k in blob for k in FORMULA_KEYWORDS):
        return "add_subtract_formula", "formula"
    return "simple_sum", "simple"


def _detail_range_uncertain(detail_cells: list[Evidence]) -> bool:
    labels = [c.row_name.strip() for c in detail_cells]
    if any(re.search(r"其中[:：]|其中|小计|合计|总计", label) for label in labels):
        return True
    normalized = [re.sub(r"^\d+[\.、)]?\s*", "", label) for label in labels]
    for label in normalized:
        if not label:
            continue
        children = [other for other in normalized if other != label and label in other and len(other) > len(label)]
        if len(children) >= 2:
            return True
    return False


def _skip(file: str, table_no: str, col_name: str, reason: str, detail: str, rows: str, confidence: float,
          position: str, arithmetic_rule_type: str = "", formula_complexity: str = "",
          detail_range_status: str = "") -> dict:
    return {
        "file": file,
        "table_no": table_no,
        "col_name": col_name,
        "skip_reason": reason,
        "arithmetic_skip_reason": reason,
        "arithmetic_rule_type": arithmetic_rule_type,
        "formula_complexity": formula_complexity,
        "detail_range_status": detail_range_status,
        "detail": detail,
        "affected_rows": rows,
        "confidence": confidence,
        "position": position,
    }
