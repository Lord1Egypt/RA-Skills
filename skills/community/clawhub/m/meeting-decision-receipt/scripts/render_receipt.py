#!/usr/bin/env python3
"""Deterministically render receipt JSON to Markdown and standalone HTML."""

from __future__ import annotations

import argparse
import html
import json
import re
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
TEMPLATES = ROOT / "templates"

DECISION_LABELS = {
    "confirmed": "已确认",
    "provisional": "暂定",
    "conditional": "条件成立后执行",
    "proposed": "仅为提议",
    "deferred": "延后再议",
    "rejected": "已排除",
    "superseded": "已被后续结论覆盖",
}

COMMITMENT_LABELS = {
    "explicit_commitment": "明确接下",
    "accepted_assignment": "已确认接下",
    "unacknowledged_assignment": "被点名，未确认",
    "implied_assignment": "会议语言指向，未确认",
    "tentative_intent": "仅表达意向",
    "conditional_commitment": "条件满足后执行",
    "unowned": "没人接",
}

NEUTRAL_COMMITMENT_LABELS = {
    "explicit_commitment": "责任已确认",
    "accepted_assignment": "责任已确认",
    "unacknowledged_assignment": "责任待确认",
    "implied_assignment": "责任指向待确认",
    "tentative_intent": "仅表达意向",
    "conditional_commitment": "条件满足后执行",
    "unowned": "负责人待确认",
}

MISSING_LABELS = {
    "owner": "明确负责人",
    "task": "具体动作",
    "due": "截止时间",
    "dependencies": "前置条件",
    "dependency_owner": "前置条件负责人",
    "dependency_due": "前置条件到达时间",
    "acceptance_criteria": "交付标准",
    "confirmation": "被指派方确认",
    "decision": "最终决定",
    "final_approver": "最终确认权",
    "source_evidence": "可核对证据",
}

CLOSE_STATUS_LABELS = {
    "closed": "已结清",
    "needs_confirmation": "待继续确认",
    "no_clear_decision": "未形成明确结论",
    "insufficient_evidence": "证据不足",
}

FIRST_SCREEN_LIMIT = 3
FIRST_SCREEN_OVERFLOW = "另有 {count} 项待确认，见判断依据。"


def _replace(template: str, values: dict[str, str]) -> str:
    rendered = template
    for key, value in values.items():
        rendered = rendered.replace("{{ " + key + " }}", value)
    return rendered


def _current_decisions(data: dict[str, Any], statuses: set[str]) -> list[dict[str, Any]]:
    return [
        item for item in data.get("decisions", [])
        if item.get("current") and item.get("status") in statuses and item.get("confidence") != "low"
    ]


def _due_text(item: dict[str, Any]) -> str:
    original = item.get("due_original")
    resolved = item.get("due_resolved")
    if original and resolved:
        return f"{original}（{resolved}）"
    return original or resolved or "时间待确认"


def _decision_text(item: dict[str, Any]) -> str:
    text = item["statement"]
    extras = []
    if item.get("scope"):
        extras.append(f"范围：{item['scope']}")
    if item.get("condition"):
        extras.append(f"条件：{item['condition']}")
    return text + (f"（{'；'.join(extras)}）" if extras else "")


def _commitment_text(item: dict[str, Any]) -> str:
    owner = item.get("owner") or "负责人待确认"
    text = f"{owner}：{item['task']}"
    if item.get("type") in {"explicit_commitment", "accepted_assignment", "conditional_commitment"} or item.get("due_original"):
        text += f"｜{_due_text(item)}"
    if item.get("dependencies"):
        text += f"｜前置：{'、'.join(item['dependencies'])}"
    if item.get("missing_fields"):
        text += f"｜仍缺：{'、'.join(MISSING_LABELS.get(field, field) for field in item['missing_fields'])}"
    return text


def _status_clauses(data: dict[str, Any], neutral: bool) -> list[str]:
    summary = data["summary"]
    decided = summary["confirmed_decisions"]
    temporary = summary["provisional_decisions"] + summary["conditional_decisions"]
    committed = summary["explicit_commitments"]
    open_count = summary["open_loops"]
    if neutral:
        return [
            f"{decided} 项明确结论",
            f"{temporary} 项待条件确认",
            f"{committed} 项责任已确认",
            f"{open_count} 项仍待确认",
        ]
    return [
        f"{decided} 项已确认",
        f"{temporary} 项暂定或附条件",
        f"{committed} 项明确接下",
        f"{open_count} 件事待确认",
    ]


def _md_list(items: list[str], empty: str) -> str:
    if not items:
        return f"- {empty}"
    return "\n".join(f"- {item}" for item in items)


def _md_numbered(items: list[str], empty: str) -> str:
    values = items or [empty]
    return "\n".join(f"{index}. {item}" for index, item in enumerate(values, start=1))


def _html_list(items: list[str], empty: str, css_class: str = "") -> str:
    values = items or [empty]
    class_attr = f' class="{css_class}"' if css_class else ""
    return '<ul role="list">' + "".join(f"<li{class_attr}>{html.escape(item)}</li>" for item in values) + "</ul>"


def _html_numbered(items: list[str], empty: str) -> str:
    values = items or [empty]
    return '<ol class="feishu-numbered">' + "".join(f"<li>{html.escape(item)}</li>" for item in values) + "</ol>"


def _limited(items: list[str], limit: int, overflow_text: str) -> list[str]:
    visible = items[:limit]
    if len(items) > limit:
        visible.append(overflow_text.format(count=len(items) - limit))
    return visible


def _status_html(clauses: list[str]) -> str:
    parts = []
    for clause in clauses:
        match = re.match(r"^(\d+)\s*(.*)$", clause)
        if match:
            parts.append(
                '<span><strong>'
                + html.escape(match.group(1))
                + "</strong><small>"
                + html.escape(match.group(2))
                + "</small></span>"
            )
        else:
            parts.append(f"<span><small>{html.escape(clause)}</small></span>")
    return "".join(parts)


def _open_loop_text(item: dict[str, Any], include_risk: bool = True) -> str:
    missing = "、".join(MISSING_LABELS.get(field, field) for field in item["missing"])
    text = f"{item['topic']}：仍缺{missing}"
    if include_risk:
        text += f"。{item['risk']}"
    return text


def _open_loops_html(items: list[dict[str, Any]], limit: int = FIRST_SCREEN_LIMIT) -> str:
    visible = items[:limit]
    rows = []
    for item in visible:
        tags = "".join(
            f'<span class="gap-tag">缺{html.escape(MISSING_LABELS.get(field, field))}</span>'
            for field in item["missing"]
        )
        rows.append(
            '<li class="open-loop-item">'
            f'<strong>{html.escape(item["topic"])}</strong>'
            f'<div class="gap-tags">{tags}</div>'
            f'<p>{html.escape(item["risk"])}</p>'
            "</li>"
        )
    if len(items) > limit:
        rows.append(
            '<li class="open-loop-overflow">'
            + html.escape(FIRST_SCREEN_OVERFLOW.format(count=len(items) - limit))
            + "</li>"
        )
    if not rows:
        rows.append('<li class="open-loop-empty">当前没有待确认事项。</li>')
    return '<ol class="open-loop-list">' + "".join(rows) + "</ol>"


def _confirmation_html(message: str) -> str:
    intro = []
    numbered = []
    closing = []
    for raw_line in message.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        match = re.match(r"^\d+[\.、]\s*(.+)$", line)
        if match:
            numbered.append(match.group(1))
        elif numbered:
            closing.append(line)
        else:
            intro.append(line)
    blocks = []
    if intro:
        blocks.append(f'<p class="confirmation-intro">{html.escape(" ".join(intro))}</p>')
    if numbered:
        blocks.append(
            '<ol class="confirmation-list">'
            + "".join(f"<li>{html.escape(item)}</li>" for item in numbered)
            + "</ol>"
        )
    if closing:
        blocks.append(f'<p class="confirmation-closing">{html.escape(" ".join(closing))}</p>')
    return "".join(blocks) or f"<p>{html.escape(message)}</p>"


def _bundle_actions_html() -> str:
    return """
    <section class="output-bar" aria-label="会议纪要输出">
      <div>
        <span class="output-kicker">一键输出会议纪要</span>
        <p>同一份审计结果，按使用场景重排。</p>
      </div>
      <nav aria-label="纪要版本">
        <a href="minutes-personal.html">给自己</a>
        <a href="minutes-executive.html">给管理层 · 飞书文档</a>
      </nav>
    </section>
    """.strip()


def _bundle_actions_markdown() -> str:
    return "**继续输出：** [给自己](minutes-personal.md) · [给管理层 · 飞书文档](minutes-executive.md)"


def _bundle_nav_html(current: str) -> str:
    links = [
        ("receipt", "receipt.html", "结论与待办"),
        ("personal", "minutes-personal.html", "给自己"),
        ("executive", "minutes-executive.html", "给管理层 · 飞书文档"),
    ]
    return "".join(
        f'<a href="{href}"' + (' aria-current="page"' if key == current else "") + f">{label}</a>"
        for key, href, label in links
    )


def _bundle_nav_markdown() -> str:
    return "[结论与待办](receipt.md) · [给自己](minutes-personal.md) · [给管理层 · 飞书文档](minutes-executive.md)"


def _evidence_markdown(data: dict[str, Any], neutral: bool = False) -> str:
    blocks = []
    commitment_labels = NEUTRAL_COMMITMENT_LABELS if neutral else COMMITMENT_LABELS
    for item in data.get("decisions", []):
        heading = f"{item['id']} · {DECISION_LABELS[item['status']]} · {item['statement']}"
        quotes = []
        for evidence in item["evidence"]:
            locator = evidence.get("timestamp") or evidence.get("paragraph")
            quotes.append(f"> [{locator}] {evidence['speaker']}：\n> “{evidence['quote']}”")
        blocks.append(f"**{heading}**\n\n" + "\n\n".join(quotes))
    for item in data.get("commitments", []):
        heading = f"{item['id']} · {commitment_labels[item['type']]} · {item['task']}"
        quotes = []
        for evidence in item["evidence"]:
            locator = evidence.get("timestamp") or evidence.get("paragraph")
            quotes.append(f"> [{locator}] {evidence['speaker']}：\n> “{evidence['quote']}”")
        blocks.append(f"**{heading}**\n\n" + "\n\n".join(quotes))
    if data.get("open_loops"):
        loop_lines = []
        for item in data["open_loops"]:
            missing = "、".join(MISSING_LABELS.get(field, field) for field in item["missing"])
            loop_lines.append(f"- **{item['id']} · {item['topic']}**：仍缺{missing}。{item['risk']}")
        blocks.append("**完整待确认事项**\n\n" + "\n".join(loop_lines))
    return "\n\n".join(blocks) or "没有可展示的判断证据。"


def _evidence_html(data: dict[str, Any], neutral: bool = False) -> str:
    blocks = []
    commitment_labels = NEUTRAL_COMMITMENT_LABELS if neutral else COMMITMENT_LABELS
    for item in data.get("decisions", []):
        title = f"{item['id']} · {DECISION_LABELS[item['status']]} · {item['statement']}"
        quotes = []
        for evidence in item["evidence"]:
            locator = evidence.get("timestamp") or evidence.get("paragraph")
            quotes.append(
                '<blockquote><span class="locator">'
                + html.escape(str(locator))
                + " · "
                + html.escape(evidence["speaker"])
                + "</span>"
                + html.escape(evidence["quote"])
                + "</blockquote>"
            )
        blocks.append(f'<div class="evidence-item"><h4>{html.escape(title)}</h4>{"".join(quotes)}</div>')
    for item in data.get("commitments", []):
        title = f"{item['id']} · {commitment_labels[item['type']]} · {item['task']}"
        quotes = []
        for evidence in item["evidence"]:
            locator = evidence.get("timestamp") or evidence.get("paragraph")
            quotes.append(
                '<blockquote><span class="locator">'
                + html.escape(str(locator))
                + " · "
                + html.escape(evidence["speaker"])
                + "</span>"
                + html.escape(evidence["quote"])
                + "</blockquote>"
            )
        blocks.append(f'<div class="evidence-item"><h4>{html.escape(title)}</h4>{"".join(quotes)}</div>')
    if data.get("open_loops"):
        rows = []
        for item in data["open_loops"]:
            missing = "、".join(MISSING_LABELS.get(field, field) for field in item["missing"])
            text = f"仍缺{missing}。{item['risk']}"
            rows.append(f"<li><strong>{html.escape(item['id'] + ' · ' + item['topic'])}</strong>：{html.escape(text)}</li>")
        blocks.append('<div class="evidence-item"><h4>完整待确认事项</h4><ul>' + "".join(rows) + "</ul></div>")
    return "".join(blocks) or "<p>没有可展示的判断证据。</p>"


def build_view(data: dict[str, Any]) -> dict[str, Any]:
    neutral = bool(data.get("safety", {}).get("neutral_language_mode"))
    confirmed = _current_decisions(data, {"confirmed", "rejected"})
    provisional = _current_decisions(data, {"provisional"})
    conditional = _current_decisions(data, {"conditional"})
    core_count = len(confirmed) + len(provisional) + len(conditional)
    commitments = data.get("commitments", [])
    owned = [item for item in commitments if item.get("type") in {"explicit_commitment", "accepted_assignment", "conditional_commitment"} and item.get("confidence") != "low"]
    unconfirmed = [item for item in commitments if item.get("type") in {"unacknowledged_assignment", "implied_assignment"}]
    tentative = [item for item in commitments if item.get("type") == "tentative_intent"]
    unowned = [item for item in commitments if item.get("type") == "unowned"]
    title = data["meeting"]["title"]
    date_text = data["meeting"].get("date") or "日期未提供"
    product_title = "会议结论与责任审计" if neutral else "会议纪要验真器"
    product_hook = "结论、责任与待确认事项" if neutral else "定了啥，谁真接活了？"
    intro = "审计结果已整理。" if neutral else "整理好了。"
    decision_empty = "本场未发现明确结论。" if core_count == 0 else "本区暂无项目。"
    responsibility_title = "责任确认" if neutral else "谁负责"
    open_title = "待确认事项"
    footer = "发送前请核对相关人员、时间与适用范围。" if neutral else "会开完，把下一步说清楚。"
    status_clauses = _status_clauses(data, neutral)
    all_open_loops = [
        f"{item['topic']}：仍缺{'、'.join(MISSING_LABELS.get(field, field) for field in item['missing'])}。{item['risk']}"
        for item in data.get("open_loops", [])
    ]
    visible_open_loops = _limited(all_open_loops, FIRST_SCREEN_LIMIT, FIRST_SCREEN_OVERFLOW)
    return {
        "neutral": neutral,
        "product_title": product_title,
        "product_hook": product_hook,
        "title": title,
        "date": date_text,
        "intro": intro,
        "status_line": " · ".join(status_clauses),
        "status_clauses": status_clauses,
        "decision_empty": decision_empty,
        "confirmed": _limited(
            [_decision_text(item) for item in confirmed],
            FIRST_SCREEN_LIMIT,
            FIRST_SCREEN_OVERFLOW,
        ),
        "provisional": _limited(
            [_decision_text(item) for item in provisional],
            FIRST_SCREEN_LIMIT,
            FIRST_SCREEN_OVERFLOW,
        ),
        "conditional": _limited(
            [_decision_text(item) for item in conditional],
            FIRST_SCREEN_LIMIT,
            FIRST_SCREEN_OVERFLOW,
        ),
        "owned": _limited(
            [_commitment_text(item) for item in owned],
            FIRST_SCREEN_LIMIT,
            FIRST_SCREEN_OVERFLOW,
        ),
        "unconfirmed": _limited(
            [_commitment_text(item) for item in unconfirmed],
            FIRST_SCREEN_LIMIT,
            FIRST_SCREEN_OVERFLOW,
        ),
        "tentative": _limited(
            [_commitment_text(item) for item in tentative],
            FIRST_SCREEN_LIMIT,
            FIRST_SCREEN_OVERFLOW,
        ),
        "unowned": _limited(
            [_commitment_text(item) for item in unowned],
            FIRST_SCREEN_LIMIT,
            FIRST_SCREEN_OVERFLOW,
        ),
        "open_loops": visible_open_loops,
        "open_loop_items": data.get("open_loops", []),
        "responsibility_title": responsibility_title,
        "open_title": open_title,
        "confirmation_message": data["confirmation_message"],
        "footer": footer,
    }


def build_personal_minutes_view(data: dict[str, Any]) -> dict[str, Any]:
    neutral = bool(data.get("safety", {}).get("neutral_language_mode"))
    core_statuses = {"confirmed", "provisional", "conditional", "rejected"}
    current_decisions = [
        item for item in data.get("decisions", [])
        if item.get("current") and item.get("status") in core_statuses and item.get("confidence") != "low"
    ]
    archived_decisions = [
        item for item in data.get("decisions", [])
        if item.get("status") in {"proposed", "deferred", "superseded"}
    ]
    labels = NEUTRAL_COMMITMENT_LABELS if neutral else COMMITMENT_LABELS
    current_lines = [
        f"[{DECISION_LABELS[item['status']]}] {_decision_text(item)}"
        for item in current_decisions
    ]
    if not current_lines:
        current_lines = ["本场未形成明确结论。"]
    commitment_lines = [
        f"[{labels[item['type']]}] {_commitment_text(item)}"
        for item in data.get("commitments", [])
    ]
    archive_lines = [
        f"[{DECISION_LABELS[item['status']]}] {_decision_text(item)}"
        for item in archived_decisions
    ]
    return {
        "neutral": neutral,
        "title": data["meeting"]["title"],
        "date": data["meeting"].get("date") or "日期未提供",
        "status_line": " · ".join(_status_clauses(data, neutral)),
        "current_decisions": current_lines,
        "commitments": commitment_lines,
        "open_loops": [_open_loop_text(item) for item in data.get("open_loops", [])],
        "archive": archive_lines,
        "confirmation_message": data["confirmation_message"],
        "evidence": _evidence_markdown(data, neutral),
        "evidence_html": _evidence_html(data, neutral),
        "footer": (
            "自用工作底稿，仅保留经审计的决定、责任、待确认事项和短证据。"
            if not neutral
            else "内部工作底稿，仅保留经审计的结论、责任、待确认事项和短证据。"
        ),
    }


def build_executive_minutes_view(data: dict[str, Any]) -> dict[str, Any]:
    core_decisions = [
        item for item in data.get("decisions", [])
        if item.get("current")
        and item.get("status") in {"confirmed", "provisional", "conditional", "rejected"}
        and item.get("confidence") != "low"
    ]
    owned = [
        item for item in data.get("commitments", [])
        if item.get("type") in {"explicit_commitment", "accepted_assignment", "conditional_commitment"}
        and item.get("confidence") != "low"
    ]
    open_loops = data.get("open_loops", [])
    escalations = [
        item for item in open_loops
        if {"decision", "final_approver"} & set(item.get("missing", []))
    ]
    escalation_ids = {item.get("id") for item in escalations}
    coordination_loops = [item for item in open_loops if item.get("id") not in escalation_ids]
    decision_lines = [
        f"[{DECISION_LABELS[item['status']]}] {_decision_text(item)}"
        for item in core_decisions
    ]
    if not decision_lines:
        decision_lines = ["本场未形成明确结论。"]
    decision_lines = _limited(decision_lines, 3, "另有 {count} 项当前结论，见结论与待办清单。")
    progress_lines = _limited(
        [_commitment_text(item) for item in owned],
        3,
        "另有 {count} 项责任已确认，见自用执行纪要。",
    )
    risk_lines = _limited(
        [_open_loop_text(item, include_risk=False) for item in coordination_loops],
        3,
        "另有 {count} 项待协调，见结论与待办清单。",
    )
    escalation_lines = _limited(
        [_open_loop_text(item, include_risk=False) for item in escalations],
        3,
        "另有 {count} 项需确认，见结论与待办清单。",
    )
    next_nodes = []
    for item in owned:
        if item.get("due_original") or item.get("due_resolved"):
            next_nodes.append(f"{item.get('owner') or '负责人待确认'} · {item['task']} · {_due_text(item)}")
    for item in core_decisions:
        if item.get("status") == "conditional" and item.get("condition"):
            scoped_statement = item["statement"]
            if item.get("scope"):
                scoped_statement += f"（范围：{item['scope']}）"
            next_nodes.append(f"条件确认 · {item['condition']} · {scoped_statement}")
    deferred_decisions = [
        item for item in data.get("decisions", [])
        if item.get("current")
        and item.get("status") == "deferred"
        and item.get("confidence") != "low"
    ]
    for item in deferred_decisions:
        next_nodes.append(f"待复议 · {_decision_text(item)}")

    summary_items = [_decision_text(item) for item in core_decisions[:3]]
    if summary_items:
        qualifier = "，重点包括" if len(core_decisions) > 3 else ""
        executive_summary = f"本次会议形成 {len(core_decisions)} 项当前结论{qualifier}：{'；'.join(summary_items)}。"
    else:
        executive_summary = "本场未形成明确结论，当前内容以待确认事项为主。"
    if open_loops:
        executive_summary += f"另有 {len(open_loops)} 项待协调。"
    else:
        executive_summary += "当前未发现待协调事项。"

    return {
        "title": data["meeting"]["title"],
        "date": data["meeting"].get("date") or "日期未提供",
        "close_status": CLOSE_STATUS_LABELS.get(data.get("close_status"), "状态待确认"),
        "status_line": " · ".join(_status_clauses(data, True)),
        "executive_summary": executive_summary,
        "decisions": decision_lines,
        "progress": progress_lines,
        "risks": risk_lines,
        "escalations": escalation_lines,
        "next_nodes": _limited(next_nodes, 3, "另有 {count} 个时间或条件节点，见自用执行纪要。"),
        "footer": "内容根据会议记录中的可核对结论整理；复制到飞书后请核对适用范围、时间和接收人。",
    }


def render_markdown(data: dict[str, Any], bundle: bool = False) -> str:
    view = build_view(data)
    template = (TEMPLATES / "receipt.template.md").read_text(encoding="utf-8")
    values = {
        "product_title": view["product_title"],
        "product_hook": view["product_hook"],
        "title": view["title"],
        "date": view["date"],
        "intro": view["intro"],
        "status_line": view["status_line"],
        "bundle_actions": _bundle_actions_markdown() if bundle else "",
        "confirmed_decisions": _md_list(view["confirmed"], view["decision_empty"]),
        "provisional_decisions": _md_list(view["provisional"], "暂无暂定项。"),
        "conditional_decisions": _md_list(view["conditional"], "暂无条件决定。"),
        "responsibility_title": view["responsibility_title"],
        "owned_commitments": _md_list(view["owned"], "暂无明确接下项。"),
        "unconfirmed_commitments": _md_list(view["unconfirmed"], "暂无未确认指派。"),
        "tentative_commitments": _md_list(view["tentative"], "暂无表达意向项。"),
        "unowned_commitments": _md_list(view["unowned"], "暂无无人负责项。"),
        "open_title": view["open_title"],
        "open_loops": _md_list(view["open_loops"], "当前没有待确认事项。"),
        "confirmation_message": view["confirmation_message"],
        "evidence": _evidence_markdown(data, view["neutral"]),
        "footer": view["footer"],
    }
    return _replace(template, values).rstrip() + "\n"


def render_html(data: dict[str, Any], bundle: bool = False) -> str:
    view = build_view(data)
    template = (TEMPLATES / "receipt.html").read_text(encoding="utf-8")
    css = (TEMPLATES / "receipt.css").read_text(encoding="utf-8")
    values = {
        "css": css,
        "product_title": html.escape(view["product_title"]),
        "product_hook": html.escape(view["product_hook"]),
        "title": html.escape(view["title"]),
        "date": html.escape(view["date"]),
        "intro": html.escape(view["intro"]),
        "status_line": _status_html(view["status_clauses"]),
        "bundle_actions": _bundle_actions_html() if bundle else "",
        "confirmed_decisions": _html_list(view["confirmed"], view["decision_empty"]),
        "provisional_decisions": _html_list(view["provisional"], "暂无暂定项。"),
        "conditional_decisions": _html_list(view["conditional"], "暂无条件决定。"),
        "responsibility_title": html.escape(view["responsibility_title"]),
        "owned_commitments": _html_list(view["owned"], "暂无明确接下项。", "state-owned"),
        "unconfirmed_commitments": _html_list(view["unconfirmed"], "暂无未确认指派。", "state-warning"),
        "tentative_commitments": _html_list(view["tentative"], "暂无表达意向项。", "state-muted"),
        "unowned_commitments": _html_list(view["unowned"], "暂无无人负责项。", "state-muted"),
        "open_title": html.escape(view["open_title"]),
        "open_loops": _open_loops_html(view["open_loop_items"]),
        "confirmation_message": _confirmation_html(view["confirmation_message"]),
        "evidence": _evidence_html(data, view["neutral"]),
        "footer": html.escape(view["footer"]),
    }
    body_class = "neutral" if view["neutral"] else "standard"
    values["body_class"] = body_class
    return _replace(template, values).rstrip() + "\n"


def render_personal_markdown(data: dict[str, Any], bundle: bool = False) -> str:
    view = build_personal_minutes_view(data)
    template = (TEMPLATES / "minutes-personal.template.md").read_text(encoding="utf-8")
    values = {
        "bundle_nav": _bundle_nav_markdown() if bundle else "",
        "title": view["title"],
        "date": view["date"],
        "status_line": view["status_line"],
        "current_decisions": _md_list(view["current_decisions"], "本场未形成明确结论。"),
        "commitments": _md_list(view["commitments"], "会议材料未提供可核对的执行事项。"),
        "open_loops": _md_list(view["open_loops"], "当前没有待确认事项。"),
        "archive": _md_list(view["archive"], "没有需要留档的提议、延后或覆盖记录。"),
        "confirmation_message": view["confirmation_message"],
        "evidence": view["evidence"],
        "footer": view["footer"],
    }
    return _replace(template, values).rstrip() + "\n"


def render_personal_html(data: dict[str, Any], bundle: bool = False) -> str:
    view = build_personal_minutes_view(data)
    template = (TEMPLATES / "minutes-personal.html").read_text(encoding="utf-8")
    css = (TEMPLATES / "minutes.css").read_text(encoding="utf-8")
    values = {
        "css": css,
        "bundle_nav": _bundle_nav_html("personal") if bundle else "",
        "title": html.escape(view["title"]),
        "date": html.escape(view["date"]),
        "status_line": html.escape(view["status_line"]),
        "current_decisions": _html_list(view["current_decisions"], "本场未形成明确结论。"),
        "commitments": _html_list(view["commitments"], "会议材料未提供可核对的执行事项。"),
        "open_loops": _html_list(view["open_loops"], "当前没有待确认事项。"),
        "archive": _html_list(view["archive"], "没有需要留档的提议、延后或覆盖记录。"),
        "confirmation_message": _confirmation_html(view["confirmation_message"]),
        "evidence": view["evidence_html"],
        "footer": html.escape(view["footer"]),
        "body_class": "neutral" if view["neutral"] else "personal",
    }
    return _replace(template, values).rstrip() + "\n"


def render_executive_markdown(data: dict[str, Any], bundle: bool = False) -> str:
    view = build_executive_minutes_view(data)
    template = (TEMPLATES / "minutes-executive.template.md").read_text(encoding="utf-8")
    values = {
        "title": view["title"],
        "date": view["date"],
        "close_status": view["close_status"],
        "status_line": view["status_line"],
        "executive_summary": view["executive_summary"],
        "decisions": _md_numbered(view["decisions"], "本场未形成明确结论。"),
        "progress": _md_numbered(view["progress"], "会议材料未提供已确认的责任事项。"),
        "risks": _md_numbered(view["risks"], "当前没有待协调事项。"),
        "escalation_section": (
            "## 四、待明确确认权\n\n" + _md_numbered(view["escalations"], "")
            if view["escalations"]
            else ""
        ),
        "next_nodes_title": "五、下个节点" if view["escalations"] else "四、下个节点",
        "next_nodes": _md_numbered(view["next_nodes"], "会议材料未提供明确的下个时间或条件节点。"),
        "footer": view["footer"],
    }
    return _replace(template, values).rstrip() + "\n"


def render_executive_html(data: dict[str, Any], bundle: bool = False) -> str:
    view = build_executive_minutes_view(data)
    template = (TEMPLATES / "minutes-executive.html").read_text(encoding="utf-8")
    css = (TEMPLATES / "minutes.css").read_text(encoding="utf-8")
    values = {
        "css": css,
        "bundle_nav": _bundle_nav_html("executive") if bundle else "",
        "title": html.escape(view["title"]),
        "date": html.escape(view["date"]),
        "close_status": html.escape(view["close_status"]),
        "status_line": html.escape(view["status_line"]),
        "executive_summary": html.escape(view["executive_summary"]),
        "decisions": _html_numbered(view["decisions"], "本场未形成明确结论。"),
        "progress": _html_numbered(view["progress"], "会议材料未提供已确认的责任事项。"),
        "risks": _html_numbered(view["risks"], "当前没有待协调事项。"),
        "escalation_section": (
            '<section class="minutes-section section-attention feishu-section">'
            "<h2>四、待明确确认权</h2>"
            + _html_numbered(view["escalations"], "")
            + "</section>"
            if view["escalations"]
            else ""
        ),
        "next_nodes_title": "五、下个节点" if view["escalations"] else "四、下个节点",
        "next_nodes": _html_numbered(view["next_nodes"], "会议材料未提供明确的下个时间或条件节点。"),
        "footer": html.escape(view["footer"]),
        "body_class": "executive",
    }
    return _replace(template, values).rstrip() + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description="Render a validated meeting receipt.")
    parser.add_argument("input", help="Receipt JSON path")
    parser.add_argument("--format", choices=["markdown", "html", "both"], default="both")
    parser.add_argument(
        "--view",
        choices=["receipt", "personal", "executive", "bundle"],
        default="receipt",
        help="Render the receipt, one audience view, or the complete three-view bundle",
    )
    parser.add_argument("--output", help="Output file for markdown or html mode")
    parser.add_argument("--output-dir", help="Output directory for both format or bundle view")
    args = parser.parse_args()

    try:
        data = json.loads(Path(args.input).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"render input error: {exc}", file=sys.stderr)
        raise SystemExit(2) from exc

    renderers = {
        "receipt": {"markdown": render_markdown, "html": render_html, "stem": "receipt"},
        "personal": {"markdown": render_personal_markdown, "html": render_personal_html, "stem": "minutes-personal"},
        "executive": {"markdown": render_executive_markdown, "html": render_executive_html, "stem": "minutes-executive"},
    }

    if args.view == "bundle":
        if not args.output_dir:
            parser.error("--output-dir is required with --view bundle")
        output_dir = Path(args.output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        formats = ["markdown", "html"] if args.format == "both" else [args.format]
        suffixes = {"markdown": ".md", "html": ".html"}
        for view_name, config in renderers.items():
            for output_format in formats:
                output_path = output_dir / f"{config['stem']}{suffixes[output_format]}"
                rendered = config[output_format](data, bundle=True)
                output_path.write_text(rendered, encoding="utf-8")
                print(f"rendered {output_path}")
        return

    config = renderers[args.view]
    if args.format == "both":
        if not args.output_dir:
            parser.error("--output-dir is required with --format both")
        output_dir = Path(args.output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        markdown_path = output_dir / f"{config['stem']}.md"
        html_path = output_dir / f"{config['stem']}.html"
        markdown_path.write_text(config["markdown"](data), encoding="utf-8")
        html_path.write_text(config["html"](data), encoding="utf-8")
        print(f"rendered {markdown_path}")
        print(f"rendered {html_path}")
        return

    rendered = config[args.format](data)
    if args.output:
        Path(args.output).write_text(rendered, encoding="utf-8")
        print(f"rendered {args.output}")
    else:
        sys.stdout.write(rendered)


if __name__ == "__main__":
    main()
