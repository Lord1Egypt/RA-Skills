#!/usr/bin/env python3
"""
memory_sync.py — Sync Cross-Agent Intel sections across all agent MEMORY.md files.
Usage: python3 memory_sync.py --base /data/.openclaw --agents pat scout publisher builder
"""
import os
import re
import argparse
import datetime

def read_section(path, section_name):
    if not os.path.exists(path):
        return ""
    content = open(path).read()
    pattern = rf"## {re.escape(section_name)}\n(.*?)(?=\n## |\Z)"
    m = re.search(pattern, content, re.DOTALL)
    return m.group(1).strip() if m else ""

def write_section(path, section_name, new_content):
    if not os.path.exists(path):
        print(f"  SKIP (not found): {path}")
        return
    content = open(path).read()
    new_block = f"## {section_name}\n{new_content}\n"
    pattern = rf"## {re.escape(section_name)}\n.*?(?=\n## |\Z)"
    if re.search(pattern, content, re.DOTALL):
        content = re.sub(pattern, new_block.rstrip(), content, flags=re.DOTALL)
    else:
        content = content.rstrip() + f"\n\n{new_block}"
    with open(path, "w") as f:
        f.write(content)
    print(f"  Updated: {path}")

def sync(base, agents):
    today = datetime.date.today().isoformat()
    intel_parts = []
    for agent in agents:
        mem_path = os.path.join(base, f"workspace-{agent}", "MEMORY.md")
        intel = read_section(mem_path, "Cross-Agent Intel")
        if intel and intel.strip() not in ("", "—"):
            intel_parts.append(f"### From {agent} ({today})\n{intel}")

    if not intel_parts:
        print("No Cross-Agent Intel found to sync.")
        return

    combined = "\n\n".join(intel_parts)
    for agent in agents:
        mem_path = os.path.join(base, f"workspace-{agent}", "MEMORY.md")
        write_section(mem_path, "Cross-Agent Intel", combined)
    print(f"\nSynced intel across {len(agents)} agents.")

def main():
    parser = argparse.ArgumentParser(description="Sync cross-agent memory")
    parser.add_argument("--base", default="/data/.openclaw")
    parser.add_argument("--agents", nargs="+", default=["pat","scout","publisher","builder"])
    args = parser.parse_args()
    sync(args.base, args.agents)

if __name__ == "__main__":
    main()
