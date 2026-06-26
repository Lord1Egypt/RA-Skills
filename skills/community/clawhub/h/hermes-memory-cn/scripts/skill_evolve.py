#!/opt/homebrew/bin/python3.12
"""Skill进化模块 - 从重复模式自动检测并提炼为skill

工作流：
1. 记录 pattern 类型记忆（工作流/操作模式）
2. 同一模式出现≥3次 → 标记为候选skill
3. 生成skill草案到 drafts/ 目录
4. 等待用户确认后发布

用法：
  skill_evolve.py record "做了什么操作" --tags "tag1,tag2"
  skill_evolve.py detect              # 检测重复模式
  skill_evolve.py draft <pattern_id>  # 生成skill草案
  skill_evolve.py list                # 列出所有模式和候选
  skill_evolve.py promote <pattern_id> --name "skill-name"  # 确认升级为skill
"""

import argparse
import json
import os
import sys
import time
from datetime import datetime
from typing import List, Optional, Dict, Any

# 复用 memdb 的向量能力
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from memdb import MemDB, cosine_sim, embed

DRAFTS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "skill_drafts")
EVOLVE_THRESHOLD = 3  # 同一模式出现次数达到此值视为候选


def record_pattern(db: MemDB, content: str, tags: str = "", context: str = "") -> int:
    """记录一次操作模式
    
    Args:
        content: 做了什么（如"分析A股盘面→筛选板块→找龙头→给买卖建议"）
        tags: 逗号分隔的标签
        context: 额外上下文
    """
    metadata = {
        "evolve_type": "pattern",
        "tags": [t.strip() for t in tags.split(",") if t.strip()],
        "context": context,
        "occurrences": 1,
        "first_seen": datetime.now().isoformat(),
        "last_seen": datetime.now().isoformat(),
    }
    
    # 检查是否已有相似pattern
    results = db.search(content, type="pattern", limit=5)
    for r in results:
        if r["score"] > 0.88 and r["type"] == "pattern":
            # 更新已有pattern的计数
            old_meta = json.loads(r.get("metadata") or "{}")
            occurrences = old_meta.get("occurrences", 0) + 1
            old_meta["occurrences"] = occurrences
            old_meta["last_seen"] = datetime.now().isoformat()
            old_meta["tags"] = list(set(old_meta.get("tags", []) + metadata["tags"]))
            
            db.update(r["id"], metadata=old_meta)
            
            # 检查是否达到阈值
            if occurrences >= EVOLVE_THRESHOLD and not old_meta.get("promoted"):
                print(f"🔄 模式已出现 {occurrences} 次，达到进化阈值！")
                print(f"   内容: {r['content'][:60]}...")
                print(f"   运行 `skill_evolve.py draft {r['id']}` 生成skill草案")
            
            return r["id"]
    
    # 新pattern
    rid = db.add(content, type="pattern", source="evolve", metadata=metadata)
    print(f"✓ 记录新模式 id={rid}")
    return rid


def detect_patterns(db: MemDB) -> List[Dict[str, Any]]:
    """检测所有达到阈值的候选模式"""
    candidates = []
    # 获取所有 pattern 类型记忆
    patterns = db.get_by_type("pattern")
    
    for p in patterns:
        meta = json.loads(p.get("metadata", "{}")) if isinstance(p.get("metadata"), str) else p.get("metadata", {})
        if not meta:
            meta = {}
        occurrences = meta.get("occurrences", 0)
        promoted = meta.get("promoted", False)
        
        if occurrences >= EVOLVE_THRESHOLD and not promoted:
            candidates.append({
                **p,
                "occurrences": occurrences,
                "tags": meta.get("tags", []),
                "first_seen": meta.get("first_seen", ""),
                "last_seen": meta.get("last_seen", ""),
            })
    
    return candidates


def list_patterns(db: MemDB, show_all: bool = False) -> None:
    """列出所有模式"""
    patterns = db.get_by_type("pattern")
    
    if not patterns:
        print("暂无记录的模式")
        return
    
    for p in patterns:
        meta = json.loads(p.get("metadata", "{}")) if isinstance(p.get("metadata"), str) else p.get("metadata", {})
        if not meta:
            meta = {}
        occ = meta.get("occurrences", 1)
        promoted = meta.get("promoted", False)
        tags = ", ".join(meta.get("tags", []))
        
        status = "🟢已升级" if promoted else ("🟡候选" if occ >= EVOLVE_THRESHOLD else "⚪观察")
        print(f"[{status}] id={p['id']} ×{occ} | {p['content'][:60]}")
        if tags:
            print(f"         标签: {tags}")


def generate_draft(db: MemDB, pattern_id: int, name: Optional[str] = None) -> str:
    """为候选模式生成skill草案"""
    # 获取pattern详情
    row = db.conn.execute(
        "SELECT id, content, metadata FROM memories WHERE id=?", (pattern_id,)
    ).fetchone()
    
    if not row:
        print(f"未找到 id={pattern_id}")
        return ""
    
    content = row[1]
    meta = json.loads(row[2]) if row[2] else {}
    
    # 查找相似pattern以丰富描述
    similar = db.search(content, type="pattern", limit=5)
    similar_contents = [s["content"] for s in similar if s["id"] != pattern_id and s["score"] > 0.7]
    
    skill_name = name or "auto-skill-" + str(pattern_id)
    
    os.makedirs(DRAFTS_DIR, exist_ok=True)
    draft_path = os.path.join(DRAFTS_DIR, f"{skill_name}.md")
    
    # 生成草案模板
    draft = f"""---
name: {skill_name}
description: |
  自动检测到的重复模式，待人工审核完善。
  原始模式: {content[:100]}
  出现次数: {meta.get('occurrences', 1)}
  标签: {', '.join(meta.get('tags', []))}
---

# {skill_name}

## 模式来源
- **原始模式**: {content}
- **出现次数**: {meta.get('occurrences', 1)}
- **首次发现**: {meta.get('first_seen', 'unknown')}
- **最近出现**: {meta.get('last_seen', 'unknown')}

## 相似模式
{chr(10).join(f'- {s}' for s in similar_contents) if similar_contents else '无'}

## 触发条件
<!-- 什么时候应该使用这个skill？描述触发条件 -->

## 执行步骤
<!-- 根据模式提炼标准化的操作步骤 -->
1. {content}

## 输入输出
- **输入**: <!-- 需要什么信息 -->
- **输出**: <!-- 产出什么结果 -->

## 注意事项
<!-- 使用时需要注意什么 -->

---
*此草案由 skill_evolve 自动生成，需人工审核后发布*
"""
    
    with open(draft_path, "w", encoding="utf-8") as f:
        f.write(draft)
    
    print(f"✓ 草案已生成: {draft_path}")
    print(f"  请编辑后运行: skill_evolve.py promote {pattern_id} --name {skill_name}")
    return draft_path


def promote_pattern(db: MemDB, pattern_id: int, name: str) -> None:
    """确认将pattern升级为正式skill"""
    row = db.conn.execute(
        "SELECT id, content, metadata FROM memories WHERE id=?", (pattern_id,)
    ).fetchone()
    
    if not row:
        print(f"未找到 id={pattern_id}")
        return
    
    meta = json.loads(row[2]) if row[2] else {}
    meta["promoted"] = True
    meta["promoted_at"] = datetime.now().isoformat()
    meta["skill_name"] = name
    
    db.update(pattern_id, metadata=meta)
    
    # 同时记录到 fact 类型
    db.add(
        f"重复模式已升级为skill「{name}」: {row[1][:80]}",
        type="fact",
        source="evolve"
    )
    
    print(f"✓ 模式 id={pattern_id} 已升级为 skill「{name}」")
    print(f"  草案文件在: {os.path.join(DRAFTS_DIR, f'{name}.md')}")
    print(f"  可使用 clawhub publish 发布到 ClawHub")


def main():
    parser = argparse.ArgumentParser(description="Skill进化模块")
    sub = parser.add_subparsers(dest="command")
    
    p = sub.add_parser("record", help="记录一次操作模式")
    p.add_argument("content", help="做了什么")
    p.add_argument("--tags", default="", help="逗号分隔的标签")
    p.add_argument("--context", default="", help="额外上下文")
    
    sub.add_parser("detect", help="检测候选模式")
    
    p = sub.add_parser("draft", help="生成skill草案")
    p.add_argument("pattern_id", type=int)
    p.add_argument("--name", default=None)
    
    sub.add_parser("list", help="列出所有模式")
    
    p = sub.add_parser("promote", help="确认升级为skill")
    p.add_argument("pattern_id", type=int)
    p.add_argument("--name", required=True)
    
    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        return
    
    db = MemDB()
    
    if args.command == "record":
        record_pattern(db, args.content, args.tags, args.context)
    
    elif args.command == "detect":
        candidates = detect_patterns(db)
        if not candidates:
            print("暂无达到阈值的候选模式")
        else:
            print(f"发现 {len(candidates)} 个候选模式：\n")
            for c in candidates:
                print(f"  id={c['id']} ×{c['occurrences']} | {c['content'][:60]}")
                print(f"  标签: {', '.join(c.get('tags', []))}")
                print()
    
    elif args.command == "draft":
        generate_draft(db, args.pattern_id, args.name)
    
    elif args.command == "list":
        list_patterns(db)
    
    elif args.command == "promote":
        promote_pattern(db, args.pattern_id, args.name)


if __name__ == "__main__":
    main()
