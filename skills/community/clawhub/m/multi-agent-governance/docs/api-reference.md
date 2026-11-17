# API Reference for Multi-Agent Governance

## MultiAgentGovernance

Main governance system class for managing agent roles, handoffs, and conflicts.

### Constructor

```python
MultiAgentGovernance(
    template: Union[str, Dict] = "standard",
    handoff_policy: Optional[Dict[str, Any]] = None,
    conflict_strategy: ResolutionStrategy = ResolutionStrategy.ORCHESTRATOR_FIRST,
    framework: str = "openclaw"
)
```

#### Parameters

- `template` (Union[str, Dict]): Role template name or custom configuration
  - `"standard"` — 9-agent template (orchestrator, requirement, design, implementation, code_review, test_planner, verification, reflection, documentation)
  - `"simplified"` — 5-agent template (orchestrator, requirement, implementation, code_review, verification)
  - `"minimal"` — 3-agent template (orchestrator, implementation, verification)
  - `Dict` — Custom role configuration list

- `handoff_policy` (Optional[Dict]): Custom handoff policy configuration
  - `required_fields` — List of required handoff fields
  - `optional_fields` — List of optional handoff fields
  - `missing_input_action` — Action for missing inputs ("block_transition", "warn_and_continue", "auto_fill_defaults")

- `conflict_strategy` (ResolutionStrategy): Conflict resolution strategy
  - `ORCHESTRATOR_FIRST` — Orchestrator makes decisions
  - `USER_FIRST` — Always ask user
  - `VOTING` — Voting among agents (highest priority wins)
  - `PRIORITY_BASED` — Priority-based resolution

- `framework` (str): Target framework name ("openclaw", "langchain", "autogen")

---

### Methods

#### register_role()

Register a custom agent role.

```python
register_role(
    name: str,
    role: str,
    responsibilities: List[str],
    must_not: List[str],
    outputs: List[str],
    reviewer_for: Optional[str] = None,
    priority: int = 0,
    metadata: Optional[Dict[str, Any]] = None
) -> None
```

#### get_role()

Get a registered role by name.

```python
get_role(role_name: str) -> Optional[AgentRoleConfig]
```

#### list_roles()

List all registered role names.

```python
list_roles() -> List[str]
```

#### validate_handoff()

Validate and enforce a handoff between agents.

```python
validate_handoff(
    from_agent: str,
    to_agent: str,
    handoff_data: Dict[str, Any]
) -> HandoffResult
```

#### validate_agent_action()

Validate if an agent can perform an action.

```python
validate_agent_action(agent: str, action: str) -> BoundaryCheckResult
```

#### resolve_conflict()

Resolve a conflict between agents.

```python
resolve_conflict(
    agents: List[str],
    disagreement_type: str,
    context: Dict[str, Any],
    severity: str = "medium"
) -> ResolutionResult
```

#### set_conflict_strategy()

Set conflict resolution strategy.

```python
set_conflict_strategy(strategy: ResolutionStrategy) -> None
```

#### generate_governance_report()

Generate comprehensive governance report.

```python
generate_governance_report() -> Dict[str, Any]
```

#### save_configuration()

Save governance configuration to file.

```python
save_configuration(filepath: Union[str, Path]) -> None
```

#### load_configuration()

Load governance configuration from file.

```python
load_configuration(filepath: Union[str, Path]) -> None
```

---

## Data Models

### AgentRoleConfig

Configuration for a single agent role.

```python
AgentRoleConfig(
    name: str,
    role: str,
    responsibilities: List[str],
    must_not: List[str],
    outputs: List[str],
    reviewer_for: Optional[str] = None,
    priority: int = 0,
    metadata: Dict[str, Any] = {}
)
```

---

### HandoffTemplate

Template for agent handoff.

```python
HandoffTemplate(
    required_fields: List[str] = [...],
    optional_fields: List[str] = [...],
    missing_input_action: MissingInputAction = MissingInputAction.BLOCK_TRANSITION,
    custom_validation_rules: Dict[str, Any] = {}
)
```

---

### ValidationResult

Result of a validation operation.

```python
ValidationResult(
    valid: bool,
    errors: List[str],
    warnings: List[str],
    missing_fields: List[str]
)
```

---

### HandoffResult

Result of a handoff operation.

```python
HandoffResult(
    success: bool,
    handoff_data: Dict[str, Any],
    validation_result: ValidationResult,
    next_phase: Optional[str] = None,
    next_gate: Optional[str] = None
)
```

---

### BoundaryCheckResult

Result of a role boundary check.

```python
BoundaryCheckResult(
    allowed: bool,
    violations: List[str],
    recommendations: List[str]
)
```

---

### AgentConflict

Represents a conflict between agents.

```python
AgentConflict(
    agents: List[str],
    disagreement_type: str,
    context: Dict[str, Any] = {},
    severity: str = "medium"
)
```

---

### ResolutionResult

Result of a conflict resolution.

```python
ResolutionResult(
    resolved: bool,
    final_decision: str,
    decision_maker: str,
    reasoning: str,
    alternative_options: List[str]
)
```

---

## Enums

### ResolutionStrategy

Conflict resolution strategies.

```python
ResolutionStrategy.ORCHESTRATOR_FIRST
ResolutionStrategy.USER_FIRST
ResolutionStrategy.VOTING
ResolutionStrategy.PRIORITY_BASED
```

---

### MissingInputAction

Actions when required input is missing.

```python
MissingInputAction.BLOCK_TRANSITION
MissingInputAction.WARN_AND_CONTINUE
MissingInputAction.AUTO_FILL_DEFAULTS
```