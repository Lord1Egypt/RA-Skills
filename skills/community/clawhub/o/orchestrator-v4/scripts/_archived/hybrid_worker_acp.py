"""
hybrid_worker_acp.py - 使用 ACP (Agent Computing Platform) spawn 子 agent 作为 Worker

核心设计：
- Fast Worker → spawn 轻量级子 agent，快速响应
- Slow Worker → spawn 深度思考子 agent，详细分析
- 完全在 OpenClaw 生态内运行，无需外部 API key
"""

import asyncio
import json
import time
import uuid
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Callable, Any

# 导入 OpenClaw 的 sessions_spawn 功能
# 注意：实际运行时由 OpenClaw 运行时注入


class WorkerMode(Enum):
    """Worker 模式"""
    FAST = "fast"    # 快速模式
    SLOW = "slow"    # 深度模式
    AUTO = "auto"    # 自动选择


class TaskComplexity(Enum):
    """任务复杂度"""
    TRIVIAL = 1
    SIMPLE = 2
    MODERATE = 3
    COMPLEX = 4
    VERY_COMPLEX = 5


@dataclass
class ACPWorkerConfig:
    """ACP Worker 配置"""
    # Fast Worker 配置
    fast_timeout: float = 60.0        # 快速响应超时
    fast_model: str = "gpt-4o-mini"   # 轻量级模型
    
    # Slow Worker 配置
    slow_timeout: float = 300.0       # 深度思考超时
    slow_model: str = "gpt-4o"        # 强力模型
    
    # 自动选择阈值
    complexity_threshold: int = 3
    
    # 子 agent 标签
    fast_label_prefix: str = "fast-worker"
    slow_label_prefix: str = "slow-worker"


@dataclass
class TaskContext:
    """任务上下文"""
    task_id: str
    task_description: str
    task_type: str = "general"
    conversation_history: List[Dict] = field(default_factory=list)
    previous_results: List[Any] = field(default_factory=list)
    available_tools: List[str] = field(default_factory=list)
    file_context: Dict[str, str] = field(default_factory=dict)
    constraints: List[str] = field(default_factory=list)
    requirements: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


class PromptTemplate:
    """Prompt 模板"""
    
    FAST_SYSTEM_PROMPT = """你是一个快速、高效的 AI 助手，专注于快速响应。

核心原则：
1. 速度优先 - 快速给出足够好的答案
2. 简洁明了 - 直击要点
3. 简单问题用简单方案
4. 必要时才询问澄清

响应格式：
- 先给直接答案
- 简要解释（如需要）
- 代码示例（仅当相关）
"""

    SLOW_SYSTEM_PROMPT = """你是一个深入、全面的 AI 助手，专注于复杂问题解决。

核心原则：
1. 深入思考后再回答
2. 考虑边界情况和影响
3. 提供全面的解决方案
4. 解释你的思考过程

方法：
1. 从多角度分析问题
2. 考虑替代方案
3. 明确评估权衡
4. 提供逐步推理
5. 包含错误处理和边界情况

响应格式：
1. 问题理解
2. 解决方案思路
3. 详细实现
4. 测试考虑
5. 潜在问题和缓解措施
"""

    @staticmethod
    def build_fast_prompt(task: str, context: TaskContext) -> str:
        """构建 Fast Worker Prompt"""
        parts = [PromptTemplate.FAST_SYSTEM_PROMPT]
        parts.append(f"\n任务：{task}\n")
        
        if context.requirements:
            parts.append("要求：")
            for r in context.requirements:
                parts.append(f"- {r}")
        
        if context.conversation_history:
            parts.append("\n历史对话：")
            for msg in context.conversation_history[-3:]:
                role = msg.get("role", "unknown")
                content = msg.get("content", "")[:200]
                parts.append(f"{role}: {content}")
        
        return "\n".join(parts)
    
    @staticmethod
    def build_slow_prompt(task: str, context: TaskContext) -> str:
        """构建 Slow Worker Prompt"""
        parts = [PromptTemplate.SLOW_SYSTEM_PROMPT]
        parts.append(f"\n任务：{task}\n")
        
        if context.requirements:
            parts.append("\n要求：")
            for r in context.requirements:
                parts.append(f"- {r}")
        
        if context.constraints:
            parts.append("\n约束：")
            for c in context.constraints:
                parts.append(f"- {c}")
        
        if context.available_tools:
            parts.append("\n可用工具：")
            for t in context.available_tools:
                parts.append(f"- {t}")
        
        if context.conversation_history:
            parts.append("\n历史对话：")
            for msg in context.conversation_history[-5:]:
                role = msg.get("role", "unknown")
                content = msg.get("content", "")[:300]
                parts.append(f"{role}: {content}")
        
        if context.file_context:
            parts.append("\n相关文件：")
            for path, content in list(context.file_context.items())[:3]:
                parts.append(f"\n{path}:\n{content[:500]}")
        
        return "\n".join(parts)


class HybridWorkerACP:
    """
    混合 Worker - ACP 版本
    
    使用 OpenClaw 的 sessions_spawn 来 spawn 子 agent 作为 Worker
    """
    
    def __init__(self, config: Optional[ACPWorkerConfig] = None):
        self.config = config or ACPWorkerConfig()
        self.template = PromptTemplate()
        
        # 统计
        self._stats = {
            "fast_calls": 0,
            "slow_calls": 0,
            "auto_switches": 0,
            "total_duration": 0.0
        }
    
    async def process(
        self,
        task: str,
        context: Optional[TaskContext] = None,
        mode: Optional[WorkerMode] = None
    ) -> Dict[str, Any]:
        """
        处理任务
        
        Args:
            task: 任务描述
            context: 任务上下文
            mode: 强制指定模式，None 则自动选择
        
        Returns:
            包含结果、使用的模式、耗时等信息的字典
        """
        ctx = context or TaskContext(
            task_id=str(uuid.uuid4())[:8],
            task_description=task
        )
        
        # 确定模式
        if mode is None or mode == WorkerMode.AUTO:
            mode, complexity = self._select_mode(task, ctx)
        else:
            complexity = TaskComplexity.MODERATE
        
        start_time = time.time()
        
        # 根据模式 spawn 不同的子 agent
        if mode == WorkerMode.FAST:
            result = await self._spawn_fast_worker(task, ctx)
            self._stats["fast_calls"] += 1
        else:
            result = await self._spawn_slow_worker(task, ctx)
            self._stats["slow_calls"] += 1
        
        duration = time.time() - start_time
        self._stats["total_duration"] += duration
        
        return {
            "result": result,
            "mode": mode.value,
            "complexity": complexity.value if isinstance(complexity, TaskComplexity) else complexity,
            "duration_sec": duration,
            "stats": self._stats.copy()
        }
    
    def _select_mode(self, task: str, context: TaskContext) -> tuple[WorkerMode, TaskComplexity]:
        """自动选择模式"""
        complexity_indicators = {
            TaskComplexity.TRIVIAL: [
                "简单", "快速", "简要", "一句话", "是/否",
                "simple", "quick", "brief", "yes/no"
            ],
            TaskComplexity.SIMPLE: [
                "解释", "什么是", "如何", "例子",
                "explain", "what is", "how to", "example"
            ],
            TaskComplexity.COMPLEX: [
                "设计", "架构", "优化", "重构", "分析",
                "design", "architecture", "optimize", "refactor", "analyze"
            ],
            TaskComplexity.VERY_COMPLEX: [
                "系统", "完整", "全面", "详细", "深入研究",
                "system", "complete", "comprehensive", "detailed", "research"
            ]
        }
        
        task_lower = task.lower()
        complexity = TaskComplexity.MODERATE
        
        for comp, indicators in complexity_indicators.items():
            if any(ind in task_lower for ind in indicators):
                complexity = comp
                break
        
        # 根据长度判断
        if len(task) < 50:
            complexity = min(complexity, TaskComplexity.SIMPLE, key=lambda x: x.value)
        elif len(task) > 500:
            complexity = max(complexity, TaskComplexity.COMPLEX, key=lambda x: x.value)
        
        # 根据阈值选择模式
        if complexity.value >= self.config.complexity_threshold:
            return WorkerMode.SLOW, complexity
        else:
            return WorkerMode.FAST, complexity
    
    async def _spawn_fast_worker(self, task: str, context: TaskContext) -> str:
        """Spawn Fast Worker 子 agent"""
        prompt = self.template.build_fast_prompt(task, context)
        label = f"{self.config.fast_label_prefix}-{context.task_id}"
        
        # 构造子 agent 任务
        agent_task = f"""{prompt}

请快速回答上述问题，保持简洁。"""
        
        # 使用 sessions_spawn 创建子 agent
        # 注意：这里使用 OpenClaw 的 sessions_spawn 工具
        return await self._call_acp(agent_task, label, self.config.fast_timeout)
    
    async def _spawn_slow_worker(self, task: str, context: TaskContext) -> str:
        """Spawn Slow Worker 子 agent"""
        prompt = self.template.build_slow_prompt(task, context)
        label = f"{self.config.slow_label_prefix}-{context.task_id}"
        
        # 构造子 agent 任务
        agent_task = f"""{prompt}

请深入分析并全面回答上述问题。"""
        
        # 使用 sessions_spawn 创建子 agent
        return await self._call_acp(agent_task, label, self.config.slow_timeout)
    
    async def _call_acp(self, task: str, label: str, timeout: float) -> str:
        """
        调用 ACP spawn 子 agent
        
        注意：这是一个模板，实际调用需要 OpenClaw 运行时环境
        在 skill 中使用时，由 OpenClaw 注入实际的 sessions_spawn 功能
        """
        # 实际实现应该类似：
        # session = await sessions_spawn(
        #     task=task,
        #     label=label,
        #     timeoutSeconds=int(timeout),
        #     mode="run"
        # )
        # return session.result
        
        # 这里返回模拟结果，实际使用时替换为真实调用
        return f"[ACP Worker Response for {label}]\nTask: {task[:100]}..."
    
    @property
    def stats(self) -> Dict:
        """获取统计"""
        return self._stats.copy()
    
    def reset_stats(self):
        """重置统计"""
        self._stats = {
            "fast_calls": 0,
            "slow_calls": 0,
            "auto_switches": 0,
            "total_duration": 0.0
        }


# ========== 便捷函数 ==========

async def quick_task(task: str, **kwargs) -> Dict[str, Any]:
    """快速处理任务（Fast 模式）"""
    worker = HybridWorkerACP(ACPWorkerConfig())
    return await worker.process(task, mode=WorkerMode.FAST, **kwargs)


async def deep_task(task: str, **kwargs) -> Dict[str, Any]:
    """深度处理任务（Slow 模式）"""
    worker = HybridWorkerACP(ACPWorkerConfig())
    return await worker.process(task, mode=WorkerMode.SLOW, **kwargs)


async def auto_task(task: str, **kwargs) -> Dict[str, Any]:
    """自动选择模式处理任务"""
    worker = HybridWorkerACP(ACPWorkerConfig())
    return await worker.process(task, mode=WorkerMode.AUTO, **kwargs)


# ========== 测试 ==========

if __name__ == "__main__":
    async def test():
        worker = HybridWorkerACP()
        
        print("=== Fast Mode ===")
        result = await worker.process("What is Python?", mode=WorkerMode.FAST)
        print(f"Mode: {result['mode']}, Duration: {result['duration_sec']:.2f}s")
        
        print("\n=== Slow Mode ===")
        result = await worker.process("Design a distributed system", mode=WorkerMode.SLOW)
        print(f"Mode: {result['mode']}, Duration: {result['duration_sec']:.2f}s")
        
        print("\n=== Auto Mode ===")
        result = await worker.process("Say hello")
        print(f"Selected mode: {result['mode']} for 'Say hello'")
        
        result = await worker.process("Design a complete microservices architecture")
        print(f"Selected mode: {result['mode']} for complex task")
        
        print("\n=== Stats ===")
        print(worker.stats)
    
    asyncio.run(test())
