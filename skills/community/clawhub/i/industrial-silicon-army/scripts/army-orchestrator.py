#!/usr/bin/env python3
"""
Agent集群任务分配器 - Level 2
Agent Army Orchestrator

功能：
- assign: Agent集群任务分配（能力匹配+负载均衡）
- optimize: 并行度优化
- failover: 故障转移策略

Author: Industrial Silicon Army
Version: 1.0.0
"""

import sys
import json
import time
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum
from collections import defaultdict


class AgentCapability(Enum):
    """Agent能力类型"""
    PROCUREMENT = "采购分析"      # 采购相关
    PRODUCTION = "生产调度"        # 生产相关
    SALES = "销售预测"            # 销售相关
    FINANCE = "财务核算"          # 财务相关
    WAREHOUSE = "库存管理"        # 仓储相关
    QUALITY = "质量检测"          # 质检相关
    LOGISTICS = "物流调度"        # 物流相关
    CUSTOMER = "客户分析"         # 客服相关
    DATA = "数据分析"             # 数据分析
    GENERAL = "通用任务"           # 通用任务


class TaskPriority(Enum):
    """任务优先级"""
    URGENT = 1    # 紧急
    HIGH = 2      # 高
    NORMAL = 3    # 普通
    LOW = 4       # 低


@dataclass
class Agent:
    """Agent定义"""
    id: str
    name: str
    capabilities: List[AgentCapability]
    load: float  # 当前负载 0-1
    max_load: float = 1.0
    status: str = "active"  # active, busy, offline
    avg_response_time: float = 1.0  # 平均响应时间(秒)
    
    def can_handle(self, task_load: float) -> bool:
        """检查是否能处理任务"""
        return self.status == "active" and (self.load + task_load) <= self.max_load
    
    def get_utilization(self) -> float:
        """获取利用率"""
        return (self.load / self.max_load) * 100 if self.max_load > 0 else 0


@dataclass
class Task:
    """任务定义"""
    id: str
    name: str
    required_capabilities: List[AgentCapability]
    priority: TaskPriority
    estimated_load: float  # 任务负载 0-1
    dependencies: List[str] = field(default_factory=list)
    deadline: Optional[str] = None
    data: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Assignment:
    """任务分配结果"""
    task_id: str
    agent_id: str
    agent_name: str
    confidence: float  # 分配置信度 0-1
    reasoning: str
    estimated_time: float  # 预估完成时间


class AgentOrchestrator:
    """Agent集群任务编排器"""
    
    def __init__(self):
        self.agents: Dict[str, Agent] = {}
        self.tasks: Dict[str, Task] = {}
        self.assignments: List[Assignment] = []
        self.failure_history: List[Dict] = []
    
    def register_agent(self, agent: Agent) -> bool:
        """注册Agent"""
        if agent.id in self.agents:
            return False
        self.agents[agent.id] = agent
        return True
    
    def add_task(self, task: Task) -> bool:
        """添加任务"""
        if task.id in self.tasks:
            return False
        self.tasks[task.id] = task
        return True
    
    def match_capabilities(self, task: Task, agent: Agent) -> float:
        """
        匹配任务与Agent能力
        
        Returns:
            匹配度 0-1
        """
        required = set(task.required_capabilities)
        provided = set(agent.capabilities)
        
        if not required:
            return 0.5  # 无能力要求，按负载分配
        
        intersection = required & provided
        
        if not intersection:
            return 0.0  # 完全不匹配
        
        # 计算匹配度
        match_ratio = len(intersection) / len(required)
        
        # 额外能力加分（最多0.2）
        extra_ratio = min(0.2, (len(provided) - len(intersection)) / len(provided))
        
        return min(1.0, match_ratio + extra_ratio)
    
    def calculate_load_score(self, agent: Agent) -> float:
        """
        计算负载得分
        
        Returns:
            负载得分 0-1，1表示最空闲
        """
        current_utilization = agent.load / agent.max_load if agent.max_load > 0 else 1.0
        return 1.0 - current_utilization
    
    def calculate_response_score(self, agent: Agent) -> float:
        """
        计算响应时间得分
        
        Returns:
            响应得分 0-1，1表示响应最快
        """
        if agent.avg_response_time <= 0:
            return 0.5
        
        # 假设1秒内响应得满分，10秒以上得0分
        score = max(0, 1.0 - (agent.avg_response_time - 1) / 9)
        return score
    
    def assign_task(self, task_id: str) -> Optional[Assignment]:
        """
        分配单个任务
        
        Returns:
            分配结果或None
        """
        if task_id not in self.tasks:
            return None
        
        task = self.tasks[task_id]
        best_agent = None
        best_score = -1
        reasoning = ""
        
        for agent in self.agents.values():
            if not agent.can_handle(task.estimated_load):
                continue
            
            # 计算综合得分
            cap_score = self.match_capabilities(task, agent)
            if cap_score == 0:
                continue
            
            load_score = self.calculate_load_score(agent)
            response_score = self.calculate_response_score(agent)
            
            # 优先级权重
            priority_weight = {
                TaskPriority.URGENT: 1.5,
                TaskPriority.HIGH: 1.2,
                TaskPriority.NORMAL: 1.0,
                TaskPriority.LOW: 0.8
            }.get(task.priority, 1.0)
            
            # 综合得分
            total_score = (
                cap_score * 0.5 +           # 能力匹配权重50%
                load_score * 0.3 +           # 负载均衡权重30%
                response_score * 0.2          # 响应速度权重20%
            ) * priority_weight
            
            if total_score > best_score:
                best_score = total_score
                best_agent = agent
                reasoning = self._generate_reasoning(task, agent, cap_score, load_score, response_score)
        
        if best_agent is None:
            return None
        
        # 执行分配
        best_agent.load += task.estimated_load
        
        # 生成预估时间
        base_time = best_agent.avg_response_time * (1 + task.estimated_load)
        estimated_time = base_time * (1 / best_score)
        
        assignment = Assignment(
            task_id=task_id,
            agent_id=best_agent.id,
            agent_name=best_agent.name,
            confidence=best_score,
            reasoning=reasoning,
            estimated_time=estimated_time
        )
        
        self.assignments.append(assignment)
        return assignment
    
    def _generate_reasoning(self, task: Task, agent: Agent, 
                            cap_score: float, load_score: float, 
                            response_score: float) -> str:
        """生成分配理由"""
        reasons = []
        
        if cap_score >= 0.8:
            reasons.append("能力高度匹配")
        elif cap_score >= 0.5:
            reasons.append("能力基本匹配")
        
        if load_score >= 0.7:
            reasons.append("当前负载较低")
        elif load_score >= 0.4:
            reasons.append("负载适中")
        
        if response_score >= 0.8:
            reasons.append("响应速度快")
        
        if task.priority == TaskPriority.URGENT:
            reasons.append("优先处理紧急任务")
        
        return "，".join(reasons) if reasons else "综合评估最优"
    
    def assign_all(self) -> List[Assignment]:
        """分配所有待处理任务"""
        # 按优先级排序
        sorted_tasks = sorted(
            self.tasks.values(),
            key=lambda t: (t.priority.value, -t.estimated_load)
        )
        
        results = []
        for task in sorted_tasks:
            result = self.assign_task(task.id)
            if result:
                results.append(result)
            else:
                results.append(Assignment(
                    task_id=task.id,
                    agent_id="",
                    agent_name="待分配",
                    confidence=0,
                    reasoning="无可用Agent或能力不匹配",
                    estimated_time=0
                ))
        
        return results
    
    def optimize_parallelism(self, task_ids: List[str]) -> Dict[str, Any]:
        """
        优化并行度
        
        Returns:
            优化建议
        """
        tasks = [self.tasks[tid] for tid in task_ids if tid in self.tasks]
        
        if not tasks:
            return {"error": "无有效任务"}
        
        # 分析依赖关系
        dependency_graph = {}
        task_loads = {}
        
        for task in tasks:
            dependency_graph[task.id] = task.dependencies
            task_loads[task.id] = task.estimated_load
        
        # 计算关键路径
        critical_path = self._find_critical_path(dependency_graph, task_loads)
        
        # 计算最优并行度
        total_load = sum(task_loads.values())
        active_agents = len([a for a in self.agents.values() if a.status == "active"])
        
        optimal_parallel = min(active_agents, len(tasks))
        efficiency = min(1.0, total_load / (optimal_parallel * 0.8))
        
        return {
            "总任务数": len(tasks),
            "活跃Agent数": active_agents,
            "最优并行度": optimal_parallel,
            "理论效率": f"{efficiency*100:.1f}%",
            "关键路径任务": critical_path,
            "建议": self._generate_parallelism_suggestions(efficiency, critical_path)
        }
    
    def _find_critical_path(self, dependencies: Dict, loads: Dict) -> List[str]:
        """查找关键路径"""
        # 简化版本：返回负载最重的任务链
        sorted_by_load = sorted(loads.items(), key=lambda x: -x[1])
        return [tid for tid, _ in sorted_by_load[:3]]
    
    def _generate_parallelism_suggestions(self, efficiency: float, 
                                          critical_path: List[str]) -> List[str]:
        """生成并行度优化建议"""
        suggestions = []
        
        if efficiency < 0.5:
            suggestions.append("当前并行效率较低，建议增加Agent数量")
            suggestions.append("考虑拆分大任务为小任务")
        elif efficiency < 0.8:
            suggestions.append("并行效率有提升空间")
            suggestions.append("关注关键路径任务的优化")
        else:
            suggestions.append("并行效率良好")
            suggestions.append("保持当前调度策略")
        
        if critical_path:
            suggestions.append(f"关键路径任务: {', '.join(critical_path)}")
        
        return suggestions
    
    def plan_failover(self, agent_id: str) -> Dict[str, Any]:
        """
        规划故障转移
        
        Args:
            agent_id: 故障Agent ID
        
        Returns:
            故障转移方案
        """
        if agent_id not in self.agents:
            return {"error": "Agent不存在"}
        
        failed_agent = self.agents[agent_id]
        
        # 查找被分配的任务
        assigned_tasks = [a for a in self.assignments if a.agent_id == agent_id]
        
        if not assigned_tasks:
            return {
                "failed_agent": agent_id,
                "message": "该Agent无待处理任务，无需转移",
                "affected_tasks": 0
            }
        
        # 寻找备选Agent
        backup_candidates = []
        for agent in self.agents.values():
            if agent.id == agent_id or agent.status != "active":
                continue
            
            cap_match = False
            for task in assigned_tasks:
                task_obj = self.tasks.get(task.task_id)
                if task_obj and self.match_capabilities(task_obj, agent) > 0:
                    cap_match = True
                    break
            
            if cap_match:
                backup_candidates.append({
                    "agent_id": agent.id,
                    "agent_name": agent.name,
                    "current_load": agent.get_utilization(),
                    "score": self.calculate_load_score(agent)
                })
        
        # 按负载排序
        backup_candidates.sort(key=lambda x: x["score"], reverse=True)
        
        # 生成转移计划
        transfer_plan = []
        remaining_load = failed_agent.load
        
        for candidate in backup_candidates:
            if remaining_load <= 0:
                break
            
            agent = self.agents[candidate["agent_id"]]
            transfer_load = min(remaining_load, (agent.max_load - agent.load) * 0.3)
            
            if transfer_load > 0:
                transfer_plan.append({
                    "to_agent": candidate["agent_name"],
                    "transfer_load": f"{transfer_load*100:.1f}%",
                    "reason": "能力匹配且负载较低"
                })
                remaining_load -= transfer_load
        
        return {
            "failed_agent": failed_agent.name,
            "affected_tasks": len(assigned_tasks),
            "total_load": f"{failed_agent.load*100:.1f}%",
            "transfer_plan": transfer_plan,
            "message": "已制定转移方案" if transfer_plan else "无可用备选Agent",
            "recovery_time_estimate": f"{len(assigned_tasks) * 2}分钟"
        }
    
    def get_cluster_status(self) -> Dict[str, Any]:
        """获取集群状态"""
        agent_stats = []
        
        for agent in self.agents.values():
            agent_stats.append({
                "id": agent.id,
                "name": agent.name,
                "status": agent.status,
                "load": f"{agent.get_utilization():.1f}%",
                "capabilities": [c.value for c in agent.capabilities],
                "response_time": f"{agent.avg_response_time:.1f}s"
            })
        
        # 计算集群总体指标
        active_count = len([a for a in self.agents.values() if a.status == "active"])
        avg_load = sum(a.load for a in self.agents.values()) / len(self.agents) if self.agents else 0
        
        return {
            "total_agents": len(self.agents),
            "active_agents": active_count,
            "cluster_load": f"{avg_load*100:.1f}%",
            "pending_tasks": len(self.tasks),
            "assigned_tasks": len(self.assignments),
            "agents": agent_stats
        }


def create_sample_cluster() -> AgentOrchestrator:
    """创建示例集群"""
    orchestrator = AgentOrchestrator()
    
    # 注册示例Agent
    agents = [
        Agent("A001", "采购专家", [AgentCapability.PROCUREMENT, AgentCapability.DATA], 0.3, 1.0, "active", 0.8),
        Agent("A002", "生产调度", [AgentCapability.PRODUCTION, AgentCapability.LOGISTICS], 0.5, 1.0, "active", 1.2),
        Agent("A003", "销售分析", [AgentCapability.SALES, AgentCapability.DATA], 0.2, 1.0, "active", 0.6),
        Agent("A004", "财务核算", [AgentCapability.FINANCE], 0.6, 1.0, "active", 1.0),
        Agent("A005", "仓储管理", [AgentCapability.WAREHOUSE, AgentCapability.LOGISTICS], 0.4, 1.0, "active", 0.9),
        Agent("A006", "质检专家", [AgentCapability.QUALITY], 0.7, 1.0, "busy", 1.5),
    ]
    
    for agent in agents:
        orchestrator.register_agent(agent)
    
    return orchestrator


def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("用法: python army-orchestrator.py <command> [args]")
        print("命令:")
        print("  assign          - 分配所有任务")
        print("  optimize        - 优化并行度")
        print("  failover        - 故障转移规划")
        print("  status          - 查看集群状态")
        return
    
    command = sys.argv[1]
    orchestrator = create_sample_cluster()
    
    if command == "assign":
        # 添加示例任务
        tasks = [
            Task("T001", "PP粒子询价", [AgentCapability.PROCUREMENT], TaskPriority.HIGH, 0.2),
            Task("T002", "生产排产", [AgentCapability.PRODUCTION], TaskPriority.NORMAL, 0.3),
            Task("T003", "销售预测", [AgentCapability.SALES, AgentCapability.DATA], TaskPriority.NORMAL, 0.25),
            Task("T004", "库存盘点", [AgentCapability.WAREHOUSE], TaskPriority.LOW, 0.15),
            Task("T005", "紧急采购", [AgentCapability.PROCUREMENT], TaskPriority.URGENT, 0.1),
        ]
        
        for task in tasks:
            orchestrator.add_task(task)
        
        results = orchestrator.assign_all()
        
        print("=" * 60)
        print("任务分配结果")
        print("=" * 60)
        
        for result in results:
            status = "✓" if result.agent_id else "✗"
            print(f"\n{status} 任务: {result.task_id}")
            print(f"  分配给: {result.agent_name}")
            print(f"  置信度: {result.confidence*100:.1f}%")
            print(f"  理由: {result.reasoning}")
            print(f"  预估时间: {result.estimated_time:.1f}秒")
        
    elif command == "optimize":
        task_ids = list(orchestrator.tasks.keys())
        if not task_ids:
            print("请先分配任务")
            return
        
        result = orchestrator.optimize_parallelism(task_ids)
        
        print("=" * 60)
        print("并行度优化分析")
        print("=" * 60)
        for k, v in result.items():
            if isinstance(v, list):
                print(f"{k}:")
                for item in v:
                    print(f"  - {item}")
            else:
                print(f"{k}: {v}")
        
    elif command == "failover":
        agent_id = sys.argv[2] if len(sys.argv) > 2 else "A001"
        result = orchestrator.plan_failover(agent_id)
        
        print("=" * 60)
        print(f"故障转移方案 ({result.get('failed_agent', 'Unknown')})")
        print("=" * 60)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        
    elif command == "status":
        result = orchestrator.get_cluster_status()
        
        print("=" * 60)
        print("集群状态")
        print("=" * 60)
        print(f"总Agent数: {result['total_agents']}")
        print(f"活跃Agent: {result['active_agents']}")
        print(f"集群负载: {result['cluster_load']}")
        print(f"待处理任务: {result['pending_tasks']}")
        print(f"已分配任务: {result['assigned_tasks']}")
        
        print("\n【Agent详情】")
        for agent in result["agents"]:
            print(f"\n  [{agent['status']}] {agent['name']}")
            print(f"    负载: {agent['load']}")
            print(f"    能力: {', '.join(agent['capabilities'])}")
            print(f"    响应时间: {agent['response_time']}")
    else:
        print(f"未知命令: {command}")


if __name__ == "__main__":
    main()
