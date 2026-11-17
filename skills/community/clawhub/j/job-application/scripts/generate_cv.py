#!/usr/bin/env python3
from __future__ import annotations

import argparse
import shutil
from pathlib import Path
from typing import Any

from common import (
    PROFILE_DIR,
    TEMPLATE_DIR,
    ValidationError,
    by_id,
    latex_escape,
    load_json,
    public_location,
    replace_tokens,
    resolve_profile_asset,
    validate_cv_selection,
    write_text,
)


def selected(ids: list[str], filename: str, profile_dir: Path) -> list[dict[str, Any]]:
    records = by_id(load_json(profile_dir / filename))
    missing = [record_id for record_id in ids if record_id not in records]
    if missing:
        raise ValidationError(f"Unknown IDs in {filename}: {', '.join(missing)}")
    return [records[record_id] for record_id in ids]


def entries(records: list[dict[str, Any]], achievement_limit: int) -> str:
    blocks = []
    for record in records:
        description = " ".join(record.get("description", [])[:achievement_limit])
        subtitle = " · ".join(
            str(value).strip()
            for value in (
                record.get("organization", ""),
                record.get("context_label", ""),
                record.get("subtitle", ""),
            )
            if str(value).strip()
        )
        blocks.append(
            "\\cvitem{%s}{%s}{%s}{%s}" % tuple(
                latex_escape(value) for value in (
                    record.get("period", ""), record.get("title", ""), subtitle, description,
                )
            )
        )
    return "\n".join(blocks)


def skill_bars(records: list[dict[str, Any]]) -> str:
    return "\n".join(
        f"\\skillbar{{{latex_escape(item['label'])}}}{{{max(0, min(5, int(item.get('score', 0))))}}}"
        for item in records
    )


def contact_location(profile: dict[str, Any]) -> str:
    """Format postal address lines for the constrained CV contact sidebar."""
    address_lines = profile.get("address_lines")
    if isinstance(address_lines, list):
        lines = [latex_escape(line) for line in address_lines if str(line).strip()]
        if lines:
            return r"\\ ".join(lines)
    return latex_escape(public_location(profile))


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate CV LaTeX from a reviewed v1/v2 selection.")
    parser.add_argument("--selection", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--profile-dir", type=Path, default=PROFILE_DIR)
    parser.add_argument("--template", type=Path, default=TEMPLATE_DIR / "cv.tex")
    args = parser.parse_args()

    try:
        profile_dir = args.profile_dir.expanduser().resolve()
        profile = load_json(profile_dir / "master_profile.json")
        choice = validate_cv_selection(load_json(args.selection), profile_dir)
        limits = choice["limits"]
        location = contact_location(profile)
        skills = selected(choice["skills"], "skills.json", profile_dir)
        languages = selected(choice["languages"], "languages.json", profile_dir)
        photo_source = resolve_profile_asset(profile_dir, profile.get("profile_picture", ""))
        photo_target = args.output.parent / "assets" / "profile-photo.png"
        photo_block = ""
        if photo_source is not None:
            photo_target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(photo_source, photo_target)
            photo_block = r"""\begin{tikzpicture}
    \clip (0,0) circle (2.18cm);
    \node at (0,-0.05) {\includegraphics[width=4.55cm]{assets/profile-photo.png}};
  \end{tikzpicture}
  \vspace{0.12cm}"""
        values = {
            "__NAME__": latex_escape(profile["full_name"]),
            "__TITLE__": latex_escape(choice["target_title"]),
            "__EMAIL__": latex_escape(profile.get("email", "")),
            "__PHONE__": latex_escape(profile.get("phone", "")),
            "__LOCATION__": location,
            "__PHOTO_BLOCK__": photo_block,
            "__ABOUT__": latex_escape(choice.get("about_me", "")),
            "__SKILLS__": skill_bars(skills),
            "__EXPERIENCE__": entries(
                selected(choice["experience"], "experience.json", profile_dir),
                limits["achievement_sentences_per_experience"],
            ),
            "__EDUCATION__": entries(
                selected(choice["education"], "education.json", profile_dir),
                limits["achievement_sentences_per_experience"],
            ),
            "__PROJECTS__": entries(
                selected(choice["projects"], "projects.json", profile_dir),
                limits["achievement_sentences_per_experience"],
            ),
            "__LANGUAGES__": skill_bars(languages),
        }
        write_text(args.output, replace_tokens(args.template.read_text(encoding="utf-8"), values))
    except (OSError, ValidationError) as error:
        parser.error(str(error))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
