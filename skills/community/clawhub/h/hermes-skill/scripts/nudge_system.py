#!/usr/bin/env python3
"""
智能 Nudge 提醒系统
基于任务复杂度和时间自动触发提醒
"""

import os
import json
import time
from datetime import datetime, timedelta
from pathlib import Path

MEMORY_DIR = Path.home() / "self-improving"
NUDGE_CONFIG = MEMORY_DIR / "nudge_config.json"
NUDGE_LOG = MEMORY_DIR / "nudge_log.json"

DEFAULT_CONFIG = {
    "learning_interval_minutes": 30,      # 学习提醒间隔
    "reflection_interval_minutes": 60,    # 反思提醒间隔  
    "cleanup_interval_hours": 24,         # 清理提醒间隔
    "memory_threshold_percent": 80,       # 内存阈值
    "enabled_nudges": ["learning", "reflection", "cleanup", "memory"]
}

def load_config():
    """加载配置"""
    if NUDGE_CONFIG.exists():
        with open(NUDGE_CONFIG) as f:
            return {**DEFAULT_CONFIG, **json.load(f)}
    return DEFAULT_CONFIG.copy()

def save_config(config):
    """保存配置"""
    with open(NUDGE_CONFIG, "w") as f:
        json.dump(config, f, indent=2)

def load_log():
    """加载日志"""
    if NUDGE_LOG.exists():
        with open(NUDGE_LOG) as f:
            return json.load(f)
    return {"last_nudges": {}, "stats": {}}

def save_log(log):
    """保存日志"""
    with open(NUDGE_LOG, "w") as f:
        json.dump(log, f, indent=2)

def check_memory_usage():
    """检查内存使用率"""
    memory_file = MEMORY_DIR / "memory.md"
    if not memory_file.exists():
        return 0
    
    with open(memory_file) as f:
        lines = f.readlines()
    
    # 粗略估算：每行约 80 字符 = ~20 tokens
    total_chars = sum(len(line) for line in lines)
    max_chars = 2200  # Hermes Agent 标准
    
    return min(100, int(total_chars / max_chars * 100))

def should_nudge(nudge_type, config, log):
    """判断是否应该触发 nudge"""
    now = datetime.now()
    last_nudges = log.get("last_nudges", {})
    
    if nudge_type not in config.get("enabled_nudges", []):
        return False, "disabled"
    
    last_time = last_nudges.get(nudge_type)
    if not last_time:
        return True, "first_time"
    
    last_dt = datetime.fromisoformat(last_time)
    elapsed = (now - last_dt).total_seconds() / 60  # 分钟
    
    intervals = {
        "learning": config["learning_interval_minutes"],
        "reflection": config["reflection_interval_minutes"],
        "cleanup": config["cleanup_interval_hours"] * 60,
        "memory": 0  # 特殊处理
    }
    
    interval = intervals.get(nudge_type, 60)
    return elapsed >= interval, f"elapsed {elapsed:.0f}m >= {interval}m"

def generate_nudge_message(nudge_type, context=None):
    """生成 nudge 消息"""
    messages = {
        "learning": [
            "💡 有新知识该保存了！",
            "💡 刚才学到了什么？记下来吧",
            "💡 积累的经验值得保存"
        ],
        "reflection": [
            "🤔 刚才的任务完成得怎么样？",
            "🧠 可以复盘一下刚才的工作",
            "💭 有什么可以改进的吗？"
        ],
        "cleanup": [
            "🧹 该整理一下记忆了",
            "📊 看看记忆库有什么要清理的",
            "🔄 记忆也该体检一下了"
        ],
        "memory": [
            "⚠️ HOT 内存已超过 80%，该整理了",
            "📝 内存快满了，先备份一下？"
        ]
    }
    
    import random
    msg_list = messages.get(nudge_type, ["💡 提醒"])
    return random.choice(msg_list)

def trigger_nudge(nudge_type, context=None):
    """触发 nudge"""
    config = load_config()
    log = load_log()
    
    # 特殊处理 memory nudge
    if nudge_type == "memory":
        usage = check_memory_usage()
        if usage < config["memory_threshold_percent"]:
            return None, "memory_ok"
        should, reason = True, f"usage_{usage}%"
    else:
        should, reason = should_nudge(nudge_type, config, log)
    
    if not should:
        return None, reason
    
    message = generate_nudge_message(nudge_type, context)
    
    # 记录触发
    log["last_nudges"][nudge_type] = datetime.now().isoformat()
    log["stats"][nudge_type] = log["stats"].get(nudge_type, 0) + 1
    save_log(log)
    
    return {
        "type": nudge_type,
        "message": message,
        "reason": reason,
        "timestamp": datetime.now().isoformat()
    }, "triggered"

def check_all_nudges():
    """检查所有 nudges"""
    config = load_config()
    results = []
    
    for nudge_type in config.get("enabled_nudges", []):
        if nudge_type == "memory":
            usage = check_memory_usage()
            if usage >= config["memory_threshold_percent"]:
                result, _ = trigger_nudge("memory")
                if result:
                    results.append(result)
        else:
            result, _ = trigger_nudge(nudge_type)
            if result:
                results.append(result)
    
    return results

def main():
    import argparse
    parser = argparse.ArgumentParser(description="智能 Nudge 系统")
    parser.add_argument("--check", action="store_true", help="检查所有 nudges")
    parser.add_argument("--trigger", type=str, help="触发特定 nudge")
    parser.add_argument("--config", action="store_true", help="显示配置")
    parser.add_argument("--stats", action="store_true", help="显示统计")
    
    args = parser.parse_args()
    
    if args.check:
        results = check_all_nudges()
        if results:
            for r in results:
                print(r["message"])
        else:
            print("No nudges needed")
    
    elif args.trigger:
        result, reason = trigger_nudge(args.trigger)
        if result:
            print(result["message"])
        else:
            print(f"Skipped: {reason}")
    
    elif args.config:
        config = load_config()
        print(json.dumps(config, indent=2))
    
    elif args.stats:
        log = load_log()
        print(json.dumps(log["stats"], indent=2))

if __name__ == "__main__":
    main()
