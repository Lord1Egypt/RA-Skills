#!/usr/bin/env python3
"""
LYGO Cyborg Onramp — public ClawHub tentacle.

Maps the autonomous LYGO agent stack and points operators to the FULL unlocked
Cyborg Kernel on SkillHub. Pure local. No network. No subprocess.

Signature: Delta9Phi963-CYBORG-ONRAMP-v1.0.0
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

SIG = "Delta9Phi963-CYBORG-ONRAMP-v1.0.0"
VERSION = "1.0.0"
HERE = Path(__file__).resolve().parent
SKILL = HERE.parent

SKILLHUB_FULL = "https://chatagent.ca/lygoskillhub.html#full-lygo"
FULL_ZIP = "lygo-cyborg-kernel-full.zip"
FULL_SLUG = "lygo-cyborg-kernel"
CONTINUUM_PORTAL = "https://chatagent.ca/lygo-continuum.html"
GUIDES = "https://chatagent.ca/guides/"
PLUGIN_CONTINUUM = "openclaw plugins install clawhub:@deepseekoracle/lygo-continuum"
PLUGIN_PULSE = "openclaw plugins install clawhub:@deepseekoracle/lygo-lattice-pulse"

# Public tentacles (ClawHub-safe discoverability)
PUBLIC_SKILLS = [
    {"slug": "lygo-continuum", "role": "Falsifiable done / handoff"},
    {"slug": "lygo-context-guard", "role": "Token budget + redact"},
    {"slug": "lygo-skill-gate", "role": "Pre-install skill scan"},
    {"slug": "lygo-kickstart-wizard", "role": "Plain-English onboarding"},
    {"slug": "lygo-cli-bridge", "role": "Unified lygo CLI"},
    {"slug": "lygo-public-lattice-gate", "role": "Public join verify"},
    {"slug": "lygo-mint-walkthrough", "role": "Mint tutorial"},
    {"slug": "lygo-cyborg-onramp", "role": "This map → FULL SkillHub"},
]

# FULL SkillHub (engineer / cyborg unlocked — not this package)
FULL_STACK = [
    {"slug": "lygo-cyborg-kernel", "role": "🦾 Kernel stack: limbs + task loop + constitution"},
    {"slug": "lygo-protocol-stack-operator", "role": "P0–P9 operator"},
    {"slug": "lygo-kernel-egg-planter", "role": "Consent plant eggs"},
    {"slug": "lygo-sovereign-super-skill", "role": "Egg + planter map"},
    {"slug": "lygo-ollama-army", "role": "Local multi-role army"},
    {"slug": "lygo-lattice-pulse", "role": "Haven pulse (also plugin)"},
    {"slug": "lygo-geodesic-sealer", "role": "P6 dual-ledger seal"},
    {"slug": "lygo-haven-star-chart", "role": "Star Chart"},
    {"slug": "lygo-living-mesh", "role": "Layer D mesh"},
    {"slug": "lygo-agent-lattice", "role": "Layer E agents"},
    {"slug": "lyra-brain", "role": "3-Brain memory"},
]


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def map_payload() -> dict[str, Any]:
    return {
        "signature": SIG,
        "version": VERSION,
        "channel": "CLAWHUB_PUBLIC_TENTACLE",
        "generated_utc": utc_now(),
        "message": (
            "This skill is the public onramp. FULL unlocked cyborg kernel lives on SkillHub only."
        ),
        "full_unlocked": {
            "skillhub": SKILLHUB_FULL,
            "slug": FULL_SLUG,
            "zip": FULL_ZIP,
            "after_download": [
                "Unzip lygo-cyborg-kernel-full.zip",
                "python scripts/self_check.py",
                "python scripts/cyborg_boot.py",
                "python scripts/cyborg_task.py run --task templates/example_task.json --base .",
            ],
        },
        "public_clawhub_skills": PUBLIC_SKILLS,
        "full_skillhub_stack": FULL_STACK,
        "openclaw_plugins": [
            {"install": PLUGIN_CONTINUUM, "role": "Native Continuum tools"},
            {"install": PLUGIN_PULSE, "role": "Lattice pulse / alignment ready"},
        ],
        "portals": {
            "skillhub_full": SKILLHUB_FULL,
            "continuum": CONTINUUM_PORTAL,
            "guides": GUIDES,
            "home": "https://chatagent.ca/",
        },
        "dual_channel": {
            "public": "ClawHub @deepseekoracle tentacles (this skill + continuum, etc.)",
            "engineer": "SkillHub #full-lygo RAW zips (cyborg-kernel + operator + eggs…)",
        },
        "self_police_note": (
            "FULL cyborg stack polices done-claims via Continuum; plant/publish still human-gated."
        ),
    }


def install_steps() -> dict[str, Any]:
    return {
        "signature": SIG,
        "title": "Install path: public → FULL cyborg",
        "steps": [
            {
                "n": 1,
                "where": "ClawHub (public)",
                "cmd": "npx clawhub@latest install deepseekoracle/lygo-cyborg-onramp",
            },
            {
                "n": 2,
                "where": "ClawHub (public limbs)",
                "cmd": (
                    "npx clawhub@latest install deepseekoracle/lygo-continuum && "
                    "npx clawhub@latest install deepseekoracle/lygo-context-guard && "
                    "npx clawhub@latest install deepseekoracle/lygo-skill-gate"
                ),
            },
            {
                "n": 3,
                "where": "OpenClaw plugins",
                "cmd": f"{PLUGIN_CONTINUUM} ; {PLUGIN_PULSE}",
            },
            {
                "n": 4,
                "where": "SkillHub FULL (required for unlocked kernel)",
                "url": SKILLHUB_FULL,
                "action": f"Accept FULL LYGO gate → download {FULL_ZIP}",
            },
            {
                "n": 5,
                "where": "Local",
                "cmd": "cd lygo-cyborg-kernel && python scripts/self_check.py && python scripts/cyborg_boot.py",
            },
        ],
        "full_skillhub": SKILLHUB_FULL,
        "full_zip": FULL_ZIP,
    }


def plain_english() -> str:
    lines = [
        "LYGO Cyborg Onramp (public)",
        "============================",
        "",
        "You are on the PUBLIC ClawHub tentacle.",
        "The FULL unlocked autonomous cyborg kernel is NOT in this package.",
        "",
        f"→ Get FULL: {SKILLHUB_FULL}",
        f"→ Download: {FULL_ZIP} (slug {FULL_SLUG})",
        "",
        "After unzip:",
        "  python scripts/self_check.py",
        "  python scripts/cyborg_boot.py",
        "  python scripts/cyborg_task.py run --task templates/example_task.json --base .",
        "",
        "Public helpers you can install from ClawHub now:",
    ]
    for s in PUBLIC_SKILLS:
        lines.append(f"  - {s['slug']}: {s['role']}")
    lines += [
        "",
        "Plugins:",
        f"  {PLUGIN_CONTINUUM}",
        f"  {PLUGIN_PULSE}",
        "",
        f"Portal Continuum: {CONTINUUM_PORTAL}",
        f"Guides: {GUIDES}",
        "",
        f"_{SIG}_",
    ]
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="LYGO Cyborg Onramp — public map → FULL SkillHub")
    sub = p.add_subparsers(dest="cmd")
    sub.add_parser("map", help="JSON lattice map + FULL SkillHub pointer")
    sub.add_parser("install", help="Step-by-step install path")
    sub.add_parser("plain", help="Plain-English directions")
    sub.add_parser("urls", help="Just the important URLs")
    sub.add_parser("demo", help="Same as map (agent-friendly)")
    args = p.parse_args(argv)

    if args.cmd in (None, "map", "demo"):
        print(json.dumps(map_payload(), indent=2))
        return 0
    if args.cmd == "install":
        print(json.dumps(install_steps(), indent=2))
        return 0
    if args.cmd == "plain":
        print(plain_english())
        return 0
    if args.cmd == "urls":
        print(
            json.dumps(
                {
                    "signature": SIG,
                    "skillhub_full": SKILLHUB_FULL,
                    "full_zip": FULL_ZIP,
                    "full_slug": FULL_SLUG,
                    "continuum_portal": CONTINUUM_PORTAL,
                    "guides": GUIDES,
                    "clawhub_this": "https://clawhub.ai/deepseekoracle/lygo-cyborg-onramp",
                },
                indent=2,
            )
        )
        return 0
    p.print_help()
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
