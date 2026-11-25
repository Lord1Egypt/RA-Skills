"""GitHub Actions workflow-command (annotation) output for iterate diagnostics.

``iterate doctor`` and ``iterate report`` are CI-facing commands: they run in
GitHub Actions, exit non-zero when findings exist, and can be consumed by
scripts via ``--json``. But plain text/JSON output does not surface *where* in
the diff a problem lives — the developer sees a red check and has to open the
job log to learn which check failed.

GitHub Actions solves this with workflow commands (``::error …``,
``::warning …``), which GitHub renders as inline annotations on the PR's
"Files changed" / "Checks" view. This module turns iterate's doctor findings
into those commands so a failing ``iterate doctor`` in CI annotates the diff
directly, with the exact check name and message — no log-diving.

Everything here writes to **stderr** on purpose. ``doctor`` and ``report``
reserve stdout for the machine document (the global ``--json`` / ``--out``
contract), so annotations must never corrupt it. GitHub parses workflow
commands from either stream, so stderr keeps stdout byte-identical while the
annotations still appear in the PR.

The module is a pure formatter plus a tiny emit helper: it has no dependency
on the doctor/report modules, so the escaping and the mapping from a finding
to an annotation are unit-testable in isolation and reusable by any future
diagnostic command.
"""

from __future__ import annotations

import os
import sys
from collections.abc import Iterable
from dataclasses import dataclass
from typing import Any, TextIO

#: GitHub Actions treats only these as renderable annotation levels. The
#: ``notice`` level is deliberately not produced from findings (a passing check
#: is not a problem worth annotating), but it is a valid render target.
_SEVERITIES = frozenset({"notice", "warning", "error"})

#: Map an iterate finding severity to the GitHub annotation level.
_SEVERITY_MAP = {"ok": "notice", "warn": "warning", "error": "error"}

#: Findings whose subject is ITERATE.md rather than the config. Everything else
#: maps to ``iterate.config.yaml`` (the config is the anchor of every other
#: doctor check, and the message itself names the specific problem).
_ITERATE_MD_CHECKS = frozenset({"iterate.md.markers", "onboarding"})


def escape_message(value: str) -> str:
    """Escape a workflow-command **message** (the text after ``::``).

    ``%`` is escaped first so a literal ``%25`` in a message round-trips
    instead of being decoded a second time by the runner.
    """
    return value.replace("%", "%25").replace("\r", "%0D").replace("\n", "%0A")


def escape_property(value: str) -> str:
    """Escape a workflow-command **property value** (inside ``key=value``).

    Adds ``:`` and ``,`` on top of :func:`escape_message`, because those
    delimit the ``k=v,k2=v2`` property list.
    """
    return escape_message(value).replace(":", "%3A").replace(",", "%2C")


@dataclass(frozen=True)
class Annotation:
    """A single workflow command, ready to render.

    ``severity`` must be one of :data:`_SEVERITIES`. ``file`` / ``line`` are
    optional: GitHub renders an annotation without them as a job-level message,
    and with them as an inline comment anchored to that file/line.
    """

    severity: str
    message: str
    file: str | None = None
    line: int | None = None

    def __post_init__(self) -> None:
        if self.severity not in _SEVERITIES:
            raise ValueError(f"invalid annotation severity: {self.severity!r}")


def render(annotation: Annotation) -> str:
    """Render an :class:`Annotation` as a single workflow-command line."""
    properties: list[str] = []
    if annotation.file:
        properties.append(f"file={escape_property(annotation.file)}")
    if annotation.line is not None:
        properties.append(f"line={annotation.line}")
    command = f"::{annotation.severity}"
    if properties:
        command += " " + ",".join(properties)
    command += f"::{escape_message(annotation.message)}"
    return command


def emit(
    annotations: Iterable[Annotation],
    *,
    stream: TextIO | None = None,
) -> int:
    """Write annotations, one line each, and return how many were written.

    Defaults to **stderr** (see the module docstring for why stdout is wrong):
    ``doctor`` / ``report`` own stdout for the JSON/Markdown document, and
    GitHub parses workflow commands from either stream anyway.
    """
    out = stream if stream is not None else sys.stderr
    count = 0
    for annotation in annotations:
        out.write(render(annotation) + "\n")
        count += 1
    return count


def _finding_message(finding: Any) -> str:
    """Best-effort human message for a finding (object or mapping)."""
    if isinstance(finding, dict):
        message = finding.get("message", "")
    else:
        message = getattr(finding, "message", "")
    text = str(message).strip()
    return text or "iterate diagnostic finding"


def _finding_check(finding: Any) -> str:
    """Return the finding's check name (object or mapping), or ''."""
    if isinstance(finding, dict):
        value = finding.get("check", "")
    else:
        value = getattr(finding, "check", "")
    return str(value or "")


def _finding_severity(finding: Any) -> str:
    """Return the finding's severity (object or mapping), or ''."""
    if isinstance(finding, dict):
        value = finding.get("severity", "")
    else:
        value = getattr(finding, "severity", "")
    return str(value or "")


def annotations_from_findings(findings: Iterable[Any]) -> list[Annotation]:
    """Map iterate findings to GitHub annotations.

    ``findings`` items may be :class:`~iterate_cli.doctor.DoctorFinding`
    objects or plain mappings with ``severity`` / ``check`` / ``message``
    (the shape ``doctor`` and ``report`` expose under ``--json``).

    Passing findings are skipped: a green check is not a problem, and
    annotating it would add noise to every healthy run.
    """
    annotations: list[Annotation] = []
    for finding in findings:
        severity = _SEVERITY_MAP.get(_finding_severity(finding))
        if severity is None or severity == "notice":
            continue
        check = _finding_check(finding)
        file_name = "ITERATE.md" if check in _ITERATE_MD_CHECKS else "iterate.config.yaml"
        annotations.append(
            Annotation(
                severity=severity,
                message=_finding_message(finding),
                file=file_name,
            )
        )
    return annotations


def enabled_from_args(annotate: bool | None) -> bool:
    """Decide whether annotations should be emitted for a run.

    Args:
        annotate: Tri-state from the CLI: ``True`` (``--annotate``), ``False``
            (``--no-annotate``), or ``None`` (auto-detect).

    Returns:
        ``True`` when annotations should be emitted. The explicit flags win;
        otherwise the run auto-detects GitHub Actions via ``GITHUB_ACTIONS``,
        so a plain ``iterate doctor`` in a workflow annotates the diff without
        the user having to remember a flag — and ``iterate doctor
        --no-annotate`` still silences it for the rare team that wants plain
        job logs.
    """
    if annotate is True:
        return True
    if annotate is False:
        return False
    return os.environ.get("GITHUB_ACTIONS", "").strip().lower() == "true"
