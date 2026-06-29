#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""score_meeting.py — CLI entry for meeting-quality-scorer."""
from __future__ import annotations
import argparse
import sys
from pathlib import Path


def _check_deps() -> None:
    import importlib.util
    missing = []
    for mod, pip in [("openai", "openai"), ("yaml", "pyyaml"), ("jinja2", "jinja2")]:
        if not importlib.util.find_spec(mod):
            missing.append(pip)
    if missing:
        print(f"[meeting-quality-scorer] Missing: {', '.join(missing)}\nRun: pip install -r requirements.txt", file=sys.stderr)
        sys.exit(2)


def main(argv: list[str] | None = None) -> int:
    _check_deps()

    from scripts.parser import parse
    from scripts.scorer import participation_score, compute_total
    from scripts.llm_adapter import resolve_config, LLMClient, LLMUnavailableError
    from scripts.analyzer import run_analysis
    from scripts.reporter import render_markdown, render_html, save_reports

    p = argparse.ArgumentParser(description="Score meeting quality from a transcript.")
    p.add_argument("--input", required=True, help="Transcript text file")
    p.add_argument("--out-md", default="report.md")
    p.add_argument("--out-html", default="report.html")
    p.add_argument("--config", default=None)
    args = p.parse_args(argv)

    transcript = Path(args.input).read_text(encoding="utf-8")
    if len(transcript.strip()) < 100:
        print("[score_meeting] Transcript too short (< 100 chars)", file=sys.stderr)
        return 2
    if len(transcript) > 200_000:
        print("[score_meeting] Transcript too large (> 200k chars)", file=sys.stderr)
        return 2

    parsed = parse(transcript)

    cfg = resolve_config(env_prefix="MQS", config_path=args.config)
    llm = LLMClient(cfg["base_url"], cfg["api_key"], cfg["model"])

    try:
        analysis = run_analysis(transcript, parsed, llm)
    except LLMUnavailableError as e:
        print(f"[score_meeting] LLM unavailable: {e}", file=sys.stderr)
        Path("partial-report.md").write_text(f"# Partial Report\nLLM unavailable: {e}\n", encoding="utf-8")
        return 1

    p_score = participation_score(parsed["utterances"])
    scores = compute_total(
        decision=analysis["decision_clarity"],
        time_eff=analysis["time_efficiency"],
        participation=p_score,
    )
    scores["participation"] = p_score

    md = render_markdown(analysis, parsed, scores)
    html = render_html(analysis, parsed, scores)
    save_reports(md, html, args.out_md, args.out_html)
    print(f"[score_meeting] 报告已生成: {args.out_md}, {args.out_html}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
