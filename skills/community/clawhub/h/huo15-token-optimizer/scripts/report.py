#!/usr/bin/env python3
"""huo15-token-optimizer report — Token 消耗统计看板"""
import os, json, sys
from datetime import datetime

WORKSPACE_BASE = os.path.expanduser("~/.openclaw")
CONFIG_PATH = os.path.join(os.path.dirname(__file__), "..", "config.json")

def estimate_tokens(size_bytes):
    return int(size_bytes * 0.3)

def report():
    config = load_config() if os.path.exists(CONFIG_PATH) else {}
    
    rows = []
    grand_size = 0
    file_types = {}
    
    for d in sorted(os.listdir(WORKSPACE_BASE)):
        if not d.startswith("workspace"):
            continue
        ws_path = os.path.join(WORKSPACE_BASE, d)
        if not os.path.isdir(ws_path):
            continue
        
        ws_name = d.replace("workspace-", "").replace("workspace.", "")
        ws_size = 0
        
        for fname in ["AGENTS.md", "DREAMS.md", "MEMORY.md", "SOUL.md", "USER.md", "IDENTITY.md", "TOOLS.md"]:
            fp = os.path.join(ws_path, fname)
            if os.path.exists(fp):
                size = os.path.getsize(fp)
                ws_size += size
                file_types[fname] = file_types.get(fname, 0) + size
        
        if ws_size > 0:
            rows.append((ws_name, ws_size, estimate_tokens(ws_size)))
            grand_size += ws_size
    
    rows.sort(key=lambda x: x[1], reverse=True)
    
    print("# Token 消耗报告")
    print(f"生成: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"总 token 估算: {estimate_tokens(grand_size):,} tokens ({grand_size/1024:.1f}KB)")
    print()
    
    print("## 工作区排名")
    print("| 工作区 | 大小 | Token 估算 |")
    print("|--------|------|-----------|")
    for name, size, tokens in rows[:15]:
        bar = "█" * min(int(size / grand_size * 10), 10) if grand_size > 0 else ""
        print(f"| {name[:30]} | {size/1024:.1f}KB | ~{tokens:,} |")
    
    print()
    print("## 文件类型占比")
    print("| 文件类型 | 大小 | 占比 |")
    print("|----------|------|------|")
    for fname, size in sorted(file_types.items(), key=lambda x: x[1], reverse=True):
        pct = size / grand_size * 100 if grand_size > 0 else 0
        print(f"| {fname} | {size/1024:.1f}KB | {pct:.0f}% |")

def load_config():
    try:
        with open(CONFIG_PATH) as f:
            return json.load(f)
    except:
        return {}

if __name__ == "__main__":
    report()
