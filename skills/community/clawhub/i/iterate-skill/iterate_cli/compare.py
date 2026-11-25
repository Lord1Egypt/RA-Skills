"""Config-vs-scan gap analysis (``iterate scan --compare``).

``iterate scan`` answers "what does this project look like?" and ``iterate
config`` answers "what is configured?". Neither answers the question that
matters right after the stack changes: *is the configuration still in step with
the project?* A layer added since onboarding (a frontend, an API package, a new
language) shows up in the scan's suggestions but is absent from
``iterate.config.yaml``; the user only finds out by reading two JSON documents
side by side.

``iterate scan --compare`` closes that loop. It is **read-only** (only reads the
config and the filesystem), **advisory** (never a failure — an out-of-sync
config is a normal state, not an error) and works with or without a config:

* config missing  → point at ``init`` / ``onboard``;
* config unusable → point at ``doctor --fix``;
* config present  → report the suggested dimensions that are not enabled, the
  suggested named sets that are not configured, and the validation modules
  that have no commands, plus the exact command(s) that close each gap.

The comparison deliberately reports *only* suggestions the config is missing.
Extra dimensions/sets or customised validation commands are normal user
choices, not gaps; flagging them would turn a diagnostic into a nag.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from iterate_cli.refresh import CONFIG_YAML, load_onboarding_config
from iterate_cli.scan import collect_scan_data
from iterate_cli.tui import tui

#: Stable machine-readable config states for ``--json`` consumers.
CONFIG_OK = "ok"
CONFIG_MISSING = "missing"
CONFIG_UNUSABLE = "unusable"


def _string_list(value: Any) -> list[str]:
    """Return the non-empty strings of ``value`` when it is a list, else []."""
    if not isinstance(value, list):
        return []
    return [str(item).strip() for item in value if isinstance(item, str) and item.strip()]


def _mapping(value: Any) -> dict[str, Any]:
    """Return ``value`` when it is a mapping, else an empty dict."""
    return value if isinstance(value, dict) else {}


def _current_config_view(config: dict[str, Any] | None) -> dict[str, Any]:
    """Extract the fields compared against the scan, defensively.

    Hand-edited configs are validated by ``doctor``; this read-only comparison
    must never crash on one. Every wrong-shaped field is treated as "not
    configured" so the report degrades to a suggestion instead of a traceback.
    """
    if config is None:
        return {
            "dimensions": [],
            "dimension_sets": [],
            "validation_modules": [],
        }
    validation = _mapping(config.get("validation"))
    commands = _mapping(validation.get("commands"))
    return {
        "dimensions": _string_list(config.get("dimensions")),
        # Any declared set counts as configured, even a hand-written one with a
        # custom shape: refresh/doctor own normalisation, and second-guessing
        # the user here would report a set they clearly meant to define.
        "dimension_sets": sorted(str(name) for name in _mapping(config.get("dimension_sets"))),
        "validation_modules": sorted(str(name) for name in commands),
    }


def _count(noun: str, count: int, plural: str | None = None) -> str:
    """Render ``1 dimension`` / ``2 dimensions`` without a fixed ``(s)``."""
    if count == 1:
        return f"1 {noun}"
    return f"{count} {plural or noun + 's'}"


def _merge_dimensions(current: list[str], missing: list[str]) -> list[str]:
    """Union preserving the user's existing order, then the suggested order."""
    merged: list[str] = []
    seen: set[str] = set()
    for dimension in [*current, *missing]:
        if dimension not in seen:
            seen.add(dimension)
            merged.append(dimension)
    return merged


def build_comparison(
    project_root: Path,
    scan_data: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Compare the current config with a fresh scan's suggestions.

    Args:
        project_root: Project root directory.
        scan_data: Optional pre-computed ``collect_scan_data`` payload; when
            omitted it is collected here (so the CLI can reuse one scan).

    Returns:
        A JSON-serialisable report with stable keys: ``command``, ``project``,
        ``config``, ``suggested``, ``gaps``, ``in_sync``, ``next`` and
        ``read_only``. ``gaps`` always has the three list keys
        ``dimensions`` / ``dimension_sets`` / ``validation_modules`` so a
        consumer can index them unconditionally.
    """
    data = scan_data if scan_data is not None else collect_scan_data(project_root)
    config_path = project_root / CONFIG_YAML
    config_exists = config_path.is_file()
    config = load_onboarding_config(project_root) if config_exists else None
    if not config_exists:
        status = CONFIG_MISSING
    elif config is None:
        status = CONFIG_UNUSABLE
    else:
        status = CONFIG_OK

    current = _current_config_view(config)
    suggested_sets = _mapping(data.get("suggested_dimension_sets"))
    suggested_commands = _mapping(data.get("suggested_validation_commands"))
    suggested = {
        "dimensions": _string_list(data.get("suggested_dimensions")),
        "dimension_sets": {
            str(name): _mapping(spec) for name, spec in sorted(suggested_sets.items())
        },
        "validation_modules": sorted(str(name) for name in suggested_commands),
    }

    # Only a readable config can be "behind"; absent/unusable configs get their
    # own guidance instead of a misleading list of every suggestion as a gap.
    gaps: dict[str, list[str]] = {
        "dimensions": [],
        "dimension_sets": [],
        "validation_modules": [],
    }
    next_steps: list[str] = []
    if status == CONFIG_OK:
        enabled = set(current["dimensions"])
        configured_sets = set(current["dimension_sets"])
        configured_modules = set(current["validation_modules"])
        gaps["dimensions"] = [
            dimension for dimension in suggested["dimensions"] if dimension not in enabled
        ]
        gaps["dimension_sets"] = [
            name for name in suggested["dimension_sets"] if name not in configured_sets
        ]
        gaps["validation_modules"] = [
            name
            for name in suggested["validation_modules"]
            if name not in configured_modules
        ]
        if gaps["dimensions"]:
            merged = _merge_dimensions(current["dimensions"], gaps["dimensions"])
            next_steps.append(f"iterate config set dimensions {','.join(merged)}")
        if gaps["dimension_sets"] or gaps["validation_modules"]:
            # refresh additively reconciles both sections without touching the
            # user's enabled dimensions (which is why the explicit config set
            # above is listed separately).
            next_steps.append("iterate refresh")
    elif status == CONFIG_MISSING:
        next_steps.extend(["iterate init --yes", "iterate onboard"])
    else:
        next_steps.extend(["iterate doctor --fix", "iterate doctor"])

    in_sync = status == CONFIG_OK and not any(gaps.values())
    return {
        "command": "scan --compare",
        "project": str(project_root),
        "config": {
            "file": CONFIG_YAML,
            "status": status,
            **current,
        },
        "suggested": suggested,
        "gaps": gaps,
        "in_sync": in_sync,
        "next": next_steps,
        "read_only": True,
    }


def render_comparison(comparison: dict[str, Any], json_output: bool = False) -> int:
    """Render a comparison report; always returns 0 (advisory, read-only).

    Args:
        comparison: Payload from :func:`build_comparison`.
        json_output: When True, emit exactly one JSON document on stdout.

    Returns:
        Always 0: an out-of-sync configuration is reported, never gated.
    """
    if json_output:
        print(json.dumps(comparison, ensure_ascii=False, indent=2, default=str))
        return 0

    config = _mapping(comparison.get("config"))
    gaps = _mapping(comparison.get("gaps"))
    status = str(config.get("status", CONFIG_UNUSABLE))

    tui.intro("Iterate Skill — Scan vs config")
    tui.key_value("Project", str(comparison.get("project", "")))
    if status == CONFIG_OK:
        summary = (
            f"{_count('dimension', len(config.get('dimensions') or []))}, "
            f"{_count('set', len(config.get('dimension_sets') or []))}, "
            f"{_count('validation module', len(config.get('validation_modules') or []))}"
        )
        tui.key_value("Config", f"{CONFIG_YAML} ({summary})")
    else:
        tui.key_value("Config", f"{CONFIG_YAML} ({status})")

    if status == CONFIG_MISSING:
        tui.warning(f"{CONFIG_YAML} not found; nothing to compare yet.")
        tui.hint("Run `iterate init --yes` (prompt-free) or `iterate onboard`.")
    elif status == CONFIG_UNUSABLE:
        tui.error(f"{CONFIG_YAML} could not be read as a YAML mapping.")
        tui.hint("Run `iterate doctor --fix`, or fix the file and re-run.")
    elif comparison.get("in_sync"):
        tui.success(
            "Config matches the scanner's suggestions — no gaps found."
        )
    else:
        sections = (
            (
                "Suggested dimensions not enabled / 建议但未启用的维度",
                "dimensions",
            ),
            (
                "Suggested dimension sets not configured / 建议但未配置的维度集",
                "dimension_sets",
            ),
            (
                "Suggested validation modules without commands / 建议但缺命令的校验模块",
                "validation_modules",
            ),
        )
        for title, key in sections:
            values = [str(value) for value in (gaps.get(key) or [])]
            if not values:
                continue
            tui.section(title)
            for value in values:
                tui.bullet(value)
        next_steps = [str(step) for step in (comparison.get("next") or [])]
        if next_steps:
            tui.section("Next steps / 下一步")
            for step in next_steps:
                # Commands are copy-paste material: print them verbatim rather
                # than wrapping at a space in the middle of an argument list.
                tui.command(step, indent=2)

    tui.empty_line()
    tui.hint("Read-only: nothing was written.")
    tui.hint("Machine-readable: `iterate scan --compare --json`")
    return 0


def run_compare(project_root: Path, json_output: bool = False) -> int:
    """Collect, compare and render in one call (used by ``iterate scan --compare``)."""
    return render_comparison(build_comparison(project_root), json_output=json_output)
