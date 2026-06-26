#!/usr/bin/env python3
"""
OpenClaw Agent 管理脚本
添加、删除、修改 Agent 配置
"""

import json
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime

# 配置路径
OPENCLAW_CONFIG = Path.home() / ".openclaw" / "openclaw.json"


class AgentManager:
    """OpenClaw Agent 管理器"""
    
    def __init__(self, config_path: Path = OPENCLAW_CONFIG):
        self.config_path = config_path
        self.config = None
        self.agents = []
    
    def load_config(self) -> bool:
        """加载配置文件"""
        if not self.config_path.exists():
            print(f"❌ 配置文件不存在：{self.config_path}")
            return False
        
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                self.config = json.load(f)
            self.agents = self.config.get("agents", {}).get("list", [])
            return True
        except Exception as e:
            print(f"❌ 加载配置失败：{e}")
            return False
    
    def save_config(self) -> bool:
        """保存配置文件"""
        try:
            # 备份原配置
            backup_path = self.config_path.with_suffix('.json.bak')
            backup_path.write_text(
                self.config_path.read_text(encoding='utf-8'),
                encoding='utf-8'
            )
            print(f"✓ 备份已保存：{backup_path}")
            
            # 保存新配置
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, ensure_ascii=False, indent=2)
            
            print(f"✓ 配置已保存：{self.config_path}")
            return True
        except Exception as e:
            print(f"❌ 保存配置失败：{e}")
            return False
    
    def add_agent(self, agent_id: str, model: str, name: Optional[str] = None,
                  subagents: Optional[List[str]] = None, default: bool = False) -> bool:
        """添加新 Agent"""
        # 检查是否已存在
        for agent in self.agents:
            if agent.get("id") == agent_id:
                print(f"❌ Agent '{agent_id}' 已存在")
                return False
        
        # 创建 agent 配置
        new_agent = {
            "id": agent_id,
            "name": name or agent_id.replace("-", " ").title(),
            "model": model
        }
        
        # 添加 subagents 配置
        if subagents:
            new_agent["subagents"] = {
                "allowAgents": subagents
            }
        
        # 设置 default
        if default:
            # 移除其他 default agent
            for agent in self.agents:
                agent.pop("default", None)
            new_agent["default"] = True
        
        # 添加到列表
        self.agents.append(new_agent)
        self.config["agents"]["list"] = self.agents
        
        print(f"✅ Agent '{agent_id}' 添加成功")
        print(f"   名称：{new_agent['name']}")
        print(f"   模型：{model}")
        if subagents:
            print(f"   子 Agent: {', '.join(subagents)}")
        
        return self.save_config()
    
    def remove_agent(self, agent_id: str, force: bool = False) -> bool:
        """删除 Agent"""
        # 检查是否存在
        agent_found = None
        for agent in self.agents:
            if agent.get("id") == agent_id:
                agent_found = agent
                break
        
        if not agent_found:
            print(f"❌ Agent '{agent_id}' 不存在")
            return False
        
        # 检查依赖关系
        if not force:
            for agent in self.agents:
                if agent.get("id") == agent_id:
                    continue
                subagents = agent.get("subagents", {}).get("allowAgents", [])
                if agent_id in subagents:
                    print(f"⚠️  Agent '{agent_id}' 被以下 agent 引用:")
                    print(f"   - {agent.get('id')}")
                    print(f"   使用 --force 强制删除")
                    return False
        
        # 删除
        self.agents = [a for a in self.agents if a.get("id") != agent_id]
        self.config["agents"]["list"] = self.agents
        
        # 从其他 agent 的 allowAgents 中移除
        for agent in self.agents:
            if "subagents" in agent and "allowAgents" in agent["subagents"]:
                if agent_id in agent["subagents"]["allowAgents"]:
                    agent["subagents"]["allowAgents"].remove(agent_id)
        
        print(f"✅ Agent '{agent_id}' 删除成功")
        return self.save_config()
    
    def update_agent(self, agent_id: str, **kwargs) -> bool:
        """更新 Agent 配置"""
        agent_found = None
        for agent in self.agents:
            if agent.get("id") == agent_id:
                agent_found = agent
                break
        
        if not agent_found:
            print(f"❌ Agent '{agent_id}' 不存在")
            return False
        
        # 更新字段
        updates = []
        for key, value in kwargs.items():
            if key in ["id", "name", "model", "default"]:
                agent_found[key] = value
                updates.append(f"{key}={value}")
            elif key == "subagents":
                agent_found["subagents"] = {"allowAgents": value}
                updates.append(f"subagents={value}")
        
        if not updates:
            print("⚠️  没有指定要更新的字段")
            return False
        
        print(f"✅ Agent '{agent_id}' 更新成功:")
        for update in updates:
            print(f"   - {update}")
        
        return self.save_config()
    
    def list_agents(self, verbose: bool = False) -> None:
        """列出所有 Agent"""
        print("=" * 60)
        print(f"  OpenClaw Agents ({len(self.agents)}个)")
        print("=" * 60)
        print()
        
        for i, agent in enumerate(self.agents, 1):
            agent_id = agent.get("id", "unknown")
            name = agent.get("name", agent_id)
            model = agent.get("model", "未配置")
            default = agent.get("default", False)
            
            icon = "👑" if default else "🤖"
            print(f"{i}. {icon} {agent_id} ({name})")
            print(f"   模型：{model}")
            
            if verbose:
                subagents = agent.get("subagents", {}).get("allowAgents", [])
                if subagents:
                    print(f"   子 Agent: {', '.join(subagents)}")
            
            print()
        
        print("=" * 60)


def main():
    """命令行入口"""
    import argparse
    
    parser = argparse.ArgumentParser(description="OpenClaw Agent 管理工具")
    subparsers = parser.add_subparsers(dest="action", help="操作类型")
    
    # add 命令
    add_parser = subparsers.add_parser("add", help="添加 Agent")
    add_parser.add_argument("--id", required=True, help="Agent ID")
    add_parser.add_argument("--model", required=True, help="模型配置 (如 qwen/qwen3.5-plus)")
    add_parser.add_argument("--name", help="Agent 名称")
    add_parser.add_argument("--subagents", nargs="+", help="允许的子 Agent 列表")
    add_parser.add_argument("--default", action="store_true", help="设为默认 Agent")
    
    # remove 命令
    remove_parser = subparsers.add_parser("remove", help="删除 Agent")
    remove_parser.add_argument("--id", required=True, help="Agent ID")
    remove_parser.add_argument("--force", action="store_true", help="强制删除")
    
    # update 命令
    update_parser = subparsers.add_parser("update", help="更新 Agent")
    update_parser.add_argument("--id", required=True, help="Agent ID")
    update_parser.add_argument("--model", help="新模型配置")
    update_parser.add_argument("--name", help="新名称")
    update_parser.add_argument("--subagents", nargs="+", help="新的子 Agent 列表")
    
    # list 命令
    list_parser = subparsers.add_parser("list", help="列出所有 Agent")
    list_parser.add_argument("--verbose", "-v", action="store_true", help="显示详细信息")
    
    args = parser.parse_args()
    
    manager = AgentManager()
    if not manager.load_config():
        sys.exit(1)
    
    if args.action == "add":
        success = manager.add_agent(
            args.id, args.model, args.name, args.subagents, args.default
        )
    elif args.action == "remove":
        success = manager.remove_agent(args.id, args.force)
    elif args.action == "update":
        kwargs = {}
        if args.model:
            kwargs["model"] = args.model
        if args.name:
            kwargs["name"] = args.name
        if args.subagents:
            kwargs["subagents"] = args.subagents
        success = manager.update_agent(args.id, **kwargs)
    elif args.action == "list":
        manager.list_agents(args.verbose)
        success = True
    else:
        parser.print_help()
        success = False
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
