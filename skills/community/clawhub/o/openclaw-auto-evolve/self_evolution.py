#!/usr/bin/env python3
"""
OpenClaw 自进化系统 - 轻量版
直接可用的核心功能，不依赖外部core模块
"""

import json
import os
from pathlib import Path
from datetime import datetime

WORKSPACE = Path(os.environ.get("OPENCLAW_WORKSPACE", "/root/.openclaw/workspace"))
STATE_DIR = WORKSPACE / "state"
LEARNINGS_DIR = WORKSPACE / ".learnings"

def get_system_health():
    """获取系统健康状态"""
    health_score = 100
    issues = []
    
    # 检查关键文件
    critical_files = [
        WORKSPACE / "SOUL.md",
        WORKSPACE / "MEMORY.md",
        WORKSPACE / "AGENTS.md"
    ]
    
    for f in critical_files:
        if not f.exists():
            health_score -= 20
            issues.append(f"缺失: {f.name}")
    
    return {"score": health_score, "issues": issues}

def get_rules_summary():
    """获取规则摘要"""
    rules_file = STATE_DIR / "auto_learned_rules.md"
    if not rules_file.exists():
        return {"count": 0, "recent": []}
    
    with open(rules_file) as f:
        content = f.read()
    
    # 简单统计
    lines = [l for l in content.split('\n') if l.strip().startswith('-')]
    return {"count": len(lines), "recent": lines[:5]}

def record_learning(insight, source="manual"):
    """记录学习心得"""
    LEARNINGS_DIR.mkdir(exist_ok=True)
    today = datetime.now().strftime("%Y-%m-%d")
    learning_file = LEARNINGS_DIR / f"{today}-learning.md"
    
    content = f"""# 学习记录 - {today}

## 来源: {source}

### 洞察
{insight}

---
记录时间: {datetime.now().isoformat()}
"""
    
    with open(learning_file, "a") as f:
        f.write(content + "\n")
    
    return {"status": "success", "file": str(learning_file)}

# 技能入口点
def invoke(query: str) -> dict:
    """技能主入口"""
    query = query.lower()
    
    if "健康" in query or "health" in query:
        return get_system_health()
    elif "规则" in query or "rules" in query:
        return get_rules_summary()
    elif "学习" in query:
        return {"status": "ready", "message": "请输入你想要记录的学习内容"}
    else:
        return {
            "status": "ready",
            "message": "自进化系统就绪。使用: /健康 查看状态, /规则 查看规则"
        }

if __name__ == "__main__":
    print(json.dumps(invoke("状态"), ensure_ascii=False, indent=2))