#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""init_subproject.py —— 小说子项目脚手架。

Why this exists
---------------
Standing up a novel subproject by hand took the -1928 project the better part
of two days: directory layout, issue forms, PR checklist, decision ledger,
report index, layered memory. None of that is novel-writing; all of it is
repeated for every book. This script writes the skeleton so the first commit is
about the story, not about plumbing.

What it creates
---------------
    <root>/
      chapters/  worldbuilding/  characters/  notes-personal/  issues/
      .workbuddy/reports/  .workbuddy/memory/
      .github/CODEOWNERS
      .github/ISSUE_TEMPLATE/{config.yml,章节认领.md,设定勘误.md,创作建议.md,文件卫生.md}
      .github/PULL_REQUEST_TEMPLATE.md
      README.md  CHANGELOG.md  progress.md  SYNOPSIS.md
      SUPPORT.md  SECURITY.md
      notes-personal/裁决项台账.md
      .gitattributes  .editorconfig  .gitignore

Existing files are never overwritten unless --force is given.

Usage
-----
    python scripts/init_subproject.py --name "奉天1928" --root ../-1928
    python scripts/init_subproject.py --name "My Novel" --root . --dry-run
    python scripts/init_subproject.py --name "My Novel" --root . --force

Exit codes
----------
0  created (or dry-run completed)
2  usage / IO error

Every write uses newline='\\n'. See scan_hygiene.py for why that matters.
"""

from __future__ import annotations

import argparse
import io
import sys
from pathlib import Path

T = "# ---------------------------------------------------------------------------"


def write(path: Path, content: str, force: bool, dry: bool, log: list) -> None:
    if path.exists() and not force:
        log.append(f"skip   {path}")
        return
    log.append(f"write  {path}")
    if dry:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    with io.open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(content)


# --------------------------------------------------------------------------
# Templates
# --------------------------------------------------------------------------

def t_gitattributes() -> str:
    return (
        "# LF everywhere, including Windows checkouts.\n"
        "* text=auto eol=lf\n"
        "*.md text eol=lf\n"
        "*.py text eol=lf\n"
        "*.yml text eol=lf\n"
    )


def t_editorconfig() -> str:
    return (
        "root = true\n\n"
        "[*]\n"
        "charset = utf-8\n"
        "end_of_line = lf\n"
        "indent_style = space\n"
        "indent_size = 2\n"
        "insert_final_newline = true\n"
        "trim_trailing_whitespace = true\n\n"
        "[*.md]\n"
        "trim_trailing_whitespace = false\n"
    )


def t_gitignore() -> str:
    return (
        "# OS\n.DS_Store\nThumbs.db\nDesktop.ini\n\n"
        "# Editor\n.idea/\n.vscode/\n*.swp\n*.swo\n*~\n\n"
        "# Python\n__pycache__/\n*.py[cod]\n.venv/\nvenv/\n\n"
        "# Temp / backup\n*.tmp\n\n"
        "# Local workspace — reports are working artefacts and are not committed.\n"
        "# Release files must not reference anything under these paths.\n"
        ".workbuddy/reports/\n"
        ".workbuddy/memory/\n"
        ".workbuddy/scripts/\n"
        "_trash/\n"
    )


def t_codeowners() -> str:
    return (
        "# CODEOWNERS\n"
        "# Replace @OWNER with the real GitHub handle before this takes effect.\n"
        "# GitHub silently ignores lines whose owner does not exist.\n\n"
        "# *                    @OWNER\n"
        "# /chapters/           @OWNER\n"
        "# /worldbuilding/      @OWNER\n"
        "# /characters/         @OWNER\n"
        "# /notes-personal/     @OWNER\n"
        "# /.github/            @OWNER\n"
        "# /CONTRIBUTING.md     @OWNER\n"
    )


def t_issue_config(repo_hint: str) -> str:
    return (
        "blank_issues_enabled: true\n"
        "contact_links:\n"
        "  - name: Writing rules and file-hygiene regulations\n"
        f"    url: {repo_hint}blob/main/CONTRIBUTING.md\n"
        "    about: Claiming flow, naming conventions, authority order. Read before posting.\n"
        "  - name: Style guide\n"
        f"    url: {repo_hint}blob/main/STYLE-GUIDE.md\n"
        "    about: Punctuation, word count, naming, quotation conventions.\n"
        "  - name: Synopsis\n"
        f"    url: {repo_hint}blob/main/SYNOPSIS.md\n"
        "    about: Volume structure and time span. Read before outlining.\n"
    )


def t_issue_claim() -> str:
    return (
        "---\n"
        "name: Chapter claim\n"
        "about: Claim a chapter to write or revise\n"
        "title: '[claim] ch-XXX'\n"
        "labels: ['chapter', 'claim']\n"
        "---\n\n"
        "## Chapter\n\n"
        "- Chapter number:\n"
        "- Working title:\n"
        "- Volume / arc:\n\n"
        "## Plan\n\n"
        "- [ ] Outline entry read (`worldbuilding/OUTLINE/`)\n"
        "- [ ] Character dossiers read (`characters/`)\n"
        "- [ ] Hard numbers confirmed (check the ledger before inventing any)\n\n"
        "## Target\n\n"
        "- Word count target:\n"
        "- Draft due:\n\n"
        "## Notes\n\n"
        "Anything the reviewer should watch for.\n"
    )


def t_issue_errata() -> str:
    return (
        "---\n"
        "name: Setting errata\n"
        "about: Report a factual, numeric or continuity error\n"
        "title: '[errata] '\n"
        "labels: ['errata', 'continuity']\n"
        "---\n\n"
        "## Where\n\n"
        "- File:\n"
        "- Line / chapter:\n\n"
        "## What is wrong\n\n"
        "## Why it is wrong\n\n"
        "Cite the source or the internal ledger entry.\n\n"
        "## Suggested fix\n\n"
        "## Blast radius\n\n"
        "- [ ] Appears in more than one chapter\n"
        "- [ ] Appears in the outline\n"
        "- [ ] Already recorded in the decision ledger (`notes-personal/裁决项台账.md`)\n"
    )


def t_issue_proposal() -> str:
    return (
        "---\n"
        "name: Creative proposal\n"
        "about: Propose a plot thread, character or world element\n"
        "title: '[idea] '\n"
        "labels: ['enhancement', 'creative']\n"
        "---\n\n"
        "## Proposal\n\n"
        "## Where it would land\n\n"
        "- Volume / arc:\n"
        "- Chapters affected:\n\n"
        "## Does it collide with anything\n\n"
        "Search the ledger and the setting docs first. State what you checked.\n\n"
        "## Cost\n\n"
        "New characters, new locations, new numbers — list them.\n"
    )


def t_issue_hygiene() -> str:
    return (
        "---\n"
        "name: File hygiene\n"
        "about: Junk files, encoding damage, line-ending drift\n"
        "title: '[hygiene] '\n"
        "labels: ['hygiene', 'chore']\n"
        "---\n\n"
        "## Symptom\n\n"
        "## Affected paths\n\n"
        "## Detection\n\n"
        "```\n"
        'python "<SCRIPTS>/scan_hygiene.py" --root .\n'
        "```\n\n"
        "## Proposed cleanup\n\n"
        "State whether any trace needs to be recorded in CHANGELOG before removal.\n"
    )


def t_pr_template(scripts: str) -> str:
    return (
        "## What this PR contains\n\n"
        "- Type: [ ] new chapter  [ ] revision  [ ] setting/outline  [ ] errata  "
        "[ ] hygiene  [ ] engineering\n"
        "- Object: chapter ___ / file ___\n\n"
        "## Summary\n\n"
        "> \n\n"
        "## Draft-first flow\n\n"
        "- [ ] Change landed in `notes-personal/` draft first\n"
        f"- [ ] `{scripts}/humanizer_check.py <file>` run (PASS, or WARN reviewed)\n"
        "- [ ] Review report archived to `.workbuddy/reports/` and indexed\n"
        "- [ ] Release sync done through `_promote_draft.py`, or this is an errata-only edit\n\n"
        "## Gates\n\n"
        "- Three-stage review (三审制度), each stage archived to `.workbuddy/reports/`:\n"
        f"  - [ ] `{scripts}/review_all.py --stage first`  (初审·责任编辑: humanizer/scale/punctuation)\n"
        f"  - [ ] `{scripts}/review_all.py --stage second` (复审·编辑部主任: continuity/rationality)\n"
        f"  - [ ] `{scripts}/review_all.py --stage final`  (终审·主编: full regression + sign-off)\n"
        f"- [ ] `{scripts}/scan_hygiene.py --root .`\n"
        f"- [ ] `{scripts}/check_refs.py --root .`\n\n"
        "## Updated\n\n"
        "- [ ] `CHANGELOG.md`\n"
        "- [ ] `progress.md` (when chapters move)\n"
        "- [ ] `notes-personal/裁决项台账.md` (when a ruling is made)\n"
    )


def t_support(scripts: str) -> str:
    return (
        "# Support\n\n"
        "## Where to go\n\n"
        "| You want to | Go to |\n"
        "|---|---|\n"
        "| Claim a chapter | Chapter claim issue |\n"
        "| Report a setting / number / continuity error | Setting errata issue |\n"
        "| Propose plot, character, world element | Creative proposal issue |\n"
        "| Report junk or encoding damage | File hygiene issue |\n"
        "| Submit finished text | Pull request (see the PR template) |\n"
        "| Report a leaked credential | SECURITY.md — **never a public issue** |\n\n"
        "## Check before posting\n\n"
        "1. Has someone already filed this (search open *and* closed)?\n"
        "2. Has a review report already handled it (`.workbuddy/reports/README.md`)?\n"
        "3. Is the conflict already on the ledger (`notes-personal/裁决项台账.md`)?\n\n"
        "## Question template\n\n"
        "```\n"
        "Goal:\n"
        "Tried:\n"
        "Stuck at: (file + line, or verbatim error)\n"
        "Expected:\n"
        "```\n\n"
        "## Tooling\n\n"
        f"Shared scripts live in the skill repository (`{scripts}/`) and are invoked "
        "from this project root.\n"
    )


def t_security() -> str:
    return (
        "# Security Policy\n\n"
        "## Scope\n\n"
        "This is a content repository. No build, no release, no runtime dependencies.\n\n"
        "## Reporting\n\n"
        "This repository must never contain secrets: API keys, tokens, private keys, "
        "passwords, connection strings.\n\n"
        "If you find one:\n\n"
        "1. **Do not** paste the credential into a public issue. Describe the location "
        "(file + line) and the type only.\n"
        "2. Report privately through GitHub Security Advisories.\n"
        "3. We aim to remove or rotate within 72 hours of confirmation.\n\n"
        "## Not a security issue\n\n"
        "- Historical claims, fictional settings, numeric errors -> errata issue\n"
        "- Junk files and encoding damage -> hygiene issue\n"
        "- Licensing -> LICENSE\n"
    )


def t_readme(name: str, scripts: str) -> str:
    return (
        f"# {name}\n\n"
        "> One-line pitch. Replace this line.\n\n"
        "## Structure\n\n"
        "```\n"
        "chapters/        release text (the only authoritative copy)\n"
        "worldbuilding/   setting docs + OUTLINE/\n"
        "characters/      character dossiers\n"
        "notes-personal/  working drafts (never published from here)\n"
        "issues/          per-arc discussion\n"
        ".workbuddy/reports/  review reports + index\n"
        ".workbuddy/memory/   layered session memory\n"
        "```\n\n"
        "## Change order (mandatory)\n\n"
        "1. Edit the draft in `notes-personal/`\n"
        f"2. `{scripts}/humanizer_check.py <file>`\n"
        "3. Archive the review report and index it\n"
        "4. Gate passes\n"
        f"5. `{scripts}/_promote_draft.py <chapter>` to sync `chapters/`\n"
        "6. Record in `CHANGELOG.md` / `progress.md`\n\n"
        "## Licence\n\n"
        "Text: CC BY-NC-SA 4.0. See LICENSE.\n"
    )


def t_changelog(name: str) -> str:
    return (
        "# Changelog\n\n"
        f"All notable changes to 《{name}》.\n\n"
        "Format: one entry per change — title line, metadata line, then one sentence "
        "per line. Long content goes under a `####` detail section, never inside a table "
        "cell.\n\n"
        "## [Unreleased]\n\n"
        "### Added\n\n"
        "- (project skeleton created by `init_subproject.py`)\n"
    )


def t_progress(name: str) -> str:
    return (
        f"# Progress — 《{name}》\n\n"
        "Single source of truth for progress. Chapter counts come from `chapters/` only.\n\n"
        "| Volume | Arc | Chapters planned | Chapters drafted | Chapters released |\n"
        "|---|---|---|---|---|\n"
        "| 1 | | | | |\n\n"
        "## Conventions\n\n"
        "- Drafted = exists in `notes-personal/`.\n"
        "- Released = promoted into `chapters/`.\n"
        "- Word counts use the `cn()` convention (Chinese characters only).\n"
    )


def t_synopsis(name: str) -> str:
    return (
        f"# Synopsis — 《{name}》\n\n"
        "## Premise\n\n"
        "> The one divergence that makes this book this book. One paragraph.\n\n"
        "## Volumes\n\n"
        "| Volume | Span | Arc count | Core question |\n"
        "|---|---|---|---|\n"
        "| 1 | | | |\n\n"
        "## Constraints\n\n"
        "- Time window:\n"
        "- Hard boundaries (what may never happen):\n"
    )


def t_ledger() -> str:
    return (
        "# Decision ledger\n\n"
        "Every cross-session ruling gets a number and a line here. A ruling that is not "
        "on this ledger is not a ruling.\n\n"
        "| ID | Date | Subject | Ruling | Where it landed | Report |\n"
        "|---|---|---|---|---|---|\n"
        "| D001 | | | | | |\n\n"
        "## Rules\n\n"
        "- One row per ruling, never edited in place after it has been applied.\n"
        "- Superseded rulings stay; mark them superseded and point to the new ID.\n"
        "- `Where it landed` names the concrete file/chapter so the next pass can "
        "verify rather than re-decide.\n"
    )


def t_reports_readme() -> str:
    return (
        "# Reports index\n\n"
        "A report is not archived until it is listed here. Unlisted == never happened.\n\n"
        "| # | Date | Subject | Type | File | Words |\n"
        "|---|---|---|---|---|---|\n"
        "| 001 | | | | | |\n\n"
        "## Rules\n\n"
        "- Number sequentially, never reuse a number.\n"
        "- `Words` uses the humanizer-reported count, so the column is comparable.\n"
        "- Three indexes must agree: this file, `CHANGELOG.md`, `progress.md`.\n"
    )


def t_memory_index() -> str:
    return (
        "# Memory hall — entrance\n\n"
        "Layering: **year -> quarter -> month -> day**. Upper layers hold index and "
        "distilled conclusions only; detail lives in the day files. Side halls hold "
        "cross-time conventions and are not archived by date.\n\n"
        "## Year\n\n"
        "| Year | File | Summary |\n"
        "|---|---|---|\n\n"
        "## Quarter\n\n"
        "## Month\n\n"
        "## Day\n\n"
        "## Side halls\n\n"
        "## Maintenance\n\n"
        "- Day: append only, never rewrite.\n"
        "- Month: distilled from the day layer at month end.\n"
        "- Quarter: distilled from the month layer.\n"
        "- Year: distilled from the quarter layer.\n"
        "- After editing any layer, check that the index above still resolves.\n"
    )


# --------------------------------------------------------------------------
# Driver
# --------------------------------------------------------------------------

def build(root: Path, name: str, scripts: str, owner: str, force: bool, dry: bool) -> list:
    log: list = []
    gh = root / ".github"
    it = gh / "ISSUE_TEMPLATE"

    for d in ("chapters", "worldbuilding", "characters", "notes-personal", "issues",
              ".workbuddy/reports", ".workbuddy/memory"):
        p = root / d
        log.append(f"mkdir  {p}")
        if not dry:
            p.mkdir(parents=True, exist_ok=True)

    repo_hint = f"https://github.com/{owner}/{root.name}/" if owner else ""

    targets = [
        (root / ".gitattributes", t_gitattributes()),
        (root / ".editorconfig", t_editorconfig()),
        (root / ".gitignore", t_gitignore()),
        (gh / "CODEOWNERS", t_codeowners()),
        (it / "config.yml", t_issue_config(repo_hint or "")),
        (it / "章节认领.md", t_issue_claim()),
        (it / "设定勘误.md", t_issue_errata()),
        (it / "创作建议.md", t_issue_proposal()),
        (it / "文件卫生.md", t_issue_hygiene().replace("<SCRIPTS>", scripts)),
        (gh / "PULL_REQUEST_TEMPLATE.md", t_pr_template(scripts)),
        (root / "SUPPORT.md", t_support(scripts)),
        (root / "SECURITY.md", t_security()),
        (root / "README.md", t_readme(name, scripts)),
        (root / "CHANGELOG.md", t_changelog(name)),
        (root / "progress.md", t_progress(name)),
        (root / "SYNOPSIS.md", t_synopsis(name)),
        (root / "notes-personal" / "裁决项台账.md", t_ledger()),
        (root / ".workbuddy" / "reports" / "README.md", t_reports_readme()),
        (root / ".workbuddy" / "memory" / "MEMORY.md", t_memory_index()),
    ]

    for path, content in targets:
        write(path, content, force, dry, log)
    return log


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Scaffold a novel subproject.")
    ap.add_argument("--name", required=True, help="novel title")
    ap.add_argument("--root", default=".", help="target directory (created if missing)")
    ap.add_argument("--scripts", default="../GitHub Novel Serialization Skill/scripts",
                    help="relative path to the shared scripts directory")
    ap.add_argument("--owner", default="OWNER", help="GitHub owner, used in generated links")
    ap.add_argument("--force", action="store_true", help="overwrite existing files")
    ap.add_argument("--dry-run", action="store_true", help="print the plan, write nothing")
    args = ap.parse_args(argv)

    root = Path(args.root)
    if not args.dry_run:
        root.mkdir(parents=True, exist_ok=True)

    log = build(root, args.name, args.scripts, args.owner, args.force, args.dry_run)
    for line in log:
        print(line)
    print(f"\n{len(log)} item(s) planned." if args.dry_run else f"\n{len(log)} item(s) processed.")

    if not args.dry_run:
        print("\nNext:")
        print(f"  1. git init && git remote add origin <url>   (in {root})")
        print(f"  2. python \"{args.scripts}/humanizer_check.py\" --help")
        print(f"  3. python \"{args.scripts}/scan_hygiene.py\" --root . --fail-on crlf,junk")
        print("  4. Replace @OWNER in .github/CODEOWNERS before pushing.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
