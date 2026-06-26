#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Handoff Reader - 讀取並解析交接日誌

用法：
    python handoff_reader.py --date 2026-04-07
    python handoff_reader.py --chain hermes_v2
    python handoff_reader.py --latest
"""

import os
import json
from datetime import datetime, timedelta
from pathlib import Path

# 設定
HANDOFF_DIR = Path(os.path.expanduser("~/.sumo/handoffs"))
CHAIN_REGISTRY = HANDOFF_DIR / "chain_registry.json"

def get_timestamp():
    return datetime.now().strftime("%Y-%m-%dT%H:%M:%S.000Z")

def read_daily_handoffs(date_str=None):
    """讀取指定日期的所有 handoff"""
    if not date_str:
        date_str = datetime.now().strftime("%Y-%m-%d")
    
    daily_file = HANDOFF_DIR / f"{date_str}.jsonl"
    if not daily_file.exists():
        print(f"[WARN] 找不到 {daily_file}")
        return []
    
    handoffs = []
    with open(daily_file, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                handoffs.append(json.loads(line))
    
    return handoffs

def read_chain(chain_id):
    """讀取指定 chain 的所有 handoff"""
    if not CHAIN_REGISTRY.exists():
        return []
    
    with open(CHAIN_REGISTRY, 'r', encoding='utf-8') as f:
        registry = json.load(f)
    
    if chain_id not in registry["chains"]:
        print(f"[WARN] Chain {chain_id} 不存在")
        return []
    
    chain = registry["chains"][chain_id]
    sequence = chain["sequence"]
    
    # 讀取所有相關的 handoff
    handoffs = []
    for i in range(1, sequence + 1):
        for h in read_all_handoffs():
            if h.get("chain_id") == chain_id and h.get("sequence") == i:
                handoffs.append(h)
    
    return handoffs

def read_all_handoffs():
    """讀取所有 handoff"""
    if not HANDOFF_DIR.exists():
        return []
    
    all_handoffs = []
    for f in HANDOFF_DIR.glob("*.jsonl"):
        with open(f, 'r', encoding='utf-8') as file:
            for line in file:
                if line.strip():
                    all_handoffs.append(json.loads(line))
    
    return all_handoffs

def get_latest(count=5):
    """取得最近 N 筆 handoff"""
    all_h = read_all_handoffs()
    all_h.sort(key=lambda x: x.get("timestamp", ""), reverse=True)
    return all_h[:count]

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Handoff Reader")
    parser.add_argument("--date", help="指定日期 (YYYY-MM-DD)")
    parser.add_argument("--chain", help="Chain ID")
    parser.add_argument("--latest", action="store_true", help="最近 5 筆")
    
    args = parser.parse_args()
    
    if args.latest:
        handoffs = get_latest()
        print(f"=== 最近 {len(handoffs)} 筆 Handoff ===")
        for h in handoffs:
            print(f"\n[{h['timestamp']}] {h['handoff_id']}")
            print(f"  Chain: {h['chain_id']}, Seq: {h['sequence']}")
            print(f"  {h['sender']['agent_name']} -> {h['receiver']['agent_name']}")
            print(f"  Task: {h['task']['label']}")
            print(f"  Status: {h['status']}")
            print(f"  Output: {h['outputs']['summary'][:50]}...")
    
    elif args.chain:
        handoffs = read_chain(args.chain)
        print(f"=== Chain: {args.chain} ({len(handoffs)} handoffs) ===")
        for h in handoffs:
            print(f"\n[Seq {h['sequence']}] {h['handoff_id']}")
            print(f"  {h['sender']['agent_name']} -> {h['receiver']['agent_name']}")
            print(f"  Status: {h['status']}")
    
    elif args.date:
        handoffs = read_daily_handoffs(args.date)
        print(f"=== {args.date} ({len(handoffs)} handoffs) ===")
        for h in handoffs:
            print(f"\n[{h['timestamp']}] {h['handoff_id']}")
            print(f"  {h['sender']['agent_name']} -> {h['receiver']['agent_name']}")
            print(f"  Task: {h['task']['label']}, Status: {h['status']}")
    
    else:
        # 顯示今日
        handoffs = read_daily_handoffs()
        print(f"=== 今日 ({len(handoffs)} handoffs) ===")
        for h in handoffs:
            print(f"  [{h['sequence']}] {h['sender']['agent_name']} -> {h['receiver']['agent_name']} | {h['task']['label']}")

if __name__ == "__main__":
    main()