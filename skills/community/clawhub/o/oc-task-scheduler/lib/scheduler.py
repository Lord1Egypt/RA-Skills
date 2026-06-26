#!/usr/bin/env python3
"""
Task Scheduler - Background task queue with WebSocket updates

Based on Bytebot Task System
"""

import asyncio
import json
import time
import uuid
from datetime import datetime
from enum import Enum
from typing import Dict, List, Callable, Optional, Any, Set
from dataclasses import dataclass, field, asdict
from pathlib import Path


class TaskStatus(Enum):
    CREATED = "created"
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    RETRYING = "retrying"


class TaskPriority(Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    URGENT = 4


@dataclass
class Task:
    """Represents a task"""
    id: str
    description: str
    status: TaskStatus = TaskStatus.CREATED
    priority: TaskPriority = TaskPriority.MEDIUM
    created_at: float = field(default_factory=time.time)
    started_at: Optional[float] = None
    completed_at: Optional[float] = None
    handler: Optional[Callable] = None
    params: Dict[str, Any] = field(default_factory=dict)
    result: Any = None
    error: Optional[str] = None
    retry_count: int = 0
    max_retries: int = 3
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "id": self.id,
            "description": self.description,
            "status": self.status.value,
            "priority": self.priority.value,
            "created_at": self.created_at,
            "started_at": self.started_at,
            "completed_at": self.completed_at,
            "params": self.params,
            "result": self.result,
            "error": self.error,
            "retry_count": self.retry_count
        }
    
    @property
    def duration_ms(self) -> Optional[int]:
        """Get task duration in milliseconds"""
        if self.started_at and self.completed_at:
            return int((self.completed_at - self.started_at) * 1000)
        return None


class TaskScheduler:
    """Task scheduler with queue and WebSocket support"""
    
    def __init__(self, max_concurrency: int = 4, persist_path: Optional[str] = None):
        self.max_concurrency = max_concurrency
        self.persist_path = persist_path
        
        self._tasks: Dict[str, Task] = {}
        self._queue: asyncio.PriorityQueue = asyncio.PriorityQueue()
        self._running: Set[str] = set()
        self._cancelled: Set[str] = set()
        self._handlers: Dict[str, Callable] = {}
        self._status_callbacks: List[Callable] = []
        self._event_callbacks: Dict[str, List[Callable]] = {}
        
        self._shutdown = False
        self._worker_task: Optional[asyncio.Task] = None
    
    def create_task(self, description: str, 
                   priority: TaskPriority = TaskPriority.MEDIUM,
                   handler: Optional[Callable] = None,
                   params: Optional[Dict[str, Any]] = None) -> Task:
        """Create a new task"""
        task_id = f"task_{uuid.uuid4().hex[:12]}"
        task = Task(
            id=task_id,
            description=description,
            priority=priority,
            handler=handler,
            params=params or {}
        )
        
        self._tasks[task_id] = task
        self._notify_event("task.created", task)
        
        # Add to queue
        asyncio.create_task(self._queue.put((-priority.value, task.created_at, task_id)))
        self._update_status(task_id, TaskStatus.PENDING)
        
        return task
    
    def schedule_task(self, description: str, cron: str,
                     priority: TaskPriority = TaskPriority.MEDIUM,
                     handler: Optional[Callable] = None) -> str:
        """Schedule a recurring task (placeholder for cron)"""
        # For now, just create immediate task
        # Full cron support would require a separate scheduler
        task = self.create_task(description, priority, handler)
        return task.id
    
    def get_task(self, task_id: str) -> Optional[Task]:
        """Get task by ID"""
        return self._tasks.get(task_id)
    
    def list_tasks(self, status: Optional[TaskStatus] = None,
                   limit: int = 100) -> List[Task]:
        """List tasks"""
        tasks = list(self._tasks.values())
        
        if status:
            tasks = [t for t in tasks if t.status == status]
        
        # Sort by created_at desc
        tasks.sort(key=lambda t: t.created_at, reverse=True)
        
        return tasks[:limit]
    
    def cancel_task(self, task_id: str) -> bool:
        """Cancel a task"""
        task = self._tasks.get(task_id)
        if not task:
            return False
        
        if task.status in [TaskStatus.COMPLETED, TaskStatus.FAILED, TaskStatus.CANCELLED]:
            return False
        
        self._cancelled.add(task_id)
        self._update_status(task_id, TaskStatus.CANCELLED)
        return True
    
    def retry_task(self, task_id: str) -> bool:
        """Retry a failed task"""
        task = self._tasks.get(task_id)
        if not task or task.status != TaskStatus.FAILED:
            return False
        
        task.retry_count += 1
        task.error = None
        task.status = TaskStatus.PENDING
        
        asyncio.create_task(self._queue.put((-task.priority.value, task.created_at, task_id)))
        self._update_status(task_id, TaskStatus.PENDING)
        return True
    
    def delete_task(self, task_id: str) -> bool:
        """Delete a task"""
        if task_id in self._tasks:
            del self._tasks[task_id]
            return True
        return False
    
    def on_status_change(self, callback: Callable) -> None:
        """Register status change callback"""
        self._status_callbacks.append(callback)
    
    def on_event(self, event: str, callback: Callable) -> None:
        """Register event callback"""
        if event not in self._event_callbacks:
            self._event_callbacks[event] = []
        self._event_callbacks[event].append(callback)
    
    def _update_status(self, task_id: str, new_status: TaskStatus) -> None:
        """Update task status and notify"""
        task = self._tasks.get(task_id)
        if not task:
            return
        
        old_status = task.status
        task.status = new_status
        
        # Notify callbacks
        for callback in self._status_callbacks:
            try:
                callback(task_id, old_status, new_status)
            except Exception:
                pass
        
        # Notify event
        self._notify_event("task.status_changed", {
            "id": task_id,
            "old_status": old_status.value,
            "new_status": new_status.value,
            "timestamp": time.time()
        })
    
    def _notify_event(self, event: str, data: Any) -> None:
        """Notify event subscribers"""
        callbacks = self._event_callbacks.get(event, [])
        for callback in callbacks:
            try:
                callback(data)
            except Exception:
                pass
    
    async def start(self) -> None:
        """Start the scheduler"""
        self._shutdown = False
        self._worker_task = asyncio.create_task(self._worker())
    
    async def stop(self) -> None:
        """Stop the scheduler"""
        self._shutdown = True
        if self._worker_task:
            self._worker_task.cancel()
            try:
                await self._worker_task
            except asyncio.CancelledError:
                pass
    
    async def _worker(self) -> None:
        """Worker loop"""
        while not self._shutdown:
            try:
                # Wait for task
                priority, created_at, task_id = await asyncio.wait_for(
                    self._queue.get(), timeout=1.0
                )
                
                if task_id in self._cancelled:
                    continue
                
                task = self._tasks.get(task_id)
                if not task or task.status != TaskStatus.PENDING:
                    continue
                
                # Check concurrency
                while len(self._running) >= self.max_concurrency:
                    await asyncio.sleep(0.1)
                
                # Execute task
                self._running.add(task_id)
                asyncio.create_task(self._execute_task(task_id))
                
            except asyncio.TimeoutError:
                continue
            except Exception as e:
                print(f"Worker error: {e}")
    
    async def _execute_task(self, task_id: str) -> None:
        """Execute a single task"""
        task = self._tasks.get(task_id)
        if not task:
            return
        
        self._update_status(task_id, TaskStatus.RUNNING)
        task.started_at = time.time()
        
        try:
            # Execute handler
            if task.handler:
                if asyncio.iscoroutinefunction(task.handler):
                    result = await task.handler(**task.params)
                else:
                    result = task.handler(**task.params)
                task.result = result
            
            task.completed_at = time.time()
            self._update_status(task_id, TaskStatus.COMPLETED)
            self._notify_event("task.completed", task)
            
        except Exception as e:
            task.error = str(e)
            task.completed_at = time.time()
            
            if task.retry_count < task.max_retries:
                self._update_status(task_id, TaskStatus.RETRYING)
                await asyncio.sleep(1)  # Delay before retry
                self.retry_task(task_id)
            else:
                self._update_status(task_id, TaskStatus.FAILED)
                self._notify_event("task.failed", task)
        
        finally:
            self._running.discard(task_id)
    
    def save_state(self, path: Optional[str] = None) -> None:
        """Save scheduler state"""
        path = path or self.persist_path
        if not path:
            return
        
        state = {
            "tasks": {tid: t.to_dict() for tid, t in self._tasks.items()}
        }
        Path(path).write_text(json.dumps(state, indent=2))
    
    def load_state(self, path: Optional[str] = None) -> None:
        """Load scheduler state"""
        path = path or self.persist_path
        if not path or not Path(path).exists():
            return
        
        # Load tasks (handlers won't be restored)
        pass  # Placeholder
