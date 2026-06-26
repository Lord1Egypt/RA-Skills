#!/usr/bin/env python3
"""
routing_config.py — Generate openclaw.json agent entries for a multi-agent fleet.
Usage: python3 routing_config.py --output /data/.openclaw/openclaw.json
"""
import json
import argparse
import os

AGENT_TEMPLATES = {
    "main": {
        "name": "main", "agentId": "main",
        "workspace": "/data/.openclaw/workspace-pat",
        "model": {
            "primary": "openrouter/minimax/minimax-m2.5",
            "fallbacks": ["openrouter/deepseek/deepseek-v3.2", "openrouter/moonshotai/kimi-k2.5"]
        }
    },
    "scout": {
        "name": "Scout", "agentId": "scout",
        "workspace": "/data/.openclaw/workspace-scout",
        "model": {
            "primary": "openrouter/deepseek/deepseek-v3.2",
            "fallbacks": ["openrouter/minimax/minimax-m2.5", "openrouter/moonshotai/kimi-k2.5"]
        }
    },
    "publisher": {
        "name": "Publisher", "agentId": "publisher",
        "workspace": "/data/.openclaw/workspace-publisher",
        "model": {
            "primary": "openrouter/minimax/minimax-m2.5",
            "fallbacks": ["openrouter/deepseek/deepseek-v3.2", "openrouter/moonshotai/kimi-k2.5"]
        }
    },
    "builder": {
        "name": "Builder", "agentId": "builder",
        "workspace": "/data/.openclaw/workspace-builder",
        "model": {
            "primary": "openrouter/deepseek/deepseek-v3.2",
            "fallbacks": ["openrouter/minimax/minimax-m2.5", "openrouter/moonshotai/kimi-k2.5"]
        }
    }
}

CRON_TEMPLATES = [
    {"name": "Morning Briefing", "agentId": "main", "schedule": {"expr": "0 7 * * *"}},
    {"name": "Evening Summary",  "agentId": "main", "schedule": {"expr": "0 20 * * *"}},
    {"name": "Scout: Marketplace", "agentId": "scout", "schedule": {"expr": "0 10 * * *"}},
    {"name": "Scout: Inbound",     "agentId": "scout", "schedule": {"expr": "0 16 * * *"}},
    {"name": "Publisher: Tweet",   "agentId": "publisher", "schedule": {"expr": "0 8 * * *"}},
    {"name": "Publisher: Content", "agentId": "publisher", "schedule": {"expr": "0 9 * * 1,3,5"}},
    {"name": "Publisher: Video",   "agentId": "publisher", "schedule": {"expr": "0 10 * * 2,4"}},
    {"name": "Builder: Daily",     "agentId": "builder",   "schedule": {"expr": "0 10 * * *"}},
]

def generate(agents, output_path):
    config = {"agents": {"list": [AGENT_TEMPLATES[a] for a in agents if a in AGENT_TEMPLATES]}}
    if output_path:
        if os.path.exists(output_path):
            existing = json.load(open(output_path))
            existing["agents"]["list"] = config["agents"]["list"]
            config = existing
        with open(output_path, "w") as f:
            json.dump(config, f, indent=2)
        print(f"Written to {output_path}")
    else:
        print(json.dumps(config, indent=2))

def main():
    parser = argparse.ArgumentParser(description="Generate OpenClaw routing config")
    parser.add_argument("--agents", nargs="+", default=["main","scout","publisher","builder"])
    parser.add_argument("--output", default=None, help="Path to openclaw.json (prints if omitted)")
    args = parser.parse_args()
    generate(args.agents, args.output)

if __name__ == "__main__":
    main()
