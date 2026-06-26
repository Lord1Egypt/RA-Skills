#!/usr/bin/env python3
"""
Compare current workspace files against what the generator would produce.
Shows colored diff of differences.

Usage:
    python3 persona-diff.py --workspace ~/.openclaw/workspace --config ~/.openclaw/openclaw.json
"""

import argparse
import difflib
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.config import read_config
from lib.templates import load_profile, blend_profiles

# Import generators
from importlib.machinery import SourceFileLoader

_scripts = Path(__file__).resolve().parent

generate_soul = SourceFileLoader(
    "generate_soul", str(_scripts / "generate-soul.py")
).load_module()

generate_user = SourceFileLoader(
    "generate_user", str(_scripts / "generate-user.py")
).load_module()

generate_identity = SourceFileLoader(
    "generate_identity", str(_scripts / "generate-identity.py")
).load_module()


# ANSI colors
RED = "\033[0;31m"
GREEN = "\033[0;32m"
CYAN = "\033[0;36m"
YELLOW = "\033[1;33m"
BOLD = "\033[1m"
NC = "\033[0m"


def _colored_diff(current_lines, generated_lines, filename):
    """Generate colored unified diff."""
    diff = list(difflib.unified_diff(
        current_lines, generated_lines,
        fromfile=f"current/{filename}",
        tofile=f"generated/{filename}",
        lineterm=""
    ))
    if not diff:
        return None

    output = []
    for line in diff:
        if line.startswith("+++") or line.startswith("---"):
            output.append(f"{BOLD}{line}{NC}")
        elif line.startswith("+"):
            output.append(f"{GREEN}{line}{NC}")
        elif line.startswith("-"):
            output.append(f"{RED}{line}{NC}")
        elif line.startswith("@@"):
            output.append(f"{CYAN}{line}{NC}")
        else:
            output.append(line)
    return "\n".join(output)


def _build_profile_from_config(persona):
    """Build a personality profile dict from openclaw.json persona config."""
    personality = persona.get("personality", {})
    comm_style = personality.get("communicationStyle", {})
    bounds = personality.get("boundaries", {})

    # Check for blend
    archetypes = personality.get("archetypes")
    if archetypes and isinstance(archetypes, list) and len(archetypes) > 1:
        profile = blend_profiles(archetypes)
    else:
        archetype = personality.get("archetype", "custom")
        try:
            profile = load_profile(archetype)
        except FileNotFoundError:
            profile = load_profile("custom")

    profile["name"] = persona.get("name", "Agent")
    profile["emoji"] = persona.get("emoji", "")
    profile["creature"] = persona.get("identity", {}).get("creature", "")
    profile["vibe"] = persona.get("identity", {}).get("vibe", "")

    if personality.get("traits"):
        profile["traits"] = personality["traits"]
    if comm_style:
        profile["communication"] = {
            "brevity": comm_style.get("brevity", 3),
            "humor": comm_style.get("humor", False),
            "swearing": comm_style.get("swearing", "never"),
            "banOpeningPhrases": comm_style.get("openingPhrases") == "banned",
        }
    if bounds:
        profile["boundaries"] = bounds

    return profile


def diff_workspace(workspace_path, config_path):
    """Compare workspace files against generated versions. Returns diff strings."""
    workspace = Path(workspace_path)
    config = read_config(config_path)
    persona = config.get("persona", {})

    if not persona:
        return {"error": "No persona config found"}

    profile = _build_profile_from_config(persona)
    diffs = {}

    # SOUL.md
    soul_path = workspace / "SOUL.md"
    if soul_path.exists():
        current = soul_path.read_text(encoding="utf-8").splitlines()
        generated = generate_soul.generate_soul(profile).splitlines()
        diff = _colored_diff(current, generated, "SOUL.md")
        if diff:
            diffs["SOUL.md"] = diff

    # USER.md
    user_path = workspace / "USER.md"
    if user_path.exists():
        user_context = config.get("userContext", {})
        if not user_context:
            user_context = {
                "userName": persona.get("userName", "User"),
                "callNames": persona.get("userName", "User"),
                "timezone": "UTC",
            }
        current = user_path.read_text(encoding="utf-8").splitlines()
        generated = generate_user.generate_user(user_context).splitlines()
        diff = _colored_diff(current, generated, "USER.md")
        if diff:
            diffs["USER.md"] = diff

    # IDENTITY.md
    id_path = workspace / "IDENTITY.md"
    if id_path.exists():
        id_context = {
            "name": persona.get("name", "Agent"),
            "emoji": persona.get("emoji", ""),
            "creature": persona.get("identity", {}).get("creature", ""),
            "vibe": persona.get("identity", {}).get("vibe", ""),
            "nickname": persona.get("identity", {}).get("nickname", ""),
        }
        current = id_path.read_text(encoding="utf-8").splitlines()
        generated = generate_identity.generate_identity(id_context).splitlines()
        diff = _colored_diff(current, generated, "IDENTITY.md")
        if diff:
            diffs["IDENTITY.md"] = diff

    return diffs


def main():
    parser = argparse.ArgumentParser(description="Diff workspace vs generated files")
    parser.add_argument("--workspace", "-w", required=True, help="Workspace directory")
    parser.add_argument("--config", "-c", help="Config file path")
    args = parser.parse_args()

    config_path = args.config
    if not config_path:
        for candidate in [
            Path(args.workspace).parent / "openclaw.json",
            Path.home() / ".openclaw" / "openclaw.json",
        ]:
            if candidate.exists():
                config_path = str(candidate)
                break

    if not config_path or not Path(config_path).exists():
        print("Error: No config file found. Use --config to specify.", file=sys.stderr)
        sys.exit(1)

    diffs = diff_workspace(args.workspace, config_path)

    if "error" in diffs:
        print(f"Error: {diffs['error']}", file=sys.stderr)
        sys.exit(1)

    if not diffs:
        print("✅ All files match generated output. No differences found.")
    else:
        print(f"{BOLD}Found differences in {len(diffs)} file(s):{NC}\n")
        for filename, diff_text in diffs.items():
            print(f"{YELLOW}=== {filename} ==={NC}")
            print(diff_text)
            print()


if __name__ == "__main__":
    main()
