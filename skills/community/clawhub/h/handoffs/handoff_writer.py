#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Handoff Writer - 結構化寫入交接日誌

用法：
    python handoff_writer.py --task-id "task_xyz" --sender "engineer" 
                            --receiver "professor" --status "completed" 
                            --chain-id "hermes_v2"
                            --summary "完成了XXX" --artifacts "file1.md,file2.md"
"""

import os
import sys
import json
import uuid
from datetime import datetime
from pathlib import Path

# 設定
HANDOFF_DIR = Path(os.path.expanduser("~/.sumo/handoffs"))
CHAIN_REGISTRY = HANDOFF_DIR / "chain_registry.json"

def get_timestamp():
    return datetime.now().strftime("%Y-%m-%dT%H:%M:%S.000Z")

def init_chain(chain_id):
    """初始化任務鏈"""
    HANDOFF_DIR.mkdir(parents=True, exist_ok=True)
    if not CHAIN_REGISTRY.exists():
        with open(CHAIN_REGISTRY, 'w', encoding='utf-8') as f:
            json.dump({"chains": {}}, f)
    
    with open(CHAIN_REGISTRY, 'r', encoding='utf-8') as f:
        registry = json.load(f)
    
    if chain_id not in registry["chains"]:
        registry["chains"][chain_id] = {
            "chain_id": chain_id,
            "created_at": get_timestamp(),
            "sequence": 0,
            "tasks": []
        }
    
    return registry

def write_handoff(task_id, sender, receiver, chain_id, status, summary, 
                 artifacts=None, next_requirements=None, working_dir=None,
                 last_modified_files=None, confidence=0.85):
    """寫入結構化交接日誌"""
    HANDOFF_DIR.mkdir(parents=True, exist_ok=True)
    
    # 取得 sequence
    registry = init_chain(chain_id)
    sequence = registry["chains"][chain_id]["sequence"] + 1
    
    # 更新 registry
    registry["chains"][chain_id]["sequence"] = sequence
    with open(CHAIN_REGISTRY, 'w', encoding='utf-8') as f:
        json.dump(registry, f, indent=2)
    
    # 建立 handoff 資料
    handoff = {
        "version": "1.0",
        "type": "handoff",
        "handoff_id": f"h_{datetime.now().strftime('%Y%m%dT%H%M%S')}_{str(uuid.uuid4())[:8]}",
        "timestamp": get_timestamp(),
        "chain_id": chain_id,
        "sequence": sequence,
        "sender": {
            "agent_id": sender,
            "agent_name": f"{sender}蘇茉"
        },
        "receiver": {
            "agent_id": receiver,
            "agent_name": f"{receiver}蘇茉"
        },
        "task": {
            "task_id": task_id,
            "label": task_id,
            "description": summary
        },
        "status": status,
        "outputs": {
            "summary": summary,
            "artifacts": artifacts or [],
            "next_requirements": next_requirements or []
        },
        "context_snapshot": {
            "working_dir": working_dir or "",
            "last_modified_files": last_modified_files or []
        },
        "dependencies": {
            "required": [],
            "satisfied": []
        },
        "quality": {
            "self_check": "passed" if status == "completed" else "pending",
            "confidence": confidence
        }
    }
    
    # 寫入當日檔案
    date_str = datetime.now().strftime("%Y-%m-%d")
    daily_file = HANDOFF_DIR / f"{date_str}.jsonl"
    
    with open(daily_file, 'a', encoding='utf-8') as f:
        f.write(json.dumps(handoff, ensure_ascii=False) + '\n')
    
    print(f"[OK] Handoff 寫入成功: {handoff['handoff_id']}")
    print(f"      Chain: {chain_id}, Sequence: {sequence}")
    print(f"      Sender: {sender} -> Receiver: {receiver}")
    
    return handoff

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Handoff Writer")
    parser.add_argument("--task-id", required=True, help="任務 ID")
    parser.add_argument("--sender", required=True, help="發送者 agent")
    parser.add_argument("--receiver", required=True, help="接收者 agent")
    parser.add_argument("--chain-id", required=True, help="任務鏈 ID")
    parser.add_argument("--status", required=True, choices=["completed", "running", "failed"], help="狀態")
    parser.add_argument("--summary", required=True, help="任務摘要")
    parser.add_argument("--artifacts", help="產出檔案（逗號分隔）")
    parser.add_argument("--next", help="下一棒需求（逗號分隔）")
    parser.add_argument("--working-dir", help="工作目錄")
    parser.add_argument("--files", help="修改的檔案（逗號分隔）")
    parser.add_argument("--confidence", type=float, default=0.85, help="信心度（預設 0.85）")
    
    args = parser.parse_args()
    
    write_handoff(
        task_id=args.task_id,
        sender=args.sender,
        receiver=args.receiver,
        chain_id=args.chain_id,
        status=args.status,
        summary=args.summary,
        artifacts=args.artifacts.split(",") if args.artifacts else None,
        next_requirements=args.next.split(",") if args.next else None,
        working_dir=args.working_dir,
        last_modified_files=args.files.split(",") if args.files else None,
        confidence=args.confidence
    )

if __name__ == "__main__":
    main()