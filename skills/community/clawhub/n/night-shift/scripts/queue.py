"""Queue manager — CRUD operations for night-shift plans."""

from __future__ import annotations

if __name__ == "queue" and "site-packages" in __file__:
    import importlib.util
    import sysconfig
    from pathlib import Path

    _stdlib_queue = Path(sysconfig.get_path("stdlib")) / "queue.py"
    _spec = importlib.util.spec_from_file_location("_stdlib_queue", _stdlib_queue)
    _module = importlib.util.module_from_spec(_spec)
    assert _spec and _spec.loader
    _spec.loader.exec_module(_module)
    globals().update(_module.__dict__)
else:
    import json
    import os
    from typing import Optional
    from pathlib import Path

    try:
        from .models import Plan, PlanStatus
        from .phase_generator import generate_phases
    except ImportError:
        from models import Plan, PlanStatus
        from phase_generator import generate_phases

    # Auto-detect workspace root
    _SKILL_DIR = Path(__file__).resolve().parent.parent  # skills/night-shift/
    _WORKSPACE = Path(os.environ.get("OPENCLAW_WORKSPACE", _SKILL_DIR.parent.parent))  # ~/.openclaw/workspace
    _DATA_DIR = _WORKSPACE / "data" / "night-shift"

    # Paths
    BASE_DIR = _DATA_DIR
    QUEUE_FILE = BASE_DIR / "queue.json"
    PLANS_DIR = BASE_DIR / "plans"



def _ensure_dirs():
    BASE_DIR.mkdir(parents=True, exist_ok=True)
    PLANS_DIR.mkdir(parents=True, exist_ok=True)


def _load_queue_index() -> dict:
    """Load the queue index (lightweight — id, title, status, priority, created_at only)."""
    if not QUEUE_FILE.exists():
        return {"version": 1, "plans": []}
    with open(QUEUE_FILE) as f:
        return json.load(f)


def _save_queue_index(index: dict):
    """Save the queue index."""
    _ensure_dirs()
    with open(QUEUE_FILE, "w") as f:
        json.dump(index, f, indent=2)


def _load_plan(plan_id: str) -> Optional[Plan]:
    """Load a full plan from its JSON file."""
    plan_file = PLANS_DIR / f"{plan_id}.json"
    if not plan_file.exists():
        return None
    try:
        with open(plan_file) as f:
            return Plan.from_dict(json.load(f))
    except (KeyError, ValueError, json.JSONDecodeError) as e:
        print(f"[WARN] Cannot load plan {plan_id}: {e}")
        return None


def _save_plan(plan: Plan):
    """Save a plan to its JSON file."""
    _ensure_dirs()
    plan_file = PLANS_DIR / f"{plan.id}.json"
    with open(plan_file, "w") as f:
        json.dump(plan.to_dict(), f, indent=2)


def _update_index_entry(plan: Plan):
    """Update or add a plan's entry in the queue index."""
    index = _load_queue_index()
    # Remove existing entry for this plan
    index["plans"] = [p for p in index["plans"] if p["id"] != plan.id]
    # Add updated entry
    index["plans"].append(
        {
            "id": plan.id,
            "title": plan.title,
            "status": plan.status.value,
            "priority": plan.priority,
            "created_at": plan.created_at,
            "phase_count": len(plan.phases),
            "repo_url": plan.repo_url,
        }
    )
    _save_queue_index(index)


def add_plan(
    title: str,
    description: str = "",
    repo_url: Optional[str] = None,
    priority: str = "medium",
    auto_approve: bool = False,
    max_retries: int = 2,
    token_budget: int = 100000,
    source: str = "telegram",
    source_message_id: Optional[int] = None,
) -> Plan:
    """Create a new plan with auto-generated phases."""
    _ensure_dirs()

    # Check for duplicate repo_url
    if repo_url:
        index = _load_queue_index()
        for entry in index["plans"]:
            if entry.get("repo_url") == repo_url and entry["status"] in (
                "queued",
                "approved",
            ):
                raise ValueError(
                    f"Repo {repo_url} already queued as {entry['id']}. "
                    f"Remove it first or use a different description."
                )

    plan = Plan(
        title=title,
        description=description,
        repo_url=repo_url,
        priority=priority,
        auto_approve=auto_approve,
        max_retries=max_retries,
        token_budget=token_budget,
        source=source,
        source_message_id=source_message_id,
    )

    # Auto-generate phases
    plan.phases = generate_phases(title, description, repo_url, plan.id)

    # Save
    _save_plan(plan)
    _update_index_entry(plan)

    return plan


def list_plans(status_filter: Optional[str] = None) -> list[dict]:
    """List plans with optional status filter. Returns lightweight index entries."""
    index = _load_queue_index()
    plans = index["plans"]

    if status_filter:
        status_filter = status_filter.lower()
        plans = [p for p in plans if p["status"] == status_filter]

    # Sort by priority weight (critical first), then by created_at
    priority_order = {"critical": 0, "high": 1, "medium": 2, "low": 3}
    plans.sort(key=lambda p: (priority_order.get(p.get("priority", "medium"), 99), p.get("created_at", "")))

    return plans


def get_plan(plan_id: str) -> Optional[Plan]:
    """Get a full plan by ID."""
    return _load_plan(plan_id) if plan_id else None


def approve_plan(plan_id: str) -> bool:
    """Mark a plan as approved for execution."""
    plan = _load_plan(plan_id)
    if not plan:
        return False
    if plan.status not in (PlanStatus.QUEUED, PlanStatus.FAILED):
        return False
    plan.status = PlanStatus.APPROVED
    _save_plan(plan)
    _update_index_entry(plan)
    return True


def approve_all() -> int:
    """Approve all queued plans. Returns count of approved plans."""
    index = _load_queue_index()
    count = 0
    for entry in index["plans"]:
        if entry["status"] == "queued":
            if approve_plan(entry["id"]):
                count += 1
    return count


def remove_plan(plan_id: str) -> bool:
    """Remove a plan (only queued/approved/failed plans can be removed)."""
    plan = _load_plan(plan_id)
    if not plan:
        return False
    if plan.status in (PlanStatus.EXECUTING,):
        raise ValueError(f"Cannot remove plan {plan_id}: currently executing")

    # Remove plan file
    plan_file = PLANS_DIR / f"{plan_id}.json"
    if plan_file.exists():
        plan_file.unlink()

    # Remove from index
    index = _load_queue_index()
    index["plans"] = [p for p in index["plans"] if p["id"] != plan_id]
    _save_queue_index(index)

    return True


def set_priority(plan_id: str, priority: str) -> bool:
    """Change a plan's priority."""
    plan = _load_plan(plan_id)
    if not plan:
        return False
    plan.priority = priority
    _save_plan(plan)
    _update_index_entry(plan)
    return True


def edit_phase(
    plan_id: str,
    phase_id: int,
    new_prompt: Optional[str] = None,
    new_title: Optional[str] = None,
    new_verification: Optional[str] = None,
    new_verification_config: Optional[dict] = None,
) -> bool:
    """Edit a specific phase of a plan."""
    plan = _load_plan(plan_id)
    if not plan:
        return False
    for phase in plan.phases:
        if phase.id == phase_id:
            if new_prompt:
                phase.prompt = new_prompt
            if new_title:
                phase.title = new_title
            if new_verification:
                phase.verification = new_verification
            if new_verification_config is not None:
                phase.verification_config = new_verification_config
            _save_plan(plan)
            return True
    return False


def reorder_phase(plan_id: str, phase_id: int, before_phase_id: int) -> bool:
    """Reorder phases — move phase_id to before before_phase_id."""
    plan = _load_plan(plan_id)
    if not plan:
        return False

    phases = plan.phases
    phase_idx = None
    before_idx = None

    for i, p in enumerate(phases):
        if p.id == phase_id:
            phase_idx = i
        if p.id == before_phase_id:
            before_idx = i

    if phase_idx is None or before_idx is None:
        return False

    # Remove phase from current position
    phase = phases.pop(phase_idx)
    # Adjust before_idx if needed
    if phase_idx < before_idx:
        before_idx -= 1
    # Insert at new position
    phases.insert(before_idx, phase)

    # Re-number phase IDs
    for i, p in enumerate(phases):
        p.id = i + 1

    # Update depends_on references
    old_to_new = {}
    for p in phases:
        old_to_new[p.id] = (
            p.id
        )  # IDs already renumbered, but depends_on might reference old IDs

    _save_plan(plan)
    return True


def get_approved_plans() -> list[Plan]:
    """Get all approved plans, sorted by priority."""
    index = _load_queue_index()
    approved_entries = [p for p in index["plans"] if p["status"] == "approved"]

    priority_order = {"critical": 0, "high": 1, "medium": 2, "low": 3}
    approved_entries.sort(
        key=lambda p: (priority_order.get(p["priority"], 99), p["created_at"])
    )

    plans = []
    for entry in approved_entries:
        plan = _load_plan(entry["id"])
        if plan:
            plans.append(plan)
    return plans


def get_next_plan() -> Optional[Plan]:
    """Get the highest-priority approved plan."""
    plans = get_approved_plans()
    return plans[0] if plans else None


# --- CLI interface for Telegram commands ---


def format_plan_list(plans: list[dict]) -> str:
    """Format plan list for Telegram display."""
    if not plans:
        return "📋 No plans in queue."

    lines = ["📋 **Night-Shift Queue**\n"]
    priority_icons = {"critical": "🔴", "high": "🟠", "medium": "🟡", "low": "🟢"}
    status_icons = {
        "queued": "⏳",
        "approved": "✅",
        "executing": "🔄",
        "completed": "✅",
        "failed": "❌",
        "skipped": "⏭️",
    }

    for p in plans:
        icon = priority_icons.get(p["priority"], "⚪")
        status = status_icons.get(p["status"], "❓")
        phases = p.get("phase_count", "?")
        repo = f" ({p['repo_url']})" if p.get("repo_url") else ""
        lines.append(f"{icon} {status} **#{p['id']}** — {p['title']}{repo}")
        lines.append(
            f"   Priority: {p['priority']} | Phases: {phases} | Created: {p['created_at'][:10]}"
        )

    return "\n".join(lines)


def format_plan_detail(plan: Plan) -> str:
    """Format full plan details for Telegram display."""
    lines = [
        f"📋 **Plan #{plan.id}** — {plan.title}",
        f"Status: {plan.status.value} | Priority: {plan.priority}",
        f"Branch: `{plan.branch}` | Base: `{plan.base_branch}`",
        f"Retries: {plan.max_retries} | Token budget: {plan.token_budget:,}",
        "",
        f"_{plan.description}_",
        "",
        "**Phases:**",
    ]

    for phase in plan.phases:
        status_icon = {
            "pending": "⬜",
            "running": "🔄",
            "passed": "✅",
            "failed": "❌",
            "skipped": "⏭️",
        }.get(phase.status.value, "❓")

        deps = (
            f" (after phase {', '.join(str(d) for d in phase.depends_on)})"
            if phase.depends_on
            else ""
        )
        lines.append(f"  {status_icon} Phase {phase.id}: {phase.title}{deps}")
        lines.append(
            f"     Verify: {phase.verification} | Est: {phase.estimated_tokens:,} tokens"
        )
        if phase.depends_on:
            lines.append(f"     Depends on: phases {phase.depends_on}")

    return "\n".join(lines)
