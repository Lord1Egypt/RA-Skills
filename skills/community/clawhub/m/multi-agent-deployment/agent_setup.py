#!/usr/bin/env python3
"""
agent_setup.py — Create OpenClaw agent workspace directory structure.
Usage: python3 agent_setup.py --agents pat scout publisher builder --base /data/.openclaw
"""
import os
import json
import argparse
import datetime

SOUL_TEMPLATE = """# Soul

You are {name}, an AI agent in a multi-agent OpenClaw fleet.

## Mission
[Define this agent's specific role and responsibilities]

## Every Session
1. Read SOUL.md
2. Read USER.md
3. MEMORY.md loads automatically
4. Read latest memory/YYYY-MM-DD.md
5. Check drafts/ for pending items

## Hard Limits
- NEVER act without explicit approval for public-facing actions
- NEVER fabricate data or metrics
"""

MEMORY_TEMPLATE = """Last updated: {date}

## Active Priorities

## Key Decisions

## Lessons Learned

## Cross-Agent Intel
"""

SETTINGS = {
    "hooks": {
        "internal": {"enabled": True},
        "session-memory": {"enabled": True, "messages": 25},
        "bootstrap-extra-files": {"enabled": True, "paths": ["memory/*.md"]}
    }
}

CLAUDEIGNORE = "*.db\n*.jsonl\narchive-v1/\n*.bak*\n*.pyc\n__pycache__/\n*.log\n"

def create_workspace(base_path, agent_name):
    ws = os.path.join(base_path, f"workspace-{agent_name.lower()}")
    for d in [ws, os.path.join(ws, "memory"), os.path.join(ws, "drafts"),
              os.path.join(ws, "skills"), os.path.join(ws, ".claude")]:
        os.makedirs(d, exist_ok=True)
        print(f"  mkdir: {d}")

    today = datetime.date.today().isoformat()
    files = {
        "SOUL.md": SOUL_TEMPLATE.format(name=agent_name),
        "MEMORY.md": MEMORY_TEMPLATE.format(date=today),
        ".claude/settings.json": json.dumps(SETTINGS, indent=2),
        ".claudeignore": CLAUDEIGNORE,
    }
    for fname, content in files.items():
        path = os.path.join(ws, fname)
        with open(path, "w") as f:
            f.write(content)
        print(f"  wrote: {fname}")
    print(f"  done: {ws}")

def main():
    parser = argparse.ArgumentParser(description="Create OpenClaw agent workspaces")
    parser.add_argument("--agents", nargs="+", required=True)
    parser.add_argument("--base", default="/data/.openclaw")
    args = parser.parse_args()
    for agent in args.agents:
        print(f"\nSetting up: {agent}")
        create_workspace(args.base, agent)
    print("\nDone. Edit each SOUL.md to define agent missions.")

if __name__ == "__main__":
    main()
