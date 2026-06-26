#!/usr/bin/env python3
"""
OClaw-Hermes 统一核心 v3.0
深度融合：Hermes五层记忆 + DeerFlow六智能体 + OpenClaw Skills

核心创新：
1. 记忆驱动的智能体路由
2. Skill-记忆双向增强
3. 跨平台状态同步
4. 智能体协作记忆沉淀
"""

import sys
sys.path.insert(0, 'C:\\Users\\wry08\\.openclaw\\skills\\oclaw-hermes\\scripts')

from mflow_v2 import MFlowEngineV2, MemoryEntry
from auto_memory import AutoMemorySystem
from datetime import datetime
import hashlib
import json
from typing import List, Dict, Optional, Any, Callable
from dataclasses import dataclass, field
from enum import Enum
import threading
import time

class AgentType(Enum):
    """DeerFlow 六大智能体类型"""
    LEAD = "lead"           # 主控智能体
    RESEARCH = "research"   # 研究智能体
    CODE = "code"          # 代码智能体
    BROWSER = "browser"    # 浏览器智能体
    MEMORY = "memory"      # 记忆智能体
    SKILL = "skill"        # Skill智能体

class TaskType(Enum):
    """任务类型"""
    RESEARCH = "research"
    CODE = "code"
    ANALYSIS = "analysis"
    CREATIVE = "creative"
    MEMORY = "memory"
    SKILL = "skill"

@dataclass
class AgentState:
    """智能体状态"""
    agent_type: AgentType
    status: str = "idle"  # idle, running, completed, error
    current_task: str = None
    memory_context: List[str] = field(default_factory=list)
    skill_history: List[str] = field(default_factory=list)
    start_time: datetime = None
    end_time: datetime = None
    
    def __post_init__(self):
        if self.start_time is None:
            self.start_time = datetime.now()

@dataclass
class UnifiedTask:
    """统一任务"""
    id: str
    type: TaskType
    content: str
    agent_states: Dict[AgentType, AgentState] = field(default_factory=dict)
    memory_entries: List[str] = field(default_factory=list)
    skill_calls: List[Dict] = field(default_factory=list)
    result: Any = None
    created_at: datetime = None
    completed_at: datetime = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()

class UnifiedCore:
    """
    统一核心 - 深度融合三大系统
    """
    
    def __init__(self):
        self.mflow = MFlowEngineV2()
        self.auto_memory = AutoMemorySystem()
        self.active_tasks: Dict[str, UnifiedTask] = {}
        self.agent_registry: Dict[AgentType, Callable] = {}
        self.skill_registry: Dict[str, Dict] = {}
        self._lock = threading.Lock()
        
        # 初始化智能体注册表
        self._init_agents()
        
    def _init_agents(self):
        """初始化六大智能体"""
        self.agent_registry = {
            AgentType.LEAD: self._lead_agent,
            AgentType.RESEARCH: self._research_agent,
            AgentType.CODE: self._code_agent,
            AgentType.BROWSER: self._browser_agent,
            AgentType.MEMORY: self._memory_agent,
            AgentType.SKILL: self._skill_agent
        }
    
    def _lead_agent(self, task: UnifiedTask) -> Dict:
        """
        主控智能体 - 任务分解与路由
        
        核心功能：
        1. 分析用户意图
        2. 检索相关记忆
        3. 推荐相关Skills
        4. 分解子任务
        5. 调度其他智能体
        """
        # 1. 检索相关记忆
        memory_context = self.mflow.retrieve(
            task.content, 
            top_k=5,
            use_graph=True
        )
        
        # 2. 推荐Skills
        suggested_skills = self.auto_memory.suggest_skills(task.content)
        
        # 3. 意图分析（简化版）
        intent = self._analyze_intent(task.content)
        
        # 4. 任务分解
        subtasks = self._decompose_task(task, intent, memory_context)
        
        # 5. 存储意图记忆
        self.auto_memory.record_user_intent(
            task.content,
            intent["type"],
            intent["confidence"]
        )
        
        return {
            "intent": intent,
            "memory_context": memory_context,
            "suggested_skills": suggested_skills,
            "subtasks": subtasks
        }
    
    def _research_agent(self, task: UnifiedTask, query: str = None) -> Dict:
        """
        研究智能体 - 深度研究链
        
        继承 DeerFlow 研究能力：
        1. 问题分解
        2. 多源搜索
        3. 信息验证
        4. 综合分析
        5. 记忆沉淀
        """
        research_query = query or task.content
        
        # 1. 检查记忆中是否有相关研究
        existing = self.mflow.retrieve(research_query, layer="long", top_k=3)
        
        # 2. 执行研究（简化版）
        # 实际应调用 DeerFlow 的研究链
        research_result = {
            "query": research_query,
            "sources": ["web_search", "memory"],
            "findings": f"研究发现: {research_query}",
            "existing_knowledge": existing
        }
        
        # 3. 存储研究结果到长期记忆
        self.auto_memory.extract_and_store_facts(
            research_result["findings"],
            "research"
        )
        
        return research_result
    
    def _code_agent(self, task: UnifiedTask, code_request: str = None) -> Dict:
        """
        代码智能体 - 代码生成与执行
        
        功能：
        1. 代码生成
        2. 代码审查
        3. 执行监控
        4. 错误处理
        """
        request = code_request or task.content
        
        # 检索相关代码记忆
        code_memories = self.mflow.retrieve(request, layer="skill", top_k=3)
        
        return {
            "request": request,
            "context": code_memories,
            "generated_code": "# 代码生成结果",
            "execution_result": None
        }
    
    def _browser_agent(self, task: UnifiedTask, url: str = None) -> Dict:
        """
        浏览器智能体 - 网页浏览与数据提取
        
        功能：
        1. 网页导航
        2. 内容提取
        3. 数据结构化
        4. 截图存档
        """
        return {
            "url": url,
            "extracted_content": None,
            "screenshot": None
        }
    
    def _memory_agent(self, task: UnifiedTask, operation: str = "retrieve") -> Dict:
        """
        记忆智能体 - 记忆管理与优化
        
        功能：
        1. 记忆检索
        2. 记忆整合
        3. 记忆清理
        4. 记忆同步
        """
        if operation == "retrieve":
            results = self.mflow.retrieve(task.content, top_k=5)
            return {"operation": "retrieve", "results": results}
        
        elif operation == "consolidate":
            result = self.mflow.consolidate_memories("short")
            return {"operation": "consolidate", "result": result}
        
        elif operation == "sync":
            result = self.mflow.sync()
            return {"operation": "sync", "result": result}
        
        return {"operation": "unknown"}
    
    def _skill_agent(self, task: UnifiedTask, skill_name: str = None, skill_input: str = None) -> Dict:
        """
        Skill智能体 - Skills调用与管理
        
        功能：
        1. Skill选择
        2. 参数填充
        3. 调用执行
        4. 结果存储
        """
        # 记录Skill调用
        self.auto_memory.record_skill_call(
            skill_name or "unknown",
            skill_input or task.content,
            "Skill执行结果",
            success=True
        )
        
        return {
            "skill": skill_name,
            "input": skill_input,
            "output": None,
            "status": "called"
        }
    
    def _analyze_intent(self, content: str) -> Dict:
        """分析用户意图"""
        # 关键词映射
        intent_patterns = {
            TaskType.RESEARCH: ["研究", "调查", "分析", "查询", "搜索", "research", "study"],
            TaskType.CODE: ["代码", "编程", "写", "生成", "code", "program"],
            TaskType.ANALYSIS: ["分析", "评估", "计算", "analyze", "evaluate"],
            TaskType.CREATIVE: ["创建", "设计", "写", "create", "design", "write"],
            TaskType.MEMORY: ["记忆", "回忆", "同步", "memory", "sync"],
            TaskType.SKILL: ["skill", "技能", "使用", "调用"]
        }
        
        content_lower = content.lower()
        scores = {}
        
        for task_type, patterns in intent_patterns.items():
            score = sum(1 for p in patterns if p in content_lower)
            scores[task_type] = score
        
        # 选择最高分
        best_type = max(scores, key=scores.get)
        confidence = min(scores[best_type] / 2, 1.0)  # 归一化
        
        return {
            "type": best_type.value,
            "confidence": confidence,
            "all_scores": {k.value: v for k, v in scores.items()}
        }
    
    def _decompose_task(self, task: UnifiedTask, intent: Dict, memory_context: List) -> List[Dict]:
        """分解任务为子任务"""
        subtasks = []
        
        # 根据意图类型分解
        if intent["type"] == "research":
            subtasks = [
                {"agent": AgentType.MEMORY, "action": "check_existing"},
                {"agent": AgentType.RESEARCH, "action": "web_search"},
                {"agent": AgentType.RESEARCH, "action": "analyze"},
                {"agent": AgentType.MEMORY, "action": "store_findings"}
            ]
        elif intent["type"] == "code":
            subtasks = [
                {"agent": AgentType.MEMORY, "action": "retrieve_patterns"},
                {"agent": AgentType.CODE, "action": "generate"},
                {"agent": AgentType.CODE, "action": "review"},
                {"agent": AgentType.MEMORY, "action": "store_snippet"}
            ]
        elif intent["type"] == "skill":
            subtasks = [
                {"agent": AgentType.MEMORY, "action": "retrieve_skill_usage"},
                {"agent": AgentType.SKILL, "action": "execute"},
                {"agent": AgentType.MEMORY, "action": "record_usage"}
            ]
        else:
            # 默认流程
            subtasks = [
                {"agent": AgentType.MEMORY, "action": "retrieve_context"},
                {"agent": AgentType.LEAD, "action": "plan"},
                {"agent": AgentType.MEMORY, "action": "store_result"}
            ]
        
        return subtasks
    
    def execute(self, content: str, task_id: str = None) -> Dict:
        """
        执行统一任务
        
        Args:
            content: 用户输入
            task_id: 可选的任务ID
            
        Returns:
            执行结果
        """
        # 1. 创建任务
        task = UnifiedTask(
            id=task_id or hashlib.md5(f"{content}_{datetime.now()}".encode()).hexdigest()[:16],
            type=TaskType.ANALYSIS,  # 临时，会被 Lead Agent 更新
            content=content
        )
        
        with self._lock:
            self.active_tasks[task.id] = task
        
        # 2. 启动主控智能体
        lead_result = self._lead_agent(task)
        task.type = TaskType(lead_result["intent"]["type"])
        
        # 3. 执行子任务
        results = {"lead": lead_result}
        
        for subtask in lead_result["subtasks"]:
            agent_type = subtask["agent"]
            
            # 更新智能体状态
            task.agent_states[agent_type] = AgentState(
                agent_type=agent_type,
                status="running",
                current_task=subtask["action"]
            )
            
            # 执行智能体
            agent_func = self.agent_registry.get(agent_type)
            if agent_func:
                try:
                    result = agent_func(task)
                    results[agent_type.value] = result
                    task.agent_states[agent_type].status = "completed"
                except Exception as e:
                    task.agent_states[agent_type].status = "error"
                    results[agent_type.value] = {"error": str(e)}
            
            task.agent_states[agent_type].end_time = datetime.now()
        
        # 4. 整合结果
        task.result = self._integrate_results(results)
        task.completed_at = datetime.now()
        
        # 5. 存储任务记忆
        self._store_task_memory(task)
        
        return {
            "task_id": task.id,
            "intent": lead_result["intent"],
            "suggested_skills": lead_result["suggested_skills"],
            "memory_context": lead_result["memory_context"],
            "agent_results": results,
            "final_result": task.result
        }
    
    def _integrate_results(self, results: Dict) -> str:
        """整合各智能体结果"""
        parts = []
        
        if "research" in results:
            parts.append(f"研究发现: {results['research'].get('findings', '')}")
        
        if "code" in results:
            parts.append(f"代码结果: {results['code'].get('execution_result', '')}")
        
        if "skill" in results:
            parts.append(f"Skill调用: {results['skill'].get('skill', '')}")
        
        return "\n".join(parts) if parts else "任务执行完成"
    
    def _store_task_memory(self, task: UnifiedTask):
        """存储任务记忆"""
        # 存储到即时记忆
        entry = MemoryEntry(
            id=f"task_{task.id}",
            layer="instant",
            content=f"""任务执行记录
ID: {task.id}
类型: {task.type.value}
内容: {task.content[:200]}
结果: {str(task.result)[:200]}
智能体: {[a.value for a in task.agent_states.keys()]}
耗时: {(task.completed_at - task.created_at).total_seconds() if task.completed_at else 0}s""",
            source="unified_core",
            timestamp=datetime.now(),
            importance=7.0,
            metadata={
                "task_id": task.id,
                "task_type": task.type.value,
                "agent_count": len(task.agent_states),
                "skill_count": len(task.skill_calls)
            }
        )
        
        self.mflow.store(entry)
        
        # 提取重要事实到长期记忆
        if task.result:
            self.auto_memory.extract_and_store_facts(
                str(task.result),
                "general"
            )
    
    def get_task_status(self, task_id: str) -> Optional[Dict]:
        """获取任务状态"""
        task = self.active_tasks.get(task_id)
        if not task:
            return None
        
        return {
            "id": task.id,
            "type": task.type.value,
            "status": "completed" if task.completed_at else "running",
            "agents": {k.value: v.status for k, v in task.agent_states.items()},
            "created_at": task.created_at.isoformat(),
            "completed_at": task.completed_at.isoformat() if task.completed_at else None
        }
    
    def get_system_status(self) -> Dict:
        """获取系统状态"""
        memory_stats = self.mflow.get_stats()
        
        return {
            "active_tasks": len(self.active_tasks),
            "registered_agents": len(self.agent_registry),
            "memory_stats": memory_stats,
            "status": "running"
        }

# 便捷函数
def unified_execute(content: str) -> Dict:
    """便捷函数：执行统一任务"""
    core = UnifiedCore()
    return core.execute(content)

def get_relevant_skills(query: str) -> List[str]:
    """便捷函数：获取相关Skills"""
    core = UnifiedCore()
    return core.auto_memory.suggest_skills(query)

def get_memory_context(query: str) -> List[Dict]:
    """便捷函数：获取记忆上下文"""
    core = UnifiedCore()
    return core.mflow.retrieve(query, top_k=5)

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="OClaw-Hermes 统一核心")
    parser.add_argument("command", choices=["execute", "status", "skills", "memory"])
    parser.add_argument("--content", "-c", help="输入内容")
    parser.add_argument("--query", "-q", help="查询")
    parser.add_argument("--task-id", help="任务ID")
    
    args = parser.parse_args()
    
    core = UnifiedCore()
    
    if args.command == "execute":
        result = core.execute(args.content)
        print(json.dumps(result, ensure_ascii=False, indent=2, default=str))
    
    elif args.command == "status":
        if args.task_id:
            status = core.get_task_status(args.task_id)
        else:
            status = core.get_system_status()
        print(json.dumps(status, ensure_ascii=False, indent=2, default=str))
    
    elif args.command == "skills":
        skills = core.auto_memory.suggest_skills(args.query)
        print(json.dumps({"suggested_skills": skills}, ensure_ascii=False))
    
    elif args.command == "memory":
        memories = core.mflow.retrieve(args.query, top_k=5)
        print(json.dumps(memories, ensure_ascii=False, indent=2))
