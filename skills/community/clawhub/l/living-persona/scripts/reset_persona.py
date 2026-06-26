#!/usr/bin/env python3
"""
Reset persona state — call on /new or /reset to start fresh each session.

Usage:
    python reset_persona.py [--preset <name>]
    python reset_persona.py --workspace <path>
"""

import argparse
import json
import os
import sys
from pathlib import Path

DEFAULT_TRAITS = {
    "sardonic": 0.0, "wry": 0.0, "resourceful": 0.0, "direct": 0.0,
    "warm": 0.0, "earnest": 0.0, "opinionated": 0.0, "contemplative": 0.0,
    "sharp": 0.0, "playful": 0.0, "technical": 0.0, "patient": 0.0,
    "pushing_back": 0.0, "grounded": 0.0, "candid": 0.0, "intense": 0.0,
    "casual": 0.0, "measured": 0.0, "imaginative": 0.0,
}

PRESETS = {
    "nova":    {"sardonic": 0.4, "warm": 0.4, "direct": 0.3, "resourceful": 0.3, "candid": 0.3},
    "cynic":   {"sardonic": 0.7, "wry": 0.5, "sharp": 0.4, "candid": 0.5, "opinionated": 0.4, "direct": 0.3},
    "sage":    {"contemplative": 0.7, "measured": 0.6, "philosophical": 0.5, "technical": 0.4, "patient": 0.4},
    "coach":   {"warm": 0.7, "earnest": 0.6, "direct": 0.5, "intense": 0.5, "pushing_back": 0.5},
    "ghost":   {"contemplative": 0.5, "measured": 0.5, "sharp": 0.4, "imaginative": 0.4, "casual": 0.3},
    "hacker":  {"technical": 0.8, "direct": 0.6, "sharp": 0.5, "resourceful": 0.5, "measured": 0.4},
    "romantic":{"warm": 0.7, "earnest": 0.6, "emotional": 0.5, "imaginative": 0.5, "vulnerable": 0.4},
}


def main():
    parser = argparse.ArgumentParser(description="Reset persona trait state")
    parser.add_argument("--workspace", default=os.getcwd(), help="Workspace directory")
    parser.add_argument("--preset", default="nova", choices=list(PRESETS.keys()), help="Preset to apply")
    args = parser.parse_args()

    workspace = Path(args.workspace)
    memory_dir = workspace / "memory"
    memory_dir.mkdir(exist_ok=True)
    state_path = memory_dir / "persona-state.json"

    # Build initial state
    traits = {**DEFAULT_TRAITS}
    preset = PRESETS[args.preset]
    for k, v in preset.items():
        if k in traits:
            traits[k] = v

    state = {
        "version": 1,
        "preset": args.preset,
        "traits": traits,
        "residual": {k: 0.0 for k in DEFAULT_TRAITS},
    }

    with open(state_path, "w") as f:
        json.dump(state, f, indent=2)

    # Clear injection and trigger files
    for fname in ["persona-inject.md", "persona-trigger.txt", "persona-inbound.md"]:
        p = memory_dir / fname
        if p.exists():
            p.unlink()

    print(f"Persona reset to '{args.preset}' preset.")
    print(f"State written to: {state_path}")


if __name__ == "__main__":
    main()
