"""
Task Distributor - 任务分发器

功能：
- 管理目标工作区（Worker）注册
- 任务分发到目标工作区
- 收集并聚合结果
- 通知用户任务完成

使用方式：
    distributor = TaskDistributor("ws_main")
    
    # 分发任务到多个工作区
    results = await distributor.dispatch("查茅台股价", workers=["ws_finance", "ws_data"])
    
    # 或自动选择合适的工作区
    results = await distributor.dispatch("查股价", workers=["auto"])
"""

import asyncio
import json
import logging
import time
import uuid
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field, asdict

# 导入协议定义
import sys
from pathlib import Path
_project_root = Path(__file__).parent
sys.path.insert(0, str(_project_root))
from src.protocols.task_protocol import (
    TaskMessage, TaskStatus, MessageType, WorkerInfo
)
from src.core.audit_log import ImmutableAuditLog

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s'
)


@dataclass
class TaskResult:
    """任务执行结果"""
    task_id: str
    worker_ws: str
    worker_name: str
    status: str
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    started_at: float = 0
    completed_at: float = 0
    
    @property
    def duration_ms(self) -> float:
        return (self.completed_at - self.started_at) * 1000


@dataclass
class DispatchResult:
    """分发结果聚合"""
    task_id: str
    task_action: str
    total_workers: int
    results: List[TaskResult] = field(default_factory=list)
    completed_count: int = 0
    failed_count: int = 0
    started_at: float = 0
    completed_at: float = 0
    
    @property
    def is_all_completed(self) -> bool:
        return self.completed_count + self.failed_count >= self.total_workers
    
    @property
    def aggregated_result(self) -> Dict[str, Any]:
        """聚合所有结果"""
        if self.failed_count == self.total_workers:
            return {"error": "所有工作区执行失败"}
        
        # 收集所有非错误结果
        valid_results = [r.result for r in self.results if r.result]
        
        if not valid_results:
            return {"error": "无有效结果"}
        
        # 如果只有一个，直接返回
        if len(valid_results) == 1:
            return valid_results[0]
        
        # 多个结果，聚合
        return {
            "count": len(valid_results),
            "results": valid_results,
            "summary": f"完成于 {self.completed_count}/{self.total_workers} 个工作区"
        }


class WorkerRegistry:
    """工作区注册表"""
    
    def __init__(self):
        self._workers: Dict[str, WorkerInfo] = {}
    
    def register(self, worker: WorkerInfo):
        """注册工作区"""
        self._workers[worker.ws_id] = worker
        logger.info(f"[REG] 注册工作区: {worker.ws_id} ({worker.ws_name})")
    
    def unregister(self, ws_id: str):
        """注销工作区"""
        if ws_id in self._workers:
            del self._workers[ws_id]
            logger.info(f"[DEL] 注销工作区: {ws_id}")
    
    def get(self, ws_id: str) -> Optional[WorkerInfo]:
        """获取工作区信息"""
        return self._workers.get(ws_id)
    
    def list_all(self) -> List[WorkerInfo]:
        """列出所有工作区"""
        return list(self._workers.values())
    
    def find_by_capability(self, capability: str) -> List[WorkerInfo]:
        """按能力查找工作区"""
        return [
            w for w in self._workers.values()
            if capability in w.capabilities
        ]
    
    def update_heartbeat(self, ws_id: str):
        """更新心跳"""
        if ws_id in self._workers:
            self._workers[ws_id].last_heartbeat = time.time()


class TaskDistributor:
    """任务分发器"""
    
    def __init__(
        self,
        ws_id: str,
        ws_name: str = "主工作区",
        listen_host: str = "0.0.0.0",
        listen_port: int = 8766,
        audit_log_dir: str = ".pao/audit_logs"
    ):
        self.ws_id = ws_id
        self.ws_name = ws_name
        self.listen_host = listen_host
        self.listen_port = listen_port
        
        self.registry = WorkerRegistry()
        self._pending_results: Dict[str, asyncio.Future] = {}
        self._active_tasks: Dict[str, DispatchResult] = {}
        
        # 审计日志
        self.audit_log = ImmutableAuditLog(audit_log_dir)
        
        # 任务超时（秒）
        self.timeout = 300
    
    async def start(self):
        """启动分发器"""
        logger.info(f"[START] 启动 TaskDistributor: {self.ws_id}")
        logger.info(f"   监听: ws://{self.listen_host}:{self.listen_port}")
        
        # 可以启动一个简单的 HTTP 服务器接收回调
        # 这里先简化，不启动服务器
    
    async def dispatch(
        self,
        task_action: str,
        task_params: Dict[str, Any] = None,
        workers: List[str] = None,
        task_type: str = "auto",
        priority: int = 5
    ) -> DispatchResult:
        """
        分发任务到工作区
        
        参数:
            task_action: 任务动作描述
            task_params: 任务参数
            workers: 目标工作区列表，"auto" 表示自动选择
            task_type: 任务类型
            priority: 优先级
        
        返回:
            DispatchResult: 聚合结果
        """
        task_params = task_params or {}
        task_id = f"task_{uuid.uuid4().hex[:12]}"
        
        # 选择目标工作区
        target_workers = await self._select_workers(workers or ["auto"], task_type)
        
        if not target_workers:
            logger.warning("[WARN] 没有可用的工作区")
            return DispatchResult(
                task_id=task_id,
                task_action=task_action,
                total_workers=0,
                completed_at=time.time()
            )
        
        logger.info(f"[SEND] 分发任务 [{task_id}]: {task_action}")
        logger.info(f"   目标工作区: {[w.ws_id for w in target_workers]}")
        
        # 记录审计日志：任务分发
        self.audit_log.append(
            actor=self.ws_id,
            action="dispatch",
            target=task_id,
            result="pending",
            details={
                "task_action": task_action,
                "task_params": task_params,
                "workers": [w.ws_id for w in target_workers],
                "task_type": task_type,
                "priority": priority
            }
        )
        
        # 创建分发结果
        dispatch_result = DispatchResult(
            task_id=task_id,
            task_action=task_action,
            total_workers=len(target_workers),
            started_at=time.time()
        )
        self._active_tasks[task_id] = dispatch_result
        
        # 并行分发到所有工作区
        tasks = [
            self._send_to_worker(task_id, task_action, task_params, worker, task_type, priority)
            for worker in target_workers
        ]
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # 聚合结果
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                dispatch_result.results.append(TaskResult(
                    task_id=task_id,
                    worker_ws=target_workers[i].ws_id,
                    worker_name=target_workers[i].ws_name,
                    status="failed",
                    error=str(result)
                ))
                dispatch_result.failed_count += 1
            else:
                dispatch_result.results.append(result)
                if result.status == "completed":
                    dispatch_result.completed_count += 1
                else:
                    dispatch_result.failed_count += 1
        
        dispatch_result.completed_at = time.time()
        
        logger.info(f"[DONE] 任务完成 [{task_id}]: 成功 {dispatch_result.completed_count}, 失败 {dispatch_result.failed_count}")
        
        return dispatch_result
    
    async def _select_workers(
        self,
        worker_ids: List[str],
        task_type: str
    ) -> List[WorkerInfo]:
        """选择目标工作区（支持层级调度）"""
        if "auto" in worker_ids:
            # 自动选择：返回所有在线工作区
            all_workers = [w for w in self.registry.list_all() if w.status == "online"]
            
            # 根据任务类型决定调度策略
            if task_type in ("heavy", "compute_intensive", "analysis"):
                # 重任务：优先选择 T1 高性能设备，按评分排序
                sorted_workers = sorted(all_workers, key=lambda w: w.get_total_score(), reverse=True)
                logger.info(f"[SCHEDULE] 重任务调度，优先选择高性能设备: {[w.ws_id for w in sorted_workers]}")
                return sorted_workers
            else:
                # 普通任务：按在线顺序返回
                return all_workers

        # 指定工作区
        workers = []
        for ws_id in worker_ids:
            w = self.registry.get(ws_id)
            if w:
                workers.append(w)

        return workers
    
    async def _send_to_worker(
        self,
        task_id: str,
        task_action: str,
        task_params: Dict[str, Any],
        worker: WorkerInfo,
        task_type: str,
        priority: int
    ) -> TaskResult:
        """发送任务到单个工作区"""
        # 构建任务消息
        task_msg = {
            "msg_type": MessageType.TASK_REQUEST.value,
            "sender_ws": self.ws_id,
            "sender_name": self.ws_name,
            "recipient_ws": worker.ws_id,
            "recipient_name": worker.ws_name,
            "task_id": task_id,
            "task_type": task_type,
            "task_action": task_action,
            "task_params": task_params,
            "priority": priority,
            "callback_url": f"ws://{self.listen_host}:{self.listen_port}/callback"
        }
        
        logger.info(f"[SEND] 发送到 {worker.ws_id} ({worker.host}:{worker.port})")
        
        # 记录审计日志：发送到工作区
        self.audit_log.append(
            actor=self.ws_id,
            action="send",
            target=task_id,
            result="pending",
            details={
                "worker_id": worker.ws_id,
                "worker_name": worker.ws_name,
                "host": worker.host,
                "port": worker.port
            }
        )
        
        start_time = time.time()
        
        try:
            import httpx
            
            # 连接工作区
            url = f"http://{worker.host}:{worker.port}/task"
            
            async with httpx.AsyncClient() as client:
                resp = await client.post(url, json=task_msg, timeout=self.timeout)
                resp.raise_for_status()
                result = resp.json()
            
            completed_at = time.time()
            
            # 记录审计日志：任务完成
            self.audit_log.append(
                actor=worker.ws_id,
                action="result",
                target=task_id,
                result="success",
                details={
                    "duration_ms": (completed_at - start_time) * 1000,
                    "result_summary": str(result.get("result", ""))[:200]
                }
            )
            
            return TaskResult(
                task_id=task_id,
                worker_ws=worker.ws_id,
                worker_name=worker.ws_name,
                status=result.get("status", "completed"),
                result=result.get("result"),
                error=result.get("error"),
                started_at=start_time,
                completed_at=completed_at
            )
        
        except Exception as e:
            logger.error(f"[ERR] 发送到 {worker.ws_id} 失败: {e}")
            
            # 记录审计日志：任务失败
            self.audit_log.append(
                actor=worker.ws_id,
                action="error",
                target=task_id,
                result="failure",
                details={
                    "error": str(e),
                    "worker_id": worker.ws_id
                }
            )
            
            return TaskResult(
                task_id=task_id,
                worker_ws=worker.ws_id,
                worker_name=worker.ws_name,
                status="failed",
                error=str(e),
                started_at=start_time,
                completed_at=time.time()
            )
    
    def register_worker(self, worker: WorkerInfo):
        """手动注册工作区"""
        self.registry.register(worker)
    
    async def handle_callback(self, msg: Dict[str, Any]):
        """处理回调结果"""
        task_id = msg.get("task_id")
        
        if task_id in self._active_tasks:
            result = self._active_tasks[task_id]
            # 可以在这里更新状态
            pass
    
    def get_status(self) -> Dict[str, Any]:
        """获取分发器状态"""
        return {
            "ws_id": self.ws_id,
            "ws_name": self.ws_name,
            "workers": [
                {"ws_id": w.ws_id, "status": w.status, "capabilities": w.capabilities}
                for w in self.registry.list_all()
            ],
            "active_tasks": len(self._active_tasks)
        }


# ==================== 便捷调用 ====================

_distributor: Optional[TaskDistributor] = None


async def get_distributor() -> TaskDistributor:
    """获取全局分发器"""
    global _distributor
    if _distributor is None:
        _distributor = TaskDistributor("main")
        await _distributor.start()
    return _distributor


async def dispatch_task(
    action: str,
    params: Dict[str, Any] = None,
    workers: List[str] = None
) -> Dict[str, Any]:
    """
    便捷的任务分发函数
    
    示例:
        result = await dispatch_task("查股价", {"stock": "600519"})
        result = await dispatch_task("文件搜索", {"pattern": "*.py"}, workers=["ws_code"])
    """
    dist = await get_distributor()
    dispatch_result = await dist.dispatch(action, params, workers)
    return dispatch_result.aggregated_result


# ==================== 测试 ====================

async def demo():
    """演示"""
    print("=" * 60)
    print("Task Distributor 演示")
    print("=" * 60)
    
    # 创建分发器
    dist = TaskDistributor("ws_main", "主工作区")
    
    # 手动注册工作区（模拟）
    dist.register_worker(WorkerInfo(
        ws_id="ws_finance",
        ws_name="金融分析区",
        host="localhost",
        port=8765,
        status="online",
        capabilities=["data_query", "stock_analysis"]
    ))
    
    dist.register_worker(WorkerInfo(
        ws_id="ws_code",
        ws_name="代码分析区",
        host="localhost",
        port=8767,
        status="online",
        capabilities=["code_analysis", "file_search"]
    ))
    
    # 分发任务（这会失败因为没有真实的服务，但展示流程）
    print("\n📤 分发测试任务...")
    result = await dist.dispatch(
        "测试任务",
        {"message": "hello"},
        workers=["ws_finance"]
    )
    
    print(f"\n结果: {result.aggregated_result}")


if __name__ == "__main__":
    asyncio.run(demo())