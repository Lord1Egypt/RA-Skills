#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""jd_analyze.py — CLI entry for jd-truth-detector."""
from __future__ import annotations
import argparse
import sys
from pathlib import Path


def main(argv: list[str] | None = None) -> int:
    from scripts.input_parser import (
        detect_input_type, fetch_url, parse_file, parse_resume, validate_jd,
        InputFetchError, UnsupportedFormatError, InputTooShortError, InputTooLargeError,
    )
    from scripts.pre_scanner import scan
    from scripts.llm_adapter import resolve_config, LLMClient, LLMUnavailableError
    from scripts.analyzer import run_analysis
    from scripts.reporter import render_markdown, render_html, save_reports

    p = argparse.ArgumentParser(description="Reverse-engineer job descriptions.")
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument("--jd-text")
    g.add_argument("--jd-url")
    g.add_argument("--jd-file")
    p.add_argument("--resume-text", default=None)
    p.add_argument("--resume-file", default=None)
    p.add_argument("--out-md", default="report.md")
    p.add_argument("--out-html", default="report.html")
    p.add_argument("--config", default=None)
    args = p.parse_args(argv)

    # Parse JD input
    try:
        input_type = detect_input_type(jd_text=args.jd_text, jd_url=args.jd_url, jd_file=args.jd_file)
        if input_type == "text":
            jd_text = args.jd_text
        elif input_type == "url":
            jd_text = fetch_url(args.jd_url)
        else:  # file
            jd_text = parse_file(args.jd_file)
        jd_text = validate_jd(jd_text)
    except (InputFetchError, UnsupportedFormatError, InputTooShortError, InputTooLargeError) as e:
        print(f"[jd_analyze] {e}", file=sys.stderr)
        return 2

    # Parse resume (optional)
    resume_text = None
    if args.resume_file:
        try:
            resume_text = parse_resume(args.resume_file)
        except Exception as e:
            print(f"[jd_analyze] Resume parse failed: {e}", file=sys.stderr)
            return 2
    elif args.resume_text:
        resume_text = parse_resume(args.resume_text)

    # Pre-scan
    stats = scan(jd_text)

    # LLM config
    cfg = resolve_config(env_prefix="JTD", config_path=args.config)
    llm = LLMClient(cfg["base_url"], cfg["api_key"], cfg["model"])

    # Run analysis
    try:
        analysis = run_analysis(jd_text, resume_text, stats, llm)
    except LLMUnavailableError as e:
        print(f"[jd_analyze] LLM unavailable: {e}", file=sys.stderr)
        Path("partial-report.md").write_text(f"# Partial Report\nPre-scan complete:\n{stats}\nLLM unavailable: {e}\n", encoding="utf-8")
        return 1

    # Render
    md = render_markdown(analysis, stats)
    html = render_html(analysis, stats)
    save_reports(md, html, args.out_md, args.out_html)
    print(f"[jd_analyze] 报告已生成: {args.out_md}, {args.out_html}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
