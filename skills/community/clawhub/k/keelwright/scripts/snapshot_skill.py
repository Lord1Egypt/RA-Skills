#!/usr/bin/env python3
# Copyright (c) 2026 ratingtesting — MIT-0 (see LICENSE). Free to use/modify/redistribute, no attribution required.
"""snapshot_skill.py — versioned backups + tamper detection for the keelwright skill.

WHY: a weak model editing the skill in another session truncated SKILL.md from ~500 lines to 86
(2026-07-21), silently destroying the map, glossary, and gates. There was no git and no backup,
so recovery meant scraping the session DB. This script makes that never-again cheap:

  * `snapshot`  — copy the whole skill tree into backups/<UTC>/ and refresh a manifest of
                  sha256 + line counts. Keeps the last N snapshots (default 10).
  * `verify`    — compare the live skill against the newest snapshot; flag any file that SHRANK
                  by more than a threshold (a truncation/corruption signal) or vanished.
  * `restore`   — copy a chosen snapshot (default: newest) back over the live skill.
              Dry run unless `--yes`. Files added since the snapshot are reported but
              KEPT unless `--prune` (a planted file is not in the snapshot, so a plain
              restore would leave it behind while looking clean).
              Usage: restore [snapshot-name] [--prune] [--yes]

It is stdlib-only and cross-platform. Run `snapshot` before and after any risky edit, and
`verify` on entry to catch out-of-band corruption early.

BACKUPS LIVE OUTSIDE THE skills/ DIRECTORY (important): snapshots are written to
`<hermes>/keelwright-backups/` — a sibling of `skills/`, NOT anywhere under `skills/`.
The skill loader scans ALL of `skills/` recursively and keys on the `name:` frontmatter, so
ANY `SKILL.md` under `skills/` (even in `skills/keelwright-backups/…`) registers a second skill
named `keelwright` and makes `skill_view(name='keelwright')` fail as ambiguous. Writing backups
one level above `skills/` keeps the name unambiguous and the published surface clean.

USAGE
  python snapshot_skill.py snapshot [keep=10]
  python snapshot_skill.py verify
  python snapshot_skill.py verify-additions
  python snapshot_skill.py restore [<snapshot_name>]
"""
import sys, shutil, hashlib, json, time
from pathlib import Path

SKILL = Path(__file__).resolve().parent.parent          # .../skills/keelwright
# Backups sit OUTSIDE skills/ (one level up) so nested SKILL.md copies never collide with the loader.
BACKUPS = SKILL.parent.parent / "keelwright-backups"    # .../hermes/keelwright-backups
IGNORE = {"backups", "keelwright-backups", ".git", "__pycache__", ".pytest_cache"}


def _walk():
    for f in SKILL.rglob("*"):
        if f.is_file() and not any(p in IGNORE for p in f.relative_to(SKILL).parts):
            yield f


def _manifest():
    m = {}
    for f in _walk():
        rel = str(f.relative_to(SKILL)).replace("\\", "/")
        data = f.read_bytes()
        m[rel] = {"sha256": hashlib.sha256(data).hexdigest(),
                  "lines": data.count(b"\n"), "bytes": len(data)}
    return m


def snapshot(keep=10):
    ts = time.strftime("%Y%m%dT%H%M%SZ", time.gmtime())
    dest = BACKUPS / ts
    for f in _walk():
        rel = f.relative_to(SKILL)
        (dest / rel).parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(f, dest / rel)
    (dest / "_manifest.json").write_text(json.dumps(_manifest(), indent=2), encoding="utf-8")
    print(f"[snapshot] {dest} — {len(list((dest).rglob('*')))} files")
    # prune old
    snaps = sorted([d for d in BACKUPS.iterdir() if d.is_dir()])
    for old in snaps[:-keep]:
        shutil.rmtree(old); print(f"[prune] {old.name}")
    return 0


def _newest():
    snaps = sorted([d for d in BACKUPS.iterdir() if d.is_dir()]) if BACKUPS.exists() else []
    return snaps[-1] if snaps else None


def verify(shrink_pct=30):
    snap = _newest()
    if not snap:
        print("[verify] no snapshot yet — run `snapshot` first."); return 1
    prev = json.loads((snap / "_manifest.json").read_text(encoding="utf-8"))
    cur = _manifest()
    problems = []
    for rel, old in prev.items():
        if rel == "_manifest.json":
            continue
        new = cur.get(rel)
        if new is None:
            problems.append(f"[MISSING] {rel} existed in {snap.name}, gone now.")
            continue
        if old["lines"] > 20 and new["lines"] < old["lines"] * (1 - shrink_pct / 100):
            problems.append(f"[SHRANK] {rel}: {old['lines']}→{new['lines']} lines "
                            f"(>{shrink_pct}% smaller) — possible truncation/corruption.")
    for p in problems:
        print(p)
    print(f"\n=== verify vs {snap.name}: {'CLEAN' if not problems else str(len(problems))+' ALERT(S)'} ===")
    return 1 if problems else 0


def verify_additions():
    """Detect foreign writes by comparing the live tree against git HEAD.
    
    snapshot verify only detects SHRINKAGE (truncation). A foreign agent that ADDS files
    or EDITS existing files without removing content passes verify silently. This command
    catches that by checking git diff against the last known-good commit.
    """
    import subprocess as _sp
    git_dir = SKILL / ".git"
    if not git_dir.exists():
        print("[verify-additions] no .git in skill dir — cannot detect foreign writes.")
        return 1
    r = _sp.run(["git", "-C", str(SKILL), "log", "--oneline", "-1"], capture_output=True, text=True)
    if r.returncode != 0:
        print("[verify-additions] git log failed"); return 1
    commit = r.stdout.strip().split()[0]
    r2 = _sp.run(["git", "-C", str(SKILL), "diff", "--name-only", "HEAD"], capture_output=True, text=True)
    changed = [l.strip() for l in r2.stdout.splitlines() if l.strip()]
    r3 = _sp.run(["git", "-C", str(SKILL), "ls-files", "--others", "--exclude-standard"], capture_output=True, text=True)
    new_files = [l.strip() for l in r3.stdout.splitlines() if l.strip()]
    EXPECTED = {"PROGRESS.md","phoenix-log.md","autoresearch-lessons.md",".loop_state",".loop_stopped"}
    new_files = [f for f in new_files if Path(f).name not in EXPECTED]
    problems = []
    for f in changed: problems.append(f"[MODIFIED] {f} — changed since {commit}")
    for f in new_files: problems.append(f"[UNTRACKED] {f} — new file (foreign write?)")
    for p in problems: print(p)
    if problems:
        print(f"\n=== verify-additions vs {commit}: {len(problems)} ALERT(S) ===")
    else:
        print(f"\n=== verify-additions vs {commit}: CLEAN ===")
    return 1 if problems else 0


def restore(name=None, prune=False, yes=False):
    """Copy a snapshot back over the live skill.

    IMPORTANT: by default this OVERWRITES files present in the snapshot but does NOT
    delete files added since it was taken. That matters for tamper recovery: a planted
    file is not in the snapshot, so a plain restore leaves it in place and the tree only
    looks clean. Extra files are therefore always reported, and `--prune` removes them
    for a true byte-for-byte rollback.
    """
    snap = (BACKUPS / name) if name else _newest()
    if not snap or not snap.is_dir():
        print(f"[restore] snapshot not found: {name}"); return 1

    snap_files = {f.relative_to(snap) for f in snap.rglob("*")
                  if f.is_file() and f.name != "_manifest.json"}
    live_files = {f.relative_to(SKILL) for f in SKILL.rglob("*")
                  if f.is_file() and not any(p in ("backups", ".git", "__pycache__")
                                             for p in f.relative_to(SKILL).parts)}
    extra = sorted(live_files - snap_files)

    print(f"[restore] snapshot: {snap.name}")
    print(f"[restore] will overwrite {len(snap_files)} file(s) in {SKILL}")
    if extra:
        print(f"[restore] {len(extra)} file(s) exist live but NOT in the snapshot:")
        for rel in extra[:20]:
            print(f"           + {rel}")
        if len(extra) > 20:
            print(f"           ... and {len(extra) - 20} more")
        print("[restore] these are NOT part of the snapshot. If you are recovering from")
        print("          tampering, treat them as suspect — a planted file would appear here.")
        if not prune:
            print("[restore] they will be LEFT IN PLACE. Use --prune to delete them.")

    if not yes:
        print("[restore] DRY RUN — nothing written. Re-run with --yes to apply.")
        return 0

    for rel in snap_files:
        dest = SKILL / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(snap / rel, dest)

    removed = 0
    if prune:
        for rel in extra:
            try:
                (SKILL / rel).unlink()
                removed += 1
            except OSError as e:
                print(f"[restore] could not remove {rel}: {e}")

    print(f"[restore] restored {len(snap_files)} file(s) from {snap.name}"
          + (f"; removed {removed} extra file(s)" if prune else
             (f"; {len(extra)} extra file(s) left in place" if extra else "")))
    return 0


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    cmd = sys.argv[1]
    if cmd == "snapshot":
        sys.exit(snapshot(int(sys.argv[2]) if len(sys.argv) > 2 else 10))
    if cmd == "verify":
        sys.exit(verify())
    if cmd == "verify-additions":
        sys.exit(verify_additions())
    if cmd == "restore":
        flags = {a for a in sys.argv[2:] if a.startswith("--")}
        positional = [a for a in sys.argv[2:] if not a.startswith("--")]
        sys.exit(restore(positional[0] if positional else None,
                         prune="--prune" in flags,
                         yes="--yes" in flags))
    sys.exit(__doc__)


if __name__ == "__main__":
    main()
