#!/usr/bin/env python3
"""Configure opportunity-scout niches, keywords, sources, and schedule.

Usage:
    configure.py --init                          Copy example config to config.json
    configure.py --add-niche "Name" --keywords "k1,k2,k3"
    configure.py --add-source reddit:r/SaaS,hackernews [--niche "Name"]
    configure.py --remove-niche "Name"
    configure.py --set-schedule daily|weekly
    configure.py --set-weight signal_strength=0.3,engagement=0.2
    configure.py --show                          Print current config
"""

import argparse
import json
import os
import shutil
import sys

SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_PATH = os.path.join(SKILL_DIR, "config.json")
EXAMPLE_PATH = os.path.join(SKILL_DIR, "assets", "config.example.json")


def load_config():
    """Load config.json or exit with helpful message."""
    if not os.path.exists(CONFIG_PATH):
        print(f"Error: {CONFIG_PATH} not found.", file=sys.stderr)
        print("Run: configure.py --init  (copies example config)", file=sys.stderr)
        sys.exit(1)
    with open(CONFIG_PATH, "r") as f:
        return json.load(f)


def save_config(config):
    """Write config back to disk."""
    with open(CONFIG_PATH, "w") as f:
        json.dump(config, f, indent=2)
    print(f"Config saved to {CONFIG_PATH}")


def init_config():
    """Copy example config to config.json."""
    if os.path.exists(CONFIG_PATH):
        print(f"Config already exists at {CONFIG_PATH}")
        print("Delete it first or edit directly.")
        sys.exit(1)
    if not os.path.exists(EXAMPLE_PATH):
        print(f"Error: Example config not found at {EXAMPLE_PATH}", file=sys.stderr)
        sys.exit(1)
    shutil.copy2(EXAMPLE_PATH, CONFIG_PATH)
    print(f"Initialized config from example: {CONFIG_PATH}")


def add_niche(config, name, keywords, sources=None, extra_signal_keywords=None):
    """Add a new niche or update existing one."""
    # Check if niche exists
    for niche in config.get("niches", []):
        if niche["name"].lower() == name.lower():
            print(f"Updating existing niche: {name}")
            if keywords:
                niche["keywords"] = keywords
            if sources:
                existing = set(niche.get("sources", []))
                existing.update(sources)
                niche["sources"] = sorted(existing)
            if extra_signal_keywords:
                niche["extra_signal_keywords"] = extra_signal_keywords
            return config

    # Create new niche
    niche = {
        "name": name,
        "keywords": keywords if keywords else [],
        "sources": sources if sources else [],
    }
    if extra_signal_keywords:
        niche["extra_signal_keywords"] = extra_signal_keywords
    config.setdefault("niches", []).append(niche)
    print(f"Added niche: {name}")
    return config


def remove_niche(config, name):
    """Remove a niche by name."""
    niches = config.get("niches", [])
    original_len = len(niches)
    config["niches"] = [n for n in niches if n["name"].lower() != name.lower()]
    if len(config["niches"]) < original_len:
        print(f"Removed niche: {name}")
    else:
        print(f"Niche not found: {name}", file=sys.stderr)
        sys.exit(1)
    return config


def add_sources(config, sources, niche_name=None):
    """Add sources to a specific niche or all niches."""
    niches = config.get("niches", [])
    if not niches:
        print("Error: No niches configured. Add a niche first.", file=sys.stderr)
        sys.exit(1)

    targets = niches
    if niche_name:
        targets = [n for n in niches if n["name"].lower() == niche_name.lower()]
        if not targets:
            print(f"Error: Niche '{niche_name}' not found.", file=sys.stderr)
            sys.exit(1)

    for niche in targets:
        existing = set(niche.get("sources", []))
        existing.update(sources)
        niche["sources"] = sorted(existing)
        print(f"Updated sources for '{niche['name']}': {niche['sources']}")

    return config


def set_schedule(config, schedule):
    """Set scan schedule."""
    if schedule not in ("daily", "weekly"):
        print("Error: Schedule must be 'daily' or 'weekly'.", file=sys.stderr)
        sys.exit(1)
    config["schedule"] = schedule
    print(f"Schedule set to: {schedule}")
    return config


def set_weights(config, weight_str):
    """Set scoring weights from comma-separated key=value pairs."""
    valid_keys = {"signal_strength", "engagement", "freshness", "competition", "recurrence"}
    weights = config.get("scoring_weights", {})

    for pair in weight_str.split(","):
        pair = pair.strip()
        if "=" not in pair:
            print(f"Error: Invalid weight format '{pair}'. Use key=value.", file=sys.stderr)
            sys.exit(1)
        key, val = pair.split("=", 1)
        key = key.strip()
        if key not in valid_keys:
            print(f"Error: Unknown weight '{key}'. Valid: {valid_keys}", file=sys.stderr)
            sys.exit(1)
        try:
            weights[key] = float(val)
        except ValueError:
            print(f"Error: Weight value must be a number: '{val}'", file=sys.stderr)
            sys.exit(1)

    total = sum(weights.values())
    if abs(total - 1.0) > 0.01:
        print(f"Warning: Weights sum to {total:.2f}, not 1.0. Consider rebalancing.")

    config["scoring_weights"] = weights
    print(f"Scoring weights updated: {weights}")
    return config


def show_config(config):
    """Pretty-print current configuration."""
    print(json.dumps(config, indent=2))


def main():
    parser = argparse.ArgumentParser(description="Configure opportunity-scout")
    parser.add_argument("--init", action="store_true", help="Initialize config from example")
    parser.add_argument("--add-niche", metavar="NAME", help="Add or update a niche")
    parser.add_argument("--keywords", help="Comma-separated niche keywords")
    parser.add_argument("--extra-signal-keywords", help="Comma-separated extra signal keywords")
    parser.add_argument("--add-source", help="Comma-separated sources to add")
    parser.add_argument("--niche", help="Target niche for --add-source")
    parser.add_argument("--remove-niche", metavar="NAME", help="Remove a niche")
    parser.add_argument("--set-schedule", choices=["daily", "weekly"], help="Set scan schedule")
    parser.add_argument("--set-weight", metavar="WEIGHTS", help="Set scoring weights (key=val,...)")
    parser.add_argument("--show", action="store_true", help="Show current config")

    args = parser.parse_args()

    if args.init:
        init_config()
        return

    if not any([args.add_niche, args.add_source, args.remove_niche,
                args.set_schedule, args.set_weight, args.show]):
        parser.print_help()
        return

    config = load_config()

    if args.show:
        show_config(config)
        return

    if args.add_niche:
        keywords = [k.strip() for k in args.keywords.split(",")] if args.keywords else []
        extra = [k.strip() for k in args.extra_signal_keywords.split(",")] if args.extra_signal_keywords else None
        sources = [s.strip() for s in args.add_source.split(",")] if args.add_source else None
        config = add_niche(config, args.add_niche, keywords, sources, extra)
    elif args.add_source:
        sources = [s.strip() for s in args.add_source.split(",")]
        config = add_sources(config, sources, args.niche)

    if args.remove_niche:
        config = remove_niche(config, args.remove_niche)

    if args.set_schedule:
        config = set_schedule(config, args.set_schedule)

    if args.set_weight:
        config = set_weights(config, args.set_weight)

    save_config(config)


if __name__ == "__main__":
    main()
