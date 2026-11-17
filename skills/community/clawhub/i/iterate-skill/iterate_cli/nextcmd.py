"""Guided "what should I do next?" advice (``iterate next``).

``status``, ``show`` and ``doctor`` each report *state*; none of them answers
the question a new (or returning) user actually has: "which single command do
I run now?". A first-time user had to read the README to discover the
install → init → doctor → personalize → ``/iterate`` path, and a returning user
looking at a drifted project had to know that ``refresh --diff`` exists before
``refresh``.

``iterate next`` turns the same read-only signals into a prioritized, ordered
plan: one next command with a reason, optional follow-up steps, and notes for
environment gaps (for example "not a git repository"). It is advisory and
never writes, so it is safe in scripts; ``--json`` exposes the plan for CI and
other skills. Exit code is always 0 (like ``scan``): the command answers a
question, it does not gate.

The module is side-effect free; the CLI handler only renders the plan.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from iterate_cli.doctor import DOCTOR_CHECK_NAMES, run_doctor
from iterate_cli.refresh import (
    CONFIG_YAML,
    check_onboarding_drift,
    drift_unavailable_code,
    is_onboarding_complete,
    load_onboarding_config,
)
from iterate_cli.tui import tui

#: Stable machine-readable states. These are the contract for ``--json``
#: consumers; branch on them, never on the human-readable reason text.
STATE_NOT_ONBOARDED = "not_onboarded"
STATE_CONFIG_CORRUPT = "config_corrupt"
STATE_CONFIG_MISSING = "config_missing"
STATE_DRIFT = "drift"
STATE_UNHEALTHY = "unhealthy"
STATE_WARNINGS = "warnings"
STATE_HEALTHY = "healthy"

#: Human labels for the TUI renderer.
_STATE_LABELS: dict[str, str] = {
    STATE_NOT_ONBOARDED: "not initialized",
    STATE_CONFIG_CORRUPT: "config needs repair",
    STATE_CONFIG_MISSING: "config missing",
    STATE_DRIFT: "tech stack drifted",
    STATE_UNHEALTHY: "health checks failing",
    STATE_WARNINGS: "healthy with warnings",
    STATE_HEALTHY: "healthy",
}


def _step(
    command: str,
    reason: str,
    *,
    blocking: bool = False,
    detail: str = "",
) -> dict[str, Any]:
    """Build one plan step with a stable shape."""
    return {
        "command": command,
        "reason": reason,
        "blocking": blocking,
        "detail": detail,
    }


def _drift_detail(drift: Any) -> str:
    """Summarize the concrete drift items for the plan (bounded for display)."""
    items: list[str] = []
    for label, values in (
        ("added", getattr(drift, "added", ())),
        ("removed", getattr(drift, "removed", ())),
        ("changed", getattr(drift, "changed", ())),
    ):
        names = [str(value) for value in values]
        if names:
            shown = ", ".join(names[:5])
            if len(names) > 5:
                shown += f", … (+{len(names) - 5} more)"
            items.append(f"{label}: {shown}")
    return "; ".join(items)


def plan_next(project_root: Path) -> dict[str, Any]:
    """Compute the prioritized next-action plan for ``project_root``.

    Read-only: it loads the config, checks manifest drift and runs doctor's
    non-drift checks. The drift check is deliberately excluded from the doctor
    call because it is computed once here — running it twice would rescan every
    manifest for the same answer.

    Args:
        project_root: The project root directory.

    Returns:
        A JSON-serialisable plan with stable keys: ``command``, ``project``,
        ``state``, ``blocking``, ``onboarded``, ``config_exists``,
        ``config_ok``, ``drift``, ``drift_reason``, ``doctor``, ``next``,
        ``steps`` and ``notes``. ``next`` is the first step (or ``None`` when
        the plan is empty, which does not happen for a healthy project: it
        still suggests handing the goal to the assistant).
    """
    config_path = project_root / CONFIG_YAML
    config_exists = config_path.is_file()
    config = load_onboarding_config(project_root) if config_exists else None
    onboarded = is_onboarding_complete(project_root)
    config_corrupt = config_exists and config is None

    steps: list[dict[str, Any]] = []
    notes: list[str] = []
    drift_value: bool | None = None
    # Stable "why is there no drift result" code, even for the pre-onboarding
    # states: a consumer can then tell "not initialized yet" from "check
    # disabled" without inferring it from ``state``.
    drift_reason: str | None = drift_unavailable_code(project_root, config)
    doctor_errors = 0
    doctor_warnings = 0

    if not (project_root / ".git").exists():
        notes.append(
            "Not a git repository — iterate's per-round commits and worktrees "
            "need git; run `git init` first."
        )

    if config_corrupt:
        state = STATE_CONFIG_CORRUPT
        steps.append(
            _step(
                "iterate doctor --fix",
                "iterate.config.yaml exists but could not be parsed; --fix "
                "repairs the safely fixable problems (a timestamped backup is "
                "written first).",
                blocking=True,
            )
        )
        steps.append(
            _step(
                "iterate doctor",
                "If --fix cannot repair it, doctor names the exact problem; "
                "restore a backup with `iterate backup list` if needed.",
            )
        )
        notes.append(
            "A timestamped backup may already exist — `iterate backup list` "
            "shows what can be restored."
        )
    elif not onboarded:
        state = STATE_NOT_ONBOARDED
        if config_exists:
            steps.append(
                _step(
                    "iterate onboard",
                    "iterate.config.yaml exists but ITERATE.md is missing; "
                    "onboarding completes the pair without discarding your "
                    "config.",
                    blocking=True,
                )
            )
        else:
            steps.append(
                _step(
                    "iterate init --yes",
                    "No iterate.config.yaml or ITERATE.md yet; init writes both "
                    "from the project scan, with no prompts.",
                    blocking=True,
                )
            )
            steps.append(
                _step(
                    "iterate onboard",
                    "Prefer prompts? The interactive wizard produces the same "
                    "files and lets you adjust every value.",
                )
            )
    elif not config_exists:
        state = STATE_CONFIG_MISSING
        steps.append(
            _step(
                "iterate init --yes",
                "ITERATE.md exists but iterate.config.yaml is missing; init "
                "recreates the config and preserves the USER-OWNED section of "
                "ITERATE.md.",
                blocking=True,
            )
        )
    else:
        onboarding = (
            config.get("onboarding") if isinstance(config, dict) else None
        )
        onboarding = onboarding if isinstance(onboarding, dict) else {}
        drift_enabled = onboarding.get("drift_check", True)
        drift = (
            check_onboarding_drift(project_root, config)
            if drift_enabled
            else None
        )
        drift_value = drift.has_drift if drift is not None else None
        drift_reason = (
            None
            if drift is not None
            else drift_unavailable_code(project_root, config)
        )

        report = run_doctor(
            project_root,
            checks=set(DOCTOR_CHECK_NAMES) - {"drift"},
        )
        doctor_errors = sum(1 for f in report.findings if f.severity == "error")
        doctor_warnings = sum(1 for f in report.findings if f.severity == "warn")

        if drift is not None and drift.has_drift:
            state = STATE_DRIFT
            steps.append(
                _step(
                    "iterate refresh --diff",
                    "Manifests changed since onboarding; preview the exact "
                    "ITERATE.md/config rewrite first (never writes).",
                    blocking=True,
                    detail=_drift_detail(drift),
                )
            )
            steps.append(
                _step(
                    "iterate refresh",
                    "Apply the refresh once the diff looks right.",
                )
            )
        elif doctor_errors:
            state = STATE_UNHEALTHY
            steps.append(
                _step(
                    "iterate doctor --fix",
                    f"{doctor_errors} health check(s) failed; --fix applies "
                    "safe repairs and re-runs diagnostics.",
                    blocking=True,
                )
            )
            steps.append(
                _step(
                    "iterate doctor",
                    "See the remaining findings and their fix hints.",
                )
            )
        elif doctor_warnings:
            state = STATE_WARNINGS
            steps.append(
                _step(
                    "iterate doctor",
                    f"{doctor_warnings} warning(s) — review them before "
                    "starting a review round (warnings do not block by "
                    "default).",
                )
            )
            steps.append(
                _step(
                    '/iterate "<goal>"',
                    "Start the review loop once the warnings are understood.",
                )
            )
        else:
            state = STATE_HEALTHY
            steps.append(
                _step(
                    '/iterate "<goal>"',
                    "Project is initialized and healthy — hand your goal to "
                    "the AI assistant.",
                )
            )
            steps.append(
                _step(
                    "iterate personalize",
                    "Optional: capture project-specific constraints the "
                    "scanner cannot detect.",
                )
            )

    return {
        "command": "next",
        "project": str(project_root),
        "state": state,
        "blocking": any(step["blocking"] for step in steps),
        "onboarded": onboarded,
        "config_exists": config_exists,
        "config_ok": config is not None,
        "drift": drift_value,
        "drift_reason": drift_reason,
        "doctor": {"errors": doctor_errors, "warnings": doctor_warnings},
        "next": steps[0] if steps else None,
        "steps": steps,
        "notes": notes,
    }


def render_next(plan: dict[str, Any], json_output: bool = False) -> int:
    """Render a plan produced by :func:`plan_next`.

    Args:
        plan: The plan dict.
        json_output: When True, print one JSON document instead of TUI lines.

    Returns:
        Always 0: ``next`` is advisory, not a gate (use ``doctor`` or
        ``report --strict`` for exit-code gating).
    """
    if json_output:
        import json

        print(json.dumps(plan, ensure_ascii=False, indent=2, default=str))
        return 0

    tui.intro("Iterate Skill — Next")
    tui.key_value("Project", str(plan["project"]))
    tui.key_value(
        "State", _STATE_LABELS.get(plan["state"], str(plan["state"]))
    )

    next_step = plan.get("next")
    if next_step:
        tui.empty_line()
        tui.key_value("Next step", str(next_step["command"]))
        tui.hint(str(next_step["reason"]), indent=4)
        if next_step.get("detail"):
            tui.hint(str(next_step["detail"]), indent=4)

    remaining = list(plan.get("steps", []))[1:]
    if remaining:
        tui.empty_line()
        for step in remaining:
            tui.key_value("Then", str(step["command"]))
            tui.hint(str(step["reason"]), indent=4)

    for note in plan.get("notes", []):
        tui.empty_line()
        tui.warning(str(note), indent=2)

    return 0


def run_next(project_root: Path, json_output: bool = False) -> int:
    """Handle the ``iterate next`` subcommand end to end."""
    return render_next(plan_next(project_root), json_output=json_output)
