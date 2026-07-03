#!/usr/bin/env python3
"""huo15-token-optimizer scan — 扫描所有 OpenClaw 工作区，输出 token 消耗报告"""
import os, json, sys

WORKSPACE_BASE = os.path.expanduser("~/.openclaw")
CONFIG_PATH = os.path.join(os.path.dirname(__file__), "..", "config.json")

def load_config():
    with open(CONFIG_PATH) as f:
        return json.load(f)

def count_dream_entries(content):
    count = 0
    for line in content.split("\n"):
        if line.strip().startswith("*") and "at" in line and "GMT" in line:
            count += 1
    return count

def estimate_tokens(size_bytes):
    return int(size_bytes * 0.3)

def scan():
    config = load_config()
    thresholds = config["thresholds"]
    workspaces = []
    total_tokens = 0
    
    for d in sorted(os.listdir(WORKSPACE_BASE)):
        if not d.startswith("workspace"):
            continue
        ws_path = os.path.join(WORKSPACE_BASE, d)
        if not os.path.isdir(ws_path):
            continue
        
        ws = {"name": d.replace("workspace-", "").replace("workspace.", ""), "files": {}, "issues": []}
        ws_tokens = 0
        
        for fname in ["AGENTS.md", "DREAMS.md", "MEMORY.md", "SOUL.md", "USER.md", "IDENTITY.md", "TOOLS.md"]:
            fp = os.path.join(ws_path, fname)
            if not os.path.exists(fp):
                continue
            size = os.path.getsize(fp)
            tokens = estimate_tokens(size)
            ws_tokens += tokens
            
            file_info = {"size": size, "token_est": tokens, "status": "ok"}
            
            if fname == "AGENTS.md" and size > thresholds["agents_max_kb"] * 1024:
                file_info["status"] = "oversized"
                ws["issues"].append(f"AGENTS.md {size}B > {thresholds['agents_max_kb']}KB （自定义格式，需人工确认）")
            elif fname == "DREAMS.md":
                with open(fp) as f:
                    entries = count_dream_entries(f.read())
                file_info["entries"] = entries
                if entries > thresholds["dreams_max_entries"]:
                    file_info["status"] = "oversized"
                    ws["issues"].append(f"DREAMS.md {entries} entries > {thresholds['dreams_max_entries']}")
            elif fname == "MEMORY.md" and size > thresholds["memory_max_kb"] * 1024:
                file_info["status"] = "oversized"
                ws["issues"].append(f"MEMORY.md {size}B > {thresholds['memory_max_kb']}KB")
            
            ws["files"][fname] = file_info
        
        ws["tokens_est"] = ws_tokens
        total_tokens += ws_tokens
        if ws["issues"]:
            workspaces.append(ws)
    
    # Report
    report = {
        "total_tokens_est": total_tokens,
        "total_workspaces_scanned": len(workspaces) + len([d for d in os.listdir(WORKSPACE_BASE) if d.startswith("workspace") and os.path.isdir(os.path.join(WORKSPACE_BASE, d)) and not any(w["name"] == d for w in workspaces)]),
        "workspaces_with_issues": len(workspaces),
        "workspaces": workspaces
    }
    
    print(json.dumps(report, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    scan()
