"""
Task Scheduler Library

Background task queue with WebSocket real-time updates
"""

from .scheduler import TaskScheduler, Task, TaskStatus, TaskPriority

__version__ = "1.0.0"
__all__ = ['TaskScheduler', 'Task', 'TaskStatus', 'TaskPriority']
