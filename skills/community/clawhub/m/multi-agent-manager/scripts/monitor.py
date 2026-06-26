#!/usr/bin/env python3
"""
Agent Orchestrator - Monitor Agent Status
实时监控智能体状态
"""

import json
import subprocess
import sys
import time
from datetime import datetime

def get_agent_status():
    """获取智能体状态"""
    try:
        result = subprocess.run(
            ['openclaw', 'status', '--json'],
            capture_output=True,
            text=True,
            check=True
        )
        return json.loads(result.stdout)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return None

def format_status(status):
    """格式化状态输出"""
    print(f"\n{'='*60}")
    print(f"Agent Status - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*60}\n")
    
    # 版本信息
    version = status.get('runtimeVersion', 'unknown')
    print(f"OpenClaw: {version}")
    
    # Heartbeat 配置
    heartbeat = status.get('heartbeat', {})
    agents_hb = heartbeat.get('agents', [])
    print(f"\nAgents: {len(agents_hb)} configured\n")
    
    for agent in agents_hb:
        agent_id = agent.get('agentId', 'unknown')
        enabled = agent.get('enabled', False)
        every = agent.get('every', 'N/A')
        status_icon = '✓' if enabled else '✗'
        print(f"  {status_icon} {agent_id}")
        print(f"     Heartbeat: {every}")
    
    # 会话统计
    sessions = status.get('sessions', {})
    session_count = sessions.get('count', 0)
    print(f"\nActive Sessions: {session_count}")
    
    # 最近会话
    recent = sessions.get('recent', [])
    if recent:
        print(f"\nRecent Activity:")
        for sess in recent[:3]:  # 只显示前3个
            agent_id = sess.get('agentId', 'unknown')
            age_ms = sess.get('age', 0)
            age_str = f"{age_ms // 1000}s ago" if age_ms < 60000 else f"{age_ms // 60000}m ago"
            print(f"  • {agent_id} - {age_str}")
    
    print()

def monitor_loop(interval=5):
    """持续监控"""
    try:
        while True:
            status = get_agent_status()
            if status:
                format_status(status)
            time.sleep(interval)
    except KeyboardInterrupt:
        print("\nMonitoring stopped")

def main():
    watch = '--watch' in sys.argv
    
    if watch:
        interval = 5
        if '--interval' in sys.argv:
            idx = sys.argv.index('--interval')
            if idx + 1 < len(sys.argv):
                interval = int(sys.argv[idx + 1])
        monitor_loop(interval)
    else:
        status = get_agent_status()
        if status:
            format_status(status)

if __name__ == '__main__':
    main()
