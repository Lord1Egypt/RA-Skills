"""
类型定义
"""
from enum import Enum
from typing import List, Dict, Optional, Any
from dataclasses import dataclass, field


class RefinementType(Enum):
    """精炼类型"""
    FINALIZE = "finalize"
    REFINE_SUBTASKS = "refine_subtasks"
    REFINE_TRUTHS = "refine_truths"


@dataclass
class Goal:
    """用户目标"""
    original_prompt: str
    clarified_objective: str
    constraints: List[str] = field(default_factory=list)
    success_criteria: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "original_prompt": self.original_prompt,
            "clarified_objective": self.clarified_objective,
            "constraints": self.constraints,
            "success_criteria": self.success_criteria
        }


@dataclass
class FundamentalTruth:
    """基础事实/公理"""
    id: str
    content: str
    description: str = ""
    is_fundamental: bool = True
    dependencies: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "content": self.content,
            "description": self.description,
            "is_fundamental": self.is_fundamental,
            "dependencies": self.dependencies
        }


@dataclass
class SubTask:
    """原子子任务"""
    id: str
    title: str
    description: str
    acceptance_criteria: List[str] = field(default_factory=list)
    dependencies: List[str] = field(default_factory=list)
    is_feasible: bool = True
    is_atomic: bool = True
    assigned_agent_id: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "acceptance_criteria": self.acceptance_criteria,
            "dependencies": self.dependencies,
            "is_feasible": self.is_feasible,
            "is_atomic": self.is_atomic,
            "assigned_agent_id": self.assigned_agent_id
        }


@dataclass
class RefinementDecision:
    """精炼决策"""
    decision: RefinementType
    reason: str
    feedback: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "decision": self.decision.value,
            "reason": self.reason,
            "feedback": self.feedback
        }


@dataclass
class TaskResult:
    """子任务执行结果"""
    task_id: str
    success: bool
    output: Any
    validation_passed: bool
    error_message: str = ""
    execution_time_ms: int = 0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "task_id": self.task_id,
            "success": self.success,
            "output": self.output,
            "validation_passed": self.validation_passed,
            "error_message": self.error_message,
            "execution_time_ms": self.execution_time_ms
        }


@dataclass
class ExecutionPlan:
    """执行计划"""
    ordered_tasks: List[SubTask]
    parallel_batches: List[List[SubTask]]
    has_circular_dependency: bool = False
    circular_dependency_details: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "ordered_tasks": [t.to_dict() for t in self.ordered_tasks],
            "parallel_batches": [[t.to_dict() for t in batch] for batch in self.parallel_batches],
            "has_circular_dependency": self.has_circular_dependency,
            "circular_dependency_details": self.circular_dependency_details
        }


@dataclass
class FinalResult:
    """最终结果"""
    goal: Goal
    truths: List[FundamentalTruth]
    tasks: List[SubTask]
    task_results: List[TaskResult]
    synthesized_output: Any
    global_validation_passed: bool
    iteration_count: int
    report: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "goal": self.goal.to_dict(),
            "truths": [t.to_dict() for t in self.truths],
            "tasks": [t.to_dict() for t in self.tasks],
            "task_results": [r.to_dict() for r in self.task_results],
            "synthesized_output": self.synthesized_output,
            "global_validation_passed": self.global_validation_passed,
            "iteration_count": self.iteration_count,
            "report": self.report
        }
