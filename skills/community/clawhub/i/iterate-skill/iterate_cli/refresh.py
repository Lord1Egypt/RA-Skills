"""Onboarding refresh logic.

Handles two refresh modes:
- Incremental refresh: re-scan manifests, regenerate AI-maintained sections
  of ITERATE.md while preserving user-owned sections.
- Full re-onboarding: backup old files and run the full onboarding flow again.
"""

from __future__ import annotations

import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml

from iterate_cli import __version__ as SKILL_VERSION
from iterate_cli.fingerprint import (
    DriftResult,
    capture_fingerprints,
    check_drift,
    fingerprints_from_dict,
    fingerprints_to_dict,
)
from iterate_cli.generator import (
    DEFAULT_LANGUAGE,
    DEFAULT_REVIEW_SCOPE,
    DEFAULT_SCOPE_CHUNK_SIZE,
    DEFAULT_TARGET_BRANCH,
    OnboardingData,
    atomic_write,
    generate_refreshed_md,
    normalize_reasoning_effort,
    write_onboarding_outputs,
)
from iterate_cli.scan import (
    ScanResult,
    scan_project,
    suggest_command_whitelist,
    suggest_dimensions,
    suggest_validation_commands,
)
from iterate_cli.tui import tui
from iterate_cli.wizard import NO_CHANGES_NEEDED, run_wizard

# Files managed by onboarding.
ITERATE_MD = "ITERATE.md"
CONFIG_YAML = "iterate.config.yaml"

# Outcomes of full_reonboard (returned as strings so callers can render
# accurate user-facing messages instead of conflating every success path).
REONBOARD_COMPLETED = "completed"
REONBOARD_NO_CHANGES = "no-changes"
REONBOARD_CANCELLED = "cancelled"
REONBOARD_FAILED = "failed"


def load_onboarding_config(project_root: Path) -> dict[str, Any] | None:
    """Load the project-level iterate.config.yaml if it exists.

    Args:
        project_root: The project root directory.

    Returns:
        Parsed config dict, or None if the file does not exist, cannot
        be parsed, or is not a YAML mapping (errors are logged to stderr).
        Returning None for non-mapping content prevents AttributeError
        crashes in callers that call ``.get()`` on the result.
    """
    config_path = project_root / CONFIG_YAML
    if not config_path.is_file():
        return None
    try:
        config = yaml.safe_load(config_path.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        tui.error(f"Failed to parse {config_path}: {exc}")
        return None
    except (OSError, UnicodeDecodeError) as exc:
        # OSError: permission denied, file removed between is_file() and
        #   read_text(), filesystem errors, etc.
        # UnicodeDecodeError: file contains non-UTF-8 bytes (inherits
        #   ValueError, not OSError, so listed explicitly).
        # Either way: log and return None so callers fall back to defaults.
        tui.error(f"Failed to read {config_path}: {exc}")
        return None

    # yaml.safe_load returns None for an empty file (handled by ``or {}``
    # in callers) but a list/scalar for malformed content like ``- item``
    # or ``just a string``. Such non-dict results would crash callers
    # that call ``.get()``, so reject them here.
    if config is not None and not isinstance(config, dict):
        tui.error(
            f"{config_path} is not a YAML mapping (got {type(config).__name__})"
        )
        return None
    return config


def _load_refresh_config(project_root: Path) -> dict[str, Any] | None:
    """Load the project config for a refresh, distinguishing "absent" from "corrupt".

    A refresh regenerates the AI-maintained sections of ITERATE.md and updates
    ``onboarding.fingerprints`` inside ``iterate.config.yaml``. It must preserve
    every other user-customised field (dimensions, validation, personalization,
    …). If the config file exists but cannot be parsed (corrupt YAML, non-mapping,
    unreadable), refresh must **refuse to run** rather than silently rewriting the
    file with empty defaults — which would destroy the user's configuration.

    Returns:
        The parsed config dict, or ``{}`` when ``iterate.config.yaml`` does not
        exist (a legitimate first-refresh case). Returns ``None`` only when the
        file exists but cannot be parsed or read, signalling that refresh should
        abort.
    """
    config_path = project_root / CONFIG_YAML
    if not config_path.is_file():
        return {}
    config = load_onboarding_config(project_root)
    if config is None:
        # File exists, but load_onboarding_config logged the specific reason
        # (YAMLError / OSError / non-mapping) and returned None.
        return None
    return config


def get_stored_fingerprints(config: dict[str, Any]) -> list[dict[str, str]]:
    """Extract stored fingerprints from a loaded config dict.

    Malformed entries (non-dicts, missing ``path``/``sha256`` keys) are
    skipped via ``fingerprints_from_dict`` so a hand-edited config degrades
    to "no stored fingerprints" instead of crashing drift detection.

    Args:
        config: Parsed iterate.config.yaml content.

    Returns:
        List of fingerprint dicts, or empty list if not present.
    """
    onboarding = config.get("onboarding")
    onboarding = onboarding if isinstance(onboarding, dict) else {}
    raw = onboarding.get("fingerprints") or []
    if not isinstance(raw, list):
        return []
    return [entry.to_dict() for entry in fingerprints_from_dict(raw)]


def get_drift_ignore(config: dict[str, Any]) -> list[str]:
    """Extract drift-ignore glob patterns from the onboarding section.

    Patterns are matched against manifest basenames via fnmatch. Non-string
    or non-list values are discarded so malformed manual edits degrade to
    "ignore nothing" instead of crashing drift detection.

    Args:
        config: Parsed iterate.config.yaml content.

    Returns:
        List of fnmatch patterns, or empty list if not present.
    """
    onboarding = config.get("onboarding")
    onboarding = onboarding if isinstance(onboarding, dict) else {}
    raw = onboarding.get("drift_ignore") or []
    if not isinstance(raw, list):
        return []
    return [str(p) for p in raw if isinstance(p, str)]


def is_onboarding_complete(project_root: Path) -> bool:
    """Check whether onboarding has been completed for this project.

    Onboarding is considered complete if ITERATE.md exists in the project root.

    Args:
        project_root: The project root directory.

    Returns:
        True if ITERATE.md exists.
    """
    return (project_root / ITERATE_MD).is_file()


#: Stable machine-readable codes for "drift check unavailable". CLI exit
#: codes and TUI hint selection branch on THESE constants — never on the
#: human-readable message text, so rewording a message can never silently
#: flip a CI gate (the previous substring match on "could not be parsed"
#: would have).
DRIFT_REASON_CORRUPT = "corrupt_config"
DRIFT_REASON_NOT_ONBOARDED = "not_onboarded"
DRIFT_REASON_DISABLED = "drift_check_disabled"
DRIFT_REASON_NO_FINGERPRINTS = "no_fingerprints"
DRIFT_REASON_UNKNOWN = "unknown"

_DRIFT_REASON_MESSAGES: dict[str, str] = {
    DRIFT_REASON_CORRUPT: "iterate.config.yaml exists but could not be parsed",
    DRIFT_REASON_NOT_ONBOARDED: "onboarding not completed",
    DRIFT_REASON_DISABLED: "drift check is disabled (drift_check: false)",
    DRIFT_REASON_NO_FINGERPRINTS: (
        "no fingerprints recorded yet (run `iterate refresh` to capture them)"
    ),
    DRIFT_REASON_UNKNOWN: "drift check unavailable",
}


def drift_unavailable_code(
    project_root: Path, config: dict[str, Any] | None
) -> str:
    """Return a stable reason CODE for "drift check unavailable".

    Distinguishes "not onboarded" from "config corrupt" from "check disabled"
    from "no fingerprints yet". The code is the machine contract; the message
    from ``drift_unavailable_reason`` is derived from it for display. Lives
    here (next to ``check_onboarding_drift``) so ``status``, ``show`` and
    ``fingerprint`` cannot drift apart.
    """
    config_path = project_root / CONFIG_YAML
    if config_path.is_file() and config is None:
        return DRIFT_REASON_CORRUPT
    # Onboarding state outranks every other reason: without a completed
    # onboarding, `iterate refresh` refuses to run ("onboarding not
    # completed"), so advertising "run `iterate refresh`" here would send the
    # user to a command guaranteed to reject them. Evaluate this BEFORE the
    # config-presence guard: a never-onboarded project usually has no
    # iterate.config.yaml at all, so ``config`` is ``None`` there and the code
    # would otherwise fall through to the vaguer "unknown".
    if not is_onboarding_complete(project_root):
        return DRIFT_REASON_NOT_ONBOARDED
    if config is not None:
        onboarding = (
            config.get("onboarding")
            if isinstance(config.get("onboarding"), dict)
            else {}
        )
        if not onboarding.get("drift_check", True):
            return DRIFT_REASON_DISABLED
        stored = onboarding.get("fingerprints") or []
        if not isinstance(stored, list) or not stored:
            return DRIFT_REASON_NO_FINGERPRINTS
    return DRIFT_REASON_UNKNOWN


def drift_unavailable_reason(
    project_root: Path, config: dict[str, Any] | None
) -> str:
    """Return a human-readable reason for "drift check unavailable".

    Display counterpart of ``drift_unavailable_code`` (same four cases plus
    corrupt-config). The message must only be SHOWN to users; code that
    branches on the reason must use the code, not substring matching.
    """
    return _DRIFT_REASON_MESSAGES[drift_unavailable_code(project_root, config)]


#: Sentinel for "no pre-loaded config supplied" — ``None`` is a meaningful
#: value (the config exists but is unparseable), so it cannot double as the
#: default for an optional pre-loaded-config parameter.
_CONFIG_NOT_PASSED = object()


def check_onboarding_drift(
    project_root: Path,
    config: dict[str, Any] | None | object = _CONFIG_NOT_PASSED,
) -> DriftResult | None:
    """Check for drift since the last onboarding.

    Args:
        project_root: The project root directory.
        config: Optional ALREADY-LOADED config to reuse. Pass ``None``
            explicitly when the config exists but could not be parsed (avoids
            a second load emitting a SECOND identical parse-error report);
            omit the argument to load the config here (previous behaviour).

    Returns:
        DriftResult if onboarding was completed and drift check is enabled,
        None if onboarding was never completed or drift check is disabled.
    """
    if config is _CONFIG_NOT_PASSED:
        config = load_onboarding_config(project_root)
    if config is None:
        return None

    onboarding = config.get("onboarding")
    onboarding = onboarding if isinstance(onboarding, dict) else {}
    if not onboarding.get("drift_check", True):
        return None

    stored = get_stored_fingerprints(config)
    if not stored:
        return None

    return check_drift(project_root, stored, get_drift_ignore(config))


def incremental_refresh(project_root: Path) -> bool:
    """Perform an incremental refresh of ITERATE.md.

    Re-scans the project, regenerates the AI-maintained sections of
    ITERATE.md while preserving user-owned sections, and updates the
    fingerprints in iterate.config.yaml. Both files are written atomically;
    on failure the previous state is restored where possible.

    Args:
        project_root: The project root directory.

    Returns:
        True if refresh succeeded, False if ITERATE.md does not exist,
        cannot be read, or a write failure occurred.
    """
    ok, refreshed_md, config_yaml, error = _build_refresh_outputs(project_root)
    if not ok:
        tui.error(error)
        return False
    return _write_refresh_outputs(project_root, refreshed_md, config_yaml)


def preview_refresh(
    project_root: Path, include_diff: bool = False
) -> dict[str, Any]:
    """Compute a dry-run preview of what ``incremental_refresh`` would change.

    No files are written. Intended for ``iterate refresh --dry-run`` so a
    user can review the impact before committing to a refresh.

    Args:
        project_root: The project root directory.
        include_diff: When True, also compute ``md_diff`` / ``config_diff``
            unified diff strings so a caller can render exactly what would
            change rather than only the line counts. The config diff is only
            populated when the config is *semantically* different (a
            whitespace-only rewrite is not reported as a change), matching
            ``config_changed``.

    Returns:
        A dict:
        - ``ok``: bool — whether a preview could be computed.
        - ``error``: str — human-readable reason when ``ok`` is False.
        - ``changed``: bool — whether ITERATE.md or config would change.
        - ``config_changed``: bool — whether iterate.config.yaml would change.
        - ``md_changed_lines``: int — total added+removed lines in ITERATE.md.
        - ``stats``: dict with added/removed/changed line counts.
        - ``md_diff``: str (only when ``include_diff``) — unified diff of the
          ITERATE.md rewrite.
        - ``config_diff``: str (only when ``include_diff``) — unified diff of
          the iterate.config.yaml rewrite, or ``""`` when the config is not
          semantically changed.
    """
    empty = {
        "ok": False,
        "error": "",
        "changed": False,
        "config_changed": False,
        "md_changed_lines": 0,
        "stats": {},
    }
    ok, refreshed_md, config_yaml, error = _build_refresh_outputs(project_root)
    if not ok:
        empty["error"] = error
        return empty

    try:
        current_md = (project_root / ITERATE_MD).read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        empty["error"] = f"Failed to read {ITERATE_MD}: {exc}"
        return empty

    current_config = ""
    config_path = project_root / CONFIG_YAML
    try:
        current_config = config_path.read_text(encoding="utf-8")
    except FileNotFoundError:
        # A missing iterate.config.yaml is a legitimate first-refresh state
        # (_load_refresh_config returns {} for it, and incremental_refresh
        # succeeds): treat it as empty so preview and the real refresh agree
        # instead of the dry-run failing where the write path succeeds.
        current_config = ""
    except (OSError, UnicodeDecodeError) as exc:
        # Any OTHER read failure after _build_refresh_outputs parsed the
        # config is genuine (permissions flipped mid-run, IO error). Treating
        # it as an empty string would falsely flag config_changed and misguide
        # the preview (which claims to refuse to overwrite an unparseable
        # config).
        empty["error"] = f"Failed to read {CONFIG_YAML}: {exc}"
        return empty

    md_changed = refreshed_md != current_md
    config_changed = not _config_semantically_equal(current_config, config_yaml)
    stats = _diff_stats(current_md, refreshed_md)
    result: dict[str, Any] = {
        "ok": True,
        "error": "",
        "changed": md_changed or config_changed,
        "config_changed": config_changed,
        "md_changed_lines": stats["changed"],
        "stats": stats,
    }
    if include_diff:
        result["md_diff"] = unified_diff(
            current_md, refreshed_md, ITERATE_MD, ITERATE_MD
        )
        result["config_diff"] = (
            unified_diff(current_config, config_yaml, CONFIG_YAML, CONFIG_YAML)
            if config_changed
            else ""
        )
    return result


def _build_refresh_outputs(project_root: Path) -> tuple[bool, str, str, str]:
    """Build the refreshed ITERATE.md and config YAML without writing.

    Args:
        project_root: The project root directory.

    Returns:
        ``(ok, refreshed_md, config_yaml, error)``. When ``ok`` is False,
        the two content strings are empty and ``error`` explains why.
    """
    iterate_md_path = project_root / ITERATE_MD
    if not iterate_md_path.is_file():
        return False, "", "", f"{ITERATE_MD} does not exist."
    try:
        existing_md = iterate_md_path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        return False, "", "", f"Failed to read {iterate_md_path}: {exc}"

    scan = scan_project(project_root)
    existing_config = _load_refresh_config(project_root)
    if existing_config is None:
        return False, "", "", f"{CONFIG_YAML} exists but could not be parsed; refusing to overwrite with defaults."
    data = _build_refresh_data(project_root, scan, existing_config)
    try:
        refreshed_md = generate_refreshed_md(data, existing_md)
    except ValueError as exc:
        # Refusing to overwrite an ITERATE.md without the USER-OWNED markers
        # (it may be hand-edited); surface the reason instead of destroying it.
        return False, "", "", str(exc)
    except (OSError, UnicodeDecodeError) as exc:
        # A broken/stripped install where neither the packaged template nor
        # the repo fallback is readable must not crash refresh with a raw
        # traceback; surface a clean error instead.
        return False, "", "", f"Failed to generate {ITERATE_MD}: {exc}"
    new_config = _build_refreshed_config(existing_config, data)
    config_yaml = yaml.safe_dump(
        new_config,
        default_flow_style=False,
        allow_unicode=True,
        sort_keys=False,
    )
    return True, refreshed_md, config_yaml, ""


def _config_semantically_equal(existing_text: str, new_yaml: str) -> bool:
    """Compare two config documents by value, not by bytes.

    ``yaml.safe_dump`` drops comments, so a byte comparison against a config
    authored from the shipped template always reported a change — refresh then
    rewrote the file (erasing all guidance comments) even though no value had
    moved. Unparseable input falls back to "different" so a corrupt file is
    never mistaken for a no-op.
    """
    try:
        return yaml.safe_load(existing_text) == yaml.safe_load(new_yaml)
    except yaml.YAMLError:
        return False


def _backup_refresh_config(config_path: Path) -> Path | None:
    """Copy the current config before a value-changing rewrite.

    Comments cannot survive ``safe_dump``; keeping a timestamped, uniquely
    suffixed copy makes a refresh recoverable (same ``.refresh-*`` convention
    as the other writers' ``.configset-*`` / ``.doctorfix-*`` backups).

    Raises:
        OSError: If the copy fails. The caller aborts the rewrite: proceeding
            without a recoverable pre-change snapshot would make the very
            failure mode (permissions/quota) that caused the backup error
            irreversible.
    """
    if not config_path.is_file():
        return None
    from iterate_cli.generator import backup_file

    return backup_file(config_path, "refresh")


def _write_refresh_outputs(project_root: Path, refreshed_md: str, config_yaml: str) -> bool:
    """Atomically write refreshed ITERATE.md and config, rolling back on failure.

    Both files are written with ``_atomic_write`` (temp file + ``os.replace``).
    Files whose content is unchanged are skipped (a refresh that changed
    nothing is a logical no-op and must not churn mtimes or fail on read-only
    dirs). If either write fails, the other is rolled back to its pre-refresh
    state. If rollback itself fails, files may be inconsistent (logged to
    stderr).

    Args:
        project_root: The project root directory.
        refreshed_md: New ITERATE.md content.
        config_yaml: New iterate.config.yaml YAML content.

    Returns:
        True on success, False if a write or rollback failed.
    """
    iterate_md_path = project_root / ITERATE_MD
    config_path = project_root / CONFIG_YAML

    backup_md: str | None = None
    backup_config: str | None = None
    try:
        try:
            backup_md = iterate_md_path.read_text(encoding="utf-8")
        except FileNotFoundError:
            # A refresh on a project without ITERATE.md creates it; there is
            # nothing to roll back TO.
            backup_md = None
        except (OSError, UnicodeDecodeError) as exc:
            # An existing-but-unreadable file cannot be rolled back. Fail
            # closed *before* writing anything instead of leaving a rewritten
            # config next to a file we could not snapshot.
            tui.error(
                f"Cannot refresh: {iterate_md_path} exists but cannot be read "
                f"for rollback ({exc}). Fix its permissions/encoding and retry; "
                "nothing was written."
            )
            return False
        try:
            backup_config = config_path.read_text(encoding="utf-8")
        except FileNotFoundError:
            # Legitimate first-refresh state (no iterate.config.yaml yet —
            # _load_refresh_config treats that as {}): there is nothing to
            # roll back TO, and the file is about to be created. An error
            # line here used to appear on every successful first refresh.
            backup_config = None
        except (OSError, UnicodeDecodeError) as exc:
            tui.error(
                f"Cannot refresh: {config_path} exists but cannot be read for "
                f"rollback ({exc}). Fix its permissions/encoding and retry; "
                "nothing was written."
            )
            return False

        # A logical no-op refresh (nothing changed since the last run) must not
        # churn file mtimes/inodes or fail on read-only project dirs, so only
        # rewrite each file when its content actually differs. A failed backup
        # read (None) counts as "differs" and still triggers a write.
        needs_md = backup_md != refreshed_md
        needs_config = (
            backup_config is None
            or not _config_semantically_equal(backup_config, config_yaml)
        )
        wrote_md = False
        wrote_config = False
        if needs_md:
            atomic_write(iterate_md_path, refreshed_md)
            wrote_md = True
        if needs_config:
            if backup_config is not None:
                _backup_refresh_config(config_path)
            atomic_write(config_path, config_yaml)
            wrote_config = True
    except OSError as exc:
        tui.error(f"Failed to write refresh outputs: {exc}")
        if wrote_md and backup_md is not None:
            try:
                atomic_write(iterate_md_path, backup_md)
            except OSError as rollback_exc:
                tui.error(f"Rollback failed for {iterate_md_path}: {rollback_exc}")
        if wrote_config and backup_config is not None:
            try:
                atomic_write(config_path, backup_config)
            except OSError as rollback_exc:
                tui.error(f"Rollback failed for {config_path}: {rollback_exc}")
        return False
    return True


def unified_diff(before: str, after: str, fromfile: str, tofile: str) -> str:
    """Build a unified diff between two text blobs.

    ``difflib.unified_diff`` yields context lines including the ``---`` /
    ``+++`` and ``@@`` hunks, which is exactly what a human or a review tool
    wants when deciding whether to apply a refresh. The diff is generated
    without a trailing newline after the final hunk so the CLI can print it
    as-is; callers that write to a file add their own newline.

    Args:
        before: Original text.
        after: New text.
        fromfile: Label for the "before" side (typically the file path).
        tofile: Label for the "after" side.

    Returns:
        A unified diff string (empty when the two blobs are identical).
    """
    import difflib

    if before == after:
        return ""
    return "".join(
        difflib.unified_diff(
            before.splitlines(),
            after.splitlines(),
            fromfile=fromfile,
            tofile=tofile,
            lineterm="\n",
        )
    )


def _coerce_bool(value: Any) -> bool:
    """Coerce a git-boolean config value to a real bool, secure-by-default.

    Mirrors the push_per_round normalisation: only real bools are
    authoritative, and a truthy scalar (``"yes"``, ``"on"``, ``1``, ``"true"``)
    is accepted so a hand-edited value does not silently flip a user's
    ``use_worktree``/``auto_merge`` to its default. Anything unrecognised is
    False (the secure default), matching the documented defaults.

    Args:
        value: The raw config value.

    Returns:
        The coerced bool.
    """
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in ("1", "true", "yes", "on")


def _diff_stats(before: str, after: str) -> dict[str, int]:
    """Count added/removed lines between two text blobs.

    Uses ``difflib.SequenceMatcher`` opcodes instead of parsing unified-diff
    markers: a content line that itself starts with ``+``/``-`` (e.g. an
    added ``++ comment`` line) previously collided with the ``+++ `` file
    header and was dropped from the counts. Opcode length arithmetic has no
    such ambiguity.

    Args:
        before: Original text.
        after: New text.

    Returns:
        A dict with ``added``, ``removed`` and ``changed`` (added + removed)
        line counts.
    """
    import difflib

    added = 0
    removed = 0
    matcher = difflib.SequenceMatcher(
        None, before.splitlines(), after.splitlines()
    )
    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag == "insert":
            added += j2 - j1
        elif tag == "delete":
            removed += i2 - i1
        elif tag == "replace":
            added += j2 - j1
            removed += i2 - i1
    return {"added": added, "removed": removed, "changed": added + removed}


def _build_refreshed_config(
    existing_config: dict[str, Any],
    data: OnboardingData,
) -> dict[str, Any]:
    """Build a refreshed config dict, persisting reconciled refresh results.

    In addition to updating the onboarding fingerprints, this writes back the
    additively-reconciled values computed by ``_build_refresh_data`` so an
    incremental refresh actually persists tooling/whitelist/dimension-sets
    reconciliation for newly-detected languages (previously these were
    computed, used to render ITERATE.md, then dropped — the config drifted
    from what was advertised).

    Does not write to disk; the caller is responsible for writing (typically
    as part of an atomic refresh).

    Args:
        existing_config: The existing parsed config dict.
        data: Fresh OnboardingData carrying reconciled refresh results.

    Returns:
        New config dict with reconciled fields, fingerprints and
        completed_at/skill_version updated.
    """

    def _as_dict_list(value: object) -> dict[str, Any]:
        return dict(value) if isinstance(value, dict) else {}

    def _as_list(value: object) -> list[str]:
        return list(value) if isinstance(value, list) else []

    config = dict(existing_config)
    onboarding_section = config.get("onboarding")
    onboarding = (
        dict(onboarding_section) if isinstance(onboarding_section, dict) else {}
    )

    # Persist the reconciled fields from _build_refresh_data. These preserve
    # existing (possibly customised) values and additively append suggestions
    # for newly-detected languages.
    config["dimensions"] = _as_list(data.dimensions)
    config["dimension_sets"] = _as_dict_list(data.dimension_sets)
    config["reasoning_effort"] = data.reasoning_effort
    config["language"] = data.language
    review = _as_dict_list(existing_config.get("review"))
    review["scope"] = data.review_scope
    config["review"] = review
    git_cfg = _as_dict_list(existing_config.get("git"))
    git_cfg["target_branch"] = data.target_branch
    git_cfg["push_per_round"] = data.push_per_round
    # Persist the preserved git booleans too, so the written config and the
    # OnboardingData they came from cannot disagree (previously they were only
    # carried through the existing git dict, which happened to work but left
    # the two views of the same setting with no single source of truth).
    git_cfg["use_worktree"] = data.use_worktree
    git_cfg["auto_merge"] = data.auto_merge
    config["git"] = git_cfg
    validation = _as_dict_list(existing_config.get("validation"))
    # Schema requires command_whitelist to be non-empty when present (minItems
    # 1); an operator-cleared whitelist is expressed by dropping the key
    # (mirroring personalize.merge_personalization_into_config) so the
    # refreshed config stays schema-valid instead of persisting an invalid
    # ``command_whitelist: []`` that doctor/refresh would keep flagging.
    if data.command_whitelist:
        validation["command_whitelist"] = _as_list(data.command_whitelist)
    else:
        validation.pop("command_whitelist", None)
    validation["commands"] = _as_dict_list(data.validation_commands)
    config["validation"] = validation

    # Idempotent fingerprint refresh: only restamp ``completed_at`` when the
    # manifest fingerprints actually changed (keeps ``iterate refresh`` a no-op
    # when nothing drifted; ``--dry-run`` reports "no changes needed" instead of
    # always showing a diff due to a fresh timestamp).
    #
    # NOTE: this timestamp is "when the CONFIG was last reconciled". The Meta
    # row in ITERATE.md is deliberately NOT restamped (refresh reuses the old
    # value so an unchanged refresh stays byte-for-byte identical), so it keeps
    # meaning "when ITERATE.md was last generated". The two can therefore
    # diverge after a fingerprint-only refresh; that is intentional, not a
    # staleness bug — do not "fix" one to match the other without revisiting
    # the idempotency requirement above.
    new_fp = fingerprints_to_dict(data.fingerprints)
    if onboarding.get("fingerprints") != new_fp:
        onboarding["completed_at"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    onboarding["fingerprints"] = new_fp
    # Keep the recorded skill version in sync with the installed version so a
    # version bump surfaced by ``iterate doctor`` (which advises ``iterate
    # refresh`` as the fix) is actually resolved here rather than persisting a
    # stale record that doctor keeps flagging.
    if onboarding.get("skill_version") != SKILL_VERSION:
        onboarding["skill_version"] = SKILL_VERSION
    config["onboarding"] = onboarding
    return config


def full_reonboard(
    project_root: Path,
    input_func=None,
) -> str:
    """Perform a full re-onboarding, backing up old files first.

    Backs up existing ITERATE.md and iterate.config.yaml, then runs the
    full onboarding wizard. If input_func is None, uses the default input().

    Args:
        project_root: The project root directory.
        input_func: Optional input callable for testing.

    Returns:
        One of the REONBOARD_* status strings:
        - ``REONBOARD_COMPLETED`` — wizard produced data and outputs were written.
        - ``REONBOARD_NO_CHANGES`` — returning user declined all updates;
          nothing was written (old files remain intact).
        - ``REONBOARD_CANCELLED`` — wizard was cancelled before any write.
        - ``REONBOARD_FAILED`` — no existing files, or backup/write failed
          (errors are logged to stderr).
    """
    iterate_md_path = project_root / ITERATE_MD
    config_path = project_root / CONFIG_YAML

    if not iterate_md_path.is_file() and not config_path.is_file():
        return REONBOARD_FAILED

    # Backup existing files. The name embeds a short random salt so two
    # re-onboards in the same second cannot silently overwrite each other's
    # snapshot (mirroring configcmd.run_config_set's salted backup).
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    import uuid

    backup_suffix = f"{timestamp}-{uuid.uuid4().hex[:6]}"
    try:
        if iterate_md_path.is_file():
            shutil.copy2(
                iterate_md_path, project_root / f"{ITERATE_MD}.bak-{backup_suffix}"
            )
        if config_path.is_file():
            shutil.copy2(
                config_path, project_root / f"{CONFIG_YAML}.bak-{backup_suffix}"
            )
    except OSError as exc:
        tui.error(f"Backup failed, aborting re-onboarding: {exc}")
        return REONBOARD_FAILED

    # Marker pre-check (after backup, before the wizard runs): when the
    # USER-OWNED markers are gone, write_onboarding_outputs would fall back to
    # the TEMPLATE user section and overwrite the live file — the previous
    # warning was printed by that same command AFTER the overwrite, telling
    # the user to "restore the markers and re-run" a file it had just
    # replaced. Warn here (the .bak-<suffix> copy above is the real safety
    # net) so the downgrade is announced before anything happens.
    if iterate_md_path.is_file():
        from iterate_cli.generator import has_valid_user_owned_markers

        try:
            existing_md_text = iterate_md_path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            existing_md_text = None
        if existing_md_text is not None and not has_valid_user_owned_markers(
            existing_md_text
        ):
            tui.warning(
                "Existing ITERATE.md is missing the USER-OWNED section markers; "
                "reonboard will rebuild the user section from the template."
            )
            tui.hint(
                f"Your current file is backed up at "
                f"{ITERATE_MD}.bak-{backup_suffix}.",
                indent=2,
            )

    # Run the full wizard.
    if input_func is not None:
        data = run_wizard(project_root, input_func=input_func)
    else:
        data = run_wizard(project_root)

    def _remove_backups() -> None:
        """Best-effort removal of the snapshots taken above.

        Called on the no-write exit paths (cancelled / no changes): nothing
        was written, so the copies are pure litter in the repo root that
        accumulated as untracked ``*.bak-*`` files on every cancelled
        re-onboard. A failed unlink is harmless and must not change the
        returned status.
        """
        for name in (ITERATE_MD, CONFIG_YAML):
            try:
                (project_root / f"{name}.bak-{backup_suffix}").unlink(missing_ok=True)
            except OSError:
                pass

    if data is None:
        _remove_backups()
        return REONBOARD_CANCELLED
    if data is NO_CHANGES_NEEDED:
        # Returning user declined all updates; nothing to write, so drop the
        # snapshots as well — there is nothing to recover from.
        _remove_backups()
        return REONBOARD_NO_CHANGES

    # Preserve existing personalization when the user did not re-personalize,
    # so a basic-config update does not silently drop structured rules
    # (protected paths, risk areas, extra validation commands, etc.) or
    # free-form notes/conventions stored in ITERATE.md. Mirrors the rescue in
    # cli._cmd_onboard (cli.py:546-556).
    if data.personalization is None:
        from iterate_cli.personalize import load_existing_personalization

        existing_onboarding_config = load_onboarding_config(project_root) or {}
        existing_personalization = load_existing_personalization(
            project_root, existing_onboarding_config
        )
        if not existing_personalization.is_empty():
            data.personalization = existing_personalization

    try:
        # Preserve the user-owned ITERATE.md section (manual edits +
        # personalization content) across a full re-onboard, keeping behaviour
        # consistent with ``onboard`` on an existing project. The .bak copy
        # already saved above remains as a safety net.
        existing_md: str | None = None
        if iterate_md_path.is_file():
            try:
                existing_md = iterate_md_path.read_text(encoding="utf-8")
            except (OSError, UnicodeDecodeError) as exc:
                # Refuse to continue: regenerating from scratch would silently
                # drop the user-owned (manual) section. The .bak snapshot taken
                # above keeps the original intact for manual recovery.
                tui.error(
                    f"Failed to read {iterate_md_path} for user-owner preservation: {exc}"
                )
                tui.info(
                    "为避免覆盖你的手动编辑区，已中止 re-onboarding。"
                    "原文件保留在 .bak 备份中，请先修复读取问题后重试。"
                )
                return REONBOARD_FAILED
        write_onboarding_outputs(data, project_root, existing_md)
    except (OSError, ValueError) as exc:
        # OSError: write failed (rolled back). ValueError: generated
        # ITERATE.md lacks the USER-OWNED markers (damaged template) —
        # write_onboarding_outputs refuses before touching the filesystem.
        tui.error(f"Failed to write onboarding outputs: {exc}")
        return REONBOARD_FAILED

    # On success the pre-write snapshots are intentionally kept as a safety net.
    # Name them: otherwise every re-onboard silently leaves untracked
    # ``*.bak-*`` files in the project root with no hint they exist.
    kept_backups = [
        f"{name}.bak-{backup_suffix}"
        for name in (ITERATE_MD, CONFIG_YAML)
        if (project_root / f"{name}.bak-{backup_suffix}").is_file()
    ]
    if kept_backups:
        tui.hint("Pre-re-onboard backup kept: " + ", ".join(kept_backups))
    return REONBOARD_COMPLETED


def _reconcile_validation_suggestions(
    validation_commands: dict[str, list[str]],
    effective_whitelist: list[str],
    scan: ScanResult,
) -> tuple[dict[str, list[str]], list[str]]:
    """Additively reconcile validation tooling with a newly-detected stack.

    When a language has been added to the project since the last onboarding,
    its suggested validation commands and command-whitelist prefixes are
    appended so the refreshed config actually validates it. Existing
    (possibly customised) configuration is preserved and never removed —
    only missing entries for newly-detected languages are added.

    Args:
        validation_commands: Existing ``validation.commands`` mapping.
        effective_whitelist: The currently effective command whitelist.
        scan: Fresh ScanResult used to derive per-language suggestions.

    Returns:
        Updated (validation_commands, effective_whitelist).
    """
    suggested_commands = suggest_validation_commands(scan)
    commands = dict(validation_commands)
    for module, cmds in suggested_commands.items():
        if module not in commands:
            commands[module] = list(cmds)

    suggested_prefixes = suggest_command_whitelist(scan)
    seen = set(effective_whitelist)
    whitelist = list(effective_whitelist)
    for prefix in suggested_prefixes:
        if prefix not in seen:
            seen.add(prefix)
            whitelist.append(prefix)
    return commands, whitelist


def _resolve_validation_config(
    existing_config: dict[str, Any],
    scan: ScanResult,
) -> tuple[dict[str, list[str]], list[str]]:
    """Resolve validation.commands + effective command_whitelist for a refresh.

    Preserves existing (possibly customised) validation configuration and
    additively reconciles tooling with the newly-detected tech stack (a
    language added since the last onboarding gets its suggested commands +
    whitelist prefixes appended).

    An explicit ``command_whitelist: []`` is NOT treated as a "run no
    commands" intent: the schema forbids it (minItems 1) and
    ``_build_refreshed_config`` drops the key, so the previous "preserve for
    one round, refill with suggestions on the next" behaviour only delayed
    the refill by one refresh while claiming to honour an intent the config
    cannot actually express. It is now flagged (tui.warning) and resolved
    exactly like an absent key — predictable on the very first refresh.

    Returns:
        (validation_commands, effective_whitelist).
    """
    validation_existing = existing_config.get("validation")
    validation_existing = validation_existing if isinstance(validation_existing, dict) else {}
    # Guard against a hand-edited scalar ``validation.commands`` value: the
    # reconcile step does ``dict(commands)``, which would crash on a string.
    existing_commands = validation_existing.get("commands")
    if existing_commands is not None and not isinstance(existing_commands, dict):
        tui.warning(
            "validation.commands is not a mapping — ignored; scan suggestions "
            "are used instead."
        )
        existing_commands = {}
    validation_commands = existing_commands if isinstance(existing_commands, dict) else {}
    # Normalize PER-MODULE values (not just the top-level type): a hand-edited
    # `{python: "pytest -q"}` (scalar instead of a list) passed the guard above,
    # was written back verbatim by _build_refreshed_config, and then tripped
    # doctor/validate forever — refresh claims to normalize hand edits back to
    # schema-valid values, so non-list modules are dropped (announced) and
    # non-string entries filtered, mirroring wizard._load_existing_onboarding_data.
    normalized_commands: dict[str, list[str]] = {}
    for module, cmds in validation_commands.items():
        if not isinstance(cmds, list):
            tui.warning(
                f"validation.commands[{module!r}] is not a list — dropped "
                "(doctor/validate would reject it)."
            )
            continue
        filtered = [c for c in cmds if isinstance(c, str) and c.strip()]
        if len(filtered) != len(cmds):
            tui.warning(
                f"validation.commands[{module!r}] had non-string/empty entries — "
                "they were dropped."
            )
        if not filtered:
            # All entries were invalid: an empty list violates the schema
            # (minItems 1), so the module cannot be kept as-is either.
            tui.warning(
                f"validation.commands[{module!r}] has no valid commands — module dropped."
            )
            continue
        normalized_commands[str(module)] = filtered
    validation_commands = normalized_commands
    has_whitelist_key = "command_whitelist" in validation_existing
    command_whitelist = validation_existing.get("command_whitelist")
    if isinstance(command_whitelist, list):
        # Schema requires items to be non-empty strings. A hand-edited
        # `[["pytest"]]` used to reach `set(...)` and crash refresh with
        # `TypeError: unhashable type: 'list'`; `[123]` was written back as an
        # invalid config. Filter (and say so) instead of aborting the run.
        valid_entries = [
            entry.strip()
            for entry in command_whitelist
            if isinstance(entry, str) and entry.strip()
        ]
        if len(valid_entries) != len(command_whitelist):
            tui.warning(
                "validation.command_whitelist contained non-string or empty "
                "entries; they were dropped (the schema requires non-empty "
                "strings)."
            )
        command_whitelist = valid_entries
    if not command_whitelist:
        # Key present but empty (`[]`) or a hand-edited scalar/absent: all
        # three are schema-invalid-or-absent states, so resolve them the same
        # way and TELL the operator when a present-but-invalid value was
        # ignored — silently refilling was the old two-round flip.
        if has_whitelist_key:
            tui.warning(
                "validation.command_whitelist is empty or not a list — the "
                "schema requires a non-empty list, so scan suggestions are "
                "used instead (set explicit prefixes to override)."
            )
        command_whitelist = suggest_command_whitelist(scan)
    # An explicit empty whitelist can no longer reach here, so the whitelist
    # is always reconciled additively (newly-detected languages get prefixes).
    return _reconcile_validation_suggestions(
        validation_commands, command_whitelist, scan
    )


def _preserve_onboarding_meta(existing_config: dict[str, Any]) -> tuple[str, str, str]:
    """Extract channel + user-entered text from the existing onboarding section.

    Returns:
        (channel, project_description, code_conventions).
    """
    onboarding_section = existing_config.get("onboarding")
    onboarding_section = onboarding_section if isinstance(onboarding_section, dict) else {}
    channel = onboarding_section.get("channel", "cli")
    if not isinstance(channel, str):
        # A hand-edited config may hold a non-string channel; normalise so the
        # regenerated config never persists an invalid value.
        channel = "cli"
    project_description = str(onboarding_section.get("project_description") or "")
    code_conventions = str(onboarding_section.get("code_conventions") or "")
    return channel, project_description, code_conventions


def _preserve_reviewer_tuning(existing_config: dict[str, Any]) -> dict[str, Any]:
    """Extract reviewer tuning keys, preserving them across a refresh."""
    reviewer_cfg = existing_config.get("reviewer")
    reviewer_cfg = reviewer_cfg if isinstance(reviewer_cfg, dict) else {}
    return {
        "output_schema_validation": reviewer_cfg.get("output_schema_validation", True),
        "evidence_validation": reviewer_cfg.get("evidence_validation", True),
        "coverage_validation": reviewer_cfg.get("coverage_validation", True),
        "scope_chunk_size": reviewer_cfg.get("scope_chunk_size", DEFAULT_SCOPE_CHUNK_SIZE),
    }


def _build_refresh_data(
    project_root: Path,
    scan: ScanResult,
    existing_config: dict[str, Any],
) -> OnboardingData:
    """Build OnboardingData for a refresh, preserving existing settings."""
    # Preserve existing dimensions, target_branch, etc.
    existing_dimensions = existing_config.get("dimensions")
    # A hand-edited scalar/string dimensions value (e.g. ``dimensions:
    # "correctness"``) must not be iterated character-by-character by the
    # ITERATE.md renderer; fall back to scan suggestions instead. Non-string
    # LIST elements (``dimensions: [1, 2]``) are coerced to strings and empty
    # ones dropped so the rebuilt config stays schema-valid.
    if isinstance(existing_dimensions, list):
        dimensions = [
            str(d)
            for d in existing_dimensions
            # None is a YAML null (``dimensions: [- ]``-style hand edit): it
            # would stringify to the literal "None" and get rendered into
            # ITERATE.md as a dimension name, so drop it explicitly rather
            # than let str() launder it through.
            if d is not None and str(d).strip()
        ] or suggest_dimensions(scan)
    else:
        dimensions = suggest_dimensions(scan)
    # Preserve scope-specific dimension sets, additively reconciling with a
    # freshly-detected stack (a layer added since onboarding gets its preset).
    from iterate_cli.dimension_sets import (
        merge_dimension_sets,
        normalize_dimension_sets,
        suggest_dimension_sets,
    )

    existing_dimension_sets = normalize_dimension_sets(
        existing_config.get("dimension_sets"),
        # This normalized value is written back to iterate.config.yaml, so a
        # dropped hand-written entry must be announced — silently deleting it
        # on the next `iterate refresh` (exit 0, no output) was data loss.
        on_drop=lambda name: tui.warning(
            f"dimension_sets entry {name!r} was dropped from the "
            "refreshed config (see `iterate doctor`)."
        ),
    )
    dimension_sets = merge_dimension_sets(existing_dimension_sets, suggest_dimension_sets(scan))
    git_cfg = existing_config.get("git")
    git_cfg = git_cfg if isinstance(git_cfg, dict) else {}
    review_cfg = existing_config.get("review")
    review_cfg = review_cfg if isinstance(review_cfg, dict) else {}
    target_branch = git_cfg.get("target_branch", DEFAULT_TARGET_BRANCH)
    # Schema-enum normalisation (mirrors wizard._load_existing_onboarding_data):
    # a hand-edited `target_branch:` (null), `review.scope: everything`,
    # `push_per_round: "yes"` or non-string dimension entries would otherwise
    # be written back verbatim by the refresh rebuild, persisting an invalid
    # config that doctor keeps flagging on every run.
    if not isinstance(target_branch, str) or not target_branch.strip():
        target_branch = DEFAULT_TARGET_BRANCH
    review_scope = review_cfg.get("scope", DEFAULT_REVIEW_SCOPE)
    if review_scope not in ("changed-only", "full"):
        review_scope = DEFAULT_REVIEW_SCOPE
    # Secure-by-default: push_per_round must default to False, matching
    # OnboardingData (generator.py) and the documented default. A hand-edited
    # non-bool (``"yes"``, 1) is coerced: any non-empty truthy scalar except
    # the canonical ``false``/``"false"`` forms would otherwise round-trip as
    # an invalid value; treat only real bools as authoritative.
    push_per_round = git_cfg.get("push_per_round", False)
    if not isinstance(push_per_round, bool):
        # Keep parity with the wizard's _TRUE_STRINGS: `on` loaded as True
        # there but was rewritten to False here.
        push_per_round = str(push_per_round).strip().lower() in (
            "1", "true", "yes", "on"
        )
    # Preserve the two git booleans refresh does not reconcile, with the same
    # truthy-scalar coercion as push_per_round. Previously they were left at
    # their OnboardingData defaults (False) on the refresh path — a dead field
    # that would clobber a user's ``use_worktree: true`` if any consumer ever
    # read them, and that made the data model disagree with the config it was
    # derived from.
    use_worktree = _coerce_bool(git_cfg.get("use_worktree", False))
    auto_merge = _coerce_bool(git_cfg.get("auto_merge", False))
    validation_commands, effective_whitelist = _resolve_validation_config(
        existing_config, scan
    )
    language = existing_config.get("language", DEFAULT_LANGUAGE)
    if language not in ("zh", "en"):
        language = DEFAULT_LANGUAGE

    # NOTE: the raw ``personalization`` block is preserved verbatim by
    # _build_refreshed_config, and generate_refreshed_md splices the existing
    # ITERATE.md user-owned section back in unchanged. Loading it into
    # OnboardingData here would therefore be dead work -- and worse, the loader
    # emits "malformed ... will not be preserved" warnings that are false for
    # refresh (refresh *does* preserve the raw dict). Deliberately not loaded.

    # Capture fresh fingerprints, honouring drift-ignore patterns.
    ignore_patterns = get_drift_ignore(existing_config)
    # Reuse the stored digest when a manifest exists but is transiently
    # unreadable, so refresh does not permanently erase its baseline.
    fingerprints = capture_fingerprints(
        project_root,
        ignore_patterns,
        fallback_fingerprints=get_stored_fingerprints(existing_config),
    )

    channel, project_description, code_conventions = _preserve_onboarding_meta(
        existing_config
    )
    reviewer = _preserve_reviewer_tuning(existing_config)
    reasoning_effort = normalize_reasoning_effort(
        existing_config.get("reasoning_effort")
    )

    return OnboardingData(
        project_root=project_root,
        channel=channel,
        scan=scan,
        project_description=project_description,
        code_conventions=code_conventions,
        dimensions=dimensions,
        dimension_sets=dimension_sets,
        target_branch=target_branch,
        review_scope=review_scope,
        use_worktree=use_worktree,
        auto_merge=auto_merge,
        push_per_round=push_per_round,
        validation_commands=validation_commands,
        command_whitelist=effective_whitelist,
        fingerprints=fingerprints,
        language=language,
        reasoning_effort=reasoning_effort,
        output_schema_validation=reviewer["output_schema_validation"],
        evidence_validation=reviewer["evidence_validation"],
        coverage_validation=reviewer["coverage_validation"],
        scope_chunk_size=reviewer["scope_chunk_size"],
        drift_ignore=ignore_patterns,
    )
