"""
End-to-end tests for complete multi-agent workflows
"""

import pytest
from datetime import datetime

from src import (
    MultiAgentGovernance,
    ResolutionStrategy,
)


# ============================================================================
# Standard 9-Agent Complete Workflow Test
# ============================================================================

class TestStandard9AgentWorkflow:
    """End-to-end test for complete 9-agent standard workflow"""

    def test_complete_change_workflow(self):
        """
        Simulate a complete change workflow with 9 agents:
        requirement -> design -> implementation -> code_review -> test_planning ->
        verification -> reflection -> documentation -> archive
        """
        governance = MultiAgentGovernance(
            template="standard",
            conflict_strategy=ResolutionStrategy.ORCHESTRATOR_FIRST
        )

        # Step 1: Requirement phase
        print("\n=== Step 1: Requirement Phase ===")
        handoff_to_design = {
            "from": "requirement_agent",
            "to": "design_agent",
            "change_id": "change-e2e-001",
            "phase": "requirement",
            "inputs": {
                "proposal.md": "# Feature Proposal\n\nAdd user authentication feature"
            },
            "assumptions": [
                "OAuth 2.0 will be used",
                "User database exists"
            ],
            "open_questions": [
                "Should we support social login?",
                "What's the expected user volume?"
            ],
            "required_outputs": ["design.md", "test_strategy"],
            "required_skills": ["brainstorming", "openspec-new-change"],
            "gate_before_next": "design-gate",
            "timestamp": datetime.now().isoformat()
        }

        result = governance.validate_handoff("requirement_agent", "design_agent", handoff_to_design)
        assert result.success
        print(f"Requirement -> Design handoff: SUCCESS")

        # Step 2: Design phase
        print("\n=== Step 2: Design Phase ===")
        handoff_to_implementation = {
            "from": "design_agent",
            "to": "implementation_agent",
            "change_id": "change-e2e-001",
            "phase": "design",
            "inputs": {
                "design.md": "# Technical Design\n\nArchitecture: OAuth 2.0 + JWT"
            },
            "assumptions": [
                "JWT tokens will expire in 1 hour"
            ],
            "open_questions": [],
            "required_outputs": ["code_changes", "updated_tasks"],
            "required_skills": [],
            "gate_before_next": "development-gate",
            "timestamp": datetime.now().isoformat()
        }

        result = governance.validate_handoff("design_agent", "implementation_agent", handoff_to_implementation)
        assert result.success
        print(f"Design -> Implementation handoff: SUCCESS")

        # Step 3: Implementation phase
        print("\n=== Step 3: Implementation Phase ===")
        handoff_to_review = {
            "from": "implementation_agent",
            "to": "code_review_agent",
            "change_id": "change-e2e-001",
            "phase": "development",
            "inputs": {
                "code_changes": "authentication.py",
                "implementation_notes": "Implemented OAuth 2.0 flow"
            },
            "assumptions": [],
            "open_questions": [],
            "required_outputs": ["review_findings", "review_decision"],
            "required_skills": [],
            "gate_before_next": "code-review-gate",
            "timestamp": datetime.now().isoformat()
        }

        result = governance.validate_handoff("implementation_agent", "code_review_agent", handoff_to_review)
        assert result.success
        print(f"Implementation -> Code Review handoff: SUCCESS")

        # Step 4: Code Review phase
        print("\n=== Step 4: Code Review Phase ===")

        # Validate that code_review_agent can review implementation_agent's work
        action_result = governance.validate_agent_action(
            agent="code_review_agent",
            action="Review correctness and security"
        )
        assert action_result.allowed
        print(f"Code Review action validation: ALLOWED")

        # Simulate review passed
        handoff_to_test_planning = {
            "from": "code_review_agent",
            "to": "test_planner_agent",
            "change_id": "change-e2e-001",
            "phase": "code_review",
            "inputs": {
                "review_findings": "Security check passed",
                "review_decision": "approve"
            },
            "assumptions": [],
            "open_questions": [],
            "required_outputs": ["test_plan", "test_mapping"],
            "required_skills": [],
            "gate_before_next": "test-planning-gate",
            "timestamp": datetime.now().isoformat()
        }

        result = governance.validate_handoff("code_review_agent", "test_planner_agent", handoff_to_test_planning)
        assert result.success
        print(f"Code Review -> Test Planning handoff: SUCCESS")

        # Step 5: Test Planning phase
        print("\n=== Step 5: Test Planning Phase ===")
        handoff_to_verification = {
            "from": "test_planner_agent",
            "to": "verification_agent",
            "change_id": "change-e2e-001",
            "phase": "test_planning",
            "inputs": {
                "test_plan": "Unit tests for authentication flow",
                "test_mapping": "OAuth 2.0 flow coverage"
            },
            "assumptions": [],
            "open_questions": [],
            "required_outputs": ["verification-report.md", "pass_fail_result"],
            "required_skills": [],
            "gate_before_next": "testing-gate",
            "timestamp": datetime.now().isoformat()
        }

        result = governance.validate_handoff("test_planner_agent", "verification_agent", handoff_to_verification)
        assert result.success
        print(f"Test Planning -> Verification handoff: SUCCESS")

        # Step 6: Verification phase
        print("\n=== Step 6: Verification Phase ===")
        handoff_to_reflection = {
            "from": "verification_agent",
            "to": "reflection_agent",
            "change_id": "change-e2e-001",
            "phase": "testing",
            "inputs": {
                "verification-report.md": "All tests passed",
                "pass_fail_result": "pass"
            },
            "assumptions": [],
            "open_questions": [],
            "required_outputs": ["retrospective.md", "reflection_findings"],
            "required_skills": [],
            "gate_before_next": "reflection-gate",
            "timestamp": datetime.now().isoformat()
        }

        result = governance.validate_handoff("verification_agent", "reflection_agent", handoff_to_reflection)
        assert result.success
        print(f"Verification -> Reflection handoff: SUCCESS")

        # Step 7: Reflection phase
        print("\n=== Step 7: Reflection Phase ===")
        handoff_to_documentation = {
            "from": "reflection_agent",
            "to": "documentation_agent",
            "change_id": "change-e2e-001",
            "phase": "reflection",
            "inputs": {
                "retrospective.md": "Process went smoothly",
                "reflection_findings": "No major blockers"
            },
            "assumptions": [],
            "open_questions": [],
            "required_outputs": ["documentation_impact_result"],
            "required_skills": [],
            "gate_before_next": "archive-gate",
            "timestamp": datetime.now().isoformat()
        }

        result = governance.validate_handoff("reflection_agent", "documentation_agent", handoff_to_documentation)
        assert result.success
        print(f"Reflection -> Documentation handoff: SUCCESS")

        # Step 8: Documentation phase
        print("\n=== Step 8: Documentation Phase ===")

        # Check documentation impact
        action_result = governance.validate_agent_action(
            agent="documentation_agent",
            action="Check whether long-term specs need updates"
        )
        assert action_result.allowed
        print(f"Documentation action validation: ALLOWED")

        # Step 9: Archive phase
        print("\n=== Step 9: Archive Phase ===")

        # Validate archiver can archive after reflection
        action_result = governance.validate_agent_action(
            agent="orchestrator_agent",
            action="Archive completed change"
        )
        assert action_result.allowed
        print(f"Archive action validation: ALLOWED")

        # Generate governance report
        print("\n=== Governance Report ===")
        report = governance.generate_governance_report()
        print(f"Total handoffs completed: {len(report['recent_handoffs'])}")
        print(f"Total conflicts resolved: {len(report['recent_conflicts'])}")

        assert len(report['recent_handoffs']) == 7  # All handoffs recorded
        assert report['registered_roles'] == 9


# ============================================================================
# Simplified 5-Agent Workflow Test
# ============================================================================

class TestSimplified5AgentWorkflow:
    """End-to-end test for 5-agent simplified workflow"""

    def test_simplified_workflow(self):
        """
        Simulate a simplified workflow with 5 agents:
        orchestrator -> requirement -> implementation -> code_review -> verification
        """
        governance = MultiAgentGovernance(template="simplified")

        print("\n=== Simplified 5-Agent Workflow ===")

        # Handoff 1: Requirement -> Implementation (skip design)
        handoff_data = {
            "from": "requirement_agent",
            "to": "implementation_agent",
            "change_id": "change-simplified-001",
            "phase": "requirement",
            "inputs": {"proposal.md": "Simple feature"},
            "assumptions": [],
            "open_questions": [],
            "required_outputs": ["code_changes"],
            "required_skills": [],
            "gate_before_next": "development-gate"
        }

        result = governance.validate_handoff("requirement_agent", "implementation_agent", handoff_data)
        assert result.success
        print(f"Requirement -> Implementation: SUCCESS")

        # Handoff 2: Implementation -> Code Review
        handoff_data = {
            "from": "implementation_agent",
            "to": "code_review_agent",
            "change_id": "change-simplified-001",
            "phase": "development",
            "inputs": {"code_changes": "feature.py"},
            "assumptions": [],
            "open_questions": [],
            "required_outputs": ["review_decision"],
            "required_skills": [],
            "gate_before_next": "testing-gate"
        }

        result = governance.validate_handoff("implementation_agent", "code_review_agent", handoff_data)
        assert result.success
        print(f"Implementation -> Code Review: SUCCESS")

        # Handoff 3: Code Review -> Verification
        handoff_data = {
            "from": "code_review_agent",
            "to": "verification_agent",
            "change_id": "change-simplified-001",
            "phase": "code_review",
            "inputs": {"review_decision": "approve"},
            "assumptions": [],
            "open_questions": [],
            "required_outputs": ["verification-report.md"],
            "required_skills": [],
            "gate_before_next": "archive-gate"
        }

        result = governance.validate_handoff("code_review_agent", "verification_agent", handoff_data)
        assert result.success
        print(f"Code Review -> Verification: SUCCESS")

        report = governance.generate_governance_report()
        assert len(report['recent_handoffs']) == 3


# ============================================================================
# Minimal 3-Agent Workflow Test
# ============================================================================

class TestMinimal3AgentWorkflow:
    """End-to-end test for 3-agent minimal workflow"""

    def test_minimal_workflow(self):
        """
        Simulate a minimal workflow with 3 agents:
        orchestrator -> implementation -> verification
        """
        governance = MultiAgentGovernance(template="minimal")

        print("\n=== Minimal 3-Agent Workflow ===")

        # Handoff 1: Implementation -> Verification (skip all intermediate)
        handoff_data = {
            "from": "implementation_agent",
            "to": "verification_agent",
            "change_id": "change-minimal-001",
            "phase": "implementation",
            "inputs": {"code_changes": "minimal_feature.py"},
            "assumptions": [],
            "open_questions": [],
            "required_outputs": ["verification-report.md"],
            "required_skills": [],
            "gate_before_next": "archive-gate"
        }

        result = governance.validate_handoff("implementation_agent", "verification_agent", handoff_data)
        assert result.success
        print(f"Implementation -> Verification: SUCCESS")

        report = governance.generate_governance_report()
        assert len(report['recent_handoffs']) == 1


# ============================================================================
# Real Change Scenario with Conflicts
# ============================================================================

class TestRealChangeScenarioWithConflicts:
    """End-to-end test simulating a real change with conflicts"""

    def test_change_with_workflow_conflict(self):
        """
        Simulate a real change scenario where agents disagree on workflow selection
        """
        governance = MultiAgentGovernance(
            template="standard",
            conflict_strategy=ResolutionStrategy.ORCHESTRATOR_FIRST
        )

        print("\n=== Real Change Scenario: Workflow Dispute ===")

        # Initial handoff succeeds
        handoff_data = {
            "from": "requirement_agent",
            "to": "design_agent",
            "change_id": "change-conflict-001",
            "phase": "requirement",
            "inputs": {"proposal.md": "Complex feature proposal"},
            "assumptions": [],
            "open_questions": [],
            "required_outputs": ["design.md"],
            "required_skills": [],
            "gate_before_next": "design-gate"
        }

        result = governance.validate_handoff("requirement_agent", "design_agent", handoff_data)
        assert result.success
        print(f"Requirement phase completed")

        # Conflict arises: design_agent and implementation_agent disagree
        print(f"Conflict: Workflow selection disputed")

        conflict_result = governance.resolve_conflict(
            agents=["design_agent", "implementation_agent"],
            disagreement_type="workflow_selection_disputed",
            context={
                "proposal": "Complex feature",
                "complexity": "high",
                "suggested_workflow": "lightweight_tweak"
            },
            severity="high"
        )

        assert conflict_result.resolved
        assert conflict_result.decision_maker == "orchestrator_agent"
        print(f"Conflict resolved by orchestrator: {conflict_result.final_decision}")

        # Workflow proceeds after conflict resolution
        handoff_data = {
            "from": "design_agent",
            "to": "implementation_agent",
            "change_id": "change-conflict-001",
            "phase": "design",
            "inputs": {"design.md": "Technical design"},
            "assumptions": [],
            "open_questions": [],
            "required_outputs": ["code_changes"],
            "required_skills": [],
            "gate_before_next": "development-gate"
        }

        result = governance.validate_handoff("design_agent", "implementation_agent", handoff_data)
        assert result.success
        print(f"Design phase completed after conflict resolution")

        report = governance.generate_governance_report()
        assert len(report['recent_handoffs']) == 2
        assert len(report['recent_conflicts']) == 1


# ============================================================================
# Multi-Round Interaction Scenario
# ============================================================================

class TestMultiRoundInteraction:
    """End-to-end test for multi-round agent interactions"""

    def test_three_rounds_of_handoffs(self):
        """
        Simulate three rounds of complete handoffs with state accumulation
        """
        governance = MultiAgentGovernance(template="simplified")

        print("\n=== Multi-Round Interaction: 3 Rounds ===")

        for round_num in range(3):
            print(f"\n--- Round {round_num + 1} ---")

            # Round 1: Requirement -> Implementation
            handoff1 = {
                "from": "requirement_agent",
                "to": "implementation_agent",
                "change_id": f"change-round-{round_num}",
                "phase": "requirement",
                "inputs": {"proposal.md": f"Round {round_num} feature"},
                "assumptions": [],
                "open_questions": [],
                "required_outputs": ["code_changes"],
                "required_skills": [],
                "gate_before_next": "development-gate",
                "timestamp": f"2026-07-02T{round_num}:00:00Z"
            }

            result1 = governance.validate_handoff("requirement_agent", "implementation_agent", handoff1)
            assert result1.success
            print(f"Round {round_num + 1}: Requirement -> Implementation SUCCESS")

            # Round 2: Implementation -> Code Review
            handoff2 = {
                "from": "implementation_agent",
                "to": "code_review_agent",
                "change_id": f"change-round-{round_num}",
                "phase": "development",
                "inputs": {"code_changes": f"round_{round_num}.py"},
                "assumptions": [],
                "open_questions": [],
                "required_outputs": ["review_decision"],
                "required_skills": [],
                "gate_before_next": "testing-gate",
                "timestamp": f"2026-07-02T{round_num}:30:00Z"
            }

            result2 = governance.validate_handoff("implementation_agent", "code_review_agent", handoff2)
            assert result2.success
            print(f"Round {round_num + 1}: Implementation -> Code Review SUCCESS")

        # Verify all handoffs recorded
        report = governance.generate_governance_report()
        assert len(report['recent_handoffs']) == 6  # 3 rounds * 2 handoffs

        # Verify no conflicts (clean workflow)
        assert len(report['recent_conflicts']) == 0

        print(f"\n=== Multi-Round Summary ===")
        print(f"Total handoffs: {len(report['recent_handoffs'])}")
        print(f"Total conflicts: {len(report['recent_conflicts'])}")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])  # -s to see print outputs