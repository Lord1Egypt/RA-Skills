#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_ROOT = SCRIPT_DIR.parent
WORKSPACE = SKILL_ROOT.parents[1]
if str(SKILL_ROOT) not in sys.path:
    sys.path.insert(0, str(SKILL_ROOT))

from lib.audit import (  # noqa: E402
    ai_review,
    analyze_block,
    build_bundle,
    clean_blocks,
    collect_paths,
    combine,
    load_policy,
    render_path,
    split_blocks,
    write_report,
)


def scan_blocks(paths: list[Path], policy: dict, with_ai: bool) -> list[dict]:
    results: list[dict] = []
    max_chars = int(policy.get("size_limits", {}).get("max_file_chars", 50000))
    for path in paths:
        for block in split_blocks(path, max_chars):
            static_result = analyze_block(block, policy)
            ai_result = ai_review(block, static_result) if with_ai and static_result["recommendation"] != "PASS" else None
            decision = combine(static_result, ai_result, policy)
            results.append(
                {
                    "block": block,
                    "static_analysis": static_result,
                    "ai_review": ai_result,
                    "decision": decision,
                }
            )
    return results


def print_summary(bundle: dict, report_path: Path) -> None:
    print("=" * 72)
    print(f"[{bundle['decision']['recommendation']}] memory audit | risk={bundle['decision']['risk_score']}")
    print(bundle["summary"]["summary"])
    suspicious = [item for item in bundle["blocks"] if item["decision"]["recommendation"] != "PASS"]
    if suspicious:
        print("suspicious blocks:")
        for item in suspicious[:10]:
            block = item["block"]
            summary = "; ".join(finding["summary"] for finding in item["static_analysis"]["findings"][:2])
            print(f"- {block['path']}:{block['start_line']}-{block['end_line']} :: {summary}")
    else:
        print("no suspicious blocks")
    print(f"report: {report_path}")


def serialize_bundle(bundle: dict) -> dict:
    serializable = dict(bundle)
    serializable["blocks"] = [
        {
            "block": {
                "path": str(item["block"].path),
                "start_line": item["block"].start_line,
                "end_line": item["block"].end_line,
                "text": item["block"].text[:400],
            },
            "static_analysis": item["static_analysis"],
            "ai_review": item["ai_review"],
            "decision": item["decision"],
        }
        for item in bundle["blocks"]
    ]
    return serializable


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Audit OpenClaw memory files for poisoning and hidden steering")
    parser.add_argument("--policy", help="Custom policy path")
    parser.add_argument("--format", choices=("text", "json"), default="text")
    parser.add_argument("--with-ai", action="store_true", help="Enable optional AI review on suspicious blocks")

    subparsers = parser.add_subparsers(dest="command", required=True)

    scan_parser = subparsers.add_parser("scan", help="Scan memory files")
    scan_parser.add_argument("--path", action="append", default=[], help="File or directory to scan")

    clean_parser = subparsers.add_parser("clean", help="Clean suspicious memory blocks")
    clean_parser.add_argument("--path", action="append", default=[], help="File or directory to clean")
    clean_parser.add_argument("--apply", action="store_true", help="Actually rewrite files after creating backups")

    return parser


def main() -> int:
    args = build_parser().parse_args()
    policy = load_policy(SKILL_ROOT, args.policy)
    paths = collect_paths(policy, WORKSPACE, args.path)
    if not paths:
        print("No memory files found to audit.", file=sys.stderr)
        return 1

    results = scan_blocks(paths, policy, args.with_ai)
    bundle = build_bundle(results, policy, [str(path) for path in paths])
    serializable_bundle = serialize_bundle(bundle)
    reports_dir = render_path(policy["reports_dir"], WORKSPACE)
    report_path = write_report(serializable_bundle, reports_dir)

    if args.command == "clean":
        if not args.apply:
            print("Use clean --apply to rewrite files. Scan report already generated.", file=sys.stderr)
            if args.format == "json":
                print(json.dumps(serializable_bundle, ensure_ascii=False, indent=2))
            else:
                print_summary(serializable_bundle, report_path)
            return 1 if bundle["decision"]["recommendation"] == "BLOCK" else 0
        backups_dir = render_path(policy["backups_dir"], WORKSPACE)
        actions = clean_blocks(paths, results, backups_dir)
        serializable_bundle["clean_actions"] = actions

    if args.format == "json":
        print(json.dumps(serializable_bundle, ensure_ascii=False, indent=2))
    else:
        print_summary(serializable_bundle, report_path)
        if serializable_bundle.get("clean_actions"):
            print("clean actions:")
            for action in serializable_bundle["clean_actions"]:
                print(f"- {action['path']} -> backup {action['backup']}")

    return 1 if bundle["decision"]["recommendation"] == "BLOCK" else 0


if __name__ == "__main__":
    sys.exit(main())
