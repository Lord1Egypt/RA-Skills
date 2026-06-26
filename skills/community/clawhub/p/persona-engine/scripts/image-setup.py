#!/usr/bin/env python3
"""
Image provider configuration and reference image management.
Configures Gemini, Grok Imagine, or both in openclaw.json.

Usage:
    python3 image-setup.py --provider gemini --description "Warm caramel skin..." --config ~/.openclaw/openclaw.json
    python3 image-setup.py --interactive
"""

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.providers import get_image_provider_config
from lib.config import merge_config


def interactive_setup(config_path):
    """Run interactive image setup."""
    print("\n🎨 Visual Identity Setup\n")
    print("  Choose an image provider:")
    print("    [1] Gemini (photorealistic, reference image support)")
    print("    [2] Grok Imagine (creative, fewer restrictions)")
    print("    [3] Both (Gemini default, Grok for creative)")
    print("    [4] None (no visual identity)")

    choice = input("  > ").strip()
    provider_map = {"1": "gemini", "2": "grok", "3": "both", "4": "none"}
    provider = provider_map.get(choice, "none")

    if provider == "none":
        print("  Image generation disabled.")
        return

    description = input("\n  Describe your agent's appearance:\n  > ").strip()
    style = input("  Style (photorealistic/artistic/anime/cartoon) [photorealistic]: ").strip() or "photorealistic"
    always_include = input("  Always include in images (e.g., 'gold earrings, red scarf'): ").strip()

    kwargs = {
        "description": description,
        "style": style,
        "always_include": always_include,
    }

    image_config = get_image_provider_config(provider, **kwargs)
    if image_config:
        # Add spontaneous behavior config
        print("\n  Enable spontaneous selfies? (y/n)")
        if input("  > ").strip().lower().startswith("y"):
            image_config["spontaneous"] = {
                "enabled": True,
                "triggers": ["selfie", "show me", "what do you look like", "pic"],
            }

        merge_config({"persona": {"image": image_config}}, config_path)
        print(f"\n  ✅ Image provider configured: {provider}")
        print("  Note: Reference image generation requires an active API key and")
        print("  must be done through the agent or a separate generation step.")


def non_interactive_setup(provider, config_path, **kwargs):
    """Configure image provider non-interactively."""
    if provider == "none":
        return

    image_config = get_image_provider_config(provider, **kwargs)
    if image_config:
        merge_config({"persona": {"image": image_config}}, config_path)
        print(f"Image provider configured: {provider}", file=sys.stderr)


def main():
    parser = argparse.ArgumentParser(description="Image provider setup")
    parser.add_argument("--provider", choices=["gemini", "grok", "both", "none"])
    parser.add_argument("--description", default="", help="Appearance description")
    parser.add_argument("--style", default="photorealistic")
    parser.add_argument("--always-include", default="")
    parser.add_argument("--reference-image", default="")
    parser.add_argument("--config", default=str(Path.home() / ".openclaw" / "openclaw.json"))
    parser.add_argument("--interactive", action="store_true")
    parser.add_argument("--non-interactive", action="store_true")
    parser.add_argument("--regen", action="store_true", help="Regenerate reference image")
    args = parser.parse_args()

    if args.regen:
        print("Reference image regeneration requires an active API connection.", file=sys.stderr)
        print("Use the agent-selfie skill or image generation API to create a new reference.", file=sys.stderr)
        return

    if args.interactive:
        interactive_setup(args.config)
    elif args.provider:
        non_interactive_setup(
            args.provider,
            args.config,
            description=args.description,
            style=args.style,
            always_include=args.always_include,
            reference_image=args.reference_image,
        )
    else:
        interactive_setup(args.config)


if __name__ == "__main__":
    main()
