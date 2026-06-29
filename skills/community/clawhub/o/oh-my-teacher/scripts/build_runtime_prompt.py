#!/usr/bin/env python3
"""Bundle Oh My Teacher references into a single runtime prompt.

Useful when deploying the skill to environments that do not support multi-file
reference loading, such as custom GPTs, Dify custom tools, or generic agent
system prompts.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REGISTRY_PATH = Path("agents") / "registry.json"

# Files to include (in order) and the context tag to prepend.
INCLUDE_ORDER: list[tuple[str, str]] = [
    ("SKILL.md", "=== SKILL.md (operating principle + command routing) ==="),
    ("references/agent-adapter-contract.md", "=== agent-adapter-contract.md (multi-agent contract) ==="),
    ("references/agent-optimization.md", "=== agent-optimization.md (capability optimization paths) ==="),
    ("references/agent-inventory.md", "=== agent-inventory.md (agent capability inventory) ==="),
    ("references/staged-review-workflow.md", "=== staged-review-workflow.md (phased exam-prep workflow) ==="),
    ("references/focus-feedback-iteration.md", "=== focus-feedback-iteration.md (active review loop) ==="),
    ("references/opt-in-reminders.md", "=== opt-in-reminders.md (explicit reminders + knowledge digests) ==="),
    ("references/INDEX.md", "=== INDEX.md (reference map + command catalog + environment fallbacks) ==="),
    ("references/environment-adaptation.md", "=== environment-adaptation.md (capability detection + fallbacks) ==="),
    ("references/course-profiles.md", "=== course-profiles.md (snapshot template + exam optimization) ==="),
    ("references/interaction-modes.md", "=== interaction-modes.md (teaching modes) ==="),
    ("references/subject-adaptation.md", "=== subject-adaptation.md (subject-specific adaptation) ==="),
    ("references/question-types.md", "=== question-types.md (question types + grading rubric) ==="),
    ("references/practice-workflows.md", "=== practice-workflows.md (active recall + mock + oral + error repair) ==="),
    ("references/review-plans.md", "=== review-plans.md (plans + cram + last page) ==="),
    ("references/spaced-repetition.md", "=== spaced-repetition.md (SRS algorithm) ==="),
    ("references/visual-generation.md", "=== visual-generation.md (visual + image + video) ==="),
    ("references/coding-demos.md", "=== coding-demos.md (code demo guidelines) ==="),
    ("references/materials-ingestion.md", "=== materials-ingestion.md (file ingestion) ==="),
]


def load_registry(skill_root: Path) -> dict:
    registry_path = skill_root / REGISTRY_PATH
    try:
        registry = json.loads(registry_path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ValueError(f"Agent registry not found: {registry_path}") from exc
    except json.JSONDecodeError as exc:
        raise ValueError(f"Agent registry is invalid JSON: {exc}") from exc
    if not isinstance(registry.get("agents"), list):
        raise ValueError("Agent registry must contain an agents list.")
    return registry


def agent_entries(skill_root: Path) -> dict[str, dict]:
    registry = load_registry(skill_root)
    entries: dict[str, dict] = {}
    for entry in registry["agents"]:
        agent_id = entry.get("id")
        if not isinstance(agent_id, str) or not agent_id:
            raise ValueError("Each registry agent must have a non-empty id.")
        if agent_id in entries:
            raise ValueError(f"Duplicate agent id in registry: {agent_id}")
        entries[agent_id] = entry
    return entries


def list_agents(skill_root: Path) -> str:
    entries = agent_entries(skill_root)
    lines = ["Available agents:"]
    for agent_id in sorted(entries):
        entry = entries[agent_id]
        lines.append(f"- {agent_id}: {entry.get('display_name', agent_id)}")
    return "\n".join(lines)


def read_resource(skill_root: Path, rel_path: str, skip_optional: bool) -> str | None:
    full_path = skill_root / rel_path
    if not full_path.exists():
        if not skip_optional:
            print(f"Warning: {full_path} not found, skipping.", file=sys.stderr)
        return None
    text = full_path.read_text(encoding="utf-8")
    if rel_path == "SKILL.md" and text.startswith("---\n"):
        try:
            _, _, rest = text.split("---", 2)
            text = rest.lstrip("\n")
        except ValueError:
            pass
    return text.strip()


def build(skill_root: Path, skip_optional: bool = False, agent: str = "generic") -> str:
    entries = agent_entries(skill_root)
    if agent not in entries:
        known = ", ".join(sorted(entries))
        raise ValueError(f"Unknown agent {agent!r}. Known agents: {known}")
    entry = entries[agent]

    parts: list[str] = []
    parts.append("# Oh My Teacher - Bundled Runtime Prompt")
    parts.append("")
    parts.append(f"Generated from: {skill_root.resolve()}")
    parts.append(f"Agent: {entry.get('id')} ({entry.get('display_name', entry.get('id'))})")
    parts.append(f"Source status: {entry.get('source_status', 'unknown')}")
    profiles = entry.get("optimization_profiles", [])
    if profiles:
        parts.append("Optimization profiles: " + ", ".join(profiles))
    parts.append("")

    adapter_path = entry.get("adapter_path")
    if not isinstance(adapter_path, str) or not adapter_path:
        raise ValueError(f"Agent {agent!r} must define adapter_path.")
    adapter_text = read_resource(skill_root, adapter_path, skip_optional)
    if adapter_text:
        parts.append(f"=== {adapter_path} (agent adapter) ===")
        parts.append("")
        parts.append(adapter_text)
        parts.append("")

    registry_text = read_resource(skill_root, str(REGISTRY_PATH), skip_optional)
    if registry_text:
        parts.append("=== agents/registry.json (agent registry) ===")
        parts.append("")
        parts.append(registry_text)
        parts.append("")

    for rel_path, header in INCLUDE_ORDER:
        text = read_resource(skill_root, rel_path, skip_optional)
        if text is None:
            continue
        parts.append(header)
        parts.append("")
        parts.append(text)
        parts.append("")

    return "\n".join(parts)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build a bundled system prompt from Oh My Teacher references.")
    parser.add_argument("--root", default=".", help="Skill root directory (default: current dir).")
    parser.add_argument("--output", "-o", help="Output file (default: stdout).")
    parser.add_argument("--agent", default="generic", help="Agent id from agents/registry.json (default: generic).")
    parser.add_argument("--list-agents", action="store_true", help="List known agent ids and exit.")
    parser.add_argument("--skip-optional", action="store_true", help="Silently skip missing files instead of warning.")
    args = parser.parse_args(argv)

    root = Path(args.root).resolve()
    try:
        if args.list_agents:
            print(list_agents(root))
            return 0
        prompt = build(root, skip_optional=args.skip_optional, agent=args.agent)
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    if args.output:
        Path(args.output).write_text(prompt, encoding="utf-8")
        print(f"Bundled prompt written to {args.output} for agent {args.agent} ({len(prompt)} chars)", file=sys.stderr)
    else:
        sys.stdout.write(prompt)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
