from __future__ import annotations

import re
from collections import defaultdict

from .models import Evidence, FinancialFact, Issue

PERCENT_RE = re.compile(r"(-?\d+(?:\.\d+)?)\s*%")
YEAR_RE = re.compile(r"(20[2-3]\d)")


def check_text_table_consistency(evidence: list[Evidence], facts: list[FinancialFact] | None = None) -> list[Issue]:
    text_rows = [_parse_text_ratio(ev) for ev in evidence if ev.kind == "text"]
    text_rows = [row for row in text_rows if row]
    table_groups = _table_collection_ratios(evidence)
    issues: list[Issue] = []
    for row in text_rows:
        table = _nearest_table(row, table_groups)
        if not table:
            continue
        mismatches = []
        for year, text_value in row["values"].items():
            if year not in table["values"]:
                continue
            table_value = table["values"][year]
            if abs(text_value - table_value) > 0.01:
                mismatches.append((year, text_value, table_value, table_value - text_value))
        if not mismatches:
            continue
        analysis = "；".join(f"{year}年度：正文{text_v:.2f}%，表格{table_v:.2f}%，差异{diff:.2f}个百分点"
                           for year, text_v, table_v, diff in mismatches)
        issue = Issue(
            issue_id=f"TXTBL{len(issues)+1:05d}",
            level="C",
            category="表文数据不一致",
            round="",
            files=sorted({row["filename"], table["filename"]}),
            item="期后回款比例",
            conclusion=f"正文与表格的期后回款比例不一致，涉及年度：{'、'.join(y for y, *_ in mismatches)}。",
            source_1=f"{row['filename']} {row['position']}：正文期后回款比例 {row['values']}",
            source_2=f"{table['filename']} {table['position']}：表格期后回款比例 {table['values']}",
            diff_amount=max(abs(x[3]) for x in mismatches),
            caliber_analysis=analysis,
            evidence_pages=[f"{row['filename']} {row['position']}", f"{table['filename']} {table['position']}"],
            evidence_ids=[row["evidence_id"], table["evidence_id"]],
            source_1_text=f"{row['filename']} {row['position']}｜{row['text'][:180]}",
            source_2_text=f"{table['filename']} {table['position']}｜{table['text'][:180]}",
            basis="正文按报告期各期默认绑定为2023、2024、2025；表格按列标题年度绑定后逐年比较，未按出现顺序硬比。",
            suggestion="请核对并统一正文描述或表格中的期后回款比例。",
            extraction_confidence=0.82,
            judgement_confidence=0.84,
            need_manual_review=True,
            status="MANUAL_REVIEW_CANDIDATE",
            review_priority="key",
            count_in_exception_total=True,
            display_default=True,
        )
        issues.append(issue)
    return issues


def _parse_text_ratio(ev: Evidence) -> dict | None:
    text = ev.text
    if "期后回款比例" not in text or "分别为" not in text:
        return None
    values = [float(v) for v in PERCENT_RE.findall(text)]
    if len(values) < 3:
        return None
    years = _years_from_text(text)
    if not years:
        if "报告期" not in text:
            return None
        years = ["2023", "2024", "2025"]
    if len(years) < len(values):
        return None
    return {
        "doc_id": ev.doc_id,
        "filename": ev.filename,
        "position": ev.position,
        "evidence_id": ev.evidence_id,
        "paragraph_no": ev.paragraph_no,
        "section": ev.section,
        "text": text,
        "values": {years[i]: values[i] for i in range(min(len(values), len(years)))},
    }


def _years_from_text(text: str) -> list[str]:
    years = []
    range_match = re.search(r"(20[2-3]\d)\s*[-－—至]\s*(20[2-3]\d)\s*年", text)
    if range_match:
        start, end = int(range_match.group(1)), int(range_match.group(2))
        if 2020 <= start <= end <= 2030:
            return [str(y) for y in range(start, end + 1)]
    for year in YEAR_RE.findall(text):
        if year not in years:
            years.append(year)
    return years


def _table_collection_ratios(evidence: list[Evidence]) -> list[dict]:
    grouped: dict[tuple[str, str, str], dict] = defaultdict(lambda: {"values": {}, "texts": [], "positions": [], "ids": []})
    for ev in evidence:
        if ev.kind != "table":
            continue
        blob = " ".join([ev.row_name, ev.col_name, ev.text])
        if "期后回款比例" not in blob:
            continue
        year_match = YEAR_RE.search(ev.col_name) or YEAR_RE.search(blob)
        value_match = PERCENT_RE.search(ev.text)
        if not year_match or not value_match:
            continue
        key = (ev.doc_id, ev.table_no or ev.table_name, ev.row_name or "期后回款比例")
        item = grouped[key]
        item["doc_id"] = ev.doc_id
        item["filename"] = ev.filename
        item["table_no"] = ev.table_no or ev.table_name
        item["position"] = ev.position
        item["evidence_id"] = ev.evidence_id
        item["section"] = ev.section
        item["values"][year_match.group(1)] = float(value_match.group(1))
        item["texts"].append(f"{ev.col_name}={ev.text}")
        item["positions"].append(ev.position)
        item["ids"].append(ev.evidence_id)
    rows = []
    for item in grouped.values():
        if len(item["values"]) >= 2:
            item["text"] = "；".join(item["texts"])
            rows.append(item)
    return rows


def _nearest_table(row: dict, tables: list[dict]) -> dict | None:
    candidates = [t for t in tables if t.get("doc_id") == row["doc_id"]]
    if not candidates:
        return None
    if row.get("section"):
        same_section = [t for t in candidates if t.get("section") == row["section"]]
        if same_section:
            return same_section[0]
    return candidates[0]
