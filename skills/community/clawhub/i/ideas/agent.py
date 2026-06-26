#!/usr/bin/env python3
"""Ideas skill - AI handles all logic via SKILL.md"""
import os, json
SKILL_DIR = os.path.expanduser("~/.openclaw/skills/ideas")

def read(path):
    if os.path.exists(path):
        with open(path) as f: return json.load(f)
    return {"ideas": []}

def write(path, data):
    with open(path, 'w') as f: json.dump(data, f, indent=2, ensure_ascii=False)

def path(file):
    return {
        "ideas": f"{SKILL_DIR}/ideas.json",
    }[file]

if __name__ == "__main__":
    print("按SKILL.md规则处理：记录/查询/更新/删除想法")
