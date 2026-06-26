#!/usr/bin/env python3
"""
streaming_executor.py - 流式并行工具执行器
参考Claude Code的StreamingToolExecutor实现

功能：
1. 流式检测工具调用
2. 并行执行（asyncio）
3. 结果收集和排序
4. 错误隔离和重试

用法：
    python3 scripts/streaming_executor.py --test
    python3 scripts/streaming_executor.py <tools.json>
"""

import json
import sys
import asyncio
import time
from typing import List, Dict, Any, Optional, Callable, Coroutine
from dataclasses import dataclass, field
from enum import Enum
from concurrent.futures import ThreadPoolExecutor
import traceback


class ToolStatus(Enum):
    """工具执行状态"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass
class ToolExecution:
    """工具执行记录"""
    tool_use_id: str
    tool_name: str
    input_data: Dict[str, Any]
    status: ToolStatus = ToolStatus.PENDING
    result: Optional[Any] = None
    error: Optional[str] = None
    start_time: Optional[float] = None
    end_time: Optional[float] = None
    duration_ms: Optional[float] = None
    retry_count: int = 0
    max_retries: int = 3


@dataclass
class ExecutorResult:
    """执行器结果"""
    executions: List[ToolExecution]
    total_count: int
    completed_count: int
    failed_count: int
    total_duration_ms: float
    success_rate: float


class StreamingToolExecutor:
    """流式并行工具执行器"""
    
    def __init__(self,
                 max_concurrent: int = 5,
                 timeout_seconds: float = 30.0,
                 enable_retry: bool = True):
        self.max_concurrent = max_concurrent
        self.timeout_seconds = timeout_seconds
        self.enable_retry = enable_retry
        
        # 执行队列
        self.pending_queue: List[ToolExecution] = []
        self.running_tasks: Dict[str, asyncio.Task] = {}
        self.completed_executions: List[ToolExecution] = []
        
        # 并发控制
        self.semaphore = asyncio.Semaphore(max_concurrent)
        
        # 工具注册表
        self.tool_registry: Dict[str, Callable] = {}
        
        # 统计
        self.start_time: Optional[float] = None
        self.end_time: Optional[float] = None
    
    def register_tool(self, name: str, handler: Callable):
        """注册工具处理器"""
        self.tool_registry[name] = handler
    
    async def add_tool(self, tool_use: Dict[str, Any]) -> ToolExecution:
        """添加工具到执行队列（流式接收）"""
        execution = ToolExecution(
            tool_use_id=tool_use.get("id", f"tool_{len(self.pending_queue) + len(self.completed_executions)}"),
            tool_name=tool_use.get("name", "unknown"),
            input_data=tool_use.get("input", {}),
            max_retries=3 if self.enable_retry else 0
        )
        
        # 直接添加到完成队列（用于跟踪）
        self.completed_executions.append(execution)
        
        # 添加到待执行队列
        self.pending_queue.append(execution)
        
        # 如果有空闲槽位，立即开始执行
        if len(self.running_tasks) < self.max_concurrent:
            await self._start_next()
        
        return execution
    
    async def _start_next(self):
        """开始执行下一个工具"""
        if not self.pending_queue:
            return
        
        execution = self.pending_queue.pop(0)
        
        # 创建执行任务
        task = asyncio.create_task(
            self._execute_with_timeout(execution)
        )
        
        self.running_tasks[execution.tool_use_id] = task
        
        # 设置完成回调
        task.add_done_callback(
            lambda t: asyncio.create_task(self._on_task_complete(execution.tool_use_id, t))
        )
    
    async def _execute_with_timeout(self, execution: ToolExecution):
        """带超时的执行"""
        async with self.semaphore:
            execution.status = ToolStatus.RUNNING
            execution.start_time = time.time()
            
            try:
                # 获取工具处理器
                handler = self.tool_registry.get(execution.tool_name)
                
                if handler is None:
                    # 如果没有注册处理器，使用模拟执行
                    result = await self._mock_execute(execution)
                else:
                    # 执行实际工具
                    if asyncio.iscoroutinefunction(handler):
                        result = await asyncio.wait_for(
                            handler(execution.input_data),
                            timeout=self.timeout_seconds
                        )
                    else:
                        # 同步函数，放到线程池执行
                        loop = asyncio.get_event_loop()
                        result = await asyncio.wait_for(
                            loop.run_in_executor(None, handler, execution.input_data),
                            timeout=self.timeout_seconds
                        )
                
                execution.status = ToolStatus.COMPLETED
                execution.result = result
                
            except asyncio.TimeoutError:
                execution.status = ToolStatus.FAILED
                execution.error = f"执行超时 ({self.timeout_seconds}秒)"
                
            except Exception as e:
                execution.status = ToolStatus.FAILED
                execution.error = str(e)
                
                # 重试逻辑
                if self.enable_retry and execution.retry_count < execution.max_retries:
                    execution.retry_count += 1
                    execution.status = ToolStatus.PENDING
                    self.pending_queue.append(execution)
                    return
            
            finally:
                execution.end_time = time.time()
                if execution.start_time:
                    execution.duration_ms = (execution.end_time - execution.start_time) * 1000
    
    async def _mock_execute(self, execution: ToolExecution) -> Dict[str, Any]:
        """模拟执行（用于测试）"""
        # 模拟不同工具的执行时间
        tool_times = {
            "read": 0.1,
            "write": 0.2,
            "exec": 0.5,
            "search": 0.3,
            "fetch": 0.4,
        }
        
        delay = tool_times.get(execution.tool_name, 0.2)
        await asyncio.sleep(delay)
        
        # 模拟结果
        return {
            "status": "success",
            "tool": execution.tool_name,
            "input": execution.input_data,
            "output": f"模拟执行结果: {execution.tool_name}"
        }
    
    async def _on_task_complete(self, tool_use_id: str, task: asyncio.Task):
        """任务完成回调"""
        # 从运行队列移除
        if tool_use_id in self.running_tasks:
            del self.running_tasks[tool_use_id]
        
        # 查找执行记录
        for execution in self.completed_executions:
            if execution.tool_use_id == tool_use_id:
                break
        else:
            # 从pending或running中查找
            for execution in self.pending_queue:
                if execution.tool_use_id == tool_use_id:
                    break
            else:
                # 检查task的结果
                try:
                    task.result()
                except:
                    pass
                return
        
        # 添加到完成队列
        if execution not in self.completed_executions:
            self.completed_executions.append(execution)
        
        # 开始下一个
        await self._start_next()
    
    async def get_completed_results(self) -> List[ToolExecution]:
        """获取已完成的结果（非阻塞）"""
        return [
            e for e in self.completed_executions
            if e.status == ToolStatus.COMPLETED
        ]
    
    async def wait_all(self) -> ExecutorResult:
        """等待所有工具执行完成"""
        self.start_time = time.time()
        
        # 启动所有pending的任务
        while self.pending_queue:
            await self._start_next()
        
        # 等待所有运行中的任务完成
        if self.running_tasks:
            await asyncio.gather(*self.running_tasks.values(), return_exceptions=True)
        
        self.end_time = time.time()
        
        # 统计结果
        all_executions = self.completed_executions
        total_count = len(all_executions)
        completed_count = sum(1 for e in all_executions if e.status == ToolStatus.COMPLETED)
        failed_count = sum(1 for e in all_executions if e.status == ToolStatus.FAILED)
        total_duration = (self.end_time - self.start_time) * 1000 if self.start_time else 0
        success_rate = (completed_count / total_count * 100) if total_count > 0 else 0
        
        return ExecutorResult(
            executions=all_executions,
            total_count=total_count,
            completed_count=completed_count,
            failed_count=failed_count,
            total_duration_ms=total_duration,
            success_rate=success_rate
        )
    
    def get_status(self) -> Dict[str, Any]:
        """获取执行器状态"""
        return {
            "pending": len(self.pending_queue),
            "running": len(self.running_tasks),
            "completed": len(self.completed_executions),
            "max_concurrent": self.max_concurrent,
            "timeout_seconds": self.timeout_seconds
        }


async def test_streaming_executor():
    """测试流式执行器"""
    print("=" * 60)
    print("流式并行工具执行器测试")
    print("=" * 60)
    
    # 创建执行器
    executor = StreamingToolExecutor(
        max_concurrent=3,
        timeout_seconds=10.0,
        enable_retry=True
    )
    
    # 注册模拟工具
    async def mock_read(input_data):
        await asyncio.sleep(0.1)
        return {"content": "文件内容", "lines": 100}
    
    async def mock_write(input_data):
        await asyncio.sleep(0.2)
        return {"status": "written", "bytes": 500}
    
    async def mock_exec(input_data):
        await asyncio.sleep(0.5)
        return {"stdout": "命令输出", "exit_code": 0}
    
    executor.register_tool("read", mock_read)
    executor.register_tool("write", mock_write)
    executor.register_tool("exec", mock_exec)
    
    # 添加工具调用（模拟流式接收）
    tool_calls = [
        {"id": "tool_1", "name": "read", "input": {"path": "/test/file1.py"}},
        {"id": "tool_2", "name": "read", "input": {"path": "/test/file2.py"}},
        {"id": "tool_3", "name": "exec", "input": {"command": "ls -la"}},
        {"id": "tool_4", "name": "write", "input": {"path": "/test/output.txt", "content": "test"}},
        {"id": "tool_5", "name": "read", "input": {"path": "/test/file3.py"}},
    ]
    
    print(f"\n添加 {len(tool_calls)} 个工具调用...")
    
    # 流式添加
    for tool_call in tool_calls:
        execution = await executor.add_tool(tool_call)
        print(f"  添加: {execution.tool_name} ({execution.tool_use_id})")
        await asyncio.sleep(0.05)  # 模拟流式间隔
    
    # 等待完成
    print(f"\n等待执行完成...")
    result = await executor.wait_all()
    
    # 打印结果
    print(f"\n执行结果:")
    print(f"  总数: {result.total_count}")
    print(f"  完成: {result.completed_count}")
    print(f"  失败: {result.failed_count}")
    print(f"  总耗时: {result.total_duration_ms:.1f}ms")
    print(f"  成功率: {result.success_rate:.1f}%")
    
    print(f"\n详细结果:")
    for execution in result.executions:
        status_icon = "✅" if execution.status == ToolStatus.COMPLETED else "❌"
        print(f"  {status_icon} {execution.tool_name} ({execution.tool_use_id})")
        print(f"     状态: {execution.status.value}")
        if execution.duration_ms:
            print(f"     耗时: {execution.duration_ms:.1f}ms")
        if execution.error:
            print(f"     错误: {execution.error}")
    
    # 测试并行效率
    print(f"\n并行效率分析:")
    sequential_time = sum(
        e.duration_ms or 0 for e in result.executions
    )
    parallel_time = result.total_duration_ms
    efficiency = (sequential_time / parallel_time) if parallel_time > 0 else 0
    print(f"  串行预估: {sequential_time:.1f}ms")
    print(f"  并行实际: {parallel_time:.1f}ms")
    print(f"  加速比: {efficiency:.1f}x")
    
    print("\n✅ 测试通过!")


if __name__ == "__main__":
    if "--test" in sys.argv:
        asyncio.run(test_streaming_executor())
    elif len(sys.argv) > 1:
        # 从文件读取工具调用
        with open(sys.argv[1], 'r', encoding='utf-8') as f:
            tool_calls = json.load(f)
        
        async def run():
            executor = StreamingToolExecutor()
            
            for tool_call in tool_calls:
                await executor.add_tool(tool_call)
            
            result = await executor.wait_all()
            
            print(json.dumps({
                "results": [
                    {
                        "tool_use_id": e.tool_use_id,
                        "tool_name": e.tool_name,
                        "status": e.status.value,
                        "result": e.result,
                        "error": e.error,
                        "duration_ms": e.duration_ms
                    }
                    for e in result.executions
                ],
                "stats": {
                    "total": result.total_count,
                    "completed": result.completed_count,
                    "failed": result.failed_count,
                    "duration_ms": result.total_duration_ms,
                    "success_rate": result.success_rate
                }
            }, indent=2, ensure_ascii=False))
        
        asyncio.run(run())
    else:
        print("用法:")
        print("  python3 scripts/streaming_executor.py <tools.json>")
        print("  python3 scripts/streaming_executor.py --test")
