#!/usr/bin/env python3
"""Validate and package this skill for ClawHub-style distribution.

Usage:
  python scripts/package_clawhub_skill.py --skill-dir ./paper-defense-qa-code-training --dist ./dist

Outputs:
  dist/paper-defense-qa-code-training-v<version>-clawhub.zip
  dist/paper-defense-qa-code-training-v<version>.skill

The .skill file is a zip archive with a .skill suffix.
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import zipfile
from pathlib import Path

SLUG_RE = re.compile(r"^[a-z0-9][a-z0-9-]*$")
SEMVER_RE = re.compile(r"^\d+\.\d+\.\d+(?:[-+][0-9A-Za-z.-]+)?$")
MAX_SIZE_BYTES = 50 * 1024 * 1024

TEXT_EXTENSIONS = {
    ".md",
    ".txt",
    ".json",
    ".yaml",
    ".yml",
    ".py",
    ".sh",
    ".toml",
    ".csv",
    ".tsv",
    ".svg",
    ".html",
    ".css",
    ".js",
}
TEXT_BASENAMES = {
    "README",
    "SKILL",
}
IGNORE_DIRS = {"__pycache__", ".git", ".clawhub", ".clawdhub", "dist", "build", ".pytest_cache"}
IGNORE_EXTS = {".pyc", ".pyo", ".zip", ".skill"}
IGNORE_BASENAMES = {".clawhubignore", ".clawdhubignore", ".gitignore", "LICENSE"}


def read_frontmatter(skill_md: Path) -> dict[str, str]:
    text = skill_md.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise ValueError("SKILL.md must start with YAML frontmatter")
    end = text.find("\n---", 4)
    if end == -1:
        raise ValueError("SKILL.md frontmatter is not closed")
    block = text[4:end]
    meta: dict[str, str] = {}
    for line in block.splitlines():
        if not line.strip() or line.startswith(" ") or line.startswith("\t"):
            continue
        if ":" in line:
            key, value = line.split(":", 1)
            meta[key.strip()] = value.strip().strip('"')
    return meta


def is_text_file(path: Path) -> bool:
    if path.name in TEXT_BASENAMES:
        return True
    if path.stem in TEXT_BASENAMES:
        return True
    return path.suffix.lower() in TEXT_EXTENSIONS


def iter_package_files(skill_dir: Path):
    for path in sorted(skill_dir.rglob("*")):
        if path.is_dir():
            continue
        rel = path.relative_to(skill_dir)
        if any(part in IGNORE_DIRS for part in rel.parts):
            continue
        if path.name in IGNORE_BASENAMES:
            continue
        if path.suffix.lower() in IGNORE_EXTS:
            continue
        yield path


def validate(skill_dir: Path) -> list[str]:
    errors: list[str] = []
    if not skill_dir.exists() or not skill_dir.is_dir():
        return [f"Skill directory not found: {skill_dir}"]
    if not SLUG_RE.match(skill_dir.name):
        errors.append(f"Skill folder name must be lowercase URL-safe slug: {skill_dir.name}")
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        errors.append("Missing SKILL.md")
    else:
        try:
            meta = read_frontmatter(skill_md)
        except ValueError as exc:
            errors.append(str(exc))
            meta = {}
        for key in ["name", "description", "version"]:
            if not meta.get(key):
                errors.append(f"SKILL.md frontmatter missing {key}")
        if meta.get("name") and not SLUG_RE.match(meta["name"]):
            errors.append(f"frontmatter name should be URL-safe: {meta['name']}")
        if meta.get("version") and not SEMVER_RE.match(meta["version"]):
            errors.append(f"frontmatter version should be semver: {meta['version']}")
        if meta.get("description") and len(meta["description"]) < 80:
            errors.append("frontmatter description is too short to reliably trigger the skill")
        meta_json = skill_dir / "_meta.json"
        if meta_json.exists():
            try:
                package_meta = json.loads(meta_json.read_text(encoding="utf-8"))
            except json.JSONDecodeError as exc:
                errors.append(f"_meta.json is invalid JSON: {exc}")
            else:
                if package_meta.get("version") != meta.get("version"):
                    errors.append("_meta.json version should match SKILL.md frontmatter version")
    license_candidates = [skill_dir / "LICENSE.md", skill_dir / "README.md", skill_dir / "SKILL.md"]
    license_text = "\n".join(
        candidate.read_text(encoding="utf-8", errors="ignore")
        for candidate in license_candidates
        if candidate.exists()
    )
    if "MIT No Attribution" not in license_text and "MIT-0" not in license_text:
        errors.append("Bundle should clearly state MIT No Attribution / MIT-0 in LICENSE.md, README.md, or SKILL.md")
    total = 0
    for path in iter_package_files(skill_dir):
        total += path.stat().st_size
        if not is_text_file(path):
            errors.append(f"Non-text or unsupported file type: {path.relative_to(skill_dir)}")
    if total > MAX_SIZE_BYTES:
        errors.append(f"Bundle exceeds 50MB limit: {total} bytes")
    return errors


def make_archive(skill_dir: Path, output: Path) -> None:
    if output.exists():
        output.unlink()
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for path in iter_package_files(skill_dir):
            arcname = skill_dir.name + "/" + str(path.relative_to(skill_dir))
            zf.write(path, arcname)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--skill-dir", default=".")
    parser.add_argument("--dist", default="dist")
    args = parser.parse_args()

    skill_dir = Path(args.skill_dir).resolve()
    dist = Path(args.dist).resolve()
    errors = validate(skill_dir)
    if errors:
        print("ClawHub package validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    dist.mkdir(parents=True, exist_ok=True)
    version = read_frontmatter(skill_dir / "SKILL.md")["version"]
    zip_path = dist / f"{skill_dir.name}-v{version}-clawhub.zip"
    skill_path = dist / f"{skill_dir.name}-v{version}.skill"
    make_archive(skill_dir, zip_path)
    shutil.copyfile(zip_path, skill_path)
    print(f"Wrote {zip_path}")
    print(f"Wrote {skill_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
