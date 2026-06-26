#!/usr/bin/env python3
"""
Skill Usage Tracker - 技能使用追踪系统
接入 memory-optimization KG，记录技能调用历史

Usage:
    python3 skill_tracker.py record --skill coding-agent --status success
    python3 skill_tracker.py record --skill weather --status success --duration 0.5
    python3 skill_tracker.py stats
    python3 skill_tracker.py stats --skill coding-agent
"""

import json
import os
import sys
import hashlib
import argparse
from datetime import datetime
from pathlib import Path
from collections import Counter

SCRIPT_DIR = Path(__file__).parent
KG_FILE = SCRIPT_DIR / "ontology" / "graph.jsonl"

# 尝试导入 memory-optimization 的 KG 功能
MEMORY_ONTOLOGY_PATH = Path.home() / ".openclaw" / "workspace" / "skills" / "memory-optimization" / "scripts"
if str(MEMORY_ONTOLOGY_PATH) not in sys.path:
    sys.path.insert(0, str(MEMORY_ONTOLOGY_PATH))

try:
    from memory_ontology import get_entities_by_type, create_entity
    KG_FUNCTIONS_AVAILABLE = True
except ImportError:
    KG_FUNCTIONS_AVAILABLE = False

# 技能类型定义
SKILL_CATEGORIES = {
    "feishu": ["feishu-doc", "feishu-drive", "feishu-perm", "feishu-wiki", "feishu-evolver-wrapper"],
    "apple": ["apple-notes", "apple-reminders", "things-mac"],
    "coding": ["coding-agent", "skill-creator", "github-integration"],
    "memory": ["memory-optimization", "evolving-memory", "openspace", "capability-evolver"],
    "api": ["notion", "notion-api", "mcporter", "acpx"],
    "system": ["healthcheck", "node-connect", "clawhub", "find-skills"],
    "utility": ["weather", "bounty-hunter"],
}


def get_skill_category(skill_name: str) -> str:
    """获取技能分类"""
    for category, skills in SKILL_CATEGORIES.items():
        if skill_name in skills:
            return category
    return "other"


def generate_entity_id(prefix: str = "skill") -> str:
    """生成实体 ID"""
    timestamp = datetime.now().isoformat()
    hash_obj = hashlib.md5(timestamp.encode())
    return f"{prefix}_{hash_obj.hexdigest()[:8]}"


def record_skill_usage(skill_name: str, status: str = "success", duration: float = None, error: str = None):
    """记录技能使用"""
    properties = {
        "skill_name": skill_name,
        "category": get_skill_category(skill_name),
        "status": status,  # success, failed, partial
    }
    if duration is not None:
        properties["duration_seconds"] = duration
    if error is not None:
        properties["error"] = error
    
    # 优先使用 memory-optimization KG 函数
    if KG_FUNCTIONS_AVAILABLE:
        try:
            entity_id = create_entity("SkillUsage", properties)
            print(f"✅ Recorded: {skill_name} ({status}) [KG]")
            return entity_id
        except Exception as e:
            print(f"⚠️ KG 函数调用失败: {e}, 回退到原始写入")
    
    # 回退：直接写文件
    entity_id = generate_entity_id("skill")
    timestamp = datetime.now().isoformat()
    
    entity = {
        "op": "create",
        "entity": {
            "id": entity_id,
            "type": "SkillUsage",
            "properties": properties,
            "tags": [f"#{skill_name}", f"#{status}", "#skill-usage"],
            "created": timestamp,
            "updated": timestamp,
        },
        "timestamp": timestamp
    }
    
    KG_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(KG_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(entity, ensure_ascii=False) + "\n")
    
    print(f"✅ Recorded: {skill_name} ({status}) [FILE]")
    return entity_id


def get_stats(skill_name: str = None) -> dict:
    """获取技能使用统计"""
    if not KG_FILE.exists():
        return {"total": 0, "by_skill": {}, "by_status": {}, "by_category": {}}
    
    stats = {"total": 0, "by_skill": Counter(), "by_status": Counter(), "by_category": Counter()}
    
    # 优先使用 memory-optimization KG 函数
    global KG_FUNCTIONS_AVAILABLE
    if KG_FUNCTIONS_AVAILABLE:
        try:
            entities = get_entities_by_type("SkillUsage")
            for e in entities:
                props = e.get("properties", {})
                if skill_name and props.get("skill_name") != skill_name:
                    continue
                stats["total"] += 1
                stats["by_skill"][props.get("skill_name", "unknown")] += 1
                stats["by_status"][props.get("status", "unknown")] += 1
                stats["by_category"][props.get("category", "other")] += 1
        except Exception as e:
            print(f"⚠️ KG 函数调用失败: {e}, 回退到原始解析")
            KG_FUNCTIONS_AVAILABLE = False
    
    # 回退：原始 JSON 解析
    if not KG_FUNCTIONS_AVAILABLE:
        with open(KG_FILE, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line: continue
                try:
                    record = json.loads(line)
                    if record.get("op") == "create":
                        entity = record.get("entity", {})
                        if entity.get("type") == "SkillUsage":
                            props = entity.get("properties", {})
                            
                            # 过滤指定技能
                            if skill_name and props.get("skill_name") != skill_name:
                                continue
                            
                            stats["total"] += 1
                            skill = props.get("skill_name", "unknown")
                            status = props.get("status", "unknown")
                            category = props.get("category", "other")
                            
                            stats["by_skill"][skill] += 1
                            stats["by_status"][status] += 1
                            stats["by_category"][category] += 1
                except Exception:
                    continue
    
    # 转换 Counter 为 dict
    stats["by_skill"] = dict(stats["by_skill"])
    stats["by_status"] = dict(stats["by_status"])
    stats["by_category"] = dict(stats["by_category"])
    
    return stats


def print_stats(stats: dict, skill_name: str = None):
    """打印统计信息"""
    print(f"\n📊 技能使用统计")
    print(f"=" * 40)
    print(f"总调用次数: {stats['total']}")
    
    if skill_name:
        print(f"\n🔍 技能: {skill_name}")
    
    if stats["by_skill"]:
        print(f"\n📦 按技能:")
        for skill, count in sorted(stats["by_skill"].items(), key=lambda x: -x[1]):
            print(f"   {skill}: {count}")
    
    if stats["by_status"]:
        print(f"\n📈 按状态:")
        for status, count in sorted(stats["by_status"].items()):
            emoji = "✅" if status == "success" else "❌" if status == "failed" else "⚠️"
            print(f"   {emoji} {status}: {count}")
    
    if stats["by_category"]:
        print(f"\n📂 按分类:")
        for cat, count in sorted(stats["by_category"].items(), key=lambda x: -x[1]):
            print(f"   {cat}: {count}")


def scan_sessions(save_to_kg=False):
    """扫描 session 历史，自动识别技能调用"""
    
    # 如果需要保存，先加载上次扫描的记录（避免重复写入）
    last_scan_file = SCRIPT_DIR / "ontology" / ".last_scan.json"
    last_scan = {}
    if last_scan_file.exists():
        try:
            last_scan = json.loads(last_scan_file.read_text())
        except Exception:
            pass
    # 技能调用模式（命令 -> 技能名）
    SKILL_PATTERNS = {
        "openclaw skills": "clawhub",
        "openclaw status": "system",
        "evolver": "capability-evolver",
        "python3 memory_ontology": "memory-optimization",
        "python3 skill_tracker": "skill-tracker",
        "python3 daily-cleanup": "memory-optimization",
        "things": "things-mac",
        "memo": "apple-notes",
        "remindctl": "apple-reminders",
        "gh ": "github",
        "curl": "network",
        "web_fetch": "utility",
        "web_search": "utility",
    }
    
    sessions_dir = Path.home() / ".openclaw" / "agents" / "main" / "sessions"
    if not sessions_dir.exists():
        print("❌ No sessions directory found")
        return
    
    found_skills = Counter()
    
    for session_file in sorted(sessions_dir.glob("*.jsonl"))[-10:]:  # 最近 10 个 session
        try:
            with open(session_file, 'r', encoding='utf-8') as f:
                for line in f:
                    try:
                        record = json.loads(line)
                        # 查找 toolCall 类型
                        if record.get("type") == "message":
                            content = record.get("message", {}).get("content", [])
                            for item in content:
                                if item.get("type") == "toolCall":
                                    args = item.get("arguments", {})
                                    command = args.get("command", "")
                                    if command:
                                        for pattern, skill in SKILL_PATTERNS.items():
                                            if pattern in command:
                                                found_skills[skill] += 1
                    except Exception:
                        continue
        except Exception:
            continue
    
    print(f"\n🔍 最近 session 扫描结果:")
    print("=" * 40)
    if not found_skills:
        print("   (未识别到技能调用)")
    for skill, count in found_skills.most_common():
        print(f"   {skill}: {count} 次")
    
    # 写入 KG
    if save_to_kg and found_skills:
        print(f"\n💾 写入 KG...")
        # 只写入有变化的技能
        for skill, count in found_skills.items():
            prev = last_scan.get(skill, 0)
            if count > prev:  # 有新增调用
                for _ in range(count - prev):
                    record_skill_usage(skill, "success")
        
        # 保存扫描记录
        last_scan_file.parent.mkdir(parents=True, exist_ok=True)
        last_scan_file.write_text(json.dumps(dict(found_skills)))
        print(f"✅ 已同步 {sum(found_skills.values())} 条记录到 KG")
    
    return dict(found_skills)


def main():
    parser = argparse.ArgumentParser(description="Skill Usage Tracker")
    subparsers = parser.add_subparsers(dest="command", help="Commands")
    
    # record 命令
    record_parser = subparsers.add_parser("record", help="记录技能使用")
    record_parser.add_argument("--skill", required=True, help="技能名称")
    record_parser.add_argument("--status", default="success", choices=["success", "failed", "partial"], help="调用状态")
    record_parser.add_argument("--duration", type=float, help="耗时（秒）")
    record_parser.add_argument("--error", help="错误信息")
    
    # stats 命令
    stats_parser = subparsers.add_parser("stats", help="查看统计")
    stats_parser.add_argument("--skill", help="筛选技能")
    
    # scan 命令
    scan_parser = subparsers.add_parser("scan", help="扫描 session 历史自动识别技能")
    scan_parser.add_argument("--save", action="store_true", help="将结果写入 KG")
    
    args = parser.parse_args()
    
    if args.command == "record":
        record_skill_usage(args.skill, args.status, args.duration, args.error)
    
    elif args.command == "stats":
        stats = get_stats(args.skill)
        print_stats(stats, args.skill)
    
    elif args.command == "scan":
        scan_sessions(save_to_kg=args.save if hasattr(args, 'save') else False)
    
    else:
        parser.print_help()


if __name__ == "__main__":
    main()