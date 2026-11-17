#!/usr/bin/env python3
from __future__ import annotations

import argparse
import shutil
import subprocess
from pathlib import Path

from common import PROFILE_DIR
from validate_application import (
    DEFAULT_MAX_VERTICAL_FILL,
    DEFAULT_MIN_VERTICAL_FILL,
    validate_application,
)


def render(source: Path, pdflatex: str) -> str:
    command = [
        pdflatex,
        "-interaction=nonstopmode",
        "-halt-on-error",
        source.name,
    ]
    outputs = []
    for pass_number in (1, 2):
        completed = subprocess.run(
            command,
            cwd=source.parent,
            check=False,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
        outputs.append(f"--- pass {pass_number} ---\n{completed.stdout}{completed.stderr}")
        if completed.returncode:
            raise RuntimeError(f"pdflatex failed for {source.name} on pass {pass_number}; see build.log")
    return "\n".join(outputs)


def main() -> int:
    parser = argparse.ArgumentParser(description="Render CV.tex and cover_letter.tex with pdflatex.")
    parser.add_argument("application_directory", type=Path)
    parser.add_argument("--profile-dir", type=Path, default=PROFILE_DIR,
                        help="Profile directory used by post-render validation")
    parser.add_argument("--skip-validation", action="store_true",
                        help="DEBUG ONLY: do not run the mandatory post-render quality checks")
    parser.add_argument("--strict-fill", action="store_true",
                        help="Treat a too-empty CV as a rendering failure")
    parser.add_argument("--min-vertical-fill", type=float, default=DEFAULT_MIN_VERTICAL_FILL)
    parser.add_argument("--max-vertical-fill", type=float, default=DEFAULT_MAX_VERTICAL_FILL)
    args = parser.parse_args()

    pdflatex = shutil.which("pdflatex")
    if not pdflatex:
        raise SystemExit("pdflatex was not found on PATH. Install a LaTeX distribution first.")

    app_dir = args.application_directory.expanduser().resolve()
    if not app_dir.is_dir():
        raise SystemExit(f"Directory not found: {app_dir}")

    sources = [app_dir / "CV.tex", app_dir / "cover_letter.tex"]
    missing = [source.name for source in sources if not source.is_file()]
    if missing:
        raise SystemExit(f"Missing source files: {', '.join(missing)}")

    logs = []
    try:
        for source in sources:
            logs.append(f"===== {source.name} =====\n{render(source, pdflatex)}")
    finally:
        (app_dir / "build.log").write_text("\n".join(logs), encoding="utf-8")

    print(f"Rendered {app_dir / 'CV.pdf'} and {app_dir / 'cover_letter.pdf'}")
    if args.skip_validation:
        print("WARNING: post-render application validation was skipped (debug option).")
        return 0
    report = validate_application(
        app_dir,
        args.profile_dir,
        strict_fill=args.strict_fill,
        min_vertical_fill=args.min_vertical_fill,
        max_vertical_fill=args.max_vertical_fill,
    )
    if report.pages is not None:
        print(f"CV pages: {report.pages}")
    if report.vertical_fill is not None:
        print(f"CV vertical fill: {report.vertical_fill:.1%}")
    if report.last_text_y is not None:
        print(f"CV last text Y: {report.last_text_y:.2f}")
    for warning in report.warnings:
        print(f"WARNING: {warning}")
    if not report.ok:
        for error in report.errors:
            print(f"ERROR: {error}")
        raise SystemExit("Rendered files failed application validation")
    print("Application validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
