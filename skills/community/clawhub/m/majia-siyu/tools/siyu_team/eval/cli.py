"""``siyu-eval`` command line interface.

* ``compliance`` scans deterministic rules and never emits a quality score;
* ``validate`` checks SKILL.md frontmatter, directory names and the 8KB limit.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path
from typing import Any

from . import static as static_mod
from .models import ScanMode


_COMPLIANCE_FLAGS = {
    "COMPLIANCE_RED",
    "ABSOLUTE_CLAIM",
    "INDUCE_SHARE",
    "PRIVACY_COLLECT",
    "ATTRIBUTED_CLAIM",
    "QUOTED_RISK_MENTION",
    "RISK_TERM_MENTION",
}


def _compliance_file(path: str, mode: ScanMode) -> tuple[int, dict[str, Any]]:
    if not os.path.exists(path):
        return 2, {"file": path, "error": "找不到文件", "passed": False}
    try:
        text = Path(path).read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        return 2, {"file": path, "error": f"读取失败：{exc}", "passed": False}
    result = _compliance_payload(text, mode)
    return (
        1 if result["hard_fail"] else 0,
        {
            "file": path,
            "mode": result["mode"],
            "passed": not result["hard_fail"],
            "hard_fail": result["hard_fail"],
            "flags": result["flags"],
            "hits": result["details"],
        },
    )


def _compliance_payload(text: str, mode: ScanMode) -> dict[str, Any]:
    """Keep compliance facts separate from roughness/quality heuristics."""

    result = static_mod.scan_result(text, mode=mode).to_dict()
    details = [
        detail
        for detail in result["details"]
        if detail.get("flag") in _COMPLIANCE_FLAGS
    ]
    flags = list(dict.fromkeys(str(detail["flag"]) for detail in details))
    return {
        **result,
        "flags": flags,
        "details": details,
        "hard_fail": any(bool(detail.get("hard")) for detail in details),
    }


def _print_compliance_report(report: dict[str, Any]) -> None:
    path = report["file"]
    if report.get("error"):
        print(f"❌ {path}：{report['error']}")
        return
    print(f"== 静态合规检查：{path}（mode={report['mode']}） ==")
    hits = report["hits"]
    if not hits:
        print("规则命中：无")
    for hit in hits:
        level = "阻断" if hit["hard"] else "提示"
        location = (
            f"offset={hit['offset']}:{hit['end']}"
            if hit["offset"] >= 0
            else "document"
        )
        description = hit.get("description") or hit.get("desc", "")
        print(f"- [{level}] {hit['rule']} ({location})：{description}")
        if hit.get("snippet"):
            print(f"  snippet: {hit['snippet']}")
    if report["passed"]:
        print("✅ 静态合规检查通过。")
    else:
        print("❌ 命中硬性合规规则，方案不得交付。")


def cmd_compliance(args: argparse.Namespace) -> int:
    """Scan one or more files; output compliance facts only."""

    mode = ScanMode(getattr(args, "mode", ScanMode.CUSTOMER_COPY.value))
    reports: list[dict[str, Any]] = []
    worst = 0
    for path in args.files:
        code, report = _compliance_file(path, mode)
        worst = max(worst, code)
        reports.append(report)

    payload = {
        "schema_version": "1.0",
        "report_type": "compliance",
        "mode": mode.value,
        "passed": worst == 0,
        "files": reports,
    }
    if getattr(args, "json", False):
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        for report in reports:
            _print_compliance_report(report)
        if len(reports) > 1:
            print(
                "整体结果（静态合规）：%s（%d 个文件）"
                % ("✅ 全部通过" if worst == 0 else "❌ 存在不通过", len(reports))
            )
        print("静态合规扫描结束。")
    return worst


def cmd_validate(args: argparse.Namespace) -> int:
    """Validate SKILL.md frontmatter, directory names and the 8KB limit."""

    root = args.path
    problems = 0
    for dirpath, _, files in os.walk(root):
        for filename in files:
            if filename != "SKILL.md":
                continue
            path = os.path.join(dirpath, filename)
            raw = open(path, "rb").read()
            text = raw.decode("utf-8")
            match = re.match(r"^---\s*\n(.*?)\n---\s*\n", text, re.DOTALL)
            if not match:
                print("⚠️ 缺 frontmatter:", path)
                problems += 1
                continue
            name_match = re.search(
                r"^name:\s*([^\n]+)$", match.group(1), re.MULTILINE
            )
            if not name_match:
                print("⚠️ 缺 frontmatter name:", path)
                problems += 1
            else:
                name = name_match.group(1).strip().strip("'\"")
                dirname = os.path.basename(dirpath)
                if name != dirname:
                    print(
                        f"⚠️ name 与目录名不一致: {path} "
                        f"({name!r} != {dirname!r})"
                    )
                    problems += 1
            if len(raw) > 8 * 1024:
                print(f"⚠️ 超过 8KB: {path} ({len(raw)} bytes)")
                problems += 1
    print("校验完成，问题数:", problems)
    return 1 if problems else 0


def _add_mode_argument(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--mode",
        choices=[mode.value for mode in ScanMode],
        default=ScanMode.CUSTOMER_COPY.value,
        help="扫描语境（默认 customer_copy）",
    )


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(
        prog="siyu-eval", description="私域文案静态合规扫描"
    )
    sub = parser.add_subparsers(dest="cmd", required=True)

    compliance_parser = sub.add_parser(
        "compliance", help="静态合规扫描（不产出质量分或徽章）"
    )
    compliance_parser.add_argument("files", nargs="+", metavar="file")
    compliance_parser.add_argument("--json", action="store_true")
    _add_mode_argument(compliance_parser)
    compliance_parser.set_defaults(func=cmd_compliance)

    validate_parser = sub.add_parser("validate")
    validate_parser.add_argument("path", nargs="?", default="plugins/")
    validate_parser.set_defaults(func=cmd_validate)

    args = parser.parse_args(argv)
    sys.exit(args.func(args))


if __name__ == "__main__":
    main()
