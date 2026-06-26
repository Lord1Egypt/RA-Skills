# auto-evolve core types — no external dependencies
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Optional

# ---- Enums ---------------------------------------------------------------

class RiskLevel(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class ChangeCategory(Enum):
    ADDED = "added"
    MODIFIED = "modified"
    DELETED = "deleted"
    OPTIMIZATION = "optimization"
    PENDING_APPROVAL = "pending_approval"

class OperationMode(Enum):
    DRY_RUN = "dry_run"
    FULL_AUTO = "full_auto"
    SEMI_AUTO = "semi_auto"

# ---- Repository -----------------------------------------------------------

@dataclass
class Repository:
    path: str
    remote_url: str = ""
    branch: str = "master"
    auto_monitor: bool = True
    auto_commit: bool = True
    issues_close: bool = True
    skill_name: str = ""
    skill_version: str = ""
    _resolved_path: Optional[Path] = field(default=None, repr=False)

    def resolve_path(self) -> Path:
        if self._resolved_path:
            return self._resolved_path
        p = Path(self.path)
        if p.is_absolute():
            self._resolved_path = p
        else:
            self._resolved_path = Path.home() / p
        return self._resolved_path

# ---- ChangeItem ----------------------------------------------------------

@dataclass
class ChangeItem:
    id: int
    repo: str
    file_path: str
    category: ChangeCategory
    description: str
    diff: str = ""
    risk: RiskLevel = RiskLevel.MEDIUM
    value_score: float = 0.0
    cost_score: float = 0.0
    priority: float = 0.0
    approved: bool = False
    risk_floor: RiskLevel = RiskLevel.MEDIUM
    risk_ceiling: RiskLevel = RiskLevel.HIGH
    tags: list[str] = field(default_factory=list)
    issue_id: Optional[str] = None
    commit_hash: Optional[str] = None
    change_type: str = ""

    def to_dict(self) -> dict:
        return {
            "id": self.id, "repo": self.repo, "file_path": self.file_path,
            "category": self.category.value, "description": self.description,
            "risk": self.risk.value, "value_score": self.value_score,
            "cost_score": self.cost_score, "priority": self.priority,
            "approved": self.approved, "risk_floor": self.risk_floor.value,
            "risk_ceiling": self.risk_ceiling.value, "tags": self.tags,
            "issue_id": self.issue_id, "commit_hash": self.commit_hash,
            "change_type": self.change_type,
        }

# ---- OptimizationFinding --------------------------------------------------

@dataclass
class OptimizationFinding:
    type: str
    file_path: str
    description: str
    language: str = ""
    line_start: int = 0
    line_end: int = 0
    duplicate_count: int = 0
    duplicate_files: list[str] = field(default_factory=list)
    function_name: str = ""
    lines_of_code: int = 0
    auto_executable: bool = False
    risk: RiskLevel = RiskLevel.LOW
    template: str = ""
    dependencies: list[str] = field(default_factory=list)

# ---- IterationManifest ---------------------------------------------------

@dataclass
class IterationManifest:
    iteration_id: str
    timestamp: str
    repos_affected: list[str] = field(default_factory=list)
    items_approved: int = 0
    items_auto: int = 0
    items_rejected: int = 0
    todos_resolved: int = 0
    files_changed: int = 0
    lines_added: int = 0
    lines_removed: int = 0
    cost_total_usd: float = 0.0
    effect_score: float = 0.0
    commit_hash: str = ""

# ---- LearningEntry ------------------------------------------------------

@dataclass
class LearningEntry:
    timestamp: str
    description: str
    reason: str = ""
    approved: bool = False
    repo: str = ""
    agent_id: str = ""

# ---- AlertEntry ---------------------------------------------------------

@dataclass
class AlertEntry:
    timestamp: str
    alert_type: str
    message: str
    severity: str = "info"

# ---- IterationMetrics ----------------------------------------------------

@dataclass
class IterationMetrics:
    iteration_id: str
    todos_resolved: int = 0
    files_affected: int = 0
    lines_added: int = 0
    lines_removed: int = 0
    net_delta: int = 0
