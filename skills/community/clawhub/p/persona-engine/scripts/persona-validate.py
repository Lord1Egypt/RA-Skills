#!/usr/bin/env python3
"""
Validate workspace persona files for completeness and correctness.

Usage:
    python3 persona-validate.py --workspace ~/.openclaw/workspace
    python3 persona-validate.py --workspace ~/.openclaw/workspace --config ~/.openclaw/openclaw.json
"""

import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))


REQUIRED_FILES = ["SOUL.md", "USER.md", "IDENTITY.md", "MEMORY.md", "AGENTS.md", "HEARTBEAT.md"]

SOUL_REQUIRED_SECTIONS = ["Who You Are", "Core Truths", "Communication", "Boundaries", "Continuity"]

REQUIRED_PERSONA_FIELDS = ["name", "emoji"]


def validate_workspace(workspace_path, config_path=None):
    """Validate workspace files and config. Returns list of issues."""
    workspace = Path(workspace_path)
    issues = []
    warnings = []

    # Check workspace exists
    if not workspace.exists():
        issues.append(f"Workspace directory not found: {workspace}")
        return issues, warnings

    # Check required files
    for fname in REQUIRED_FILES:
        fpath = workspace / fname
        if not fpath.exists():
            issues.append(f"Missing file: {fname}")
        elif fpath.stat().st_size == 0:
            issues.append(f"Empty file: {fname}")

    # Validate SOUL.md structure
    soul_path = workspace / "SOUL.md"
    if soul_path.exists() and soul_path.stat().st_size > 0:
        soul = soul_path.read_text(encoding="utf-8")
        for section in SOUL_REQUIRED_SECTIONS:
            if section not in soul:
                issues.append(f"SOUL.md missing section: {section}")

        # Check for name in header
        if not re.search(r"^#\s*SOUL\.md", soul, re.MULTILINE):
            warnings.append("SOUL.md missing standard header format")

    # Check memory directory
    memory_dir = workspace / "memory"
    if not memory_dir.exists():
        warnings.append("No memory/ directory found")
    elif not list(memory_dir.glob("*.md")):
        warnings.append("memory/ directory is empty (no daily notes)")

    # Validate config if provided
    if config_path:
        cp = Path(config_path)
        if not cp.exists():
            issues.append(f"Config file not found: {config_path}")
        else:
            try:
                with open(cp, "r") as f:
                    config = json.load(f)
                persona = config.get("persona", {})
                if not persona:
                    issues.append("Config missing 'persona' section")
                else:
                    for field in REQUIRED_PERSONA_FIELDS:
                        if not persona.get(field):
                            issues.append(f"Config missing persona.{field}")

                    personality = persona.get("personality", {})
                    if not personality.get("archetype"):
                        warnings.append("Config missing persona.personality.archetype")
                    if not personality.get("communicationStyle"):
                        warnings.append("Config missing persona.personality.communicationStyle")
            except json.JSONDecodeError as e:
                issues.append(f"Config is invalid JSON: {e}")

    return issues, warnings


def main():
    parser = argparse.ArgumentParser(description="Validate persona workspace")
    parser.add_argument("--workspace", "-w", required=True, help="Workspace directory")
    parser.add_argument("--config", "-c", help="Config file path")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    args = parser.parse_args()

    config_path = args.config
    if not config_path:
        # Try common locations
        for candidate in [
            Path(args.workspace).parent / "openclaw.json",
            Path.home() / ".openclaw" / "openclaw.json",
        ]:
            if candidate.exists():
                config_path = str(candidate)
                break

    issues, warnings = validate_workspace(args.workspace, config_path)

    if args.json:
        print(json.dumps({"issues": issues, "warnings": warnings, "valid": len(issues) == 0}, indent=2))
    else:
        if not issues and not warnings:
            print("✅ Workspace is valid. All files present and well-formed.")
            sys.exit(0)

        if issues:
            print("❌ Issues found:\n")
            for issue in issues:
                print(f"  ERROR: {issue}")

        if warnings:
            print("\n⚠️  Warnings:\n")
            for warning in warnings:
                print(f"  WARN: {warning}")

        if issues:
            print(f"\n{len(issues)} error(s), {len(warnings)} warning(s)")
            sys.exit(1)
        else:
            print(f"\n0 errors, {len(warnings)} warning(s)")
            sys.exit(0)


if __name__ == "__main__":
    main()
