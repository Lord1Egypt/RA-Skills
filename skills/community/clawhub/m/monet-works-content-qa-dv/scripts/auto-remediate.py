#!/usr/bin/env python3
"""
auto-remediate.py — Monet Works QA → Remediation Auto-Fix Pipeline
====================================================================
Consumes a full QA verdict JSON (list of REVISE items) and applies
auto-fixes where possible. Human-judgment issues are flagged and
passed through with a clear explanation.

Usage:
  python3 auto-remediate.py --verdict verdict.json --content draft.md --type financial
  python3 auto-remediate.py --verdict verdict.json --content draft.md --type financial --variant default
  cat verdict.json | python3 auto-remediate.py --content draft.md --type financial

Exit codes:
  0 — all issues auto-fixed (or no issues found)
  1 — partial: some REVISE items remain (require human judgment)
  2 — failed: unrecoverable error

Change report JSON is written to stderr. Fixed content goes to stdout.

QA Verdict JSON schema (input):
  {
    "content_id": "post-001",      // optional
    "content_file": "draft.md",    // optional (overridden by --content flag)
    "verdict": "REVISE",           // PASS | REVISE | REJECT
    "content_type": "financial",   // optional (overridden by --type flag)
    "issues": [
      {
        "issue_type": "missing_disclaimer",
        "severity": "critical",
        "description": "No financial disclaimer found",
        "original_text": "",       // optional
        "location": "end"          // optional
      },
      {
        "issue_type": "banned_phrase",
        "severity": "minor",
        "description": "Found banned phrase: 'game-changer'",
        "original_text": "This is a game-changer for investors."
      },
      {
        "issue_type": "tone_misalignment",
        "severity": "major",
        "description": "Tone is too casual for the target audience."
      }
    ]
  }
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path
from typing import Any

# ---------------------------------------------------------------------------
# Paths to data files (relative to this script's directory)
# ---------------------------------------------------------------------------
SCRIPT_DIR = Path(__file__).parent
DATA_DIR = SCRIPT_DIR.parent / "data"

DISCLAIMER_TEMPLATES_PATH = DATA_DIR / "disclaimer-templates.json"
BANNED_PHRASES_PATH = DATA_DIR / "banned-phrase-alternatives.json"
CTA_TEMPLATES_PATH = DATA_DIR / "cta-templates.json"


# ---------------------------------------------------------------------------
# Issue types that can be auto-fixed vs those requiring human judgment
# ---------------------------------------------------------------------------
AUTO_FIXABLE_TYPES = {
    "missing_disclaimer",
    "banned_phrase",
    "missing_cta",
    "excessive_length",
    "cta_missing",
    "disclaimer_missing",
    "word_count_exceeded",
    "length_exceeded",
}

HUMAN_JUDGMENT_TYPES = {
    "tone_misalignment",
    "tone",
    "strategy_misalignment",
    "strategy",
    "unclear_thesis",
    "thesis",
    "evidence_gap",
    "evidence",
    "nda_violation",
    "nda",
    "factual_error",
    "factual",
    "audience_mismatch",
    "brand_voice",
    "quality_gate",
    "wording",
    "structure",
    "argument",
}

HUMAN_JUDGMENT_REASONS = {
    "tone_misalignment": "Tone adjustments require editorial judgment to preserve brand voice and audience fit.",
    "tone": "Tone adjustments require editorial judgment to preserve brand voice and audience fit.",
    "strategy_misalignment": "Strategy alignment requires understanding of campaign goals and audience intent.",
    "strategy": "Strategy alignment requires understanding of campaign goals and audience intent.",
    "unclear_thesis": "Thesis rewriting requires editorial judgment about the core argument.",
    "thesis": "Thesis rewriting requires editorial judgment about the core argument.",
    "evidence_gap": "Adding evidence requires sourcing verifiable data — a human must validate claims.",
    "evidence": "Adding evidence requires sourcing verifiable data — a human must validate claims.",
    "nda_violation": "NDA violations require legal review before any replacement can be approved.",
    "nda": "NDA violations require legal review before any replacement can be approved.",
    "factual_error": "Factual corrections require verified source material — do not auto-fix.",
    "factual": "Factual corrections require verified source material — do not auto-fix.",
    "audience_mismatch": "Audience calibration requires understanding the intended reader — requires human review.",
    "brand_voice": "Brand voice adjustments require editorial judgment and creative review.",
    "quality_gate": "Quality gate failures require editorial review of the full piece.",
    "wording": "Wording improvements require editorial judgment to maintain tone and argument.",
    "structure": "Structural changes require understanding of the full narrative arc.",
    "argument": "Argument strengthening requires editorial judgment and subject matter expertise.",
}


# ---------------------------------------------------------------------------
# Load data files
# ---------------------------------------------------------------------------

def load_json(path: Path) -> dict:
    try:
        with open(path, encoding="utf-8") as fh:
            return json.load(fh)
    except OSError as exc:
        sys.exit(f"ERROR: Cannot load data file '{path}': {exc}")
    except json.JSONDecodeError as exc:
        sys.exit(f"ERROR: Invalid JSON in '{path}': {exc}")


def load_data() -> tuple[dict, dict, dict]:
    """Returns (disclaimers, banned_phrases_map, cta_templates)."""
    disclaimers = load_json(DISCLAIMER_TEMPLATES_PATH)
    banned_raw = load_json(BANNED_PHRASES_PATH)
    cta_templates = load_json(CTA_TEMPLATES_PATH)

    # Build a simple phrase→replacement dict from the array format
    banned_map: dict[str, str] = {}
    for entry in banned_raw.get("phrases", []):
        banned_map[entry["banned"]] = entry.get("approved", "")

    return disclaimers, banned_map, cta_templates


# ---------------------------------------------------------------------------
# Individual fix handlers
# ---------------------------------------------------------------------------

def fix_missing_disclaimer(
    content: str,
    content_type: str,
    disclaimers: dict,
    issue: dict,
) -> tuple[str, dict[str, Any]]:
    """Inject disclaimer if not already present."""
    type_key = content_type if content_type in disclaimers else "general"
    tmpl = disclaimers[type_key]
    separator = tmpl.get("separator", "\n\n---\n\n")
    disclaimer_text = tmpl.get("full", tmpl.get("short", ""))

    # Check if disclaimer already present
    detection_keywords = ["disclaimer", "not financial advice", "not investment advice",
                          "informational purposes only", "consult.*advisor"]
    already_present = any(
        re.search(kw, content, re.IGNORECASE) for kw in detection_keywords
    )

    if already_present:
        return content, {
            "issue_type": issue["issue_type"],
            "original_text": issue.get("original_text", ""),
            "fixed_text": "(disclaimer already present — skipped)",
            "auto_fixed": True,
            "reason": "Disclaimer detected in content — no injection needed.",
            "action": "skipped",
        }

    fixed_content = content.rstrip() + separator + disclaimer_text
    return fixed_content, {
        "issue_type": issue["issue_type"],
        "original_text": issue.get("original_text", ""),
        "fixed_text": disclaimer_text,
        "auto_fixed": True,
        "reason": f"Injected {type_key} disclaimer from template library.",
        "action": "injected",
        "template_used": f"{type_key}.full",
    }


def fix_banned_phrase(
    content: str,
    issue: dict,
    banned_map: dict[str, str],
) -> tuple[str, dict[str, Any]]:
    """Replace banned phrases with approved alternatives."""
    # Sort longest-first to avoid partial matches
    sorted_phrases = sorted(banned_map.keys(), key=len, reverse=True)

    changes_made: list[dict] = []
    original_content = content

    for phrase in sorted_phrases:
        replacement = banned_map[phrase]
        pattern = re.compile(re.escape(phrase), re.IGNORECASE)
        matches = pattern.findall(content)
        if not matches:
            continue

        if not replacement:
            # Empty replacement = delete the phrase
            def _delete(m: re.Match) -> str:
                return ""
            content = pattern.sub(_delete, content)
        else:
            def _replace(m: re.Match) -> str:
                original = m.group(0)
                if original and original[0].isupper():
                    return replacement[0].upper() + replacement[1:]
                return replacement

            content = pattern.sub(_replace, content)

        changes_made.append({
            "phrase": phrase,
            "replacement": replacement or "(deleted)",
            "occurrences": len(matches),
        })

    if not changes_made:
        # Check if the specific phrase from the issue was already replaced in a prior pass
        original_text = issue.get("original_text", "")
        # Look up each word in original_text against the banned map
        already_fixed = False
        if original_text:
            for phrase in sorted(banned_map.keys(), key=len, reverse=True):
                if phrase.lower() in original_text.lower():
                    # Phrase was in original_text but no longer in content — already fixed
                    if phrase.lower() not in content.lower():
                        already_fixed = True
                        break
        if already_fixed:
            return content, {
                "issue_type": issue["issue_type"],
                "original_text": original_text,
                "fixed_text": "(already fixed in a prior banned_phrase pass)",
                "auto_fixed": True,
                "reason": "Banned phrase was already replaced by an earlier fix pass — no action needed.",
                "action": "already_fixed",
            }
        return content, {
            "issue_type": issue["issue_type"],
            "original_text": original_text,
            "fixed_text": original_text,
            "auto_fixed": False,
            "reason": "No matching banned phrases found in the approved alternatives list. Manual review required.",
            "action": "no_match",
        }

    return content, {
        "issue_type": issue["issue_type"],
        "original_text": issue.get("original_text", "(see changes)"),
        "fixed_text": f"Replaced {sum(c['occurrences'] for c in changes_made)} occurrence(s)",
        "auto_fixed": True,
        "reason": f"Substituted {len(changes_made)} banned phrase(s) with approved alternatives.",
        "action": "replaced",
        "replacements": changes_made,
    }


def fix_missing_cta(
    content: str,
    content_type: str,
    cta_templates: dict,
    issue: dict,
    variant: str = "default",
) -> tuple[str, dict[str, Any]]:
    """Append CTA if not already present."""
    type_key = content_type if content_type in cta_templates else "general"
    tmpl = cta_templates[type_key]
    detection_signals = tmpl.get("detection_signals", [])

    already_present = any(
        re.search(re.escape(signal), content, re.IGNORECASE)
        for signal in detection_signals
    )

    if already_present:
        return content, {
            "issue_type": issue["issue_type"],
            "original_text": issue.get("original_text", ""),
            "fixed_text": "(CTA already present — skipped)",
            "auto_fixed": True,
            "reason": "CTA signal detected in content — no injection needed.",
            "action": "skipped",
        }

    cta_variant = variant if variant in tmpl else "default"
    cta_text = tmpl[cta_variant]
    fixed_content = content.rstrip() + cta_text

    return fixed_content, {
        "issue_type": issue["issue_type"],
        "original_text": issue.get("original_text", ""),
        "fixed_text": cta_text.strip(),
        "auto_fixed": True,
        "reason": f"Appended {type_key}/{cta_variant} CTA template.",
        "action": "appended",
        "template_used": f"{type_key}.{cta_variant}",
    }


def fix_excessive_length(
    content: str,
    issue: dict,
    max_words: int | None,
) -> tuple[str, dict[str, Any]]:
    """Truncate to word limit."""
    words = content.split()
    original_wc = len(words)

    # Try to extract max words from issue description if not provided
    if max_words is None:
        desc = issue.get("description", "")
        match = re.search(r"(\d+)\s*words?", desc, re.IGNORECASE)
        if match:
            max_words = int(match.group(1))
        else:
            return content, {
                "issue_type": issue["issue_type"],
                "original_text": f"{original_wc} words",
                "fixed_text": f"{original_wc} words (unchanged)",
                "auto_fixed": False,
                "reason": "No word limit specified in issue or --max-words flag. Manual truncation required.",
                "action": "skipped",
            }

    if original_wc <= max_words:
        return content, {
            "issue_type": issue["issue_type"],
            "original_text": f"{original_wc} words",
            "fixed_text": f"{original_wc} words (within limit)",
            "auto_fixed": True,
            "reason": f"Word count {original_wc} is within the {max_words}-word limit — no truncation needed.",
            "action": "skipped",
        }

    # Truncate at word boundary with ellipsis
    truncated = " ".join(words[:max_words]) + "..."
    final_wc = len(truncated.split())

    return truncated, {
        "issue_type": issue["issue_type"],
        "original_text": f"{original_wc} words",
        "fixed_text": f"{final_wc} words",
        "auto_fixed": True,
        "reason": f"Truncated from {original_wc} to {max_words} words at word boundary with ellipsis.",
        "action": "truncated",
        "original_word_count": original_wc,
        "final_word_count": final_wc,
        "max_words": max_words,
    }


def handle_human_judgment(issue: dict) -> dict[str, Any]:
    """Return a change-report entry for a human-judgment issue."""
    issue_type = issue.get("issue_type", "unknown")
    default_reason = "This issue requires human editorial judgment and cannot be auto-fixed."
    reason = HUMAN_JUDGMENT_REASONS.get(issue_type, default_reason)

    return {
        "issue_type": issue_type,
        "original_text": issue.get("original_text", ""),
        "fixed_text": "",
        "auto_fixed": False,
        "reason": reason,
        "action": "requires_human_review",
        "severity": issue.get("severity", "unknown"),
        "description": issue.get("description", ""),
    }


# ---------------------------------------------------------------------------
# Main pipeline
# ---------------------------------------------------------------------------

def process_verdict(
    content: str,
    verdict: dict,
    content_type: str,
    max_words: int | None,
    cta_variant: str,
    disclaimers: dict,
    banned_map: dict[str, str],
    cta_templates: dict,
) -> tuple[str, list[dict[str, Any]]]:
    """
    Process all issues in the verdict. Apply auto-fixes, flag human-judgment items.
    Returns (fixed_content, change_report_items).
    """
    issues = verdict.get("issues", [])
    change_report: list[dict[str, Any]] = []
    fixed = content

    # If verdict is PASS and no issues, return immediately
    if verdict.get("verdict") in ("PASS", "pass") and not issues:
        return fixed, []

    for issue in issues:
        issue_type = issue.get("issue_type", "").lower().replace("-", "_").replace(" ", "_")

        # Normalize common aliases
        if issue_type in ("disclaimer_missing", "no_disclaimer"):
            issue_type = "missing_disclaimer"
        elif issue_type in ("cta_missing", "no_cta"):
            issue_type = "missing_cta"
        elif issue_type in ("length_exceeded", "word_count_exceeded", "too_long"):
            issue_type = "excessive_length"

        # Update normalized type
        issue = {**issue, "issue_type": issue_type}

        if issue_type == "missing_disclaimer":
            fixed, report_item = fix_missing_disclaimer(fixed, content_type, disclaimers, issue)
            change_report.append(report_item)

        elif issue_type == "banned_phrase":
            fixed, report_item = fix_banned_phrase(fixed, issue, banned_map)
            change_report.append(report_item)

        elif issue_type == "missing_cta":
            fixed, report_item = fix_missing_cta(fixed, content_type, cta_templates, issue, cta_variant)
            change_report.append(report_item)

        elif issue_type == "excessive_length":
            fixed, report_item = fix_excessive_length(fixed, issue, max_words)
            change_report.append(report_item)

        elif issue_type in HUMAN_JUDGMENT_TYPES:
            change_report.append(handle_human_judgment(issue))

        else:
            # Unknown issue type — check if it looks like it could be auto-fixed
            # or should be flagged for human review
            change_report.append({
                "issue_type": issue_type,
                "original_text": issue.get("original_text", ""),
                "fixed_text": "",
                "auto_fixed": False,
                "reason": f"Unknown issue type '{issue_type}'. Cannot determine if auto-fixable. Flagged for human review.",
                "action": "unknown_type",
                "severity": issue.get("severity", "unknown"),
                "description": issue.get("description", ""),
            })

    return fixed, change_report


# ---------------------------------------------------------------------------
# Summary stats
# ---------------------------------------------------------------------------

def build_summary(
    change_report: list[dict],
    original_content: str,
    fixed_content: str,
    verdict: dict,
) -> dict[str, Any]:
    auto_fixed = [c for c in change_report if c.get("auto_fixed")]
    not_fixed = [c for c in change_report if not c.get("auto_fixed")]

    return {
        "status": "partial" if not_fixed else ("ok" if auto_fixed else "no_changes"),
        "original_verdict": verdict.get("verdict", "REVISE"),
        "content_id": verdict.get("content_id", ""),
        "total_issues": len(change_report),
        "auto_fixed_count": len(auto_fixed),
        "human_review_count": len(not_fixed),
        "original_word_count": len(original_content.split()),
        "final_word_count": len(fixed_content.split()),
        "changes": change_report,
    }


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Monet Works QA → Remediation Auto-Fix Pipeline",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument(
        "--verdict", "-v",
        metavar="PATH_OR_JSON",
        help="Path to QA verdict JSON file, or inline JSON string. If omitted, reads from stdin.",
    )
    parser.add_argument(
        "--content", "-c",
        metavar="PATH",
        help="Path to the content file to fix.",
        required=True,
    )
    parser.add_argument(
        "--type", "-t",
        dest="content_type",
        default="general",
        choices=["financial", "investment", "health", "legal", "general", "linkedin", "twitter"],
        help="Content type (default: general). Determines which disclaimer/CTA templates to use.",
    )
    parser.add_argument(
        "--max-words",
        type=int,
        metavar="N",
        help="Max word count ceiling (used for excessive_length fixes).",
    )
    parser.add_argument(
        "--cta-variant",
        default="default",
        metavar="VARIANT",
        help="CTA template variant: default, newsletter, consultation, download, etc.",
    )
    parser.add_argument(
        "--no-banner",
        action="store_true",
        help="Suppress the change report JSON on stderr.",
    )
    return parser.parse_args()


def load_verdict(args: argparse.Namespace) -> dict:
    if not args.verdict:
        raw = sys.stdin.read()
    else:
        try:
            with open(args.verdict, encoding="utf-8") as fh:
                raw = fh.read()
        except OSError:
            raw = args.verdict  # treat as inline JSON

    try:
        return json.loads(raw)
    except json.JSONDecodeError as exc:
        sys.exit(f"ERROR: Cannot parse verdict JSON: {exc}")


def load_content(args: argparse.Namespace) -> str:
    try:
        with open(args.content, encoding="utf-8") as fh:
            return fh.read()
    except OSError as exc:
        sys.exit(f"ERROR: Cannot read content file '{args.content}': {exc}")


def main() -> None:
    args = parse_args()

    # Load data templates
    disclaimers, banned_map, cta_templates = load_data()

    # Load inputs
    verdict = load_verdict(args)
    content = load_content(args)

    if not content.strip():
        sys.exit("ERROR: Empty content file.")

    # Resolve content type — verdict can specify it, CLI flag overrides
    content_type = args.content_type
    if content_type == "general" and verdict.get("content_type"):
        content_type = verdict["content_type"]

    # Process
    fixed_content, change_report = process_verdict(
        content=content,
        verdict=verdict,
        content_type=content_type,
        max_words=args.max_words,
        cta_variant=args.cta_variant,
        disclaimers=disclaimers,
        banned_map=banned_map,
        cta_templates=cta_templates,
    )

    # Build summary
    summary = build_summary(change_report, content, fixed_content, verdict)

    # Output fixed content to stdout
    print(fixed_content, end="")

    # Output change report to stderr
    if not args.no_banner:
        print(json.dumps(summary, indent=2), file=sys.stderr)

    # Exit code logic
    human_review_count = summary["human_review_count"]
    if human_review_count == 0:
        sys.exit(0)   # all fixed (or nothing to fix)
    elif summary["auto_fixed_count"] > 0:
        sys.exit(1)   # partial — some fixed, some need human
    else:
        sys.exit(1)   # all need human review (still exit 1, not 2)


if __name__ == "__main__":
    main()
