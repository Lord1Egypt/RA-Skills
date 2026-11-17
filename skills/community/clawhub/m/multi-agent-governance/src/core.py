"""
Core implementation of Multi-Agent Governance System
"""

from typing import List, Dict, Any, Optional, Union
from pathlib import Path
import yaml
import json

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
from .templates import StandardTemplate, SimplifiedTemplate, MinimalTemplate
from .validators import GovernanceValidator, HandoffValidator
from .resolvers import ConflictResolver


class AgentRoleRegistry:
    """Agent role registration center"""

    def __init__(self):
        self._roles: Dict[str, AgentRoleConfig] = {}

    def register_role(self, role_config: AgentRoleConfig) -> None:
        """Register a new agent role"""
        if role_config.name in self._roles:
            raise ValueError(f"Role '{role_config.name}' already registered")
        self._roles[role_config.name] = role_config

    def get_role(self, role_name: str) -> Optional[AgentRoleConfig]:
        """Get a registered role by name"""
        return self._roles.get(role_name)

    def list_roles(self) -> List[str]:
        """List all registered role names"""
        return list(self._roles.keys())

    def update_role(self, role_name: str, updates: Dict[str, Any]) -> None:
        """Update an existing role"""
        if role_name not in self._roles:
            raise ValueError(f"Role '{role_name}' not found")

        role = self._roles[role_name]
        for key, value in updates.items():
            if hasattr(role, key):
                setattr(role, key, value)
            else:
                role.metadata[key] = value

    def remove_role(self, role_name: str) -> None:
        """Remove a registered role"""
        if role_name not in self._roles:
            raise ValueError(f"Role '{role_name}' not found")
        del self._roles[role_name]

    def load_template(self, template: Union[str, Dict]) -> None:
        """Load roles from a template"""
        if isinstance(template, str):
            template_map = {
                "standard": StandardTemplate,
                "simplified": SimplifiedTemplate,
                "minimal": MinimalTemplate,
            }
            if template not in template_map:
                raise ValueError(f"Unknown template: {template}")
            roles_data = template_map[template].get_roles()
        else:
            roles_data = template

        for role_data in roles_data:
            role_config = AgentRoleConfig(**role_data)
            self.register_role(role_config)

    def to_dict(self) -> Dict[str, Any]:
        """Export all roles to dictionary"""
        return {name: role.to_dict() for name, role in self._roles.items()}

    def save_to_file(self, filepath: Union[str, Path]) -> None:
        """Save roles to YAML or JSON file"""
        filepath = Path(filepath)
        data = self.to_dict()

        if filepath.suffix in ['.yaml', '.yml']:
            with open(filepath, 'w', encoding='utf-8') as f:
                yaml.dump(data, f, default_flow_style=False, allow_unicode=True)
        elif filepath.suffix == '.json':
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        else:
            raise ValueError(f"Unsupported file format: {filepath.suffix}")

    def load_from_file(self, filepath: Union[str, Path]) -> None:
        """Load roles from YAML or JSON file"""
        filepath = Path(filepath)

        if filepath.suffix in ['.yaml', '.yml']:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
        elif filepath.suffix == '.json':
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
        else:
            raise ValueError(f"Unsupported file format: {filepath.suffix}")

        for name, role_data in data.items():
            role_config = AgentRoleConfig(**role_data)
            self.register_role(role_config)


class HandoffPolicyManager:
    """Agent handoff policy manager"""

    def __init__(self, template: Optional[HandoffTemplate] = None):
        self.template = template or HandoffTemplate()
        self._custom_templates: Dict[str, HandoffTemplate] = {}

    def define_custom_template(self, name: str, template: HandoffTemplate) -> None:
        """Define a custom handoff template"""
        self._custom_templates[name] = template

    def get_template(self, name: Optional[str] = None) -> HandoffTemplate:
        """Get handoff template"""
        if name and name in self._custom_templates:
            return self._custom_templates[name]
        return self.template

    def validate_handoff(self, handoff_data: Dict[str, Any], template_name: Optional[str] = None) -> ValidationResult:
        """Validate a handoff"""
        template = self.get_template(template_name)
        validator = HandoffValidator(template)
        return validator.validate(handoff_data)

    def enforce_handoff(
        self,
        from_agent: str,
        to_agent: str,
        data: Dict[str, Any],
        template_name: Optional[str] = None
    ) -> HandoffResult:
        """Enforce a handoff between agents"""
        validation_result = self.validate_handoff(data, template_name)

        success = validation_result.valid
        if not success and self.template.missing_input_action == MissingInputAction.BLOCK_TRANSITION:
            success = False

        handoff_data = {
            "from": from_agent,
            "to": to_agent,
            **data
        }

        return HandoffResult(
            success=success,
            handoff_data=handoff_data,
            validation_result=validation_result,
            next_phase=data.get("next_phase"),
            next_gate=data.get("next_gate")
        )

    def to_dict(self) -> Dict[str, Any]:
        """Export policy to dictionary"""
        return {
            "default_template": self.template.to_dict(),
            "custom_templates": {name: t.to_dict() for name, t in self._custom_templates.items()}
        }


class MultiAgentGovernance:
    """Main governance system class"""

    def __init__(
        self,
        template: Union[str, Dict] = "standard",
        handoff_policy: Optional[Dict[str, Any]] = None,
        conflict_strategy: ResolutionStrategy = ResolutionStrategy.ORCHESTRATOR_FIRST,
        framework: str = "openclaw"
    ):
        """
        Initialize the governance system

        Args:
            template: Role template name ("standard", "simplified", "minimal") or custom config dict
            handoff_policy: Custom handoff policy configuration
            conflict_strategy: Conflict resolution strategy
            framework: Target framework name
        """
        self.registry = AgentRoleRegistry()
        self.registry.load_template(template)

        handoff_template = HandoffTemplate()
        if handoff_policy:
            # Extract parameters from handoff_policy and create HandoffTemplate
            required_fields = handoff_policy.get("required_fields", handoff_template.required_fields)
            optional_fields = handoff_policy.get("optional_fields", handoff_template.optional_fields)
            missing_input_action_str = handoff_policy.get("missing_input_action", "block_transition")
            
            # Convert string to MissingInputAction enum if needed
            if isinstance(missing_input_action_str, str):
                missing_input_action = MissingInputAction(missing_input_action_str)
            else:
                missing_input_action = missing_input_action_str
            
            custom_validation_rules = handoff_policy.get("custom_validation_rules", {})
            
            handoff_template = HandoffTemplate(
                required_fields=required_fields,
                optional_fields=optional_fields,
                missing_input_action=missing_input_action,
                custom_validation_rules=custom_validation_rules
            )

        self.handoff_manager = HandoffPolicyManager(handoff_template)
        self.conflict_resolver = ConflictResolver(conflict_strategy)
        self.validator = GovernanceValidator(self.registry)

        self.framework = framework
        self._governance_report: Dict[str, Any] = {}

    def register_role(
        self,
        name: str,
        role: str,
        responsibilities: List[str],
        must_not: List[str],
        outputs: List[str],
        reviewer_for: Optional[str] = None,
        priority: int = 0,
        metadata: Optional[Dict[str, Any]] = None
    ) -> None:
        """Register a custom agent role"""
        role_config = AgentRoleConfig(
            name=name,
            role=role,
            responsibilities=responsibilities,
            must_not=must_not,
            outputs=outputs,
            reviewer_for=reviewer_for,
            priority=priority,
            metadata=metadata or {}
        )
        self.registry.register_role(role_config)

    def get_role(self, role_name: str) -> Optional[AgentRoleConfig]:
        """Get a registered role"""
        return self.registry.get_role(role_name)

    def list_roles(self) -> List[str]:
        """List all registered roles"""
        return self.registry.list_roles()

    def validate_handoff(
        self,
        from_agent: str,
        to_agent: str,
        handoff_data: Dict[str, Any]
    ) -> HandoffResult:
        """Validate and enforce a handoff between agents"""
        # Check if both agents exist
        if not self.registry.get_role(from_agent):
            return HandoffResult(
                success=False,
                handoff_data=handoff_data,
                validation_result=ValidationResult(
                    valid=False,
                    errors=[f"Agent '{from_agent}' not registered"]
                )
            )

        if not self.registry.get_role(to_agent):
            return HandoffResult(
                success=False,
                handoff_data=handoff_data,
                validation_result=ValidationResult(
                    valid=False,
                    errors=[f"Agent '{to_agent}' not registered"]
                )
            )

        # Enforce handoff
        result = self.handoff_manager.enforce_handoff(from_agent, to_agent, handoff_data)

        # Record in governance report
        self._record_handoff(result)

        return result

    def validate_agent_action(self, agent: str, action: str) -> BoundaryCheckResult:
        """Validate if an agent can perform an action"""
        return self.validator.validate_agent_action(agent, action)

    def resolve_conflict(
        self,
        agents: List[str],
        disagreement_type: str,
        context: Dict[str, Any],
        severity: str = "medium"
    ) -> ResolutionResult:
        """Resolve a conflict between agents"""
        conflict = AgentConflict(
            agents=agents,
            disagreement_type=disagreement_type,
            context=context,
            severity=severity
        )

        result = self.conflict_resolver.resolve(conflict, self.registry)

        # Record in governance report
        self._record_conflict(conflict, result)

        return result

    def set_conflict_strategy(self, strategy: ResolutionStrategy) -> None:
        """Set conflict resolution strategy"""
        if isinstance(strategy, str):
            # Convert string to ResolutionStrategy enum
            try:
                strategy = ResolutionStrategy(strategy)
            except ValueError:
                raise ValueError(f"Invalid conflict strategy: {strategy}. Must be one of: {list(ResolutionStrategy)}")
        elif not isinstance(strategy, ResolutionStrategy):
            raise ValueError(f"Invalid conflict strategy type: {type(strategy)}. Must be ResolutionStrategy or string")

        self.conflict_resolver.strategy = strategy

    def generate_governance_report(self) -> Dict[str, Any]:
        """Generate comprehensive governance report"""
        return {
            "registered_roles": len(self.registry.list_roles()),
            "roles": self.registry.to_dict(),
            "handoff_policy": self.handoff_manager.to_dict(),
            "conflict_strategy": self.conflict_resolver.strategy.value,
            "framework": self.framework,
            "recent_handoffs": self._governance_report.get("handoffs", []),
            "recent_conflicts": self._governance_report.get("conflicts", []),
        }

    def save_configuration(self, filepath: Union[str, Path]) -> None:
        """Save entire governance configuration to file"""
        filepath = Path(filepath)
        config = {
            "roles": self.registry.to_dict(),
            "handoff_policy": self.handoff_manager.to_dict(),
            "conflict_strategy": self.conflict_resolver.strategy.value,
            "framework": self.framework,
        }

        if filepath.suffix in ['.yaml', '.yml']:
            with open(filepath, 'w', encoding='utf-8') as f:
                yaml.dump(config, f, default_flow_style=False, allow_unicode=True)
        elif filepath.suffix == '.json':
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)

    def load_configuration(self, filepath: Union[str, Path]) -> None:
        """Load governance configuration from file"""
        filepath = Path(filepath)

        if filepath.suffix in ['.yaml', '.yml']:
            with open(filepath, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
        elif filepath.suffix == '.json':
            with open(filepath, 'r', encoding='utf-8') as f:
                config = json.load(f)

        # Clear existing roles
        self.registry._roles.clear()

        # Load roles
        for name, role_data in config.get("roles", {}).items():
            role_config = AgentRoleConfig(**role_data)
            self.registry.register_role(role_config)

        # Load handoff policy
        if "handoff_policy" in config:
            default_template = config["handoff_policy"].get("default_template")
            if default_template:
                # Ensure missing_input_action is converted to enum if it's a string
                if "missing_input_action" in default_template and isinstance(default_template["missing_input_action"], str):
                    default_template["missing_input_action"] = MissingInputAction(default_template["missing_input_action"])
                self.handoff_manager.template = HandoffTemplate(**default_template)

        # Load conflict strategy
        if "conflict_strategy" in config:
            self.conflict_resolver.strategy = ResolutionStrategy(config["conflict_strategy"])

        self.framework = config.get("framework", "openclaw")

    def _record_handoff(self, result: HandoffResult) -> None:
        """Record handoff in governance report"""
        if "handoffs" not in self._governance_report:
            self._governance_report["handoffs"] = []

        self._governance_report["handoffs"].append({
            "from": result.handoff_data.get("from"),
            "to": result.handoff_data.get("to"),
            "success": result.success,
            "timestamp": result.handoff_data.get("timestamp"),
        })

    def _record_conflict(self, conflict: AgentConflict, result: ResolutionResult) -> None:
        """Record conflict in governance report"""
        if "conflicts" not in self._governance_report:
            self._governance_report["conflicts"] = []

        self._governance_report["conflicts"].append({
            "agents": conflict.agents,
            "disagreement_type": conflict.disagreement_type,
            "severity": conflict.severity,
            "resolved": result.resolved,
            "decision_maker": result.decision_maker,
        })