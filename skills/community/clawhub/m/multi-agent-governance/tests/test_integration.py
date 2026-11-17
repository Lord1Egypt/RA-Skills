"""
Integration tests for complete workflows
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
    MissingInputAction,
)


# ============================================================================
# YAML/JSON Serialization Complete Workflow Tests
# ============================================================================

class TestSerializationWorkflow:
    """Test complete serialization and deserialization workflows"""

    def test_yaml_save_load_preserves_roles(self):
        """Test YAML serialization preserves all roles"""
        governance = MultiAgentGovernance(template="standard")

        # Add custom roles
        governance.register_role(
            name="custom_agent_1",
            role="Custom Agent 1",
            responsibilities=["custom_task"],
            must_not=["custom_action"],
            outputs=["custom_output"],
            priority=8
        )

        governance.register_role(
            name="custom_agent_2",
            role="Custom Agent 2",
            responsibilities=["another_task"],
            must_not=["another_action"],
            outputs=["another_output"],
            priority=6
        )

        # Save to YAML
        with tempfile.NamedTemporaryFile(suffix=".yaml", delete=False) as f:
            temp_path = Path(f.name)

        governance.save_configuration(temp_path)

        # Load into new instance
        governance2 = MultiAgentGovernance(template="minimal")
        governance2.load_configuration(temp_path)

        # Verify all roles preserved
        roles = governance2.list_roles()
        assert len(roles) == 11  # 9 standard + 2 custom
        assert "custom_agent_1" in roles
        assert "custom_agent_2" in roles

        # Verify role details preserved
        custom_role = governance2.get_role("custom_agent_1")
        assert custom_role.role == "Custom Agent 1"
        assert custom_role.priority == 8

        temp_path.unlink()

    def test_json_save_load_preserves_governance_state(self):
        """Test JSON serialization preserves governance state"""
        governance = MultiAgentGovernance(
            template="standard",
            handoff_policy={
                "required_fields": ["from", "to", "inputs"],
                "missing_input_action": "warn_and_continue"
            }
        )

        # Set custom conflict strategy
        governance.set_conflict_strategy(ResolutionStrategy.USER_FIRST)

        # Save to JSON
        with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as f:
            temp_path = Path(f.name)

        governance.save_configuration(temp_path)

        # Load into new instance
        governance2 = MultiAgentGovernance(template="minimal")
        governance2.load_configuration(temp_path)

        # Verify governance state preserved
        assert governance2.conflict_resolver.strategy == ResolutionStrategy.USER_FIRST
        assert governance2.framework == "openclaw"

        # Verify handoff policy preserved
        assert governance2.handoff_manager.template.missing_input_action == MissingInputAction.WARN_AND_CONTINUE

        temp_path.unlink()

    def test_cross_format_conversion(self):
        """Test conversion between YAML and JSON formats"""
        governance = MultiAgentGovernance(template="standard")

        # Save to YAML
        with tempfile.NamedTemporaryFile(suffix=".yaml", delete=False) as f:
            yaml_path = Path(f.name)
        governance.save_configuration(yaml_path)

        # Load from YAML and save to JSON
        governance2 = MultiAgentGovernance(template="minimal")
        governance2.load_configuration(yaml_path)

        with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as f:
            json_path = Path(f.name)
        governance2.save_configuration(json_path)

        # Load from JSON
        governance3 = MultiAgentGovernance(template="minimal")
        governance3.load_configuration(json_path)

        # Verify consistency
        assert len(governance3.list_roles()) == len(governance.list_roles())

        yaml_path.unlink()
        json_path.unlink()


# ============================================================================
# Configuration Persistence and Recovery Tests
# ============================================================================

class TestConfigurationPersistence:
    """Test configuration persistence and recovery"""

    def test_multiple_save_operations(self):
        """Test multiple save operations preserve latest state"""
        governance = MultiAgentGovernance(template="minimal")

        # First state
        governance.register_role(
            name="agent_v1",
            role="Agent V1",
            responsibilities=["task_v1"],
            must_not=["action_v1"],
            outputs=["output_v1"]
        )

        with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as f:
            temp_path = Path(f.name)
        governance.save_configuration(temp_path)

        # Second state
        governance.register_role(
            name="agent_v2",
            role="Agent V2",
            responsibilities=["task_v2"],
            must_not=["action_v2"],
            outputs=["output_v2"]
        )
        governance.save_configuration(temp_path)

        # Load and verify second state
        governance2 = MultiAgentGovernance(template="minimal")
        governance2.load_configuration(temp_path)

        roles = governance2.list_roles()
        assert "agent_v1" in roles
        assert "agent_v2" in roles

        temp_path.unlink()

    def test_incremental_configuration_updates(self):
        """Test incremental configuration updates"""
        governance = MultiAgentGovernance(template="minimal")

        # Initial configuration
        with tempfile.NamedTemporaryFile(suffix=".yaml", delete=False) as f:
            temp_path = Path(f.name)

        governance.save_configuration(temp_path)

        # Incremental updates
        for i in range(3):
            governance.register_role(
                name=f"incremental_agent_{i}",
                role=f"Incremental Agent {i}",
                responsibilities=[f"task_{i}"],
                must_not=[f"action_{i}"],
                outputs=[f"output_{i}"]
            )
            governance.save_configuration(temp_path)

        # Final load
        governance2 = MultiAgentGovernance(template="minimal")
        governance2.load_configuration(temp_path)

        roles = governance2.list_roles()
        assert len(roles) == 6  # 3 minimal + 3 incremental

        temp_path.unlink()

    def test_configuration_recovery_after_crash_simulation(self):
        """Test configuration recovery after simulated crash"""
        governance = MultiAgentGovernance(template="standard")

        # Create and save configuration
        with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as f:
            temp_path = Path(f.name)

        governance.save_configuration(temp_path)

        # Simulate crash - destroy governance instance
        governance_destroyed = None

        # Recover from saved configuration
        governance_recovered = MultiAgentGovernance(template="minimal")
        governance_recovered.load_configuration(temp_path)

        # Verify recovery successful
        assert len(governance_recovered.list_roles()) == 9
        assert governance_recovered.framework == "openclaw"

        temp_path.unlink()


# ============================================================================
# Framework Adapter Compatibility Tests
# ============================================================================

class TestFrameworkAdapters:
    """Test compatibility with different frameworks"""

    def test_openclaw_framework_adapter(self):
        """Test OpenClaw framework compatibility"""
        governance = MultiAgentGovernance(
            template="standard",
            framework="openclaw"
        )

        assert governance.framework == "openclaw"

        # Verify standard handoff works
        handoff_data = {
            "from": "requirement_agent",
            "to": "design_agent",
            "change_id": "change-openclaw",
            "phase": "requirement",
            "inputs": {},
            "assumptions": [],
            "open_questions": [],
            "required_outputs": [],
            "required_skills": [],
            "gate_before_next": "design-gate"
        }

        result = governance.validate_handoff("requirement_agent", "design_agent", handoff_data)
        assert result.success

    def test_langchain_framework_adapter(self):
        """Test LangChain framework compatibility"""
        governance = MultiAgentGovernance(
            template="simplified",
            framework="langchain"
        )

        assert governance.framework == "langchain"

        # Verify simplified workflow works
        roles = governance.list_roles()
        assert len(roles) == 5

    def test_autogen_framework_adapter(self):
        """Test AutoGen framework compatibility"""
        governance = MultiAgentGovernance(
            template="minimal",
            framework="autogen"
        )

        assert governance.framework == "autogen"

        # Verify minimal workflow works
        roles = governance.list_roles()
        assert len(roles) == 3

    def test_framework_switch_preserves_roles(self):
        """Test switching frameworks preserves roles"""
        governance = MultiAgentGovernance(
            template="standard",
            framework="openclaw"
        )

        # Add custom role
        governance.register_role(
            name="custom_role",
            role="Custom Role",
            responsibilities=["custom_task"],
            must_not=["custom_action"],
            outputs=["custom_output"]
        )

        # Save configuration
        with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as f:
            temp_path = Path(f.name)
        governance.save_configuration(temp_path)

        # Load with different framework
        governance2 = MultiAgentGovernance(template="minimal", framework="langchain")
        governance2.load_configuration(temp_path)

        # Verify roles preserved but framework changed
        roles = governance2.list_roles()
        assert len(roles) == 10  # 9 standard + 1 custom
        assert governance2.framework == "openclaw"  # Framework from config

        temp_path.unlink()


# ============================================================================
# Multi-format Configuration File Tests
# ============================================================================

class TestMultiFormatConfiguration:
    """Test configuration files in multiple formats"""

    def test_yaml_with_complex_structure(self):
        """Test YAML with complex nested structure"""
        governance = MultiAgentGovernance(template="standard")

        # Add roles with complex metadata
        governance.register_role(
            name="complex_agent",
            role="Complex Agent",
            responsibilities=["task1", "task2"],
            must_not=["action1", "action2"],
            outputs=["output1", "output2"],
            metadata={
                "nested": {
                    "level1": {
                        "level2": "value"
                    }
                },
                "list": [1, 2, 3],
                "special_chars": "中文测试"
            }
        )

        # Save to YAML
        with tempfile.NamedTemporaryFile(suffix=".yaml", delete=False) as f:
            temp_path = Path(f.name)
        governance.save_configuration(temp_path)

        # Load and verify complex structure preserved
        governance2 = MultiAgentGovernance(template="minimal")
        governance2.load_configuration(temp_path)

        role = governance2.get_role("complex_agent")
        assert role.metadata["nested"]["level1"]["level2"] == "value"
        assert role.metadata["list"] == [1, 2, 3]
        assert role.metadata["special_chars"] == "中文测试"

        temp_path.unlink()

    def test_json_with_unicode_content(self):
        """Test JSON with Unicode content"""
        governance = MultiAgentGovernance(template="standard")

        governance.register_role(
            name="unicode_agent",
            role="Unicode 中文角色",
            responsibilities=["中文任务", "English Task"],
            must_not=["中文禁止动作"],
            outputs=["输出结果"],
            metadata={"描述": "这是一个测试"}
        )

        # Save to JSON
        with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as f:
            temp_path = Path(f.name)
        governance.save_configuration(temp_path)

        # Load and verify Unicode preserved
        governance2 = MultiAgentGovernance(template="minimal")
        governance2.load_configuration(temp_path)

        role = governance2.get_role("unicode_agent")
        assert role.role == "Unicode 中文角色"
        assert "中文任务" in role.responsibilities

        temp_path.unlink()


# ============================================================================
# Governance Report Integration Tests
# ============================================================================

class TestGovernanceReportIntegration:
    """Test governance report generation with real data"""

    def test_report_after_multiple_operations(self):
        """Test report generation after multiple operations"""
        governance = MultiAgentGovernance(template="standard")

        # Perform multiple handoffs
        for i in range(3):
            handoff_data = {
                "from": "requirement_agent",
                "to": "design_agent",
                "change_id": f"change-{i}",
                "phase": "requirement",
                "inputs": {},
                "assumptions": [],
                "open_questions": [],
                "required_outputs": [],
                "required_skills": [],
                "gate_before_next": "design-gate",
                "timestamp": f"2026-07-02T{i}:00:00Z"
            }
            governance.validate_handoff("requirement_agent", "design_agent", handoff_data)

        # Perform multiple conflict resolutions
        for i in range(2):
            governance.resolve_conflict(
                agents=["design_agent", "implementation_agent"],
                disagreement_type="workflow_selection_disputed",
                context={"proposal": f"proposal-{i}"}
            )

        # Generate report
        report = governance.generate_governance_report()

        assert len(report["recent_handoffs"]) == 3
        assert len(report["recent_conflicts"]) == 2
        assert report["registered_roles"] == 9

    def test_report_persistence(self):
        """Test report persistence across save/load"""
        governance = MultiAgentGovernance(template="standard")

        # Perform operations
        handoff_data = {
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
        governance.validate_handoff("requirement_agent", "design_agent", handoff_data)

        governance.resolve_conflict(
            agents=["design_agent", "implementation_agent"],
            disagreement_type="scope_or_risk_disputed",
            context={}
        )

        # Save configuration
        with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as f:
            temp_path = Path(f.name)
        governance.save_configuration(temp_path)

        # Load and generate report
        governance2 = MultiAgentGovernance(template="minimal")
        governance2.load_configuration(temp_path)

        # Note: Governance report (handoffs/conflicts) is not persisted in config
        # This test documents expected behavior
        report = governance2.generate_governance_report()
        assert report["registered_roles"] == 9

        temp_path.unlink()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])