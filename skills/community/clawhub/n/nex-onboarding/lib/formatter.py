"""
Nex Onboarding - Output Formatting
MIT-0 License - Copyright 2026 Nex AI (Kevin Blancaflor)
"""

from typing import Dict, List, Optional


def format_progress(onboarding: Dict, progress: Dict) -> str:
    """Format onboarding progress with visual checklist."""
    lines = []

    # Header
    lines.append(f"Onboarding: {onboarding['client_name']}", )
    if onboarding["retainer_tier"]:
        lines.append(f"Tier: {onboarding['retainer_tier']}")
    if onboarding["assigned_to"]:
        lines.append(f"Assigned to: {onboarding['assigned_to']}")

    lines.append(f"Started: {onboarding['started_at'][:10]}")
    lines.append(f"Progress: {progress['percentage']}% ({progress['completed']}/{progress['total']})")
    lines.append("---")

    # Steps with visual indicators
    next_pending = None
    for step in onboarding["steps"]:
        status = step["status"]

        # Status symbol
        if status == "completed":
            symbol = "[x]"
        elif status == "in_progress":
            symbol = "[>]"
        elif status == "blocked":
            symbol = "[!]"
        elif status == "skipped":
            symbol = "[~]"
        else:  # pending
            symbol = "[ ]"
            if next_pending is None:
                next_pending = step

        # Format line
        step_num = str(step["step_number"]).rjust(2)
        title = step["title"]
        line = f" {symbol} {step_num}. {title}"

        # Add marker for next step
        if step == next_pending:
            line += "        <- NEXT"

        lines.append(line)

        # Add notes if blocked or has notes
        if status == "blocked" and step["notes"]:
            lines.append(f"         BLOCKED: {step['notes']}")
        elif status == "skipped" and step["notes"]:
            lines.append(f"         SKIPPED: {step['notes']}")

    lines.append("---")

    # Next step info
    if next_pending:
        lines.append(f"Next: Step {next_pending['step_number']} - {next_pending['title']}")
        if next_pending["description"]:
            lines.append(f"      {next_pending['description']}")
    else:
        lines.append("All steps completed!")

    return "\n".join(lines)


def format_onboarding_list(onboardings: List[Dict]) -> str:
    """Format list of onboardings."""
    if not onboardings:
        return "No onboardings found."

    lines = []
    lines.append(f"{'Client':<30} {'Status':<12} {'Tier':<12} {'Started':<12}")
    lines.append("-" * 66)

    for ob in onboardings:
        client = ob["client_name"][:29]
        status = ob["status"][:11]
        tier = (ob["retainer_tier"] or "-")[:11]
        started = ob["started_at"][:10]

        lines.append(f"{client:<30} {status:<12} {tier:<12} {started:<12}")

    return "\n".join(lines)


def format_step_detail(step: Dict) -> str:
    """Format a single step with details."""
    lines = []

    status_text = {
        "pending": "Pending",
        "in_progress": "In Progress",
        "completed": "Completed",
        "skipped": "Skipped",
        "blocked": "Blocked",
    }

    lines.append(f"Step {step['step_number']}: {step['title']}")
    lines.append(f"Status: {status_text.get(step['status'], step['status'])}")
    lines.append(f"Category: {step['category']}")
    lines.append(f"Required: {'Yes' if step['required'] else 'No'}")

    if step["description"]:
        lines.append(f"Description: {step['description']}")

    if step["notes"]:
        lines.append(f"Notes: {step['notes']}")

    if step["completed_at"]:
        lines.append(f"Completed: {step['completed_at']}")

    if step["completed_by"]:
        lines.append(f"Completed by: {step['completed_by']}")

    return "\n".join(lines)


def format_stats(stats: Dict) -> str:
    """Format statistics."""
    lines = []

    lines.append("Nex Onboarding Statistics")
    lines.append("=" * 40)
    lines.append("")

    lines.append("Overall")
    lines.append(f"  Total Onboardings: {stats['total_onboardings']}")
    lines.append(f"  Active: {stats['active_onboardings']}")
    lines.append(f"  Completed: {stats['completed_onboardings']}")
    lines.append(f"  Completion Rate: {stats['completion_rate']}%")
    lines.append("")

    lines.append("Steps")
    lines.append(f"  Total Steps Across All: {stats['total_steps']}")
    lines.append(f"  Completed: {stats['completed_steps']}")
    lines.append(f"  Blocked: {stats['blocked_steps']}")
    lines.append(f"  Completion Rate: {stats['step_completion_rate']}%")
    lines.append("")

    if stats["bottlenecks"]:
        lines.append("Bottleneck Steps")
        for bn in stats["bottlenecks"]:
            lines.append(f"  Step {bn['step']}: {bn['title']} ({bn['blocked_count']} blocked)")

    return "\n".join(lines)


def format_template_detail(template: Dict, steps: List[Dict]) -> str:
    """Format template with steps."""
    lines = []

    lines.append(f"Template: {template['name']}")
    lines.append(f"Description: {template['description']}")
    lines.append(f"Total Steps: {len(steps)}")
    lines.append("")

    for step in steps:
        required = "REQUIRED" if step["required"] else "optional"
        lines.append(f"{step['step']:2d}. {step['title']:<35} [{step['category']:<12}] {required}")
        lines.append(f"    {step['description']}")

    return "\n".join(lines)


def format_error(message: str) -> str:
    """Format error message."""
    return f"Error: {message}"


def format_success(message: str) -> str:
    """Format success message."""
    return f"✓ {message}"
