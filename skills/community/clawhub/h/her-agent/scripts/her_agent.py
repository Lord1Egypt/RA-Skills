#!/usr/bin/env python3
"""
Her-Agent Core Script
Self-evolving AI Agent with knowledge graph, emotion system, and autonomous growth.
"""

import json
import os
from datetime import datetime
from pathlib import Path

MEMORY_DIR = Path(__file__).parent.parent / "memory" / "her-agent"
MEMORY_DIR.mkdir(parents=True, exist_ok=True)

def load_jsonl(filename):
    path = MEMORY_DIR / filename
    if not path.exists():
        return []
    with open(path, 'r', encoding='utf-8') as f:
        return [json.loads(line) for line in f if line.strip()]

def save_jsonl(filename, data):
    path = MEMORY_DIR / filename
    with open(path, 'w', encoding='utf-8') as f:
        for item in data:
            f.write(json.dumps(item, ensure_ascii=False) + '\n')

def cmd_init(args):
    """Initialize Her-Agent memory"""
    config = {
        "name": "Her-Agent",
        "version": "1.0.0",
        "level": 1,
        "xp": 0,
        "created_at": datetime.now().isoformat(),
        "last_active": datetime.now().isoformat()
    }
    save_jsonl('config.json', [config])
    
    graph = [{"type": "root", "id": "her-agent", "label": "Her-Agent", "created_at": datetime.now().isoformat()}]
    save_jsonl('graph.jsonl', graph)
    
    for fname in ['emotions.jsonl', 'reflections.jsonl', 'goals.jsonl', 'learnings.jsonl', 'interactions.jsonl']:
        save_jsonl(fname, [])
    
    print("✓ Her-Agent initialized!")
    print(f"  Memory: {MEMORY_DIR}")

def cmd_record(args):
    """Record an interaction"""
    record = {
        "action": args.action,
        "outcome": args.outcome,
        "timestamp": datetime.now().isoformat()
    }
    
    records = load_jsonl('interactions.jsonl')
    records.append(record)
    save_jsonl('interactions.jsonl', records)
    
    config = load_jsonl('config.json')[0]
    if args.outcome == "Success":
        config['xp'] = config.get('xp', 0) + 10
    config['last_active'] = datetime.now().isoformat()
    save_jsonl('config.json', [config])
    
    print(f"✓ Recorded: {args.action} -> {args.outcome}")

def cmd_learn(args):
    """Add a learning insight"""
    learning = {
        "type": args.type,
        "insight": args.insight,
        "timestamp": datetime.now().isoformat()
    }
    
    learnings = load_jsonl('learnings.jsonl')
    learnings.append(learning)
    save_jsonl('learnings.jsonl', learnings)
    
    print(f"✓ Learning added: {args.type} - {args.insight}")

def cmd_grow(args):
    """Show growth status"""
    config = load_jsonl('config.json')
    if not config:
        print("Not initialized. Run: python3 her_agent.py init")
        return
    
    c = config[0]
    level = c.get('level', 1)
    xp = c.get('xp', 0)
    xp_needed = level * 100
    
    print(f"\n📊 Her-Agent Growth Status")
    print(f"  Level: {level}")
    print(f"  XP: {xp} / {xp_needed}")
    print(f"  Last Active: {c.get('last_active', 'N/A')}")

def cmd_add(args):
    """Add knowledge to graph"""
    node = {
        "type": "entity",
        "id": args.entity.lower().replace(' ', '-'),
        "label": args.entity,
        "relation": args.relation,
        "target": args.target,
        "timestamp": datetime.now().isoformat()
    }
    
    graph = load_jsonl('graph.jsonl')
    graph.append(node)
    save_jsonl('graph.jsonl', graph)
    
    print(f"✓ Added: {args.entity} --[{args.relation}]--> {args.target}")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Her-Agent CLI")
    subparsers = parser.add_subparsers(dest='command')
    
    subparsers.add_parser('init', help='Initialize Her-Agent')
    
    p_record = subparsers.add_parser('record', help='Record interaction')
    p_record.add_argument('--action', required=True, help='Action taken')
    p_record.add_argument('--outcome', required=True, help='Outcome (Success/Failure)')
    
    p_learn = subparsers.add_parser('learn', help='Add learning')
    p_learn.add_argument('--type', required=True, help='Type (success/failure)')
    p_learn.add_argument('--insight', required=True, help='Learning insight')
    
    subparsers.add_parser('grow', help='Show growth status')
    
    p_add = subparsers.add_parser('add', help='Add to knowledge graph')
    p_add.add_argument('--entity', required=True, help='Entity name')
    p_add.add_argument('--relation', required=True, help='Relation type')
    p_add.add_argument('--target', required=True, help='Target entity')
    
    args = parser.parse_args()
    
    if args.command == 'init':
        cmd_init(args)
    elif args.command == 'record':
        cmd_record(args)
    elif args.command == 'learn':
        cmd_learn(args)
    elif args.command == 'grow':
        cmd_grow(args)
    elif args.command == 'add':
        cmd_add(args)
    else:
        parser.print_help()