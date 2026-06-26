"""Structured diagnostics are the single source of truth for governance findings."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class StructuredDiagnostic:
    diagnosis_type: str
    severity: str
    primary_cause: str
    secondary_contributors: list[str] = field(default_factory=list)
    capability_family: str | None = None
    target_classes_involved: list[str] = field(default_factory=list)
    artifacts_involved: list[str] = field(default_factory=list)
    provisional: bool = False
    coverage_gaps: list[str] = field(default_factory=list)
    repair_hints: list[str] = field(default_factory=list)


def render_summary(diagnostic: StructuredDiagnostic) -> list[str]:
    lines = [
        f"{diagnostic.severity} {diagnostic.diagnosis_type}: {diagnostic.primary_cause}",
    ]

    if diagnostic.capability_family is not None:
        lines.append(f"capability_family: {diagnostic.capability_family}")

    if diagnostic.secondary_contributors:
        lines.append(
            "secondary_contributors: " + ", ".join(diagnostic.secondary_contributors)
        )

    if diagnostic.target_classes_involved:
        lines.append(
            "target_classes: " + ", ".join(diagnostic.target_classes_involved)
        )

    if diagnostic.artifacts_involved:
        lines.append(
            "artifacts: " + ", ".join(diagnostic.artifacts_involved)
        )

    if diagnostic.provisional:
        lines.append("provisional: true")

    if diagnostic.coverage_gaps:
        lines.append("coverage_gaps: " + ", ".join(diagnostic.coverage_gaps))

    if diagnostic.repair_hints:
        lines.append("repair_hints: " + " | ".join(diagnostic.repair_hints))

    return lines
