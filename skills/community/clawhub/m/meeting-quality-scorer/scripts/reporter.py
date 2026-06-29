#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""reporter.py — Markdown and HTML report rendering."""
from __future__ import annotations
from datetime import date
from pathlib import Path
import jinja2


def _build_context(analysis: dict, parsed: dict, scores: dict) -> dict:
    speaker_stats: dict[str, int] = {}
    for u in parsed.get("utterances", []):
        spk = u.get("speaker")
        if spk:
            speaker_stats[spk] = speaker_stats.get(spk, 0) + len(u.get("text", ""))
    total_chars = sum(speaker_stats.values()) or 1

    recommendations = _generate_recommendations(analysis, scores)

    return {
        "date": date.today().isoformat(),
        "total_score": scores.get("total", 0),
        "degraded": scores.get("degraded", False),
        "decision_score": analysis.get("decision_clarity"),
        "time_score": analysis.get("time_efficiency"),
        "participation_score": scores.get("participation"),
        "decisions": analysis.get("decisions", []),
        "filler_segments": analysis.get("filler_segments", []),
        "speaker_stats": speaker_stats,
        "total_chars": total_chars,
        "recommendations": recommendations,
    }


def _generate_recommendations(analysis: dict, scores: dict) -> list[str]:
    tips = []
    ds = analysis.get("decision_clarity")
    if ds is not None and ds < 60:
        undecided = [d["topic"] for d in analysis.get("decisions", []) if not d.get("decided")]
        if undecided:
            tips.append(f"以下议题未形成决议，下次会议前请跟进：{', '.join(undecided[:3])}")
        tips.append("每个议题结束时明确 owner 和 deadline")
    ts = analysis.get("time_efficiency")
    if ts is not None and ts < 80:
        tips.append("控制闲聊时间，可指定一人负责 time-keeping")
    ps = scores.get("participation")
    if ps is not None and ps < 50:
        tips.append("发言分布不均衡，主持人可主动 cue 沉默参与者")
    if not tips:
        tips.append("会议质量良好，保持现有节奏")
    return tips


def _get_env() -> jinja2.Environment:
    tmpl_dir = Path(__file__).parent.parent / "templates"
    loader = jinja2.FileSystemLoader(str(tmpl_dir))
    env = jinja2.Environment(loader=loader, autoescape=False)
    return env


def render_markdown(analysis: dict, parsed: dict, scores: dict) -> str:
    ctx = _build_context(analysis, parsed, scores)
    env = _get_env()
    tmpl = env.get_template("report.md.j2")
    return tmpl.render(**ctx)


def render_html(analysis: dict, parsed: dict, scores: dict) -> str:
    ctx = _build_context(analysis, parsed, scores)
    env = _get_env()
    tmpl = env.get_template("report.html.j2")
    return tmpl.render(**ctx)


def save_reports(md_str: str | None, html_str: str | None, out_md: str | None, out_html: str | None) -> None:
    if md_str and out_md:
        Path(out_md).write_text(md_str, encoding="utf-8")
    if html_str and out_html:
        Path(out_html).write_text(html_str, encoding="utf-8")
