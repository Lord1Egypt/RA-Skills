"""
Example 2: Handoff validation and conflict resolution
"""

from multi_agent_governance import MultiAgentGovernance, ResolutionStrategy

# Initialize with standard template and custom settings
governance = MultiAgentGovernance(
    template="standard",
    conflict_strategy=ResolutionStrategy.ORCHESTRATOR_FIRST
)

# Define handoff from requirement to design phase
print("=== Handoff Validation ===")
handoff_data = {
    "from": "requirement_agent",
    "to": "design_agent",
    "change_id": "change-2026-001",
    "phase": "requirement",
    "inputs": {
        "proposal.md": "Feature proposal for user authentication"
    },
    "assumptions": [
        "Authentication will use OAuth 2.0",
        "User database already exists"
    ],
    "open_questions": [
        "Should we support social login?",
        "What's the expected user volume?"
    ],
    "required_outputs": [
        "design.md",
        "test_strategy"
    ],
    "required_skills": [
        "openspec-new-change",
        "brainstorming"
    ],
    "gate_before_next": "design-gate",
    "timestamp": "2026-07-02T10:00:00Z"
}

result = governance.validate_handoff(
    from_agent="requirement_agent",
    to_agent="design_agent",
    handoff_data=handoff_data
)

print(f"Handoff success: {result.success}")
print(f"Validation valid: {result.validation_result.valid}")
print(f"Next phase: {result.next_phase}")
print(f"Next gate: {result.next_gate}")

if not result.success:
    print(f"Errors: {result.validation_result.errors}")
    print(f"Missing fields: {result.validation_result.missing_fields}")

# Resolve a conflict between agents
print("\n=== Conflict Resolution ===")
conflict_result = governance.resolve_conflict(
    agents=["design_agent", "implementation_agent"],
    disagreement_type="workflow_selection_disputed",
    context={
        "proposal": "Feature proposal",
        "design": "Technical design",
        "complexity": "high"
    },
    severity="high"
)

print(f"Conflict resolved: {conflict_result.resolved}")
print(f"Final decision: {conflict_result.final_decision}")
print(f"Decision maker: {conflict_result.decision_maker}")
print(f"Reasoning: {conflict_result.reasoning}")
print(f"Alternatives: {conflict_result.alternative_options}")

# Try user-first strategy
print("\n=== User-First Strategy ===")
governance.set_conflict_strategy(ResolutionStrategy.USER_FIRST)

conflict_result = governance.resolve_conflict(
    agents=["requirement_agent", "design_agent"],
    disagreement_type="scope_or_risk_disputed",
    context={
        "original_scope": "Full feature",
        "proposed_scope": "MVP only",
        "risk_level": "medium"
    }
)

print(f"Conflict resolved: {conflict_result.resolved}")
print(f"Decision maker: {conflict_result.decision_maker}")
print(f"Alternatives: {conflict_result.alternative_options}")

# Generate report showing recent handoffs and conflicts
print("\n=== Governance Report ===")
report = governance.generate_governance_report()
print(f"Recent handoffs: {len(report['recent_handoffs'])}")
print(f"Recent conflicts: {len(report['recent_conflicts'])}")

for handoff in report['recent_handoffs']:
    print(f"- {handoff['from']} -> {handoff['to']}: {handoff['success']}")

for conflict in report['recent_conflicts']:
    print(f"- {conflict['agents']}: {conflict['disagreement_type']} (resolved: {conflict['resolved']})")