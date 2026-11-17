#!/usr/bin/env python3
"""Prune the InfinityContext archive and reclaim disk space.

Portable core: standard library only, no shell commands, no network access.

Safety rules (deny by default):
  * the archive directory must be a **verified InfinityContext archive**: it has
    to contain the owner-only marker file ``.infinity-context-archive`` whose
    JSON declares ``app=infinity-context`` and a supported marker version
  * protected directories (filesystem root, the user home and its common
    subdirectories, system directories) are always refused
  * only files whose **full name** matches an InfinityContext artifact pattern
    are considered - a bare extension allowlist is never used
  * enumeration is non-recursive; unexpected subdirectories are skipped
  * symbolic links are never followed or deleted
  * ``VACUUM`` runs only after a read-only schema check
    (``session_chunks`` + ``chunk_fts``)
  * nothing is removed unless BOTH ``--apply`` and ``--confirm-destructive``
    are given, and the validated scope is printed first
  * every candidate is re-checked with ``lstat`` immediately before ``unlink``

Usage:
    python cleanup.py --dry-run
    python cleanup.py --apply --confirm-destructive --days 30
    python cleanup.py --apply --confirm-destructive --archive-dir ~/.dsh/infinity-context/archive
    python cleanup.py --init-marker --archive-dir <dir>   # migrate an old archive
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sqlite3
import stat
import sys
import time
from pathlib import Path

# T09：归档目录所有权校验（同目录模块，随包分发）
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import secure_fs  # noqa: E402

DEFAULT_HOME = Path(os.environ.get("INFINITY_CONTEXT_HOME") or (Path.home() / ".infinity-context"))
DEFAULT_ARCHIVE = DEFAULT_HOME / "archive"

# 归档身份标记：由 session_to_sqlite.py 在归档目录首次加固后写入
MARKER_NAME = ".infinity-context-archive"
MARKER_APP = "infinity-context"
MARKER_VERSION = 1
SUPPORTED_MARKER_VERSIONS = (1,)

# 只有**完整文件名**匹配下列模式的产物才会被清理（绝不使用裸扩展名白名单）。
# 文件名格式与 session_to_sqlite.py 生成的 safe_key-stamp.db 一致。
ARTIFACT_PATTERNS = (
    re.compile(r"^[A-Za-z0-9_-]{1,128}-\d{8}-\d{6}\.db$"),
    re.compile(r"^[A-Za-z0-9_-]{1,128}-\d{8}-\d{6}\.db-(?:wal|shm)$"),
    re.compile(r"^[A-Za-z0-9_-]{1,128}-\d{8}-\d{6}\.jsonl(?:\.bak)?$"),
    re.compile(r"^[A-Za-z0-9_-]{1,128}-\d{8}-\d{6}\.bak$"),
)
DB_PATTERN = ARTIFACT_PATTERNS[0]


class CleanupRefused(RuntimeError):
    """The selected directory is not a verified InfinityContext archive."""


def resolve_archive(raw: str) -> Path:
    path = Path(raw).expanduser()
    if not path.is_absolute():
        raise SystemExit(f"SECURITY: archive path must be absolute: {path}")
    return path.resolve()


def is_inside(child: Path, parent: Path) -> bool:
    try:
        child.relative_to(parent)
        return True
    except ValueError:
        return False


def is_artifact(name: str) -> bool:
    return any(pattern.match(name) for pattern in ARTIFACT_PATTERNS)


# ---------------------------------------------------------------------------
# 归档身份标记
# ---------------------------------------------------------------------------

def marker_payload() -> dict:
    from datetime import datetime, timezone
    return {
        "app": MARKER_APP,
        "marker_version": MARKER_VERSION,
        "created_utc": datetime.now(timezone.utc).isoformat(),
    }


def write_marker(archive: Path) -> Path:
    """Atomically create the owner-only marker in an already secured archive."""
    marker = archive / MARKER_NAME
    flags = os.O_CREAT | os.O_EXCL | os.O_WRONLY | getattr(os, "O_NOFOLLOW", 0)
    try:
        fd = os.open(str(marker), flags, 0o600)
    except FileExistsError:
        return marker
    except OSError as exc:
        raise CleanupRefused(f"cannot create archive marker {marker}: {exc}") from exc
    with os.fdopen(fd, "w", encoding="utf-8") as handle:
        json.dump(marker_payload(), handle, indent=2)
        handle.write("\n")
    secure_fs.secure_file(marker)
    return marker


def read_marker(archive: Path) -> dict:
    """Return the marker payload or raise ``CleanupRefused``."""
    marker = archive / MARKER_NAME
    try:
        st = os.lstat(marker)
    except FileNotFoundError as exc:
        raise CleanupRefused(
            f"{archive} is not a verified InfinityContext archive "
            f"(missing {MARKER_NAME}). Refusing to delete anything. If this really is "
            f"an archive created by an older version, review it and run: "
            f"python cleanup.py --init-marker --archive-dir \"{archive}\""
        ) from exc
    except OSError as exc:
        raise CleanupRefused(f"cannot inspect archive marker {marker}: {exc}") from exc
    if stat.S_ISLNK(st.st_mode):
        raise CleanupRefused(f"archive marker is a symbolic link: {marker}")
    if not stat.S_ISREG(st.st_mode):
        raise CleanupRefused(f"archive marker is not a regular file: {marker}")
    getuid = getattr(os, "getuid", None)
    if getuid is not None and st.st_uid != getuid():
        raise CleanupRefused(f"archive marker is not owned by the current user: {marker}")
    try:
        with open(marker, "r", encoding="utf-8") as handle:
            data = json.load(handle)
    except (OSError, json.JSONDecodeError) as exc:
        raise CleanupRefused(f"archive marker is unreadable: {exc}") from exc
    if not isinstance(data, dict) or data.get("app") != MARKER_APP:
        raise CleanupRefused("archive marker app id mismatch")
    if data.get("marker_version") not in SUPPORTED_MARKER_VERSIONS:
        raise CleanupRefused(
            f"unsupported archive marker version: {data.get('marker_version')!r}")
    return data


def reject_protected(archive: Path) -> None:
    """Refuse broad system / user directories even if a marker is present."""
    home = Path.home().resolve()
    protected = {
        Path(archive.anchor),
        home,
        home / "Documents",
        home / "Desktop",
        home / "Downloads",
        home / "Pictures",
        home / "Videos",
        home / "Music",
        home / ".ssh",
        home / ".config",
    }
    if os.name == "nt":
        for name in ("USERPROFILE", "APPDATA", "LOCALAPPDATA", "ProgramData",
                     "SystemRoot", "WINDIR", "PUBLIC"):
            value = os.environ.get(name)
            if value:
                try:
                    protected.add(Path(value).resolve())
                except OSError:
                    pass
    else:
        protected.update({Path("/etc"), Path("/usr"), Path("/var"), Path("/bin"),
                          Path("/sbin"), Path("/lib"), Path("/opt"), Path("/tmp")})
    if archive in protected:
        raise CleanupRefused(f"refusing to operate on a protected directory: {archive}")


def is_infinity_database(db_path: Path) -> bool:
    """Read-only schema probe: only our own databases may be vacuumed."""
    try:
        conn = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)
    except sqlite3.Error:
        return False
    try:
        tables = {row[0] for row in conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table'")}
        return {"session_chunks", "chunk_fts"} <= tables
    except sqlite3.Error:
        return False
    finally:
        conn.close()


def vacuum(db_path: Path) -> bool:
    try:
        conn = sqlite3.connect(str(db_path))
        conn.execute("VACUUM")
        conn.close()
        return True
    except Exception as exc:  # noqa: BLE001 - report, never abort the run
        print(f"  VACUUM_SKIP {db_path.name}: {exc}", file=sys.stderr)
        return False


def init_marker(archive: Path) -> int:
    """Explicit, one-off migration for archives created before the marker existed."""
    if not archive.is_dir():
        print(f"SECURITY: not a directory: {archive}", file=sys.stderr)
        return 2
    try:
        secure_fs.assert_safe_directory(archive)
    except secure_fs.UnsafeArchiveError as exc:
        print(f"SECURITY: {exc}", file=sys.stderr)
        return 2
    try:
        reject_protected(archive)
    except CleanupRefused as exc:
        print(f"SECURITY: {exc}", file=sys.stderr)
        return 2

    # 只有在目录中确实存在一个本应用的数据库时才允许写入标记
    proof = None
    for entry in archive.iterdir():
        if entry.is_symlink() or not entry.is_file():
            continue
        if DB_PATTERN.match(entry.name) and is_infinity_database(entry):
            proof = entry
            break
    if proof is None:
        print("SECURITY: no InfinityContext database found in this directory; "
              "refusing to write the archive marker", file=sys.stderr)
        return 2

    marker = write_marker(archive)
    print(f"MARKER_WRITTEN {marker} (verified against {proof.name})")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Prune the InfinityContext archive")
    parser.add_argument("--archive-dir", default=str(DEFAULT_ARCHIVE),
                        help=f"archive directory (default: {DEFAULT_ARCHIVE})")
    parser.add_argument("--days", type=int, default=30,
                        help="retention in days, 1..3650 (default: 30)")
    parser.add_argument("--apply", action="store_true",
                        help="actually delete; without it the run is a dry-run")
    parser.add_argument("--confirm-destructive", action="store_true",
                        help="required together with --apply: acknowledges the validated "
                             "deletion scope printed in the summary")
    parser.add_argument("--init-marker", action="store_true",
                        help="explicit one-off migration: write the archive marker into an "
                             "existing archive after verifying one of our databases is present")
    args = parser.parse_args()

    if not 1 <= args.days <= 3650:
        raise SystemExit(f"SECURITY: --days must be 1..3650, got {args.days}")

    archive = resolve_archive(args.archive_dir)
    if not archive.is_dir():
        print(f"ARCHIVE_MISSING: {archive}")
        return 0

    if args.init_marker:
        return init_marker(archive)

    # T09：拒绝其它本地账号拥有的归档目录
    try:
        secure_fs.assert_safe_directory(archive)
    except secure_fs.UnsafeArchiveError as exc:
        print(f"SECURITY: {exc}", file=sys.stderr)
        return 2

    # T09：必须是被验证过的 InfinityContext 归档 + 非受保护目录
    try:
        marker = read_marker(archive)
        reject_protected(archive)
    except CleanupRefused as exc:
        print(f"SECURITY: {exc}", file=sys.stderr)
        return 3

    cutoff = time.time() - args.days * 86400
    candidates: list[tuple[Path, int]] = []
    skipped = 0

    # 非递归：归档根目录下的文件；意外子目录一律跳过并告警
    for entry in sorted(archive.iterdir()):
        if entry.is_dir() and not entry.is_symlink():
            print(f"  SECURITY_SKIP (unexpected subdirectory): {entry.name}")
            skipped += 1
            continue
        if entry.is_symlink() or not entry.is_file():
            skipped += 1
            continue
        if not is_inside(entry.resolve(), archive):
            print(f"  SECURITY_SKIP (escapes archive): {entry}")
            skipped += 1
            continue
        if entry.name == MARKER_NAME or not is_artifact(entry.name):
            skipped += 1
            continue
        try:
            st = entry.stat()
        except OSError:
            skipped += 1
            continue
        if st.st_mtime >= cutoff:
            continue
        candidates.append((entry, st.st_size))

    total_bytes = sum(size for _, size in candidates)

    print("=" * 64)
    print(f"ARCHIVE ROOT (canonical): {archive}")
    print(f"MARKER VALIDATED:         app={marker['app']} "
          f"version={marker['marker_version']}")
    print(f"RETENTION:                {args.days} days (cutoff {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(cutoff))})")
    print(f"FILES TO DELETE:          {len(candidates)}")
    print(f"BYTES TO RECLAIM:         {total_bytes:,}")
    print("=" * 64)
    for entry, size in candidates:
        print(f"  {'DELETE' if args.apply else 'WOULD DELETE'} {entry.name} ({size} bytes)")

    if not args.apply:
        print(f"CLEANUP DRY-RUN: candidates={len(candidates)} skipped={skipped} "
              f"reclaimed={total_bytes} archive={archive}")
        print("(nothing was deleted - re-run with --apply --confirm-destructive)")
        return 0

    if not args.confirm_destructive:
        print("SECURITY: --apply also requires --confirm-destructive "
              "after reviewing the validated scope above", file=sys.stderr)
        return 4

    deleted = 0
    reclaimed = 0
    for entry, size in candidates:
        # TOCTOU：删除前用 lstat 重新验证类型、位置与时间
        try:
            st = os.lstat(entry)
        except OSError:
            continue
        if stat.S_ISLNK(st.st_mode) or not stat.S_ISREG(st.st_mode):
            print(f"  SECURITY_SKIP (type changed since scan): {entry.name}")
            continue
        if st.st_mtime >= cutoff or not is_artifact(entry.name):
            continue
        try:
            entry.unlink()
        except OSError as exc:
            print(f"  DELETE_FAIL {entry.name}: {exc}", file=sys.stderr)
            continue
        deleted += 1
        reclaimed += size

    vacuumed = 0
    for db in sorted(archive.iterdir()):
        if db.is_symlink() or not db.is_file():
            continue
        if not DB_PATTERN.match(db.name):
            continue
        if not is_infinity_database(db):
            print(f"  VACUUM_SKIP (not an InfinityContext database): {db.name}")
            continue
        if vacuum(db):
            vacuumed += 1

    print(f"CLEANUP APPLIED: deleted={deleted} skipped={skipped} "
          f"reclaimed={reclaimed} bytes vacuumed={vacuumed} archive={archive}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
