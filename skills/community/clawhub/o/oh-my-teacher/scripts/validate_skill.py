#!/usr/bin/env python3
"""Validate the Oh My Teacher skill package."""

from __future__ import annotations

import argparse
import ast
import json
import re
import sys
from pathlib import Path

COMMAND_RE = re.compile(r"(?<![\w/])/(?P<cmd>[a-z][a-z0-9-]*)(?![\w.-])")
INDEX_ROW_RE = re.compile(r"^\|\s*`(?P<command>/[a-z][a-z0-9-]*)(?:\s+[^`]*)?`\s*\|")
INDEX_REF_RE = re.compile(r"`([\w-]+\.md)`")
MOJIBAKE_MARKERS = ("????", "鈥", "鎺ㄧ悊", "鎬濈淮")
DANGEROUS_REASONING_PATTERNS = [
    "write your reasoning chain",
    "chain-of-thought",
    "use cot",
    "<thought>",
    "推理链",
    "思维链",
]
IMA_TOOLS = [
    "ask_user",
    "fetch",
    "file_edit",
    "file_read",
    "file_write",
    "provide_file",
    "memory_recall",
    "memory_write",
    "match",
    "search",
    "shell",
    "subagent_spawn",
    "task_plan",
    "use_skill",
]
IMA_SKILLS = [
    "ima-knowledge",
    "ima-note",
    "ima-ppt",
    "ima-report",
    "ima-skill-creator",
]
AGENT_ID_RE = re.compile(r"^[a-z][a-z0-9-]*$")
REQUIRED_AGENT_IDS = {
    "generic",
    "codex",
    "claude",
    "openclaw",
    "hermes",
    "workbuddy",
    "qoder-work",
    "trae",
}
ALLOWED_AGENT_SOURCE_STATUS = {"baseline", "official", "observed", "community", "unknown"}
ALLOWED_CAPABILITY_TAGS = {
    "file-read",
    "file-write",
    "shell",
    "sandbox",
    "search",
    "kb-retrieval",
    "citations",
    "memory",
    "task-plan",
    "subagents",
    "ide",
    "rendering",
    "proactive-message",
    "scheduler",
    "unknown",
}
ALLOWED_OPTIMIZATION_PROFILES = {
    "scripted-agent",
    "file-agent",
    "retrieval-agent",
    "memory-agent",
    "ide-agent",
    "visual-agent",
    "planner-agent",
    "delegating-agent",
    "reminder-agent",
    "prompt-agent",
}


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def frontmatter(skill_md: str) -> dict[str, str]:
    if not skill_md.startswith("---\n"):
        raise ValueError("SKILL.md must start with YAML frontmatter.")
    try:
        raw = skill_md.split("---", 2)[1]
    except IndexError as exc:
        raise ValueError("SKILL.md frontmatter is not closed.") from exc
    result: dict[str, str] = {}
    current_key: str | None = None
    for line in raw.splitlines():
        if not line.strip():
            continue
        if line.startswith((" ", "\t")):
            if current_key is not None:
                result[current_key] += "\n" + line.strip()
            continue
        if ":" not in line:
            raise ValueError(f"Invalid frontmatter line: {line!r}")
        key, value = line.split(":", 1)
        current_key = key.strip()
        result[current_key] = value.strip()
    return result


def commands_from_index(index_md: str) -> set[str]:
    commands: set[str] = set()
    for line in index_md.splitlines():
        match = INDEX_ROW_RE.match(line)
        if match:
            commands.add(match.group("command"))
    return commands


def commands_from_markdown(root: Path) -> dict[Path, set[str]]:
    found: dict[Path, set[str]] = {}
    for path in sorted(root.rglob("*.md")):
        if any(part == "__pycache__" for part in path.parts):
            continue
        text = read_text(path)
        commands = {"/" + match.group("cmd") for match in COMMAND_RE.finditer(text)}
        if commands:
            found[path] = commands
    return found


def course_template_keys(path: Path) -> set[str]:
    tree = ast.parse(read_text(path), filename=str(path))
    for node in tree.body:
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id == "TEMPLATES":
                    value = ast.literal_eval(node.value)
                    if isinstance(value, dict):
                        return {str(key) for key in value}
        if (
            isinstance(node, ast.AnnAssign)
            and isinstance(node.target, ast.Name)
            and node.target.id == "TEMPLATES"
            and node.value is not None
        ):
            value = ast.literal_eval(node.value)
            if isinstance(value, dict):
                return {str(key) for key in value}
    raise ValueError("TEMPLATES dict not found.")


def check(condition: bool, errors: list[str], message: str) -> None:
    if not condition:
        errors.append(message)


def validate_agent_configs(root: Path, errors: list[str]) -> None:
    agent_dir = root / "agents"
    for path in sorted(agent_dir.glob("*")):
        if path.suffix.lower() not in {".yaml", ".yml", ".json"}:
            continue
        text = read_text(path)
        lower = text.lower()
        hits = [pattern for pattern in DANGEROUS_REASONING_PATTERNS if pattern in lower]
        check(not hits, errors, f"{path.relative_to(root)} asks for hidden reasoning disclosure: {', '.join(hits)}")
        marker_hits = [marker for marker in MOJIBAKE_MARKERS if marker in text]
        check(not marker_hits, errors, f"{path.relative_to(root)} appears to contain mojibake: {', '.join(marker_hits)}")
        if path.suffix.lower() == ".json":
            try:
                json.loads(text)
            except json.JSONDecodeError as exc:
                errors.append(f"{path.relative_to(root)} is invalid JSON: {exc}")


def validate_ima_files(root: Path, index_commands: set[str], errors: list[str]) -> None:
    ima_agent = root / "agents" / "ima.yaml"
    ima_ref = root / "references" / "ima-adaptation.md"
    chinese_ref = root / "references" / "chinese-routing.md"
    check(ima_agent.exists(), errors, "Missing agents/ima.yaml.")
    check(ima_ref.exists(), errors, "Missing references/ima-adaptation.md.")
    check(chinese_ref.exists(), errors, "Missing references/chinese-routing.md.")
    if ima_agent.exists():
        agent_text = read_text(ima_agent)
        for phrase in ["SKILL.md", "ima-native", "search source=kb", "ima-note", "task_plan"]:
            check(phrase in agent_text, errors, f"agents/ima.yaml must mention {phrase!r}.")
    if ima_ref.exists():
        ima_text = read_text(ima_ref)
        for tool in IMA_TOOLS:
            check(tool in ima_text, errors, f"ima-adaptation.md missing ima tool: {tool}.")
        for skill in IMA_SKILLS:
            check(skill in ima_text, errors, f"ima-adaptation.md missing native skill: {skill}.")
        check("only when shell is explicitly available" in ima_text, errors, "ima-adaptation.md must say local Python requires explicit shell availability.")
    if chinese_ref.exists():
        chinese_text = read_text(chinese_ref)
        for phrase in ["老师说这些是重点", "帮我看往年题怎么复习", "整理错题", "今天该复习什么", "生成复习 PPT"]:
            check(phrase in chinese_text, errors, f"chinese-routing.md missing trigger phrase: {phrase}.")
    required_ima_commands = {
        "/source-map",
        "/paper-analyze",
        "/teacher-emphasis",
        "/wrong-note",
        "/dashboard",
        "/last-page",
        "/report",
        "/ppt",
    }
    missing_ima = sorted(required_ima_commands - index_commands)
    check(not missing_ima, errors, "ima commands missing from INDEX.md: " + ", ".join(missing_ima))


def load_agent_registry(root: Path) -> dict:
    registry_path = root / "agents" / "registry.json"
    try:
        registry = json.loads(read_text(registry_path))
    except FileNotFoundError as exc:
        raise ValueError("Missing agents/registry.json.") from exc
    except json.JSONDecodeError as exc:
        raise ValueError(f"agents/registry.json is invalid JSON: {exc}") from exc
    if not isinstance(registry, dict):
        raise ValueError("agents/registry.json must contain a JSON object.")
    return registry


def validate_agent_registry(root: Path, errors: list[str]) -> None:
    contract_path = root / "references" / "agent-adapter-contract.md"
    inventory_path = root / "references" / "agent-inventory.md"
    check(contract_path.exists(), errors, "Missing references/agent-adapter-contract.md.")
    check(inventory_path.exists(), errors, "Missing references/agent-inventory.md.")
    try:
        registry = load_agent_registry(root)
    except ValueError as exc:
        errors.append(str(exc))
        return

    check(registry.get("contract_path") == "references/agent-adapter-contract.md", errors, "agents/registry.json contract_path is incorrect.")
    check(registry.get("inventory_path") == "references/agent-inventory.md", errors, "agents/registry.json inventory_path is incorrect.")
    agents = registry.get("agents")
    if not isinstance(agents, list) or not agents:
        errors.append("agents/registry.json must contain a non-empty agents list.")
        return

    inventory_text = read_text(inventory_path) if inventory_path.exists() else ""
    seen_ids: set[str] = set()
    for index, entry in enumerate(agents, 1):
        if not isinstance(entry, dict):
            errors.append(f"agents/registry.json agent #{index} must be an object.")
            continue
        agent_id = entry.get("id")
        if not isinstance(agent_id, str) or not AGENT_ID_RE.match(agent_id):
            errors.append(f"agents/registry.json agent #{index} has invalid id: {agent_id!r}.")
            continue
        check(agent_id not in seen_ids, errors, f"Duplicate agent id in registry: {agent_id}.")
        seen_ids.add(agent_id)

        adapter_path_value = entry.get("adapter_path")
        check(isinstance(adapter_path_value, str) and adapter_path_value.startswith("agents/"), errors, f"Agent {agent_id} must define an agents/... adapter_path.")
        if isinstance(adapter_path_value, str):
            adapter_path = root / adapter_path_value
            check(adapter_path.exists(), errors, f"Agent {agent_id} adapter does not exist: {adapter_path_value}.")
            if adapter_path.exists():
                adapter_text = read_text(adapter_path)
                for phrase in ["SKILL.md", "agent-adapter-contract.md", "agent-optimization.md", "agent-inventory.md", "Best path:", f'agent_id: "{agent_id}"']:
                    check(phrase in adapter_text, errors, f"Agent {agent_id} adapter missing {phrase!r}.")

        source_status = entry.get("source_status")
        check(source_status in ALLOWED_AGENT_SOURCE_STATUS, errors, f"Agent {agent_id} has invalid source_status: {source_status!r}.")
        capability_tags = entry.get("capability_tags")
        if not isinstance(capability_tags, list) or not capability_tags:
            errors.append(f"Agent {agent_id} must define non-empty capability_tags.")
        else:
            invalid_tags = sorted({tag for tag in capability_tags if tag not in ALLOWED_CAPABILITY_TAGS})
            check(not invalid_tags, errors, f"Agent {agent_id} has invalid capability tags: {', '.join(invalid_tags)}.")
        optimization_profiles = entry.get("optimization_profiles")
        if not isinstance(optimization_profiles, list) or not optimization_profiles:
            errors.append(f"Agent {agent_id} must define non-empty optimization_profiles.")
        else:
            invalid_profiles = sorted({profile for profile in optimization_profiles if profile not in ALLOWED_OPTIMIZATION_PROFILES})
            check(not invalid_profiles, errors, f"Agent {agent_id} has invalid optimization profiles: {', '.join(invalid_profiles)}.")
        check(f"### {agent_id}" in inventory_text, errors, f"references/agent-inventory.md missing record for agent {agent_id}.")

    missing_required = sorted(REQUIRED_AGENT_IDS - seen_ids)
    check(not missing_required, errors, "Required agent ids missing from registry: " + ", ".join(missing_required))
    default_agent = registry.get("default_agent")
    check(default_agent in seen_ids, errors, f"Registry default_agent is not registered: {default_agent!r}.")


def validate(root: Path) -> list[str]:
    errors: list[str] = []
    skill_path = root / "SKILL.md"
    index_path = root / "references" / "INDEX.md"
    openai_agent = root / "agents" / "openai.yaml"
    scripts_dir = root / "scripts"
    refs_dir = root / "references"

    for path, label in [(skill_path, "SKILL.md"), (index_path, "references/INDEX.md"), (openai_agent, "agents/openai.yaml")]:
        check(path.exists(), errors, f"Missing {label}.")
    for name in ["export_flashcards.py", "snapshot.py", "srs.py", "validate_skill.py", "package_check.py", "course_templates.py", "build_runtime_prompt.py"]:
        check((scripts_dir / name).exists(), errors, f"Missing required script: scripts/{name}.")
    for name in [
        "INDEX.md",
        "course-profiles.md",
        "environment-adaptation.md",
        "materials-ingestion.md",
        "subject-adaptation.md",
        "interaction-modes.md",
        "socratic-mode.md",
        "feynman-mode.md",
        "learning-strategies.md",
        "course-templates.md",
        "agent-adapter-contract.md",
        "agent-optimization.md",
        "agent-inventory.md",
        "staged-review-workflow.md",
        "focus-feedback-iteration.md",
        "opt-in-reminders.md",
    ]:
        check((refs_dir / name).exists(), errors, f"Missing required reference: references/{name}.")
    if errors:
        return errors

    try:
        fm = frontmatter(read_text(skill_path))
    except ValueError as exc:
        errors.append(str(exc))
        fm = {}
    check(set(fm) >= {"name", "description"}, errors, "SKILL.md frontmatter must contain at least name and description.")
    extra_keys = set(fm) - {"name", "description"}
    check(not extra_keys, errors, "SKILL.md frontmatter has unrecognized keys: " + ", ".join(sorted(extra_keys)))
    check(fm.get("name") == "oh-my-teacher", errors, "SKILL.md frontmatter name must be oh-my-teacher.")
    check(bool(fm.get("description")), errors, "SKILL.md frontmatter description must be non-empty.")

    index_text = read_text(index_path)
    index_commands = commands_from_index(index_text)
    check(bool(index_commands), errors, "references/INDEX.md does not define any command rows.")

    found_by_file = commands_from_markdown(root)
    all_found = set().union(*found_by_file.values()) if found_by_file else set()
    unregistered = sorted(all_found - index_commands)
    check(not unregistered, errors, "Unregistered slash commands found: " + ", ".join(unregistered))

    required_commands = {
        "/help",
        "/profile",
        "/materials",
        "/paper",
        "/lab",
        "/diagnose",
        "/plan",
        "/map",
        "/explain",
        "/socratic",
        "/feynman",
        "/quiz",
        "/mock",
        "/oral",
        "/grade",
        "/fix",
        "/flashcards",
        "/review-due",
        "/group-quiz",
        "/visual",
        "/video",
        "/code-demo",
        "/cram",
        "/resume",
        "/summary",
        "/mode",
    }
    missing_required = sorted(required_commands - index_commands)
    check(not missing_required, errors, "Core commands missing from INDEX.md: " + ", ".join(missing_required))

    known_refs = {p.name for p in refs_dir.glob("*.md")}
    referenced_in_index: set[str] = set()
    in_catalog = False
    for line in index_text.splitlines():
        if line.startswith("## Command Catalog"):
            in_catalog = True
            continue
        if in_catalog and line.startswith("## "):
            break
        if in_catalog and line.startswith("|") and "`/" in line:
            referenced_in_index.update(INDEX_REF_RE.findall(line))
    referenced_in_index.discard("SKILL.md")
    missing_refs = sorted(referenced_in_index - known_refs)
    check(not missing_refs, errors, "INDEX.md references non-existent files: " + ", ".join(missing_refs))

    pycache_dirs = [p for p in root.rglob("__pycache__") if p.is_dir()]
    check(not pycache_dirs, errors, "Generated __pycache__ directories found: " + ", ".join(str(p) for p in pycache_dirs))

    openai_text = read_text(openai_agent)
    check("SKILL.md" in openai_text, errors, "agents/openai.yaml instructions should reference SKILL.md as the primary guide.")
    validate_agent_configs(root, errors)
    validate_ima_files(root, index_commands, errors)
    validate_agent_registry(root, errors)

    compat_path = refs_dir / "review-workflows.md"
    if compat_path.exists():
        compat_text = read_text(compat_path)
        is_compat = compat_text.strip().startswith("# Review Workflows") and (
            "compatibility" in compat_text.lower() or "redirect" in compat_text.lower()
        )
        check(is_compat, errors, "references/review-workflows.md should be a compatibility entry point.")

    readme_path = root / "README.md"
    if readme_path.exists():
        readme_text = read_text(readme_path)
        referenced_in_readme = {m.group(1) for m in re.finditer(r"references/([\w-]+\.md)", readme_text)}
        stale_refs = sorted(ref for ref in referenced_in_readme if ref not in known_refs)
        check(not stale_refs, errors, "README.md references non-existent files: " + ", ".join(stale_refs))

    try:
        required_templates = {
            "advanced-math",
            "physics",
            "programming-c-cpp",
            "digital-logic",
            "marxism-basic-principles",
        }
        missing_templates = sorted(required_templates - course_template_keys(scripts_dir / "course_templates.py"))
        check(not missing_templates, errors, "Missing course templates: " + ", ".join(missing_templates))
    except Exception as exc:
        errors.append(f"Could not inspect scripts/course_templates.py: {exc}")

    examples_dir = root / "examples"
    if examples_dir.exists():
        example_text = "\n".join(read_text(path) for path in examples_dir.glob("*.md"))
        check("/socratic" in example_text, errors, "examples/ should include a /socratic usage example.")
        check("/feynman" in example_text, errors, "examples/ should include a /feynman usage example.")
        check("ima" in example_text.lower(), errors, "examples/ should include an ima usage example.")

    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate the Oh My Teacher skill package.")
    parser.add_argument("--root", default=".", help="Skill root directory.")
    args = parser.parse_args(argv)

    errors = validate(Path(args.root).resolve())
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print("Skill validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
