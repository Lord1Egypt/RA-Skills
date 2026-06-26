#!/usr/bin/env python3
"""
Multi-Agent Orchestrator - Core Engine
多智能体协同核心引擎

功能：
- Agent 注册与发现
- 任务智能分发
- 负载均衡
- Agent 间通信
- 性能监控

Usage:
  python3 orchestrator.py --register <agent-name>
  python3 orchestrator.py --dispatch <task>
  python3 orchestrator.py --status
  python3 orchestrator.py --list
"""

import json
import hashlib
import sys
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional

CONFIG_FILE = Path(__file__).parent.parent / "config" / "agents.json"
STATE_FILE = Path(__file__).parent.parent / "config" / "orchestrator-state.json"

class Colors:
    BLUE = '\033[0;34m'
    GREEN = '\033[0;32m'
    YELLOW = '\033[1;33m'
    CYAN = '\033[0;36m'
    RED = '\033[0;31m'
    MAGENTA = '\033[0;35m'
    NC = '\033[0m'
    BOLD = '\033[1m'

def log_info(msg): print(f"{Colors.BLUE}[INFO]{Colors.NC} {msg}")
def log_success(msg): print(f"{Colors.GREEN}[✓]{Colors.NC} {msg}")
def log_warning(msg): print(f"{Colors.YELLOW}[⚠]{Colors.NC} {msg}")
def log_error(msg): print(f"{Colors.RED}[✗]{Colors.NC} {msg}")

class Agent:
    """Agent 类"""
    def __init__(self, name: str, capabilities: List[str], status: str = "idle"):
        self.name = name
        self.capabilities = capabilities
        self.status = status  # idle, busy, offline
        self.tasks_completed = 0
        self.current_load = 0
        self.max_load = 10
        self.last_seen = datetime.now()
        self.performance_score = 100  # 0-100
    
    def to_dict(self) -> dict:
        return {
            'name': self.name,
            'capabilities': self.capabilities,
            'status': self.status,
            'tasks_completed': self.tasks_completed,
            'current_load': self.current_load,
            'max_load': self.max_load,
            'last_seen': self.last_seen.isoformat(),
            'performance_score': self.performance_score
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        agent = cls(data['name'], data['capabilities'], data.get('status', 'idle'))
        agent.tasks_completed = data.get('tasks_completed', 0)
        agent.current_load = data.get('current_load', 0)
        agent.max_load = data.get('max_load', 10)
        try:
            agent.last_seen = datetime.fromisoformat(data['last_seen'])
        except (AttributeError, ValueError):
            agent.last_seen = datetime.now()
        agent.performance_score = data.get('performance_score', 100)
        return agent

class Orchestrator:
    """多智能体协同引擎"""
    
    def __init__(self):
        self.agents: Dict[str, Agent] = {}
        self.task_queue = []
        self.task_history = []
        self.load_config()
    
    def load_config(self):
        """加载配置"""
        if CONFIG_FILE.exists():
            try:
                with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    for agent_data in config.get('agents', []):
                        agent = Agent.from_dict(agent_data)
                        self.agents[agent.name] = agent
                log_info(f"已加载 {len(self.agents)} 个 Agent")
            except Exception as e:
                log_error(f"加载配置失败：{e}")
        else:
            log_warning("配置文件不存在，将创建新配置")
            self.save_config()
    
    def save_config(self):
        """保存配置"""
        CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)
        config = {
            'version': '1.0',
            'updated_at': datetime.now().isoformat(),
            'agents': [agent.to_dict() for agent in self.agents.values()],
            'task_history': self.task_history[-100:]  # 保留最近 100 个任务
        }
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        log_success(f"配置已保存：{CONFIG_FILE}")
    
    def register_agent(self, name: str, capabilities: List[str]) -> bool:
        """注册 Agent"""
        if name in self.agents:
            log_warning(f"Agent {name} 已存在，更新信息")
            self.agents[name].capabilities = capabilities
        else:
            agent = Agent(name, capabilities)
            self.agents[name] = agent
            log_success(f"已注册 Agent: {name}")
        
        self.save_config()
        return True
    
    def unregister_agent(self, name: str) -> bool:
        """注销 Agent"""
        if name in self.agents:
            del self.agents[name]
            log_success(f"已注销 Agent: {name}")
            self.save_config()
            return True
        else:
            log_error(f"Agent {name} 不存在")
            return False
    
    def list_agents(self) -> List[Agent]:
        """列出所有 Agent"""
        return list(self.agents.values())
    
    def find_best_agent(self, task: str) -> Optional[Agent]:
        """根据任务找到最合适的 Agent（智能分发）"""
        if not self.agents:
            return None
        
        # 简单的基于能力的匹配
        best_agent = None
        best_score = 0
        
        for agent in self.agents.values():
            if agent.status == 'offline':
                continue
            
            # 计算负载分数（越低越好）
            load_score = 1 - (agent.current_load / agent.max_load)
            
            # 计算性能分数
            perf_score = agent.performance_score / 100
            
            # 计算能力匹配分数
            task_keywords = task.lower().split()
            capability_matches = sum(1 for cap in agent.capabilities 
                                    if any(kw in cap.lower() for kw in task_keywords))
            capability_score = capability_matches / max(len(agent.capabilities), 1)
            
            # 综合评分
            total_score = (load_score * 0.4) + (perf_score * 0.4) + (capability_score * 0.2)
            
            if total_score > best_score:
                best_score = total_score
                best_agent = agent
        
        return best_agent
    
    def dispatch_task(self, task: str, agent_name: Optional[str] = None) -> dict:
        """分发任务"""
        task_id = hashlib.md5(f"{task}{datetime.now()}".encode()).hexdigest()[:8]
        
        # 如果指定了 Agent
        if agent_name:
            if agent_name not in self.agents:
                return {'success': False, 'error': f'Agent {agent_name} 不存在'}
            agent = self.agents[agent_name]
        else:
            # 自动选择最佳 Agent
            agent = self.find_best_agent(task)
            if not agent:
                return {'success': False, 'error': '没有可用的 Agent'}
        
        # 检查 Agent 状态
        if agent.status == 'offline':
            return {'success': False, 'error': f'Agent {agent.name} 离线'}
        
        if agent.current_load >= agent.max_load:
            return {'success': False, 'error': f'Agent {agent.name} 负载已满'}
        
        # 分发任务
        agent.current_load += 1
        agent.status = 'busy'
        
        task_record = {
            'task_id': task_id,
            'task': task,
            'agent': agent.name,
            'status': 'dispatched',
            'created_at': datetime.now().isoformat(),
            'completed_at': None
        }
        
        self.task_queue.append(task_record)
        self.task_history.append(task_record)
        
        log_success(f"任务已分发：{task[:50]}... → Agent: {agent.name}")
        
        return {
            'success': True,
            'task_id': task_id,
            'agent': agent.name,
            'estimated_time': '5-10 分钟'
        }
    
    def complete_task(self, task_id: str, success: bool = True):
        """标记任务完成"""
        for task in self.task_queue:
            if task['task_id'] == task_id:
                task['status'] = 'completed' if success else 'failed'
                task['completed_at'] = datetime.now().isoformat()
                
                # 更新 Agent 状态
                agent_name = task['agent']
                if agent_name in self.agents:
                    agent = self.agents[agent_name]
                    agent.current_load = max(0, agent.current_load - 1)
                    if agent.current_load == 0:
                        agent.status = 'idle'
                    if success:
                        agent.tasks_completed += 1
                        agent.performance_score = min(100, agent.performance_score + 1)
                    else:
                        agent.performance_score = max(0, agent.performance_score - 5)
                
                self.task_queue.remove(task)
                log_success(f"任务已完成：{task_id}")
                break
    
    def get_status(self) -> dict:
        """获取系统状态"""
        total_agents = len(self.agents)
        idle_agents = sum(1 for a in self.agents.values() if a.status == 'idle')
        busy_agents = sum(1 for a in self.agents.values() if a.status == 'busy')
        offline_agents = sum(1 for a in self.agents.values() if a.status == 'offline')
        
        avg_load = sum(a.current_load for a in self.agents.values()) / max(total_agents, 1)
        avg_performance = sum(a.performance_score for a in self.agents.values()) / max(total_agents, 1)
        
        return {
            'total_agents': total_agents,
            'idle_agents': idle_agents,
            'busy_agents': busy_agents,
            'offline_agents': offline_agents,
            'tasks_in_queue': len(self.task_queue),
            'tasks_completed': sum(a.tasks_completed for a in self.agents.values()),
            'avg_load': avg_load,
            'avg_performance': avg_performance,
            'agents': [a.to_dict() for a in self.agents.values()]
        }

def print_status(orchestrator: Orchestrator):
    """打印状态"""
    status = orchestrator.get_status()
    
    print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*60}{Colors.NC}")
    print(f"{Colors.BOLD}{Colors.CYAN}🤖 Multi-Agent Orchestrator Status{Colors.NC}")
    print(f"{Colors.BOLD}{Colors.CYAN}{'='*60}{Colors.NC}\n")
    
    print(f"Agent 总数：{status['total_agents']}")
    print(f"  {Colors.GREEN}空闲：{status['idle_agents']}{Colors.NC}")
    print(f"  {Colors.YELLOW}忙碌：{status['busy_agents']}{Colors.NC}")
    print(f"  {Colors.RED}离线：{status['offline_agents']}{Colors.NC}")
    print()
    print(f"任务队列：{status['tasks_in_queue']}")
    print(f"已完成任务：{status['tasks_completed']}")
    print(f"平均负载：{status['avg_load']:.1f}/10")
    print(f"平均性能：{status['avg_performance']:.1f}/100")
    print()
    
    if status['agents']:
        print(f"{Colors.BOLD}Agent 列表：{Colors.NC}\n")
        for agent in status['agents']:
            status_icon = "🟢" if agent['status'] == 'idle' else "🟡" if agent['status'] == 'busy' else "🔴"
            load_bar = "█" * agent['current_load'] + "░" * (agent['max_load'] - agent['current_load'])
            print(f"  {status_icon} {agent['name']}")
            print(f"      能力：{', '.join(agent['capabilities'])}")
            print(f"      负载：[{load_bar}] {agent['current_load']}/{agent['max_load']}")
            print(f"      性能：{agent['performance_score']}/100")
            print(f"      完成任务：{agent['tasks_completed']}")
            print()
    
    print(f"{Colors.BOLD}{Colors.CYAN}{'='*60}{Colors.NC}\n")

def main():
    parser = argparse.ArgumentParser(description='多智能体协同引擎')
    parser.add_argument('--register', type=str, help='注册 Agent（名称）')
    parser.add_argument('--capabilities', type=str, nargs='+', help='Agent 能力列表')
    parser.add_argument('--unregister', type=str, help='注销 Agent')
    parser.add_argument('--dispatch', type=str, help='分发任务')
    parser.add_argument('--agent', type=str, help='指定 Agent')
    parser.add_argument('--complete', type=str, help='标记任务完成')
    parser.add_argument('--status', action='store_true', help='显示状态')
    parser.add_argument('--list', action='store_true', help='列出所有 Agent')
    
    args = parser.parse_args()
    
    orchestrator = Orchestrator()
    
    if args.register:
        capabilities = args.capabilities or ['general']
        orchestrator.register_agent(args.register, capabilities)
    
    elif args.unregister:
        orchestrator.unregister_agent(args.unregister)
    
    elif args.dispatch:
        result = orchestrator.dispatch_task(args.dispatch, args.agent)
        if result['success']:
            log_success(f"任务分发成功：{result}")
        else:
            log_error(f"任务分发失败：{result['error']}")
    
    elif args.complete:
        orchestrator.complete_task(args.complete)
    
    elif args.status:
        print_status(orchestrator)
    
    elif args.list:
        agents = orchestrator.list_agents()
        if agents:
            print(f"\n{Colors.BOLD}已注册的 Agent：{Colors.NC}\n")
            for agent in agents:
                print(f"  • {agent.name}")
                print(f"    能力：{', '.join(agent.capabilities)}")
                print(f"    状态：{agent.status}")
                print()
        else:
            log_warning("没有已注册的 Agent")
    
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
