#!/usr/bin/env python3
# Copyright (c) 2026 ratingtesting — MIT-0 (see LICENSE). Free to use/modify/redistribute, no attribution required.
"""export_skill.py — bundle the entire keelwright skill into a portable .zip

Packages the public skill (excludes internal/ and backups/ unless --all) plus QA results
and the current git state, so it can be unpacked on another machine in one step.

Stdlib only. Usage:
  python export_skill.py                  → export to ~/kw-qa/keelwright-export-<ts>.zip
  python export_skill.py -o /tmp/kw.zip   → export to a specific path
  python export_skill.py --all            → include internal/ and backups/ (full state)
"""
import zipfile, os, time, argparse, hashlib
from pathlib import Path

SKILL = Path(os.environ.get("KEELWRIGHT",
    os.path.expanduser("~/.keelwright/skills/keelwright")))

SKIP_PUBLIC = {"internal", "backups", ".git", "__pycache__", ".pytest_cache"}
SKIP_ALL = {".git", "__pycache__", ".pytest_cache"}
MANIFEST_ENTRIES = []


def rel(root: Path, f: Path):
    return str(f.relative_to(root)).replace("\\", "/")


def add_to_zip(zf: zipfile.ZipFile, base: Path, pattern: str = "*",
               skip_dirs: set = None, max_bytes: int = 10 * 1024 * 1024):
    """Walk base/pattern, skip dirs in skip_dirs, add files to zf. Skip files > max_bytes."""
    if skip_dirs is None:
        skip_dirs = set()
    added = 0
    for f in sorted(base.rglob(pattern)):
        if not f.is_file():
            continue
        if f.is_symlink():
            continue
        rel_parts = f.relative_to(base).parts
        if any(part in skip_dirs for part in rel_parts):
            continue
        size = f.stat().st_size
        if size > max_bytes:
            print(f"  [SKIP] {rel(base, f)} ({size//1024}KB > {max_bytes//1024}KB limit)")
            continue
        arcname = rel(base, f)
        zf.write(f, arcname)
        data = f.read_bytes()
        MANIFEST_ENTRIES.append({
            "path": arcname, "size": size, "sha256": hashlib.sha256(data).hexdigest()
        })
        added += 1
    return added


def export(out_path: Path, include_internal: bool, include_runs: bool = False):
    skip = SKIP_ALL if include_internal else SKIP_PUBLIC
    total = 0

    print(f"Skill source: {SKILL}")
    if not SKILL.exists():
        print(f"[ERROR] Skill not found at {SKILL}"); return 1

    out_path.parent.mkdir(parents=True, exist_ok=True)

    with zipfile.ZipFile(out_path, "w", zipfile.ZIP_DEFLATED) as zf:
        # 1. Skill files
        print("\n--- Skill files ---")
        total += add_to_zip(zf, SKILL, skip_dirs=skip)

        # 2. QA results (always included — public)
        qa = SKILL / "qa-results"
        if qa.exists():
            print(f"\n--- QA results ---")
            total += add_to_zip(zf, qa.parent, skip_dirs=skip)

        # 3. External QA run dirs (kw-qa/) — OPT-IN via --include-runs.
        #    These live OUTSIDE the skill tree and hold raw run history: local absolute paths,
        #    prompts, model outputs, machine names. Bundling them by default meant a zip handed
        #    to someone else silently carried the author's environment. Now you ask for them.
        qa_inside_skill = (SKILL / "qa-results").exists()
        kwqa = SKILL.parent.parent / "kw-qa"  # ~/kw-qa/
        if not include_runs:
            print(f"\n--- External QA runs (kw-qa/): SKIPPED ---")
            print(f"  They can contain local paths and raw prompts. Use --include-runs to add them.")
        elif kwqa.exists() and kwqa != SKILL and not qa_inside_skill:
            print(f"\n--- External QA runs (kw-qa/) — INCLUDED at your request ---")
            print(f"  WARNING: raw run data may embed local paths/prompts. Review before sharing.")
            for run in sorted(kwqa.iterdir()):
                if not run.is_dir():
                    continue
                rj = run / "results.jsonl"
                if rj.exists():
                    total += add_to_zip(zf, run, skip_dirs={"__pycache__", "node_modules"})
                    print(f"  included: {run.name}")
        elif qa_inside_skill:
            print(f"\n--- QA runs already inside skill/qa-results/ (skipping external scan) ---")

        # 4. Context transfer prompt — also gated: it comes from kw-qa/ and can carry
        #    session-specific context the recipient should not silently inherit.
        ct = kwqa / "CONTEXT-TRANSFER-PROMPT.md" if (include_runs and kwqa.exists()) else None
        if ct and ct.exists():
            zf.write(ct, "_CONTEXT-TRANSFER-PROMPT.md")
            total += 1

        # 5. Manifest (sha256 of every file — tamper detection on import)
        import json as _json
        # NOTE: do NOT embed the absolute local skill_path — it leaks the exporter's
        # home directory / username when the ZIP is shared. Use a relative marker only.
        zf.writestr("_MANIFEST.json", _json.dumps({
            "exported": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "skill_name": SKILL.name if hasattr(SKILL, "name") else str(SKILL).split("/")[-1],
            "files": len(MANIFEST_ENTRIES),
            "total_bytes": sum(e["size"] for e in MANIFEST_ENTRIES),
            "entries": MANIFEST_ENTRIES,
        }, indent=2))
        total += 1

    size = out_path.stat().st_size
    print(f"\n=== EXPORTED ===")
    print(f"  {out_path}")
    print(f"  {total} files, {size:,} bytes ({size//1024}KB)")
    return 0


def main():
    parser = argparse.ArgumentParser(description="Export keelwright skill to portable .zip")
    parser.add_argument("-o", "--output", help="Output .zip path")
    parser.add_argument("--all", action="store_true", help="Include internal/ and backups/")
    parser.add_argument("--include-runs", action="store_true",
                        help="Also bundle external ~/kw-qa/ run dirs and the context-transfer "
                             "prompt. WARNING: raw run data can embed local absolute paths, "
                             "prompts and model output — review before sharing the zip.")
    args = parser.parse_args()

    if args.output:
        out = Path(args.output)
    else:
        ts = time.strftime("%Y%m%dT%H%M%SZ", time.gmtime())
        out = Path(os.path.expanduser("~/kw-qa")) / f"keelwright-export-{ts}.zip"

    return export(out, args.all, args.include_runs)


if __name__ == "__main__":
    exit(main())
