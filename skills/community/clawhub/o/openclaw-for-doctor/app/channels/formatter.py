from __future__ import annotations

from app.core.models import TaskResult


def format_task_result_message(result: TaskResult) -> str:
    lines = [
        f"[OpenClaw Doctor] Task {result.task_id}",
        f"Role: {result.role_stage.value} | Mode: {result.reasoning_mode.value}",
        f"Use-case: {result.use_case.value}",
        "",
        f"Summary: {result.summary}",
        "",
        "Action Plan:",
    ]

    for step in result.action_plan:
        lines.append(f"- {step}")

    if result.citations:
        lines.append("")
        lines.append("Evidence:")
        for citation in result.citations[:3]:
            lines.append(
                f"- {citation.source}: {citation.title} [{citation.evidence_level}]"
            )

    lines.append("")
    lines.append("Guardrails:")
    for guardrail in result.guardrails:
        lines.append(f"- {guardrail}")

    return "\n".join(lines)
