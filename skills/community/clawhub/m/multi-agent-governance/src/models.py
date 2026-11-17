"""
Data models for Multi-Agent Governance System
"""

from typing import List, Dict, Any, Optional, Literal
from dataclasses import dataclass, field
from enum import Enum


class ResolutionStrategy(Enum):
    """Conflict resolution strategies"""
    ORCHESTRATOR_FIRST = "orchestrator_first"
    USER_FIRST = "user_first"
    VOTING = "voting"
    PRIORITY_BASED = "priority_based"


class MissingInputAction(Enum):
    """Actions when required input is missing in handoff"""
    BLOCK_TRANSITION = "block_transition"
    WARN_AND_CONTINUE = "warn_and_continue"
    AUTO_FILL_DEFAULTS = "auto_fill_defaults"


@dataclass
class AgentRoleConfig:
    """Configuration for a single agent role"""
    name: str
    role: str
    responsibilities: List[str] = field(default_factory=list)
    must_not: List[str] = field(default_factory=list)
    outputs: List[str] = field(default_factory=list)
    reviewer_for: Optional[str] = None
    priority: int = 0  # For priority-based conflict resolution
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "name": self.name,
            "role": self.role,
            "responsibilities": self.responsibilities,
            "must_not": self.must_not,
            "outputs": self.outputs,
            "reviewer_for": self.reviewer_for,
            "priority": self.priority,
            "metadata": self.metadata,
        }


@dataclass
class HandoffTemplate:
    """Template for agent handoff"""
    required_fields: List[str] = field(default_factory=lambda: [
        "from", "to", "change_id", "phase", "inputs", "assumptions",
        "open_questions", "required_outputs", "required_skills", "gate_before_next"
    ])
    optional_fields: List[str] = field(default_factory=lambda: [
        "notes", "timestamp", "metadata"
    ])
    missing_input_action: MissingInputAction = MissingInputAction.BLOCK_TRANSITION
    custom_validation_rules: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        missing_action_value = self.missing_input_action
        if isinstance(missing_action_value, MissingInputAction):
            missing_action_value = missing_action_value.value

        return {
            "required_fields": self.required_fields,
            "optional_fields": self.optional_fields,
            "missing_input_action": missing_action_value,
            "custom_validation_rules": self.custom_validation_rules,
        }


@dataclass
class ValidationResult:
    """Result of a validation operation"""
    valid: bool
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    missing_fields: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "valid": self.valid,
            "errors": self.errors,
            "warnings": self.warnings,
            "missing_fields": self.missing_fields,
        }


@dataclass
class BoundaryCheckResult:
    """Result of a role boundary check"""
    allowed: bool
    violations: List[str] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "allowed": self.allowed,
            "violations": self.violations,
            "recommendations": self.recommendations,
        }


@dataclass
class HandoffResult:
    """Result of a handoff operation"""
    success: bool
    handoff_data: Dict[str, Any]
    validation_result: ValidationResult
    next_phase: Optional[str] = None
    next_gate: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "success": self.success,
            "handoff_data": self.handoff_data,
            "validation_result": self.validation_result.to_dict(),
            "next_phase": self.next_phase,
            "next_gate": self.next_gate,
        }


@dataclass
class AgentConflict:
    """Represents a conflict between agents"""
    agents: List[str]
    disagreement_type: str
    context: Dict[str, Any] = field(default_factory=dict)
    severity: Literal["low", "medium", "high", "critical"] = "medium"

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "agents": self.agents,
            "disagreement_type": self.disagreement_type,
            "context": self.context,
            "severity": self.severity,
        }


@dataclass
class ResolutionResult:
    """Result of a conflict resolution"""
    resolved: bool
    final_decision: str
    decision_maker: str
    reasoning: str
    alternative_options: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "resolved": self.resolved,
            "final_decision": self.final_decision,
            "decision_maker": self.decision_maker,
            "reasoning": self.reasoning,
            "alternative_options": self.alternative_options,
        }