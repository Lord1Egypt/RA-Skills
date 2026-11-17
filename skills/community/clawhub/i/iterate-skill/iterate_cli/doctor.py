"""Project health diagnostics for the iterate skill.

``iterate doctor`` checks a project's iterate.config.yaml, ITERATE.md and
onboarding state against the skill's own canonical definitions so that a
project drifting from the skill's expectations is surfaced early.

Checks performed:
- Onboarding completeness (ITERATE.md + iterate.config.yaml exist).
- Config loads as a YAML mapping and fully matches config/config.schema.json.
- ``dimensions`` reference only canonical dimension ids.
- ``review.scope`` is one of the supported values.
- ``git.target_branch`` is a non-empty string.
- ``validation.commands`` values are non-empty lists of strings.
- ``validation.command_whitelist`` entries are safe and every command is whitelisted.
- ``personalization`` dimension references point at enabled dimensions.
- Onboarding ``skill_version`` vs the installed skill version.
- Manifest drift (tech-stack changed since onboarding).

All checks can be run in a structured (``--json``) or human (TUI) mode.
"""

from __future__ import annotations

import copy
import json
import os
import re
import shutil
import sys
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml

from iterate_cli import __version__ as SKILL_VERSION
from iterate_cli.fingerprint import capture_fingerprints, fingerprints_to_dict
from iterate_cli.generator import (
    REASONING_EFFORT_VALUES,
    USER_END_MARKER,
    USER_START_MARKER,
    atomic_write,
    has_valid_user_owned_markers,
)
from iterate_cli.personalize import FORBIDDEN_COMMAND_CHARS
from iterate_cli.refresh import (
    CONFIG_YAML,
    ITERATE_MD,
    check_onboarding_drift,
    get_drift_ignore,
    is_onboarding_complete,
    load_onboarding_config,
)
from iterate_cli.tui import tui

# Shell-chaining metacharacters that must never appear in a whitelist entry
# or a validation command. This is the SAME canonical set as personalize.py's
# FORBIDDEN_COMMAND_CHARS (kept in sync by tests/test_validate.py) so that a
# command accepted at personalization time is also accepted by doctor, and
# vice-versa.
COMMAND_METACHARS: frozenset[str] = frozenset(FORBIDDEN_COMMAND_CHARS)

# Canonical dimension ids declared in config/dimensions.yaml (the single
# source of truth for the skill). Kept in sync by tests/test_dimension_lock.py.
CANONICAL_DIMENSIONS: tuple[str, ...] = (
    "correctness",
    "security",
    "performance",
    "architecture",
    "style-tests",
    "tech-debt",
    "spec-compliance",
    "frontend-backend",
    "ui-ux",
)

# Supported review.scope values.
SUPPORTED_SCOPES: frozenset[str] = frozenset({"full", "changed-only"})

# Supported output languages (config/schema: language enum).
SUPPORTED_LANGUAGES: frozenset[str] = frozenset({"zh", "en"})

# Bounds enforced by config/config.schema.json for max_rounds.
MAX_ROUNDS_MIN: int = 1
MAX_ROUNDS_MAX: int = 50

# Cap on schema-violation messages reported in a single doctor run, to avoid
# flooding output when a config has many malformed keys.
SCHEMA_MAX_ERRORS: int = 5

# Config schema location: prefer the bundled copy (shipped in the package via
# pyproject package-data), fall back to the repo-relative config/ so running
# from source still works — mirrors TEMPLATE_PATH in generator.py.
_BUNDLED_SCHEMA = Path(__file__).resolve().parent / "data" / "config.schema.json"
_REPO_SCHEMA = Path(__file__).resolve().parent.parent / "config" / "config.schema.json"
SCHEMA_PATH = _BUNDLED_SCHEMA if _BUNDLED_SCHEMA.exists() else _REPO_SCHEMA


@dataclass
class DoctorFinding:
    """A single diagnostic finding."""

    severity: str  # "ok" | "warn" | "error"
    check: str
    message: str
    detail: str = ""


@dataclass
class DoctorReport:
    """Aggregated doctor output for a project."""

    project: str
    findings: list[DoctorFinding] = field(default_factory=list)
    fixes: list[str] = field(default_factory=list)

    def has_errors(self) -> bool:
        return any(f.severity == "error" for f in self.findings)

    def has_warnings(self) -> bool:
        return any(f.severity == "warn" for f in self.findings)

    def to_dict(self, *, strict: bool = False) -> dict[str, Any]:
        """Structured representation for ``--json`` output.

        Args:
            strict: Mirrors ``doctor --strict``, under which warnings also make
                the process exit 1.

        Returns:
            The report payload. ``healthy`` is defined as ``exit code == 0``,
            so it must account for ``--strict``: computing it from
            ``has_errors()`` alone meant a warnings-only report under
            ``--strict`` printed ``"healthy": true`` while the process exited 1,
            so `jq .healthy` and `$?` disagreed about the same run. The raw
            signals are reported alongside it so no information is lost.
        """
        has_errors = self.has_errors()
        has_warnings = self.has_warnings()
        blocking = has_errors or (strict and has_warnings)
        return {
            "project": self.project,
            "skill_version": SKILL_VERSION,
            "healthy": not blocking,
            "blocking": blocking,
            "strict": strict,
            "has_errors": has_errors,
            "has_warnings": has_warnings,
            "fixes": list(self.fixes),
            "findings": [
                {
                    "severity": f.severity,
                    "check": f.check,
                    "message": f.message,
                    "detail": f.detail,
                }
                for f in self.findings
            ],
        }


def _ok(report: DoctorReport, check: str, message: str) -> None:
    report.findings.append(DoctorFinding("ok", check, message))


def _warn(report: DoctorReport, check: str, message: str, detail: str = "") -> None:
    report.findings.append(DoctorFinding("warn", check, message, detail))


def _err(report: DoctorReport, check: str, message: str, detail: str = "") -> None:
    report.findings.append(DoctorFinding("error", check, message, detail))


def _dimension_ids(config: dict[str, Any]) -> list[str]:
    """Return the declared dimensions.

    - ``dimensions`` absent → canonical defaults (schema makes it optional).
    - ``dimensions`` a list → its entries as strings.
    - ``dimensions`` present but NOT a list (e.g. a scalar string from a
      hand-edited config) → ``[]``, so ``_check_dimensions`` reports the
      malformed value as an error instead of silently treating it as "all
      canonical" and declaring the config healthy.
    """
    dims = config.get("dimensions")
    if dims is None:
        return list(CANONICAL_DIMENSIONS)
    if isinstance(dims, list):
        return [str(d) for d in dims]
    return []


def _load_config_schema() -> dict[str, Any] | None:
    """Load the canonical config JSON Schema, or None if unavailable.

    Uses the packaged copy (SCHEMA_PATH) so doctor works both from source
    and inside an installed package. Returns None when the schema file is
    missing or malformed, in which case schema validation is skipped.
    """
    try:
        schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    return schema if isinstance(schema, dict) else None


def _schema_violations(config: dict[str, Any]) -> list[str] | None:
    """Validate ``config`` against the canonical JSON Schema.

    Returns a list of human-readable ``path: message`` violations (empty when
    the config is valid), or ``None`` when schema validation is **unavailable**
    (schema file missing/malformed or ``jsonschema`` not installed) so the
    caller can distinguish "fully matches" from "validation skipped" instead of
    reporting a false success. Mirrors the schema pass in scripts/validate.py.
    """
    schema = _load_config_schema()
    if schema is None:
        return None
    try:
        from jsonschema import Draft202012Validator  # type: ignore[import-untyped]
    except ImportError:
        return None
    violations: list[str] = []
    try:
        validator = Draft202012Validator(schema)
    except ValueError:
        # Schema is structurally invalid (e.g. malformed ``$ref`` / type
        # constraint). Skipping schema validation is safer than crashing the
        # whole doctor run on a broken schema file.
        return None
    for error in validator.iter_errors(config):
        path = "/".join(str(part) for part in error.path) or "<root>"
        violations.append(f"{path}: {error.message}")
    return violations


def _command_is_whitelisted(command: Any, whitelist: Any) -> bool:
    """True when a command equals or is prefixed by a whitelisted entry.

    Mirrors scripts/validate.py::command_is_whitelisted: a command is allowed
    when it equals a whitelisted prefix, or starts with one followed by
    whitespace (so ``pytest tests/`` is ``pytest`` plus an argument). Also
    rejects shell-chaining metacharacters anywhere in the command body, so a
    whitelisted prefix cannot be abused to smuggle ``; rm -rf /`` style
    side effects past the check.
    """
    if not isinstance(command, str) or not isinstance(whitelist, list):
        return False
    stripped = command.strip()
    for ch in stripped:
        if ch in COMMAND_METACHARS:
            return False
    for prefix in whitelist:
        if not isinstance(prefix, str):
            continue
        if stripped == prefix:
            return True
        if (
            len(stripped) > len(prefix)
            and stripped.startswith(prefix)
            and stripped[len(prefix)].isspace()
        ):
            return True
    return False


#: Every check name a doctor run can report, in run order. These are the exact
#: ``check`` values surfaced in ``findings[].check`` under ``--json`` and are
#: what ``iterate doctor --check`` accepts.
DOCTOR_CHECK_NAMES: tuple[str, ...] = (
    "onboarding",
    "config.parse",
    "config.schema",
    "dimensions",
    "max_rounds",
    "reasoning_effort",
    "language",
    "review.scope",
    "git.target_branch",
    "validation.commands",
    "validation.command_whitelist",
    "validation.whitelist",
    "invariants",
    "invariants.commands",
    "invariants.ensure",
    "skill_version",
    "drift",
    "personalization.consistency",
    "dimension_sets",
    "iterate.md.markers",
)

#: Names that can run without a parsed config (the rest need ``config``).
_NON_CONFIG_CHECKS = frozenset({"onboarding", "config.parse", "iterate.md.markers"})

#: Maps each finding name to the ``_check_*`` group that produces it, so a
#: group with several sibling names (e.g. ``validation.whitelist`` also records
#: ``validation.command_whitelist``) runs exactly once.
_GROUP_FOR_FINDING: dict[str, str] = {
    "config.schema": "config_schema",
    "dimensions": "dimensions",
    "max_rounds": "max_rounds",
    "reasoning_effort": "reasoning_effort",
    "language": "language",
    "review.scope": "review_scope",
    "git.target_branch": "git_branch",
    "validation.commands": "validation_commands",
    "validation.command_whitelist": "validation_whitelist",
    "validation.whitelist": "validation_whitelist",
    "invariants": "invariants",
    "invariants.commands": "invariants",
    "invariants.ensure": "invariants",
    "skill_version": "skill_version",
    "drift": "manifest_drift",
    "personalization.consistency": "personalization",
    "dimension_sets": "dimension_sets",
    "iterate.md.markers": "iterate_md_markers",
}


def run_doctor(project_root: Path, checks: set[str] | None = None) -> DoctorReport:
    """Run health checks against ``project_root``.

    Each check is factored into a single-purpose ``_check_*`` function so
    the orchestration stays readable and each check stays under the
    function-length / nesting budget. The two fatal checks (onboarding
    completeness, config parse) short-circuit the run: nothing downstream
    can be validated without a parsed config.

    ``checks``, when given, restricts the run to those named checks (the
    ``check`` values reported in findings; see :data:`DOCTOR_CHECK_NAMES`).
    The preamble checks that a config-dependent check needs (onboarding,
    config parse) still run as silent prerequisites so a blocker is always
    explained, but they only surface their own findings when explicitly
    requested. ``--list-checks`` in the CLI lists ``DOCTOR_CHECK_NAMES``.

    Args:
        project_root: Project root directory.
        checks: Optional set of check names to run (None = all checks).

    Returns:
        A DoctorReport aggregating every finding.

    Raises:
        ValueError: If ``checks`` names a check not in :data:`DOCTOR_CHECK_NAMES`.
    """
    report = DoctorReport(str(project_root))
    if checks is None:
        requested = set(DOCTOR_CHECK_NAMES)
    else:
        requested = set(checks)
        unknown = requested - set(DOCTOR_CHECK_NAMES)
        if unknown:
            raise ValueError(
                "unknown doctor check(s): "
                + ", ".join(sorted(unknown))
                + " (run `iterate doctor --list-checks` for the available checks)"
            )

    config_names = set(DOCTOR_CHECK_NAMES) - _NON_CONFIG_CHECKS
    need_config = bool(requested & config_names)
    wants_config_parse = "config.parse" in requested or need_config

    # Onboarding gates everything in the unfiltered flow. As a prerequisite it
    # runs silently, surfacing only its errors so a missing ITERATE.md is still
    # explained when the operator asked for one config-dependent check.
    if "onboarding" in requested:
        if not _check_onboarding(report, project_root):
            return report
    elif wants_config_parse:
        prereq = DoctorReport(str(project_root))
        if not _check_onboarding(prereq, project_root):
            report.findings.extend(
                f for f in prereq.findings if f.severity != "ok"
            )
            return report

    # Config parse produces the ``config`` every config-dependent check needs.
    config: dict[str, Any] | None = None
    if wants_config_parse:
        if "config.parse" in requested:
            config = _check_config_parse(report, project_root)
        else:
            prereq = DoctorReport(str(project_root))
            config = _check_config_parse(prereq, project_root)
            report.findings.extend(
                f for f in prereq.findings if f.severity != "ok"
            )
        if config is None:
            return report

    run_groups: set[str] = set()
    for name in DOCTOR_CHECK_NAMES:
        if name in ("onboarding", "config.parse"):
            continue
        if name not in requested:
            continue
        group = _GROUP_FOR_FINDING[name]
        if group in run_groups:
            continue  # a sibling finding name maps to the same runner
        run_groups.add(group)
        _run_doctor_check(report, name, project_root, config)

    # A group can report sibling check names (e.g. the validation.whitelist
    # runner also records validation.command_whitelist). Keep only what was
    # requested, plus any error so a blocker is never silently hidden.
    if checks is not None:
        report.findings = [
            f
            for f in report.findings
            if f.check in requested or f.severity == "error"
        ]

    return report


def _run_doctor_check(
    report: DoctorReport,
    name: str,
    project_root: Path,
    config: dict[str, Any] | None,
) -> None:
    """Dispatch a single non-preamble check by its finding name."""
    if name == "iterate.md.markers":
        _check_iterate_md_markers(report, project_root)
        return
    if config is None:
        # A config-dependent check without a parsed config cannot run; the
        # preamble already reported the parse failure and stopped the run.
        return
    if name == "config.schema":
        _check_config_schema(report, config)
    elif name == "dimensions":
        _check_dimensions(report, config)
    elif name == "max_rounds":
        _check_max_rounds(report, config)
    elif name == "reasoning_effort":
        _check_reasoning_effort(report, config)
    elif name == "language":
        _check_language(report, config)
    elif name == "review.scope":
        _check_review_scope(report, config)
    elif name == "git.target_branch":
        _check_git_branch(report, config)
    elif name == "validation.commands":
        _check_validation_commands(report, config)
    elif name in ("validation.command_whitelist", "validation.whitelist"):
        _check_validation_whitelist(report, config)
    elif name in ("invariants", "invariants.commands", "invariants.ensure"):
        _check_invariants(report, config, project_root)
    elif name == "skill_version":
        _check_skill_version(report, config)
    elif name == "drift":
        _check_manifest_drift(report, project_root, config)
    elif name == "personalization.consistency":
        _check_personalization(report, config)
    elif name == "dimension_sets":
        _check_dimension_sets(report, config)


def _check_onboarding(report: DoctorReport, project_root: Path) -> bool:
    """Check onboarding completeness; return False to stop the run."""
    if not is_onboarding_complete(project_root):
        _err(
            report,
            "onboarding",
            "Onboarding is not complete: ITERATE.md is missing.",
            "Run `iterate onboard` to initialize the project.",
        )
        return False
    _ok(report, "onboarding", "ITERATE.md present.")
    return True


def _check_config_parse(
    report: DoctorReport, project_root: Path
) -> dict[str, Any] | None:
    """Load the config as a YAML mapping; return None to stop the run."""
    from iterate_cli.personalize import CorruptConfigError, load_config_strict

    config_path = project_root / CONFIG_YAML
    if not config_path.is_file():
        _err(
            report,
            "config.parse",
            "iterate.config.yaml is missing.",
            "Run `iterate onboard` to initialize the project.",
        )
        return None
    try:
        config = load_config_strict(config_path)
    except CorruptConfigError as exc:
        _err(
            report,
            "config.parse",
            "iterate.config.yaml is corrupt and cannot be parsed.",
            str(exc),
        )
        return None
    except (OSError, UnicodeDecodeError) as exc:
        _err(
            report,
            "config.parse",
            f"iterate.config.yaml is unreadable: {exc}",
        )
        return None
    if not config:
        _err(
            report,
            "config.parse",
            "iterate.config.yaml is empty or not a YAML mapping.",
        )
        return None
    _ok(report, "config.parse", "iterate.config.yaml parsed as a valid YAML mapping.")
    return config


def _check_config_schema(report: DoctorReport, config: dict[str, Any]) -> None:
    """Full config validation against the canonical JSON Schema.

    Surfaced as a warning (not an error) so valid-but-tuned configs that a
    targeted check already flags (e.g. unknown dimension) keep their warn
    severity.
    """
    schema_violations = _schema_violations(config)
    if schema_violations is None:
        # Validation itself is unavailable (missing schema/jsonschema). Report
        # a warning instead of a false "fully matches" success so the operator
        # knows the schema gate did not actually run.
        _warn(
            report,
            "config.schema",
            "Config schema validation could not run (schema file or jsonschema unavailable).",
        )
        return
    if not schema_violations:
        _ok(report, "config.schema", "iterate.config.yaml fully matches the config schema.")
        return
    shown = schema_violations[:SCHEMA_MAX_ERRORS]
    detail = "\n".join(f"  - {violation}" for violation in shown)
    if len(schema_violations) > SCHEMA_MAX_ERRORS:
        detail += f"\n  … and {len(schema_violations) - SCHEMA_MAX_ERRORS} more violation(s)."
    _warn(
        report,
        "config.schema",
        f"iterate.config.yaml does not fully match the schema ({len(schema_violations)} violation(s)).",
        detail,
    )


def _check_dimensions(report: DoctorReport, config: dict[str, Any]) -> None:
    """Dimensions must reference canonical ids, be non-empty and unique."""
    canonical_set = set(CANONICAL_DIMENSIONS)
    dims = _dimension_ids(config)

    raw = config.get("dimensions")
    if raw is not None and not isinstance(raw, list):
        # A scalar/non-list dimensions value (e.g. `dimensions: "correctness"`)
        # is malformed: report it as an error and stop — the per-entry checks
        # below would otherwise be meaningless (and a previous fallback to the
        # canonical list silently reported such configs as "healthy").
        _err(
            report,
            "dimensions",
            "dimensions must be a list of canonical dimension ids.",
            f"Got {type(raw).__name__} instead of a list.",
        )
        return

    # Empty list is a hard error: emit it first and return so we never
    # also report the verbose "all configured dimensions are canonical"
    # success line for the same check (which would contradict it).
    if not dims:
        _err(report, "dimensions", "dimensions must not be an empty list.", "Configure at least one dimension.")
        return

    unknown = [d for d in dims if d not in canonical_set]
    if unknown:
        _warn(
            report,
            "dimensions",
            f"Config references {len(unknown)} unknown dimension(s): {', '.join(sorted(unknown))}.",
            "Unknown dimensions are ignored by reviewers; check config/dimensions.yaml.",
        )
    else:
        _ok(report, "dimensions", f"All {len(dims)} configured dimension(s) are canonical.")

    seen: set[str] = set()
    dups: list[str] = []
    for d in dims:
        if d in seen:
            dups.append(d)
        else:
            seen.add(d)
    if dups:
        _warn(
            report,
            "dimensions",
            f"dimensions contains duplicate(s): {', '.join(sorted(set(dups)))}.",
            "Remove duplicate entries (schema requires uniqueItems).",
        )


def _check_max_rounds(report: DoctorReport, config: dict[str, Any]) -> None:
    """max_rounds must be an integer within [MAX_ROUNDS_MIN, MAX_ROUNDS_MAX]."""
    max_rounds = config.get("max_rounds")
    if max_rounds is None:
        return
    if (
        not isinstance(max_rounds, int)
        or isinstance(max_rounds, bool)
        or not (MAX_ROUNDS_MIN <= max_rounds <= MAX_ROUNDS_MAX)
    ):
        _err(
            report,
            "max_rounds",
            f"max_rounds must be an integer in [{MAX_ROUNDS_MIN}, {MAX_ROUNDS_MAX}], got {max_rounds!r}.",
        )
        return
    _ok(report, "max_rounds", f"max_rounds={max_rounds} is within bounds.")


def _check_reasoning_effort(report: DoctorReport, config: dict[str, Any]) -> None:
    """reasoning_effort must be one of the supported levels (or unset)."""
    reasoning_effort = config.get("reasoning_effort")
    if reasoning_effort is None:
        _ok(report, "reasoning_effort", "reasoning_effort not set (provider default).")
        return
    # isinstance guard first: a hand-edited `reasoning_effort: {a: 1}` /
    # `reasoning_effort: [low]` is UNHASHABLE and used to raise TypeError out
    # of the membership test — doctor, the tool meant to diagnose broken
    # configs, crashed on one. Non-strings fall through to the same error path.
    if not isinstance(reasoning_effort, str) or reasoning_effort not in REASONING_EFFORT_VALUES:
        _err(
            report,
            "reasoning_effort",
            f"reasoning_effort {reasoning_effort!r} is not a supported level.",
            f"Supported: {', '.join(sorted(REASONING_EFFORT_VALUES))}.",
        )
        return
    _ok(
        report,
        "reasoning_effort",
        f"reasoning_effort={reasoning_effort!r} is a supported level.",
    )


def _check_language(report: DoctorReport, config: dict[str, Any]) -> None:
    """language must be one of the supported output languages."""
    language = config.get("language")
    if language is None:
        return
    # isinstance guard first: `language: [zh]` is unhashable and must degrade
    # to the same "not supported" warning instead of a TypeError traceback.
    if not isinstance(language, str) or language not in SUPPORTED_LANGUAGES:
        _warn(
            report,
            "language",
            f"language {language!r} is not supported.",
            f"Supported: {', '.join(sorted(SUPPORTED_LANGUAGES))}.",
        )
        return
    _ok(report, "language", f"language {language!r} is supported.")


def _check_review_scope(report: DoctorReport, config: dict[str, Any]) -> None:
    """review.scope must be one of the supported values."""
    review = config.get("review")
    if review is not None and not isinstance(review, dict):
        _err(
            report,
            "review.scope",
            "review must be a mapping (dict) of review settings.",
            f"Got {type(review).__name__} instead of a mapping.",
        )
        return
    scope = review.get("scope") if review else None
    # isinstance guard first: `review.scope: [full]` is unhashable and must
    # degrade to the same "not supported" warning instead of a TypeError.
    if scope is not None and (not isinstance(scope, str) or scope not in SUPPORTED_SCOPES):
        _warn(
            report,
            "review.scope",
            f"review.scope {scope!r} is not a supported value.",
            f"Supported: {', '.join(sorted(SUPPORTED_SCOPES))}.",
        )
        return
    _ok(report, "review.scope", "review.scope is valid (or defaults to full).")


def _check_git_branch(report: DoctorReport, config: dict[str, Any]) -> None:
    """git.target_branch must be a non-empty string when configured."""
    git_cfg = config.get("git")
    if git_cfg is not None and not isinstance(git_cfg, dict):
        _err(
            report,
            "git.target_branch",
            "git must be a mapping (dict) of git settings.",
            f"Got {type(git_cfg).__name__} instead of a mapping.",
        )
        return
    branch = git_cfg.get("target_branch") if git_cfg else None
    if branch is not None and (not isinstance(branch, str) or not branch.strip()):
        _err(report, "git.target_branch", "git.target_branch must be a non-empty string.")
        return
    _ok(report, "git.target_branch", "git.target_branch is valid (or defaults to main).")


def _check_validation_commands(report: DoctorReport, config: dict[str, Any]) -> None:
    """validation.commands values must be non-empty lists of strings.

    Also cross-checks every command against the same known-safe prefix gate
    ``guard`` enforces at execution time: a metachar-free but arbitrary
    executable (``mytool --check``) passes the structural checks yet is
    refused by ``guard pre-check``/``post-check`` — doctor used to report
    "healthy" while guard deterministically failed, two gates disagreeing
    about one config. And a warn (not error) is emitted when an onboarded
    config declares no commands at all, mirroring guard's fail-closed
    post-check reasoning without flipping healthy for brand-new projects.
    """
    from iterate_cli.guard import _command_is_safe as _command_is_safe_command

    validation = config.get("validation")
    if validation is not None and not isinstance(validation, dict):
        _err(
            report,
            "validation.commands",
            "validation must be a mapping (dict) of validation settings.",
            f"Got {type(validation).__name__} instead of a mapping.",
        )
        return
    commands = validation.get("commands") if validation else None
    if commands is None or commands == {}:
        # run_doctor only reaches this check after onboarding (ITERATE.md)
        # verified AND the config parsed, so this is an onboarded project
        # with no validation commands — exactly the state guard post-check
        # fails closed on. Warn (not error): the config is schema-valid.
        # An explicit empty mapping is the SAME "nothing to verify" state as
        # an absent key and must not be reported as a passing check.
        _warn(
            report,
            "validation.commands",
            "no validation.commands configured — `iterate guard post-check` "
            "would fail closed.",
            "Add validation.commands (or run `iterate onboard`) so the "
            "pre-check/post-check gate has something to verify.",
        )
        return
    if not isinstance(commands, dict):
        _err(
            report,
            "validation.commands",
            "validation.commands must be a mapping of module -> list of commands.",
        )
        return
    invalid: list[str] = []
    unknown_tool: list[str] = []
    for module, cmds in commands.items():
        if isinstance(cmds, list) and cmds and all(isinstance(c, str) and c.strip() for c in cmds):
            # Known-safe gate: report (not silently accept) commands guard
            # will refuse at execution time. guard._command_is_safe is the
            # authoritative check (metachar-free + known-safe tool prefix —
            # it does NOT consult command_whitelist), so mirror it exactly
            # instead of inventing a whitelist fallback that guard lacks.
            # Check EVERY command, not just the first: guard pre/post-check
            # validates each entry, so a module `[pytest, "mytool --check"]`
            # must be flagged here too — checking only cmds[0] let doctor
            # report "healthy" while guard deterministically failed.
            for cmd in cmds:
                if not _command_is_safe_command(cmd):
                    unknown_tool.append(f"{module}: {cmd!r}")
            continue
        # Report every invalid module, not just the first: an operator fixing
        # a multi-module config must see all violations in one run.
        invalid.append(f"{module!r}")
    if invalid:
        _err(
            report,
            "validation.commands",
            "validation.commands entries must be non-empty lists of strings.",
            "Invalid module(s): " + ", ".join(invalid[:SCHEMA_MAX_ERRORS]),
        )
        return
    if unknown_tool:
        _warn(
            report,
            "validation.commands",
            "validation command(s) use a tool guard does not recognise as "
            "known-safe — `iterate guard pre-check` will refuse them. The "
            "optional validation.command_whitelist has NO runtime effect; add "
            "the tool to guard's known-safe prefixes "
            "(ITERATE_EXTRA_SAFE_COMMAND_PREFIXES) instead.",
            "; ".join(unknown_tool[:SCHEMA_MAX_ERRORS]),
        )
        return
    _ok(report, "validation.commands", "validation.commands module lists are valid.")


def _check_validation_whitelist(report: DoctorReport, config: dict[str, Any]) -> None:
    """command_whitelist structure (6b) and command compliance (6c).

    Even when no ``command_whitelist`` is configured, every validation
    command is still checked for shell metacharacters (6c safety net): a
    command like ``pytest; rm -rf /`` must never pass a health gate simply
    because the optional whitelist key is absent.
    """
    validation = config.get("validation") if isinstance(config.get("validation"), dict) else None
    whitelist = validation.get("command_whitelist") if validation else None
    commands = validation.get("commands") if validation else None

    if whitelist is None:
        # No whitelist constraint → structure check is not applicable, but the
        # command metacharacter check below still applies to every configured
        # command.
        if commands is not None and not _check_commands_metachars(report, commands):
            # A metachar error (validation.whitelist) was already recorded
            # above; do not also print a message claiming the commands "were
            # checked" and passed, which would contradict the error.
            return
        # Only claim the commands were checked when they were actually a
        # mapping: a non-dict ``commands`` is malformed (flagged by
        # _check_validation_commands) and nothing was examined here.
        detail = (
            "commands checked for shell metacharacters."
            if isinstance(commands, dict)
            else "no validation commands to check."
        )
        _ok(
            report,
            "validation.command_whitelist",
            f"no command_whitelist configured (optional); {detail}",
        )
        return

    # 6b. command_whitelist must be a non-empty list of unique non-empty strings.
    invalid = not isinstance(whitelist, list) or not whitelist
    if not invalid:
        cleaned = [w for w in whitelist if isinstance(w, str) and w.strip()]
        invalid = len(cleaned) != len(whitelist) or len(set(cleaned)) != len(cleaned)
    if invalid:
        _warn(
            report,
            "validation.command_whitelist",
            "command_whitelist must be a non-empty list of unique non-empty strings.",
        )
        # A malformed whitelist (e.g. a bare string like "make") cannot be used
        # for compliance checking, so fall back to the standalone metacharacter
        # safety net. Otherwise a command like "make; rm -rf /" could pass the
        # health gate merely because a (broken) whitelist key is present —
        # the docstring below promises metacharacters are rejected regardless
        # of any whitelist.
        if commands is not None:
            _check_commands_metachars(report, commands)
        return
    _ok(report, "validation.command_whitelist", "command_whitelist is a valid non-empty list.")

    # 6c. Compliance (prefix matching) only applies when commands are also
    # configured, but the whitelist *entry* character safety net always runs:
    # scripts/validate.py rejects metachar whitelist entries regardless of
    # validation.commands, and a metachar entry is a latent chaining risk the
    # moment commands are added later.
    if commands is not None:
        _check_whitelist_compliance(report, whitelist, commands)
    else:
        _check_whitelist_entry_chars(report, whitelist)


def _check_commands_metachars(report: DoctorReport, commands: Any) -> bool:
    """Every configured validation command must be free of shell metacharacters.

    This is the standalone safety net for configs without a
    ``command_whitelist``: metacharacters that allow command chaining
    (``;`` ``|`` ``&`` ``$`` ...) are rejected regardless of any whitelist,
    so a hand-edited config cannot smuggle side effects into the executable
    validation commands.

    Returns ``True`` when all commands are safe, ``False`` when an error was
    recorded, so callers can avoid emitting a contradictory success line.
    """
    if not isinstance(commands, dict):
        return True
    unsafe: list[str] = []
    for module, cmds in commands.items():
        if not isinstance(cmds, list):
            continue
        for idx, command in enumerate(cmds):
            if isinstance(command, str) and any(
                ch in COMMAND_METACHARS for ch in command
            ):
                unsafe.append(f"{module}[{idx}] {command!r}")
    if unsafe:
        _err(
            report,
            "validation.whitelist",
            "validation command(s) contain shell metacharacters (possible command chaining).",
            "; ".join(unsafe[:SCHEMA_MAX_ERRORS]),
        )
        return False
    return True


def _check_whitelist_entry_chars(report: DoctorReport, whitelist: Any) -> None:
    """Whitelist entries must be free of shell metacharacters (no commands case).

    Runs when ``validation.commands`` is absent. Entry-level safety must not
    depend on commands being configured: ``scripts/validate.py`` rejects
    metachar whitelist entries unconditionally, so a latent chaining risk is
    surfaced now rather than silently waiting for commands to be added.
    """
    if not isinstance(whitelist, list):
        return
    safe_prefix = re.compile(r"^[A-Za-z0-9_. -]+$")
    bad = [
        entry
        for entry in whitelist
        if not (isinstance(entry, str) and safe_prefix.match(entry.strip()))
    ]
    if bad:
        _warn(
            report,
            "validation.whitelist",
            "command_whitelist contains entry(ies) with unsafe shell characters.",
            "Allowed in a whitelist entry: letters, digits, underscore, dash, dot and space.",
        )


def _check_whitelist_compliance(
    report: DoctorReport, whitelist: Any, commands: Any
) -> None:
    """Every configured command must be prefixed by a whitelisted entry, and
    whitelist entries must not contain shell metacharacters."""
    # Structural problems (whitelist not a list, commands not a dict) are
    # reported by the caller/schema as a warning/error; skip to avoid a
    # TypeError/AttributeError crash on malformed-but-non-fatal config.
    if not isinstance(whitelist, list) or not isinstance(commands, dict):
        return
    safe_prefix = re.compile(r"^[A-Za-z0-9_. -]+$")
    # Strip leading/trailing whitespace before both the syntax check and the
    # prefix match: an entry like " pytest " is syntactically valid but would
    # never match a real command, producing misleading "not in whitelist"
    # warnings.
    bad_entries = [
        entry
        for entry in whitelist
        if not (isinstance(entry, str) and safe_prefix.match(entry.strip()))
    ]
    stripped_whitelist = [w.strip() for w in whitelist if isinstance(w, str)]
    if bad_entries:
        _warn(
            report,
            "validation.whitelist",
            "command_whitelist contains entry(ies) with unsafe shell characters.",
            "Allowed in a whitelist entry: letters, digits, underscore, dash, dot and space.",
        )
    non_whitelisted: list[str] = []
    unsafe: list[str] = []
    for module, cmds in commands.items():
        if not isinstance(cmds, list):
            continue
        for idx, command in enumerate(cmds):
            if not isinstance(command, str):
                continue
            # Shell metacharacters are a hard security error regardless of the
            # whitelist (matching the standalone safety net for configs without
            # a command_whitelist). Everything else falls back to prefix
            # compliance, which is a non-blocking warning. The metachar scan
            # runs even when some whitelist entries are themselves unsafe: a
            # bad entry must never disable the command-level safety net.
            if any(ch in COMMAND_METACHARS for ch in command):
                unsafe.append(f"{module}[{idx}] {command!r}")
            elif not _command_is_whitelisted(command, stripped_whitelist):
                non_whitelisted.append(f"{module}[{idx}] {command!r}")
    if unsafe:
        _err(
            report,
            "validation.whitelist",
            "validation command(s) contain shell metacharacters (possible command chaining).",
            "; ".join(unsafe[:SCHEMA_MAX_ERRORS]),
        )
        return
    if non_whitelisted:
        _warn(
            report,
            "validation.whitelist",
            f"{len(non_whitelisted)} configured validation command(s) are not in command_whitelist.",
            "; ".join(non_whitelisted[:SCHEMA_MAX_ERRORS]),
        )
        return
    if not bad_entries:
        _ok(report, "validation.whitelist", "All configured validation commands are whitelisted.")


def _check_skill_version(report: DoctorReport, config: dict[str, Any]) -> None:
    """Onboarding skill_version vs the installed skill version."""
    onboarding = config.get("onboarding") if isinstance(config.get("onboarding"), dict) else None
    recorded_version = onboarding.get("skill_version") if onboarding else None
    if recorded_version is None:
        # No recorded version (e.g. a hand-written config without an onboarding
        # record): nothing to compare, and claiming "matches" would be false.
        _ok(
            report,
            "skill_version",
            "No recorded onboarding skill version; nothing to compare.",
        )
        return
    if recorded_version != SKILL_VERSION:
        _warn(
            report,
            "skill_version",
            f"Onboarded with skill {recorded_version!r}, but current skill is {SKILL_VERSION!r}.",
            "Run `iterate refresh` to update the recorded skill version.",
        )
        return
    _ok(report, "skill_version", f"Skill version {SKILL_VERSION!r} matches onboarding record.")


def _check_manifest_drift(
    report: DoctorReport, project_root: Path, config: dict[str, Any] | None
) -> None:
    """Manifest drift (tech-stack changed since onboarding)."""
    # Reuse the ALREADY-LOADED config instead of re-reading the file here: the
    # previous re-load both wasted a parse and risked computing the drift
    # verdict from a different config revision than the one every other check
    # validated (TOCTOU / non-determinism).
    drift = check_onboarding_drift(project_root, config)
    if drift is None:
        # Explain *why* drift detection did not run (three distinct causes),
        # instead of conflating them in a single ok line.
        reason = "config could not be read"
        if config is not None:
            onboarding = config.get("onboarding")
            onboarding = onboarding if isinstance(onboarding, dict) else {}
            if not onboarding.get("drift_check", True):
                reason = "drift check is disabled (drift_check: false)"
            else:
                stored = onboarding.get("fingerprints") or []
                if not isinstance(stored, list) or not stored:
                    reason = "no fingerprints recorded yet (run `iterate refresh` to capture them)"
                else:
                    reason = "drift check unavailable"
        _ok(report, "drift", f"No drift check applicable ({reason}).")
        return
    if drift.has_drift:
        _warn(report, "drift", f"Manifest drift detected: {drift.summary()}", drift.advice())
        return
    _ok(report, "drift", "No manifest drift detected.")


def _check_personalization(report: DoctorReport, config: dict[str, Any]) -> None:
    """Personalization dimension references must point at enabled dimensions."""
    dims = _dimension_ids(config)
    personalization = config.get("personalization") if isinstance(config.get("personalization"), dict) else None
    if personalization is None or not dims:
        return
    enabled = set(dims)
    broken: list[str] = []
    # Guard against a hand-edited string: iterating it would flag each
    # character as a broken dimension (matching load_personalization_from_config).
    fix_priority = personalization.get("fix_priority_order")
    if isinstance(fix_priority, list):
        for idx, item in enumerate(fix_priority):
            if isinstance(item, str) and item not in enabled:
                broken.append(f"fix_priority_order[{idx}] {item!r}")
    # Guard truthy non-list values (e.g. a hand-edited scalar) so iterating
    # them cannot crash the whole doctor run (matching
    # load_personalization_from_config tolerance).
    raw_dim_focus = personalization.get("dimension_focus") or []
    if not isinstance(raw_dim_focus, list):
        raw_dim_focus = []
    for idx, item in enumerate(raw_dim_focus):
        if not isinstance(item, dict):
            continue
        dimension = item.get("dimension")
        # Missing/empty dimension entries are skipped (matching
        # scripts/validate.py::validate_personalization_consistency) so a
        # hand-edited config with an incomplete entry is not misreported as
        # "points to disabled dimension None". A non-string dimension (list /
        # dict) must ALSO be skipped: `x not in enabled` raises TypeError on an
        # unhashable value, crashing the very command meant to diagnose a
        # broken config.
        if isinstance(dimension, str) and dimension and dimension not in enabled:
            broken.append(f"dimension_focus[{idx}] {dimension!r}")
    raw_known = personalization.get("known_intentional") or []
    if not isinstance(raw_known, list):
        raw_known = []
    for idx, item in enumerate(raw_known):
        if not isinstance(item, dict):
            continue
        dimension = item.get("dimension")
        if isinstance(dimension, str) and dimension and dimension not in enabled:
            broken.append(f"known_intentional[{idx}] {dimension!r}")
    if broken:
        _warn(
            report,
            "personalization.consistency",
            f"{len(broken)} personalization reference(s) point to disabled dimensions.",
            "; ".join(broken[:SCHEMA_MAX_ERRORS]),
        )
        return
    _ok(report, "personalization.consistency", "personalization dimension references are consistent.")


def _check_dimension_sets(report: DoctorReport, config: dict[str, Any]) -> None:
    """dimension_sets must be well-formed and internally consistent.

    Each named set must carry a non-empty, unique ``dimensions`` list whose
    entries are canonical ids; ``focus`` overrides must only reference
    dimensions actually present in that set. Dimension sets are optional, so
    an absent ``dimension_sets`` is healthy.
    """
    raw = config.get("dimension_sets")
    if raw is None:
        _ok(report, "dimension_sets", "No dimension_sets configured (defaults to global dimensions).")
        return
    if not isinstance(raw, dict):
        _err(
            report,
            "dimension_sets",
            "dimension_sets must be a mapping of scope name to set spec.",
            f"Got {type(raw).__name__} instead.",
        )
        return
    if not raw:
        # An explicit-empty mapping is semantically identical to an absent key
        # (both mean "no sets configured"). Other falsy values (``[]``, ``""``,
        # ``0``) are *not*: they are the wrong type and must be reported, so
        # only ``None`` and ``{}`` take this success path.
        _ok(report, "dimension_sets", "No dimension_sets configured (defaults to global dimensions).")
        return

    canonical_set = set(CANONICAL_DIMENSIONS)
    name_re = re.compile(r"^[A-Za-z0-9_.-]+$")
    problems: list[str] = []
    for name, spec in raw.items():
        # YAML allows non-string keys; the regex `match` would raise TypeError
        # on an int key, turning the diagnostic into a traceback. Normalize to
        # str for analysis (reporting the original key in the message).
        if not isinstance(name, str) or not name_re.match(str(name)):
            problems.append(f"set name {name!r} has invalid characters")
            continue
        if not isinstance(spec, dict):
            problems.append(f"{name}: spec is not a mapping")
            continue
        dims = spec.get("dimensions")
        if not isinstance(dims, list) or not dims:
            problems.append(f"{name}: dimensions must be a non-empty list")
            dims = []
        # Coerce entries to str before membership/sorting: a hand-edited config
        # mixing ints and strings would otherwise make sorted() raise TypeError.
        unknown = [d for d in dims if str(d) not in canonical_set]
        if unknown:
            problems.append(f"{name}: unknown dimension(s): {', '.join(sorted(set(map(str, unknown))))}")
        seen: set[str] = set()
        for d in dims:
            # A hand-edited config may hold non-string (even unhashable, e.g.
            # nested list) entries; coerce to str so ``in`` can never raise
            # TypeError on an unhashable value (mirrors the ``unknown`` pass
            # above, which already normalises with str()).
            key = str(d)
            if key in seen:
                problems.append(f"{name}: duplicate dimension {d!r}")
            seen.add(key)
        focus = spec.get("focus")
        if focus is not None:
            if not isinstance(focus, dict):
                problems.append(f"{name}: focus must be a mapping")
            else:
                for dim in focus:
                    # Coerce to str before the set membership test: a
                    # hand-edited config can put an unhashable YAML key (a
                    # sequence) under focus, and `dim not in seen` on a list
                    # would raise TypeError instead of a clean finding.
                    if str(dim) not in seen:
                        problems.append(f"{name}: focus[{dim!r}] not in this set's dimensions")

    if problems:
        _warn(
            report,
            "dimension_sets",
            f"{len(problems)} dimension_sets consistency issue(s).",
            "\n".join(f"  - {p}" for p in problems[:SCHEMA_MAX_ERRORS]),
        )
        return
    _ok(
        report,
        "dimension_sets",
        f"All {len(raw)} dimension_set(s) are well-formed and internally consistent.",
    )


def _ensure_path_escapes(root: Path, entry: str) -> bool:
    """Return True when an ``invariants.ensure`` entry is absolute or escapes ``root``.

    Mirrors the delivery-time check in ``iterate invariant`` (guard.py): an
    absolute path, or a relative path that resolves outside the project root,
    is rejected there, so doctor must flag it too instead of reporting healthy.
    ``root`` must already be resolved.
    """
    if Path(entry).is_absolute():
        return True
    try:
        target = (root / entry).resolve()
    except OSError:
        # A path that cannot be resolved at all cannot be inside the root.
        return True
    return not target.is_relative_to(root)


def _check_invariants(
    report: DoctorReport, config: dict[str, Any], project_root: Path
) -> None:
    """invariants section structure + invariant command metachar safety.

    ``iterate invariant`` executes ``invariants.commands`` as shell commands
    at delivery time, so a metachar command there is the same command-chaining
    risk as an unsafe ``validation.commands`` entry — the standalone safety
    net must cover it too.

    ``invariants.ensure`` entries are also checked for the same
    relative-path/containment rule ``iterate invariant`` enforces at delivery
    time, so doctor never reports healthy for a config that will be rejected
    later.
    """
    invariants = config.get("invariants")
    if invariants is not None and not isinstance(invariants, dict):
        _err(
            report,
            "invariants",
            "invariants must be a mapping (ensure + commands).",
            f"Got {type(invariants).__name__} instead.",
        )
        return
    if invariants is None:
        _ok(
            report,
            "invariants",
            "No invariants configured (iterate invariant degrades to validation.commands).",
        )
        return

    ensure = invariants.get("ensure")
    if ensure is None:
        _ok(report, "invariants.ensure", "No invariants.ensure assertions configured.")
    elif (
        not isinstance(ensure, list)
        or not ensure
        or not all(isinstance(e, str) and e.strip() for e in ensure)
    ):
        _err(
            report,
            "invariants.ensure",
            "invariants.ensure must be a non-empty list of relative path strings.",
        )
    elif len(set(ensure)) != len(ensure):
        _warn(
            report,
            "invariants.ensure",
            "invariants.ensure contains duplicate path entries.",
        )
    else:
        # Reject absolute paths and entries that escape the project root: the
        # error message above promises "relative path strings", and
        # `iterate invariant` refuses these at delivery time, so accepting them
        # here would be a false green light.
        root = project_root.resolve()
        escaping = [e for e in ensure if _ensure_path_escapes(root, e)]
        if escaping:
            _err(
                report,
                "invariants.ensure",
                "invariants.ensure entries must be relative paths inside the "
                "project root (absolute or '..' paths are rejected by "
                "`iterate invariant`).",
                "; ".join(escaping[:SCHEMA_MAX_ERRORS]),
            )
        else:
            _ok(report, "invariants.ensure", f"{len(ensure)} invariant file assertion(s).")

    commands = invariants.get("commands")
    if commands is None:
        _ok(report, "invariants.commands", "No invariants.commands configured.")
        return
    if not isinstance(commands, dict):
        _err(
            report,
            "invariants.commands",
            "invariants.commands must be a mapping of module -> list of commands.",
        )
        return
    unsafe: list[str] = []
    for module, cmds in commands.items():
        if not isinstance(cmds, list):
            continue
        for idx, command in enumerate(cmds):
            if isinstance(command, str) and any(
                ch in COMMAND_METACHARS for ch in command
            ):
                unsafe.append(f"{module}[{idx}] {command!r}")
    if unsafe:
        _err(
            report,
            "invariants.commands",
            "invariant command(s) contain shell metacharacters (possible command chaining).",
            "; ".join(unsafe[:SCHEMA_MAX_ERRORS]),
        )
        return
    _ok(report, "invariants.commands", "invariant commands contain no shell metacharacters.")


def _check_iterate_md_markers(report: DoctorReport, project_root: Path) -> None:
    """ITERATE.md must carry the USER-OWNED markers that refresh preserves.

    ``iterate refresh`` refuses to overwrite an ITERATE.md missing either
    marker (it may be hand-edited), surfacing the problem only at refresh
    time. Doctor surfaces it proactively so a project whose markers were
    accidentally removed is flagged before the next refresh attempt.
    """
    iterate_md_path = project_root / ITERATE_MD
    try:
        content = iterate_md_path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        # Unreadable/non-UTF-8 ITERATE.md must not vanish from the report:
        # silently returning produced "onboarding ✓ + 0 marker findings" —
        # a fake-complete healthy report for a file doctor could not read.
        _warn(
            report,
            "iterate.md.markers",
            "ITERATE.md exists but could not be read as UTF-8.",
            f"{exc}. Re-save the file as UTF-8, then re-run `iterate doctor`.",
        )
        return
    if not has_valid_user_owned_markers(content):
        _warn(
            report,
            "iterate.md.markers",
            "ITERATE.md is missing the USER-OWNED section markers.",
            "Run `iterate reonboard` to restore markers, or re-add "
            f"{USER_START_MARKER} / {USER_END_MARKER} around your manual edits.",
        )
        return
    _ok(report, "iterate.md.markers", "ITERATE.md USER-OWNED section markers are present.")


def apply_safe_fixes(config: dict[str, Any]) -> tuple[dict[str, Any], list[str]]:
    """Apply safe, non-destructive fixes to a config dict.

    Only fixes deterministic, unambiguous problems that cannot lose user
    data. Every fix mirrors a ``doctor`` check, so a repaired config no
    longer triggers that warning/error.

    Args:
        config: The parsed iterate.config.yaml content.

    Returns:
        A tuple of (possibly-updated config, human-readable fix list).
        The fix list is empty when nothing needed fixing.
    """
    # Deep-copy so nested ``git``/``onboarding`` dicts below are never mutated
    # in the caller's original config object.
    new_config = copy.deepcopy(config)
    fixes: list[str] = []

    # dimensions: must be non-empty and unique (schema minItems/uniqueItems).
    # Non-string members (e.g. a nested list from a hand edit) are unhashable
    # and would crash ``set``/``in``; mirror the check path (_dimension_ids
    # stringifies) so ``doctor --fix`` repairs instead of crashing. Non-string
    # entries are dropped instead of stringified into junk dimension names.
    dims = new_config.get("dimensions")
    if isinstance(dims, list):
        seen: set[str] = set()
        deduped: list[str] = []
        for d in dims:
            if not isinstance(d, str):
                fixes.append(f"dimensions: removed non-string entry {d!r}.")
                continue
            if d not in seen:
                deduped.append(d)
                seen.add(d)
        # Count duplicates against the *string-only* list. Comparing against the
        # pre-filter `dims` conflated the two removal causes and made the
        # user-facing fix log state a falsehood about their own config:
        # ['a', 'b', 123] reported "removed 1 duplicate" with zero duplicates,
        # and ['a', 'a', ['x']] reported "removed 2 duplicates" for one.
        string_entries = sum(1 for d in dims if isinstance(d, str))
        duplicates = string_entries - len(deduped)
        if duplicates:
            fixes.append(f"dimensions: removed {duplicates} duplicate(s).")
        if not deduped:
            deduped = list(CANONICAL_DIMENSIONS)
            fixes.append("dimensions: empty, restored canonical defaults.")
        new_config["dimensions"] = deduped
    elif dims is not None:
        # A non-list ``dimensions`` (e.g. the scalar "correctness") is an ERROR
        # in _check_dimensions, but repairing only lists made ``doctor --fix``
        # report "no safe fixes needed" while doctor kept flagging the same
        # config forever.
        new_config["dimensions"] = list(CANONICAL_DIMENSIONS)
        fixes.append("dimensions: non-list value reset to canonical defaults.")

    # personalization.* lists and dimension_sets.*.dimensions declare
    # ``uniqueItems`` in the schema. Dedupe them here too: `personalize`
    # prevents new duplicates, but a hand edit (or a config written before
    # that guard) otherwise left `doctor --fix` unable to repair the very
    # error it reported.
    personalization = new_config.get("personalization")
    if isinstance(personalization, dict):
        for key in ("protected_paths", "forbidden_fixes", "fix_priority_order"):
            value = personalization.get(key)
            if not isinstance(value, list):
                continue
            deduped: list[str] = []
            seen_values: set[str] = set()
            for entry in value:
                if isinstance(entry, str) and entry not in seen_values:
                    seen_values.add(entry)
                    deduped.append(entry)
            if len(deduped) != len(value):
                fixes.append(
                    f"personalization.{key}: removed "
                    f"{len(value) - len(deduped)} duplicate/invalid entry(ies)."
                )
                personalization[key] = deduped

    dimension_sets = new_config.get("dimension_sets")
    if isinstance(dimension_sets, dict):
        for name, spec in dimension_sets.items():
            if not isinstance(spec, dict):
                continue
            dims = spec.get("dimensions")
            if not isinstance(dims, list):
                continue
            deduped_dims: list[str] = []
            seen_dims: set[str] = set()
            for entry in dims:
                if isinstance(entry, str) and entry not in seen_dims:
                    seen_dims.add(entry)
                    deduped_dims.append(entry)
            if len(deduped_dims) != len(dims):
                fixes.append(
                    f"dimension_sets.{name}.dimensions: removed "
                    f"{len(dims) - len(deduped_dims)} duplicate/invalid entry(ies)."
                )
                spec["dimensions"] = deduped_dims

    # language: must be one of zh/en. isinstance guard first so an unhashable
    # hand-edited value (`language: [zh]`) is repaired instead of crashing
    # `doctor --fix` with a TypeError (mirrors the check path above).
    language = new_config.get("language")
    if language is not None and (not isinstance(language, str) or language not in SUPPORTED_LANGUAGES):
        new_config["language"] = "en"
        fixes.append(f"language: {language!r} invalid, reset to 'en'.")

    # reasoning_effort: must be one of low/medium/high (None = provider default).
    # Same unhashable-value guard as language.
    reasoning_effort = new_config.get("reasoning_effort")
    if reasoning_effort is not None and (
        not isinstance(reasoning_effort, str) or reasoning_effort not in REASONING_EFFORT_VALUES
    ):
        new_config["reasoning_effort"] = None
        fixes.append(
            f"reasoning_effort: {reasoning_effort!r} invalid, reset to provider default (null)."
        )

    # max_rounds: must be an integer in [1, 50].
    max_rounds = new_config.get("max_rounds")
    if max_rounds is not None:
        if isinstance(max_rounds, bool) or not isinstance(max_rounds, int):
            new_config.pop("max_rounds", None)
            fixes.append("max_rounds: removed non-integer value.")
        elif not (MAX_ROUNDS_MIN <= max_rounds <= MAX_ROUNDS_MAX):
            clamped = max(MAX_ROUNDS_MIN, min(MAX_ROUNDS_MAX, max_rounds))
            new_config["max_rounds"] = clamped
            fixes.append(f"max_rounds: clamped to {clamped}.")

    # git.target_branch: must be a non-empty string.
    git_cfg = new_config.get("git")
    if isinstance(git_cfg, dict):
        branch = git_cfg.get("target_branch")
        if branch is not None and (not isinstance(branch, str) or not branch.strip()):
            git_cfg["target_branch"] = "main"
            fixes.append("git.target_branch: empty, reset to 'main'.")

    # onboarding.skill_version: must match the installed skill version.
    onboarding = new_config.get("onboarding")
    if isinstance(onboarding, dict):
        recorded = onboarding.get("skill_version")
        if recorded is not None and recorded != SKILL_VERSION:
            onboarding["skill_version"] = SKILL_VERSION
            fixes.append(f"onboarding.skill_version: updated {recorded!r} → {SKILL_VERSION!r}.")

    return new_config, fixes


def run_doctor_fix(project_root: Path) -> tuple[bool, list[str]]:
    """Apply safe fixes to iterate.config.yaml with a timestamped backup.

    A backup with a ``.doctorfix-<timestamp>`` suffix is written before any
    change so the original config is always recoverable. Returns
    ``(True, [])`` when nothing needed fixing.

    Args:
        project_root: Project root directory.

    Returns:
        A tuple of (success, list of applied fixes). On failure the fixes
        already detected are still returned so the caller can log them.
    """
    config_path = project_root / CONFIG_YAML
    if not config_path.is_file():
        tui.error(
            "Doctor --fix: iterate.config.yaml not found; nothing to fix. "
            "Run `iterate onboard` to initialize the project."
        )
        return False, []

    config = load_onboarding_config(project_root)
    empty_config_rebuilt = False
    if config is None or not config:
        # An EMPTY config file is a repairable state, not a parse failure —
        # load_onboarding_config reports it as None, and reporting "could not be
        # parsed" sent the user chasing a YAML error that does not exist.
        # A file whose content parses to an empty mapping (``{}``, ``---``, or
        # only comments) arrives here as an empty dict, which is the same
        # repairable state: ``apply_safe_fixes({})`` finds nothing to fix, so
        # the old code returned "nothing to fix" while doctor kept reporting
        # the config as unusable.
        raw_text: str | None
        try:
            raw_text = config_path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            raw_text = None
        has_content = raw_text is not None and any(
            line.strip() and not line.strip().startswith("#")
            for line in raw_text.splitlines()
        )
        if config is not None or not has_content:
            # Empty mapping (``{}``) or no meaningful text at all (empty file /
            # comments only) → safe to rebuild.
            tui.warning(
                "Doctor --fix: iterate.config.yaml is empty; rebuilding it with safe defaults."
            )
            # Seeding is what makes the rebuild real: `apply_safe_fixes({})`
            # finds nothing to repair, so the old `config = {}` fell through the
            # `if not fixes: return True, []` early return and NOTHING was
            # written — while the caller printed "rebuilding it with safe
            # defaults" and doctor kept reporting the file as empty. A minimal
            # schema-valid config (canonical dimensions) plus an explicit fix
            # entry guarantees the write happens.
            config = {"dimensions": list(CANONICAL_DIMENSIONS)}
            empty_config_rebuilt = True
        else:
            tui.error(
                "Doctor --fix: iterate.config.yaml exists but could not be parsed; "
                "run `iterate doctor` without --fix for details."
            )
            return False, []

    new_config, fixes = apply_safe_fixes(config)
    if empty_config_rebuilt:
        # Report the rebuild itself; without this entry a seeded config that
        # needed no further repair would again look like "nothing to fix".
        fixes.insert(
            0,
            "iterate.config.yaml: empty, rebuilt with canonical dimensions "
            "(add goal/validation.commands next).",
        )

    # Capture missing fingerprints for an onboarded project so drift detection
    # is reactivated. The most common silent drift-disable is an onboarding
    # record (skill_version set) whose fingerprints are empty — e.g. an
    # AI-channel/hand-edited onboarding. This is additive and safe: existing
    # fingerprints are left untouched.
    onboarding = new_config.get("onboarding")
    if isinstance(onboarding, dict) and onboarding.get("skill_version"):
        stored = onboarding.get("fingerprints")
        if not isinstance(stored, list) or not stored:
            captured = fingerprints_to_dict(
                capture_fingerprints(project_root, get_drift_ignore(new_config))
            )
            if captured:
                onboarding["fingerprints"] = captured
                fixes.append(
                    f"onboarding.fingerprints: captured {len(captured)} manifest fingerprint(s)."
                )

    if not fixes:
        return True, []

    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    # The random suffix matters: the timestamp has one-second granularity, so
    # two `doctor --fix` runs inside the same second (a CI retry loop, a shell
    # `for` over configs, two terminals) resolved to the same backup path and
    # the second copy2 overwrote the first — destroying the only pre-fix copy
    # of a file the fix is about to rewrite. Matches the convention already
    # used by configcmd (salt) and refresh (uuid).
    backup_path = config_path.with_name(
        f"{CONFIG_YAML}.doctorfix-{timestamp}-{uuid.uuid4().hex[:6]}"
    )
    try:
        shutil.copy2(config_path, backup_path)
        atomic_write(
            config_path,
            yaml.safe_dump(
                new_config,
                default_flow_style=False,
                allow_unicode=True,
                sort_keys=False,
            ),
        )
    except (OSError, yaml.YAMLError) as exc:
        tui.error(f"Doctor --fix: failed to write fixed config: {exc}")
        return False, fixes
    return True, fixes


def export_report_json(
    report: DoctorReport, out_path: Path, *, strict: bool = False
) -> None:
    """Write the structured DoctorReport to ``out_path`` as JSON.

    Args:
        report: The report to serialize.
        out_path: Destination file path (UTF-8, JSON with 2-space indent).
        strict: Mirrors ``doctor --strict``. MUST be threaded through from the
            CLI: exporting with the default ``strict=False`` while the process
            itself exits 1 under ``--strict`` produced a file claiming
            ``healthy: true`` for a run that failed — the exact contradiction
            ``to_dict``'s docstring warns about, reintroduced on the export
            path. The caller (``_cmd_doctor``) passes its own ``strict`` flag.

    Raises:
        OSError: When the file cannot be written.
    """
    payload = json.dumps(
        report.to_dict(strict=strict), ensure_ascii=False, indent=2
    )
    out_path.parent.mkdir(parents=True, exist_ok=True)
    # Unique tmp name (pid + random suffix): a fixed "<name>.tmp" made two
    # concurrent exports to the same target stomp each other's half-written
    # file, and a failed write_text left the tmp behind forever. Write →
    # atomic replace → best-effort cleanup of the tmp on any failure.
    tmp_path = out_path.with_name(
        f"{out_path.name}.{os.getpid()}.{uuid.uuid4().hex[:6]}.tmp"
    )
    try:
        tmp_path.write_text(payload + "\n", encoding="utf-8")
        os.replace(tmp_path, out_path)
    finally:
        try:
            tmp_path.unlink(missing_ok=True)
        except OSError:
            pass  # cleanup is best-effort; the real error surfaces above


def _resolve_output_language(project_root: Path) -> str:
    """Best-effort read of the project's configured output ``language``.

    Doctor's structured findings are English-only, but the "Next action(s)"
    hints are operator-facing prose and must follow the project's ``language``
    setting. Reads the config directly (rather than via
    ``load_onboarding_config``, which logs to stderr) so a corrupt config —
    already reported as a ``config.parse`` finding above — does not print a
    second, duplicate error line during rendering. Falls back to ``"en"`` for
    a missing/unreadable config or an unsupported value; rendering must never
    crash on a hand-edited config.
    """
    config_path = project_root / CONFIG_YAML
    try:
        raw = yaml.safe_load(config_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, yaml.YAMLError):
        return "en"
    if not isinstance(raw, dict):
        return "en"
    language = raw.get("language")
    if isinstance(language, str) and language in SUPPORTED_LANGUAGES:
        return language
    return "en"


def render_report(
    report: DoctorReport,
    json_output: bool = False,
    strict: bool = False,
    language: str | None = None,
) -> int:
    """Render a DoctorReport to the terminal.

    Args:
        report: The report to render.
        json_output: When True, print a structured JSON blob instead of TUI.
        strict: When True, warnings also flip the exit code to 1 (default
            doctor exit semantics: only errors are blocking; ``--strict``
            lets CI gate on any non-clean state, mirroring the summary line).
        language: Output language for the "Next action(s)" hints (``zh`` /
            ``en``). When None, it is read from the project's config so the
            hints match the rest of the operator's setup.

    Returns:
        Exit code: 0 when healthy (errors absent); 1 when errors are present.
        With ``strict``, 1 is returned when warnings are present as well.
    """
    blocking = report.has_errors() or (strict and report.has_warnings())
    if json_output:
        print(json.dumps(report.to_dict(strict=strict), ensure_ascii=False, indent=2))
        return 1 if blocking else 0

    if language is None:
        language = _resolve_output_language(Path(report.project))
    if language not in SUPPORTED_LANGUAGES:
        language = "en"

    tui.intro(f"Iterate Skill — Doctor / {report.project}")

    for finding in report.findings:
        if finding.severity == "ok":
            tui.success(f"[{finding.check}] {finding.message}", indent=2)
        elif finding.severity == "warn":
            tui.warning(f"[{finding.check}] {finding.message}", indent=2)
            if finding.detail:
                tui.hint(finding.detail, indent=4)
        else:
            tui.error(f"[{finding.check}] {finding.message}", indent=2)
            if finding.detail:
                tui.hint(finding.detail, indent=4)

    _render_next_actions(tui, report, language=language)

    _render_summary(tui, report)
    return 1 if blocking else 0


def _render_summary(tui: Any, report: DoctorReport) -> None:
    """Render the doctor end-of-run summary line.

    Distinguishes three outcomes so the summary never contradicts the
    findings shown above:
    - errors present → error summary, exit code already set to 1 by caller.
    - warnings only  → *not* reported as plain "healthy" (the checks
      surfaced warnings the operator should look at), but still non-blocking.
    - clean          → "healthy".
    """
    tui.empty_line()
    error_count = sum(1 for f in report.findings if f.severity == "error")
    warn_count = sum(1 for f in report.findings if f.severity == "warn")
    if error_count:
        passed_count = sum(1 for f in report.findings if f.severity == "ok")
        tui.error(
            f"Doctor: {error_count} error(s) found "
            f"({passed_count} check(s) passed)."
        )
        return
    if warn_count:
        tui.warning(
            f"Doctor: healthy but with {warn_count} warning(s) — non-blocking."
        )
        return
    tui.success(f"Doctor: healthy ({len(report.findings)} checks passed).")


def _render_next_actions(
    tui: Any, report: DoctorReport, language: str = "en"
) -> None:
    """Aggregate actionable next steps for a doctor run.

    Grep-friendly, forge a single ``Next action(s):`` block mapping the most
    common problems to the command that fixes them, so users are not left
    guessing what to do after seeing warnings/errors.

    The hint prose follows the project's configured ``language`` (``zh`` /
    ``en``) — it used to be hardcoded Chinese even though the rest of the
    doctor output is English, so an English-language project saw a mixed
    report. Unknown languages fall back to English.
    """
    checks = {f.check for f in report.findings if f.severity in ("warn", "error")}
    if not checks:
        return

    zh = language == "zh"

    def _t(
        zh_label: str,
        zh_command: str,
        en_label: str,
        en_command: str,
    ) -> tuple[str, str]:
        return (zh_label, zh_command) if zh else (en_label, en_command)

    actions: list[tuple[str, str]] = []
    if "config.parse" in checks:
        actions.append(
            _t(
                "修复 iterate.config.yaml 的语法错误",
                "编辑配置后运行 `iterate doctor`",
                "Fix the YAML syntax error in iterate.config.yaml",
                "edit the config, then run `iterate doctor`",
            )
        )
    if "config.schema" in checks:
        actions.append(
            _t(
                "配置字段不符合规范",
                "编辑 iterate.config.yaml 中所示字段，或运行 `iterate reonboard` 重新生成",
                "Config fields do not conform to the schema",
                "edit the fields shown in iterate.config.yaml, or run `iterate reonboard` to regenerate",
            )
        )
    if "validation.commands" in checks:
        actions.append(
            _t(
                "validation.commands 结构异常",
                "编辑配置使每个模块对应非空命令列表",
                "validation.commands structure is invalid",
                "edit the config so every module maps to a non-empty command list",
            )
        )
    if (
        "validation.command_whitelist" in checks
        or "validation.whitelist" in checks
    ):
        actions.append(
            _t(
                "命令白名单/验证命令含非法字符",
                "运行 `iterate personalize` 重新配置验证命令，或在配置中修正白名单",
                "Command whitelist / validation command contains an illegal character",
                "run `iterate personalize` to reconfigure validation commands, or fix the whitelist in the config",
            )
        )
    if (
        "invariants" in checks
        or "invariants.commands" in checks
        or "invariants.ensure" in checks
    ):
        actions.append(
            _t(
                "invariants 配置异常",
                "在 iterate.config.yaml 中修正 invariants.commands / invariants.ensure",
                "invariants config is invalid",
                "fix invariants.commands / invariants.ensure in iterate.config.yaml",
            )
        )
    if "skill_version" in checks:
        actions.append(
            _t(
                "录制的技能版本过旧",
                "运行 `iterate refresh` 更新录制版本",
                "Recorded skill version is out of date",
                "run `iterate refresh` to update the recorded version",
            )
        )
    if "dimensions" in checks or "review.scope" in checks:
        actions.append(
            _t(
                "维度/范围配置异常",
                "在 iterate.config.yaml 中修正或运行 `iterate reonboard`",
                "dimensions / review scope config is invalid",
                "fix it in iterate.config.yaml or run `iterate reonboard`",
            )
        )
    if "drift" in checks:
        actions.append(
            _t(
                "技术栈漂移",
                "运行 `iterate refresh` 同步知识库（非阻塞）",
                "Tech-stack drift",
                "run `iterate refresh` to sync the knowledge base (non-blocking)",
            )
        )
    handled = {
        "config.parse", "config.schema", "validation.commands",
        "validation.command_whitelist", "validation.whitelist", "invariants",
        "invariants.commands", "invariants.ensure", "skill_version",
        "dimensions", "review.scope", "drift",
    }
    unmapped = sorted(checks - handled)
    if unmapped:
        # New checks used to appear on screen with no next action at all.
        # One generic entry keeps every warning/error actionable.
        actions.append(
            _t(
                "仍有诊断项未通过：" + ", ".join(unmapped),
                "先运行 `iterate doctor --fix`；仍失败则按上方提示编辑配置或运行 `iterate refresh`",
                "Unresolved diagnostic(s): " + ", ".join(unmapped),
                "run `iterate doctor --fix` first; if it persists, edit the "
                "config as shown above or run `iterate refresh`",
            )
        )

    if actions:
        tui.empty_line()
        tui.info("Next action(s): ", indent=2)
        for label, command in actions:
            tui.bullet(f"{label} → {command}", indent=4)


def main(argv: list[str] | None = None) -> int:
    """CLI entry point for ``iterate doctor`` (standalone, for tests)."""
    import argparse

    parser = argparse.ArgumentParser(prog="iterate doctor")
    parser.add_argument("-p", "--project", default=".", help="Project root directory.")
    parser.add_argument("--json", action="store_true", help="Emit structured JSON.")
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Warnings also flip the exit code to 1 (parity with `iterate doctor`).",
    )
    parser.add_argument(
        "--json-out",
        default=None,
        help="Also write the structured JSON report to this path.",
    )
    args = parser.parse_args(argv)

    project_root = Path(args.project).resolve()
    report = run_doctor(project_root)
    code = render_report(report, json_output=args.json, strict=args.strict)
    if args.json_out:
        try:
            export_report_json(
                report, Path(args.json_out).resolve(), strict=args.strict
            )
        except OSError as exc:
            tui.error(f"doctor: failed to write JSON report to {args.json_out}: {exc}")
            return 1
    return code


if __name__ == "__main__":
    sys.exit(main())