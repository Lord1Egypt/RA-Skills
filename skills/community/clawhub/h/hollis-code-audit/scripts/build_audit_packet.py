#!/usr/bin/env python3
"""Build a compact packet for an external reviewer model or subagent."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Dict, List, Optional

from audit_snapshot import ignored_by_pattern, load_ignore_patterns, run_git


MODE_FOCUS = {
    "quick": "Current diff/status only; focus on high-risk regressions.",
    "standard": "Project intent, requested scope, adjacent contracts, and tests.",
    "security": "Auth, permissions, path handling, secrets, LLM/network, audit logs.",
    "deep": "Broader risk map, cross-module contracts, independent review, test strategy.",
    "intent": "Whether the change violates README/AGENTS/product purpose.",
}


def load_config(root: Path, path: Optional[str]) -> Dict[str, object]:
    if not path:
        default = Path(__file__).resolve().parents[1] / "config.json"
        path = str(default) if default.exists() else ""
    if not path:
        return {}
    config_path = Path(path)
    if not config_path.is_absolute():
        config_path = root / config_path
    if not config_path.exists():
        return {}
    return json.loads(config_path.read_text(encoding="utf-8"))


def split_lines(value: Optional[str], limit: int) -> List[str]:
    if not value:
        return []
    return value.splitlines()[:limit]


def capped(value: Optional[str], max_chars: int) -> str:
    if not value:
        return ""
    if len(value) <= max_chars:
        return value
    return value[:max_chars] + "\n\n[TRUNCATED]\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".")
    parser.add_argument("--mode", choices=sorted(MODE_FOCUS), default=None)
    parser.add_argument("--scope", default="diff", help="diff, status, files, module, repo, or free text.")
    parser.add_argument("--reviewer", default="", help="User-specified reviewer model/subagent.")
    parser.add_argument("--producer-agent", default="", help="Agent/model that produced the code, if relevant.")
    parser.add_argument("--prior-review", action="append", default=[], help="Path to a prior review artifact. Can be repeated.")
    parser.add_argument("--config", default="", help="Optional config JSON path.")
    parser.add_argument("--include-diff", action="store_true", help="Include capped git diff body.")
    parser.add_argument("--max-diff-chars", type=int, default=20000)
    parser.add_argument("--output", default="", help="Write packet to this path instead of stdout.")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    config = load_config(root, args.config)
    mode = args.mode or config.get("default_mode") or "standard"
    skip_patterns = list(config.get("skip_paths", []))
    ignore_patterns = load_ignore_patterns(root, skip_patterns)

    status = split_lines(run_git(root, ["status", "--short"]), 120)
    diff_stat = split_lines(run_git(root, ["diff", "--stat"]), 80)
    changed = split_lines(run_git(root, ["diff", "--name-only"]), 160)
    staged = split_lines(run_git(root, ["diff", "--cached", "--name-only"]), 160)
    visible_changed = [
        item for item in sorted(set(changed + staged)) if not ignored_by_pattern(item, ignore_patterns)
    ]
    branch = run_git(root, ["branch", "--show-current"]) or "unknown"
    diff_body = capped(run_git(root, ["diff"]), args.max_diff_chars) if args.include_diff else ""

    always_read = config.get("always_read") or ["AGENTS.md", "README.md"]
    preferred = config.get("preferred_reviewers") or []
    reviewer = args.reviewer or (preferred[0] if preferred else "")

    lines = [
        "# Code Audit Packet",
        "",
        f"- Root: `{root}`",
        f"- Branch: `{branch}`",
        f"- Mode: `{mode}` - {MODE_FOCUS.get(mode, MODE_FOCUS['standard'])}",
        f"- Scope: `{args.scope}`",
        f"- Reviewer route: `{reviewer or 'not specified'}`",
        f"- Producer agent: `{args.producer_agent or 'not specified'}`",
        f"- External review forbidden by config: `{bool(config.get('forbidden_external_review', False))}`",
        "",
        "## Intent Sources To Read First",
        "",
        *[f"- `{item}`" for item in always_read],
        "",
        "## Git Status",
        "",
        "```text",
        *(status or ["clean or unavailable"]),
        "```",
        "",
        "## Diff Stat",
        "",
        "```text",
        *(diff_stat or ["no unstaged diff or unavailable"]),
        "```",
        "",
        "## Prior Review Artifacts",
        "",
        *([f"- `{item}`" for item in args.prior_review] or ["- none provided"]),
        "",
        "## Changed Files",
        "",
        *([f"- `{item}`" for item in visible_changed] or ["- none or all ignored"]),
        "",
        "## Audit Questions",
        "",
        "- What concrete bugs, security risks, contract breaks, or missing tests exist in this scope?",
        "- Does the change conflict with the project's README/AGENTS intent or trust boundaries?",
        "- Do prior review artifacts contain findings that are confirmed, contradicted, or unsupported by local evidence?",
        "- Which edge cases should be tested before relying on this change?",
        "- Which concerns are confirmed by evidence, and which are only hypotheses?",
        "",
        "## Sharing Safety",
        "",
        "- Redact secrets, customer data, private documents, and unreleased business material before external review.",
        "- Do not use an external reviewer if repo policy or user instruction forbids it.",
        "- Treat reviewer output as candidate findings; validate locally before reporting.",
        "",
        "## Ignore Patterns",
        "",
        *[f"- `{item}`" for item in ignore_patterns],
    ]

    if diff_body:
        lines.extend(["", "## Diff Body", "", "```diff", diff_body, "```"])
    else:
        lines.extend(["", "## Diff Body", "", "Not included. Re-run with `--include-diff` only if safe to share."])

    packet = "\n".join(lines) + "\n"
    if args.output:
        Path(args.output).write_text(packet, encoding="utf-8")
    else:
        print(packet, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
