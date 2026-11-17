from __future__ import annotations

import re
from collections import defaultdict

from .models import Evidence, Issue


def check_format(evidence: list[Evidence]) -> list[Issue]:
    issues: list[Issue] = []
    period_tips: dict[str, int] = defaultdict(int)
    for ev in evidence:
        text = ev.text
        if "如下表所示" in text:
            nearby_table = any(
                x.doc_id == ev.doc_id
                and x.kind == "table"
                and (x.page in {ev.page, ev.page + 1} or x.page == 0 or ev.page == 0)
                for x in evidence
            )
            if not nearby_table:
                issues.append(_issue(ev, "格式及交叉引用问题", "出现“如下表所示”，但相邻位置未解析到表格。", "补充对应表格，或调整引用表述。", "C"))
        if _has_unbalanced_brackets(text):
            issues.append(_issue(ev, "格式及文字问题", "括号疑似未闭合。", "补齐括号或删除多余括号。", "C"))
        if "报告期各期" in text and not re.search(r"20\d{2}", text) and period_tips[ev.doc_id] < 5:
            issues.append(_issue(
                ev,
                "期间表述提示",
                "出现“报告期各期”但本段未列明具体期间，作为低优先级解析提示。",
                "结合前后段落和相邻表格确认报告期范围。",
                "D",
                status="PERIOD_VAGUE",
            ))
            period_tips[ev.doc_id] += 1
    return issues


_LIST_MARKER_CHARS = set("0123456789一二三四五六七八九十①②③④⑤⑥⑦⑧⑨⑩")


def _has_unbalanced_brackets(text: str) -> bool:
    """用栈校验括号是否配对；半角全角统一，并放过中文常见的列表序号（如“1）”“2）”）。

    关键点：遇到右括号且当前没有未配对的左括号时，若它紧跟在数字/中文数字之后，
    判定为列表序号（如“其中：1）……2）……”），不计为多余右括号；
    否则才认定为真正的括号不配对。左括号始终入栈，结尾仍有剩余即未闭合。
    """
    openers = {"（", "("}
    closers = {"）", ")"}
    stack: list[str] = []
    for idx, ch in enumerate(text):
        if ch in openers:
            stack.append(ch)
        elif ch in closers:
            if stack:
                stack.pop()
            else:
                prev = text[idx - 1] if idx > 0 else ""
                if prev in _LIST_MARKER_CHARS:
                    continue  # 列表序号，非多余右括号
                return True  # 真正多余的右括号
    return bool(stack)  # 仍有未闭合的左括号


def _issue(ev: Evidence, category: str, conclusion: str, suggestion: str, level: str, status: str = "MANUAL_REVIEW_CANDIDATE") -> Issue:
    return Issue(
        issue_id="FMT",
        level=level,
        category=category,
        round="",
        files=[ev.filename],
        item=ev.section or ev.question_no or "正文",
        conclusion=conclusion,
        source_1=ev.text,
        caliber_analysis="格式和文字规则检查。",
        evidence_pages=[f"{ev.filename} {ev.position or ('P' + str(ev.page))}"],
        evidence_ids=[ev.evidence_id],
        basis="本地规则命中。",
        suggestion=suggestion,
        extraction_confidence=0.8,
        judgement_confidence=0.55 if level == "D" else 0.65,
        need_manual_review=True,
        status=status,
    )
