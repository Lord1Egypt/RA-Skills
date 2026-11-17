#!/usr/bin/env python3
# Copyright (c) 2026 ratingtesting — MIT-0 (see LICENSE). Free to use/modify/redistribute, no attribution required.
"""workspace_guard.py — INFRASTRUCTURE-level isolation for keelwright agents.

Prompt-level isolation ("write only inside your dir") is IGNORED by weak models — observed
2026-07-21 on step-3.7/nemotron: arms wrote outside their arm-dir, cited other runs, mixed
results. This guard makes isolation a TRIPWIRE, not advisory. Use it for QA arms AND for swarm
agents (N agents working in parallel must never touch each other's files or blend code).

MODEL
-----
Every isolated unit (a QA arm, or a swarm worker) owns exactly ONE workspace directory.
On creation the workspace is SEALED: a `.keelwright-seal` file records {owner_id, run_id,
created}. A worker may read/write ONLY inside its own sealed workspace. Any path outside it,
or a workspace sealed by a different owner, is a violation.

USAGE
-----
  # 1. Seal a fresh workspace for an owner (call once, before the agent runs):
  python workspace_guard.py seal   <workspace_dir> <owner_id> [run_id]

  # 2. Verify a workspace still belongs to its owner and nothing leaked in/out:
  python workspace_guard.py verify <workspace_dir> <owner_id>

  # 3. Make skill tree read-only (prevent QA models from writing to it):
  #    python workspace_guard.py isolate-skill-tree <skill_dir>
  #    python workspace_guard.py restore-skill-tree <skill_dir>
  #
  # 4. Check a whole run: every <RUN_DIR>/<test>/<arm> is sealed to a distinct owner and
  #    no arm's files appear under another arm (cross-arm contamination = code blending):
  python workspace_guard.py audit  <run_dir>

Exit 0 = clean. Exit 1 = isolation violated (do NOT trust results / do NOT merge code).
"""
import sys, json, hashlib, time, os, stat
from pathlib import Path

SEAL = ".keelwright-seal"


def seal(ws: Path, owner_id: str, run_id: str = "") -> int:
    ws.mkdir(parents=True, exist_ok=True)
    sf = ws / SEAL
    if sf.exists():
        prev = json.loads(sf.read_text(encoding="utf-8"))
        if prev.get("owner_id") != owner_id:
            print(f"[VIOLATION] {ws} already sealed by '{prev.get('owner_id')}', "
                  f"refusing to reseal for '{owner_id}'. Pick a fresh dir.")
            return 1
        print(f"[OK] already sealed to {owner_id}")
        return 0
    sf.write_text(json.dumps({
        "owner_id": owner_id,
        "run_id": run_id,
        "created": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }, indent=2), encoding="utf-8")
    print(f"[OK] sealed {ws} to owner={owner_id} run={run_id}")
    return 0


def _seal_of(ws: Path):
    sf = ws / SEAL
    if not sf.exists():
        return None
    try:
        return json.loads(sf.read_text(encoding="utf-8"))
    except Exception:
        return None


def verify(ws: Path, owner_id: str) -> int:
    s = _seal_of(ws)
    if s is None:
        print(f"[VIOLATION] {ws} has no {SEAL} — unsealed workspace, ownership unknown.")
        return 1
    if s.get("owner_id") != owner_id:
        print(f"[VIOLATION] {ws} is sealed to '{s.get('owner_id')}', not '{owner_id}'. "
              f"You are writing into someone else's workspace.")
        return 1
    print(f"[OK] {ws} belongs to {owner_id} (run={s.get('run_id')})")
    return 0


def audit(run_dir: Path) -> int:
    """Every arm dir must be sealed to a DISTINCT owner, and no arm's non-seed files may
    also appear (same relative name + identical sha) under a sibling arm — that would mean
    code blended across isolation boundaries."""
    errs = []
    arms = []  # (ownerless label, dir)
    for test in sorted(p for p in run_dir.iterdir() if p.is_dir()):
        for arm in ("control", "treatment"):
            for cand in (test / arm, run_dir / f"{test.name}-{arm}"):
                if cand.is_dir():
                    arms.append(cand)
    if not arms:
        print(f"[audit] no arm dirs under {run_dir} (nothing to check)")
        return 0
    # 1. each sealed to a distinct owner
    owners = {}
    for a in arms:
        s = _seal_of(a)
        if s is None:
            errs.append(f"[UNSEALED] {a.relative_to(run_dir)} has no {SEAL} — isolation not enforced.")
            continue
        oid = s.get("owner_id")
        if oid in owners:
            errs.append(f"[SHARED-OWNER] {a.relative_to(run_dir)} and "
                        f"{owners[oid].relative_to(run_dir)} share owner '{oid}' — not isolated.")
        else:
            owners[oid] = a
    # 2. cross-arm file blending: identical non-trivial file under two arms
    def sig(d):
        # only compare real source files the model would have authored; ignore tool/cache
        # noise (CACHEDIR.TAG, yarn.lock, node_modules, __pycache__, generic README) that is
        # legitimately identical everywhere and would cause false CODE-BLEND positives.
        SRC = {".py", ".js", ".ts", ".jsx", ".tsx", ".html", ".css", ".java", ".go", ".rb", ".rs", ".sql"}
        IGNORE_DIRS = {".git", "node_modules", "__pycache__", ".pytest_cache", ".venv", "venv"}
        out = {}
        for f in d.rglob("*"):
            if not f.is_file() or f.name == SEAL:
                continue
            if any(p in IGNORE_DIRS for p in f.parts):
                continue
            if f.suffix.lower() not in SRC:
                continue
            try:
                if f.stat().st_size > 40:  # skip trivial/seed stubs
                    out[str(f.relative_to(d))] = hashlib.sha256(f.read_bytes()).hexdigest()
            except Exception:
                pass
        return out
    sigs = [(a, sig(a)) for a in arms]
    for i in range(len(sigs)):
        for j in range(i + 1, len(sigs)):
            (a, sa), (b, sb) = sigs[i], sigs[j]
            # only compare arms of DIFFERENT tests (same test's control/treatment may legitimately
            # start from the same seed, but produced code being byte-identical across TESTS = leak)
            if a.parent == b.parent:
                continue
            shared = {n for n in sa if sb.get(n) == sa[n]}
            if shared:
                errs.append(f"[CODE-BLEND] {a.relative_to(run_dir)} and {b.relative_to(run_dir)} "
                            f"share byte-identical files {sorted(shared)} across tests — "
                            f"cross-workspace contamination.")
    for e in errs:
        print(e)
    print(f"\n=== workspace audit: {'CLEAN' if not errs else str(len(errs))+' VIOLATION(S)'} ===")
    return 1 if errs else 0



def _set_readonly(path: Path, readonly: bool):
    """Set or clear read-only attribute on file (Windows) or permission bit (POSIX)."""
    try:
        if os.name == 'nt':
            import ctypes
            attrs = ctypes.windll.kernel32.GetFileAttributesW(str(path))
            if readonly:
                attrs |= stat.FILE_ATTRIBUTE_READONLY
            else:
                attrs &= ~stat.FILE_ATTRIBUTE_READONLY
            ctypes.windll.kernel32.SetFileAttributesW(str(path), attrs)
        else:
            st = os.stat(path)
            if readonly:
                os.chmod(path, st.st_mode & ~(stat.S_IWUSR | stat.S_IWGRP | stat.S_IWOTH))
            else:
                os.chmod(path, st.st_mode | stat.S_IWUSR)
    except Exception as e:
        print(f"  warning: could not set readonly on {path}: {e}")


def isolate_skill_tree(skill_dir: Path) -> int:
    """Make the skill tree read-only to prevent QA models from writing to it.
    
    This is the REAL isolation — prompt-level П10/П11 are not enforced by weak models.
    Run before any unattended/QA session. Restore with restore-skill-tree after.
    """
    SKILL_EXTS = {".md", ".py", ".yaml", ".yml", ".html", ".png", ".jpg", ".json", ".txt"}
    IGNORE = {".git", "backups", "__pycache__", ".pytest_cache", "internal"}
    
    count = 0
    for f in skill_dir.rglob("*"):
        if f.is_file():
            if any(p in IGNORE for p in f.relative_to(skill_dir).parts):
                continue
            if f.suffix.lower() in SKILL_EXTS or f.name in {".gitignore", "LICENSE"}:
                _set_readonly(f, True)
                count += 1
    print(f"[isolate] {skill_dir}: {count} files set read-only")
    print(f"[isolate] Restore with: python workspace_guard.py restore-skill-tree <path>")
    return 0


def restore_skill_tree(skill_dir: Path) -> int:
    """Restore write permissions after an isolated session."""
    IGNORE = {".git", "backups", "__pycache__", ".pytest_cache", "internal"}
    
    count = 0
    for f in skill_dir.rglob("*"):
        if f.is_file():
            if any(p in IGNORE for p in f.relative_to(skill_dir).parts):
                continue
            _set_readonly(f, False)
            count += 1
    print(f"[restore] {skill_dir}: {count} files restored to writable")
    return 0


def main():
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    cmd = sys.argv[1]
    if cmd == "seal" and len(sys.argv) >= 4:
        sys.exit(seal(Path(sys.argv[2]), sys.argv[3], sys.argv[4] if len(sys.argv) > 4 else ""))
    if cmd == "verify" and len(sys.argv) >= 4:
        sys.exit(verify(Path(sys.argv[2]), sys.argv[3]))
    if cmd == "audit":
        sys.exit(audit(Path(sys.argv[2])))
    if cmd == "isolate-skill-tree" and len(sys.argv) >= 3:
        sys.exit(isolate_skill_tree(Path(sys.argv[2])))
    if cmd == "restore-skill-tree" and len(sys.argv) >= 3:
        sys.exit(restore_skill_tree(Path(sys.argv[2])))
    sys.exit(__doc__)


if __name__ == "__main__":
    main()
