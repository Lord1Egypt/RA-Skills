#!/usr/bin/env python3
"""
Self-Improving Agent v2 - Memory Check Tool
Check relevant memories before executing commands
"""

import sys
import json
import os
from datetime import datetime

# Use environment variable if set, otherwise use ~/.openclaw
def get_base_dir():
    if "OPENCLAW_HOME" in os.environ:
        return os.path.join(os.environ["OPENCLAW_HOME"], "memory", "self-improving")
    home = os.path.expanduser("~")
    # Try to detect OpenClaw home
    for candidate in [
        os.path.join(home, ".openclaw"),
        os.path.join(home, "AppData", "Roaming", "openclaw"),
    ]:
        if os.path.exists(os.path.join(candidate, "memory")):
            return os.path.join(candidate, "memory", "self-improving")
    return os.path.join(home, ".openclaw", "memory", "self-improving")

SELF_IMPROVING_DIR = get_base_dir()
SKILLS_REGISTRY = os.path.join(SELF_IMPROVING_DIR, "skills_registry.json")

def ensure_dir():
    os.makedirs(SELF_IMPROVING_DIR, exist_ok=True)

def load_jsonl(filename):
    path = os.path.join(SELF_IMPROVING_DIR, filename)
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]

def load_skills_registry():
    if os.path.exists(SKILLS_REGISTRY):
        with open(SKILLS_REGISTRY, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"skills": []}

def search_skills(query):
    registry = load_skills_registry()
    q = query.lower()
    results = []
    for s in registry.get("skills", []):
        if (q in s.get("trigger", "").lower() or 
            q in s.get("description", "").lower() or
            q in s.get("name", "").lower()):
            results.append(s)
    return results

def check_memory(command):
    ensure_dir()
    results = {"errors": [], "corrections": [], "best_practices": [], "skills": []}
    q = command.lower()
    
    for e in load_jsonl("errors.jsonl"):
        if q in e.get("command", "").lower() or q in e.get("error", "").lower():
            results["errors"].append(e)
    
    for c in load_jsonl("corrections.jsonl"):
        if q in c.get("topic", "").lower() or q in c.get("wrong", "").lower():
            results["corrections"].append(c)
    
    for b in load_jsonl("best_practices.jsonl"):
        if q in b.get("practice", "").lower() or q in b.get("category", "").lower():
            results["best_practices"].append(b)
    
    results["skills"] = search_skills(command)
    return results

def print_results(results, command):
    found = False
    
    if results["errors"]:
        found = True
        print(f"\n[WARNING] Found {len(results['errors'])} related error(s):")
        for e in results["errors"][:3]:
            print(f"  Command: {e.get('command', '-')}")
            print(f"  Error: {e.get('error', '-')}")
            if e.get("fix"):
                print(f"  Fix: {e.get('fix')}")
            print()
    
    if results["corrections"]:
        found = True
        print(f"[MEMORY] Found {len(results['corrections'])} user correction(s):")
        for c in results["corrections"][:3]:
            print(f"  Topic: {c.get('topic', '-')}")
            print(f"  Wrong: {c.get('wrong', '-')}")
            print(f"  Correct: {c.get('correct', '-')}")
            print()
    
    if results["skills"]:
        found = True
        print(f"[SKILL] Found {len(results['skills'])} registered skill(s):")
        for s in results["skills"][:3]:
            print(f"  [{s.get('name', '-')}] {s.get('trigger', '-')}")
            print(f"    {s.get('description', '-')}")
            print(f"    Success: {s.get('success_count', 0)}x | Last used: {s.get('last_used', '-')}")
            print()
    
    if not found:
        print(f"[OK] No relevant memories found for: {command}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python check_memory.py <command>")
        print(f"Memory dir: {SELF_IMPROVING_DIR}")
        sys.exit(1)
    
    command = " ".join(sys.argv[1:])
    results = check_memory(command)
    print_results(results, command)
