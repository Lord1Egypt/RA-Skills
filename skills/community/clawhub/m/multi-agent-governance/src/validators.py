"""
Validators for governance system
"""

from typing import Dict, Any, List
from .models import (
    ValidationResult,
    BoundaryCheckResult,
    HandoffTemplate,
    MissingInputAction,
)


class HandoffValidator:
    """Validator for agent handoffs"""

    def __init__(self, template: HandoffTemplate):
        self.template = template

    def validate(self, handoff_data: Dict[str, Any]) -> ValidationResult:
        """Validate a handoff against the template"""
        errors = []
        warnings = []
        missing_fields = []

        # Handle None or invalid handoff_data
        if handoff_data is None or not isinstance(handoff_data, dict):
            errors.append("Handoff data must be a dictionary")
            return ValidationResult(
                valid=False,
                errors=errors,
                warnings=warnings,
                missing_fields=list(self.template.required_fields)
            )

        # Check required fields
        for field in self.template.required_fields:
            if field not in handoff_data:
                missing_fields.append(field)
                if self.template.missing_input_action == MissingInputAction.BLOCK_TRANSITION:
                    errors.append(f"Missing required field: {field}")
                elif self.template.missing_input_action == MissingInputAction.WARN_AND_CONTINUE:
                    warnings.append(f"Missing required field: {field}")
                elif self.template.missing_input_action == MissingInputAction.AUTO_FILL_DEFAULTS:
                    # Auto-fill would be handled elsewhere, just warn for now
                    warnings.append(f"Missing required field: {field}")

        # Check optional fields (only warn if missing)
        for field in self.template.optional_fields:
            if field not in handoff_data:
                warnings.append(f"Missing optional field: {field}")

        # Apply custom validation rules
        for field, rule in self.template.custom_validation_rules.items():
            if field in handoff_data:
                value = handoff_data[field]
                if not self._apply_custom_rule(value, rule):
                    errors.append(f"Custom validation failed for field '{field}'")

        valid = len(errors) == 0

        return ValidationResult(
            valid=valid,
            errors=errors,
            warnings=warnings,
            missing_fields=missing_fields
        )

    def _apply_custom_rule(self, value: Any, rule: Dict[str, Any]) -> bool:
        """Apply a custom validation rule"""
        rule_type = rule.get("type")

        if rule_type == "type_check":
            expected_type = rule.get("expected_type")
            return isinstance(value, expected_type)

        elif rule_type == "value_check":
            allowed_values = rule.get("allowed_values")
            return value in allowed_values

        elif rule_type == "regex_check":
            import re
            pattern = rule.get("pattern")
            return bool(re.match(pattern, str(value)))

        elif rule_type == "custom_function":
            func = rule.get("function")
            return func(value)

        return True


class GovernanceValidator:
    """Validator for agent governance rules"""

    def __init__(self, registry):
        self.registry = registry

    def validate_agent_action(self, agent: str, action: str) -> BoundaryCheckResult:
        """Validate if an agent can perform an action"""
        role = self.registry.get_role(agent)

        if not role:
            return BoundaryCheckResult(
                allowed=False,
                violations=[f"Agent '{agent}' not registered"],
                recommendations=["Register the agent role first"]
            )

        violations = []
        recommendations = []

        # Check if action is in must_not list
        for must_not_action in role.must_not:
            if self._action_matches(action, must_not_action):
                violations.append(f"Agent '{agent}' cannot: {must_not_action}")
                recommendations.append(f"Transfer this action to another agent or request user approval")

        # Check if action aligns with responsibilities
        action_allowed = False
        for responsibility in role.responsibilities:
            if self._action_matches(action, responsibility):
                action_allowed = True
                break

        if not action_allowed and len(violations) == 0:
            recommendations.append(f"Action '{action}' not explicitly in responsibilities. Consider adding it.")

        allowed = len(violations) == 0

        return BoundaryCheckResult(
            allowed=allowed,
            violations=violations,
            recommendations=recommendations
        )

    def check_role_boundary(self, agent: str, target_agent: str) -> BoundaryCheckResult:
        """Check if two agents have overlapping responsibilities"""
        agent_role = self.registry.get_role(agent)
        target_role = self.registry.get_role(target_agent)

        if not agent_role or not target_role:
            return BoundaryCheckResult(
                allowed=False,
                violations=["One or both agents not registered"],
                recommendations=["Register both agent roles first"]
            )

        violations = []
        recommendations = []

        # Check for overlapping responsibilities
        overlapping = []
        for resp in agent_role.responsibilities:
            if resp in target_role.responsibilities:
                overlapping.append(resp)

        if overlapping:
            warnings_msg = f"Overlapping responsibilities: {', '.join(overlapping)}"
            recommendations.append(f"Clarify which agent handles: {warnings_msg}")

        # Check if target is reviewer for agent
        if target_role.reviewer_for == agent:
            recommendations.append(f"'{target_agent}' is designated reviewer for '{agent}'")

        return BoundaryCheckResult(
            allowed=True,
            violations=violations,
            recommendations=recommendations
        )

    def _action_matches(self, action: str, pattern: str) -> bool:
        """Check if an action matches a pattern"""
        # Direct match (exact match)
        action_lower = action.lower().strip()
        pattern_lower = pattern.lower().strip()

        if action_lower == pattern_lower:
            return True

        # For must_not patterns, we want strict matching to avoid false positives
        # Only match if the action is clearly trying to do the forbidden behavior
        # Example: "Skip security and performance checks" should NOT match "Review correctness and security"

        # Keyword match with semantic understanding
        action_keywords = set(action_lower.split())
        pattern_keywords = set(pattern_lower.split())

        # For must_not patterns like "Skip X", only match actions that contain "skip" or similar negation words
        negation_words = ["skip", "bypass", "ignore", "avoid", "omit"]

        has_negation_in_pattern = any(neg_word in pattern_lower for neg_word in negation_words)
        has_negation_in_action = any(neg_word in action_lower for neg_word in negation_words)

        # If pattern has negation but action doesn't, it's not a match
        if has_negation_in_pattern and not has_negation_in_action:
            return False

        # If both have negation and share significant keywords, it's likely a match
        if has_negation_in_pattern and has_negation_in_action:
            # Check if they share meaningful keywords beyond negation words
            shared_keywords = action_keywords & pattern_keywords
            meaningful_shared = shared_keywords - set(negation_words)
            if len(meaningful_shared) > 0:
                return True

        # For non-negation patterns, use more lenient matching
        if not has_negation_in_pattern:
            # Substring match for non-negation patterns
            if pattern_lower in action_lower or action_lower in pattern_lower:
                return True
            # Keyword overlap for non-negation patterns
            if len(action_keywords & pattern_keywords) >= 2:  # At least 2 shared keywords
                return True

        return False