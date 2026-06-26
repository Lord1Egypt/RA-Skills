#!/usr/bin/env python3
"""
Long Task Manager - 长时间任务处理框架
版本: v1.0
作者: BI Alpha
"""

import json
import os
import time
import uuid
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Callable
from dataclasses import dataclass, asdict
from enum import Enum


class TaskStatus(Enum):
    """任务状态"""
    PENDING = "pending"      # 等待执行
    RUNNING = "running"      # 执行中
    COMPLETED = "completed"  # 已完成
    FAILED = "failed"        # 失败
    CANCELLED = "cancelled"  # 已取消


@dataclass
class TaskConfig:
    """任务配置"""
    name: str
    type: str
    total_items: int
    params: Dict = None
    estimated_time: Optional[int] = None
    
    def __post_init__(self):
        if self.params is None:
            self.params = {}


@dataclass
class TaskStatusInfo:
    """任务状态信息"""
    task_id: str
    status: str
    progress: str = "0%"
    current_item: str = ""
    completed: int = 0
    total: int = 0
    detail: str = ""
    started_at: Optional[str] = None
    updated_at: Optional[str] = None
    error: Optional[str] = None
    detail: str = ""
    started_at: Optional[str] = None
    updated_at: Optional[str] = None
    error: Optional[str] = None


@dataclass
class TaskResult:
    """任务结果"""
    task_id: str
    status: str
    files: List[str] = None
    summary: str = ""
    elapsed_time: int = 0
    completed_at: Optional[str] = None
    
    def __post_init__(self):
        if self.files is None:
            self.files = []


class LongTaskManager:
    """
    长时间任务管理器
    
    功能:
    - 提交长时间任务
    - 实时进度追踪
    - 任务取消
    - 结果获取
    """
    
    def __init__(
        self,
        task_dir: str = "/tmp/long_tasks",
        max_concurrent: int = 5,
        default_timeout: Optional[int] = None
    ):
        """
        初始化管理器
        
        Args:
            task_dir: 任务存储目录
            max_concurrent: 最大并发任务数
            default_timeout: 默认超时(秒), None=无限制
        """
        self.task_dir = Path(task_dir)
        self.task_dir.mkdir(parents=True, exist_ok=True)
        self.max_concurrent = max_concurrent
        self.default_timeout = default_timeout
        
        # 运行时状态
        self._running_tasks: Dict[str, dict] = {}
        self._progress_callbacks: Dict[str, Callable] = {}
        
    def _get_task_path(self, task_id: str) -> Path:
        """获取任务目录"""
        return self.task_dir / task_id
    
    def _get_config_path(self, task_id: str) -> Path:
        """获取配置文件路径"""
        return self._get_task_path(task_id) / "config.json"
    
    def _get_status_path(self, task_id: str) -> Path:
        """获取状态文件路径"""
        return self._get_task_path(task_id) / "status.json"
    
    def _get_result_path(self, task_id: str) -> Path:
        """获取结果文件路径"""
        return self._get_task_path(task_id) / "result.json"
    
    def _generate_task_id(self, agent_id: str) -> str:
        """生成任务ID"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        random_suffix = uuid.uuid4().hex[:8]
        return f"{agent_id}_{timestamp}_{random_suffix}"
    
    def submit(
        self,
        agent_id: str,
        task_config: Dict,
        priority: str = "normal"
    ) -> str:
        """
        提交长时间任务
        
        Args:
            agent_id: 执行Agent ID
            task_config: 任务配置
            priority: 优先级 (high/normal/low)
            
        Returns:
            task_id: 任务ID
        """
        # 生成任务ID
        task_id = self._generate_task_id(agent_id)
        task_path = self._get_task_path(task_id)
        task_path.mkdir(parents=True, exist_ok=True)
        
        # 保存配置
        config = {
            "task_id": task_id,
            "agent_id": agent_id,
            "priority": priority,
            "config": task_config,
            "submitted_at": datetime.now().isoformat(),
            "status": TaskStatus.PENDING.value
        }
        
        with open(self._get_config_path(task_id), 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        
        # 初始化状态
        status = TaskStatusInfo(
            task_id=task_id,
            status=TaskStatus.PENDING.value,
            progress="0%",
            current_item="初始化",
            completed=0,
            total=task_config.get('total_items', 0),
            detail="任务已提交，等待执行"
        )
        
        self._save_status(status)
        
        print(f"✅ 任务已提交: {task_id}")
        print(f"   名称: {task_config.get('name', 'Unknown')}")
        print(f"   Agent: {agent_id}")
        print(f"   工作量: {task_config.get('total_items', 0)} 项")
        
        return task_id
    
    def _save_status(self, status: TaskStatus):
        """保存状态到文件"""
        status.updated_at = datetime.now().isoformat()
        
        with open(self._get_status_path(status.task_id), 'w', encoding='utf-8') as f:
            json.dump(asdict(status), f, indent=2, ensure_ascii=False)
    
    def get_status(self, task_id: str) -> Optional[Dict]:
        """
        获取任务状态
        
        Args:
            task_id: 任务ID
            
        Returns:
            状态字典，不存在返回None
        """
        status_path = self._get_status_path(task_id)
        
        if not status_path.exists():
            return None
        
        with open(status_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def get_result(self, task_id: str) -> Optional[Dict]:
        """
        获取任务结果
        
        Args:
            task_id: 任务ID
            
        Returns:
            结果字典，未完成返回None
        """
        result_path = self._get_result_path(task_id)
        
        if not result_path.exists():
            return None
        
        with open(result_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def update_progress(
        self,
        task_id: str,
        progress: str,
        current_item: str = "",
        detail: str = "",
        completed: int = None
    ):
        """
        更新任务进度
        
        Args:
            task_id: 任务ID
            progress: 进度 (如 "45%")
            current_item: 当前执行项
            detail: 详细说明
            completed: 已完成数量
        """
        status_data = self.get_status(task_id)
        
        if not status_data:
            raise ValueError(f"任务不存在: {task_id}")
        
        status = TaskStatusInfo(**status_data)
        
        # 更新状态
        status.status = TaskStatus.RUNNING.value
        status.progress = progress
        if current_item:
            status.current_item = current_item
        if detail:
            status.detail = detail
        if completed is not None:
            status.completed = completed
        
        self._save_status(status)
        
        # 触发回调
        if task_id in self._progress_callbacks:
            callback = self._progress_callbacks[task_id]
            callback(status)
    
    def complete(self, task_id: str, result: Dict):
        """
        标记任务完成
        
        Args:
            task_id: 任务ID
            result: 结果数据
        """
        # 更新状态
        status_data = self.get_status(task_id)
        if status_data:
            status = TaskStatusInfo(**status_data)
            status.status = TaskStatus.COMPLETED.value
            status.progress = "100%"
            status.completed = status.total
            status.detail = "任务完成"
            self._save_status(status)
        
        # 保存结果
        result_data = TaskResult(
            task_id=task_id,
            status=TaskStatus.COMPLETED.value,
            files=result.get('files', []),
            summary=result.get('summary', ''),
            elapsed_time=result.get('elapsed_time', 0),
            completed_at=datetime.now().isoformat()
        )
        
        with open(self._get_result_path(task_id), 'w', encoding='utf-8') as f:
            json.dump(asdict(result_data), f, indent=2, ensure_ascii=False)
        
        print(f"✅ 任务完成: {task_id}")
    
    def fail(self, task_id: str, error: str):
        """
        标记任务失败
        
        Args:
            task_id: 任务ID
            error: 错误信息
        """
        status_data = self.get_status(task_id)
        
        if status_data:
            status = TaskStatusInfo(**status_data)
            status.status = TaskStatus.FAILED.value
            status.error = error
            status.detail = f"任务失败: {error}"
            self._save_status(status)
        
        print(f"❌ 任务失败: {task_id} - {error}")
    
    def cancel(self, task_id: str) -> bool:
        """
        取消任务
        
        Args:
            task_id: 任务ID
            
        Returns:
            True: 取消成功
            False: 任务已完成或不存在
        """
        status_data = self.get_status(task_id)
        
        if not status_data:
            return False
        
        if status_data['status'] in [TaskStatus.COMPLETED.value, TaskStatus.FAILED.value]:
            return False
        
        # 创建取消标记文件
        cancel_path = self._get_task_path(task_id) / "cancel"
        cancel_path.touch()
        
        # 更新状态
        status = TaskStatusInfo(**status_data)
        status.status = TaskStatus.CANCELLED.value
        status.detail = "任务已取消"
        self._save_status(status)
        
        print(f"🛑 任务已取消: {task_id}")
        return True
    
    def is_cancelled(self, task_id: str) -> bool:
        """
        检查任务是否被取消
        
        Args:
            task_id: 任务ID
            
        Returns:
            True: 已取消
        """
        cancel_path = self._get_task_path(task_id) / "cancel"
        return cancel_path.exists()
    
    def list_tasks(
        self,
        status_filter: str = None,
        agent_id: str = None
    ) -> List[Dict]:
        """
        列出所有任务
        
        Args:
            status_filter: 状态过滤
            agent_id: Agent过滤
            
        Returns:
            任务列表
        """
        tasks = []
        
        for task_path in self.task_dir.iterdir():
            if not task_path.is_dir():
                continue
            
            task_id = task_path.name
            status = self.get_status(task_id)
            
            if not status:
                continue
            
            # 状态过滤
            if status_filter and status['status'] != status_filter:
                continue
            
            # Agent过滤
            config_path = task_path / "config.json"
            if config_path.exists() and agent_id:
                with open(config_path, 'r') as f:
                    config = json.load(f)
                if config.get('agent_id') != agent_id:
                    continue
            
            tasks.append(status)
        
        # 按时间排序
        tasks.sort(key=lambda x: x.get('updated_at', ''), reverse=True)
        
        return tasks
    
    def register_progress_callback(self, task_id: str, callback: Callable):
        """
        注册进度回调函数
        
        Args:
            task_id: 任务ID
            callback: 回调函数 (接收TaskStatus参数)
        """
        self._progress_callbacks[task_id] = callback
    
    def cleanup_old_tasks(self, days: int = 7):
        """
        清理旧任务
        
        Args:
            days: 保留天数
        """
        cutoff = datetime.now().timestamp() - (days * 24 * 60 * 60)
        
        for task_path in self.task_dir.iterdir():
            if not task_path.is_dir():
                continue
            
            # 检查最后修改时间
            mtime = task_path.stat().st_mtime
            
            if mtime < cutoff:
                import shutil
                shutil.rmtree(task_path)
                print(f"🗑️ 清理旧任务: {task_path.name}")


class TaskWorker:
    """
    任务工作器 (在Agent内部使用)
    
    用于Agent内部上报进度
    """
    
    def __init__(self, task_id: str, task_dir: str = "/tmp/long_tasks"):
        """
        初始化工作器
        
        Args:
            task_id: 任务ID
            task_dir: 任务目录
        """
        self.task_id = task_id
        self.task_dir = Path(task_dir)
        self.manager = LongTaskManager(task_dir)
        
        # 记录开始时间
        self.started_at = datetime.now()
        self.last_report_time = self.started_at
    
    def update_progress(
        self,
        progress: str,
        current_item: str = "",
        detail: str = "",
        completed: int = None
    ):
        """
        更新进度
        
        Args:
            progress: 进度 (如 "45%")
            current_item: 当前项
            detail: 详情
            completed: 已完成数量
        """
        self.manager.update_progress(
            self.task_id,
            progress=progress,
            current_item=current_item,
            detail=detail,
            completed=completed
        )
        
        self.last_report_time = datetime.now()
    
    def complete(self, result: Dict):
        """
        完成任务
        
        Args:
            result: 结果数据
        """
        elapsed = int((datetime.now() - self.started_at).total_seconds())
        result['elapsed_time'] = elapsed
        
        self.manager.complete(self.task_id, result)
    
    def fail(self, error: str):
        """
        标记失败
        
        Args:
            error: 错误信息
        """
        self.manager.fail(self.task_id, error)
    
    def should_continue(self) -> bool:
        """
        检查是否应该继续执行
        
        Returns:
            True: 继续执行
            False: 任务被取消
        """
        return not self.manager.is_cancelled(self.task_id)
    
    def check_interval(self, interval_seconds: int = 30) -> bool:
        """
        检查是否到了上报间隔
        
        Args:
            interval_seconds: 间隔秒数
            
        Returns:
            True: 应该上报
        """
        elapsed = (datetime.now() - self.last_report_time).total_seconds()
        return elapsed >= interval_seconds


# 便捷函数
def submit_long_task(
    agent_id: str,
    task_config: Dict,
    task_dir: str = "/tmp/long_tasks"
) -> str:
    """
    便捷函数: 提交长时间任务
    
    Args:
        agent_id: Agent ID
        task_config: 任务配置
        task_dir: 任务目录
        
    Returns:
        task_id
    """
    manager = LongTaskManager(task_dir)
    return manager.submit(agent_id, task_config)


def get_task_status(task_id: str, task_dir: str = "/tmp/long_tasks") -> Optional[Dict]:
    """
    便捷函数: 获取任务状态
    
    Args:
        task_id: 任务ID
        task_dir: 任务目录
        
    Returns:
        状态字典
    """
    manager = LongTaskManager(task_dir)
    return manager.get_status(task_id)


def wait_for_completion(
    task_id: str,
    task_dir: str = "/tmp/long_tasks",
    poll_interval: int = 5,
    on_progress: Callable = None
) -> Dict:
    """
    便捷函数: 等待任务完成
    
    Args:
        task_id: 任务ID
        task_dir: 任务目录
        poll_interval: 轮询间隔(秒)
        on_progress: 进度回调函数
        
    Returns:
        任务结果
    """
    manager = LongTaskManager(task_dir)
    
    while True:
        status = manager.get_status(task_id)
        
        if not status:
            raise ValueError(f"任务不存在: {task_id}")
        
        # 调用进度回调
        if on_progress:
            on_progress(status)
        
        # 检查是否完成
        if status['status'] == TaskStatus.COMPLETED.value:
            return manager.get_result(task_id)
        
        if status['status'] == TaskStatus.FAILED.value:
            raise RuntimeError(f"任务失败: {status.get('error', 'Unknown')}")
        
        if status['status'] == TaskStatus.CANCELLED.value:
            raise RuntimeError("任务已取消")
        
        time.sleep(poll_interval)


if __name__ == "__main__":
    # 简单测试
    print("✅ Long Task Manager 模块加载成功")
    print(f"   版本: v1.0")
    print(f"   功能: 长时间任务管理、进度追踪")
