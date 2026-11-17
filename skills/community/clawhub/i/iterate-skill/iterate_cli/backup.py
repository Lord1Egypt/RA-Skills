"""Backup inspection and restore (``iterate backup``).

The CLI writes a timestamped copy of a file beside itself before every
mutation — ``config set``/``config unset`` (``*.configset-*`` /
``*.configunset-*``), ``doctor --fix`` (``*.doctorfix-*``), ``refresh`` /
``personalize`` / ``onboard`` (``*.refresh-*`` / ``*.personalize-*`` /
``*.onboard-*``), ``import`` (``*.import-*``) and ``reonboard``
(``*.bak-*``). Until now there was **no way to see or restore them**: a user
who needed to undo a bad ``config set`` had to ``ls`` the project directory
and guess which of the ``*.configset-*`` files was the pre-change copy, or
re-run the interactive wizard and hope.

This module closes that gap. ``iterate backup list`` enumerates every
recognisable backup in the project root (newest first, with the original
file, the operation that wrote it, and the UTC timestamp). ``iterate backup
restore FILE`` puts one back: the current file is itself backed up first
(tagged ``restore``) so a restore is reversible, then the backup content is
written to the original path. A restore never touches a file that does not
look like an iterate backup, never leaves the project root, and is refused
when the target is a directory.

The CLI layer (``iterate_cli/cli.py``) handles I/O, prompts and exit codes;
everything here is pure and unit-testable.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

from iterate_cli.generator import atomic_write, backup_file

#: Every tag the CLI uses when it copies a file aside before rewriting it,
#: plus the ``restore`` tag this module writes before overwriting a target so
#: a restore is itself reversible. Keeping the list here (rather than in the
#: regex literal) lets ``list`` label each backup with the operation that
#: created it.
BACKUP_TAGS: tuple[str, ...] = (
    "configset",
    "configunset",
    "doctorfix",
    "refresh",
    "personalize",
    "onboard",
    "import",
    "bak",
    "restore",
)

#: Human label for each tag, shown in the TUI listing. Unknown tags fall back
#: to the raw tag so a future tag added elsewhere still renders.
TAG_LABELS: dict[str, str] = {
    "configset": "config set",
    "configunset": "config unset",
    "doctorfix": "doctor --fix",
    "refresh": "refresh",
    "personalize": "personalize",
    "onboard": "onboard",
    "import": "import",
    "bak": "reonboard",
    "restore": "restore",
}

#: ``<base>.<tag>-<UTCstamp>-<salt>`` where tag is one of BACKUP_TAGS, stamp
#: is ``YYYYMMDDTHHMMSSZ`` and salt is 6 hex chars (``uuid4().hex[:6]``).
#: Anchored and greedy on the base so ``iterate.config.yaml.configset-…``
#: yields base ``iterate.config.yaml``, not ``iterate.config``.
_BACKUP_RE = re.compile(
    r"^(?P<base>.+)\.(?P<tag>configset|configunset|doctorfix|refresh|"
    r"personalize|onboard|import|bak|restore)-"
    r"(?P<stamp>\d{8}T\d{6}Z)-(?P<salt>[0-9a-f]{6})$"
)


class BackupError(Exception):
    """A backup could not be listed or restored.

    The message is user-facing and always states what to do next; the CLI
    prints it verbatim (to stdout as ``{"error": ...}`` under ``--json``).
    """


@dataclass(frozen=True)
class BackupEntry:
    """One recognisable backup file in the project root.

    Attributes:
        path: Absolute path of the backup file.
        base: The original file the backup was taken from (its filename).
        tag: The operation tag that created it (one of ``BACKUP_TAGS``).
        stamp: The ``YYYYMMDDTHHMMSSZ`` UTC timestamp component.
        size: Backup file size in bytes.
    """

    path: Path
    base: str
    tag: str
    stamp: str
    size: int

    @property
    def timestamp(self) -> datetime:
        """The backup's UTC timestamp, timezone-aware."""
        return datetime.strptime(self.stamp, "%Y%m%dT%H%M%SZ").replace(
            tzinfo=timezone.utc
        )

    @property
    def label(self) -> str:
        """Human-readable operation label for the TUI listing."""
        return TAG_LABELS.get(self.tag, self.tag)

    def to_dict(self) -> dict[str, Any]:
        """JSON-serialisable representation."""
        return {
            "path": str(self.path),
            "name": self.path.name,
            "base": self.base,
            "tag": self.tag,
            "operation": self.label,
            "timestamp": self.timestamp.isoformat(),
            "size": self.size,
        }


def _parse_backup_name(name: str) -> tuple[str, str, str] | None:
    """Split a backup filename into ``(base, tag, stamp)`` or None.

    Returns None when ``name`` is not a recognisable iterate backup, so callers
    can refuse to touch unrelated files.
    """
    match = _BACKUP_RE.match(name)
    if not match:
        return None
    return match.group("base"), match.group("tag"), match.group("stamp")


def list_backups(project_root: Path) -> list[BackupEntry]:
    """Return every recognisable backup file under ``project_root``.

    Newest first (by UTC timestamp, then by salt as a stable tie-break). A
    project with no backups returns an empty list — that is informational, not
    an error.
    """
    entries: list[BackupEntry] = []
    try:
        children = list(project_root.iterdir())
    except OSError as exc:
        raise BackupError(f"cannot read project directory {project_root}: {exc}") from exc
    for path in children:
        if not path.is_file():
            continue
        parsed = _parse_backup_name(path.name)
        if parsed is None:
            continue
        base, tag, stamp = parsed
        try:
            size = path.stat().st_size
        except OSError:
            continue  # raced away or unreadable; skip rather than fail the listing
        entries.append(BackupEntry(path=path, base=base, tag=tag, stamp=stamp, size=size))
    entries.sort(key=lambda e: (e.stamp, e.path.name), reverse=True)
    return entries


def restore_backup(
    project_root: Path,
    backup_arg: str,
    *,
    dry_run: bool = False,
) -> dict[str, Any]:
    """Restore one backup file to its original name.

    The backup is resolved against ``project_root`` and must be a recognisable
    iterate backup file (see :func:`_parse_backup_name`). Before the target is
    overwritten, the *current* target is itself backed up (tag ``restore``), so
    the restore is reversible; then the backup content is written to the target
    atomically. ``--dry-run`` reports everything without writing.

    Returns a JSON-serialisable outcome dict::

        {
            "ok": True,
            "dry_run": bool,
            "backup": str,            # the restored backup path
            "target": str,            # the original path restored to
            "base": str,              # original filename
            "tag": str,               # operation that made the backup
            "operation": str,         # human label
            "timestamp": str,         # backup UTC ISO timestamp
            "pre_restore_backup": str | None,  # fresh backup of the current
                                               # target, or None when the
                                               # target did not exist
            "restored": bool,
        }

    Raises:
        BackupError: If the argument is not a recognisable backup, points
            outside the project root, names a directory target, or the write
            fails.
    """
    # Resolve the backup path against the project root and refuse anything that
    # escapes it (a symlink, an absolute path, or a ``../`` traversal).
    backup_path = Path(backup_arg)
    if not backup_path.is_absolute():
        backup_path = project_root / backup_path
    try:
        backup_resolved = backup_path.resolve()
        project_resolved = project_root.resolve()
        backup_resolved.relative_to(project_resolved)
    except (OSError, ValueError) as exc:
        raise BackupError(
            f"backup must be inside the project directory {project_root}: {backup_arg}"
        ) from exc

    parsed = _parse_backup_name(backup_resolved.name)
    if parsed is None:
        raise BackupError(
            f"{backup_resolved.name} is not an iterate backup "
            "(expected <file>.<tag>-<UTCstamp>-<salt>, e.g. "
            "iterate.config.yaml.configset-20261101T091500Z-a1b2c3). "
            "Run `iterate backup list` to see the available backups."
        )
    if not backup_resolved.is_file():
        raise BackupError(
            f"backup not found: {backup_resolved} (run `iterate backup list` "
            "to see the available backups)"
        )

    base, tag, stamp = parsed
    target = backup_resolved.parent / base

    # Defense-in-depth: validate the DERIVED target stays inside the project
    # root, not just the backup argument. ``base`` comes from a filename
    # component so it cannot contain ``/``, but a crafted name like
    # ``...configset-<stamp>-<salt>`` yields greedy ``base == ".."`` which
    # would resolve to the project's PARENT directory. Today the ``is_dir()``
    # guard below happens to reject that, but the containment guarantee must
    # not rest on an incidental invariant — a future refactor that relaxes
    # ``is_dir()`` would otherwise open an arbitrary sibling-file overwrite.
    try:
        target.resolve().relative_to(project_resolved)
    except (OSError, ValueError) as exc:
        raise BackupError(
            f"cannot restore {backup_resolved.name}: {base} resolves outside "
            f"the project directory {project_root}"
        ) from exc

    if target.is_dir():
        raise BackupError(
            f"cannot restore {backup_resolved.name}: {base} is a directory, "
            "not a file"
        )
    if target == backup_resolved:
        raise BackupError(
            f"cannot restore {backup_resolved.name}: it is already the live file"
        )

    target_exists = target.is_file()
    pre_restore_backup: str | None = None

    if dry_run:
        return {
            "ok": True,
            "dry_run": True,
            "backup": str(backup_resolved),
            "target": str(target),
            "base": base,
            "tag": tag,
            "operation": TAG_LABELS.get(tag, tag),
            "timestamp": datetime.strptime(stamp, "%Y%m%dT%H%M%SZ")
            .replace(tzinfo=timezone.utc)
            .isoformat(),
            "pre_restore_backup": None,
            "restored": False,
        }

    try:
        # Read as bytes first: a backup of a non-UTF-8 file (binary, or a
        # config saved in a legacy code page) would make read_text("utf-8")
        # raise UnicodeDecodeError — a generic "failed to restore" that never
        # tells the operator the backup itself is the problem, and leaves it
        # permanently unrestorable. Detect that case and say what to do.
        content_bytes = backup_resolved.read_bytes()
        try:
            content = content_bytes.decode("utf-8")
        except UnicodeDecodeError:
            raise BackupError(
                f"{backup_resolved.name} is not UTF-8 text, so it cannot be "
                "restored with `iterate backup restore`. Restore the file "
                "manually from that backup path."
            ) from None
        # Back up the current target so the restore can be undone. If the
        # target does not exist there is nothing to preserve; the restore
        # simply recreates it.
        if target_exists:
            pre_restore_backup = backup_file(target, "restore")
        atomic_write(target, content)
    except (OSError, UnicodeDecodeError) as exc:
        raise BackupError(f"failed to restore {backup_resolved.name}: {exc}") from exc

    return {
        "ok": True,
        "dry_run": False,
        "backup": str(backup_resolved),
        "target": str(target),
        "base": base,
        "tag": tag,
        "operation": TAG_LABELS.get(tag, tag),
        "timestamp": datetime.strptime(stamp, "%Y%m%dT%H%M%SZ")
        .replace(tzinfo=timezone.utc)
        .isoformat(),
        "pre_restore_backup": str(pre_restore_backup) if pre_restore_backup else None,
        "restored": True,
    }


_AGE_RE = re.compile(r"^\s*(\d+)\s*([dwhm])?\s*$")


def parse_backup_age(value: str) -> timedelta:
    """Parse a ``--older-than`` duration into a ``timedelta``.

    Accepts ``30d`` (days, the default unit), ``2w`` (weeks), ``24h`` (hours),
    ``90m`` (minutes) or a bare integer (days). Raises :class:`BackupError`
    with an actionable message on anything else, so the CLI can print the
    accepted forms instead of a raw traceback.
    """
    match = _AGE_RE.fullmatch(value)
    if not match:
        raise BackupError(
            f"invalid --older-than value {value!r} (expected a duration like "
            "'30d', '7d', '24h', '90m', or a plain number of days)"
        )
    amount = int(match.group(1))
    unit = (match.group(2) or "d").strip()
    if amount <= 0:
        raise BackupError("--older-than must be a positive duration")
    return {
        "d": timedelta(days=amount),
        "w": timedelta(weeks=amount),
        "h": timedelta(hours=amount),
        "m": timedelta(minutes=amount),
    }[unit]


def prune_backups(
    project_root: Path,
    *,
    keep: int | None = None,
    older_than: str | None = None,
    dry_run: bool = False,
) -> dict[str, Any]:
    """Prune backup files under a retention policy.

    At least one of ``keep`` or ``older_than`` is required:

    * ``keep`` (>= 1): for each distinct base file, keep the ``keep`` newest
      backups and delete the rest — a rolling window per original file.
    * ``older_than`` (a duration like ``30d`` / ``7d`` / ``24h`` / ``90m``):
      delete every backup older than that age, even the newest of its base.

    When both are given the union applies: a backup is deleted if it is beyond
    the newest ``keep`` of its own base **or** older than ``older_than``.
    ``--dry-run`` reports the same outcome without deleting anything. Only
    recognisable iterate backups are ever touched; the live files they protect
    are never candidates, so pruning can never lose project state.

    Returns a JSON-serialisable outcome::

        {
            "ok": True,
            "dry_run": bool,
            "project": str,
            "keep": int | None,
            "older_than": str | None,
            "total": int,
            "deleted": [BackupEntry.to_dict(), ...],
            "kept": [BackupEntry.to_dict(), ...],
        }

    Raises:
        BackupError: If no policy is given, ``keep`` is < 1, ``older_than`` is
            invalid, or a delete fails.
    """
    if keep is None and older_than is None:
        raise BackupError(
            "prune needs at least one of --keep or --older-than "
            "(e.g. `iterate backup prune --keep 5`)"
        )
    if keep is not None and keep < 1:
        raise BackupError("--keep must be at least 1 (0 would delete every backup)")
    parsed_age = parse_backup_age(older_than) if older_than is not None else None

    all_backups = list_backups(project_root)  # newest first
    now = datetime.now(timezone.utc)

    # Rank every backup within its own base (0 = newest), so --keep is a
    # rolling window per original file rather than a global count that could
    # wipe the only backup of a rarely-touched file.
    rank_by_path: dict[str, int] = {}
    per_base_count: dict[str, int] = {}
    for entry in all_backups:
        per_base_count[entry.base] = per_base_count.get(entry.base, 0) + 1
        rank_by_path[str(entry.path)] = per_base_count[entry.base] - 1

    deleted: list[BackupEntry] = []
    kept: list[BackupEntry] = []
    for entry in all_backups:
        beyond_keep = keep is not None and rank_by_path[str(entry.path)] >= keep
        too_old = parsed_age is not None and (now - entry.timestamp) > parsed_age
        (deleted if (beyond_keep or too_old) else kept).append(entry)

    if not dry_run:
        for entry in deleted:
            try:
                entry.path.unlink()
            except OSError as exc:
                raise BackupError(
                    f"failed to prune {entry.path.name}: {exc} (re-run "
                    "`iterate backup list` to see what remains)"
                ) from exc

    return {
        "ok": True,
        "dry_run": dry_run,
        "project": str(project_root),
        "keep": keep,
        "older_than": older_than,
        "total": len(all_backups),
        "deleted": [entry.to_dict() for entry in deleted],
        "kept": [entry.to_dict() for entry in kept],
    }


def backups_json(project_root: Path, backups: list[BackupEntry]) -> str:
    """Serialise a listing as the single ``--json`` document."""
    return json.dumps(
        {
            "project": str(project_root),
            "count": len(backups),
            "backups": [entry.to_dict() for entry in backups],
        },
        ensure_ascii=False,
        indent=2,
    )
