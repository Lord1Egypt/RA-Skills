#!/usr/bin/env python3
"""
Agent Orchestrator - Visualize Agent Network
可视化智能体网络和关系
"""

import json
import subprocess
import sys
from pathlib import Path

def get_agents():
    """获取所有智能体列表"""
    try:
        result = subprocess.run(
            ['openclaw', 'agents', 'list', '--json'],
            capture_output=True,
            text=True,
            check=True
        )
        return json.loads(result.stdout)
    except Exception as e:
        print(f"Error getting agents: {e}", file=sys.stderr)
        return []

def get_agent_sessions(agent_id):
    """获取智能体的会话"""
    try:
        result = subprocess.run(
            ['openclaw', 'sessions', 'list', '--json'],
            capture_output=True,
            text=True,
            check=True
        )
        sessions = json.loads(result.stdout)
        return [s for s in sessions if s.get('agentId') == agent_id]
    except Exception as e:
        return []

def visualize_text(agents):
    """文本格式可视化"""
    print("\n=== Agent Network ===\n")
    
    for agent in agents:
        agent_id = agent.get('id', 'unknown')
        model = agent.get('model', 'default')
        workspace = agent.get('workspace', 'N/A')
        
        print(f"🤖 {agent_id}")
        print(f"   Model: {model}")
        print(f"   Workspace: {workspace}")
        
        sessions = get_agent_sessions(agent_id)
        if sessions:
            print(f"   Active Sessions: {len(sessions)}")
        print()

def visualize_json(agents):
    """JSON 格式输出"""
    output = {
        'agents': [],
        'total': len(agents)
    }
    
    for agent in agents:
        agent_data = {
            'id': agent.get('id'),
            'model': agent.get('model'),
            'workspace': agent.get('workspace'),
            'sessions': len(get_agent_sessions(agent.get('id', '')))
        }
        output['agents'].append(agent_data)
    
    print(json.dumps(output, indent=2))

def main():
    format_type = 'text'
    if '--format' in sys.argv:
        idx = sys.argv.index('--format')
        if idx + 1 < len(sys.argv):
            format_type = sys.argv[idx + 1]
    
    agents = get_agents()
    
    if not agents:
        print("No agents found", file=sys.stderr)
        sys.exit(1)
    
    if format_type == 'json':
        visualize_json(agents)
    else:
        visualize_text(agents)

if __name__ == '__main__':
    main()
