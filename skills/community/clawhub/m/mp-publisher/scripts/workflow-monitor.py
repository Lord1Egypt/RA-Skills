#!/usr/bin/env python3
"""
公众号文章发布流程监控器
========================
监控和协调文章发布流程的各个阶段

用法:
    python workflow-monitor.py start <article_file>   # 开始新流程
    python workflow-monitor.py update <stage> [score] # 更新阶段
    python workflow-monitor.py check                  # 检查超时
    python workflow-monitor.py status                 # 查看状态
    python workflow-monitor.py complete               # 完成流程
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path

# ============================================================================
# 配置
# ============================================================================

STATE_FILE = Path.home() / ".openclaw" / "workspace-work" / ".workflow-state.json"
TIMEOUT_MINUTES = 30  # 每个阶段超时时间

STAGES = ["writer", "reviewer", "designer", "mp-editor"]

# ============================================================================
# 状态管理
# ============================================================================

def load_state():
    """加载流程状态"""
    if not STATE_FILE.exists():
        return None
    try:
        with open(STATE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return None

def save_state(state):
    """保存流程状态"""
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)

def get_current_time():
    """获取当前时间字符串"""
    return datetime.now().isoformat()

def time_diff_minutes(start_time):
    """计算时间差（分钟）"""
    start = datetime.fromisoformat(start_time)
    now = datetime.now()
    return (now - start).total_seconds() / 60

# ============================================================================
# 命令处理
# ============================================================================

def cmd_start(article_file):
    """开始新流程"""
    state = {
        "article": article_file,
        "stage": "writer",
        "start_time": get_current_time(),
        "stage_start_time": get_current_time(),
        "retry_count": 0,
        "score": None,
        "status": "running"
    }
    save_state(state)
    print(f"[OK] 流程已启动: {article_file}")
    print(f"     当前阶段: writer")

def cmd_update(stage, score=None):
    """更新阶段"""
    state = load_state()
    if not state:
        print("[ERROR] 没有正在运行的流程")
        return 1
    
    # 验证阶段顺序
    current_idx = STAGES.index(state["stage"]) if state["stage"] in STAGES else -1
    next_idx = STAGES.index(stage) if stage in STAGES else -1
    
    if next_idx <= current_idx and stage != "writer":
        print(f"[WARN] 阶段顺序可能有问题: {state['stage']} -> {stage}")
    
    state["stage"] = stage
    state["stage_start_time"] = get_current_time()
    if score:
        state["score"] = score
    state["status"] = "running"
    
    save_state(state)
    print(f"[OK] 阶段已更新: {stage}")
    if score:
        print(f"     评分: {score}")

def cmd_check():
    """检查超时"""
    state = load_state()
    if not state:
        print("[]")
        return 0
    
    if state["status"] != "running":
        print(json.dumps(state, ensure_ascii=False))
        return 0
    
    minutes = time_diff_minutes(state["stage_start_time"])
    
    if minutes > TIMEOUT_MINUTES:
        state["status"] = "timeout"
        save_state(state)
        print(json.dumps({
            "status": "timeout",
            "article": state["article"],
            "stage": state["stage"],
            "minutes": round(minutes, 1)
        }, ensure_ascii=False))
        return 1
    else:
        print(json.dumps({
            "status": "running",
            "article": state["article"],
            "stage": state["stage"],
            "minutes": round(minutes, 1)
        }, ensure_ascii=False))
        return 0

def cmd_status():
    """查看状态"""
    state = load_state()
    if not state:
        print("[INFO] 没有正在运行的流程")
        return 0
    
    print(f"文章: {state.get('article', 'N/A')}")
    print(f"阶段: {state.get('stage', 'N/A')}")
    print(f"状态: {state.get('status', 'N/A')}")
    print(f"评分: {state.get('score', 'N/A')}")
    print(f"重试: {state.get('retry_count', 0)}")
    
    if "stage_start_time" in state:
        minutes = time_diff_minutes(state["stage_start_time"])
        print(f"当前阶段用时: {round(minutes, 1)} 分钟")

def cmd_complete():
    """完成流程"""
    state = load_state()
    if not state:
        print("[ERROR] 没有正在运行的流程")
        return 1
    
    state["status"] = "completed"
    state["end_time"] = get_current_time()
    save_state(state)
    print(f"[OK] 流程已完成: {state['article']}")

def cmd_increment():
    """增加重试计数"""
    state = load_state()
    if not state:
        print("[ERROR] 没有正在运行的流程")
        return 1
    
    state["retry_count"] = state.get("retry_count", 0) + 1
    save_state(state)
    print(f"[OK] 重试计数: {state['retry_count']}")

# ============================================================================
# 主函数
# ============================================================================

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return 0
    
    cmd = sys.argv[1]
    
    if cmd == "start" and len(sys.argv) >= 3:
        return cmd_start(sys.argv[2])
    elif cmd == "update" and len(sys.argv) >= 3:
        score = int(sys.argv[3]) if len(sys.argv) >= 4 else None
        return cmd_update(sys.argv[2], score)
    elif cmd == "check":
        return cmd_check()
    elif cmd == "status":
        return cmd_status()
    elif cmd == "complete":
        return cmd_complete()
    elif cmd == "increment":
        return cmd_increment()
    else:
        print(__doc__)
        return 1

if __name__ == "__main__":
    sys.exit(main())
