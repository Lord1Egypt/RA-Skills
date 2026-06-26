#!/usr/bin/env python3
"""
Multi-Agent Deploy Script
自动创建新的 assistant agent，编号递增，沿用现有结构
"""

import json
import os
import shutil
import sys
from pathlib import Path

def get_next_assistant_number(base_path: Path) -> int:
    """获取下一个可用的 assistant 编号"""
    existing = []
    for item in base_path.iterdir():
        if item.is_dir():
            name = item.name
            if name == 'assistant':
                existing.append(0)
            elif name.startswith('assistant'):
                try:
                    num = int(name.replace('assistant', ''))
                    existing.append(num)
                except ValueError:
                    pass
    return max(existing) + 1 if existing else 1

def create_workspace(base_path: Path, number: int, template_path: Path) -> Path:
    """创建工作空间目录"""
    # 检查模板是否存在
    if not template_path.exists():
        print(f"❌ 模板工作空间不存在：{template_path}")
        sys.exit(1)
    
    workspace_name = f'workspace-assistant{number}' if number > 0 else 'workspace-assistant'
    workspace_path = base_path.parent / workspace_name
    
    if workspace_path.exists():
        print(f"⚠️  工作空间已存在：{workspace_path}")
        return workspace_path
    
    workspace_path.mkdir(parents=True, exist_ok=True)
    
    # 复制模板文件（排除 .openclaw 等隐藏目录）
    copied = 0
    for template_file in template_path.glob('*'):
        if template_file.is_file() and not template_file.name.startswith('.'):
            dest = workspace_path / template_file.name
            shutil.copy2(template_file, dest)
            print(f"✓ 创建：{dest.name}")
            copied += 1
    
    if copied == 0:
        print(f"⚠️  未复制任何文件，检查模板：{template_path}")
    
    return workspace_path

def create_agent_dir(agents_base: Path, number: int) -> Path:
    """创建 agent 目录"""
    agent_name = f'assistant{number}' if number > 0 else 'assistant'
    agent_path = agents_base / agent_name / 'agent'
    
    if agent_path.exists():
        print(f"⚠️  Agent 目录已存在：{agent_path}")
        return agent_path
    
    agent_path.mkdir(parents=True, exist_ok=True)
    print(f"✓ 创建 agent 目录：{agent_path}")
    
    return agent_path

def update_config(config_path: Path, number: int):
    """更新 openclaw.json 配置"""
    with open(config_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
    
    agent_name = f'assistant{number}' if number > 0 else 'assistant'
    workspace_name = f'workspace-assistant{number}' if number > 0 else 'workspace-assistant'
    
    # 检查是否已存在
    agents_list = config.get('agents', {}).get('list', [])
    for agent in agents_list:
        if agent.get('id') == agent_name:
            print(f"⚠️  Agent 配置已存在：{agent_name}")
            return
    
    # 创建新 agent 配置
    new_agent = {
        'id': agent_name,
        'name': f'日常助手{number}' if number > 0 else '日常助手',
        'workspace': f'/home/admin/.openclaw/{workspace_name}',
        'agentDir': f'/home/admin/.openclaw/agents/{agent_name}/agent',
        'model': 'dashscope/qwen3.5-plus'
    }
    
    agents_list.append(new_agent)
    config['agents']['list'] = agents_list
    
    # 保存配置
    with open(config_path, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
    
    print(f"✓ 更新配置：{config_path}")
    print(f"  - Agent ID: {agent_name}")
    print(f"  - Name: {new_agent['name']}")
    print(f"  - Workspace: {new_agent['workspace']}")

def main():
    base_path = Path('/home/admin/.openclaw/agents')
    config_path = Path('/home/admin/.openclaw/openclaw.json')
    template_workspace = Path('/home/admin/.openclaw/workspace-assistant')
    
    # 获取下一个编号
    number = get_next_assistant_number(base_path)
    print(f"🦞 创建新的 Assistant Agent #{number}")
    print("-" * 40)
    
    # 创建工作空间
    workspace = create_workspace(base_path.parent, number, template_workspace)
    
    # 创建 agent 目录
    agent_dir = create_agent_dir(base_path, number)
    
    # 更新配置
    update_config(config_path, number)
    
    print("-" * 40)
    print(f"✅ 完成！新 Agent 已就绪")
    print(f"   重启 Gateway 生效：openclaw gateway restart")
    print(f"   或手动重启：systemctl --user restart openclaw-gateway")
    
    return 0

if __name__ == '__main__':
    sys.exit(main())
