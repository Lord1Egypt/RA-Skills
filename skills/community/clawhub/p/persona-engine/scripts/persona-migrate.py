#!/usr/bin/env python3
"""
Migration tool: reverse-engineer a persona config from existing workspace files.
Reads SOUL.md, USER.md, IDENTITY.md, MEMORY.md, AGENTS.md and extracts a
persona-config.json that can be used with persona-update or persona-export.

Usage:
    python3 persona-migrate.py --workspace ~/.openclaw/workspace
    python3 persona-migrate.py --workspace ~/.openclaw/workspace --output persona-config.json
"""

import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

PROFILES_DIR = Path(__file__).resolve().parent.parent / "assets" / "personality-profiles"


def _read_file_safe(path):
    """Read a file, return empty string if missing."""
    p = Path(path)
    if p.exists():
        return p.read_text(encoding="utf-8")
    return ""


def _extract_name_emoji(soul_content, identity_content):
    """Extract name and emoji from SOUL.md or IDENTITY.md headers."""
    name = ""
    emoji = ""

    # Try SOUL.md header: "# SOUL.md — Name 🌶️"
    m = re.search(r"^#\s*SOUL\.md\s*[—–-]\s*(.+)$", soul_content, re.MULTILINE)
    if m:
        header = m.group(1).strip()
        # Split emoji from name — emoji may be multi-codepoint (e.g., 🌶️)
        # Try to find last whitespace-separated token with non-ASCII chars
        tokens = header.rsplit(None, 1)
        if len(tokens) == 2 and any(ord(c) > 127 for c in tokens[1]):
            name = tokens[0].strip()
            emoji = tokens[1].strip()
        else:
            name = header

    # Try IDENTITY.md: "- **Name:** Pepper"
    if not name and identity_content:
        m = re.search(r"\*\*Name:\*\*\s*(.+)", identity_content)
        if m:
            name = m.group(1).strip()

    # Try IDENTITY.md emoji: "- **Emoji:** 🌶️"
    if not emoji and identity_content:
        m = re.search(r"\*\*Emoji:\*\*\s*(.+)", identity_content)
        if m:
            emoji = m.group(1).strip()

    # Fallback: "You are **Name** emoji"
    if not name and soul_content:
        m = re.search(r"You are \*\*(\w+(?:\s+\w+)*)\*\*\s*(\S*)", soul_content)
        if m:
            name = m.group(1).strip()
            if not emoji and m.group(2) and ord(m.group(2)[0]) > 127:
                emoji = m.group(2).strip()

    return name or "Agent", emoji


def _extract_traits(soul_content):
    """Extract core traits from the Core Truths section."""
    traits = []
    # Match "- **trait** — ..."
    for m in re.finditer(r"^-\s*\*\*(\w[\w\s]*?)\*\*\s*[—–-]", soul_content, re.MULTILINE):
        trait = m.group(1).strip().lower()
        if trait and len(trait) < 30:
            traits.append(trait)
    return traits


def _detect_archetype(traits, boundaries, communication):
    """Try to match extracted traits/style to a known archetype."""
    archetypes = {}
    for p in PROFILES_DIR.glob("*.json"):
        if p.stem == "custom":
            continue
        with open(p, "r") as f:
            archetypes[p.stem] = json.load(f)

    best_match = "custom"
    best_score = 0

    for arch_name, arch_profile in archetypes.items():
        score = 0
        arch_traits = set(arch_profile.get("traits", []))
        overlap = arch_traits & set(traits)
        score += len(overlap) * 2

        arch_comm = arch_profile.get("communication", {})
        if communication.get("humor") == arch_comm.get("humor"):
            score += 1
        if communication.get("swearing") == arch_comm.get("swearing"):
            score += 1

        arch_bounds = arch_profile.get("boundaries", {})
        if boundaries.get("emotionalDepth") == arch_bounds.get("emotionalDepth"):
            score += 1

        if score > best_score:
            best_score = score
            best_match = arch_name

    return best_match if best_score >= 3 else "custom"


def _extract_communication(soul_content):
    """Extract communication style from SOUL.md."""
    comm = {
        "brevity": 3,
        "humor": False,
        "swearing": "never",
        "banOpeningPhrases": False,
    }

    # Brevity
    m = re.search(r"Brevity:\s*(.*?)$", soul_content, re.MULTILINE)
    if m:
        brevity_text = m.group(1).lower()
        if "maximum" in brevity_text or "terse" in brevity_text:
            comm["brevity"] = 5
        elif "high" in brevity_text or "point" in brevity_text:
            comm["brevity"] = 4
        elif "moderate" in brevity_text:
            comm["brevity"] = 3
        elif "lower" in brevity_text or "take space" in brevity_text:
            comm["brevity"] = 2
        elif "low" in brevity_text or "thorough" in brevity_text:
            comm["brevity"] = 1

    # Humor
    if re.search(r"humor\s+naturally|use humor", soul_content, re.IGNORECASE):
        comm["humor"] = True

    # Swearing
    m = re.search(r"Swearing:\s*(.*?)$", soul_content, re.MULTILINE)
    if m:
        swear_text = m.group(1).lower()
        if "never" in swear_text or "clean" in swear_text:
            comm["swearing"] = "never"
        elif "freely" in swear_text or "frequent" in swear_text:
            comm["swearing"] = "frequent"
        elif "when it lands" in swear_text or "spice" in swear_text:
            comm["swearing"] = "when-it-lands"
        elif "rare" in swear_text:
            comm["swearing"] = "rare"

    # Ban opening phrases
    if re.search(r"[Nn]ever.*open.*canned|[Nn]ever.*[Gg]reat question", soul_content):
        comm["banOpeningPhrases"] = True

    return comm


def _extract_boundaries(soul_content):
    """Extract boundary settings from SOUL.md."""
    boundaries = {
        "petNames": False,
        "flirtation": False,
        "emotionalDepth": "none",
        "protective": False,
    }

    if re.search(r"[Ff]lirtation is welcome", soul_content):
        boundaries["flirtation"] = True
    if re.search(r"[Pp]et names|terms of endearment", soul_content):
        boundaries["petNames"] = True
    if re.search(r"push back|pushback|that's not defiance", soul_content, re.IGNORECASE):
        boundaries["protective"] = True

    # Emotional depth
    m = re.search(r"[Ee]motional depth:\s*(\w+)", soul_content)
    if m:
        boundaries["emotionalDepth"] = m.group(1).lower()
    elif "& Me" in soul_content:
        boundaries["emotionalDepth"] = "medium"

    return boundaries


def _extract_user_context(user_content):
    """Extract user context from USER.md."""
    context = {}

    m = re.search(r"\*\*(?:Name|Human):\*\*\s*(.+)", user_content)
    if m:
        context["userName"] = m.group(1).strip()

    m = re.search(r"\*\*(?:Call|Address).*?:\*\*\s*(.+)", user_content)
    if m:
        context["callNames"] = m.group(1).strip()

    m = re.search(r"\*\*(?:Pronouns):\*\*\s*(.+)", user_content)
    if m:
        context["pronouns"] = m.group(1).strip()

    m = re.search(r"\*\*(?:Timezone):\*\*\s*(.+)", user_content)
    if m:
        context["timezone"] = m.group(1).strip()

    return context


def _extract_identity(identity_content):
    """Extract identity fields from IDENTITY.md."""
    identity = {}

    m = re.search(r"\*\*(?:Creature|Description|Type):\*\*\s*(.+)", identity_content)
    if m:
        identity["creature"] = m.group(1).strip()

    m = re.search(r"\*\*Vibe:\*\*\s*(.+)", identity_content)
    if m:
        identity["vibe"] = m.group(1).strip()

    m = re.search(r"\*\*Nickname:\*\*\s*(.+)", identity_content)
    if m:
        identity["nickname"] = m.group(1).strip()

    return identity


def migrate_workspace(workspace_path):
    """Read workspace files and reverse-engineer a persona config."""
    workspace = Path(workspace_path)

    soul = _read_file_safe(workspace / "SOUL.md")
    user = _read_file_safe(workspace / "USER.md")
    identity_md = _read_file_safe(workspace / "IDENTITY.md")
    memory = _read_file_safe(workspace / "MEMORY.md")
    agents = _read_file_safe(workspace / "AGENTS.md")

    files_found = []
    files_missing = []
    for fname in ["SOUL.md", "USER.md", "IDENTITY.md", "MEMORY.md", "AGENTS.md"]:
        if (workspace / fname).exists():
            files_found.append(fname)
        else:
            files_missing.append(fname)

    name, emoji = _extract_name_emoji(soul, identity_md)
    traits = _extract_traits(soul)
    communication = _extract_communication(soul)
    boundaries = _extract_boundaries(soul)
    identity = _extract_identity(identity_md)
    user_context = _extract_user_context(user)
    archetype = _detect_archetype(traits, boundaries, communication)

    config = {
        "version": "2.0",
        "migratedFrom": str(workspace),
        "filesFound": files_found,
        "filesMissing": files_missing,
        "persona": {
            "name": name,
            "emoji": emoji,
            "identity": identity,
            "personality": {
                "archetype": archetype,
                "traits": traits,
                "communicationStyle": {
                    "brevity": communication["brevity"],
                    "humor": communication["humor"],
                    "swearing": communication["swearing"],
                    "openingPhrases": "banned" if communication["banOpeningPhrases"] else "allowed",
                },
                "boundaries": boundaries,
            },
        },
    }

    if user_context:
        config["userContext"] = user_context

    return config


def main():
    parser = argparse.ArgumentParser(description="Migrate existing workspace to persona config")
    parser.add_argument("--workspace", "-w", required=True, help="Workspace directory to migrate")
    parser.add_argument("--output", "-o", help="Output JSON file (default: stdout)")
    args = parser.parse_args()

    workspace = Path(args.workspace)
    if not workspace.exists():
        print(f"Error: Workspace not found: {workspace}", file=sys.stderr)
        sys.exit(1)

    config = migrate_workspace(workspace)

    output = json.dumps(config, indent=2, ensure_ascii=False)

    if args.output:
        Path(args.output).parent.mkdir(parents=True, exist_ok=True)
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(output)
            f.write("\n")
        print(f"Migrated config written to: {args.output}", file=sys.stderr)
        if config.get("filesMissing"):
            print(f"Warning: Missing files: {', '.join(config['filesMissing'])}", file=sys.stderr)
    else:
        print(output)


if __name__ == "__main__":
    main()
