"""
openclaw_bridge.py - OpenClaw 主会话桥接层

将 Orchestrator V4 的规划能力与 OpenClaw 主会话的 sessions_spawn 能力桥接起来。

设计思路：
- Orchestrator 负责：扫描、规划、拆分、超时计算
- 主会话负责：spawn、yield、收集、汇总
- Bridge 负责：协调两者，提供统一入口

使用方式：
    from openclaw_bridge import run_orchestrated_task
    
    result = await run_orchestrated_task(
        task="分析这个项目的架构",
        target_dir="/path/to/project",
        sessions_spawn_func=sessions_spawn,  # 主会话的 spawn 函数
        max_parallel=5,  # 最多同时派发 5 个
    )
"""

import asyncio
import sys
import time
from pathlib import Path
from typing import Any, Awaitable, Callable, Dict, List, Optional

# 导入 orchestrator
sys.path.insert(0, str(Path(__file__).parent))
from orchestrator_v4_acp import OrchestratorV4ACP, OrchestratorConfig


class OpenClawBridge:
    """OpenClaw 主会话桥接器"""
    
    def __init__(
        self,
        sessions_spawn_func: Callable[..., Awaitable[Any]],
        config: Optional[OrchestratorConfig] = None,
    ):
        """
        Args:
            sessions_spawn_func: 主会话的 sessions_spawn 函数引用
            config: Orchestrator 配置（可选）
        """
        self.spawn_func = sessions_spawn_func
        self.config = config or OrchestratorConfig(resume_from_latest_checkpoint=False)
        self.orch = OrchestratorV4ACP(self.config)
        self._spawned_tasks: Dict[str, Dict] = {}
    
    async def plan_and_spawn(
        self,
        task: str,
        target_dir: Optional[str] = None,
        max_parallel: int = 5,
        auto_spawn: bool = True,
    ) -> Dict[str, Any]:
        """
        规划任务并派发子代理
        
        Args:
            task: 用户任务描述
            target_dir: 目标目录（如果任务涉及文件系统）
            max_parallel: 最多同时派发多少个子任务
            auto_spawn: 是否自动派发（False 则只规划不派发）
        
        Returns:
            {
                "plan": {...},  # 完整规划结果
                "spawned": [...],  # 已派发的子任务列表
                "pending": [...],  # 待派发的子任务列表
                "summary": "...",  # 摘要信息
            }
        """
        # 1. 扫描（如果有目标目录）
        scan_result = None
        if target_dir:
            scan_result = self.orch.scan_task_scope(task, target_dir=target_dir)
        
        # 2. 规划
        context = {"target_dir": target_dir} if target_dir else None
        plan = self.orch.plan_complex_task(task, context=context)
        
        # 3. 派发（如果 auto_spawn=True）
        spawned = []
        pending = []
        
        if auto_spawn:
            subtasks = plan["subtasks"]
            to_spawn = subtasks[:max_parallel]
            pending = subtasks[max_parallel:]
            
            for st in to_spawn:
                try:
                    result = await self._spawn_subtask(st, task)
                    spawned.append({
                        "subtask_id": st["id"],
                        "module_key": st.get("module_key", "N/A"),
                        "session_key": result.get("childSessionKey", ""),
                        "status": "spawned",
                        "spawned_at": time.time(),
                    })
                except Exception as e:
                    spawned.append({
                        "subtask_id": st["id"],
                        "module_key": st.get("module_key", "N/A"),
                        "session_key": "",
                        "status": "failed",
                        "error": str(e),
                    })
        else:
            pending = plan["subtasks"]
        
        # 4. 生成摘要
        summary_parts = []
        if scan_result:
            summary_parts.append(scan_result.get("scan_note", ""))
        summary_parts.append(plan.get("notes", ""))
        if spawned:
            summary_parts.append(f"已派发 {len(spawned)} 个子任务")
        if pending:
            summary_parts.append(f"待派发 {len(pending)} 个子任务")
        
        return {
            "plan": plan,
            "scan": scan_result,
            "spawned": spawned,
            "pending": pending,
            "summary": "；".join(summary_parts),
        }
    
    async def _spawn_subtask(self, subtask: Dict, parent_task: str) -> Dict:
        """派发单个子任务"""
        module_key = subtask.get("module_key", subtask["id"])
        label = f"orch-{module_key}"
        
        # 使用 orchestrator 计算的超时
        timeout = subtask.get("estimated_time_sec", 300)
        
        # 使用 orchestrator 生成的 description（已包含文件读取约束）
        task_prompt = subtask["description"]
        
        result = await self.spawn_func(
            runtime="subagent",
            agentId="main",
            label=label,
            mode="run",
            task=task_prompt,
            timeoutSeconds=timeout,
            runTimeoutSeconds=timeout,
            cleanup="delete",
        )
        
        # 记录到追踪器
        self._spawned_tasks[label] = {
            "subtask": subtask,
            "result": result,
            "spawned_at": time.time(),
        }
        
        return result
    
    def get_spawned_tasks(self) -> Dict[str, Dict]:
        """获取已派发的任务列表"""
        return self._spawned_tasks.copy()
    
    async def spawn_next_batch(
        self,
        plan: Dict,
        already_spawned: int,
        batch_size: int = 5,
    ) -> List[Dict]:
        """
        派发下一批子任务
        
        Args:
            plan: 之前的规划结果
            already_spawned: 已派发的数量
            batch_size: 本批次派发数量
        
        Returns:
            本批次派发结果列表
        """
        subtasks = plan["subtasks"]
        next_batch = subtasks[already_spawned:already_spawned + batch_size]
        
        spawned = []
        for st in next_batch:
            try:
                result = await self._spawn_subtask(st, "")
                spawned.append({
                    "subtask_id": st["id"],
                    "module_key": st.get("module_key", "N/A"),
                    "session_key": result.get("childSessionKey", ""),
                    "status": "spawned",
                    "spawned_at": time.time(),
                })
            except Exception as e:
                spawned.append({
                    "subtask_id": st["id"],
                    "module_key": st.get("module_key", "N/A"),
                    "session_key": "",
                    "status": "failed",
                    "error": str(e),
                })
        
        return spawned


# ========== 便捷函数 ==========

async def run_orchestrated_task(
    task: str,
    target_dir: Optional[str] = None,
    sessions_spawn_func: Optional[Callable] = None,
    max_parallel: int = 5,
    config: Optional[OrchestratorConfig] = None,
) -> Dict[str, Any]:
    """
    一键运行编排任务（规划 + 派发）
    
    Args:
        task: 用户任务描述
        target_dir: 目标目录
        sessions_spawn_func: 主会话的 sessions_spawn 函数
        max_parallel: 最多同时派发多少个
        config: Orchestrator 配置
    
    Returns:
        {
            "plan": {...},
            "spawned": [...],
            "pending": [...],
            "summary": "...",
        }
    
    使用示例：
        result = await run_orchestrated_task(
            task="分析这个项目的架构",
            target_dir="/path/to/project",
            sessions_spawn_func=sessions_spawn,
            max_parallel=5,
        )
        
        print(result["summary"])
        # 然后主会话 sessions_yield 等待子任务完成
    """
    if not sessions_spawn_func:
        raise ValueError("必须提供 sessions_spawn_func 参数")
    
    bridge = OpenClawBridge(sessions_spawn_func, config)
    return await bridge.plan_and_spawn(
        task=task,
        target_dir=target_dir,
        max_parallel=max_parallel,
        auto_spawn=True,
    )


async def plan_only(
    task: str,
    target_dir: Optional[str] = None,
    config: Optional[OrchestratorConfig] = None,
) -> Dict[str, Any]:
    """
    只规划不派发（用于预览）
    
    Returns:
        {
            "plan": {...},
            "scan": {...},
            "summary": "...",
        }
    """
    # 创建一个 dummy spawn func
    async def dummy_spawn(**kwargs):
        return {"status": "dummy"}
    
    bridge = OpenClawBridge(dummy_spawn, config)
    return await bridge.plan_and_spawn(
        task=task,
        target_dir=target_dir,
        max_parallel=0,
        auto_spawn=False,
    )
