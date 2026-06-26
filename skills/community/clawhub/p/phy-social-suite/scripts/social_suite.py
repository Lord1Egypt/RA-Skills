#!/usr/bin/env python3
"""
phy-social-suite — Unified Social Media Content Pipeline

One command to run the full flywheel:
  1. Pull relevant atoms from your content library (phy-content-compound)
  2. Audit AI signature of your draft (phy-content-humanizer-audit)
  3. Pre-flight platform rules check (phy-platform-rules-engine)
  4. (Optional) Compare against your post forensics data

Input: draft text + platform + (optional) content library path
Output: combined report with atoms, AI audit, rules check, and improvement plan

Zero external dependencies — orchestrates the other 4 flywheel scripts.
"""

from __future__ import annotations

import importlib.util
import json
import os
import sys
import textwrap
from pathlib import Path


# ─── Dynamic import helpers ───────────────────────────────────────────

def _import_from_path(module_name: str, file_path: str):
    """Import a Python module from an absolute path."""
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    if spec is None or spec.loader is None:
        return None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _find_skill_script(skill_dir_name: str, script_name: str) -> str | None:
    """Find a skill script in standard locations."""
    candidates = [
        Path.home() / ".claude" / "skills" / skill_dir_name / "scripts" / script_name,
        Path.home() / "Desktop" / "openclaw-skills-publish" / skill_dir_name / "scripts" / script_name,
    ]
    for c in candidates:
        if c.exists():
            return str(c)
    return None


# ─── Main pipeline ────────────────────────────────────────────────────

def run_pipeline(text: str, platform: str, library_path: str | None = None,
                 topic: str | None = None) -> str:
    """Run the full social media content pipeline."""
    lines: list[str] = []
    w = lines.append

    w("=" * 66)
    w("  phy-social-suite — Full Content Pipeline")
    w("=" * 66)
    w(f"  Platform      : {platform}")
    w(f"  Draft length  : {len(text.split())} words")
    if library_path:
        w(f"  Content lib   : {library_path}")
    w("=" * 66)

    # ─── Stage 1: Content Compound (if library provided) ─────────
    if library_path and topic:
        w("\n\n" + "─" * 66)
        w("  STAGE 1: Content Atom Retrieval")
        w("─" * 66)

        compound_path = _find_skill_script("phy-content-compound", "content_compound.py")
        if compound_path:
            try:
                compound = _import_from_path("content_compound", compound_path)
                library = compound.scan_directory(library_path)
                results = compound.retrieve_atoms(library, topic, top_n=3)
                w(f"\n  Library: {library.total_atoms} atoms from {library.files_scanned} files")
                if results:
                    w(f"  Top {len(results)} atoms for \"{topic}\":\n")
                    for i, (atom, score) in enumerate(results, 1):
                        w(f"    {i}. [{atom.atom_type}] (rel: {score})")
                        wrapped = textwrap.fill(atom.text[:120], width=58,
                                                initial_indent="       ",
                                                subsequent_indent="       ")
                        w(wrapped)
                        w(f"       — {atom.source_file}:{atom.line_number}")
                else:
                    w("  No relevant atoms found for this topic.")
            except Exception as e:
                w(f"  ⚠️  Could not load content-compound: {e}")
        else:
            w("  ⚠️  phy-content-compound not installed. Skipping atom retrieval.")

    # ─── Stage 2: Humanizer Audit ────────────────────────────────
    w("\n\n" + "─" * 66)
    w("  STAGE 2: AI Signature Audit")
    w("─" * 66)

    humanizer_path = _find_skill_script("phy-content-humanizer-audit", "content_humanizer_audit.py")
    if humanizer_path:
        try:
            humanizer = _import_from_path("content_humanizer_audit", humanizer_path)
            result = humanizer.audit_content(text, platform)

            v_emoji = {"PASS": "✅", "WARN": "🟡", "FAIL": "🔴"}.get(result.verdict, "❓")
            w(f"\n  AI Signature: {result.ai_signature_pct}% {v_emoji} {result.verdict}")
            w(f"  Human Score:  {result.total_score}/{result.max_score}")

            # Show dimension summary (compact)
            w("\n  Dimensions:")
            for d in result.dimensions:
                bar = "█" * int(d.score) + "░" * (10 - int(d.score))
                w(f"    {d.name:<28} {bar} {d.score:.1f}")

            if result.banned_words_found:
                w(f"\n  🚫 AI words: {', '.join(result.banned_words_found[:5])}")

            # Top fix
            if result.ai_signature_pct > 40:
                fixes = humanizer._generate_top_fixes(result)
                if fixes:
                    w(f"\n  💡 Top fix: {fixes[0]}")
        except Exception as e:
            w(f"  ⚠️  Could not load humanizer-audit: {e}")
    else:
        w("  ⚠️  phy-content-humanizer-audit not installed. Skipping AI audit.")

    # ─── Stage 3: Platform Rules Check ───────────────────────────
    w("\n\n" + "─" * 66)
    w("  STAGE 3: Platform Rules Pre-Flight")
    w("─" * 66)

    rules_path = _find_skill_script("phy-platform-rules-engine", "platform_rules.py")
    if rules_path:
        try:
            rules = _import_from_path("platform_rules", rules_path)
            results = rules.check_post(text, platform)
            score, verdict = rules.compute_risk_score(results)
            v_icon = {"CLEAR": "✅", "LOW RISK": "🟡", "MODERATE RISK": "🟠",
                       "HIGH RISK": "🔴"}.get(verdict, "❓")

            w(f"\n  Score: {score}/100 {v_icon} {verdict}")

            fails = [r for r in results if r.status == "FAIL"]
            warns = [r for r in results if r.status == "WARN"]
            passes = [r for r in results if r.status == "PASS"]
            w(f"  Rules: {len(passes)} PASS, {len(warns)} WARN, {len(fails)} FAIL")

            if fails:
                w("\n  🚨 Must fix:")
                for f in fails:
                    w(f"    • [{f.rule_id}] {f.name}: {f.fix}")

            if warns:
                w("\n  💡 Recommendations:")
                for wr in warns[:3]:
                    w(f"    • [{wr.rule_id}] {wr.name}: {wr.fix}")
        except Exception as e:
            w(f"  ⚠️  Could not load platform-rules: {e}")
    else:
        w("  ⚠️  phy-platform-rules-engine not installed. Skipping rules check.")

    # ─── Summary ─────────────────────────────────────────────────
    w("\n\n" + "=" * 66)
    w("  VERDICT")
    w("=" * 66)

    # Collect verdicts
    all_clear = True
    if humanizer_path:
        try:
            humanizer = _import_from_path("content_humanizer_audit", humanizer_path)
            h_result = humanizer.audit_content(text, platform)
            if h_result.verdict == "FAIL":
                w("  🔴 AI signature too high — fix before posting")
                all_clear = False
            elif h_result.verdict == "WARN":
                w("  🟡 AI signature borderline — consider fixes")
                all_clear = False
        except Exception:
            pass

    if rules_path:
        try:
            rules = _import_from_path("platform_rules", rules_path)
            r_results = rules.check_post(text, platform)
            r_fails = [r for r in r_results if r.status == "FAIL"]
            if r_fails:
                w(f"  🔴 {len(r_fails)} platform rule(s) violated — must fix")
                all_clear = False
        except Exception:
            pass

    if all_clear:
        w("  ✅ All clear — ready to post!")

    w("")
    return "\n".join(lines)


# ─── CLI ──────────────────────────────────────────────────────────────

def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(
        description="phy-social-suite: Full Social Media Content Pipeline",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent("""\
            Examples:
              echo "My post draft" | python3 social_suite.py --platform linkedin
              python3 social_suite.py --file draft.txt --platform reddit
              python3 social_suite.py --text "Post..." --platform linkedin --library ~/content/ --topic "dev tools"
        """),
    )
    parser.add_argument("--text", "-t", help="Draft text (inline)")
    parser.add_argument("--file", "-f", help="Read draft from file")
    parser.add_argument("--platform", "-p", required=True,
                        choices=["linkedin", "reddit", "twitter", "x", "hackernews", "hn"])
    parser.add_argument("--library", "-l", help="Path to content library directory")
    parser.add_argument("--topic", help="Topic for atom retrieval (requires --library)")

    args = parser.parse_args()

    if args.text:
        text = args.text
    elif args.file:
        with open(args.file) as fh:
            text = fh.read()
    elif not sys.stdin.isatty():
        text = sys.stdin.read()
    else:
        parser.error("Provide text via --text, --file, or stdin")

    print(run_pipeline(text.strip(), args.platform, args.library, args.topic))


if __name__ == "__main__":
    main()
