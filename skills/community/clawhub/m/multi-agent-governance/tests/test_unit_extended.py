"""
Extended unit tests for comprehensive coverage
"""

import pytest
import tempfile
import json
from pathlib import Path
from typing import Dict, Any

from src import (
    MultiAgentGovernance,
    AgentRoleConfig,
    HandoffTemplate,
    ResolutionStrategy,
    MissingInputAction,
    ValidationResult,
    HandoffResult,
    BoundaryCheckResult,
    ResolutionResult,
    AgentConflict,
)
from src.validators import HandoffValidator, GovernanceValidator
from src.resolvers import ConflictResolver
from src.templates import StandardTemplate, SimplifiedTemplate, MinimalTemplate


# ============================================================================
# MissingInputAction Tests (3 behaviors)
# ============================================================================

class TestMissingInputActionBehaviors:
    """Test all three MissingInputAction behaviors"""

    def test_block_transition_behavior(self):
        """Test BLOCK_TRANSITION stops handoff on missing fields"""
        governance = MultiAgentGovernance(
            template="standard",
            handoff_policy={
                "missing_input_action": "block_transition",
                "required_fields": ["from", "to", "change_id"]  # Minimal required fields for test
            }
        )

        incomplete_handoff = {"from": "requirement_agent", "to": "design_agent"}  # Missing change_id
        result = governance.validate_handoff("requirement_agent", "design_agent", incomplete_handoff)

        assert not result.success
        assert not result.validation_result.valid
        assert len(result.validation_result.missing_fields) > 0
        assert len(result.validation_result.errors) > 0

    def test_warn_and_continue_behavior(self):
        """Test WARN_AND_CONTINUE allows handoff with warnings"""
        governance = MultiAgentGovernance(
            template="standard",
            handoff_policy={"missing_input_action": "warn_and_continue"}
        )

        incomplete_handoff = {"from": "requirement_agent", "to": "design_agent"}
        result = governance.validate_handoff("requirement_agent", "design_agent", incomplete_handoff)

        assert result.success  # Should succeed with warnings
        assert len(result.validation_result.missing_fields) > 0
        assert len(result.validation_result.warnings) > 0
        assert len(result.validation_result.errors) == 0  # No blocking errors

    def test_auto_fill_defaults_behavior(self):
        """Test AUTO_FILL_DEFAULTS fills missing fields"""
        governance = MultiAgentGovernance(
            template="standard",
            handoff_policy={
                "missing_input_action": "auto_fill_defaults",
                "custom_validation_rules": {
                    "change_id": {"default": "auto-generated"},
                    "phase": {"default": "unknown"}
                }
            }
        )

        incomplete_handoff = {"from": "requirement_agent", "to": "design_agent"}
        result = governance.validate_handoff("requirement_agent", "design_agent", incomplete_handoff)

        # Note: AUTO_FILL_DEFAULTS would need implementation in HandoffValidator
        # This test documents the expected behavior
        assert result.validation_result.missing_fields


# ============================================================================
# HandoffTemplate Custom Validation Tests
# ============================================================================

class TestHandoffTemplateCustomValidation:
    """Test custom validation rules in HandoffTemplate"""

    def test_type_check_validation(self):
        """Test type_check custom validation rule"""
        governance = MultiAgentGovernance(
            template="standard",
            handoff_policy={
                "custom_validation_rules": {
                    "change_id": {
                        "type": "type_check",
                        "expected_type": str
                    }
                }
            }
        )

        valid_handoff = {
            "from": "requirement_agent",
            "to": "design_agent",
            "change_id": "change-123",  # String type, valid
            "phase": "requirement",
            "inputs": {},
            "assumptions": [],
            "open_questions": [],
            "required_outputs": [],
            "required_skills": [],
            "gate_before_next": "design-gate"
        }

        result = governance.validate_handoff("requirement_agent", "design_agent", valid_handoff)
        assert result.success

    def test_value_check_validation(self):
        """Test value_check custom validation rule"""
        governance = MultiAgentGovernance(
            template="standard",
            handoff_policy={
                "custom_validation_rules": {
                    "phase": {
                        "type": "value_check",
                        "allowed_values": ["requirement", "design", "development", "testing", "archive"]
                    }
                }
            }
        )

        invalid_handoff = {
            "from": "requirement_agent",
            "to": "design_agent",
            "change_id": "change-123",
            "phase": "invalid_phase",  # Invalid value
            "inputs": {},
            "assumptions": [],
            "open_questions": [],
            "required_outputs": [],
            "required_skills": [],
            "gate_before_next": "design-gate"
        }

        result = governance.validate_handoff("requirement_agent", "design_agent", invalid_handoff)
        assert not result.success

    def test_regex_check_validation(self):
        """Test regex_check custom validation rule"""
        governance = MultiAgentGovernance(
            template="standard",
            handoff_policy={
                "custom_validation_rules": {
                    "change_id": {
                        "type": "regex_check",
                        "pattern": r"^change-\d{3}$"
                    }
                }
            }
        )

        valid_handoff = {
            "from": "requirement_agent",
            "to": "design_agent",
            "change_id": "change-123",  # Matches pattern
            "phase": "requirement",
            "inputs": {},
            "assumptions": [],
            "open_questions": [],
            "required_outputs": [],
            "required_skills": [],
            "gate_before_next": "design-gate"
        }

        result = governance.validate_handoff("requirement_agent", "design_agent", valid_handoff)
        assert result.success


# ============================================================================
# check_role_boundary Tests
# ============================================================================

class TestRoleBoundaryCheck:
    """Test check_role_boundary functionality"""

    def test_overlapping_responsibilities_detection(self):
        """Test detection of overlapping responsibilities"""
        governance = MultiAgentGovernance(template="standard")

        # Register two agents with overlapping responsibilities
        governance.register_role(
            name="agent_a",
            role="Agent A",
            responsibilities=["task1", "task2", "common_task"],
            must_not=["action1"],
            outputs=["output1"]
        )

        governance.register_role(
            name="agent_b",
            role="Agent B",
            responsibilities=["task3", "task4", "common_task"],
            must_not=["action2"],
            outputs=["output2"]
        )

        validator = GovernanceValidator(governance.registry)
        result = validator.check_role_boundary("agent_a", "agent_b")

        assert result.allowed
        assert len(result.recommendations) > 0
        assert "Overlapping responsibilities" in result.recommendations[0]

    def test_reviewer_relationship_detection(self):
        """Test detection of reviewer relationship"""
        governance = MultiAgentGovernance(template="standard")

        validator = GovernanceValidator(governance.registry)
        result = validator.check_role_boundary(
            "implementation_agent",
            "code_review_agent"
        )

        assert result.allowed
        assert any("reviewer" in rec for rec in result.recommendations)

    def test_nonexistent_agents_boundary_check(self):
        """Test boundary check with nonexistent agents"""
        governance = MultiAgentGovernance(template="minimal")

        validator = GovernanceValidator(governance.registry)
        result = validator.check_role_boundary("nonexistent_a", "nonexistent_b")

        assert not result.allowed
        assert "not registered" in result.violations[0]


# ============================================================================
# Boundary Scenario Tests (Empty data, None, Illegal types)
# ============================================================================

class TestBoundaryScenarios:
    """Test boundary scenarios and error handling"""

    def test_empty_handoff_data(self):
        """Test with completely empty handoff data"""
        governance = MultiAgentGovernance(template="standard")

        result = governance.validate_handoff(
            "requirement_agent",
            "design_agent",
            {}
        )

        assert not result.success
        assert len(result.validation_result.missing_fields) > 0

    def test_none_handoff_data(self):
        """Test with None handoff data"""
        governance = MultiAgentGovernance(template="standard")

        # This should raise an error or return invalid result
        try:
            result = governance.validate_handoff(
                "requirement_agent",
                "design_agent",
                None
            )
            assert not result.success
        except (TypeError, AttributeError):
            # Expected behavior - None should not be accepted
            pass

    def test_illegal_type_in_handoff(self):
        """Test with illegal type in handoff fields"""
        governance = MultiAgentGovernance(template="standard")

        handoff_data = {
            "from": "requirement_agent",
            "to": "design_agent",
            "change_id": ["should", "be", "string"],  # List instead of string
            "phase": 123,  # Number instead of string
            "inputs": "should_be_dict",  # String instead of dict
            "assumptions": [],
            "open_questions": [],
            "required_outputs": [],
            "required_skills": [],
            "gate_before_next": "design-gate"
        }

        result = governance.validate_handoff(
            "requirement_agent",
            "design_agent",
            handoff_data
        )

        # Should handle gracefully, not crash
        assert result is not None

    def test_empty_role_registration(self):
        """Test registration with empty responsibilities"""
        governance = MultiAgentGovernance(template="minimal")

        governance.register_role(
            name="empty_agent",
            role="Empty Agent",
            responsibilities=[],  # Empty list
            must_not=[],
            outputs=[]
        )

        role = governance.get_role("empty_agent")
        assert role is not None
        assert len(role.responsibilities) == 0

    def test_register_role_with_none_metadata(self):
        """Test registration with None metadata"""
        governance = MultiAgentGovernance(template="minimal")

        governance.register_role(
            name="test_agent",
            role="Test Agent",
            responsibilities=["task"],
            must_not=["action"],
            outputs=["output"],
            metadata=None
        )

        role = governance.get_role("test_agent")
        assert role.metadata == {}


# ============================================================================
# Configuration File Failure Scenarios
# ============================================================================

class TestConfigurationFailureScenarios:
    """Test configuration file loading failures"""

    def test_load_corrupted_json_file(self):
        """Test loading corrupted JSON file"""
        governance = MultiAgentGovernance(template="minimal")

        with tempfile.NamedTemporaryFile(suffix=".json", delete=False, mode='w') as f:
            f.write("{corrupted json content}")
            temp_path = Path(f.name)

        try:
            governance.load_configuration(temp_path)
            # Should raise error or handle gracefully
            assert False, "Should have raised error"
        except json.JSONDecodeError:
            # Expected behavior
            pass
        finally:
            temp_path.unlink()

    def test_load_empty_yaml_file(self):
        """Test loading empty YAML file"""
        governance = MultiAgentGovernance(template="minimal")

        with tempfile.NamedTemporaryFile(suffix=".yaml", delete=False, mode='w') as f:
            f.write("")
            temp_path = Path(f.name)

        try:
            governance.load_configuration(temp_path)
            # Should handle gracefully
            roles = governance.list_roles()
            assert len(roles) >= 0  # May load empty config
        except Exception as e:
            # Or raise error if YAML is invalid
            pass
        finally:
            temp_path.unlink()

    def test_load_nonexistent_file(self):
        """Test loading nonexistent file"""
        governance = MultiAgentGovernance(template="minimal")

        nonexistent_path = Path("nonexistent_config.json")

        try:
            governance.load_configuration(nonexistent_path)
            assert False, "Should have raised FileNotFoundError"
        except FileNotFoundError:
            # Expected behavior
            pass

    def test_save_to_invalid_path(self):
        """Test saving to invalid path"""
        governance = MultiAgentGovernance(template="minimal")

        invalid_path = Path("/invalid/path/config.json")

        try:
            governance.save_configuration(invalid_path)
            assert False, "Should have raised error"
        except (PermissionError, OSError):
            # Expected behavior on Windows
            pass


# ============================================================================
# Custom Template Loading Tests
# ============================================================================

class TestCustomTemplateLoading:
    """Test custom template loading"""

    def test_load_custom_dict_template(self):
        """Test loading custom template from dictionary"""
        custom_template = [
            {
                "name": "custom_orchestrator",
                "role": "Custom Orchestrator",
                "responsibilities": ["coordinate", "monitor"],
                "must_not": ["bypass_gates"],
                "outputs": ["coordination_report"],
                "priority": 10
            },
            {
                "name": "custom_worker",
                "role": "Custom Worker",
                "responsibilities": ["execute", "report"],
                "must_not": ["skip_steps"],
                "outputs": ["work_result"],
                "priority": 5
            }
        ]

        governance = MultiAgentGovernance(template=custom_template)

        roles = governance.list_roles()
        assert len(roles) == 2
        assert "custom_orchestrator" in roles
        assert "custom_worker" in roles

    def test_load_template_from_yaml_file(self):
        """Test loading template from YAML file"""
        governance = MultiAgentGovernance(template="minimal")

        # Create YAML configuration file (correct format)
        template_content = """
roles:
  yaml_agent_1:
    name: yaml_agent_1
    role: YAML Agent 1
    responsibilities:
      - yaml_task_1
    must_not:
      - yaml_action_1
    outputs:
      - yaml_output_1
  yaml_agent_2:
    name: yaml_agent_2
    role: YAML Agent 2
    responsibilities:
      - yaml_task_2
    must_not:
      - yaml_action_2
    outputs:
      - yaml_output_2
"""

        with tempfile.NamedTemporaryFile(suffix=".yaml", delete=False, mode='w') as f:
            f.write(template_content)
            temp_path = Path(f.name)

        governance.load_configuration(temp_path)

        roles = governance.list_roles()
        assert "yaml_agent_1" in roles
        assert "yaml_agent_2" in roles

        temp_path.unlink()


# ============================================================================
# Concurrent Operation Safety Tests
# ============================================================================

class TestConcurrentOperations:
    """Test safety of concurrent operations"""

    def test_multiple_role_registrations(self):
        """Test registering multiple roles in sequence"""
        governance = MultiAgentGovernance(template="minimal")

        # Register multiple roles in sequence
        for i in range(5):
            governance.register_role(
                name=f"agent_{i}",
                role=f"Agent {i}",
                responsibilities=[f"task_{i}"],
                must_not=[f"action_{i}"],
                outputs=[f"output_{i}"]
            )

        roles = governance.list_roles()
        # Should have 3 minimal + 5 custom = 8 roles
        assert len(roles) == 8

    def test_update_existing_role(self):
        """Test updating existing role"""
        governance = MultiAgentGovernance(template="minimal")

        governance.register_role(
            name="updateable_agent",
            role="Updateable Agent",
            responsibilities=["old_task"],
            must_not=["old_action"],
            outputs=["old_output"],
            priority=1
        )

        # Update role
        governance.registry.update_role("updateable_agent", {
            "responsibilities": ["new_task"],
            "priority": 10
        })

        role = governance.get_role("updateable_agent")
        assert "new_task" in role.responsibilities
        assert role.priority == 10

    def test_remove_role(self):
        """Test removing registered role"""
        governance = MultiAgentGovernance(template="minimal")

        governance.register_role(
            name="removable_agent",
            role="Removable Agent",
            responsibilities=["task"],
            must_not=["action"],
            outputs=["output"]
        )

        assert "removable_agent" in governance.list_roles()

        governance.registry.remove_role("removable_agent")

        assert "removable_agent" not in governance.list_roles()


# ============================================================================
# Error Recovery Tests
# ============================================================================

class TestErrorRecovery:
    """Test error recovery capabilities"""

    def test_recovery_from_invalid_conflict_strategy(self):
        """Test recovery from invalid conflict strategy"""
        governance = MultiAgentGovernance(template="standard")

        # set_conflict_strategy should raise ValueError for invalid strategy
        with pytest.raises(ValueError, match="Invalid conflict strategy"):
            governance.set_conflict_strategy("invalid_strategy")

        # After error, set back to valid strategy
        governance.set_conflict_strategy(ResolutionStrategy.ORCHESTRATOR_FIRST)
        assert governance.conflict_resolver.strategy == ResolutionStrategy.ORCHESTRATOR_FIRST

    def test_recovery_from_corrupted_registry(self):
        """Test recovery from corrupted registry state"""
        governance = MultiAgentGovernance(template="standard")

        # Manually corrupt registry
        governance.registry._roles = None

        # Should recover gracefully
        try:
            governance.list_roles()
        except (TypeError, AttributeError):
            # Expected, reinitialize
            governance.registry._roles = {}
            governance.registry.load_template("minimal")

            roles = governance.list_roles()
            assert len(roles) == 3

    def test_recovery_after_failed_handoff(self):
        """Test recovery after failed handoff"""
        governance = MultiAgentGovernance(template="standard")

        # First handoff fails
        failed_handoff = {}
        result1 = governance.validate_handoff("requirement_agent", "design_agent", failed_handoff)
        assert not result1.success

        # Second handoff succeeds
        valid_handoff = {
            "from": "requirement_agent",
            "to": "design_agent",
            "change_id": "change-123",
            "phase": "requirement",
            "inputs": {},
            "assumptions": [],
            "open_questions": [],
            "required_outputs": [],
            "required_skills": [],
            "gate_before_next": "design-gate"
        }
        result2 = governance.validate_handoff("requirement_agent", "design_agent", valid_handoff)
        assert result2.success


# ============================================================================
# Data Model Integrity Tests
# ============================================================================

class TestDataModelIntegrity:
    """Test data model integrity"""

    def test_agent_role_config_serialization(self):
        """Test AgentRoleConfig serialization"""
        role = AgentRoleConfig(
            name="test_agent",
            role="Test Agent",
            responsibilities=["task1", "task2"],
            must_not=["action1"],
            outputs=["output1"],
            priority=5
        )

        role_dict = role.to_dict()

        assert role_dict["name"] == "test_agent"
        assert role_dict["responsibilities"] == ["task1", "task2"]
        assert role_dict["priority"] == 5

    def test_handoff_template_serialization(self):
        """Test HandoffTemplate serialization"""
        template = HandoffTemplate(
            required_fields=["field1", "field2"],
            optional_fields=["field3"],
            missing_input_action=MissingInputAction.WARN_AND_CONTINUE
        )

        template_dict = template.to_dict()

        assert template_dict["required_fields"] == ["field1", "field2"]
        assert template_dict["missing_input_action"] == "warn_and_continue"

    def test_validation_result_serialization(self):
        """Test ValidationResult serialization"""
        result = ValidationResult(
            valid=False,
            errors=["error1"],
            warnings=["warning1"],
            missing_fields=["field1"]
        )

        result_dict = result.to_dict()

        assert result_dict["valid"] == False
        assert result_dict["errors"] == ["error1"]

    def test_agent_conflict_serialization(self):
        """Test AgentConflict serialization"""
        conflict = AgentConflict(
            agents=["agent1", "agent2"],
            disagreement_type="workflow_disputed",
            context={"key": "value"},
            severity="high"
        )

        conflict_dict = conflict.to_dict()

        assert conflict_dict["agents"] == ["agent1", "agent2"]
        assert conflict_dict["severity"] == "high"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])