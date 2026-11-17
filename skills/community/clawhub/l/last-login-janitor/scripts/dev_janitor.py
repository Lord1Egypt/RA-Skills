#!/usr/bin/env python3
"""dev_janitor.py — decision-safe developer-disk cleanup scanner.

Finds space-consuming dev artifacts (git repos, venvs, node_modules, caches,
build dirs, Docker data), dates each by its TRUTH signal (last commit for
repos, atime/mtime for venvs/caches, container usage for images), classifies
STALE vs PROTECTED with reasons, and emits a size-ranked report plus a
reviewable cleanup manifest. READ-ONLY: never deletes anything.

Pure stdlib (docker section shells out to `docker` if available).
"""
import argparse
import json
import os
import shlex
import shutil
import subprocess
import sys
import time
from dataclasses import dataclass, field, asdict
from pathlib import Path

GB = 1024 ** 3
MB = 1024 ** 2

RESTORE_CLASSES = {
    "repo": "B (re-clone)", "venv": "B (reinstall from lockfile)",
    "node_modules": "A (npm ci)", "build_dir": "A (rebuild)",
    "cache": "A (repopulate)", "docker_image": "C (re-pull)",
    "docker_volume": "E (data!)", "docker_cache": "A (rebuild layers)",
}


def human(n):
    if n >= GB:
        return f"{n / GB:.1f}G"
    if n >= MB:
        return f"{n / MB:.0f}M"
    return f"{n / 1024:.0f}K"


@dataclass
class Artifact:
    kind: str
    path: str
    size: int
    last_use_ts: float          # best-effort truth signal
    stale: bool
    protected: bool
    reason: str
    restore: str
    meta: dict = field(default_factory=dict)


def du(path):
    try:
        total = 0
        for dirpath, _dirnames, filenames in os.walk(path, onerror=lambda e: None):
            for f in filenames:
                try:
                    total += os.lstat(os.path.join(dirpath, f)).st_size
                except OSError:
                    pass
        return total
    except OSError:
        return 0


def newest_mtime(path, limit_secs=30):
    """mtime of the newest file (bounded walk)."""
    newest = 0.0
    start = time.time()
    for dirpath, _dn, filenames in os.walk(path, onerror=lambda e: None):
        if time.time() - start > limit_secs:
            break
        for f in filenames:
            try:
                m = os.lstat(os.path.join(dirpath, f)).st_mtime
                if m > newest:
                    newest = m
            except OSError:
                pass
    return newest


def git_last_commit(repo):
    try:
        out = subprocess.run(
            ["git", "-C", str(repo), "log", "-1", "--format=%ct"],
            capture_output=True, text=True, timeout=10)
        if out.returncode == 0 and out.stdout.strip():
            return float(out.stdout.strip())
    except Exception:
        pass
    return 0.0


def git_state(repo):
    """(dirty, n_stashes, unpushed_branches, has_remote)"""
    def git(*args):
        try:
            r = subprocess.run(["git", "-C", str(repo), *args],
                               capture_output=True, text=True, timeout=10)
            return r.stdout if r.returncode == 0 else ""
        except Exception:
            return ""
    status = git("status", "--porcelain")
    dirty = bool(status.strip())
    stashes = git("stash", "list").count("\n") if git("stash", "list") else 0
    remote = bool(git("remote").strip())
    unpushed = []
    if remote:
        # branches whose upstream is ahead or missing track info
        refs = git("for-each-ref", "--format=%(refname:short)",
                   "refs/heads").split()
        branches_with_commits = git(
            "for-each-ref", "--format=%(refname:short) %(upstream:track)",
            "refs/heads")
        for line in branches_with_commits.splitlines():
            parts = line.split(None, 1)
            if not parts:
                continue
            b = parts[0]
            track = parts[1] if len(parts) > 1 else ""
            if "ahead" in track:
                unpushed.append(b)
            elif track == "" or track == "[no upstream]":
                # local branch with no upstream: count commits not on any remote
                cnt = git("rev-list", "--count",
                          f"origin/main..{b}" if git("rev-parse", "--verify",
                                                    "origin/main") else
                          f"origin/master..{b}" if git("rev-parse", "--verify",
                                                       "origin/master") else "")
                try:
                    if cnt and int(cnt.strip()) > 0:
                        unpushed.append(b)
                except ValueError:
                    pass
    return dirty, stashes, unpushed, remote


def scan_repos(root, stale_ts, artifacts, progress):
    for dirpath, dirnames, _ in os.walk(root, onerror=lambda e: None):
        if ".git" in dirnames:
            repo = Path(dirpath)
            dirnames[:] = []            # don't descend into repo contents
            size = du(repo)
            commit_ts = git_last_commit(repo)
            dirty, stashes, unpushed, remote = git_state(repo)
            protected = False
            reasons = []
            if commit_ts == 0.0:
                reasons.append("no commits / not a readable repo")
                protected = True
            if dirty:
                reasons.append("dirty worktree")
                protected = True
            if stashes:
                reasons.append(f"{stashes} stash(es)")
                protected = True
            if unpushed:
                reasons.append("unpushed: " + ",".join(unpushed[:3]))
                protected = True
            if not remote and not protected and commit_ts > 0:
                # local-only repo: commits could exist nowhere else
                n = subprocess.run(["git", "-C", str(repo), "rev-list",
                                    "--count", "HEAD"], capture_output=True,
                                   text=True)
                try:
                    if int(n.stdout.strip()) > 0 and commit_ts < stale_ts:
                        reasons.append("no remote - archive before delete")
                        protected = True
                except ValueError:
                    pass
            stale = (not protected) and commit_ts < stale_ts
            if not protected and not stale and commit_ts >= stale_ts:
                reasons.append(f"active (last commit "
                               f"{time.strftime('%Y-%m-%d', time.localtime(commit_ts))})")
            artifacts.append(Artifact(
                "repo", str(repo), size, commit_ts, stale, protected,
                "; ".join(reasons) or "clean+pushed",
                RESTORE_CLASSES["repo"],
                {"dirty": dirty, "stashes": stashes,
                 "unpushed": unpushed, "remote": remote}))
            progress(repo)
            continue
        dirnames[:] = [d for d in dirnames if d not in
                       (".git", "node_modules", ".venv", "venv")]


def scan_venvs(root, stale_ts, artifacts, progress, kind="venv",
               markers=("pyvenv.cfg",)):
    for dirpath, dirnames, _ in os.walk(root, onerror=lambda e: None):
        hit = None
        for m in markers:
            if m in dirnames or (dirpath == root and False):
                pass
        # venv detection: dir contains pyvenv.cfg
        for d in list(dirnames):
            if (Path(dirpath) / d / markers[0]).exists():
                hit = Path(dirpath) / d
                dirnames.remove(d)
        if hit is None:
            # also root itself
            if (Path(dirpath) / markers[0]).exists():
                hit = Path(dirpath)
                dirnames[:] = []
        if hit is not None:
            size = du(hit)
            ts = max(os.path.getmtime(hit), newest_mtime(hit, 20))
            stale = ts < stale_ts
            parent_newer = False
            for parent in hit.parents:
                if parent in (Path(root), parent.parent):
                    break
                try:
                    if any((parent / f).exists() for f in
                           ("requirements.txt", "pyproject.toml")):
                        if parent.stat().st_mtime > ts:
                            parent_newer = True
                        break
                except OSError:
                    break
            reason = ("project files newer than venv"
                      if parent_newer else "orphaned or idle")
            protected = parent_newer and not stale
            artifacts.append(Artifact(kind, str(hit), size, ts, stale,
                                      protected, reason,
                                      RESTORE_CLASSES[kind]))
            progress(hit)


def scan_named_dirs(root, names, stale_ts, artifacts, kind, progress,
                    protect_sibling=None, sibling_grace_days=0):
    grace_ts = stale_ts - sibling_grace_days * 86400
    for dirpath, dirnames, _ in os.walk(root, onerror=lambda e: None):
        for d in list(dirnames):
            if d in names:
                target = Path(dirpath) / d
                dirnames.remove(d)
                size = du(target)
                ts = newest_mtime(target, 20)
                stale = ts < stale_ts
                reason = "stale" if stale else "recently touched"
                protected = not stale
                if protect_sibling:
                    sib = Path(dirpath) / protect_sibling
                    if sib.exists() and sib.stat().st_mtime > grace_ts:
                        protected = True
                        reason = f"sibling {protect_sibling} active"
                artifacts.append(Artifact(kind, str(target), size, ts,
                                          stale, protected, reason,
                                          RESTORE_CLASSES.get(kind, "B")))
                progress(target)
        dirnames[:] = [d for d in dirnames if not d.startswith(".git")
                       and d not in names]


def scan_caches(home, stale_ts, artifacts, progress):
    cache_roots = [
        (Path(home) / ".cache/pip", "cache"),
        (Path(home) / ".cache/uv", "cache"),
        (Path(home) / ".cache/npm", "cache"),
        (Path(home) / ".npm/_cacache", "cache"),
        (Path(home) / ".cache/go-build", "cache"),
        (Path(home) / ".gradle/caches", "cache"),
        (Path(home) / ".cache/huggingface", "cache"),
        (Path(home) / ".cache/torch", "cache"),
    ]
    for p, kind in cache_roots:
        if p.exists():
            size = du(p)
            ts = p.stat().st_mtime
            stale = ts < stale_ts and size > 0
            protected = not stale
            reason = ("cache warm (recent)" if protected else
                      "cache cold")
            artifacts.append(Artifact(kind, str(p), size, ts, stale,
                                      protected, reason,
                                      RESTORE_CLASSES[kind]))
            progress(p)


def scan_docker(stale_ts, artifacts, progress):
    def dock(*args):
        r = subprocess.run(["docker", *args], capture_output=True, text=True,
                           timeout=60)
        if r.returncode != 0:
            raise RuntimeError(r.stderr.strip())
        return r.stdout
    try:
        used_images = set()
        container_lines = dock("ps", "-a", "--format",
                               "{{.Image}}|{{.Status}}|{{.RunningFor}}").splitlines()
        running_status = {}
        for line in container_lines:
            img, status, runningfor = (line.split("|") + ["", ""])[:3]
            used_images.add(img.split(":")[0])
            running_status[img.split(":")[0]] = "Up" in status
        images = dock("images", "--format",
                      "{{.Repository}}|{{.Tag}}|{{.Size}}|{{.CreatedSince}}")
        for line in images.splitlines():
            repo, tag, size_s, since = line.split("|")
            if repo == "<none>":
                # dangling layer blob
                size = 0
            else:
                size = parse_size(size_s)
            key = repo
            protected = key in used_images
            reason = (f"used by container" if protected else
                      "no container references it")
            artifacts.append(Artifact(
                "docker_image", f"{repo}:{tag}", size, time.time(),
                not protected, protected, reason,
                RESTORE_CLASSES["docker_image"]))
        progress("docker:images")
    except (FileNotFoundError, RuntimeError, subprocess.TimeoutExpired) as e:
        print(f"[docker] unavailable: {e}", file=sys.stderr)
    try:
        vols = subprocess.run(
            ["docker", "volume", "ls", "-q"], capture_output=True, text=True,
            timeout=60).stdout.split()
        in_use = set()
        try:
            out = subprocess.run(
                ["docker", "ps", "-a", "--format", "{{.Mounts}}"],
                capture_output=True, text=True, timeout=60).stdout
            in_use = {v.strip() for line in out.splitlines()
                      for v in line.split(",")}
        except Exception:
            pass
        for v in vols:
            protected = v in in_use
            artifacts.append(Artifact(
                "docker_volume", v, 0, time.time(), not protected, protected,
                "attached" if protected else "dangling (may hold DATA)",
                RESTORE_CLASSES["docker_volume"]))
        progress("docker:volumes")
    except Exception:
        pass


def parse_size(s):
    s = s.strip().upper()
    mult = 1
    for suf, m in (("GB", GB), ("MB", MB), ("KB", 1024), ("B", 1)):
        if s.endswith(suf):
            mult = m
            s = s[: -len(suf)].strip()
            break
    try:
        return int(float(s) * mult)
    except ValueError:
        return 0


def report(artifacts, home, manifest_path=None):
    by_kind = {}
    for a in artifacts:
        by_kind.setdefault(a.kind, [0, 0])
        by_kind[a.kind][0] += a.size
        by_kind[a.kind][1] += 1
    print("=" * 74)
    print("DEV DISK AUDIT — sizing by artifact type")
    print("=" * 74)
    for k, (sz, n) in sorted(by_kind.items(), key=lambda kv: -kv[1][0]):
        print(f"  {k:<15} {human(sz):>8}  ({n} items)")
    total = sum(v[0] for v in by_kind.values())
    print(f"  {'TOTAL':<15} {human(total):>8}")

    stale = sorted([a for a in artifacts if a.stale and not a.protected],
                   key=lambda a: -a.size)
    protected = [a for a in artifacts if a.protected]
    print("\n" + "=" * 74)
    print(f"STALE CANDIDATES (review top-down; {len(stale)} items, "
          f"{human(sum(a.size for a in stale))} reclaimable)")
    print("=" * 74)
    for a in stale[:25]:
        when = time.strftime("%Y-%m-%d", time.localtime(a.last_use_ts)) \
            if a.last_use_ts else "?"
        print(f"  {human(a.size):>8}  {when}  [{a.kind}] {a.path}")
        print(f"            reason: {a.reason} | restore: {a.restore}")
    if len(stale) > 25:
        print(f"  ... +{len(stale)-25} more (see manifest)")

    print("\n" + "=" * 74)
    print(f"PROTECTED ({len(protected)} items) — do NOT delete on autopilot")
    print("=" * 74)
    for a in sorted(protected, key=lambda a: -a.size)[:15]:
        print(f"  {human(a.size):>8}  [{a.kind}] {a.path}")
        print(f"            {a.reason}")

    # conservative cleanup commands, human-reviewed; every generated
    # command shell-quotes paths (paths with spaces/must not execute)
    print("\n" + "=" * 74)
    print("SUGGESTED COMMANDS — review each line before running")
    print("=" * 74)
    cmds = []
    for a in stale:
        q = shlex.quote(a.path)      # safe against spaces & injection
        if a.kind == "cache":
            cmds.append(f"# cache (rebuildable): {a.path}\nrm -rf -- {q}")
        elif a.kind == "node_modules":
            cmds.append(f"# node_modules (npm ci restores): {a.path}\n"
                        f"rm -rf -- {q}")
        elif a.kind == "build_dir":
            cmds.append(f"# build dir: {a.path}\nrm -rf -- {q}")
        elif a.kind == "venv":
            cmds.append(f"# venv — check systemd/cron refs first!\n"
                        f"# rm -rf -- {q}")
        elif a.kind == "repo":
            cmds.append(f"# repo — confirm pushed, record URL, then:\n"
                        f"# rm -rf -- {q}")
        elif a.kind == "docker_image":
            cmds.append(f"# image unused by any container:\n"
                        f"# docker rmi {shlex.quote(a.path)}")
    for c in cmds[:20]:
        print(c)
    print(f"  (manifest has all {len(cmds)})")

    if manifest_path:
        payload = {
            "home": str(home),
            "generated": time.strftime("%Y-%m-%dT%H:%M:%S"),
            "sizing": {k: {"bytes": v[0], "items": v[1]}
                       for k, v in by_kind.items()},
            "stale": [asdict(a) for a in stale],
            "protected": [asdict(a) for a in protected],
            "commands": cmds,
        }
        Path(manifest_path).write_text(json.dumps(payload, indent=2))
        print(f"\nmanifest written: {manifest_path}")


def main():
    ap = argparse.ArgumentParser(
        description="Decision-safe dev-disk cleanup scanner (READ-ONLY)")
    ap.add_argument("roots", nargs="+",
                    help='dirs to scan (optionally preceded by the word "scan")')
    ap.add_argument("--stale-days", type=int, default=180,
                    help="staleness threshold in days (default 180)")
    ap.add_argument("--docker", action="store_true",
                    help="include docker images/volumes")
    ap.add_argument("--manifest", default=None,
                    help="write JSON manifest to this path")
    ap.add_argument("--quiet", action="store_true")
    args = ap.parse_args()

    roots = [r for r in args.roots if r != "scan"]
    stale_ts = time.time() - args.stale_days * 86400
    artifacts = []
    seen = [0]

    def progress(p):
        seen[0] += 1
        if not args.quiet:
            print(f"\r  scanned {seen[0]:>4} artifacts", end="",
                  file=sys.stderr)
    home = os.path.expanduser("~")
    for root in roots:
        root = os.path.expanduser(root)
        if not os.path.isdir(root):
            print(f"[!] not a dir: {root}", file=sys.stderr)
            continue
        scan_repos(root, stale_ts, artifacts, progress)
        scan_venvs(root, stale_ts, artifacts, progress)
        scan_named_dirs(root, {"node_modules"}, stale_ts, artifacts,
                        "node_modules", progress, protect_sibling="package.json",
                        sibling_grace_days=180)
        scan_named_dirs(root, {"dist", "build", "target", ".next", "out"},
                        stale_ts, artifacts, "build_dir", progress)
    # home-level caches: once, regardless of how many roots were scanned
    scan_caches(home, stale_ts, artifacts, progress)
    if args.docker:
        scan_docker(stale_ts, artifacts, progress)
    if not args.quiet:
        print("", file=sys.stderr)
    report(artifacts, os.path.expanduser("~"), args.manifest)
    return 0


if __name__ == "__main__":
    sys.exit(main())
