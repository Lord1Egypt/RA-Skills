"""
Model Routing Middleware

Lightweight middleware that classifies prompts and routes them
to the optimal model based on task type, context size, and
response confidence.

Usage:
    from router import route_request

    route = route_request("Write a Python function to sort a list")
    # Route(model='YOUR_CODE_MODEL', think=True, task_type='coding', ...)
"""

from router.classifiers import TaskType, classify_task, classify_task_simple, ClassificationResult
from router.router import ModelRouter, Route, route_request
from router.models import ModelRegistry, ModelInfo
from router.escalation import EscalationEngine, EscalationLevel, EscalationResult, check_escalation
from router.memory import ContextManager, ContextStatus, Message, check_context_status

__version__ = "0.1.0"
__all__ = [
    "ModelRouter",
    "Route",
    "route_request",
    "TaskType",
    "classify_task",
    "classify_task_simple",
    "ClassificationResult",
    "ModelRegistry",
    "ModelInfo",
    "EscalationEngine",
    "EscalationLevel",
    "EscalationResult",
    "check_escalation",
    "ContextManager",
    "ContextStatus",
    "Message",
    "check_context_status",
]