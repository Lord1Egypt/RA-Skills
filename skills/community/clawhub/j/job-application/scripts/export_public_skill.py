#!/usr/bin/env python3
"""Create a safe, standalone ClawHub staging directory for this skill.

Only explicitly listed, public source files are copied. This avoids accidental
publication of data from an enclosing Git repository when ClawHub discovers a
repository root above the installed skill directory.
"""
from __future__ import annotations

import argparse
import shutil
from pathlib import Path


SKILL_DIR = Path(__file__).resolve().parent.parent
PUBLIC_PATHS = (
    ".gitignore",
    "LICENSE",
    "PUBLISHING.md",
    "README.en.md",
    "README.md",
    "SKILL.md",
    "agents/openai.yaml",
    "assets/profile/education.json",
    "assets/profile/experience.json",
    "assets/profile/languages.json",
    "assets/profile/master_profile.json",
    "assets/profile/mira-hoffmann.png",
    "assets/profile/mira-hoffmann-signature.pdf",
    "assets/profile/mira-hoffmann-signature.tex",
    "assets/profile/projects.json",
    "assets/profile/skills.json",
    "assets/templates/cover-letter.tex",
    "assets/templates/cv.tex",
    "examples/application_content.json",
    "examples/cover_letter.json",
    "examples/generated/CV-example.pdf",
    "examples/generated/cover-letter-example.pdf",
    "examples/indeed_text.json",
    "examples/job.json",
    "scripts/common.py",
    "scripts/convert_application_content.py",
    "scripts/export_public_skill.py",
    "scripts/generate_cover_letter.py",
    "scripts/generate_cv.py",
    "scripts/generate_cv_selection.py",
    "scripts/generate_plain_text.py",
    "scripts/prepare_application.py",
    "scripts/render_application.py",
    "scripts/render_application.sh",
    "scripts/render_example.py",
    "scripts/validate_application.py",
    "tests/test_v2.py",
)


def copy_public_file(relative: Path, destination: Path) -> None:
    source = SKILL_DIR / relative
    resolved = source.resolve()
    if source.is_symlink() or not source.is_file() or not resolved.is_relative_to(SKILL_DIR):
        raise ValueError(f"Required public file is missing or unsafe: {source}")
    target = destination / relative
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, target)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Create a whitelist-only directory suitable for ClawHub publish --dry-run."
    )
    parser.add_argument("--output", required=True, type=Path,
                        help="New or empty destination directory outside the installed skill")
    args = parser.parse_args()

    destination = args.output.expanduser().resolve()
    if destination == SKILL_DIR or SKILL_DIR in destination.parents:
        parser.error("--output must be outside the installed skill directory")
    if destination.exists() and any(destination.iterdir()):
        parser.error("--output must be empty when it already exists")
    destination.mkdir(parents=True, exist_ok=True)

    try:
        for value in PUBLIC_PATHS:
            copy_public_file(Path(value), destination)
    except (OSError, ValueError) as error:
        parser.error(str(error))

    print(destination)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
