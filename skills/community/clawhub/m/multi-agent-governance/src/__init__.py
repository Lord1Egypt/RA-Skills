"""
Multi-Agent Governance System for OpenClaw

A comprehensive governance system for managing agent roles, responsibilities,
handoff policies, and conflict resolution in multi-agent environments.
"""

from .core import MultiAgentGovernance
from .models import (
    AgentRoleConfig,
    HandoffTemplate,
    HandoffResult,
    ValidationResult,
    BoundaryCheckResult,
    ResolutionResult,
    AgentConflict,
    ResolutionStrategy,
    MissingInputAction,
)
from .templates import (
    StandardTemplate,
    SimplifiedTemplate,
    MinimalTemplate
)

__version__ = "1.0.0"
__author__ = "Terr123123"
__license__ = "MIT"

__all__ = [
    "MultiAgentGovernance",
    "AgentRoleConfig",
    "HandoffTemplate",
    "HandoffResult",
    "ValidationResult",
    "BoundaryCheckResult",
    "ResolutionResult",
    "AgentConflict",
    "ResolutionStrategy",
    "MissingInputAction",
    "StandardTemplate",
    "SimplifiedTemplate",
    "MinimalTemplate",
]