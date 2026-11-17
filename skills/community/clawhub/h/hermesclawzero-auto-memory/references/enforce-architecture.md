# Enforce Governance Architecture — v2 Proposal

## Current Architecture

```
System Prompt
↓
Enforce Rules
↓
Long-Term Memory
↓
Conversation
↓
User
```

## Proposed Two-Layer Architecture

### Layer 1 – Prompt Governance (existing)
Parse `enforce:` from SKILL.md → inject rules above memory → preserve priority ordering.

### Layer 2 – Runtime Policy Engine (new)
Validates every dangerous action before execution:

```
LLM
↓
Action Proposal
↓
Policy Engine
↓
Allowed?
  ├─ Yes → Execute
  └─ No  → BLOCKED + reason
```

### Structured Policies replace free-text rules

```yaml
enforce:
  - priority: critical
    rule: "Never push directly to main."
    policy:
      tool: terminal
      pattern: "git push origin main"
      action: deny
      reason: "Direct pushes to main are not allowed."
```

### Policy Resolution
`critical > high > medium` — most restrictive rule wins. `allow + deny = deny`.

### Audit Log
Every blocked/approved action: timestamp, action, tool, rule matched, decision, reason.

### Plugin Architecture
`GitPolicy`, `FilesystemPolicy`, `DockerPolicy`, `ShellPolicy`, `DatabasePolicy`, `MCPPolicy`, `CustomSkillPolicies`.

### Final Architecture

```
System Prompt
↓
Enforce Rules (Layer 1)
↓
Long-Term Memory
↓
Conversation
↓
LLM Decision
↓
Runtime Policy Engine (Layer 2)
↓
Tool Execution
```

Three independent layers: **Memory** (facts), **Governance** (behavior), **Execution** (actions).
