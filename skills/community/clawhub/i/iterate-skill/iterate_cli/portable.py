"""Portable project-knowledge bundles (``iterate export`` / ``iterate import``).

A project's iterate knowledge is two files: ``iterate.config.yaml`` (goal,
dimensions, validation commands, invariants, personalization, fingerprints…)
and ``ITERATE.md`` (the generated knowledge base).  Until now those two files
could only be moved by hand — copy them, or re-run the interactive wizard on
the target machine.  That made three ordinary tasks awkward:

* **Backup / machine migration** — no supported way to snapshot the state and
  restore it later.
* **Team standardisation** — a vetted profile could not be applied to the next
  repository without walking the wizard again.
* **Review** — the state could not be attached to a PR/issue as one document.

This module defines the bundle format and the pure functions behind both
commands.  The CLI layer (``iterate_cli/cli.py``) only handles I/O, prompts and
exit codes.

Format (``bundle_version`` 1)::

    {
      "format": "iterate-skill-bundle",
      "bundle_version": 1,
      "skill_version": "3.6.0",       # informational: who wrote the bundle
      "exported_at": "2026-10-20T09:00:00Z",
      "project": "my-repo",           # basename only: no absolute paths leak
      "config": {...},                # the parsed config mapping
      "iterate_md": "..." | null      # knowledge base, null when absent
    }

Import validates the structure **and** the config against
``config/config.schema.json`` before writing anything, then writes both files
with timestamped backups — a failed or refused import leaves the project
untouched.
"""

from __future__ import annotations

import contextlib
import json
import os
import shutil
from dataclasses import dataclass, field
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any
from uuid import uuid4

import yaml

from iterate_cli import __version__
from iterate_cli.doctor import _schema_violations

#: Value of the ``format`` field. A bundle from a different tool is refused
#: rather than half-imported.
BUNDLE_FORMAT = "iterate-skill-bundle"

#: Current bundle schema version. Import refuses bundles *newer* than this.
BUNDLE_VERSION = 1

CONFIG_FILENAME = "iterate.config.yaml"
ITERATE_MD_FILENAME = "ITERATE.md"

#: Refuse absurd input files. A real bundle is a few hundred KiB at most; the
#: cap keeps a mistyped path (``iterate import /dev/zero`` or a huge tarball)
#: from being read into memory in full.
MAX_BUNDLE_BYTES = 8 * 1024 * 1024

#: ``onboarding`` keys that describe *this project's* files, not a portable
#: profile. Imported verbatim by default (faithful restore); dropped by
#: ``--reset-fingerprints`` so a profile can seed a different repository
#: without inheriting another project's manifest baseline.
PROJECT_LOCAL_ONBOARDING_KEYS: tuple[str, ...] = ("fingerprints",)


class BundleError(Exception):
    """A bundle could not be built, parsed or validated.

    The message is user-facing and always states what to do next; the CLI
    prints it verbatim (to stdout as ``{"error": ...}`` under ``--json``).
    """


@dataclass
class BundleValidation:
    """Outcome of validating a bundle document.

    Attributes:
        errors: Problems that make the bundle unusable (import refuses).
        warnings: Non-blocking remarks worth showing (unknown keys, schema
            validation unavailable, …).
        schema_checked: True when the config was actually checked against
            ``config.schema.json``; False when the schema/jsonschema was
            unavailable, so the caller can say so instead of implying a clean
            bill of health.
    """

    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    schema_checked: bool = False

    @property
    def ok(self) -> bool:
        """True when no blocking error was found."""
        return not self.errors


# ---------------------------------------------------------------------------
# Serialisation helpers
# ---------------------------------------------------------------------------


def _json_safe(value: Any) -> Any:
    """Return a JSON-serialisable copy of a YAML-loaded value.

    ``yaml.safe_load`` turns an unquoted timestamp into ``datetime``; dumping
    that with ``json.dumps`` raises ``TypeError``. Converting dates to ISO
    strings keeps the bundle valid JSON, and re-importing it writes the same
    value as a quoted YAML string, which the schema accepts.
    """
    if isinstance(value, dict):
        return {str(key): _json_safe(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_json_safe(item) for item in value]
    if isinstance(value, (datetime, date)):
        return value.isoformat()
    if value is None or isinstance(value, (str, int, float, bool)):
        return value
    # Anything else (bytes, sets, custom tags) has no portable meaning.
    return str(value)


def _utc_now(now: datetime | None) -> datetime:
    """Return ``now`` (or the current UTC time) as a timezone-aware UTC value."""
    if now is None:
        return datetime.now(timezone.utc)
    if now.tzinfo is None:
        return now.replace(tzinfo=timezone.utc)
    return now.astimezone(timezone.utc)


def build_bundle(project_root: Path, *, now: datetime | None = None) -> dict[str, Any]:
    """Capture the project's config and knowledge base as a bundle document.

    Read-only: nothing is written. Callers decide where the document goes.

    Args:
        project_root: Project root directory.
        now: Timestamp to record as ``exported_at`` (injectable for tests).

    Returns:
        The bundle mapping described in the module docstring.

    Raises:
        BundleError: No readable config, invalid YAML, a non-mapping root, or
            an unreadable ``ITERATE.md``. Each message names the fix.
    """
    config_path = project_root / CONFIG_FILENAME
    if not config_path.is_file():
        raise BundleError(
            f"No {CONFIG_FILENAME} in {project_root}. "
            "Run `iterate onboard` first (or `iterate import FILE` to restore "
            "a bundle into this directory)."
        )
    try:
        raw = config_path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        raise BundleError(f"Cannot read {CONFIG_FILENAME}: {exc}") from exc
    try:
        parsed = yaml.safe_load(raw)
    except yaml.YAMLError as exc:
        raise BundleError(
            f"{CONFIG_FILENAME} is not valid YAML: {exc}. "
            "Run `iterate doctor` to see the offending line, or fix it by hand."
        ) from exc
    if not isinstance(parsed, dict):
        if parsed is None:
            # An empty/comment-only file is a distinct, common mistake; the
            # generic "top-level must be a mapping" text sent users hunting for
            # a YAML error that does not exist.
            raise BundleError(
                f"{CONFIG_FILENAME} is empty. Run `iterate onboard` to populate "
                "it, or `iterate import FILE` to restore a saved state."
            )
        raise BundleError(
            f"{CONFIG_FILENAME} top-level must be a mapping (dict), got "
            f"{type(parsed).__name__}. Fix the file, or re-run `iterate onboard`."
        )
    config = _json_safe(parsed)
    if not isinstance(config, dict) or not config:  # defensive: see _json_safe
        raise BundleError(
            f"{CONFIG_FILENAME} is empty. Run `iterate onboard` to populate it."
        )
    # Export is the advertised backup/migration path: a bundle that `import`
    # would reject is worse than no backup at all. Validate before writing so
    # a schema-invalid config cannot be sealed into a file the tool then
    # refuses to restore.
    bundle_for_validation: dict[str, Any] = {
        "format": BUNDLE_FORMAT,
        "bundle_version": BUNDLE_VERSION,
        "skill_version": __version__,
        "exported_at": _utc_now(now).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "project": project_root.resolve().name,
        "config": config,
        # Placeholder: the real markdown is attached below. A null is valid.
        "iterate_md": None,
    }

    iterate_md: str | None = None
    md_path = project_root / ITERATE_MD_FILENAME
    if md_path.is_file():
        try:
            iterate_md = md_path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError) as exc:
            raise BundleError(f"Cannot read {ITERATE_MD_FILENAME}: {exc}") from exc

    bundle_for_validation["iterate_md"] = iterate_md
    validation = validate_bundle(bundle_for_validation)
    if not validation.ok:
        joined = "\n".join(f"  - {error}" for error in validation.errors)
        raise BundleError(
            "refusing to export a bundle that `iterate import` would reject:\n"
            f"{joined}\n"
            "Run `iterate doctor --fix`, or fix the listed values by hand, "
            "then retry the export."
        )
    # Basename only: an absolute path from the exporting machine would be
    # meaningless (and leak local directory layout) wherever it is imported.
    return bundle_for_validation


def bundle_to_json(bundle: dict[str, Any]) -> str:
    """Serialise a bundle as readable, human-diffable JSON (trailing newline)."""
    return json.dumps(bundle, ensure_ascii=False, indent=2) + "\n"


def default_bundle_name(now: datetime | None = None) -> str:
    """Return the default file name, e.g. ``iterate-bundle-20261020T090000Z.json``."""
    return f"iterate-bundle-{_utc_now(now).strftime('%Y%m%dT%H%M%SZ')}.json"


def parse_bundle_text(text: str, *, source: str = "bundle") -> dict[str, Any]:
    """Parse and validate bundle JSON from text.

    Args:
        text: Raw JSON document.
        source: Human-readable origin used in error messages (a path or
            ``"<stdin>"``).

    Returns:
        The validated bundle mapping.

    Raises:
        BundleError: Unreadable/oversized document, invalid JSON, or any
            structural/schema problem. Every error is listed in the message so
            one round trip is enough to fix all of them.
    """
    if len(text.encode("utf-8", "replace")) > MAX_BUNDLE_BYTES:
        raise BundleError(
            f"{source} is larger than {MAX_BUNDLE_BYTES // (1024 * 1024)} MiB; "
            "that is not an iterate bundle."
        )
    try:
        payload = json.loads(text)
    except json.JSONDecodeError as exc:
        raise BundleError(
            f"{source} is not valid JSON: {exc.msg} (line {exc.lineno}, "
            f"column {exc.colno})."
        ) from exc

    validation = validate_bundle(payload)
    if not validation.ok:
        joined = "\n".join(f"  - {error}" for error in validation.errors)
        raise BundleError(f"{source} is not a usable iterate bundle:\n{joined}")
    assert isinstance(payload, dict)  # guaranteed by validate_bundle
    return payload


# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------


def validate_bundle(payload: Any) -> BundleValidation:
    """Check a parsed bundle without touching the filesystem.

    Structural problems and schema violations are *errors*; unknown top-level
    keys (a bundle from a newer minor release) and an unavailable schema are
    *warnings* — the import can still proceed, but the caller must say so.

    Args:
        payload: Whatever ``json.loads`` returned.

    Returns:
        A :class:`BundleValidation` with all problems found (not just the first).
    """
    result = BundleValidation()
    if not isinstance(payload, dict):
        result.errors.append(
            f"root must be a JSON object, got {type(payload).__name__}"
        )
        return result

    fmt = payload.get("format")
    if fmt != BUNDLE_FORMAT:
        result.errors.append(
            f"format must be {BUNDLE_FORMAT!r}, got {fmt!r} "
            "(not an iterate export?)"
        )

    version = payload.get("bundle_version")
    if not isinstance(version, int) or isinstance(version, bool):
        result.errors.append(
            f"bundle_version must be an integer, got {version!r}"
        )
    elif version > BUNDLE_VERSION:
        result.errors.append(
            f"bundle_version {version} was written by a newer iterate "
            f"(this CLI supports up to {BUNDLE_VERSION}); run `iterate update` "
            "and retry"
        )
    elif version < 1:
        result.errors.append(f"bundle_version must be >= 1, got {version}")

    config = payload.get("config")
    if not isinstance(config, dict):
        result.errors.append(
            f"config must be a JSON object, got {type(config).__name__}"
        )
    elif not config:
        result.errors.append("config is empty; there is nothing to import")
    else:
        violations = _schema_violations(config)
        if violations is None:
            result.warnings.append(
                "config was not schema-checked (schema file or jsonschema "
                "unavailable); run `iterate doctor` after importing"
            )
        else:
            result.schema_checked = True
            for violation in violations:
                result.errors.append(f"config {violation}")

    iterate_md = payload.get("iterate_md", None)
    if iterate_md is not None and not isinstance(iterate_md, str):
        result.errors.append(
            f"iterate_md must be a string or null, got {type(iterate_md).__name__}"
        )
    elif isinstance(iterate_md, str) and not iterate_md.strip():
        result.errors.append(
            "iterate_md is present but empty; delete the field or re-export"
        )

    for key in ("project", "skill_version", "exported_at"):
        value = payload.get(key)
        if value is not None and not isinstance(value, str):
            result.errors.append(f"{key} must be a string, got {type(value).__name__}")

    known = {
        "format",
        "bundle_version",
        "skill_version",
        "exported_at",
        "project",
        "config",
        "iterate_md",
    }
    unknown = sorted(str(key) for key in payload if key not in known)
    if unknown:
        result.warnings.append(
            "ignoring unknown bundle key(s): " + ", ".join(unknown)
        )
    return result


def summarize_bundle(bundle: dict[str, Any]) -> dict[str, Any]:
    """Return a compact, JSON-safe description of a bundle for reports."""
    config = bundle.get("config")
    config = config if isinstance(config, dict) else {}
    iterate_md = bundle.get("iterate_md")
    return {
        "project": bundle.get("project"),
        "skill_version": bundle.get("skill_version"),
        "exported_at": bundle.get("exported_at"),
        "bundle_version": bundle.get("bundle_version"),
        "config_sections": sorted(str(key) for key in config),
        "config_keys": sorted(flatten_leaves(config)),
        "has_iterate_md": isinstance(iterate_md, str) and bool(iterate_md.strip()),
        "iterate_md_lines": (iterate_md.count("\n") + 1)
        if isinstance(iterate_md, str) and iterate_md
        else 0,
    }


# ---------------------------------------------------------------------------
# Diffing against the current project
# ---------------------------------------------------------------------------


def flatten_leaves(mapping: dict[str, Any], prefix: str = "") -> dict[str, Any]:
    """Flatten nested mappings to ``dotted.path -> leaf`` pairs.

    Lists are leaves on purpose: ``dimensions`` is compared as a set/sequence,
    not as ``dimensions.0``, so a reordered list reads as one change instead of
    a confusing index-by-index diff.
    """
    flat: dict[str, Any] = {}
    for key, value in mapping.items():
        path = f"{prefix}.{key}" if prefix else str(key)
        if isinstance(value, dict) and value:
            flat.update(flatten_leaves(value, path))
        else:
            flat[path] = value
    return flat


def _load_current_config(project_root: Path) -> dict[str, Any]:
    """Best-effort load of the project's current config (``{}`` when unusable)."""
    path = project_root / CONFIG_FILENAME
    try:
        parsed = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, yaml.YAMLError):
        return {}
    return parsed if isinstance(parsed, dict) else {}


def strip_fingerprints(config: dict[str, Any]) -> dict[str, Any]:
    """Return a copy of ``config`` without project-local onboarding keys.

    Used by ``iterate import --reset-fingerprints`` so a profile exported from
    repository A does not claim to describe repository B's manifests (which
    every drift check would then report as changed).
    """
    cleaned = json.loads(json.dumps(config))  # deep, JSON-safe copy
    onboarding = cleaned.get("onboarding")
    if isinstance(onboarding, dict):
        for key in PROJECT_LOCAL_ONBOARDING_KEYS:
            onboarding.pop(key, None)
        if not onboarding:
            cleaned.pop("onboarding", None)
    return cleaned


def diff_against_project(
    project_root: Path,
    bundle: dict[str, Any],
    *,
    reset_fingerprints: bool = False,
) -> dict[str, Any]:
    """Describe what importing ``bundle`` would change in ``project_root``.

    Read-only. Used both by ``--dry-run`` and by the confirmation prompt so the
    user sees the actual delta before consenting.

    Args:
        project_root: Target project root.
        bundle: A validated bundle.
        reset_fingerprints: Compare the incoming config *after* dropping
            project-local onboarding keys, mirroring what import would write.

    Returns:
        ``{"config": {"added": [...], "changed": [...], "removed": [...]},
        "iterate_md": "created" | "replaced" | "unchanged" | "absent",
        "would_write": [file names]}`` with dotted config keys.
    """
    incoming = bundle.get("config")
    incoming = incoming if isinstance(incoming, dict) else {}
    if reset_fingerprints:
        incoming = strip_fingerprints(incoming)

    current_leaves = flatten_leaves(_load_current_config(project_root))
    incoming_leaves = flatten_leaves(incoming)

    added = sorted(key for key in incoming_leaves if key not in current_leaves)
    removed = sorted(key for key in current_leaves if key not in incoming_leaves)
    changed = sorted(
        key
        for key in incoming_leaves
        if key in current_leaves and incoming_leaves[key] != current_leaves[key]
    )

    iterate_md = bundle.get("iterate_md")
    md_status = "absent"
    if isinstance(iterate_md, str):
        md_path = project_root / ITERATE_MD_FILENAME
        if not md_path.is_file():
            md_status = "created"
        else:
            try:
                current_md = md_path.read_text(encoding="utf-8")
            except (OSError, UnicodeDecodeError):
                current_md = None
            md_status = "same" if current_md == iterate_md else "replaced"
    # Normalise "same" to the documented "unchanged" spelling for callers.
    if md_status == "same":
        md_status = "unchanged"

    would_write = [CONFIG_FILENAME]
    if md_status in {"created", "replaced"}:
        would_write.append(ITERATE_MD_FILENAME)

    return {
        "config": {"added": added, "changed": changed, "removed": removed},
        "iterate_md": md_status,
        "would_write": would_write,
    }


# ---------------------------------------------------------------------------
# Applying
# ---------------------------------------------------------------------------


def _backup(path: Path, tag: str, now: datetime | None) -> Path | None:
    """Copy ``path`` beside itself as ``<name>.<tag>-<utc>-<salt>``.

    Returns the backup path, or None when there was nothing to back up.
    The name mirrors ``config set``/``doctor --fix`` (``*.configset-*``,
    ``*.doctorfix-*``) so every write this CLI makes is recognisable.
    """
    if not path.is_file():
        return None
    stamp = _utc_now(now).strftime("%Y%m%dT%H%M%SZ")
    backup = path.with_name(f"{path.name}.{tag}-{stamp}-{uuid4().hex[:6]}")
    shutil.copy2(path, backup)
    return backup


def apply_bundle(
    project_root: Path,
    bundle: dict[str, Any],
    *,
    reset_fingerprints: bool = False,
    now: datetime | None = None,
) -> dict[str, Any]:
    """Write a validated bundle into ``project_root``.

    Both files are backed up (when present) before being replaced, so a failed
    import is recoverable by copying the backup back. The caller is responsible
    for consent (``--yes``/prompt) and for having called :func:`validate_bundle`.

    Args:
        project_root: Target project root (must exist).
        bundle: A validated bundle.
        reset_fingerprints: Drop project-local onboarding keys before writing.
        now: Timestamp for backup names (injectable for tests).

    Returns:
        ``{"written": [...], "backups": [...], "fingerprints_reset": bool}``
        with paths relative to ``project_root`` where possible.

    Raises:
        BundleError: Serialisation or filesystem failure (with a message that
            names the backup files written so far).
    """
    config = bundle.get("config")
    if not isinstance(config, dict) or not config:
        raise BundleError("bundle has no config to import")
    if reset_fingerprints:
        config = strip_fingerprints(config)

    try:
        config_yaml = yaml.safe_dump(
            config, default_flow_style=False, allow_unicode=True, sort_keys=False
        )
    except yaml.YAMLError as exc:  # pragma: no cover - defensive
        raise BundleError(f"Cannot serialise the bundle config: {exc}") from exc

    backups: list[Path] = []
    backups_by_path: dict[Path, Path] = {}
    written: list[Path] = []
    config_path = project_root / CONFIG_FILENAME
    contents: list[tuple[Path, str]] = [(config_path, config_yaml)]
    iterate_md = bundle.get("iterate_md")
    if isinstance(iterate_md, str):
        contents.append((project_root / ITERATE_MD_FILENAME, iterate_md))

    # Stage every file first: an encoding error (lone surrogate) or a full disk
    # must fail BEFORE the existing config is touched. The previous flow wrote
    # the config and only then discovered a bad ITERATE.md, leaving the project
    # in a mixed old/new state despite the module's "refused import leaves the
    # project untouched" contract.
    staged: list[tuple[Path, Path]] = []
    try:
        for path, content in contents:
            staged_path = path.with_name(
                f".{path.name}.import-{os.getpid()}-{uuid4().hex[:8]}"
            )
            with open(staged_path, "x", encoding="utf-8", newline="") as handle:
                handle.write(content)
                handle.flush()
                os.fsync(handle.fileno())
            if path.exists():
                with contextlib.suppress(OSError):
                    shutil.copymode(path, staged_path)
            staged.append((path, staged_path))
    except (OSError, ValueError) as exc:
        for _, staged_path in staged:
            with contextlib.suppress(OSError):
                staged_path.unlink()
        raise BundleError(
            f"Failed to write into {project_root}: {exc}. "
            "Nothing was written."
        ) from exc

    try:
        for path, _ in staged:
            backup = _backup(path, "import", now)
            if backup is not None:
                backups.append(backup)
                backups_by_path[path] = backup
    except OSError as exc:
        for _, staged_path in staged:
            with contextlib.suppress(OSError):
                staged_path.unlink()
        kept = (
            " Backup(s) kept: " + ", ".join(path.name for path in backups)
            if backups
            else ""
        )
        raise BundleError(f"Failed to back up before import: {exc}.{kept}") from exc

    try:
        for path, staged_path in staged:
            # Preserve a symlinked destination (dotfile setups): os.replace on
            # a symlink swaps the *link* for a regular file, silently detaching
            # e.g. iterate.config.yaml -> ~/dotfiles and leaving the real file
            # stale. Resolve to the target so the replace happens at the real
            # path and the symlink survives — matching generator.atomic_write
            # and every other writer of the same paths.
            target = Path(os.path.realpath(path)) if path.is_symlink() else path
            os.replace(staged_path, target)
            written.append(path)
        # Publish durability: fsync the file's directory so the renames (not
        # just the staged bytes) survive a crash. Best-effort by design.
        from iterate_cli.generator import fsync_dir

        fsync_dir(project_root)
    except (OSError, ValueError) as exc:
        # Roll back the files already replaced, so a failure on the second
        # replace cannot leave a new config next to an old knowledge base.
        for path in reversed(written):
            backup = backups_by_path.get(path)
            try:
                if backup is not None:
                    shutil.copy2(backup, path)
                else:
                    path.unlink(missing_ok=True)
            except OSError:
                pass
        for _, staged_path in staged:
            with contextlib.suppress(OSError):
                staged_path.unlink()
        kept = (
            " Backup(s) kept: " + ", ".join(path.name for path in backups)
            if backups
            else ""
        )
        raise BundleError(
            f"Failed to write into {project_root}: {exc}. "
            "Already-replaced files were restored from backup." + kept
        ) from exc

    return {
        "written": [path.name for path in written],
        "backups": [path.name for path in backups],
        "fingerprints_reset": bool(reset_fingerprints),
    }
