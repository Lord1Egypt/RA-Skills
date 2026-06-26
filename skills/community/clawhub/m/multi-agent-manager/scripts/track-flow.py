#!/usr/bin/env python3
"""
Agent Orchestrator - Track Task Flow
追踪任务在智能体间的流转
"""

import json
import subprocess
import sys
from datetime import datetime

def get_session_history(session_key):
    """获取会话历史"""
    try:
        result = subprocess.run(
            ['openclaw', 'sessions', 'history', session_key, '--json'],
            capture_output=True,
            text=True,
            check=True
        )
        return json.loads(result.stdout)
    except Exception as e:
        return None

def track_task(task_id):
    """追踪任务流转"""
    print(f"\n=== Task Flow: {task_id} ===\n")
    
    # 搜索包含 task_id 的会话
    try:
        result = subprocess.run(
            ['openclaw', 'sessions', 'list', '--json'],
            capture_output=True,
            text=True,
            check=True
        )
        sessions = json.loads(result.stdout)
        
        found = False
        for session in sessions:
            session_key = session.get('key', '')
            if task_id in session_key or task_id in str(session):
                found = True
                print(f"📍 Session: {session_key}")
                print(f"   Agent: {session.get('agentId', 'unknown')}")
                print(f"   Status: {session.get('status', 'unknown')}")
                print()
        
        if not found:
            print(f"No sessions found for task: {task_id}")
    
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)

def main():
    if '--task-id' not in sys.argv:
        print("Usage: track-flow.py --task-id <id>")
        sys.exit(1)
    
    idx = sys.argv.index('--task-id')
    task_id = sys.argv[idx + 1]
    
    track_task(task_id)

if __name__ == '__main__':
    main()
