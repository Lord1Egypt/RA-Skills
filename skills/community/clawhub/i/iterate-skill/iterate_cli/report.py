"""Shareable project report (``iterate report``).

``status``, ``scan`` and ``doctor`` each answer one question, but a user who
wants to *show* the project state — in a PR description, a CI artifact, an
issue, or a handoff note — had to copy three terminal outputs and stitch them
together by hand. ``iterate report`` aggregates the same read-only data into a
single deterministic Markdown document (or one JSON document with ``--json``).

The module is intentionally side-effect free: :func:`build_report` only reads
the project, and :func:`render_markdown` only formats the result. The CLI
handler owns file writes and exit codes, so this logic is directly testable.

Exit-code semantics mirror ``doctor``: a report with errors is a failed gate
(``summary.blocking`` is true), and ``--strict`` additionally treats warnings
as blocking. ``--format`` is deliberately absent: Markdown is the human
document and the global ``--json`` flag is the machine document, matching the
contract every other command already follows.

Since v3.20.0 the Markdown report can also be appended to the GitHub Actions
run-summary page (``--github-summary`` / ``--no-github-summary``, auto-enabled
when ``GITHUB_STEP_SUMMARY`` is set): a CI run renders the whole report on the
workflow summary instead of burying it in a job log or an artifact. The write
is a separate sink — it never touches stdout, never changes the exit code, and
is best-effort (an unwritable summary warns instead of failing the gate).
"""

from __future__ import annotations

import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from iterate_cli import __version__
from iterate_cli.doctor import run_doctor
from iterate_cli.personalize import count_personalization_rules
from iterate_cli.scan import collect_scan_data
from iterate_cli.show import collect_show_data

#: GitHub Actions exposes the per-job run-summary file through this variable.
#: Appending Markdown to it renders the report on the workflow's run-summary
#: page (the "job summary" block), which is where developers already look for
#: a CI run's outcome — instead of having to open the job log or download an
#: artifact to read ``iterate report``'s document.
_GITHUB_SUMMARY_ENV = "GITHUB_STEP_SUMMARY"


def github_summary_path() -> str | None:
    """Return the GitHub Actions step-summary file path, or None outside CI.

    ``GITHUB_STEP_SUMMARY`` is set by the runner for every step of every job.
    When it is absent (local run, other CI) there is nowhere to render a step
    summary, so :func:`enabled_from_env` stays off.
    """
    value = os.environ.get(_GITHUB_SUMMARY_ENV, "").strip()
    return value or None


def enabled_from_env() -> bool:
    """Auto-detect: emit the run summary when GitHub provides the file.

    Mirrors :func:`iterate_cli.annotate.enabled_from_args`: the auto path must
    not require the user to remember a flag inside a workflow. An explicit
    ``--no-github-summary`` (see :func:`enabled_from_args`) still wins.
    """
    return github_summary_path() is not None


def enabled_from_args(summary: bool | None) -> bool:
    """Resolve the ``--github-summary``/``--no-github-summary`` tri-state.

    Args:
        summary: ``True`` (``--github-summary``), ``False``
            (``--no-github-summary``), or ``None`` (auto-detect).

    Returns:
        ``True`` when the run summary should be written. The explicit flags
        win; otherwise auto-detect via :data:`_GITHUB_SUMMARY_ENV`, exactly
        like the doctor/report annotation tri-state.
    """
    if summary is True:
        return True
    if summary is False:
        return False
    return enabled_from_env()


def append_github_summary(text: str, path: str | None = None) -> Path | None:
    """Append ``text`` to the GitHub step-summary file and return its path.

    The runner creates ``GITHUB_STEP_SUMMARY`` once per job and lets every step
    append to it, so this must **append** (never truncate) — otherwise a
    ``report`` step after another step's summary would silently erase it. The
    file is created if it does not exist yet, which also makes the helper
    directly unit-testable without a live runner.

    Args:
        text: Markdown to append. A trailing newline is guaranteed so the next
            step's summary starts on its own line.
        path: Explicit file path (test seam). Defaults to the
            ``GITHUB_STEP_SUMMARY`` environment value.

    Returns:
        The path written, or None when no path is available.
    """
    target = path or github_summary_path()
    if not target:
        return None
    target_path = Path(target)
    # Open in append mode; the runner's file may already hold other steps.
    with target_path.open("a", encoding="utf-8") as handle:
        handle.write(text)
        if not text.endswith("\n"):
            handle.write("\n")
    return target_path

#: Bilingual report labels. Doctor finding messages stay English (they are the
#: skill's canonical check names/messages); only the report's own structural
#: prose follows the project's configured language.
_LABELS: dict[str, dict[str, str]] = {
    "en": {
        "title": "Iterate Project Report",
        "tagline": "Generated by `iterate report`",
        "project": "Project",
        "skill_version": "Skill version",
        "generated": "Generated",
        "onboarding": "Onboarding",
        "onboarded": "complete",
        "not_onboarded": "not initialized",
        "channel": "channel",
        "completed": "completed",
        "health": "Health",
        "healthy": "healthy",
        "warnings_only": "healthy with warnings",
        "errors": "needs attention",
        "drift": "Drift",
        "drift_none": "No drift detected",
        "drift_unknown": "unknown (no fingerprint baseline)",
        "drift_disabled": "check disabled",
        "tech_stack": "Tech stack",
        "languages": "Languages",
        "manifests": "Manifests",
        "package_managers": "Package managers",
        "features": "Features",
        "configuration": "Review configuration",
        "target_branch": "Target branch",
        "review_scope": "Review scope",
        "max_rounds": "Max rounds",
        "dimensions": "Dimensions",
        "dimension_sets": "Dimension sets",
        "validation": "Validation",
        "whitelist": "Command whitelist",
        "personalization": "Personalization rules",
        "health_checks": "Health checks",
        "summary": "Summary",
        "passed": "passed",
        "warnings": "warning(s)",
        "errors_count": "error(s)",
        "severity": "Severity",
        "check": "Check",
        "finding": "Finding",
        "next_steps": "Next steps",
        "none": "— (none)",
        "item": "Item",
        "value": "Value",
        "drift_advice": "Drift advice",
    },
    "zh": {
        "title": "Iterate 项目报告",
        "tagline": "由 `iterate report` 生成",
        "project": "项目",
        "skill_version": "Skill 版本",
        "generated": "生成时间",
        "onboarding": "Onboarding",
        "onboarded": "已完成",
        "not_onboarded": "未初始化",
        "channel": "通道",
        "completed": "完成于",
        "health": "健康状态",
        "healthy": "健康",
        "warnings_only": "健康但有警告",
        "errors": "需要处理",
        "drift": "漂移",
        "drift_none": "未检测到漂移",
        "drift_unknown": "未知（没有指纹基线）",
        "drift_disabled": "检查已关闭",
        "tech_stack": "技术栈",
        "languages": "语言",
        "manifests": "Manifest",
        "package_managers": "包管理器",
        "features": "特性",
        "configuration": "审查配置",
        "target_branch": "目标分支",
        "review_scope": "审查范围",
        "max_rounds": "最大轮数",
        "dimensions": "审查维度",
        "dimension_sets": "维度集",
        "validation": "校验命令",
        "whitelist": "命令白名单",
        "personalization": "个性化规则",
        "health_checks": "健康检查",
        "summary": "汇总",
        "passed": "通过",
        "warnings": "警告",
        "errors_count": "错误",
        "severity": "级别",
        "check": "检查项",
        "finding": "结果",
        "next_steps": "下一步",
        "none": "—（无）",
        "item": "项目",
        "value": "值",
        "drift_advice": "漂移建议",
    },
}

_SEVERITY_ICONS = {"error": "❌", "warn": "⚠️", "ok": "✅"}


def _language(show: dict[str, Any]) -> str:
    """Pick the report language from the project's resolved config."""
    config = show.get("config")
    if isinstance(config, dict):
        value = config.get("language")
        if value in ("zh", "en"):
            return value
    return "en"


def _cell(value: Any) -> str:
    """Make a value safe for a GFM table cell (pipes/newlines/markup)."""
    text = "—" if value is None or value == "" else str(value)
    text = text.replace("\\", "\\\\").replace("|", "\\|")
    # A stray backtick in a finding/config value would otherwise open a code
    # span that swallows the rest of the document (or the next table rows).
    text = text.replace("`", "\\`")
    # GFM allows raw inline HTML, so a project-controlled value such as
    # `<img src=x onerror=...>` must not be able to inject markup into a
    # report pasted into an issue or rendered by a non-sanitising viewer.
    text = (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )
    text = text.replace("\r", " ").replace("\n", " ").strip()
    return text


def _code(value: Any) -> str:
    """Render a table cell as inline code when it is a simple scalar."""
    raw = "—" if value is None or value == "" else str(value)
    # Inline code cannot contain a literal backtick without a longer fence, and
    # wrapping an escaped one would display the backslash. Raw HTML is literal
    # inside a code span but would be escaped by _cell, so fall back for both.
    if "`" in raw or "\n" in raw or "\r" in raw or "<" in raw or ">" in raw:
        return _cell(value)
    text = raw.replace("\\", "\\\\").replace("|", "\\|")
    return f"`{text}`" if text != "—" else text


def _join(items: Any, empty: str) -> str:
    if not isinstance(items, (list, tuple)):
        return empty
    values = [str(item) for item in items if str(item).strip()]
    return ", ".join(values) if values else empty


def _count_personalization(show: dict[str, Any]) -> int:
    """Count structured personalization rules in the collected show data."""
    return count_personalization_rules(show.get("personalization"))


def _validation_summary(config: dict[str, Any], empty: str) -> str:
    validation = config.get("validation")
    if not isinstance(validation, dict):
        return empty
    commands = validation.get("commands")
    if not isinstance(commands, dict) or not commands:
        return empty
    parts = [
        f"{module}: {len(cmds)}"
        for module, cmds in sorted(commands.items())
        if isinstance(cmds, list)
    ]
    return ", ".join(parts) if parts else empty


def _dimension_set_names(config: dict[str, Any]) -> list[str]:
    """Return configured dimension-set names, tolerating a hand-edited value."""
    sets = config.get("dimension_sets")
    if not isinstance(sets, dict):
        return []
    return sorted(str(name) for name in sets)


def _whitelist(config: dict[str, Any]) -> list[Any]:
    """Return the configured command whitelist, tolerating malformed values."""
    validation = config.get("validation")
    if not isinstance(validation, dict):
        return []
    whitelist = validation.get("command_whitelist")
    return whitelist if isinstance(whitelist, list) else []


def _feature_names(scan: dict[str, Any]) -> list[str]:
    """Return the human names of the enabled ``has_*`` feature flags."""
    labels = {
        "has_specs": "specs",
        "has_tests": "tests",
        "has_ci": "CI",
        "has_frontend": "frontend",
        "has_api": "API",
    }
    return [label for key, label in labels.items() if scan.get(key) is True]


def _next_actions(report: dict[str, Any]) -> list[str]:
    """Actionable commands for the state the report describes."""
    actions: list[str] = []
    # `_cmd_init` refuses to run when iterate.config.yaml exists but cannot be
    # parsed, so `doctor --fix` (which repairs the config) must be suggested
    # before `init --yes` in the corrupt-config + not-onboarded state.
    if report.get("config_error"):
        actions.append("iterate doctor --fix")
    if not report["onboarded"]:
        actions.append("iterate init --yes")
    drift = report.get("drift")
    if drift not in (None, "none", "unknown", "disabled"):
        actions.append("iterate refresh")
    if report["summary"]["errors"] or report["summary"]["warnings"]:
        actions.append("iterate doctor")
    # --strict only adds value when warnings (not errors) are the blocker: with
    # errors present plain `doctor` already gates on every non-clean state, so
    # suggesting both would be a redundant duplicate of the same command.
    if report["summary"]["blocking"] and not report["summary"]["errors"]:
        actions.append("iterate doctor --strict")
    if not actions:
        actions.extend(["iterate status", "iterate scan --json"])
    return actions


def build_report(
    project_root: Path,
    *,
    strict: bool = False,
    now: datetime | None = None,
) -> dict[str, Any]:
    """Collect the aggregated report for ``project_root``.

    Args:
        project_root: Project root directory (the CLI validates it exists).
        strict: When True, warnings also make the report blocking, exactly
            like ``doctor --strict``.
        now: Timestamp override for deterministic tests. Defaults to the
            current UTC time.

    Returns:
        A JSON-serialisable dict. Every key is present on every project state
        (including not-onboarded ones) so ``--json`` consumers can index
        unconditionally, matching the stable-key promise of ``status`` /
        ``show``.
    """
    show = collect_show_data(project_root)
    scan = collect_scan_data(project_root)
    doctor = run_doctor(project_root)
    lang = _language(show)
    config = show.get("config") if isinstance(show.get("config"), dict) else {}

    errors = sum(1 for f in doctor.findings if f.severity == "error")
    warnings = sum(1 for f in doctor.findings if f.severity == "warn")
    passed = sum(1 for f in doctor.findings if f.severity == "ok")
    blocking = errors > 0 or (strict and warnings > 0)
    if blocking:
        health = "errors" if errors else "warnings"
    elif warnings:
        health = "warnings"
    else:
        health = "healthy"

    timestamp = (now or datetime.now(timezone.utc)).astimezone(timezone.utc)
    report: dict[str, Any] = {
        "ok": not blocking,
        "command": "report",
        "project": str(project_root),
        "skill_version": __version__,
        "generated_at": timestamp.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "language": lang,
        "strict": strict,
        "onboarded": bool(show.get("onboarded")),
        "config_error": bool(show.get("config_error")),
        "config_missing": bool(show.get("config_missing")),
        "onboarding": show.get("onboarding", {}),
        "config": config,
        "personalization_rules": _count_personalization(show),
        "drift": show.get("drift", "unknown"),
        "drift_advice": show.get("drift_advice"),
        "features": _feature_names(scan),
        "scan": {
            key: scan.get(key)
            for key in (
                "manifests",
                "detected_languages",
                "detected_package_managers",
                "top_level_dirs",
                "has_specs",
                "has_tests",
                "has_ci",
                "has_frontend",
                "has_api",
                "suggested_dimensions",
            )
        },
        "doctor": doctor.to_dict(strict=strict),
        "summary": {
            "passed": passed,
            "warnings": warnings,
            "errors": errors,
            "blocking": blocking,
            "health": health,
        },
    }
    report["next_actions"] = _next_actions(report)
    return report


def _status_line(report: dict[str, Any], labels: dict[str, str]) -> str:
    summary = report["summary"]
    if summary["health"] == "errors":
        head = labels["errors"]
    elif summary["health"] == "warnings":
        head = labels["warnings_only"]
    else:
        head = labels["healthy"]
    return (
        f"{head} — {summary['passed']} {labels['passed']}, "
        f"{summary['warnings']} {labels['warnings']}, "
        f"{summary['errors']} {labels['errors_count']}"
    )


def _drift_line(report: dict[str, Any], labels: dict[str, str]) -> str:
    drift = report.get("drift")
    if drift == "none":
        return labels["drift_none"]
    if drift == "disabled":
        return labels["drift_disabled"]
    if drift in (None, "unknown"):
        return labels["drift_unknown"]
    return _cell(str(drift))


def render_markdown(report: dict[str, Any]) -> str:
    """Render a report dict as a self-contained GFM Markdown document.

    The output is deterministic (apart from ``generated_at``) and safe to paste
    into a PR/issue: pipes and newlines in findings are escaped, and every
    section has an explicit empty value instead of a blank cell.

    Args:
        report: A value returned by :func:`build_report`.

    Returns:
        Markdown text ending in a newline.
    """
    lang = report.get("language", "en")
    labels = _LABELS.get(lang, _LABELS["en"])
    none = labels["none"]
    onboarding = report.get("onboarding") or {}
    config = report.get("config") or {}
    scan = report.get("scan") or {}
    doctor = report.get("doctor") or {}
    findings = doctor.get("findings") or []

    if report["onboarded"]:
        onboarding_value = labels["onboarded"]
        details = []
        if onboarding.get("channel") not in (None, "", "unknown"):
            details.append(f"{labels['channel']}: {_cell(onboarding['channel'])}")
        if onboarding.get("completed_at") not in (None, "", "unknown"):
            details.append(
                f"{labels['completed']}: {_cell(onboarding['completed_at'])}"
            )
        if details:
            onboarding_value += f" ({', '.join(details)})"
    else:
        onboarding_value = labels["not_onboarded"]

    lines: list[str] = [
        f"# {labels['title']}",
        "",
        (
            f"> {labels['tagline']} · iterate {_cell(report.get('skill_version'))} "
            f"· {_cell(report.get('generated_at'))}"
        ),
        "",
        f"- **{labels['project']}**: {_code(report.get('project'))}",
        f"- **{labels['onboarding']}**: {onboarding_value}",
        f"- **{labels['health']}**: {_status_line(report, labels)}",
        f"- **{labels['drift']}**: {_drift_line(report, labels)}",
        "",
        f"## {labels['tech_stack']}",
        "",
        f"| {labels['item']} | {labels['value']} |",
        "|---|---|",
        f"| {labels['languages']} | {_cell(_join(scan.get('detected_languages'), none))} |",
        f"| {labels['manifests']} | {_cell(_join(scan.get('manifests'), none))} |",
        (
            f"| {labels['package_managers']} | "
            f"{_cell(_join(scan.get('detected_package_managers'), none))} |"
        ),
        f"| {labels['features']} | {_cell(_join(report.get('features'), none))} |",
        "",
        f"## {labels['configuration']}",
        "",
        f"| {labels['item']} | {labels['value']} |",
        "|---|---|",
        f"| {labels['target_branch']} | {_code(config.get('target_branch', '—'))} |",
        f"| {labels['review_scope']} | {_code(config.get('review_scope', '—'))} |",
        f"| {labels['max_rounds']} | {_code(config.get('max_rounds', '—'))} |",
        f"| {labels['dimensions']} | {_cell(_join(config.get('dimensions'), none))} |",
        (
            f"| {labels['dimension_sets']} | "
            f"{_cell(_join(_dimension_set_names(config), none))} |"
        ),
        (
            f"| {labels['validation']} | "
            f"{_cell(_validation_summary(config, none))} |"
        ),
        (
            f"| {labels['whitelist']} | "
            f"{_cell(_join(_whitelist(config), none))} |"
        ),
        f"| {labels['personalization']} | {report.get('personalization_rules', 0)} |",
        "",
        f"## {labels['health_checks']}",
        "",
        f"**{labels['summary']}**: {_status_line(report, labels)}",
        "",
    ]

    if findings:
        lines.extend(
            [
                f"| {labels['severity']} | {labels['check']} | {labels['finding']} |",
                "|---|---|---|",
            ]
        )
        for finding in findings:
            severity = str(finding.get("severity", ""))
            icon = _SEVERITY_ICONS.get(severity, severity)
            message = _cell(finding.get("message"))
            detail = _cell(finding.get("detail"))
            text = message if detail == "—" else f"{message}<br>{detail}"
            lines.append(
                f"| {icon} {_cell(severity)} | {_cell(finding.get('check'))} | {text} |"
            )
        lines.append("")
    else:
        lines.extend([none, ""])

    advice = report.get("drift_advice")
    if advice:
        lines.extend(
            [f"**{labels['drift_advice']}**: {_cell(advice)}", ""]
        )

    lines.append(f"## {labels['next_steps']}")
    lines.append("")
    for action in report.get("next_actions") or []:
        lines.append(f"- `{action}`")
    lines.append("")
    return "\n".join(lines)


def report_json(report: dict[str, Any]) -> str:
    """Serialise a report as pretty JSON with a trailing newline."""
    import json

    return json.dumps(report, ensure_ascii=False, indent=2, default=str) + "\n"
