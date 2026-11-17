#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

from common import (
    BUNDLED_PROFILE_DIR,
    PROFILE_DIR,
    SKILL_DIR,
    TEMPLATE_DIR,
    ValidationError,
    latex_escape,
    load_application_content,
    load_json,
    public_location,
    replace_tokens,
    resolve_signature_asset,
    write_text,
)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Generate cover-letter LaTeX from application_content.json schema_version 2."
    )
    parser.add_argument("--content", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    profile_group = parser.add_mutually_exclusive_group()
    profile_group.add_argument("--profile", type=Path,
                               help="Path to master_profile.json for the letterhead.")
    profile_group.add_argument("--profile-dir", type=Path,
                               help="Profile directory containing master_profile.json.")
    parser.add_argument("--template", type=Path, default=TEMPLATE_DIR / "cover-letter.tex")
    args = parser.parse_args()

    try:
        content_path = args.content.expanduser().resolve()
        profile_path = (
            args.profile
            or (args.profile_dir / "master_profile.json" if args.profile_dir else PROFILE_DIR / "master_profile.json")
        ).expanduser().resolve()
        bundled_profile = (BUNDLED_PROFILE_DIR / "master_profile.json").resolve()
        bundled_example_dir = (SKILL_DIR / "examples").resolve()
        if profile_path == bundled_profile and not content_path.is_relative_to(bundled_example_dir):
            raise ValidationError(
                "Refusing to generate an external cover letter with the bundled example profile; "
                "pass --profile or --profile-dir (or configure JOB_APPLICATION_PROFILE_DIR)."
            )
        profile = load_json(profile_path)
        raw = load_json(args.content)
        legacy_kind = None if isinstance(raw, dict) and raw.get("schema_version") == 2 else "cover_letter"
        content = load_application_content(args.content, profile, legacy_kind=legacy_kind)
        cover = content["cover_letter"]
        location = public_location(profile)
        paragraphs = "\n\n".join(latex_escape(paragraph) for paragraph in cover["paragraphs"])
        signature_asset = resolve_signature_asset(content_path, cover.get("signature_image"))
        signature = r"\vspace{0.65cm}" + "\n"
        if signature_asset:
            signature = (
                r"\vspace{0.35cm}" + "\n"
                + rf"\includegraphics[width=4.3cm]{{{signature_asset}}}" + "\n"
                + r"\vspace{0.1cm}" + "\n"
            )
        values = {
            "__NAME__": latex_escape(profile["full_name"]),
            "__EMAIL__": latex_escape(profile.get("email", "")),
            "__PHONE__": latex_escape(profile.get("phone", "")),
            "__LOCATION__": latex_escape(location),
            "__TITLE__": latex_escape(content["job"]["role"]),
            "__COMPANY__": latex_escape(content["job"]["company"]),
            "__RECIPIENT__": latex_escape(cover["recipient"]),
            "__COMPANY_ADDRESS__": r" \\ ".join(latex_escape(line) for line in cover["company_address"]),
            "__DATE__": latex_escape(cover["date"]),
            "__SUBJECT__": latex_escape(cover["subject"]),
            "__SALUTATION__": latex_escape(cover["salutation"]),
            "__BODY__": paragraphs,
            "__CLOSING__": latex_escape(cover["closing"]),
            "__SIGNATURE__": signature,
            "__SIGNATORY__": latex_escape(cover["signatory"]),
        }
        write_text(args.output, replace_tokens(args.template.read_text(encoding="utf-8"), values))
    except (OSError, ValidationError) as error:
        parser.error(str(error))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
