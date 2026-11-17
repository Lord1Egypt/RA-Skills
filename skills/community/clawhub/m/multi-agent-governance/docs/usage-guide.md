# Usage Guide for Multi-Agent Governance

## Installation

```bash
pip install openclaw-skills
```

Or install from ClawHub:

```bash
openclaw skills install multi-agent-governance
```

## Quick Start

### Basic Usage

```python
from multi_agent_governance import MultiAgentGovernance

# Initialize with standard template
governance = MultiAgentGovernance(template="standard")

# List all registered roles
roles = governance.list_roles()
print(f"Registered {len(roles)} roles: {roles}")

# Get a specific role
orchestrator = governance.get_role("orchestrator_agent")
print(f"Orchestrator responsibilities: {orchestrator.responsibilities}")
```

### Validating Handoffs

```python
# Define handoff data
handoff_data = {
    "from": "requirement_agent",
    "to": "design_agent",
    "change_id": "change-123",
    "phase": "requirement",
    "inputs": {"proposal.md": "..."},
    "assumptions": [],
    "open_questions": [],
    "required_outputs": ["design.md"],
    "required_skills": [],
    "gate_before_next": "design-gate"
}

# Validate handoff
result = governance.validate_handoff(
    from_agent="requirement_agent",
    to_agent="design_agent",
    handoff_data=handoff_data
)

if result.success:
    print("Handoff valid! Proceeding to next phase.")
else:
    print(f"Handoff failed: {result.validation_result.errors}")
```

### Resolving Conflicts

```python
# Resolve agent disagreement
result = governance.resolve_conflict(
    agents=["design_agent", "implementation_agent"],
    disagreement_type="workflow_selection_disputed",
    context={"proposal": "...", "design": "..."},
    severity="high"
)

if result.resolved:
    print(f"Decision: {result.final_decision}")
    print(f"Decision maker: {result.decision_maker}")
else:
    print(f"Escalating to user with options: {result.alternative_options}")
```

### Validating Agent Actions

```python
# Check if an agent can perform an action
result = governance.validate_agent_action(
    agent="implementation_agent",
    action="Bypass blocking gates"
)

if result.allowed:
    print("Action allowed")
else:
    print(f"Action denied: {result.violations}")
    print(f"Recommendations: {result.recommendations}")
```

## Customizing Governance

### Using Different Templates

```python
# Simplified 5-agent template
governance = MultiAgentGovernance(template="simplified")

# Minimal 3-agent template
governance = MultiAgentGovernance(template="minimal")

# Custom configuration from dict
custom_config = [
    {
        "name": "custom_agent",
        "role": "Custom Agent",
        "responsibilities": ["custom_task"],
        "must_not": ["bypass_rules"],
        "outputs": ["custom_output"],
        "priority": 5
    }
]
governance = MultiAgentGovernance(template=custom_config)
```

### Registering Custom Roles

```python
# Register a new custom role
governance.register_role(
    name="custom_review_agent",
    role="Custom Review Agent",
    responsibilities=[
        "Review custom aspects",
        "Provide specialized feedback"
    ],
    must_not=[
        "Approve own work",
        "Skip mandatory checks"
    ],
    outputs=[
        "custom_review_findings",
        "approval_decision"
    ],
    reviewer_for="implementation_agent",
    priority=6
)
```

### Customizing Handoff Policy

```python
from multi_agent_governance import HandoffTemplate, MissingInputAction

# Define custom handoff template
custom_handoff = HandoffTemplate(
    required_fields=["from", "to", "inputs", "outputs"],
    optional_fields=["notes", "timestamp"],
    missing_input_action=MissingInputAction.WARN_AND_CONTINUE
)

governance = MultiAgentGovernance(
    template="standard",
    handoff_policy={
        "required_fields": ["from", "to", "inputs", "outputs"],
        "missing_input_action": "warn_and_continue"
    }
)
```

### Setting Conflict Resolution Strategy

```python
from multi_agent_governance import ResolutionStrategy

# Orchestrator-first (default)
governance = MultiAgentGovernance(
    template="standard",
    conflict_strategy=ResolutionStrategy.ORCHESTRATOR_FIRST
)

# User-first (always ask user)
governance = MultiAgentGovernance(
    template="standard",
    conflict_strategy=ResolutionStrategy.USER_FIRST
)

# Voting-based (highest priority wins)
governance = MultiAgentGovernance(
    template="standard",
    conflict_strategy=ResolutionStrategy.VOTING
)
```

## Saving and Loading Configuration

### Save to File

```python
# Save configuration to YAML
governance.save_configuration("governance_config.yaml")

# Save configuration to JSON
governance.save_configuration("governance_config.json")
```

### Load from File

```python
# Load configuration from YAML
governance = MultiAgentGovernance(template="minimal")
governance.load_configuration("governance_config.yaml")

# Load configuration from JSON
governance.load_configuration("governance_config.json")
```

## Generating Reports

```python
# Generate comprehensive governance report
report = governance.generate_governance_report()

print(f"Registered roles: {report['registered_roles']}")
print(f"Handoff policy: {report['handoff_policy']}")
print(f"Conflict strategy: {report['conflict_strategy']}")
print(f"Recent handoffs: {len(report['recent_handoffs'])}")
print(f"Recent conflicts: {len(report['recent_conflicts'])}")
```

## Framework Adapters

The governance system supports multiple agent frameworks:

```python
# OpenClaw (default)
governance = MultiAgentGovernance(template="standard", framework="openclaw")

# LangChain
governance = MultiAgentGovernance(template="standard", framework="langchain")

# AutoGen
governance = MultiAgentGovernance(template="standard", framework="autogen")
```

## Best Practices

1. **Use appropriate template** — Choose standard/simplified/minimal based on your project complexity
2. **Define clear responsibilities** — Ensure each agent's responsibilities are well-defined
3. **Set proper priorities** — Use priorities for voting-based conflict resolution
4. **Document handoffs** — Always include required fields in handoffs
5. **Monitor conflicts** — Track conflicts in governance report and adjust rules accordingly
6. **Save configuration** — Save governance configuration to file for persistence