#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path


ALLOWED_AT_REFS = {
    # User file types (conversation examples)
    "设定",
    "章节",
    "笔记",
    # Sub-agents (conversation examples)
    "写作助手",
    "审稿助手",
    "拆书助手",
}


BANNED_SUBSTRINGS = [
    ".md",  # file extensions in content
    "skills/",  # repo path hints in content
    "references/",  # repo path hints in content
    "./",  # relative path hints in content
]


@dataclass(frozen=True)
class Finding:
    file: Path
    message: str


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _extract_frontmatter(text: str) -> dict[str, str] | None:
    # Minimal YAML frontmatter extraction without external deps.
    if not text.startswith("---\n") and not text.startswith("---\r\n"):
        return None
    # Find the second '---' line.
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return None
    end_idx = None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            end_idx = i
            break
    if end_idx is None:
        return None

    fm: dict[str, str] = {}
    for line in lines[1:end_idx]:
        if not line.strip():
            continue
        if line.lstrip().startswith("#"):
            continue
        if ":" not in line:
            continue
        key, val = line.split(":", 1)
        key = key.strip()
        val = val.strip()
        if key:
            fm[key] = val
    return fm


def _find_at_refs(text: str) -> set[str]:
    # Capture @<name> where name is alnum/underscore/hyphen or CJK.
    # We intentionally ignore markdown inline code and fenced code blocks so that
    # conversation examples like `@某个文件` do not get treated as sub-doc refs.
    refs = set()
    for m in re.finditer(r"@([A-Za-z0-9_\-\u4e00-\u9fff]+)", text):
        refs.add(m.group(1))
    return refs


def _strip_markdown_code(text: str) -> str:
    # Remove fenced code blocks and inline code spans.
    # This is heuristic but works for our intended validation checks.
    text = re.sub(r"```.*?```", "", text, flags=re.DOTALL)
    text = re.sub(r"`[^`]*`", "", text)
    return text


def _check_banned_substrings(text: str, file: Path) -> list[Finding]:
    findings: list[Finding] = []
    for s in BANNED_SUBSTRINGS:
        if s in text:
            findings.append(Finding(file=file, message=f"content contains banned substring {s!r}"))
    return findings


def _check_required_sections(text: str, file: Path) -> list[Finding]:
    findings: list[Finding] = []
    # Keyword-based checks (Chinese).
    if "必要输入" not in text:
        findings.append(Finding(file=file, message="missing required section/keyword: 必要输入"))
    if "交付物" not in text:
        findings.append(Finding(file=file, message="missing required section/keyword: 交付物"))
    return findings


def _validate_structure(skill_dir: Path) -> list[Finding]:
    findings: list[Finding] = []
    if not skill_dir.exists():
        findings.append(Finding(file=skill_dir, message="skill directory does not exist"))
        return findings
    if not skill_dir.is_dir():
        findings.append(Finding(file=skill_dir, message="skill path is not a directory"))
        return findings

    main_doc = skill_dir / "SKILL.md"
    if not main_doc.exists():
        findings.append(Finding(file=main_doc, message="missing SKILL.md"))

    refs_dir = skill_dir / "references"
    # references is optional only if there are no sub-doc @refs; we check later.
    if refs_dir.exists():
        if not refs_dir.is_dir():
            findings.append(Finding(file=refs_dir, message="references exists but is not a directory"))
        else:
            for p in refs_dir.iterdir():
                if p.is_dir():
                    findings.append(Finding(file=p, message="references must not contain subdirectories"))
    return findings


def validate(skill_dir: Path) -> list[Finding]:
    findings: list[Finding] = []
    findings.extend(_validate_structure(skill_dir))

    main_doc = skill_dir / "SKILL.md"
    if not main_doc.exists():
        return findings

    refs_dir = skill_dir / "references"
    text_main = _read_text(main_doc)

    fm = _extract_frontmatter(text_main)
    if fm is None:
        findings.append(Finding(file=main_doc, message="missing or invalid YAML frontmatter"))
    else:
        if not fm.get("name"):
            findings.append(Finding(file=main_doc, message="frontmatter missing required key: name"))
        if not fm.get("description"):
            findings.append(Finding(file=main_doc, message="frontmatter missing required key: description"))

    findings.extend(_check_banned_substrings(text_main, main_doc))
    findings.extend(_check_required_sections(text_main, main_doc))

    at_refs = _find_at_refs(_strip_markdown_code(text_main))
    # Built-in @refs are allowed and do not require sub-doc files.
    candidate_subdocs = {r for r in at_refs if r not in ALLOWED_AT_REFS}

    if candidate_subdocs and not refs_dir.exists():
        findings.append(
            Finding(
                file=refs_dir,
                message="references directory is missing but main doc contains sub-doc references",
            )
        )
        return findings

    existing_subdocs: set[str] = set()
    if refs_dir.exists() and refs_dir.is_dir():
        for p in refs_dir.glob("*.md"):
            existing_subdocs.add(p.stem)

        # Validate each sub-doc file content too.
        for p in refs_dir.glob("*.md"):
            t = _read_text(p)
            findings.extend(_check_banned_substrings(t, p))

    missing = sorted(candidate_subdocs - existing_subdocs)
    if missing:
        findings.append(
            Finding(
                file=main_doc,
                message=f"missing sub-doc files for references: {', '.join('@' + m for m in missing)}",
            )
        )

    return findings


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="validate_nika_skill.py",
        description="Validate a target Nika skill directory in this repo (SKILL.md + references/*.md).",
    )
    parser.add_argument("skill_dir", help="Target skill directory (e.g., skills/拆书指南).")
    args = parser.parse_args(argv)

    skill_dir = Path(args.skill_dir)
    findings = validate(skill_dir)
    if not findings:
        print("OK")
        return 0

    for f in findings:
        print(f"- {f.file}: {f.message}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
