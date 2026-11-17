"""
Example 1: Basic usage of Multi-Agent Governance
"""

from multi_agent_governance import MultiAgentGovernance

# Initialize governance system with standard template
governance = MultiAgentGovernance(template="standard")

# List all registered roles
print("=== Registered Roles ===")
roles = governance.list_roles()
for role in roles:
    print(f"- {role}")

print(f"\nTotal roles: {len(roles)}")

# Get orchestrator role details
print("\n=== Orchestrator Agent Details ===")
orchestrator = governance.get_role("orchestrator_agent")
print(f"Role: {orchestrator.role}")
print(f"Responsibilities: {orchestrator.responsibilities}")
print(f"Cannot: {orchestrator.must_not}")
print(f"Outputs: {orchestrator.outputs}")
print(f"Priority: {orchestrator.priority}")

# Validate an allowed action
print("\n=== Action Validation ===")
result = governance.validate_agent_action(
    agent="orchestrator_agent",
    action="Select workflow based on routing rules"
)
print(f"Action allowed: {result.allowed}")
print(f"Violations: {result.violations}")
print(f"Recommendations: {result.recommendations}")

# Validate a disallowed action
result = governance.validate_agent_action(
    agent="orchestrator_agent",
    action="Bypass blocking gates"
)
print(f"Action allowed: {result.allowed}")
print(f"Violations: {result.violations}")

# Generate governance report
print("\n=== Governance Report ===")
report = governance.generate_governance_report()
print(f"Registered roles: {report['registered_roles']}")
print(f"Framework: {report['framework']}")
print(f"Conflict strategy: {report['conflict_strategy']}")