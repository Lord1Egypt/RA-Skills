#!/usr/bin/env python3
"""
Self-Improving Agent v2 - Proactive Skill Generation Tool
Generate reusable Skills from successful complex tasks
Inspired by Hermes Agent's auto-solidification
"""

import sys
import json
import os
from datetime import datetime

def get_base_dir():
    if "OPENCLAW_HOME" in os.environ:
        return os.environ["OPENCLAW_HOME"]
    home = os.path.expanduser("~")
    for candidate in [
        os.path.join(home, ".openclaw"),
        os.path.join(home, "AppData", "Roaming", "openclaw"),
    ]:
        if os.path.exists(candidate):
            return candidate
    return os.path.join(home, ".openclaw")

OPENCLAW_BASE = get_base_dir()
SELF_IMPROVING_DIR = os.path.join(OPENCLAW_BASE, "memory", "self-improving")
SKILLS_GENERATED_DIR = os.path.join(OPENCLAW_BASE, "skills-generated")
SKILLS_REGISTRY_FILE = os.path.join(SELF_IMPROVING_DIR, "skills_registry.json")

def ensure_dirs():
    for d in [SELF_IMPROVING_DIR, SKILLS_GENERATED_DIR]:
        os.makedirs(d, exist_ok=True)

def load_registry():
    if os.path.exists(SKILLS_REGISTRY_FILE):
        with open(SKILLS_REGISTRY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"skills": []}

def save_registry(registry):
    ensure_dirs()
    with open(SKILLS_REGISTRY_FILE, "w", encoding="utf-8") as f:
        json.dump(registry, f, ensure_ascii=False, indent=2)

def generate_skill(name, trigger, description, files=None, notes=None):
    ensure_dirs()
    
    skill_dir = os.path.join(SKILLS_GENERATED_DIR, name)
    os.makedirs(skill_dir, exist_ok=True)
    
    skill_md = f"""---
name: {name}
description: "{description}"
version: 1.0.0
trigger: "{trigger}"
generated: true
generated_by: self-improving-agent-v2
generated_at: {datetime.now().strftime('%Y-%m-%d')}
---

# {name}

## Description
{description}

## Trigger
{trigger}

## Related Files
"""
    if files:
        for f in files:
            skill_md += f"\n- {f}"
    
    if notes:
        skill_md += f"\n\n## Notes\n{notes}\n"
    
    skill_md += f"""
## Usage

When encountering a related task, reference this Skill to execute.

---
Auto-generated at {datetime.now().isoformat()}
"""
    
    with open(os.path.join(skill_dir, "SKILL.md"), "w", encoding="utf-8") as f:
        f.write(skill_md)
    
    registry = load_registry()
    skill_entry = {
        "name": name,
        "trigger": trigger,
        "description": description,
        "files": files or [],
        "notes": notes or "",
        "created_at": datetime.now().isoformat(),
        "success_count": 1,
        "last_used": datetime.now().isoformat(),
        "auto_trigger": True
    }
    
    for i, s in enumerate(registry["skills"]):
        if s["name"] == name:
            registry["skills"][i] = skill_entry
            break
    else:
        registry["skills"].append(skill_entry)
    
    save_registry(registry)
    
    print(f"[OK] Skill '{name}' generated and registered.")
    print(f"      Location: {skill_dir}")
    print(f"      Registry: {SKILLS_REGISTRY_FILE}")
    return True

def list_skills():
    registry = load_registry()
    if not registry["skills"]:
        print("No skills generated yet.")
        return
    
    print(f"Registered Skills ({len(registry['skills'])}):")
    for s in registry["skills"]:
        print(f"  [{s['name']}] trigger={s['trigger']}")
        print(f"      created={s['created_at']}, used={s['success_count']}x")

def search_skills(query):
    registry = load_registry()
    q = query.lower()
    results = []
    for s in registry.get("skills", []):
        if (q in s.get("trigger", "").lower() or 
            q in s.get("description", "").lower() or
            q in s.get("name", "").lower()):
            results.append(s)
    return results

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python generate_skill.py --name <name> --trigger <trigger> --desc <description> [--files <files>] [--notes <notes>]")
        print("  python generate_skill.py --list")
        print("  python generate_skill.py --search <query>")
        print(f"Storage: {SKILLS_GENERATED_DIR}")
        sys.exit(1)
    
    args = sys.argv[1:]
    
    if "--list" in args:
        list_skills()
        sys.exit(0)
    
    if "--search" in args:
        idx = args.index("--search")
        query = args[idx + 1] if idx + 1 < len(args) else ""
        results = search_skills(query)
        if results:
            print(f"Found {len(results)} skills:")
            for s in results:
                print(f"  [{s['name']}] {s['trigger']}")
        else:
            print("No matching skills found.")
        sys.exit(0)
    
    kwargs = {}
    i = 0
    while i < len(args):
        if args[i] == "--name":
            kwargs["name"] = args[i + 1]
        elif args[i] == "--trigger":
            kwargs["trigger"] = args[i + 1]
        elif args[i] in ("--desc", "--description"):
            kwargs["description"] = args[i + 1]
        elif args[i] == "--files":
            kwargs["files"] = args[i + 1].split(",")
        elif args[i] == "--notes":
            kwargs["notes"] = args[i + 1]
        i += 1
    
    if not kwargs.get("name") or not kwargs.get("trigger") or not kwargs.get("description"):
        print("Error: --name, --trigger, and --desc are required.")
        sys.exit(1)
    
    generate_skill(**kwargs)
