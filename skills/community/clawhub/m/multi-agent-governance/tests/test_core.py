"""
Tests for Multi-Agent Governance System
"""

import pytest
import tempfile
import json
from pathlib import Path

from src import (
    MultiAgentGovernance,
    AgentRoleConfig,
    HandoffTemplate,
    ResolutionStrategy,
    ValidationResult,
)
from src.templates import StandardTemplate, SimplifiedTemplate, MinimalTemplate


class TestAgentRoleRegistry:
    """Test AgentRoleRegistry functionality"""

    def test_register_role(self):
        """Test registering a new role"""
        governance = MultiAgentGovernance(template="minimal")
        governance.register_role(
            name="test_agent",
            role="Test Agent",
            responsibilities=["test_task"],
            must_not=["bypass_gate"],
            outputs=["test_output"]
        )

        assert "test_agent" in governance.list_roles()
        role = governance.get_role("test_agent")
        assert role.role == "Test Agent"

    def test_register_duplicate_role(self):
        """Test registering duplicate role raises error"""
        governance = MultiAgentGovernance(template="minimal")
        governance.register_role(
            name="test_agent",
            role="Test Agent",
            responsibilities=["test_task"],
            must_not=["bypass_gate"],
            outputs=["test_output"]
        )

        with pytest.raises(ValueError, match="already registered"):
            governance.register_role(
                name="test_agent",
                role="Test Agent 2",
                responsibilities=["test_task2"],
                must_not=["bypass_gate"],
                outputs=["test_output2"]
            )

    def test_load_standard_template(self):
        """Test loading standard template"""
        governance = MultiAgentGovernance(template="standard")
        roles = governance.list_roles()

        assert len(roles) == 9
        assert "orchestrator_agent" in roles
        assert "requirement_agent" in roles
        assert "implementation_agent" in roles

    def test_load_simplified_template(self):
        """Test loading simplified template"""
        governance = MultiAgentGovernance(template="simplified")
        roles = governance.list_roles()

        assert len(roles) == 5
        assert "orchestrator_agent" in roles
        assert "verification_agent" in roles

    def test_load_minimal_template(self):
        """Test loading minimal template"""
        governance = MultiAgentGovernance(template="minimal")
        roles = governance.list_roles()

        assert len(roles) == 3
        assert "orchestrator_agent" in roles


class TestHandoffPolicyManager:
    """Test HandoffPolicyManager functionality"""

    def test_validate_handoff_success(self):
        """Test successful handoff validation"""
        governance = MultiAgentGovernance(template="standard")

        handoff_data = {
            "from": "requirement_agent",
            "to": "design_agent",
            "change_id": "change-123",
            "phase": "requirement",
            "inputs": {"proposal.md": "content"},
            "assumptions": [],
            "open_questions": [],
            "required_outputs": ["design.md"],
            "required_skills": [],
            "gate_before_next": "design-gate"
        }

        result = governance.validate_handoff(
            from_agent="requirement_agent",
            to_agent="design_agent",
            handoff_data=handoff_data
        )

        assert result.success
        assert result.validation_result.valid

    def test_validate_handoff_missing_fields(self):
        """Test handoff validation with missing fields"""
        governance = MultiAgentGovernance(template="standard")

        handoff_data = {
            "from": "requirement_agent",
            "to": "design_agent",
            # Missing required fields
        }

        result = governance.validate_handoff(
            from_agent="requirement_agent",
            to_agent="design_agent",
            handoff_data=handoff_data
        )

        assert not result.success
        assert not result.validation_result.valid
        assert len(result.validation_result.missing_fields) > 0

    def test_validate_handoff_nonexistent_agent(self):
        """Test handoff with non-existent agent"""
        governance = MultiAgentGovernance(template="minimal")

        handoff_data = {"from": "nonexistent_agent", "to": "implementation_agent"}

        result = governance.validate_handoff(
            from_agent="nonexistent_agent",
            to_agent="implementation_agent",
            handoff_data=handoff_data
        )

        assert not result.success
        assert "not registered" in result.validation_result.errors[0]


class TestConflictResolver:
    """Test ConflictResolver functionality"""

    def test_orchestrator_first_strategy(self):
        """Test orchestrator-first conflict resolution"""
        governance = MultiAgentGovernance(
            template="standard",
            conflict_strategy=ResolutionStrategy.ORCHESTRATOR_FIRST
        )

        result = governance.resolve_conflict(
            agents=["design_agent", "implementation_agent"],
            disagreement_type="workflow_selection_disputed",
            context={"proposal": "...", "design": "..."}
        )

        assert result.resolved
        assert result.decision_maker == "orchestrator_agent"
        assert "standard_change workflow" in result.final_decision

    def test_user_first_strategy(self):
        """Test user-first conflict resolution"""
        governance = MultiAgentGovernance(
            template="standard",
            conflict_strategy=ResolutionStrategy.USER_FIRST
        )

        result = governance.resolve_conflict(
            agents=["design_agent", "implementation_agent"],
            disagreement_type="scope_or_risk_disputed",
            context={"proposal": "...", "design": "..."}
        )

        assert not result.resolved
        assert result.decision_maker == "user"
        assert len(result.alternative_options) > 0

    def test_voting_strategy(self):
        """Test voting-based conflict resolution"""
        governance = MultiAgentGovernance(
            template="standard",
            conflict_strategy=ResolutionStrategy.VOTING
        )

        result = governance.resolve_conflict(
            agents=["requirement_agent", "implementation_agent"],
            disagreement_type="gate_result_disputed",
            context={}
        )

        assert result.resolved
        assert "highest priority" in result.final_decision


class TestGovernanceValidator:
    """Test GovernanceValidator functionality"""

    def test_validate_allowed_action(self):
        """Test validation of allowed action"""
        governance = MultiAgentGovernance(template="standard")

        result = governance.validate_agent_action(
            agent="implementation_agent",
            action="Implement approved tasks"
        )

        assert result.allowed

    def test_validate_disallowed_action(self):
        """Test validation of disallowed action"""
        governance = MultiAgentGovernance(template="standard")

        result = governance.validate_agent_action(
            agent="implementation_agent",
            action="Expand scope without returning to requirement or design"
        )

        assert not result.allowed
        assert len(result.violations) > 0

    def test_validate_nonexistent_agent(self):
        """Test validation for non-existent agent"""
        governance = MultiAgentGovernance(template="minimal")

        result = governance.validate_agent_action(
            agent="nonexistent_agent",
            action="some_action"
        )

        assert not result.allowed
        assert "not registered" in result.violations[0]


class TestMultiAgentGovernance:
    """Test MultiAgentGovernance main class"""

    def test_initialization(self):
        """Test governance initialization"""
        governance = MultiAgentGovernance(template="standard")

        assert len(governance.list_roles()) == 9
        assert governance.framework == "openclaw"
        assert governance.conflict_resolver.strategy == ResolutionStrategy.ORCHESTRATOR_FIRST

    def test_custom_framework(self):
        """Test custom framework setting"""
        governance = MultiAgentGovernance(
            template="simplified",
            framework="langchain"
        )

        assert governance.framework == "langchain"

    def test_generate_governance_report(self):
        """Test governance report generation"""
        governance = MultiAgentGovernance(template="standard")

        report = governance.generate_governance_report()

        assert report["registered_roles"] == 9
        assert "roles" in report
        assert "handoff_policy" in report
        assert "framework" in report

    def test_save_and_load_configuration(self):
        """Test saving and loading configuration"""
        governance = MultiAgentGovernance(template="standard")

        with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as f:
            temp_path = Path(f.name)

        governance.save_configuration(temp_path)

        # Load into new governance instance
        governance2 = MultiAgentGovernance(template="minimal")
        governance2.load_configuration(temp_path)

        assert len(governance2.list_roles()) == 9
        assert governance2.framework == "openclaw"

        # Clean up
        temp_path.unlink()

    def test_yaml_configuration(self):
        """Test YAML configuration saving and loading"""
        governance = MultiAgentGovernance(template="simplified")

        with tempfile.NamedTemporaryFile(suffix=".yaml", delete=False) as f:
            temp_path = Path(f.name)

        governance.save_configuration(temp_path)

        governance2 = MultiAgentGovernance(template="minimal")
        governance2.load_configuration(temp_path)

        assert len(governance2.list_roles()) == 5

        # Clean up
        temp_path.unlink()


class TestTemplates:
    """Test predefined templates"""

    def test_standard_template_roles(self):
        """Test standard template roles"""
        roles = StandardTemplate.get_roles()

        assert len(roles) == 9
        assert all("name" in role for role in roles)
        assert all("responsibilities" in role for role in roles)

    def test_simplified_template_roles(self):
        """Test simplified template roles"""
        roles = SimplifiedTemplate.get_roles()

        assert len(roles) == 5

    def test_minimal_template_roles(self):
        """Test minimal template roles"""
        roles = MinimalTemplate.get_roles()

        assert len(roles) == 3


if __name__ == "__main__":
    pytest.main([__file__, "-v"])