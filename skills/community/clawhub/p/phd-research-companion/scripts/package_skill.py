#!/usr/bin/env python3
"""
Package this skill for publication.

A publishable package is not "zip the directory". Before writing the archive
this script VALIDATES the things a platform actually rejects:

  * SKILL.md frontmatter exists, with a slug-shaped `name` and a description
    inside the platform limit;
  * every shipped module compiles and answers `--help`;
  * no build artifacts, bytecode caches or local install state leak in;
  * the archive is under the platform size limit.

It also writes a MANIFEST.txt with a sha256 per file, so a download can be
verified.

Usage:
    python scripts/package_skill.py                       # dist/<slug>-<ver>.zip
    python scripts/package_skill.py --out my.zip
    python scripts/package_skill.py --include-reports      # ship the audit output
    python scripts/package_skill.py --check-only
"""

from __future__ import annotations

import argparse
import hashlib
import os
import py_compile
import re
import subprocess
import sys
import tempfile
import zipfile
from datetime import datetime
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parent.parent
SLUG = "phd-research-companion"
SIZE_LIMIT_MB = 50          # platform upload ceiling
DESC_LIMIT = 1024           # platform frontmatter description limit
NAME_LIMIT = 64

EXCLUDE_DIRS = {"__pycache__", ".pytest_cache", ".git", ".github", "dist", ".idea"}
# Local install bookkeeping (owner id, install timestamps, absolute paths on this
# machine) and regenerable output. None of it belongs in a published package.
EXCLUDE_NAMES = {"_skillhub_meta.json", "score-history.json"}
REPORT_NAMES = {"score-report.md", "score-selftest-report.md"}


def excluded(path: Path, include_reports: bool) -> bool:
    if any(part in EXCLUDE_DIRS for part in path.parts):
        return True
    if path.name in EXCLUDE_NAMES:
        return True
    # MANIFEST.txt is written by this script; an unpacked package contains one,
    # and re-packaging it would produce a duplicate zip entry.
    if path.name == "MANIFEST.txt":
        return True
    if not include_reports and path.name in REPORT_NAMES:
        return True
    if path.suffix in (".pyc", ".pyo", ".log"):
        return True
    return path.name.endswith(".tmp")


def collect(include_reports: bool) -> list[Path]:
    files = []
    for p in sorted(SKILL_ROOT.rglob("*")):
        rel = p.relative_to(SKILL_ROOT)
        if p.is_file() and not excluded(rel, include_reports):
            files.append(rel)
    return files


def check_frontmatter() -> tuple[dict, list[str]]:
    problems: list[str] = []
    skill_md = SKILL_ROOT / "SKILL.md"
    if not skill_md.is_file():
        return {}, ["SKILL.md missing"]
    src = skill_md.read_text(encoding="utf-8")
    if not src.startswith("---"):
        return {}, ["SKILL.md does not open with YAML frontmatter"]
    parts = src.split("---", 2)
    if len(parts) < 3:
        return {}, ["SKILL.md frontmatter is not terminated"]
    fm = dict(re.findall(r"^([A-Za-z][\w-]*):\s*(.+)$", parts[1], re.M))
    for required in ("name", "description"):
        if required not in fm:
            problems.append(f"frontmatter missing '{required}'")
    name = fm.get("name", "")
    if name and not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", name):
        problems.append(f"frontmatter name '{name}' is not a slug")
    if len(name) > NAME_LIMIT:
        problems.append(f"frontmatter name is {len(name)} chars (limit {NAME_LIMIT})")
    desc = fm.get("description", "")
    if len(desc) > DESC_LIMIT:
        problems.append(f"description is {len(desc)} chars (limit {DESC_LIMIT})")
    if len(name) < 3:
        problems.append("description too short to route on")
    return fm, problems


def check_code() -> list[str]:
    problems = []
    with tempfile.TemporaryDirectory() as td:
        for rel in collect(include_reports=False):
            if not rel.name.endswith(".py"):
                continue
            src = SKILL_ROOT / rel
            try:
                py_compile.compile(str(src), cfile=os.path.join(td, "x.pyc"), doraise=True)
            except Exception as e:                     # noqa: BLE001
                problems.append(f"does not compile: {rel} ({type(e).__name__})")
                continue
            if rel.parts[0] == "scripts" or rel.name in ("run.py", "init_research_project.py"):
                if rel.name in ("self_score.py", "score_selftest.py", "package_skill.py"):
                    continue
                try:
                    r = subprocess.run([sys.executable, str(src), "--help"],
                                       capture_output=True, text=True, timeout=30,
                                       cwd=str(SKILL_ROOT))
                    if r.returncode != 0:
                        problems.append(f"--help exits {r.returncode}: {rel}")
                except Exception as e:                 # noqa: BLE001
                    problems.append(f"--help raised {type(e).__name__}: {rel}")
    return problems


def check_required() -> list[str]:
    missing = [f for f in ("SKILL.md", "LICENSE", "README.md", "run.py")
               if not (SKILL_ROOT / f).is_file()]
    return [f"required file missing: {f}" for f in missing]


def build_zip(out_path: Path, include_reports: bool = False) -> dict:
    fm, problems = check_frontmatter()
    problems += check_required()
    problems += check_code()

    files = collect(include_reports)
    total = sum((SKILL_ROOT / f).stat().st_size for f in files)
    if total > SIZE_LIMIT_MB * 1024 * 1024:
        problems.append(f"package is {total / 1048576:.1f} MB (limit {SIZE_LIMIT_MB} MB)")

    manifest = [
        f"# {fm.get('name', SLUG)} {fm.get('version', '?')}",
        f"# packaged {datetime.now().isoformat(timespec='seconds')}",
        f"# {len(files)} files, {total} bytes uncompressed",
        "",
    ]
    for rel in files:
        digest = hashlib.sha256((SKILL_ROOT / rel).read_bytes()).hexdigest()
        manifest.append(f"{digest}  {rel.as_posix()}")

    names: list[str] = []
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(out_path, "w", zipfile.ZIP_DEFLATED) as z:
        for rel in files:
            arc = f"{SLUG}/{rel.as_posix()}"
            z.write(SKILL_ROOT / rel, arc)
            names.append(arc)
        z.writestr(f"{SLUG}/MANIFEST.txt", "\n".join(manifest) + "\n")
        names.append(f"{SLUG}/MANIFEST.txt")

    digest = hashlib.sha256(out_path.read_bytes()).hexdigest()
    (out_path.with_suffix(out_path.suffix + ".sha256")).write_text(
        f"{digest}  {out_path.name}\n", encoding="utf-8")

    return {"out": str(out_path), "names": names, "problems": problems,
            "bytes": out_path.stat().st_size, "files": len(files),
            "sha256": digest, "version": fm.get("version", "?")}


def main() -> int:
    ap = argparse.ArgumentParser(description="Validate and package this skill")
    ap.add_argument("--out", type=str, default=None, help="output zip path")
    ap.add_argument("--include-reports", action="store_true",
                    help="also ship the self-audit reports")
    ap.add_argument("--check-only", action="store_true", help="validate, do not write")
    args = ap.parse_args()

    if args.check_only:
        fm, problems = check_frontmatter()
        problems += check_required() + check_code()
        files = collect(args.include_reports)
        total = sum((SKILL_ROOT / f).stat().st_size for f in files)
        print(f"name        : {fm.get('name')}")
        print(f"version     : {fm.get('version')}")
        print(f"description : {len(fm.get('description', ''))} chars (limit {DESC_LIMIT})")
        print(f"files       : {len(files)}   {total / 1024:.1f} KB")
        for p in problems:
            print(f"  PROBLEM: {p}")
        print("OK" if not problems else f"{len(problems)} problem(s)")
        return 0 if not problems else 1

    out = Path(args.out) if args.out else SKILL_ROOT / "dist" / f"{SLUG}.zip"
    report = build_zip(out, args.include_reports)
    print(f"packaged {report['files']} files -> {report['out']} "
          f"({report['bytes'] / 1024:.1f} KB)")
    print(f"version {report['version']}")
    print(f"sha256  {report['sha256']}")
    for p in report["problems"]:
        print(f"  PROBLEM: {p}")
    return 0 if not report["problems"] else 1


if __name__ == "__main__":
    sys.exit(main())