#!/usr/bin/env python3
"""Rebuild the public fictional example documents from bundled resources only."""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


SKILL_DIR = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = SKILL_DIR / "scripts"
EXAMPLES_DIR = SKILL_DIR / "examples"
PROFILE_DIR = SKILL_DIR / "assets" / "profile"


def run(script: str, *arguments: Path | str) -> None:
    subprocess.run(
        [sys.executable, str(SCRIPTS_DIR / script), *(str(argument) for argument in arguments)],
        check=True,
    )


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Render the bundled fictional CV and cover-letter example into an external directory."
    )
    parser.add_argument("--output", required=True, type=Path,
                        help="New or empty directory outside the installed skill")
    args = parser.parse_args()

    output = args.output.expanduser().resolve()
    if output == SKILL_DIR or SKILL_DIR in output.parents:
        parser.error("--output must be outside the installed skill directory")
    if output.exists() and any(output.iterdir()):
        parser.error("--output must be empty when it already exists")
    output.mkdir(parents=True, exist_ok=True)

    try:
        run(
            "generate_cv_selection.py",
            "--job", EXAMPLES_DIR / "job.json",
            "--output", output / "cv_selection.json",
            "--profile-dir", PROFILE_DIR,
        )
        run(
            "generate_cv.py",
            "--selection", output / "cv_selection.json",
            "--output", output / "CV.tex",
            "--profile-dir", PROFILE_DIR,
        )
        run(
            "generate_cover_letter.py",
            "--content", EXAMPLES_DIR / "application_content.json",
            "--output", output / "cover_letter.tex",
            "--profile", PROFILE_DIR / "master_profile.json",
        )
        run(
            "generate_plain_text.py",
            "--content", EXAMPLES_DIR / "application_content.json",
            "--output", output / "indeed_text.txt",
            "--profile", PROFILE_DIR / "master_profile.json",
        )
        run(
            "render_application.py",
            output,
            "--profile-dir", PROFILE_DIR,
            "--strict-fill",
        )
    except subprocess.CalledProcessError as error:
        raise SystemExit(error.returncode) from error

    print(f"Rendered fictional examples in {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
