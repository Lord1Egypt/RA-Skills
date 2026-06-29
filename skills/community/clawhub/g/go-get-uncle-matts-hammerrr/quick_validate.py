#!/usr/bin/env python3
from pathlib import Path
import json
import re
import sys


ROOT = Path(__file__).resolve().parent
SKILL = ROOT / "SKILL.md"

REQUIRED_FILES = [
    "SKILL.md",
    "README.md",
    "CHANGELOG.md",
    "skill-card.md",
    "agents/openai.yaml",
    "references/claim-model.md",
    "references/evidence-rules.md",
    "references/command-safety.md",
    "references/reality-gap-checklist.md",
    "references/repeat-run.md",
    "references/report-rules.md",
    "templates/PROJECT_TRUTH_AUDIT.md",
    "templates/remediation-plan.md",
    "schemas/project-truth-audit.schema.json",
    "examples/invocation-prompts.md",
]

REQUIRED_SECTIONS = [
    "# Go Get Uncle Matt's HAMMERRR",
    "## Use This Skill When",
    "## Do Not Use This Skill When",
    "## What It Produces",
    "## What It Never Does",
    "## Operating Contract",
    "## Status Model",
    "## Evidence Rules",
    "## Anti-Patterns",
]

REQUIRED_PHRASES = [
    "read-only project-truth audit",
    "explicitly names",
    "claims against reachable runtime behavior",
    "installation, packaging, upgrade, and release paths",
    "Do not use for ordinary PR review",
    "PROJECT_TRUTH_AUDIT.md",
    "VERIFIED",
    "PARTIAL",
    "CONTRADICTED",
    "STALE",
    "DEAD",
    "UNKNOWN",
    "EXECUTED_STRONG",
    "STATIC_ONLY",
    "BLOCKED",
]

UNSUPPORTED_FRONTMATTER_KEYS = [
    "triggers:",
    "tools:",
    "allowed-tools:",
    "metadata:",
    "compatibility:",
]


def fail(message: str) -> int:
    print(f"FAIL: {message}")
    return 1


def check_file_exists() -> int:
    missing = [path for path in REQUIRED_FILES if not (ROOT / path).exists()]
    if missing:
        return fail(f"missing required files: {', '.join(missing)}")
    return 0


def check_skill() -> int:
    if not SKILL.exists():
        return fail("SKILL.md is missing")

    text = SKILL.read_text(encoding="utf-8")
    match = re.match(r"---\n(.*?)\n---\n", text, re.DOTALL)
    if not match:
        return fail("frontmatter block is missing or malformed")

    frontmatter = match.group(1)
    if "name: go-get-uncle-matts-hammerrr" not in frontmatter:
        return fail("frontmatter name is wrong")
    if "description:" not in frontmatter:
        return fail("frontmatter description is missing")

    found = [key for key in UNSUPPORTED_FRONTMATTER_KEYS if key in frontmatter]
    if found:
        return fail(f"unsupported frontmatter keys present: {', '.join(found)}")

    missing_sections = [section for section in REQUIRED_SECTIONS if section not in text]
    if missing_sections:
        return fail(f"missing sections: {', '.join(missing_sections)}")

    missing_phrases = [phrase for phrase in REQUIRED_PHRASES if phrase not in text]
    if missing_phrases:
        return fail(f"missing required phrases: {', '.join(missing_phrases)}")

    return 0


def check_schema() -> int:
    schema_path = ROOT / "schemas/project-truth-audit.schema.json"
    try:
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return fail(f"schema JSON is invalid: {exc}")

    if schema.get("$id") != "urn:go-get-uncle-matts-hammerrr:project-truth-audit":
        return fail("schema $id is wrong")
    if "claims" not in schema.get("required", []):
        return fail("schema does not require claims")
    if "findings" not in schema.get("required", []):
        return fail("schema does not require findings")
    return 0


def check_templates() -> int:
    report = (ROOT / "templates/PROJECT_TRUTH_AUDIT.md").read_text(encoding="utf-8")
    required = [
        "## Scope",
        "## Baseline",
        "## Coverage Ledger",
        "## Proof Ledger",
        "## Findings",
        "## Truth Table",
        "## Investigated And Rejected",
        "## Unknowns And Blockers",
        "## Next Proof Steps",
    ]
    missing = [section for section in required if section not in report]
    if missing:
        return fail(f"report template missing sections: {', '.join(missing)}")
    return 0


def check_agent_policy() -> int:
    agent = (ROOT / "agents/openai.yaml").read_text(encoding="utf-8")
    compact_agent = " ".join(agent.split())
    required = [
        "allow_implicit_invocation: false",
        "Use only after the user explicitly invokes",
        "Do not activate for generic review",
    ]
    missing = [phrase for phrase in required if phrase not in compact_agent]
    if missing:
        return fail(f"agent policy missing explicit-invocation guard: {', '.join(missing)}")
    if "allow_implicit_invocation: true" in agent:
        return fail("agent policy allows implicit invocation")
    return 0


def main() -> int:
    for check in (check_file_exists, check_skill, check_schema, check_templates, check_agent_policy):
        result = check()
        if result:
            return result

    print("PASS: go-get-uncle-matts-hammerrr skill package validates")
    return 0


if __name__ == "__main__":
    sys.exit(main())
