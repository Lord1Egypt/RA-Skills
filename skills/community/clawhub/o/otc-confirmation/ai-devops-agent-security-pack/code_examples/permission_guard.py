"""
Permission Guard — Role-Based Access Control for AI Agents

Evaluates operations against configurable rules and roles,
returning ALLOW / DENY / CONFIRM decisions.

Usage:
    guard = PermissionGuard(config)
    decision = guard.evaluate(operation, agent_role="developer")
    
    if decision.action == Action.DENY:
        raise PermissionError(decision.reason)
    elif decision.action == Action.CONFIRM:
        trigger_otc_flow(operation)
    else:
        execute(operation)

Requirements:
    Python 3.10+
    No external dependencies
"""

import fnmatch
import os
import re
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


# =============================================================
# Core Types
# =============================================================

class Action(Enum):
    ALLOW = "ALLOW"
    DENY = "DENY"
    CONFIRM = "CONFIRM"


@dataclass
class Operation:
    """Represents an operation the agent wants to perform."""
    type: str                           # e.g., "exec_command", "file_delete"
    command: str = ""                   # The actual command/action
    path: str = ""                      # Target file/directory path
    target: str = ""                    # Target environment/service
    parameters: dict = field(default_factory=dict)
    
    @property
    def real_path(self) -> str:
        """Resolve symlinks and normalize path."""
        if self.path:
            return os.path.realpath(os.path.expanduser(self.path))
        return ""


@dataclass
class Decision:
    """Result of a permission evaluation."""
    action: Action
    reason: str
    rule_name: str = ""
    risk_factors: list[str] = field(default_factory=list)


# =============================================================
# Absolute Deny Patterns
# =============================================================

ABSOLUTE_DENY_PATTERNS = [
    {
        "name": "recursive-root-delete",
        "pattern": r"rm\s+(-[a-zA-Z]*r[a-zA-Z]*f|.*-rf)\s+/\s*$",
        "reason": "Catastrophic: recursive delete from root",
    },
    {
        "name": "disk-format",
        "pattern": r"(mkfs\.|fdisk\s|parted\s)",
        "reason": "Disk formatting operation",
    },
    {
        "name": "disk-wipe",
        "pattern": r"dd\s+if=/dev/(zero|urandom)\s+of=/dev/",
        "reason": "Disk wipe operation",
    },
    {
        "name": "fork-bomb",
        "pattern": r":\(\)\{.*:\|:.*\};:",
        "reason": "Fork bomb detected",
    },
    {
        "name": "recursive-chmod-root",
        "pattern": r"chmod\s+(-R|--recursive)\s+\d+\s+/\s*$",
        "reason": "Recursive permission change from root",
    },
]


# =============================================================
# Role Definitions
# =============================================================

@dataclass
class RoleConfig:
    """Configuration for an agent role."""
    name: str
    allowed_operations: list[str] = field(default_factory=list)
    denied_operations: list[str] = field(default_factory=list)
    requires_confirmation: list[str] = field(default_factory=list)
    allowed_paths: list[str] = field(default_factory=list)
    excluded_paths: list[str] = field(default_factory=list)
    allowed_environments: list[str] = field(default_factory=list)
    max_concurrent: int = 10


# Default roles
DEFAULT_ROLES = {
    "researcher": RoleConfig(
        name="researcher",
        allowed_operations=["file_read", "web_search", "web_fetch", "summarize"],
        denied_operations=["exec_command", "file_write", "file_delete", "deploy"],
        allowed_paths=["*"],
        excluded_paths=["~/.ssh/*", "~/.gnupg/*", "*/secrets/*"],
    ),
    "developer": RoleConfig(
        name="developer",
        allowed_operations=[
            "file_read", "file_write", "exec_command", "git_operations"
        ],
        requires_confirmation=["exec_command"],
        allowed_paths=["~/projects/*", "~/workspace/*", "/tmp/*"],
        excluded_paths=["~/projects/*/secrets/*", "~/.ssh/*"],
    ),
    "ops-agent": RoleConfig(
        name="ops-agent",
        allowed_operations=[
            "file_read", "exec_command", "deploy", "restart_service"
        ],
        requires_confirmation=["deploy", "restart_service", "scale_resource"],
        allowed_environments=["staging"],
    ),
    "admin": RoleConfig(
        name="admin",
        allowed_operations=["*"],
        requires_confirmation=[
            "file_delete", "modify_permissions", "send_email",
            "send_message", "deploy",
        ],
    ),
}


# =============================================================
# Permission Guard
# =============================================================

class PermissionGuard:
    """Evaluates operations against roles and rules."""
    
    def __init__(self, roles: Optional[dict[str, RoleConfig]] = None):
        self.roles = roles or DEFAULT_ROLES
    
    def evaluate(self, operation: Operation, agent_role: str) -> Decision:
        """Evaluate an operation and return a decision.
        
        Evaluation order:
        1. Absolute deny patterns (always checked first)
        2. Role-based denied operations
        3. Role-based confirmation requirements
        4. Scope checks (path, environment)
        5. Role-based allowed operations
        6. Default: DENY (fail closed)
        """
        
        # --- Layer 1: Absolute deny patterns ---
        for pattern in ABSOLUTE_DENY_PATTERNS:
            if re.search(pattern["pattern"], operation.command):
                return Decision(
                    action=Action.DENY,
                    reason=pattern["reason"],
                    rule_name=pattern["name"],
                    risk_factors=["absolute_deny_pattern"],
                )
        
        # --- Layer 2: Role lookup ---
        if agent_role not in self.roles:
            return Decision(
                action=Action.DENY,
                reason=f"Unknown role: {agent_role}",
                rule_name="unknown_role",
            )
        
        role = self.roles[agent_role]
        
        # --- Layer 3: Explicit deny ---
        if operation.type in role.denied_operations:
            return Decision(
                action=Action.DENY,
                reason=f"Operation '{operation.type}' is denied for role '{agent_role}'",
                rule_name="role_deny",
            )
        
        # --- Layer 4: Check if operation is allowed ---
        if "*" not in role.allowed_operations and operation.type not in role.allowed_operations:
            return Decision(
                action=Action.DENY,
                reason=f"Operation '{operation.type}' is not in allowed list for role '{agent_role}'",
                rule_name="role_not_allowed",
            )
        
        # --- Layer 5: Scope checks ---
        if operation.real_path:
            scope_decision = self._check_path_scope(operation.real_path, role)
            if scope_decision.action == Action.DENY:
                return scope_decision
        
        if operation.target and role.allowed_environments:
            scope_decision = self._check_env_scope(operation.target, role)
            if scope_decision.action != Action.ALLOW:
                return scope_decision
        
        # --- Layer 6: Confirmation check ---
        if operation.type in role.requires_confirmation:
            risk_factors = []
            if operation.target == "production":
                risk_factors.append("production_target")
            return Decision(
                action=Action.CONFIRM,
                reason=f"Operation '{operation.type}' requires confirmation for role '{agent_role}'",
                rule_name="role_confirm",
                risk_factors=risk_factors,
            )
        
        # --- Layer 7: Allowed ---
        return Decision(
            action=Action.ALLOW,
            reason=f"Operation permitted for role '{agent_role}'",
            rule_name="role_allow",
        )
    
    def _check_path_scope(self, real_path: str, role: RoleConfig) -> Decision:
        """Check if path is within allowed scope."""
        # Check exclusions first
        for excluded in role.excluded_paths:
            expanded = os.path.expanduser(excluded)
            if fnmatch.fnmatch(real_path, expanded):
                return Decision(
                    action=Action.DENY,
                    reason=f"Path '{real_path}' is in excluded scope",
                    rule_name="path_excluded",
                )
        
        # Check allowed paths
        if not role.allowed_paths:
            return Decision(action=Action.ALLOW, reason="No path restrictions")
        
        for allowed in role.allowed_paths:
            expanded = os.path.expanduser(allowed)
            if fnmatch.fnmatch(real_path, expanded):
                return Decision(
                    action=Action.ALLOW,
                    reason=f"Path within scope: {allowed}",
                    rule_name="path_allowed",
                )
        
        return Decision(
            action=Action.DENY,
            reason=f"Path '{real_path}' is outside agent scope",
            rule_name="path_out_of_scope",
        )
    
    def _check_env_scope(self, target_env: str, role: RoleConfig) -> Decision:
        """Check environment scope."""
        if target_env not in role.allowed_environments:
            return Decision(
                action=Action.DENY,
                reason=f"Environment '{target_env}' is not in allowed list",
                rule_name="env_denied",
            )
        
        # Production always requires confirmation
        if target_env == "production":
            return Decision(
                action=Action.CONFIRM,
                reason="Production environment always requires confirmation",
                rule_name="production_confirm",
                risk_factors=["production_target"],
            )
        
        return Decision(action=Action.ALLOW, reason=f"Environment '{target_env}' permitted")


# =============================================================
# Example Usage
# =============================================================

if __name__ == "__main__":
    guard = PermissionGuard()
    
    test_cases = [
        ("developer", Operation(type="file_read", path="~/projects/app/main.go")),
        ("developer", Operation(type="exec_command", command="go test ./...")),
        ("developer", Operation(type="file_read", path="~/.ssh/id_rsa")),
        ("researcher", Operation(type="exec_command", command="ls -la")),
        ("ops-agent", Operation(type="deploy", target="staging")),
        ("ops-agent", Operation(type="deploy", target="production")),
        ("admin", Operation(type="exec_command", command="rm -rf /")),
        ("admin", Operation(type="file_delete", path="/tmp/test.log")),
    ]
    
    print("Permission Guard Evaluation Results")
    print("=" * 70)
    
    for role, op in test_cases:
        decision = guard.evaluate(op, role)
        icon = {"ALLOW": "✅", "DENY": "🚫", "CONFIRM": "⚠️"}[decision.action.value]
        print(f"\n{icon} [{role}] {op.type}: {op.command or op.path or op.target}")
        print(f"   Decision: {decision.action.value} — {decision.reason}")
        if decision.risk_factors:
            print(f"   Risk factors: {', '.join(decision.risk_factors)}")
