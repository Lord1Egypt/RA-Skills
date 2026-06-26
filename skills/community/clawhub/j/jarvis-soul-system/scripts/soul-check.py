#!/usr/bin/env python3
"""Validate SOUL.md files for all agents. Fixed encoding issues."""
import os, sys

AGENTS_DIR = os.path.expanduser("~/.openclaw/agents")
REQUIRED_SECTIONS = ["人格", "核心特质", "核心职责", "核心原则"]

def check():
    issues = []
    agents = sorted([d for d in os.listdir(AGENTS_DIR)
                     if os.path.isdir(os.path.join(AGENTS_DIR, d))])

    for name in agents:
        soul = os.path.join(AGENTS_DIR, name, "SOUL.md")
        if not os.path.exists(soul):
            issues.append(("ERROR", name, "missing SOUL.md"))
            continue

        try:
            with open(soul, 'r', encoding='utf-8') as f:
                content = f.read()
        except UnicodeDecodeError:
            issues.append(("ERROR", name, "encoding error in SOUL.md"))
            continue

        size = os.path.getsize(soul)
        missing = [s for s in REQUIRED_SECTIONS if s not in content]
        has_collab = "协作协议" in content or "上级" in content or "协议" in content

        if missing:
            issues.append(("WARN", name, f"missing sections: {', '.join(missing)}"))
        elif not has_collab:
            issues.append(("WARN", name, "missing collaboration protocol"))
        else:
            # Extract personality line
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
                    persona = line.strip()[:60]
                    break
            issues.append(("OK", name, f"{size} bytes | {persona}"))

    print(f"\n{'='*60}")
    print(f"Agent Soul Check — {len(agents)} agents scanned")
    print(f"{'='*60}")
    
    errors = 0
    warnings = 0
    oks = 0
    
    for status, name, msg in issues:
        if status == "ERROR":
            print(f"  [ERROR] {name}: {msg}")
            errors += 1
        elif status == "WARN":
            print(f"  [WARN]  {name}: {msg}")
            warnings += 1
        else:
            print(f"  [OK]    {name}: {msg}")
            oks += 1

    print(f"\n  OK: {oks}  WARN: {warnings}  ERROR: {errors}")
    print(f"{'='*60}")

    return 0 if not errors else 1

if __name__ == "__main__":
    sys.exit(check())