"""Data models for Night-Shift plan queue."""

from __future__ import annotations
import uuid
from datetime import datetime, timezone
from enum import Enum
from typing import Optional


class PlanStatus(str, Enum):
    PENDING = "pending"
    QUEUED = "queued"
    APPROVED = "approved"
    EXECUTING = "executing"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"
    CANCELLED = "cancelled"


class PhaseStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    PASSED = "passed"
    FAILED = "failed"
    SKIPPED = "skipped"


class Priority(str, Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"

    @property
    def weight(self) -> int:
        return {"critical": 4, "high": 3, "medium": 2, "low": 1}[self.value]


class VerificationType(str, Enum):
    NONE = "none"
    CHECK_FILES_EXIST = "check_files_exist"
    RUN_TESTS = "run_tests"
    RUN_BUILD = "run_build"
    CHECK_GIT_DIFF = "check_git_diff"
    LINT_CHECK = "lint_check"
    INTEGRATION_CHECK = "integration_check"
    SMOKE_TEST = "smoke_test"
    SNAPSHOT_DIFF = "snapshot_diff"
    IMPORT_CHECK = "import_check"


class Phase:
    def __init__(
        self,
        id: int,
        title: str,
        prompt: str,
        description: str = "",
        verification: str = "none",
        verification_config: Optional[dict] = None,
        estimated_tokens: int = 30000,
        depends_on: Optional[list[int]] = None,
        execution_method: str = "cursor",
    ):
        self.id = id
        self.title = title
        self.description = description
        self.prompt = prompt
        self.verification = verification
        self.verification_config = verification_config or {}
        self.estimated_tokens = estimated_tokens
        self.depends_on = depends_on or []
        self.execution_method = execution_method  # "cursor", "shell", "subagent"
        self.status = PhaseStatus.PENDING
        self.result = None
        self.started_at: Optional[str] = None
        self.completed_at: Optional[str] = None
        self.duration_seconds: Optional[float] = None
        self.tokens_used: Optional[int] = None
        self.commits: list[str] = []
        self.attempts: int = 0

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "prompt": self.prompt,
            "verification": self.verification,
            "verification_config": self.verification_config,
            "estimated_tokens": self.estimated_tokens,
            "depends_on": self.depends_on,
            "execution_method": self.execution_method,
            "status": self.status.value,
            "result": self.result,
            "started_at": self.started_at,
            "completed_at": self.completed_at,
            "duration_seconds": self.duration_seconds,
            "tokens_used": self.tokens_used,
            "commits": self.commits,
            "attempts": self.attempts,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Phase":
        p = cls(
            id=data["id"],
            title=data["title"],
            description=data.get("description", ""),
            prompt=data["prompt"],
            verification=data.get("verification", "none"),
            verification_config=data.get("verification_config", {}),
            estimated_tokens=data.get("estimated_tokens", 30000),
            depends_on=data.get("depends_on", []),
            execution_method=data.get("execution_method", "cursor"),
        )
        p.status = PhaseStatus(data.get("status", "pending"))
        p.result = data.get("result")
        p.started_at = data.get("started_at")
        p.completed_at = data.get("completed_at")
        p.duration_seconds = data.get("duration_seconds")
        p.tokens_used = data.get("tokens_used")
        p.commits = data.get("commits", [])
        p.attempts = data.get("attempts", 0)
        return p


class Execution:
    def __init__(self):
        self.started_at: Optional[str] = None
        self.completed_at: Optional[str] = None
        self.total_tokens_used: int = 0
        self.total_duration_seconds: float = 0.0
        self.total_api_calls: int = 0
        self.current_phase: Optional[int] = None
        self.checkpoints: list[dict] = []
        self.failure_log: list[dict] = []
        self.morning_report: Optional[str] = None

    def to_dict(self) -> dict:
        return {
            "started_at": self.started_at,
            "completed_at": self.completed_at,
            "total_tokens_used": self.total_tokens_used,
            "total_duration_seconds": self.total_duration_seconds,
            "total_api_calls": self.total_api_calls,
            "current_phase": self.current_phase,
            "checkpoints": self.checkpoints,
            "failure_log": self.failure_log,
            "morning_report": self.morning_report,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Execution":
        e = cls()
        e.started_at = data.get("started_at")
        e.completed_at = data.get("completed_at")
        e.total_tokens_used = data.get("total_tokens_used", 0)
        e.total_duration_seconds = data.get("total_duration_seconds", 0.0)
        e.total_api_calls = data.get("total_api_calls", 0)
        e.current_phase = data.get("current_phase")
        e.checkpoints = data.get("checkpoints", [])
        e.failure_log = data.get("failure_log", [])
        e.morning_report = data.get("morning_report")
        return e


class Plan:
    def __init__(
        self,
        title: str,
        description: str = "",
        repo_url: Optional[str] = None,
        priority: str = "medium",
        auto_approve: bool = False,
        max_retries: int = 2,
        token_budget: int = 100000,
        source: str = "telegram",
        source_message_id: Optional[int] = None,
        base_branch: str = "master",
    ):
        self.id = self._generate_id()
        self.created_at = datetime.now(timezone.utc).isoformat()
        self.source = source
        self.source_message_id = source_message_id
        self.title = title
        self.description = description
        self.repo_url = repo_url
        self.priority = priority
        self.status = PlanStatus.QUEUED
        self.auto_approve = auto_approve
        self.max_retries = max_retries
        self.token_budget = token_budget
        self.branch = f"night-shift/{self.id}"
        self.base_branch = base_branch
        self.phases: list[Phase] = []
        self.execution = Execution()

        if auto_approve:
            self.status = PlanStatus.APPROVED

    @staticmethod
    def _generate_id() -> str:
        return f"plan-{uuid.uuid4().hex[:6]}"

    def add_phase(self, phase: Phase):
        self.phases.append(phase)

    def ordered_phases(self) -> list[Phase]:
        """Return phases in dependency order (topological sort)."""
        if not self.phases:
            return []
        ordered = []
        completed_ids = set()
        remaining = list(self.phases)
        max_iterations = len(self.phases) + 1
        iteration = 0
        while remaining and iteration < max_iterations:
            iteration += 1
            for phase in remaining[:]:
                if all(dep in completed_ids for dep in phase.depends_on):
                    ordered.append(phase)
                    completed_ids.add(phase.id)
                    remaining.remove(phase)
        if remaining:
            # Circular dependency — append remaining in order
            ordered.extend(remaining)
        return ordered

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "created_at": self.created_at,
            "source": self.source,
            "source_message_id": self.source_message_id,
            "title": self.title,
            "description": self.description,
            "repo_url": self.repo_url,
            "priority": self.priority,
            "status": self.status.value,
            "auto_approve": self.auto_approve,
            "max_retries": self.max_retries,
            "token_budget": self.token_budget,
            "branch": self.branch,
            "base_branch": self.base_branch,
            "phases": [p.to_dict() for p in self.phases],
            "execution": self.execution.to_dict(),
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Plan":
        p = cls(
            title=data["title"],
            description=data.get("description", ""),
            repo_url=data.get("repo_url"),
            priority=data.get("priority", "medium"),
            auto_approve=data.get("auto_approve", False),
            max_retries=data.get("max_retries", 2),
            token_budget=data.get("token_budget", 100000),
            source=data.get("source", "telegram"),
            source_message_id=data.get("source_message_id"),
            base_branch=data.get("base_branch", "master"),
        )
        p.id = data["id"]
        p.created_at = data["created_at"]
        p.status = PlanStatus(data.get("status", "queued"))
        p.branch = data.get("branch", f"night-shift/{p.id}")
        p.phases = [Phase.from_dict(ph) for ph in data.get("phases", [])]
        p.execution = Execution.from_dict(data.get("execution", {}))
        return p

    def __repr__(self):
        return f"Plan({self.id}: {self.title!r} [{self.status.value}])"
