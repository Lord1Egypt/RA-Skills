#!/usr/bin/env python3
"""List all agents and their SOUL.md status. Fixed encoding issues."""
import os

AGENTS_DIR = os.path.expanduser("~/.openclaw/agents")

def list_agents():
    agents = sorted([d for d in os.listdir(AGENTS_DIR)
                     if os.path.isdir(os.path.join(AGENTS_DIR, d))])

    print(f"\n{'Agent':<20} {'SOUL.md':<10} {'Size':<10} Personality")
    print("-" * 70)

    for name in agents:
        soul = os.path.join(AGENTS_DIR, name, "SOUL.md")
        if os.path.exists(soul):
            size = os.path.getsize(soul)
            size_str = f"{size/1024:.1f}KB" if size > 1024 else f"{size}B"
            try:
                with open(soul, 'r', encoding='utf-8') as f:
                    content = f.read()
            except UnicodeDecodeError:
                size_str = "ENCODING ERROR"
                persona = "?"
            else:
                # Extract personality - look for first line after "## 人格" until next "##"
                lines = content.split('\n')
                persona = ""
                in_personality = False
                for line in lines:
                    if '## ' in line and ('人格' in line or 'Personality' in line):
                        in_personality = True
                        continue
                    if in_personality and line.strip():
                        if line.strip().startswith('## '):
                            break
                        persona = line.strip()[:50]
                        break
                if not persona:
                    persona = "(not set)"
            print(f"{name:<20} OK        {size_str:<10} {persona}")
        else:
            print(f"{name:<20} MISSING   -           -")

    print(f"\nTotal: {len(agents)} agents")
    with_soul = sum(1 for n in agents if os.path.exists(os.path.join(AGENTS_DIR, n, "SOUL.md")))
    print(f"With soul: {with_soul}/{len(agents)}")

if __name__ == "__main__":
    list_agents()