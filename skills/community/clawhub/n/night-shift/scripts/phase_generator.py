"""Phase auto-generator — breaks tasks into verifiable phases."""

from __future__ import annotations
import os
from pathlib import Path
from typing import Optional
try:
    from .models import Phase
except ImportError:
    from models import Phase

# Auto-detect workspace root
_SKILL_DIR = Path(__file__).resolve().parent.parent  # skills/night-shift/
_WORKSPACE = Path(os.environ.get("OPENCLAW_WORKSPACE", _SKILL_DIR.parent.parent))  # ~/.openclaw/workspace
_DATA_DIR = _WORKSPACE / "data" / "night-shift"
_WORKTREES_DIR = _DATA_DIR / "worktrees"


# Templates for common task types
STEAL_REPO_PHASES = [
    {
        "title": "Clone and analyze repo",
        "description": "Clone repo, read key files (README, package.json, core modules), document architecture",
        "prompt_template": (
            "Clone {repo_url} into /tmp/night-shift/{plan_id}/staging/ and analyze its architecture.\n"
            "Focus on: core patterns, module structure, entry points, dependencies.\n"
            "Output: architecture doc at {worktree}/docs/{repo_name}-ARCHITECTURE.md"
        ),
        "verification": "check_files_exist",
        "verification_paths": ["docs/{repo_name}-ARCHITECTURE.md"],
        "estimated_tokens": 30000,
    },
    {
        "title": "Extract reusable patterns",
        "description": "Identify and extract core patterns into reusable modules",
        "prompt_template": (
            "From the {repo_name} analysis, extract core reusable patterns.\n"
            "Create Python modules in {worktree}/skills/night-shift/patterns/.\n"
            "Each pattern should be a self-contained module with docstring and usage example."
        ),
        "verification": "import_check",
        "verification_config": {"module": "patterns"},
        "estimated_tokens": 40000,
        "depends_on": [1],
    },
    {
        "title": "Integrate as OpenClaw skill",
        "description": "Build SKILL.md, wire into OpenClaw, add tests",
        "prompt_template": (
            "Create a SKILL.md at {worktree}/skills/night-shift/SKILL.md\n"
            "Document: usage, commands, configuration, dependencies.\n"
            "Add tests at {worktree}/skills/night-shift/tests/ if applicable."
        ),
        "verification": "check_files_exist",
        "verification_paths": ["skills/night-shift/SKILL.md"],
        "estimated_tokens": 30000,
        "depends_on": [2],
    },
]

BUILD_SKILL_PHASES = [
    {
        "title": "Design skill architecture",
        "description": "Define skill structure, data flow, and API surface",
        "prompt_template": (
            "Design the architecture for: {description}\n"
            "Output: architecture doc at {worktree}/skills/{skill_name}/ARCHITECTURE.md\n"
            "Include: module structure, data flow, API surface, dependencies."
        ),
        "verification": "check_files_exist",
        "verification_paths": ["skills/{skill_name}/ARCHITECTURE.md"],
        "estimated_tokens": 25000,
    },
    {
        "title": "Implement core logic",
        "description": "Build the main skill modules",
        "prompt_template": (
            "Implement the core logic for: {description}\n"
            "Working directory: {worktree}\n"
            "Create modules in skills/{skill_name}/ with proper error handling and logging."
        ),
        "verification": "import_check",
        "verification_config": {"module": "skills.{skill_name}"},
        "estimated_tokens": 50000,
        "depends_on": [1],
    },
    {
        "title": "Write tests",
        "description": "Create test suite for the skill",
        "prompt_template": (
            "Write tests for: {description}\n"
            "Create tests at {worktree}/skills/{skill_name}/tests/\n"
            "Cover: happy path, edge cases, error handling. Use pytest."
        ),
        "verification": "run_tests",
        "verification_config": {
            "command": "cd {worktree} && python3 -m pytest skills/{skill_name}/tests/ -v --tb=short 2>&1"
        },
        "estimated_tokens": 40000,
        "depends_on": [2],
    },
    {
        "title": "Document skill",
        "description": "Create SKILL.md with usage docs",
        "prompt_template": (
            "Create SKILL.md for: {description}\n"
            "Location: {worktree}/skills/{skill_name}/SKILL.md\n"
            "Include: purpose, commands, configuration, examples, dependencies."
        ),
        "verification": "check_files_exist",
        "verification_paths": ["skills/{skill_name}/SKILL.md"],
        "estimated_tokens": 20000,
        "depends_on": [3],
    },
]

REFACTOR_PHASES = [
    {
        "title": "Analyze existing code",
        "description": "Read and understand current implementation",
        "prompt_template": (
            "Analyze the current implementation at: {worktree}\n"
            "Target: {description}\n"
            "Document: current structure, pain points, coupling, test coverage gaps.\n"
            "Output: analysis at {worktree}/docs/refactor-analysis.md"
        ),
        "verification": "check_files_exist",
        "verification_paths": ["docs/refactor-analysis.md"],
        "estimated_tokens": 30000,
    },
    {
        "title": "Plan refactoring steps",
        "description": "Define specific changes with verification criteria",
        "prompt_template": (
            "Based on the refactor analysis, plan specific changes.\n"
            "For each change: what files, what changes, how to verify.\n"
            "Output: refactor plan at {worktree}/docs/refactor-plan.md"
        ),
        "verification": "check_files_exist",
        "verification_paths": ["docs/refactor-plan.md"],
        "estimated_tokens": 25000,
        "depends_on": [1],
    },
    {
        "title": "Execute refactoring",
        "description": "Apply changes incrementally",
        "prompt_template": (
            "Execute the refactoring plan at {worktree}/docs/refactor-plan.md\n"
            "Working directory: {worktree}\n"
            "Apply changes incrementally. Run tests after each change."
        ),
        "verification": "run_tests",
        "verification_config": {
            "command": "cd {worktree} && python3 -m pytest -x --tb=short 2>&1"
        },
        "estimated_tokens": 60000,
        "depends_on": [2],
    },
]

# Generic fallback phases
GENERIC_PHASES = [
    {
        "title": "Research and plan",
        "description": "Understand the task and create an execution plan",
        "prompt_template": (
            "Research and plan: {description}\n"
            "Output: execution plan at {worktree}/docs/plan.md"
        ),
        "verification": "check_files_exist",
        "verification_paths": ["docs/plan.md"],
        "estimated_tokens": 25000,
    },
    {
        "title": "Implement",
        "description": "Build the solution",
        "prompt_template": (
            "Implement: {description}\n"
            "Working directory: {worktree}\n"
            "Follow the plan at {worktree}/docs/plan.md if it exists."
        ),
        "verification": "check_git_diff",
        "verification_config": {},
        "estimated_tokens": 50000,
        "depends_on": [1],
    },
    {
        "title": "Verify and document",
        "description": "Run verification and create documentation",
        "prompt_template": (
            "Verify the implementation of: {description}\n"
            "Working directory: {worktree}\n"
            "Run any applicable tests. Create documentation."
        ),
        "verification": "check_git_diff",
        "verification_config": {},
        "estimated_tokens": 30000,
        "depends_on": [2],
    },
]


def detect_task_type(
    title: str, description: str, repo_url: Optional[str] = None
) -> str:
    """Detect the type of task from title/description/repo_url."""
    text = f"{title} {description}".lower()

    if repo_url:
        return "steal"

    steal_keywords = ["steal", "clone", "port", "migrate from", "copy from", "rip from"]
    if any(kw in text for kw in steal_keywords):
        return "steal"

    refactor_keywords = ["refactor", "rewrite", "clean up", "restructure", "simplify"]
    if any(kw in text for kw in refactor_keywords):
        return "refactor"

    build_keywords = ["build", "create", "make", "implement", "add", "write"]
    if any(kw in text for kw in build_keywords):
        return "build"

    return "generic"


def generate_phases(
    title: str,
    description: str,
    repo_url: Optional[str] = None,
    plan_id: Optional[str] = None,
) -> list[Phase]:
    """Generate phases for a plan based on task type detection."""

    task_type = detect_task_type(title, description, repo_url)
    pid = plan_id or "plan-000"
    worktree = str(_WORKTREES_DIR / pid)

    # Select template
    if task_type == "steal" and repo_url:
        template = STEAL_REPO_PHASES
        repo_name = repo_url.rstrip("/").split("/")[-1].replace(".git", "")
        context = {
            "repo_url": repo_url,
            "repo_name": repo_name,
            "plan_id": pid,
            "worktree": worktree,
        }
    elif task_type == "refactor":
        template = REFACTOR_PHASES
        context = {"description": description, "worktree": worktree}
    elif task_type == "build":
        template = BUILD_SKILL_PHASES
        # Extract skill name from title
        skill_name = title.lower().split()
        skill_name = "-".join(skill_name[:3]) if skill_name else "new-skill"
        context = {
            "description": description,
            "skill_name": skill_name,
            "worktree": worktree,
        }
    else:
        template = GENERIC_PHASES
        context = {"description": description, "worktree": worktree}

    # Build Phase objects from template
    phases = []
    for tpl in template:
        prompt = tpl["prompt_template"].format(**context)

        verification_config = {}
        if "verification_paths" in tpl:
            paths = [p.format(**context) for p in tpl["verification_paths"]]
            verification_config["paths"] = paths
        elif "verification_config" in tpl:
            verification_config = {
                k: v.format(**context) if isinstance(v, str) else v
                for k, v in tpl["verification_config"].items()
            }

        phase = Phase(
            id=tpl.get("id", len(phases) + 1),
            title=tpl["title"],
            prompt=prompt,
            description=tpl["description"],
            verification=tpl.get("verification", "none"),
            verification_config=verification_config,
            estimated_tokens=tpl.get("estimated_tokens", 30000),
            depends_on=tpl.get("depends_on", []),
            execution_method=tpl.get("execution_method", "cursor"),
        )
        phases.append(phase)

    return phases


def generate_phases_from_custom(
    prompt_text: str, plan_id: str = "plan-000"
) -> list[Phase]:
    """Generate phases from a free-form prompt (fallback)."""
    worktree = str(_WORKTREES_DIR / plan_id)
    return [
        Phase(
            id=1,
            title="Research and plan",
            prompt=f"Research and create a plan for: {prompt_text}\nOutput: docs/plan.md",
            description="Understand the task and create an execution plan",
            verification="check_files_exist",
            verification_config={"paths": ["docs/plan.md"]},
            estimated_tokens=25000,
        ),
        Phase(
            id=2,
            title="Implement",
            prompt=f"Implement: {prompt_text}\nWorking directory: {worktree}\nFollow docs/plan.md if it exists.",
            description="Build the solution",
            verification="check_git_diff",
            verification_config={},
            estimated_tokens=50000,
            depends_on=[1],
        ),
        Phase(
            id=3,
            title="Verify and document",
            prompt=f"Verify and document the implementation of: {prompt_text}",
            description="Run verification and create documentation",
            verification="check_git_diff",
            verification_config={},
            estimated_tokens=30000,
            depends_on=[2],
        ),
    ]
