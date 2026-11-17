"""Pre-commit entry point for Markdown-oriented writing-pattern checks."""

from __future__ import annotations

import argparse
from pathlib import Path

from .linter import format_lint_report, lint_file
from .skills import list_style_skills


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="human-writing-precommit")
    parser.add_argument("files", nargs="+")
    parser.add_argument("--style", choices=["general", *list_style_skills()], default="general")
    parser.add_argument("--fail-score", type=int, default=15)
    parser.add_argument("--allow", action="append", default=[])
    args = parser.parse_args(argv)
    failed = False
    for filename in args.files:
        path = Path(filename)
        if not path.is_file():
            continue
        report = lint_file(str(path), style=args.style, allow=set(args.allow))
        print(format_lint_report(report, "github", source_name=str(path)), end="")
        failed = failed or report.score >= args.fail_score
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
