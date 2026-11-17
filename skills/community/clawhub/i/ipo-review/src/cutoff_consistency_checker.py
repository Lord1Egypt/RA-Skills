from __future__ import annotations

import re
from collections import defaultdict

from .models import Evidence, FinancialFact, Issue


CUTOFF_RE = re.compile(r"(?:统计)?(?:截止|截至|截止日期为)\s*(20\d{2})\s*年\s*(\d{1,2})\s*月\s*(?:(\d{1,2})\s*日|末)")
TOPIC_WORDS = ("期后回款", "应收票据期后兑付", "应收款项融资期后兑付", "终止确认")


def check_cutoff_date_consistency(evidence: list[Evidence], facts: list[FinancialFact] | None = None) -> list[Issue]:
    rows: list[dict] = []
    for ev in evidence:
        text = " ".join([ev.section, ev.row_name, ev.col_name, ev.text])
        if not any(word in text for word in TOPIC_WORDS):
            continue
        cutoff = _cutoff_date(text)
        if not cutoff:
            continue
        rows.append({
            "subject": _subject(text),
            "metric": _metric(text),
            "cutoff": cutoff,
            "filename": ev.filename,
            "position": ev.position,
            "evidence_id": ev.evidence_id,
            "text": text,
        })
    groups: dict[tuple[str, str], list[dict]] = defaultdict(list)
    for row in rows:
        groups[(row["subject"], row["metric"])].append(row)

    issues: list[Issue] = []
    for (subject, metric), grouped in groups.items():
        cutoffs = sorted({r["cutoff"] for r in grouped})
        if len(cutoffs) < 2:
            continue
        first_by_cutoff = []
        for cutoff in cutoffs[:4]:
            first_by_cutoff.append(next(r for r in grouped if r["cutoff"] == cutoff))
        issue = Issue(
            issue_id=f"CUT{len(issues)+1:05d}",
            level="C",
            category="截止日口径不一致",
            round="",
            files=sorted({r["filename"] for r in first_by_cutoff}),
            item=f"{subject}|{metric}",
            conclusion=f"同一主题的{metric}出现多个统计截止日：{'、'.join(cutoffs)}。",
            source_1=f"{first_by_cutoff[0]['filename']} {first_by_cutoff[0]['position']}：截至{first_by_cutoff[0]['cutoff']}",
            source_2=f"{first_by_cutoff[1]['filename']} {first_by_cutoff[1]['position']}：截至{first_by_cutoff[1]['cutoff']}",
            caliber_analysis=f"主题：{subject}；指标：{metric}；截止日集合：{'、'.join(cutoffs)}。",
            evidence_pages=[f"{r['filename']} {r['position']}" for r in first_by_cutoff],
            evidence_ids=[r["evidence_id"] for r in first_by_cutoff],
            source_1_text=f"{first_by_cutoff[0]['filename']} {first_by_cutoff[0]['position']}｜{first_by_cutoff[0]['text'][:180]}",
            source_2_text=f"{first_by_cutoff[1]['filename']} {first_by_cutoff[1]['position']}｜{first_by_cutoff[1]['text'][:180]}",
            basis="同一期后回款/兑付事项披露应使用一致统计截止日；截止日不同会导致比例或金额不可直接比较。",
            suggestion="请统一统计截止日，或在披露中说明不同截止日口径及原因。",
            extraction_confidence=0.86,
            judgement_confidence=0.82,
            need_manual_review=True,
            status="MANUAL_REVIEW_CANDIDATE",
            review_priority="key",
            count_in_exception_total=True,
            display_default=True,
        )
        issues.append(issue)
    return issues


def _cutoff_date(text: str) -> str:
    match = CUTOFF_RE.search(text)
    if not match:
        return ""
    year, month, day = match.group(1), int(match.group(2)), match.group(3)
    if day:
        return f"{year}-{month:02d}-{int(day):02d}"
    return f"{year}-{month:02d}"


def _subject(text: str) -> str:
    if "经销" in text:
        return "经销商期后回款"
    if "直销" in text:
        return "直销客户期后回款"
    if "应收票据" in text:
        return "应收票据期后兑付"
    if "应收款项融资" in text:
        return "应收款项融资期后兑付"
    if "应收账款" in text:
        return "应收账款期后回款"
    return "期后回款"


def _metric(text: str) -> str:
    if "兑付比例" in text:
        return "期后兑付比例"
    if "兑付金额" in text:
        return "期后兑付金额"
    if "比例" in text or "%" in text:
        return "期后回款比例"
    if "金额" in text:
        return "期后回款金额"
    return "期后回款"
