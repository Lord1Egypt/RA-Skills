#!/usr/bin/env python3
"""
知识图谱 - 医学知识图谱管理脚本
支持：实体创建、关系管理、事实添加、查询、摘要生成
"""

import os
import json
import sys
from datetime import datetime
from pathlib import Path

# 配置
BASE_DIR = Path("memory/mindmap")
GRAPH_FILE = BASE_DIR / "graph.jsonl"
KNOWLEDGE_DIR = BASE_DIR / "knowledge"
SUMMARY_DIR = BASE_DIR / "summary"

# 初始化目录
def init():
    BASE_DIR.mkdir(parents=True, exist_ok=True)
    KNOWLEDGE_DIR.mkdir(parents=True, exist_ok=True)
    # 创建子目录
    for subdir in ["disease", "examination", "symptom", "medication", "anatomy", "syndrome", "waveform"]:
        (KNOWLEDGE_DIR / subdir).mkdir(exist_ok=True)
    if not GRAPH_FILE.exists():
        GRAPH_FILE.write_text("")

# ID生成
def generate_id(entity_type, name):
    slug = "".join(c for c in name if c.isalnum())[:20].lower()
    return f"{entity_type[:3].lower()}_{slug}"

# 创建实体
def create_entity(entity_type, name, **props):
    entity_id = generate_id(entity_type, name)
    entity = {
        "op": "create",
        "entity": {
            "id": entity_id,
            "type": entity_type,
            "properties": {"name": name, **props},
            "created": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "updated": datetime.now().strftime("%Y-%m-%d %H:%M")
        }
    }
    with open(GRAPH_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(entity, ensure_ascii=False) + "\n")
    
    # 创建知识目录
    slug = "".join(c for c in name if c.isalnum())[:20].lower()
    entity_dir = KNOWLEDGE_DIR / entity_type.lower() / slug
    entity_dir.mkdir(parents=True, exist_ok=True)
    items_file = entity_dir / "items.json"
    if not items_file.exists():
        items_file.write_text(json.dumps([], ensure_ascii=False, indent=2))
    
    print(f"✓ 已创建 {entity_type}: {name} (ID: {entity_id})")
    return entity_id

# 创建关系
def relate(from_entity, relation, to_entity):
    relation_id = f"rel_{int(datetime.now().timestamp())}"
    rel = {
        "op": "relate",
        "relation": {
            "id": relation_id,
            "from": from_entity,
            "rel_type": relation,
            "to": to_entity,
            "created": datetime.now().strftime("%Y-%m-%d %H:%M")
        }
    }
    with open(GRAPH_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(rel, ensure_ascii=False) + "\n")
    print(f"✓ 已创建关系: {from_entity} --[{relation}]--> {to_entity}")

# 添加事实
def add_fact(entity_name, fact_text, source="用户输入", category="知识"):
    slug = "".join(c for c in entity_name if c.isalnum())[:20].lower()
    # 查找实体类型
    entity_type = None
    for et in ["disease", "examination", "symptom", "medication", "anatomy", "syndrome", "waveform"]:
        entity_dir = KNOWLEDGE_DIR / et / slug
        if entity_dir.exists():
            entity_type = et
            break
    
    if not entity_type:
        print(f"✗ 实体不存在: {entity_name}")
        return
    
    items_file = KNOWLEDGE_DIR / entity_type / slug / "items.json"
    items = json.loads(items_file.read_text(encoding="utf-8"))
    
    fact_id = f"{slug}-{len(items)+1:03d}"
    new_item = {
        "id": fact_id,
        "fact": fact_text,
        "source": source,
        "category": category,
        "created": datetime.now().strftime("%Y-%m-%d"),
        "superseded": False
    }
    items.append(new_item)
    items_file.write_text(json.dumps(items, ensure_ascii=False, indent=2))
    print(f"✓ 已添加事实到 {entity_name}: {fact_text[:30]}...")

# 查询实体
def get_entity(entity_name):
    slug = "".join(c for c in entity_name if c.isalnum())[:20].lower()
    print(f"\n=== {entity_name} ===")
    
    # 查关系
    with open(GRAPH_FILE, encoding="utf-8") as f:
        for line in f:
            data = json.loads(line)
            if "entity" in data:
                e = data["entity"]
                if e.get("properties", {}).get("name") == entity_name:
                    print(f"类型: {e['type']}")
                    print(f"创建时间: {e.get('created')}")
                    print(f"属性: {e.get('properties')}")
            elif "relation" in data:
                r = data["relation"]
                if r.get("from") == slug or r.get("to") == slug:
                    print(f"关系: {r['from']} --[{r['rel_type']}]--> {r['to']}")

# 查询事实
def get_facts(entity_name):
    slug = "".join(c for c in entity_name if c.isalnum())[:20].lower()
    for et in ["disease", "examination", "symptom", "medication", "anatomy", "syndrome", "waveform"]:
        items_file = KNOWLEDGE_DIR / et / slug / "items.json"
        if items_file.exists():
            items = json.loads(items_file.read_text(encoding="utf-8"))
            print(f"\n=== {entity_name} 知识点 ===")
            for item in items:
                if not item.get("superseded", False):
                    print(f"- {item['fact']}")
                    print(f"  来源: {item.get('source', '未知')}")

# 列出实体
def list_entities(entity_type):
    print(f"\n=== {entity_type} 列表 ===")
    entity_dir = KNOWLEDGE_DIR / entity_type.lower()
    if entity_dir.exists():
        for d in entity_dir.iterdir():
            if d.is_dir():
                print(f"- {d.name}")

# 生成摘要
def summarize(entity_name):
    slug = "".join(c for c in entity_name if c.isalnum())[:20].lower()
    
    # 收集信息
    info = {"名称": entity_name, "关系": [], "知识点": []}
    
    # 查关系
    with open(GRAPH_FILE, encoding="utf-8") as f:
        for line in f:
            data = json.loads(line)
            if "relation" in data:
                r = data["relation"]
                if slug in [r.get("from"), r.get("to")]:
                    info["关系"].append(f"{r['from']} --[{r['rel_type']}]--> {r['to']}")
    
    # 查事实
    for et in ["disease", "examination", "symptom", "medication", "anatomy", "syndrome", "waveform"]:
        items_file = KNOWLEDGE_DIR / et / slug / "items.json"
        if items_file.exists():
            items = json.loads(items_file.read_text(encoding="utf-8"))
            for item in items:
                if not item.get("superseded", False):
                    info["知识点"].append(item["fact"])
    
    # 输出摘要
    print(f"\n## {entity_name} 知识摘要\n")
    for k, v in info.items():
        if v:
            print(f"### {k}")
            for item in v:
                print(f"- {item}")
            print()

# 主函数
def main():
    init()
    
    if len(sys.argv) < 2:
        print("知识图谱 管理脚本")
        print("用法:")
        print("  python3 mindmap.py create <类型> --name <名称> [--prop <值>]")
        print("  python3 mindmap.py relate <实体1> --rel <关系> --to <实体2>")
        print("  python3 mindmap.py fact add --entity <实体> --fact <事实>")
        print("  python3 mindmap.py get <实体>")
        print("  python3 mindmap.py facts <实体>")
        print("  python3 mindmap.py list <类型>")
        print("  python3 mindmap.py summarize <实体>")
        return
    
    cmd = sys.argv[1]
    
    if cmd == "create":
        # parse args
        args = sys.argv[2:]
        entity_type = None
        name = None
        props = {}
        i = 0
        while i < len(args):
            if args[i] == "--name" and i+1 < len(args):
                name = args[i+1]
                i += 2
            elif args[i] == "--category" and i+1 < len(args):
                props["category"] = args[i+1]
                i += 2
            elif args[i] == "--purpose" and i+1 < len(args):
                props["purpose"] = args[i+1]
                i += 2
            elif args[i] == "--description" and i+1 < len(args):
                props["description"] = args[i+1]
                i += 2
            elif args[i] in ["Disease", "Examination", "Symptom", "Medication", "Anatomy", "Syndrome"]:
                entity_type = args[i]
                i += 1
            else:
                i += 1
        if entity_type and name:
            create_entity(entity_type, name, **props)
    
    elif cmd == "relate":
        from_e = None
        to_e = None
        rel_type = "related_to"
        args = sys.argv[2:]
        i = 0
        while i < len(args):
            if args[i] == "--from" and i+1 < len(args):
                from_e = args[i+1]
                i += 2
            elif args[i] == "--to" and i+1 < len(args):
                to_e = args[i+1]
                i += 2
            elif args[i] == "--rel" and i+1 < len(args):
                rel_type = args[i+1]
                i += 2
            else:
                i += 1
        if from_e and to_e:
            relate(from_e, rel_type, to_e)
    
    elif cmd == "fact":
        if len(sys.argv) > 2 and sys.argv[2] == "add":
            entity = None
            fact = None
            source = "用户输入"
            args = sys.argv[3:]
            i = 0
            while i < len(args):
                if args[i] == "--entity" and i+1 < len(args):
                    entity = args[i+1]
                    i += 2
                elif args[i] == "--fact" and i+1 < len(args):
                    fact = args[i+1]
                    i += 2
                elif args[i] == "--source" and i+1 < len(args):
                    source = args[i+1]
                    i += 2
                else:
                    i += 1
            if entity and fact:
                add_fact(entity, fact, source)
    
    elif cmd == "get":
        if len(sys.argv) > 2:
            get_entity(sys.argv[2])
    
    elif cmd == "facts":
        if len(sys.argv) > 2:
            get_facts(sys.argv[2])
    
    elif cmd == "list":
        if len(sys.argv) > 2:
            list_entities(sys.argv[2])
    
    elif cmd == "summarize":
        if len(sys.argv) > 2:
            summarize(sys.argv[2])

if __name__ == "__main__":
    main()
