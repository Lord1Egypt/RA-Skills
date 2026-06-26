#!/usr/bin/env python3
"""
ontology-clawra 记忆管理器
三层记忆架构：热层(graph.jsonl) / 冷层(archive/) / 暖层(memory.md)

写入热层必须满足以下条件之一：
1. 用户亲口确认的事实
2. 踩坑得出的非显而易见规律
3. 跨领域通用原则/真理
4. 置信度为 CONFIRMED 或 ASSUMED（有来源）

核心原则：只写入"改变了世界建模"的知识，而非仅仅"信息"
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Optional, List, Dict, Any
from dataclasses import dataclass, field
from enum import Enum

# ============================================================
# 配置
# ============================================================

SKILL_DIR = Path(__file__).parent.parent
MEMORY_DIR = SKILL_DIR / "scripts" / "memory"  # 实际路径
ARCHIVE_DIR = MEMORY_DIR / "archive"
GRAPH_FILE = MEMORY_DIR / "graph.jsonl"
MEMORY_MD = SKILL_DIR / "scripts" / "memory" / "memory.md"  # 暖层
RULES_FILE = MEMORY_DIR / "rules.yaml"
LAWS_FILE = MEMORY_DIR / "laws.yaml"

# 确保目录存在
MEMORY_DIR.mkdir(exist_ok=True)
ARCHIVE_DIR.mkdir(exist_ok=True)


# ============================================================
# 类型定义
# ============================================================

class Confidence(Enum):
    CONFIRMED = "CONFIRMED"   # 用户确认或有明确来源
    ASSUMED = "ASSUMED"       # 合理推测，有一定依据
    SPECULATIVE = "SPECULATIVE"  # 猜测，未经证实

class EntryType(Enum):
    RULE = "Rule"              # 规则
    CONCEPT = "Concept"        # 概念
    KNOWLEDGE = "Knowledge"    # 知识
    FACT = "Fact"             # 事实
    LAW = "Law"               # 法则
    
    @classmethod
    def from_string(cls, s: str):
        """从字符串创建枚举值"""
        for member in cls:
            if member.value.lower() == s.lower():
                return member
        raise ValueError(f"Unknown EntryType: {s}")


@dataclass
class MemoryEntry:
    """记忆条目"""
    id: str
    type: EntryType
    name: str
    statement: str
    confidence: Confidence
    conditions: List[str] = field(default_factory=list)
    action: str = ""
    source: str = ""
    lesson: str = ""
    created_at: str = field(default_factory=lambda: datetime.now().strftime("%Y-%m-%dT%H:%M"))
    tags: List[str] = field(default_factory=list)
    archived: bool = False

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "type": self.type.value,
            "name": self.name,
            "statement": self.statement,
            "confidence": self.confidence.value,
            "conditions": self.conditions,
            "action": self.action,
            "source": self.source,
            "lesson": self.lesson,
            "created_at": self.created_at,
            "tags": self.tags,
            "archived": self.archived
        }

    @classmethod
    def from_dict(cls, d: dict) -> 'MemoryEntry':
        return cls(
            id=d["id"],
            type=EntryType(d.get("type", "Knowledge")),
            name=d["name"],
            statement=d["statement"],
            confidence=Confidence(d.get("confidence", "ASSUMED")),
            conditions=d.get("conditions", []),
            action=d.get("action", ""),
            source=d.get("source", ""),
            lesson=d.get("lesson", ""),
            created_at=d.get("created_at", ""),
            tags=d.get("tags", []),
            archived=d.get("archived", False)
        )


# ============================================================
# 写入规则检查
# ============================================================

# 写入热层的4条准入标准
HOT_LAYER_CRITERIA = [
    "user_confirmed",    # 用户亲口确认的事实
    "non_obvious",       # 踩坑得出的非显而易见规律
    "universal",         # 跨领域通用原则/真理
    "sourced"            # 置信度为 CONFIRMED 或 ASSUMED
]


def check_admission(entry: MemoryEntry, reason: str = "") -> bool:
    """
    检查条目是否满足写入热层条件
    
    必须满足至少1条：
    1. 用户亲口确认
    2. 非显而易见的规律（踩坑得出）
    3. 跨领域通用原则
    4. 有来源（CONFIRMED/ASSUMED）
    
    同时满足以下任一条件的应该进入冷层：
    - 文档可查的信息
    - 一次性事件
    - 纯推测且无验证
    """
    # 满足1条即可写入热层
    if entry.confidence in (Confidence.CONFIRMED, Confidence.ASSUMED):
        return True
    
    # 或者满足以下任一条件
    if "user_confirmed" in entry.tags:
        return True
    if "non_obvious" in entry.tags:
        return True
    if "universal" in entry.tags:
        return True
    
    return False


def should_archive(entry: MemoryEntry) -> bool:
    """
    判断条目是否应该进入冷层（归档）
    
    满足任一条件应该归档：
    - 置信度为 SPECULATIVE 且创建超过7天未验证
    - 是一次性事件（无持续价值）
    - 文档可查的信息
    """
    if entry.confidence == Confidence.SPECULATIVE:
        # 检查创建时间
        try:
            created = datetime.strptime(entry.created_at, "%Y-%m-%dT%H:%M")
            age_days = (datetime.now() - created).days
            if age_days > 7:
                return True
        except:
            pass
    
    if "one_time" in entry.tags:
        return True
    if "documentation" in entry.tags:
        return True
    
    return False


# ============================================================
# 核心操作函数
# ============================================================

def generate_id(prefix: str = "mem") -> str:
    """生成唯一ID"""
    import random
    import string
    suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
    return f"{prefix}_{suffix}"


def read_hot_layer() -> List[MemoryEntry]:
    """读取热层所有条目"""
    entries = []
    if not GRAPH_FILE.exists():
        return entries
    
    with open(GRAPH_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                d = json.loads(line)
                if not d.get("archived", False):
                    entries.append(MemoryEntry.from_dict(d))
            except json.JSONDecodeError:
                continue
    return entries


def write_hot(entry: MemoryEntry, reason: str = "") -> bool:
    """
    写入热层（graph.jsonl）
    
    写入前检查准入条件
    """
    if not check_admission(entry, reason):
        # 不满足条件，写入冷层
        return write_cold(entry, reason="不符合热层准入条件")
    
    with open(GRAPH_FILE, 'a', encoding='utf-8') as f:
        f.write(json.dumps(entry.to_dict(), ensure_ascii=False) + '\n')
    
    return True


def write_cold(entry: MemoryEntry, reason: str = "") -> bool:
    """
    写入冷层（archive/archived.jsonl）
    """
    entry.archived = True
    if reason:
        entry.tags.append(f"archived_reason: {reason}")
    
    archive_file = ARCHIVE_DIR / "archived.jsonl"
    
    with open(archive_file, 'a', encoding='utf-8') as f:
        f.write(json.dumps(entry.to_dict(), ensure_ascii=False) + '\n')
    
    return True


def query_hot(query: str, entry_type: Optional[EntryType] = None, 
              confidence: Optional[Confidence] = None) -> List[MemoryEntry]:
    """
    查询热层
    
    Args:
        query: 查询关键词（匹配 name, statement, tags）
        entry_type: 可选，按类型过滤
        confidence: 可选，按置信度过滤
    """
    entries = read_hot_layer()
    results = []
    
    query_lower = query.lower()
    
    for entry in entries:
        # 类型过滤
        if entry_type and entry.type != entry_type:
            continue
        
        # 置信度过滤
        if confidence and entry.confidence != confidence:
            continue
        
        # 关键词匹配
        if (query_lower in entry.name.lower() or 
            query_lower in entry.statement.lower() or
            any(query_lower in tag.lower() for tag in entry.tags)):
            results.append(entry)
    
    return results


def query_cold(query: str) -> List[MemoryEntry]:
    """查询冷层（仅当热层无结果时使用）"""
    archive_file = ARCHIVE_DIR / "archived.jsonl"
    if not archive_file.exists():
        return []
    
    results = []
    query_lower = query.lower()
    
    with open(archive_file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                d = json.loads(line)
                entry = MemoryEntry.from_dict(d)
                if (query_lower in entry.name.lower() or 
                    query_lower in entry.statement.lower()):
                    results.append(entry)
            except:
                continue
    
    return results


def archive_old(max_age_days: int = 7, max_entries: int = 50) -> int:
    """
    淘汰旧条目
    
    规则：
    1. 超过7天的 SPECULATIVE 条目移入冷层
    2. 超过容量时，优先保留 CONFIRMED > ASSUMED > SPECULATIVE
    
    Returns:
        移入冷层的条目数量
    """
    entries = read_hot_layer()
    if len(entries) <= max_entries:
        return 0
    
    # 按优先级排序
    def sort_key(e: MemoryEntry):
        conf_order = {Confidence.CONFIRMED: 0, Confidence.ASSUMED: 1, Confidence.SPECULATIVE: 2}
        return (conf_order.get(e.confidence, 2), e.created_at)
    
    entries.sort(key=sort_key, reverse=True)
    
    # 保留前 max_entries 条
    to_archive = entries[max_entries:]
    count = 0
    
    for entry in to_archive:
        entry.archived = True
        archive_file = ARCHIVE_DIR / "archived.jsonl"
        with open(archive_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(entry.to_dict(), ensure_ascii=False) + '\n')
        count += 1
    
    # 重写热层（移除已归档的）
    with open(GRAPH_FILE, 'w', encoding='utf-8') as f:
        for entry in entries[:max_entries]:
            f.write(json.dumps(entry.to_dict(), ensure_ascii=False) + '\n')
    
    return count


def get_memory_context(query: str = "") -> str:
    """
    合并三层记忆，返回推理上下文
    
    格式：
    ## 热层（结构化知识）
    ...
    
    ## 暖层（长期记忆）
    ...
    """
    ctx = []
    
    # 热层
    if query:
        entries = query_hot(query)
    else:
        entries = read_hot_layer()
    
    if entries:
        ctx.append("## 热层（结构化知识）")
        for e in entries:
            ctx.append(f"- [{e.confidence.value}] {e.name}: {e.statement}")
    
    # 暖层
    if MEMORY_MD.exists():
        ctx.append("\n## 暖层（长期记忆）")
        ctx.append(MEMORY_MD.read_text())
    
    return "\n".join(ctx)


def cleanup_speculative(age_days: int = 7) -> int:
    """
    清理过期的 SPECULATIVE 条目
    
    规则：置信度为 SPECULATIVE 且超过指定天数未验证的条目移入冷层
    """
    entries = read_hot_layer()
    to_archive = []
    remaining = []
    
    for entry in entries:
        if entry.confidence == Confidence.SPECULATIVE:
            try:
                created = datetime.strptime(entry.created_at, "%Y-%m-%dT%H:%M")
                age = (datetime.now() - created).days
                if age > age_days:
                    to_archive.append(entry)
                    continue
            except:
                pass
        remaining.append(entry)
    
    # 写入冷层
    for entry in to_archive:
        entry.archived = True
        archive_file = ARCHIVE_DIR / "archived.jsonl"
        with open(archive_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(entry.to_dict(), ensure_ascii=False) + '\n')
    
    # 重写热层
    with open(GRAPH_FILE, 'w', encoding='utf-8') as f:
        for entry in remaining:
            f.write(json.dumps(entry.to_dict(), ensure_ascii=False) + '\n')
    
    return len(to_archive)


def stats() -> dict:
    """返回记忆统计"""
    hot = read_hot_layer()
    cold = []
    archive_file = ARCHIVE_DIR / "archived.jsonl"
    
    if archive_file.exists():
        with open(archive_file, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    cold.append(json.loads(line))
    
    warm = ""
    if MEMORY_MD.exists():
        warm = str(MEMORY_MD.stat().st_size) + " bytes"
    
    return {
        "hot_layer": len(hot),
        "cold_layer": len(cold),
        "warm_layer": warm,
        "by_confidence": {
            "CONFIRMED": sum(1 for e in hot if e.confidence == Confidence.CONFIRMED),
            "ASSUMED": sum(1 for e in hot if e.confidence == Confidence.ASSUMED),
            "SPECULATIVE": sum(1 for e in hot if e.confidence == Confidence.SPECULATIVE)
        }
    }


# ============================================================
# 命令行接口
# ============================================================

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="ontology-clawra 记忆管理器")
    subparsers = parser.add_subparsers(dest="cmd")
    
    # write 命令
    write_parser = subparsers.add_parser("write", help="写入条目")
    write_parser.add_argument("--type", required=True, choices=["Rule", "Concept", "Knowledge", "Fact"])
    write_parser.add_argument("--name", required=True)
    write_parser.add_argument("--statement", required=True)
    write_parser.add_argument("--confidence", default="ASSUMED", choices=["CONFIRMED", "ASSUMED", "SPECULATIVE"])
    write_parser.add_argument("--source", default="")
    write_parser.add_argument("--tags", default="")
    write_parser.add_argument("--lesson", default="")
    
    # query 命令
    query_parser = subparsers.add_parser("query", help="查询热层")
    query_parser.add_argument("keyword", help="查询关键词")
    query_parser.add_argument("--type", choices=["Rule", "Concept", "Knowledge", "Fact"])
    query_parser.add_argument("--confidence", choices=["CONFIRMED", "ASSUMED", "SPECULATIVE"])
    
    # query-cold 命令
    subparsers.add_parser("query-cold", help="查询冷层").add_argument("keyword")
    
    # stats 命令
    subparsers.add_parser("stats", help="查看统计")
    
    # archive-old 命令
    archive_parser = subparsers.add_parser("archive-old", help="淘汰旧条目")
    archive_parser.add_argument("--max-entries", type=int, default=50)
    
    # cleanup-speculative 命令
    subparsers.add_parser("cleanup-speculative", help="清理过期SPECULATIVE条目")
    
    # context 命令
    context_parser = subparsers.add_parser("context", help="获取推理上下文")
    context_parser.add_argument("--query", default="")
    
    args = parser.parse_args()
    
    if args.cmd == "write":
        entry = MemoryEntry(
            id=generate_id(),
            type=EntryType(args.type),
            name=args.name,
            statement=args.statement,
            confidence=Confidence(args.confidence),
            source=args.source,
            tags=args.tags.split(",") if args.tags else [],
            lesson=args.lesson
        )
        write_hot(entry)
        print(f"✅ 写入热层: {entry.name}")
    
    elif args.cmd == "query":
        entry_type = EntryType(args.type) if args.type else None
        confidence = Confidence(args.confidence) if args.confidence else None
        results = query_hot(args.keyword, entry_type, confidence)
        print(f"📊 热层查询结果 ({len(results)} 条):")
        for e in results:
            print(f"  [{e.confidence.value}] {e.name}: {e.statement[:60]}...")
    
    elif args.cmd == "query-cold":
        results = query_cold(args.keyword)
        print(f"📊 冷层查询结果 ({len(results)} 条):")
        for e in results:
            print(f"  [{e.confidence.value}] {e.name}: {e.statement[:60]}...")
    
    elif args.cmd == "stats":
        s = stats()
        print("📊 记忆统计:")
        print(f"  热层: {s['hot_layer']} 条")
        print(f"  冷层: {s['cold_layer']} 条")
        print(f"  暖层: {s['warm_layer']}")
        print(f"  置信度分布: {s['by_confidence']}")
    
    elif args.cmd == "archive-old":
        count = archive_old(max_entries=args.max_entries)
        print(f"📦 已归档 {count} 条")
    
    elif args.cmd == "cleanup-speculative":
        count = cleanup_speculative()
        print(f"🧹 清理了 {count} 条过期SPECULATIVE条目")
    
    elif args.cmd == "context":
        print(get_memory_context(args.query))
    
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
