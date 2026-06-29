#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""reporter.py — Markdown + HTML report rendering."""
from __future__ import annotations
from datetime import date
from pathlib import Path
import jinja2


def _get_env() -> jinja2.Environment:
    tmpl_dir = Path(__file__).parent.parent / "templates"
    loader = jinja2.FileSystemLoader(str(tmpl_dir))
    return jinja2.Environment(loader=loader, autoescape=False)


def render_markdown(analysis: dict, stats: dict) -> str:
    ctx = {
        "date": date.today().isoformat(),
        "jargon": analysis.get("jargon", []),
        "culture": analysis.get("culture", {}),
        "resume_match": analysis.get("resume_match"),
        "negotiation": analysis.get("negotiation", {}),
        "red_flag_keywords": stats.get("red_flag_keywords", {}),
    }
    env = _get_env()
    tmpl = env.get_template("report.md.j2")
    return tmpl.render(**ctx)


def render_html(analysis: dict, stats: dict) -> str:
    ctx = {
        "date": date.today().isoformat(),
        "jargon": analysis.get("jargon", []),
        "culture": analysis.get("culture", {}),
        "resume_match": analysis.get("resume_match"),
        "negotiation": analysis.get("negotiation", {}),
        "red_flag_keywords": stats.get("red_flag_keywords", {}),
    }
    env = _get_env()
    tmpl = env.get_template("report.html.j2")
    return tmpl.render(**ctx)


def save_reports(md_str: str, html_str: str, out_md: str, out_html: str) -> None:
    Path(out_md).write_text(md_str, encoding="utf-8")
    Path(out_html).write_text(html_str, encoding="utf-8")
