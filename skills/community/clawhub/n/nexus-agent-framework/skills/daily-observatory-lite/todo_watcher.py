#!/usr/bin/env python3
"""
待辦監控模組
檢查 P0-P1 卡住任務
"""

import os
import re
from datetime import datetime

def check_todo_file():
    """檢查待辦檔案"""
    workspace = os.path.expanduser("~/.openclaw/workspace-frontdesk")
    
    # 嘗試多個待辦檔案來源
    todo_sources = [
        os.path.join(workspace, "AGENTS.md"),
        os.path.join(workspace, "HEARTBEAT.md"),
        os.path.join(workspace, "MEMORY.md")
    ]
    
    for path in todo_sources:
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                lines = f.readlines()
            
            p0_matches = 0
            p1_matches = 0
            
            for line in lines:
                # Skip Markdown table rows (start with |)
                stripped = line.strip()
                if stripped.startswith("|"):
                    continue
                
                # Check for P0/P1 with keywords
                if re.search(r"P0.*?(?:待辦|任務|todo|卡住)", line, re.IGNORECASE):
                    p0_matches += 1
                if re.search(r"P1.*?(?:待辦|任務|todo|卡住)", line, re.IGNORECASE):
                    p1_matches += 1
            
            return {
                "p0_stuck": p0_matches,
                "p1_stuck": p1_matches,
                "source": os.path.basename(path)
            }
    
    return {
        "p0_stuck": 0,
        "p1_stuck": 0,
        "source": "未找到待辦檔案"
    }

def check_todo_alerts():
    """檢查待辦預警"""
    return check_todo_file()

if __name__ == "__main__":
    import json
    print(json.dumps(check_todo_alerts(), indent=2, ensure_ascii=False))
