#!/usr/bin/env python3
"""
Generate SOUL.md from a personality profile JSON.

Usage:
    python3 generate-soul.py --input profile.json --output SOUL.md
    python3 generate-soul.py --archetype companion --name "Pepper" --emoji "🌶️" ...
"""

import argparse
import json
import sys
from pathlib import Path

# Add parent to path for lib imports
sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.templates import render_template, load_profile, blend_profiles


PROFILES_DIR = Path(__file__).resolve().parent.parent / "assets" / "personality-profiles"


def load_archetype(archetype_name):
    """Load a personality archetype JSON file."""
    path = PROFILES_DIR / f"{archetype_name}.json"
    if not path.exists():
        # Try community templates
        community_dir = PROFILES_DIR.parent / "community-templates"
        path = community_dir / f"{archetype_name}.json"
    if not path.exists():
        print(f"Error: Unknown archetype '{archetype_name}'", file=sys.stderr)
        print(f"Available: {', '.join(p.stem for p in PROFILES_DIR.glob('*.json'))}", file=sys.stderr)
        sys.exit(1)
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def build_context(profile):
    """Build template context from a personality profile dict."""
    comm = profile.get("communication", {})
    bounds = profile.get("boundaries", {})
    rel = profile.get("userRelationship", {})

    # Determine brevity description
    brevity = comm.get("brevity", 3)
    brevity_map = {
        1: "Low brevity. Be thorough and detailed. Explain your reasoning.",
        2: "Lower brevity. Take space to explain well, but don't ramble.",
        3: "Moderate brevity. Balance detail with conciseness.",
        4: "High brevity. Get to the point. No padding, no preamble.",
        5: "Maximum brevity. Terse. Every word must earn its place.",
    }
    brevity_desc = brevity_map.get(brevity, brevity_map[3])

    # Determine swearing description
    swearing = comm.get("swearing", "never")
    swearing_descs = {
        "never": "Never. Keep it clean at all times.",
        "rare": "Rarely. Save it for genuine emphasis or comedic effect.",
        "when-it-lands": "When it lands. Swearing is a spice — use it to add punch, never as filler.",
        "frequent": "Freely. Swear naturally as part of your voice.",
    }
    swearing_desc = profile.get("swearingDesc") or swearing_descs.get(swearing, "")

    # Build pet names strings
    pet_names_for = ""
    pet_names_from = ""
    if rel.get("petNamesForUser"):
        names = rel["petNamesForUser"]
        pet_names_for = ", ".join(names) if isinstance(names, list) else str(names)
    if rel.get("petNamesFromUser"):
        names = rel["petNamesFromUser"]
        pet_names_from = ", ".join(names) if isinstance(names, list) else str(names)

    has_relationship = bool(
        rel.get("userName")
        or bounds.get("emotionalDepth", "none") not in ("none", "")
        or bounds.get("petNames")
        or bounds.get("flirtation")
    )

    context = {
        "name": profile.get("name", "Agent"),
        "emoji": profile.get("emoji", ""),
        "creature": profile.get("creature", profile.get("description", "")),
        "vibe": profile.get("vibe", ""),
        "traits": profile.get("traits", []),
        "humor": comm.get("humor", False),
        "banOpeningPhrases": comm.get("banOpeningPhrases", False),
        "swearingDesc": swearing_desc,
        "brevityDesc": profile.get("brevityDesc") or brevity_desc,
        "hasRelationship": has_relationship,
        "userName": rel.get("userName", profile.get("userName", "")),
        "petNamesForUser": pet_names_for,
        "petNamesFromUser": pet_names_from,
        "dynamic": rel.get("dynamic", ""),
        "emotionalDepth": bounds.get("emotionalDepth", ""),
        "flirtation": bounds.get("flirtation", False),
        "petNames": bounds.get("petNames", False),
        "protective": bounds.get("protective", False),
        "vibeSummary": profile.get("vibeSummary", ""),
        "specialInstructions": profile.get("specialInstructions", []),
        "platformNotes": profile.get("platformNotes", []),
    }
    return context


def generate_soul(profile):
    """Generate SOUL.md content from profile dict."""
    context = build_context(profile)
    return render_template("SOUL.md.hbs", context)


def main():
    parser = argparse.ArgumentParser(description="Generate SOUL.md from personality profile")
    parser.add_argument("--input", "-i", help="JSON personality profile file")
    parser.add_argument("--output", "-o", help="Output file path (default: stdout)")
    parser.add_argument("--archetype", "-a", help="Base archetype name")
    parser.add_argument("--name", help="Agent name")
    parser.add_argument("--emoji", help="Agent emoji")
    parser.add_argument("--creature", help="Agent description")
    parser.add_argument("--user-name", help="User's name")
    parser.add_argument("--traits", help="Comma-separated traits")
    args = parser.parse_args()

    if args.input:
        with open(args.input, "r", encoding="utf-8") as f:
            profile = json.load(f)

        # Support blend syntax: {"archetypes": [{"name": "companion", "weight": 0.7}, ...]}
        if "archetypes" in profile and isinstance(profile["archetypes"], list):
            blended = blend_profiles(profile["archetypes"])
            # Preserve non-archetype fields from input
            for key in ("name", "emoji", "creature", "vibe", "userName", "userRelationship"):
                if key in profile:
                    blended[key] = profile[key]
            profile = blended
        elif "archetype" in profile and profile["archetype"] not in ("custom", "blend", ""):
            # Load archetype as base, override with profile values
            try:
                base = load_archetype(profile["archetype"])
                for key, val in profile.items():
                    if key != "archetype" and val:
                        base[key] = val
                profile = base
            except SystemExit:
                pass  # Use profile as-is if archetype not found
    elif args.archetype:
        profile = load_archetype(args.archetype)
    else:
        # Read from stdin
        profile = json.load(sys.stdin)

    # Override with CLI args
    if args.name:
        profile["name"] = args.name
    if args.emoji:
        profile["emoji"] = args.emoji
    if args.creature:
        profile["creature"] = args.creature
    if args.user_name:
        profile.setdefault("userRelationship", {})["userName"] = args.user_name
        profile["userName"] = args.user_name
    if args.traits:
        profile["traits"] = [t.strip() for t in args.traits.split(",")]

    result = generate_soul(profile)

    if args.output:
        Path(args.output).parent.mkdir(parents=True, exist_ok=True)
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(result)
        print(f"Generated: {args.output}", file=sys.stderr)
    else:
        print(result)


if __name__ == "__main__":
    main()
