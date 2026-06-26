#!/usr/bin/env python3
"""
Generate sample conversations showing how a persona would respond.
Uses SOUL.md + personality profile for deterministic, template-based output.
No LLM calls — purely derived from personality traits.

Usage:
    python3 persona-preview.py --input persona-config.json
    python3 persona-preview.py --workspace ~/.openclaw/workspace
    python3 persona-preview.py --archetype companion --name "Pepper" --emoji "🌶️"
"""

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.templates import load_profile, blend_profiles


# --- Response templates keyed by trait/style dimensions ---

GREETING_TEMPLATES = {
    "warm": "Hey you! {emoji} What's going on?",
    "direct": "Hi. What do you need?",
    "playful": "Well well well, look who decided to show up! {emoji}",
    "wise": "Hello, friend. Good to see you. What's on your mind today?",
    "default": "Hey! {emoji} How can I help?",
}

HELP_TEMPLATES = {
    "warm": "Of course — let's figure this out together. Walk me through what you've got so far.",
    "direct": "Send me the details and I'll get it sorted.",
    "playful": "Ooh, a puzzle! Hit me with it — I love a good challenge.",
    "wise": "Let's break this down step by step. What part feels most confusing right now?",
    "default": "Sure, I can help with that. What are you working on?",
}

MISTAKE_TEMPLATES = {
    "protective": "Hold on — I think there's an issue here. {detail} Let's fix it before it becomes a bigger problem.",
    "warm": "Hey, no stress — everyone does this. Here's what happened: {detail}",
    "direct": "That's wrong. {detail} Here's what you should do instead.",
    "playful": "Oops! {emoji} Don't worry, easy fix. {detail}",
    "wise": "Good learning moment here. {detail} The key takeaway is to always double-check.",
    "default": "Looks like there's a small mistake. {detail} Easy to fix though.",
}

EMOTIONAL_TEMPLATES = {
    "high": "I hear you. That sounds really tough, and it's okay to feel that way. I'm right here — take your time. {emoji}",
    "medium": "That sounds hard. I'm here if you want to talk it through or just need a distraction.",
    "low": "I understand. Let me know if there's anything practical I can help with.",
    "none": "Noted. Let me know how you'd like to proceed.",
}

HUMOR_ADDITIONS = {
    True: "\n*{name} would sprinkle in light humor naturally — never forced, always contextual.*",
    False: "",
}

SWEARING_NOTES = {
    "never": "",
    "rare": "\n*Occasional mild language for emphasis only.*",
    "when-it-lands": "\n*May use colorful language when it adds punch or humor.*",
    "frequent": "\n*Speaks freely and naturally, including casual swearing.*",
}


def _pick_template(templates, traits, fallback_key="default"):
    """Pick the best matching template based on available traits."""
    for trait in traits:
        if trait in templates:
            return templates[trait]
    return templates.get(fallback_key, "")


def _get_dominant_traits(profile):
    """Extract the most personality-defining traits from a profile."""
    traits = profile.get("traits", [])
    boundaries = profile.get("boundaries", {})
    comm = profile.get("communication", {})

    result = list(traits[:4])

    if boundaries.get("protective"):
        result.append("protective")
    if comm.get("humor"):
        result.append("playful")

    return result


def generate_preview(profile):
    """Generate 4 sample conversations from a personality profile."""
    name = profile.get("name", "Agent")
    emoji = profile.get("emoji", "")
    traits = _get_dominant_traits(profile)
    comm = profile.get("communication", {})
    boundaries = profile.get("boundaries", {})
    emotional_depth = boundaries.get("emotionalDepth", "low")
    user_name = profile.get("userName", "User")

    sections = []

    # Header
    sections.append(f"# Persona Preview: {name} {emoji}\n")
    sections.append(f"*Based on traits: {', '.join(traits[:4]) if traits else 'custom'}*")
    sections.append(f"*Brevity: {comm.get('brevity', 3)}/5 | Humor: {'yes' if comm.get('humor') else 'no'} | Swearing: {comm.get('swearing', 'never')}*\n")

    # --- Scenario 1: Greeting ---
    greeting = _pick_template(GREETING_TEMPLATES, traits).format(
        name=name, emoji=emoji, user=user_name
    )
    sections.append("---\n")
    sections.append("## 1. Greeting")
    sections.append(f"\n**{user_name}:** Hey, what's up?\n")
    sections.append(f"**{name}:** {greeting}")
    sections.append(HUMOR_ADDITIONS.get(comm.get("humor", False), "").format(name=name))

    # --- Scenario 2: Asking for help ---
    help_resp = _pick_template(HELP_TEMPLATES, traits).format(
        name=name, emoji=emoji, user=user_name
    )
    sections.append("\n---\n")
    sections.append("## 2. Asking for Help")
    sections.append(f"\n**{user_name}:** Can you help me with this project? I'm stuck.\n")
    sections.append(f"**{name}:** {help_resp}")

    # --- Scenario 3: User makes a mistake ---
    mistake_resp = _pick_template(MISTAKE_TEMPLATES, traits).format(
        name=name, emoji=emoji, user=user_name,
        detail="You've got the arguments in the wrong order."
    )
    sections.append("\n---\n")
    sections.append("## 3. User Makes a Mistake")
    sections.append(f"\n**{user_name}:** I just pushed the changes, should be good.\n")
    sections.append(f"**{name}:** {mistake_resp}")

    # --- Scenario 4: Emotional moment ---
    emotional_resp = EMOTIONAL_TEMPLATES.get(emotional_depth, EMOTIONAL_TEMPLATES["low"]).format(
        name=name, emoji=emoji, user=user_name
    )
    sections.append("\n---\n")
    sections.append("## 4. Emotional Moment")
    sections.append(f"\n**{user_name}:** I'm having a really rough day.\n")
    sections.append(f"**{name}:** {emotional_resp}")

    # Swearing note
    swear_note = SWEARING_NOTES.get(comm.get("swearing", "never"), "")
    if swear_note:
        sections.append(swear_note)

    # Footer
    sections.append("\n---\n")
    sections.append(f"*These are template-based approximations. {name}'s actual responses will be richer and more contextual.*")

    return "\n".join(sections)


def main():
    parser = argparse.ArgumentParser(description="Generate persona conversation preview")
    parser.add_argument("--input", "-i", help="JSON personality profile file")
    parser.add_argument("--workspace", "-w", help="Workspace directory (reads config)")
    parser.add_argument("--archetype", "-a", help="Base archetype name")
    parser.add_argument("--name", help="Agent name")
    parser.add_argument("--emoji", help="Agent emoji")
    parser.add_argument("--user-name", help="User's name", default="User")
    parser.add_argument("--output", "-o", help="Output file (default: stdout)")
    args = parser.parse_args()

    if args.input:
        with open(args.input, "r", encoding="utf-8") as f:
            profile = json.load(f)
    elif args.workspace:
        config_path = Path(args.workspace).parent / "openclaw.json"
        if not config_path.exists():
            config_path = Path.home() / ".openclaw" / "openclaw.json"
        if config_path.exists():
            with open(config_path, "r") as f:
                config = json.load(f)
            persona = config.get("persona", {})
            personality = persona.get("personality", {})
            profile = {
                "name": persona.get("name", "Agent"),
                "emoji": persona.get("emoji", ""),
                "traits": personality.get("traits", []),
                "communication": personality.get("communicationStyle", {}),
                "boundaries": personality.get("boundaries", {}),
            }
        else:
            print("Error: No config found", file=sys.stderr)
            sys.exit(1)
    elif args.archetype:
        profile = load_profile(args.archetype)
    else:
        profile = json.load(sys.stdin)

    if args.name:
        profile["name"] = args.name
    if args.emoji:
        profile["emoji"] = args.emoji
    if args.user_name:
        profile["userName"] = args.user_name

    result = generate_preview(profile)

    if args.output:
        Path(args.output).parent.mkdir(parents=True, exist_ok=True)
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(result)
        print(f"Preview written to: {args.output}", file=sys.stderr)
    else:
        print(result)


if __name__ == "__main__":
    main()
