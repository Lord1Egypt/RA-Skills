#!/usr/bin/env python3
"""Guard the job-application → job-hunt migration: prove it MOVED content, not deleted it.

"Split it into references" quietly becomes "rewrite and condense": the file
shrinks, the commit says zero information loss, and operational rules are gone.
That regression is invisible in review — the diff is thousands of lines and every
removed line *looks* like it landed somewhere. So make it mechanical. Every
substantive line of the baseline tree must still be findable, verbatim, somewhere
a skill trigger can reach.

    # in CI, against the tag created during the migration
    python3 scripts/check_skill_lossless.py --baseline job-application-baseline

    # against a tree on disk
    python3 scripts/check_skill_lossless.py --baseline /Users/x/.claude/skills/job-application

Exit 0 = every baseline line accounted for. Exit 1 = content was lost, or the
allowlist names a file that is still present. Exit 2 = the baseline could not be
read at all — which is NOT the same answer as "content was lost", and must not
share an exit code with it.

This script is the one deliberate exception to job-hunt's gate contract: it is a
repo-level CI check, takes no --workspace, imports no journal and writes no
receipt. SKILL.md's self-check lists it under CI for that reason.

WHAT THIS DOES NOT PROVE — read before quoting a score. It measures whether the
bytes still exist, not whether they reach the context at the moment they are
needed. A refactor can score a perfect result and still degrade the skill,
because the regression is in *when* content arrives, not *whether* it survives.
Content preservation is necessary and nowhere near sufficient; the only real test
of a layering change is running the skill end-to-end afterwards and looking at
what the output is missing.

Matching is deliberately forgiving about FORM and strict about SUBSTANCE. Text is
NFKC-folded, dashes and smart quotes unified, punctuation dropped, case ignored,
and the whole corpus joined into one string before matching — so a line may be
re-wrapped, re-indented, moved to another file, or have its bullet marker changed
and still pass. What it may not do is lose a word.

Deliberate deletions are legitimate. Record them in the allowlist with a reason:
`waived` for individual lines (keyed on a hash of the normalized line, so editing
the line revokes its waiver), `deleted_files` for whole files. Adapted from
slides_maker's scripts/check_skill_lossless.py.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
import unicodedata
from pathlib import Path, PurePosixPath

sys.path.insert(0, str(Path(__file__).resolve().parent))
import paths

# Lines shorter than this once normalized are structural noise — bare list
# markers, `---` rules, lone code fences, one-word headings. They carry no rule
# that can be lost, and checking them fails every time a heading is renamed.
DEFAULT_MIN_CHARS = 25

CORPUS_SUFFIXES = (".md", ".yaml")
# Everything a skill trigger can eventually reach, keyed on the TOP-LEVEL
# directory. `docs/` is deliberately out: a line that survives only in the
# design doc has not survived — and in this repo the plan files under docs/
# quote SKILL.md verbatim, so a recursive corpus would let a condensed SKILL.md
# report LOSSLESS against itself. `scripts/` is out for the same reason in
# reverse: test fixtures are not skill content.
CORPUS_DIRS = (".", "modes", "references", "agents", "assets")


class BaselineUnavailable(Exception):
    """The baseline tree could not be read — a different answer from 'lost'."""

_DASHES = dict.fromkeys(map(ord, "—–‒―−"), "-")
_QUOTES = {0x2019: "'", 0x2018: "'", 0x201C: '"', 0x201D: '"', ord("`"): "'"}

# Keep alphanumerics and CJK/kana/hangul; everything else becomes a separator.
# Dropping CJK would blind the check on the Chinese passages this skill carries.
_DROP = re.compile(
    r"[^0-9a-z"
    r"぀-ヿ"      # kana
    r"㐀-䶿"      # CJK ext A
    r"一-鿿"      # CJK unified
    r"가-힯"      # hangul
    r"豈-﫿"      # CJK compatibility ideographs
    r"]+"
)


def normalize(text: str) -> str:
    """Fold away formatting so only word content is compared."""
    text = unicodedata.normalize("NFKC", text)
    text = text.translate(_DASHES).translate(_QUOTES)
    text = text.lower()
    text = _DROP.sub(" ", text)
    return " ".join(text.split())


def line_key(normalized: str) -> str:
    return hashlib.sha1(normalized.encode("utf-8")).hexdigest()[:16]


def in_corpus(rel) -> bool:
    """Is this relpath part of the corpus a skill trigger can reach?

    ONE rule, used by BOTH sides of the comparison. When the two sides used
    different rules the check reported losses that never happened: the git-ref
    baseline read `scripts/tests/fixtures/*.yaml` (26 substantive lines, measured)
    and the on-disk corpus never scanned `scripts/`, so a byte-identical tree
    reported CONTENT LOST. A check that cries wolf on the very migration it was
    written for is a check nobody runs twice.
    """
    rel = str(rel).replace("\\", "/")
    if not rel.endswith(CORPUS_SUFFIXES):
        return False
    parts = PurePosixPath(rel).parts
    top = parts[0] if len(parts) > 1 else "."
    return top in CORPUS_DIRS


def baseline_docs(spec: str, repo: Path) -> dict:
    """{relpath: text} for the baseline tree. `spec` is a git ref or a directory."""
    p = Path(spec)
    if p.is_dir():
        out = {}
        for f in sorted(p.rglob("*")):
            rel = f.relative_to(p)
            if f.is_file() and in_corpus(rel):
                out[rel.as_posix()] = f.read_text(encoding="utf-8", errors="replace")
        return out
    listing = subprocess.run(["git", "ls-tree", "-r", "--name-only", spec],
                             cwd=repo, capture_output=True, text=True, encoding="utf-8")
    if listing.returncode != 0:
        raise BaselineUnavailable(
            f"cannot read baseline {spec!r}: {listing.stderr.strip()}")
    out = {}
    for rel in listing.stdout.split("\n"):
        rel = rel.strip()
        if not rel or not in_corpus(rel):
            continue
        blob = subprocess.run(["git", "show", f"{spec}:{rel}"],
                              cwd=repo, capture_output=True, text=True, encoding="utf-8")
        if blob.returncode == 0:
            out[rel] = blob.stdout
    return out


def build_corpus(skill_dir: Path) -> tuple:
    files = sorted(f for f in skill_dir.rglob("*")
                   if f.is_file() and in_corpus(f.relative_to(skill_dir)))
    joined = "\n".join(f.read_text(encoding="utf-8", errors="replace") for f in files)
    return normalize(joined), files


def _find_repo(start: Path):
    p = start.resolve()
    while True:
        if (p / ".git").exists():
            return p
        if p == p.parent:
            return None
        p = p.parent


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(
        description="Verify a skill refactor moved content instead of deleting it.")
    ap.add_argument("--baseline", required=True,
                    help="a git ref (e.g. job-application-baseline) or a directory path")
    ap.add_argument("--skill-dir", default=None,
                    help="skill root (default: this script's parent directory's parent)")
    ap.add_argument("--repo", default=None, help="git repo for a ref baseline")
    ap.add_argument("--allow", default=None, help="JSON allowlist (default: scripts/lossless-allowlist.json)")
    ap.add_argument("--min-chars", type=int, default=DEFAULT_MIN_CHARS)
    ap.add_argument("--report", default=None, help="write the full missing-line report here")
    args = ap.parse_args(argv)

    skill_dir = Path(args.skill_dir).resolve() if args.skill_dir else paths.SKILL_ROOT
    repo = Path(args.repo).resolve() if args.repo else (
        _find_repo(Path(__file__).resolve().parent) or skill_dir)
    allow_path = Path(args.allow) if args.allow else paths.lossless_allowlist(skill_dir)

    allow, deleted_files = {}, {}
    if allow_path.exists():
        data = json.loads(allow_path.read_text(encoding="utf-8"))
        allow = data.get("waived") or {}
        deleted_files = data.get("deleted_files") or {}

    try:
        docs = baseline_docs(args.baseline, repo)
    except BaselineUnavailable as exc:
        print(str(exc), file=sys.stderr)
        return 2
    corpus, files = build_corpus(skill_dir)

    checked, waived = 0, 0
    missing = []          # (relpath, lineno, raw, normalized)
    for rel, text in sorted(docs.items()):
        for n, raw in enumerate(text.split("\n"), 1):
            norm = normalize(raw)
            if len(norm) < args.min_chars:
                continue
            checked += 1
            if norm in corpus:
                continue
            if line_key(norm) in allow:
                waived += 1
                continue
            missing.append((rel, n, raw.strip(), norm))

    stale = [rel for rel in sorted(deleted_files) if (skill_dir / rel).exists()]

    for rel, n, raw, _ in missing[:40]:
        print(f"LOST: {rel}:{n}: {raw[:150]}")
    if len(missing) > 40:
        print(f"LOST: … and {len(missing) - 40} more"
              + (f" (full list: {args.report})" if args.report else " (use --report for all)"))
    for rel in stale:
        print(f"NOT_DELETED: {rel} is listed in {allow_path.name} as deliberately deleted "
              f"but still exists — remove the entry or the file")

    if args.report:
        with open(args.report, "w", encoding="utf-8") as fh:
            fh.write(f"# Lost content report\n\nBaseline: `{args.baseline}`\n\n")
            for rel, n, raw, nrm in missing:
                fh.write(f"- **{rel}:{n}** `{line_key(nrm)}`\n  > {raw}\n")

    ok = not missing and not stale
    verdict = "LOSSLESS" if ok else "CONTENT LOST"
    print(f"{verdict}: {checked - len(missing)}/{checked} baseline lines accounted for "
          f"across {len(files)} files"
          + (f", {waived} waived" if waived else "")
          + (f", {len(stale)} stale deletion entr(ies)" if stale else ""))
    if not ok:
        print("Moving these into SKILL.md, modes/ or references/ fixes it. If a line is "
              "genuinely meant to go, add it to the allowlist and write down why.")
    return 0 if ok else 1


if __name__ == "__main__":
    from cli_io import configure_output

    configure_output()
    sys.exit(main())
