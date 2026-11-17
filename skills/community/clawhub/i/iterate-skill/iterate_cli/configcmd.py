"""Non-interactive config inspection and editing (``iterate config``).

``iterate config`` fills the gap left by the interactive wizard: after
onboarding, users can read and modify individual config values without
hand-editing ``iterate.config.yaml`` or re-running the interactive wizard.

Commands:
- ``iterate config``            — print the resolved config (TUI).
- ``iterate config get [key]``  — print one resolved value (or all).
- ``iterate config set k v``    — validate and write a single value
                                  (with a timestamped backup).

Only the flat keys ``iterate show`` reports are settable; the complex
sections (``validation``, ``personalization``, ``onboarding``) are managed
through their dedicated flows and intentionally out of scope here.
"""

from __future__ import annotations

import json
import shutil
import sys
from collections.abc import Callable
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from uuid import uuid4

import yaml

from iterate_cli.doctor import (
    CANONICAL_DIMENSIONS,
    MAX_ROUNDS_MAX,
    MAX_ROUNDS_MIN,
    SUPPORTED_LANGUAGES,
    SUPPORTED_SCOPES,
)
from iterate_cli.generator import (
    REASONING_EFFORT_VALUES,
    atomic_write,
)
from iterate_cli.refresh import CONFIG_YAML, load_onboarding_config
from iterate_cli.tui import tui


class ConfigValueError(ValueError):
    """Raised when a ``config set`` value fails validation."""


#: Sentinel returned by ``_read`` when an intermediate section (a segment of
#: ``spec.path``) exists but is not a mapping — e.g. ``git: legacy`` makes
#: ``git.use_worktree`` unreadable. Distinct from ``None`` (missing key).
_MALFORMED = object()


@dataclass(frozen=True)
class ConfigKeySpec:
    """Schema for a settable flat config key.

    Attributes:
        name: The flat key name (matches ``iterate show`` output).
        validator: Parses + validates the raw CLI value; returns the parsed
            value or raises :class:`ConfigValueError`.
        path: Nested dict path to write to (``()`` = top-level key).
    """

    name: str
    validator: Callable[[str], Any]
    path: tuple[str, ...]


def _parse_non_empty_string(raw: str) -> str:
    """Validate a non-empty trimmed string."""
    value = raw.strip()
    if not value:
        raise ConfigValueError("value must be a non-empty string.")
    return value


def _parse_int(min_value: int, max_value: int | None) -> Callable[[str], int]:
    """Build a validator for an integer within ``[min_value, max_value]``."""

    def _validate(raw: str) -> int:
        try:
            value = int(raw.strip())
        except ValueError as exc:
            raise ConfigValueError(f"value must be an integer, got {raw!r}.") from exc
        if value < min_value:
            raise ConfigValueError(f"value must be >= {min_value}.")
        if max_value is not None and value > max_value:
            raise ConfigValueError(f"value must be <= {max_value}.")
        return value

    return _validate


def _parse_bool(raw: str) -> bool:
    """Validate a boolean-like value (true/false/yes/no/1/0)."""
    normalized = raw.strip().lower()
    if normalized in ("true", "yes", "1"):
        return True
    if normalized in ("false", "no", "0"):
        return False
    raise ConfigValueError(
        f"value must be a boolean (true/false/yes/no/1/0), got {raw!r}."
    )


def _parse_reasoning_effort(raw: str) -> str | None:
    """Validate reasoning_effort; empty/'default' maps to provider default."""
    normalized = raw.strip().lower()
    if not normalized or normalized == "default":
        return None
    if normalized in REASONING_EFFORT_VALUES:
        return normalized
    raise ConfigValueError(
        "value must be low, medium or high (or 'default' for provider default), "
        f"got {raw!r}."
    )


def _parse_dimensions(raw: str) -> list[str]:
    """Validate a comma-separated dimension list (non-empty, unique, canonical)."""
    parts = [p.strip() for p in raw.split(",") if p.strip()]
    if not parts:
        raise ConfigValueError("value must contain at least one dimension.")
    seen: set[str] = set()
    result: list[str] = []
    for part in parts:
        if part not in CANONICAL_DIMENSIONS:
            raise ConfigValueError(
                f"unknown dimension {part!r}; valid: {', '.join(CANONICAL_DIMENSIONS)}."
            )
        if part not in seen:
            seen.add(part)
            result.append(part)
    return result


def _parse_enum(valid: frozenset[str]) -> Callable[[str], str]:
    """Build a validator for an enum of strings."""

    def _validate(raw: str) -> str:
        value = raw.strip().lower()
        if value not in valid:
            raise ConfigValueError(
                f"value must be one of {', '.join(sorted(valid))}, got {raw!r}."
            )
        return value

    return _validate


#: Flat keys settable via ``iterate config set``, mirroring ``iterate show``.
SETTABLE_KEYS: dict[str, ConfigKeySpec] = {
    "goal": ConfigKeySpec("goal", _parse_non_empty_string, ()),
    "max_rounds": ConfigKeySpec(
        "max_rounds", _parse_int(MAX_ROUNDS_MIN, MAX_ROUNDS_MAX), ()
    ),
    "reasoning_effort": ConfigKeySpec(
        "reasoning_effort", _parse_reasoning_effort, ()
    ),
    "language": ConfigKeySpec(
        "language", _parse_enum(frozenset(SUPPORTED_LANGUAGES)), ()
    ),
    "mode": ConfigKeySpec(
        "mode", _parse_enum(frozenset({"iterate", "defensive"})), ()
    ),
    "dimensions": ConfigKeySpec("dimensions", _parse_dimensions, ()),
    "atomic_max_lines": ConfigKeySpec(
        "atomic_max_lines", _parse_int(1, None), ("atomic", "max_lines")
    ),
    "atomic_max_adjacent_methods": ConfigKeySpec(
        "atomic_max_adjacent_methods",
        _parse_int(1, None),
        ("atomic", "max_adjacent_methods"),
    ),
    "use_worktree": ConfigKeySpec(
        "use_worktree", _parse_bool, ("git", "use_worktree")
    ),
    "auto_merge": ConfigKeySpec("auto_merge", _parse_bool, ("git", "auto_merge")),
    "target_branch": ConfigKeySpec(
        "target_branch", _parse_non_empty_string, ("git", "target_branch")
    ),
    "push_per_round": ConfigKeySpec(
        "push_per_round", _parse_bool, ("git", "push_per_round")
    ),
    "review_scope": ConfigKeySpec(
        "review_scope", _parse_enum(frozenset(SUPPORTED_SCOPES)), ("review", "scope")
    ),
    "output_schema_validation": ConfigKeySpec(
        "output_schema_validation",
        _parse_bool,
        ("reviewer", "output_schema_validation"),
    ),
    "evidence_validation": ConfigKeySpec(
        "evidence_validation", _parse_bool, ("reviewer", "evidence_validation")
    ),
    "coverage_validation": ConfigKeySpec(
        "coverage_validation", _parse_bool, ("reviewer", "coverage_validation")
    ),
    "scope_chunk_size": ConfigKeySpec(
        "scope_chunk_size", _parse_int(1, None), ("reviewer", "scope_chunk_size")
    ),
}


def _resolved_config(project_root: Path) -> dict[str, Any] | None:
    """Load the project config, or None when unreadable/missing."""
    return load_onboarding_config(project_root)


def _format_value(value: Any) -> str:
    """Render a config value for display; None renders as 'default'."""
    if value is None:
        return "default"
    if isinstance(value, bool):
        return "yes" if value else "no"
    if isinstance(value, list):
        return ", ".join(str(v) for v in value)
    return str(value)


def _resolve_key(key: str) -> ConfigKeySpec | None:
    """Resolve a key to its ConfigKeySpec, supporting dotted-path aliases.

    ``iterate config set git.use_worktree true`` is equivalent to
    ``iterate config set use_worktree true``: each nested settable key also
    accepts its ``".".join(path)`` form (B5), matching the section paths used
    by ``iterate show`` and hand-edited configs.

    Args:
        key: Flat key name, or a dotted section path like ``atomic.max_lines``.

    Returns:
        The matching ConfigKeySpec, or None when the key is unknown.
    """
    spec = SETTABLE_KEYS.get(key)
    if spec is not None:
        return spec
    for candidate in SETTABLE_KEYS.values():
        if candidate.path and ".".join(candidate.path) == key:
            return candidate
    return None


def run_config_get(
    project_root: Path, key: str | None, json_output: bool = False
) -> int:
    """Print one resolved config value (or all) to stdout.

    Args:
        project_root: Project root directory.
        key: Flat key to print; when None, prints every settable key.
        json_output: When True, emit a structured JSON object (single ``{[key]:
            value}``, or all keys) instead of TUI-formatted lines — matching
            the ``iterate status/show/doctor --json`` contract for scripts/CI.

    Returns:
        Exit code: 0 on success, 1 when the config is missing or the key is
        unknown.
    """
    config = _resolved_config(project_root)
    if config is None:
        # `--json` promises "stdout is one JSON object", so a precondition
        # failure must be expressed as {"error": ...} on stdout. Emitting
        # nothing left scripts reading `config get KEY --json` with an empty
        # body and a bare exit code, while the malformed-section failure in the
        # very same function *did* emit a JSON error — two contracts for one
        # command.
        # Distinguish missing from corrupt: `onboard` refuses to overwrite an
        # existing-but-unparseable config, so telling the user to run it was a
        # dead end. Corrupt configs need `doctor` (which can fix/back up).
        if (project_root / "iterate.config.yaml").is_file():
            message = (
                "iterate.config.yaml exists but could not be parsed. Run "
                "'iterate doctor' to diagnose it (add --fix to repair safely)."
            )
        else:
            message = (
                "iterate.config.yaml is missing. Run 'iterate onboard' "
                "(interactive) or 'iterate init --yes' (prompt-free) first."
            )
        if json_output:
            print(json.dumps({"error": message}, ensure_ascii=False))
        else:
            tui.error(message)
        return 1

    def _read(spec: ConfigKeySpec) -> Any:
        if not spec.path:
            return config.get(spec.name)
        section: Any = config
        for part in spec.path:
            if not isinstance(section, dict):
                return _MALFORMED
            if part not in section:
                return None
            section = section[part]
        return section

    if key is not None:
        spec = _resolve_key(key)
        if spec is None:
            message = f"Unknown config key {key!r}. Use `iterate config` to list keys."
            if json_output:
                print(json.dumps({"error": message}, ensure_ascii=False))
            else:
                tui.error(message)
            return 1
        value = _read(spec)
        if value is _MALFORMED:
            # Reporting "default" here would hide a hand-edited non-mapping
            # intermediate section; surface it so the operator fixes the file.
            if json_output:
                print(
                    json.dumps(
                        {
                            "error": f"intermediate section for {key!r} is "
                            f"not a mapping in {CONFIG_YAML}"
                        },
                        ensure_ascii=False,
                    )
                )
            else:
                tui.error(
                    f"Cannot read {key!r}: an intermediate section in "
                    f"{CONFIG_YAML} is not a mapping. Fix the file manually, "
                    "then retry."
                )
            return 1
        if json_output:
            # Key always the canonical flat name, even when the user typed
            # the dotted alias, so JSON consumers can map it back reliably.
            # ``default=str`` is required, not cosmetic: PyYAML resolves an
            # unquoted ISO date (``goal: 2024-06-01``) to a datetime.date,
            # which json.dumps cannot encode. ``--json`` promises a parseable
            # object, so a date-typed scalar must serialize, not traceback.
            print(json.dumps({spec.name: value}, ensure_ascii=False, default=str))
        else:
            print(_format_value(value))
        return 0

    # All-keys summary: refuse when any target intermediate section is
    # malformed, so a broken hand-edited config is never silently reported as
    # "default" for the affected keys.
    malformed = [
        name
        for name, spec in SETTABLE_KEYS.items()
        if _read(spec) is _MALFORMED
    ]
    if malformed:
        if json_output:
            print(
                json.dumps(
                    {
                        "error": f"intermediate section(s) not a mapping in "
                        f"{CONFIG_YAML}: {', '.join(sorted(malformed))}"
                    },
                    ensure_ascii=False,
                )
            )
        else:
            tui.error(
                f"Cannot resolve {'/'.join(sorted(malformed))} in {CONFIG_YAML}: "
                "an intermediate section is not a mapping. Fix the file manually, "
                "then retry."
            )
        return 1

    if json_output:
        print(
            json.dumps(
                {name: _read(spec) for name, spec in SETTABLE_KEYS.items()},
                ensure_ascii=False,
                default=str,
            )
        )
        return 0

    for name, spec in SETTABLE_KEYS.items():
        tui.key_value(name.replace("_", " ").title(), _format_value(_read(spec)))
    return 0


def run_config_set(
    project_root: Path, key: str, raw_value: str, json_output: bool = False
) -> int:
    """Validate and write a single config value (with a timestamped backup).

    Refuses to modify a corrupt/missing config so a damaged file is never
    silently overwritten.

    Args:
        project_root: Project root directory.
        key: Flat config key to set.
        raw_value: Raw CLI value to parse and validate.
        json_output: When True, emit a JSON confirmation object instead of TUI
            lines. Errors are still reported on stderr with a non-zero code.

    Returns:
        Exit code: 0 on success, 1 on unknown key / invalid value / write
        failure. With ``json_output``, failures additionally emit
        ``{"error": ...}`` on stdout so the one-JSON-document contract holds.
    """
    spec = _resolve_key(key)
    if spec is None:
        return _set_error(
            f"Unknown config key {key!r}. Settable keys: {', '.join(SETTABLE_KEYS)}.",
            json_output,
        )

    try:
        parsed = spec.validator(raw_value)
    except ConfigValueError as exc:
        return _set_error(f"Invalid value for {key!r}: {exc}", json_output)

    config_path = project_root / CONFIG_YAML
    if not config_path.is_file():
        return _set_error(
            "iterate.config.yaml not found. Run 'iterate onboard' first.",
            json_output,
        )

    # Single read/parse so the "is this a mapping?" check and the merge use
    # the exact same snapshot. load_config_strict collapses a malformed
    # top-level (list/scalar) to {}, which would make the write below quietly
    # clobber the operator's non-mapping YAML — refuse instead.
    try:
        raw_text = config_path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        return _set_error(f"Cannot read {CONFIG_YAML}: {exc}", json_output)
    try:
        parsed_doc = yaml.safe_load(raw_text)
    except yaml.YAMLError as exc:
        return _set_error(
            f"{CONFIG_YAML} is not valid YAML; refusing to write over it: {exc}",
            json_output,
        )
    if parsed_doc is None:
        config: dict[str, Any] = {}
    elif isinstance(parsed_doc, dict):
        config = parsed_doc
    else:
        return _set_error(
            f"{CONFIG_YAML} top-level must be a mapping (dict), got "
            f"{type(parsed_doc).__name__}. Refusing to overwrite non-mapping "
            "content; fix the file manually, then retry.",
            json_output,
        )

    section: Any = config
    for part in spec.path[:-1]:
        existing_part = section.get(part)
        if existing_part is None:
            section[part] = {}
        elif not isinstance(existing_part, dict):
            # A hand-edited scalar/list at an intermediate path segment (e.g.
            # `git: legacy`) would be silently clobbered to {} if we replaced
            # it here. Refuse instead so the operator fixes the file manually.
            return _set_error(
                f"Cannot set {key!r}: intermediate field {part!r} is "
                f"{type(existing_part).__name__}, not a mapping. Fix "
                f"{CONFIG_YAML} manually, then retry.",
                json_output,
            )
        section = section[part]
    if spec.path:
        section[spec.path[-1]] = parsed
    else:
        config[spec.name] = parsed

    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    salt = uuid4().hex[:6]
    backup_path = config_path.with_name(f"{CONFIG_YAML}.configset-{timestamp}-{salt}")
    # safe_dump can raise yaml.YAMLError (e.g. RepresenterError) when the
    # hand-edited config holds an unserialisable value; surface it cleanly
    # instead of a traceback and keep the backup for manual recovery.
    try:
        config_yaml = yaml.safe_dump(
            config, default_flow_style=False, allow_unicode=True, sort_keys=False
        )
    except yaml.YAMLError as exc:
        return _set_error(f"Cannot serialise {CONFIG_YAML}: {exc}", json_output)
    try:
        shutil.copy2(config_path, backup_path)
        atomic_write(config_path, config_yaml)
    except OSError as exc:
        return _set_error(f"Failed to write {CONFIG_YAML}: {exc}", json_output)

    # Round-tripping through safe_dump CANNOT preserve hand-written YAML
    # comments/anchors/formatting — they are silently erased on every
    # successful set (the backup keeps them). Say so instead of letting the
    # operator discover it in a diff.
    if _config_has_comments(raw_text):
        tui.warning(
            "Note: YAML comments in iterate.config.yaml are NOT preserved by "
            "`config set` (a full rewrite); see the timestamped backup."
        )

    if json_output:
        # Keep stdout clean for scripts/CI: only the JSON confirmation object.
        # Echo the CANONICAL spec.name (like `config get` does) — echoing the
        # raw input meant `config set git.use_worktree true` and
        # `config get use_worktree` reported two different keys for one field.
        print(json.dumps({"key": spec.name, "value": parsed}, ensure_ascii=False, default=str))
        return 0
    tui.success(f"{key} set to {_format_value(parsed)}.")
    tui.hint(f"Backup written to {backup_path.name}.", indent=2)
    return 0


def _set_error(message: str, json_output: bool) -> int:
    """Emit a ``config set``/``config unset`` failure honouring ``--json``.

    The global ``--json`` help promises "stdout holds exactly one JSON
    document, including on failure"; every failure branch of
    ``run_config_set`` used to write ONLY to stderr, so
    ``iterate config set ... --json`` yielded an empty stdout body plus a bare
    exit code — while ``config get``'s failure paths in this same module DID
    emit ``{"error": ...}``. Two contracts for one command; this unifies them.
    """
    if json_output:
        print(json.dumps({"error": message}, ensure_ascii=False))
    tui.error(message)
    return 1


def _config_has_comments(text: str) -> bool:
    """True when ``text`` contains at least one YAML comment line.

    Best-effort (a ``#`` inside a quoted scalar also matches) — the warning is
    advisory, never blocking.
    """
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("#") or " #" in stripped:
            return True
    return False


def run_config_unset(
    project_root: Path, key: str, json_output: bool = False
) -> int:
    """Remove a config key so it falls back to its documented default.

    The inverse of ``run_config_set``: ``config get`` renders an absent key as
    ``default``, but until now there was no way to RETURN a key to that state
    (set only accepted non-empty values), so a mistyped value could never be
    un-set short of hand-editing the YAML.

    Removes the leaf key, then prunes any ancestor section (e.g. ``git``) left
    empty by the removal. A timestamped backup is taken first, exactly like
    ``config set``.

    Args:
        project_root: Project root directory.
        key: Flat config key (or dotted alias) to remove.
        json_output: When True, emit a JSON confirmation instead of TUI lines.

    Returns:
        Exit code: 0 on success, 1 on unknown key / missing or corrupt config /
        intermediate non-mapping / key not present.
    """
    spec = _resolve_key(key)
    if spec is None:
        return _set_error(
            f"Unknown config key {key!r}. Settable keys: {', '.join(SETTABLE_KEYS)}.",
            json_output,
        )

    config_path = project_root / CONFIG_YAML
    if not config_path.is_file():
        return _set_error(
            "iterate.config.yaml not found. Run 'iterate onboard' first.",
            json_output,
        )
    try:
        raw_text = config_path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        return _set_error(f"Cannot read {CONFIG_YAML}: {exc}", json_output)
    try:
        parsed_doc = yaml.safe_load(raw_text)
    except yaml.YAMLError as exc:
        return _set_error(
            f"{CONFIG_YAML} is not valid YAML; refusing to write over it: {exc}",
            json_output,
        )
    if parsed_doc is None:
        parsed_doc = {}
    if not isinstance(parsed_doc, dict):
        return _set_error(
            f"{CONFIG_YAML} top-level must be a mapping (dict), got "
            f"{type(parsed_doc).__name__}. Refusing to overwrite non-mapping "
            "content; fix the file manually, then retry.",
            json_output,
        )
    config: dict[str, Any] = parsed_doc

    # Walk to the parent mapping, refusing a non-mapping intermediate the same
    # way run_config_set does (removing through it would corrupt the file).
    parent: Any = config
    for part in spec.path[:-1]:
        if not isinstance(parent, dict) or part not in parent:
            # Absent section ≠ broken section: `git:` missing entirely means
            # the key is simply unset, but the old flow reported "intermediate
            # field 'git' is not a mapping" — blaming a type error that does
            # not exist and sending the operator to hand-edit a healthy file.
            return _set_error(
                f"{key!r} is not set in {CONFIG_YAML} (section {part!r} is "
                "absent; nothing to unset).",
                json_output,
            )
        parent = parent[part]
        if not isinstance(parent, dict):
            return _set_error(
                f"Cannot unset {key!r}: intermediate field {part!r} is not a "
                f"mapping. Fix {CONFIG_YAML} manually, then retry.",
                json_output,
            )
    target: dict[str, Any] = parent if spec.path else config
    leaf = spec.path[-1] if spec.path else spec.name
    if leaf not in target:
        return _set_error(
            f"{key!r} is not set in {CONFIG_YAML} (nothing to unset).",
            json_output,
        )
    removed_value = target.pop(leaf)

    # Prune ancestor sections left empty by the removal so unset does not
    # leave `git: {}` litter behind. The default applies either way, but a
    # clean file is what "unset" promises.
    if spec.path:
        chain: list[tuple[dict[str, Any], str]] = []
        cursor: dict[str, Any] = config
        for part in spec.path[:-1]:
            chain.append((cursor, part))
            nxt = cursor.get(part)
            if not isinstance(nxt, dict):
                break
            cursor = nxt
        for ancestor, part in reversed(chain):
            child = ancestor.get(part)
            if isinstance(child, dict) and not child:
                del ancestor[part]

    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    salt = uuid4().hex[:6]
    backup_path = config_path.with_name(f"{CONFIG_YAML}.configunset-{timestamp}-{salt}")
    try:
        config_yaml = yaml.safe_dump(
            config, default_flow_style=False, allow_unicode=True, sort_keys=False
        )
    except yaml.YAMLError as exc:
        return _set_error(f"Cannot serialise {CONFIG_YAML}: {exc}", json_output)
    try:
        shutil.copy2(config_path, backup_path)
        atomic_write(config_path, config_yaml)
    except OSError as exc:
        return _set_error(f"Failed to write {CONFIG_YAML}: {exc}", json_output)

    if _config_has_comments(raw_text):
        tui.warning(
            "Note: YAML comments in iterate.config.yaml are NOT preserved by "
            "`config unset` (a full rewrite); see the timestamped backup."
        )

    if json_output:
        print(
            json.dumps(
                {
                    "key": spec.name,
                    "removed": True,
                    "previous_value": removed_value,
                    # `null` (not the string "default") so the JSON value
                    # matches what `config get KEY --json` reports for the same
                    # state — that also emits the key's raw value, which is
                    # `null` once the key is absent. TUI renders it as "default".
                    "value": None,
                },
                ensure_ascii=False,
                default=str,
            )
        )
        return 0
    tui.success(f"{key} unset — now falls back to its default.")
    tui.hint(f"Backup written to {backup_path.name}.", indent=2)
    return 0


# ---------------------------------------------------------------------------
# `iterate config schema` — emit the canonical JSON Schema for tooling
# ---------------------------------------------------------------------------

#: The canonical schema file, resolved the same way doctor resolves it: the
#: bundled copy shipped inside the package when present, else the repo copy.
#: Imported lazily (inside the function) so module import never touches the
#: filesystem; doctor resolves both paths at import time already.
def _schema_path() -> Path:
    from iterate_cli.doctor import SCHEMA_PATH

    return SCHEMA_PATH


def run_config_schema(
    *,
    out: str | None = None,
    compact: bool = False,
    force: bool = False,
) -> int:
    """Emit the canonical JSON Schema for ``iterate.config.yaml``.

    The schema is the single source of truth ``doctor`` (and ``scripts/
    validate.py``) validate a project's config against. Emitting it as a
    machine-readable document lets editors (yaml-language-server ``$schema``),
    CI validators and other tooling enforce exactly the same contract the CLI
    itself enforces, instead of duplicating the rules by hand.

    Args:
        out: Optional path to write the schema to (stdout when omitted).
        compact: When True, emit single-line JSON instead of pretty-printed.
        force: When True, overwrite an existing ``out`` file (refused by
            default, matching ``report --force`` / ``export --force``).

    Returns:
        Exit code: 0 on success, 1 when the schema file is missing/malformed
        or the ``out`` path cannot be written.
    """
    path = _schema_path()
    if not path.is_file():
        tui.error(f"config schema not found at {path}")
        return 1
    try:
        schema = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        tui.error(f"cannot read config schema at {path}: {exc}")
        return 1
    if not isinstance(schema, dict):
        tui.error("config schema is not a JSON object; refusing to emit it")
        return 1

    payload = (
        json.dumps(schema, ensure_ascii=False, separators=(",", ":"))
        if compact
        else json.dumps(schema, ensure_ascii=False, indent=2)
    ) + "\n"

    if out:
        out_path = Path(out)
        if out_path.exists() and not force:
            tui.error(f"{out_path} already exists (use --force to overwrite)")
            return 1
        try:
            out_path.write_text(payload, encoding="utf-8")
        except OSError as exc:
            tui.error(f"cannot write {out_path}: {exc}")
            return 1
        # Confirmation goes to stderr so stdout stays clean for scripts that
        # only care about the file artifact.
        print(f"Config schema written to {out_path}", file=sys.stderr)
        return 0

    # Schema JSON is the stdout document; emit it verbatim with no decoration.
    sys.stdout.write(payload)
    return 0
