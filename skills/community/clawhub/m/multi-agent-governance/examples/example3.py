"""
Example 3: Custom roles and configuration persistence
"""

from multi_agent_governance import MultiAgentGovernance, HandoffTemplate, ResolutionStrategy
import tempfile
from pathlib import Path

# Initialize with minimal template
governance = MultiAgentGovernance(template="minimal")
print(f"Initial roles: {governance.list_roles()}")

# Register custom roles
print("\n=== Registering Custom Roles ===")
governance.register_role(
    name="security_review_agent",
    role="Security Review Agent",
    responsibilities=[
        "Review code for security vulnerabilities",
        "Check for SQL injection, XSS, authentication issues",
        "Verify secure coding practices"
    ],
    must_not=[
        "Approve own implementation",
        "Skip mandatory security checks"
    ],
    outputs=[
        "security_review_findings",
        "security_approval_decision"
    ],
    reviewer_for="implementation_agent",
    priority=8
)

governance.register_role(
    name="performance_review_agent",
    role="Performance Review Agent",
    responsibilities=[
        "Review code for performance issues",
        "Check for N+1 queries, memory leaks",
        "Verify caching strategies"
    ],
    must_not=[
        "Approve without benchmarks",
        "Skip performance testing"
    ],
    outputs=[
        "performance_review_findings",
        "performance_benchmarks"
    ],
    reviewer_for="implementation_agent",
    priority=7
)

print(f"After custom roles: {governance.list_roles()}")

# Validate custom role actions
print("\n=== Custom Role Validation ===")
result = governance.validate_agent_action(
    agent="security_review_agent",
    action="Review code for SQL injection"
)
print(f"Security review allowed: {result.allowed}")

result = governance.validate_agent_action(
    agent="security_review_agent",
    action="Approve own implementation"
)
print(f"Self-approval allowed: {result.allowed}")
print(f"Violations: {result.violations}")

# Save configuration to file
print("\n=== Saving Configuration ===")
with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as f:
    temp_path = Path(f.name)

governance.save_configuration(temp_path)
print(f"Configuration saved to: {temp_path}")

# Load configuration into new instance
print("\n=== Loading Configuration ===")
governance2 = MultiAgentGovernance(template="minimal")
governance2.load_configuration(temp_path)

print(f"Loaded roles: {governance2.list_roles()}")
print(f"Security agent loaded: {'security_review_agent' in governance2.list_roles()}")

# Validate loaded roles
result = governance2.validate_agent_action(
    agent="security_review_agent",
    action="Review code for security vulnerabilities"
)
print(f"Loaded role validation: {result.allowed}")

# Generate report
print("\n=== Final Report ===")
report = governance2.generate_governance_report()
print(f"Total roles: {report['registered_roles']}")
print(f"Framework: {report['framework']}")

# Clean up
temp_path.unlink()