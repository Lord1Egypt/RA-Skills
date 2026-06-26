---
name: governance-inheritance
description: Hierarchical policy inheritance system for OpenClaw agents. Enables policies to be defined at organization, team, project, and session levels with automatic inheritance, override rules, and conflict resolution. Use when setting up governance policies that need to cascade across multiple sessions, when defining policy hierarchies, or when resolving policy conflicts between parent and child contexts. Required tools - exec, read, write. Environment variables - GOVERNANCE_ROOT (default ~/.openclaw/governance).
---

# Governance Inheritance

This skill provides a **hierarchical policy inheritance system** that allows policies to be defined at multiple levels and automatically inherited by child contexts.

## Policy Hierarchy Levels

Policies cascade from broad to specific:

```
Organization (broadest)
    ↓
Team
    ↓
Project
    ↓
Session (most specific)
```

### Inheritance Rules

1. **Child overrides parent**: More specific policies override broader ones
2. **Additive by default**: Policies merge unless explicitly overridden
3. **Explicit deny wins**: A `deny` at any level blocks the action
4. **Require explicit allow**: Actions without an explicit allow are blocked in strict mode

## Policy Structure

Each level contains a `policies.yaml` file:

```yaml
# policies.yaml
version: "1.0"
level: organization  # organization | team | project | session
parent: null         # path to parent policy (null for root)

# Policy blocks
policies:
  http:
    - pattern: "*.internal.company.com"
      action: allow
      scope: ["GET", "POST"]
    - pattern: "*"
      action: deny
      reason: "External HTTP requires approval"
  
  shell:
    - command: "git *"
      action: allow
    - command: "rm -rf /*"
      action: deny
      reason: "Destructive command blocked"
    - command: "*"
      action: require_approval

  file:
    read:
      - path: "~/workspace/*"
        action: allow
      - path: "/etc/*"
        action: deny
    write:
      - path: "~/workspace/*"
        action: allow
      - path: "*"
        action: require_approval

# Inheritance configuration
inheritance:
  mode: merge          # merge | override | isolate
  exceptions:          # Policies that don't inherit
    - shell.sudo
  extensions:          # Child can extend these
    - http.allowlist
```

## Quick Start

### 1. Initialize Organization Policies

```bash
python scripts/init_governance.py --level organization --path ~/.openclaw/governance
```

### 2. Create Team-Level Override

```bash
python scripts/init_governance.py --level team --name engineering --parent ~/.openclaw/governance/organization
```

### 3. Evaluate Policy for Action

```typescript
const result = await context.tools.governanceInheritance.evaluate({
  action: "http",
  details: { method: "GET", url: "https://api.example.com/data" },
  context: {
    sessionId: "sess_123",
    project: "my-project",
    team: "engineering"
  }
});

// result: { allowed: true } | { allowed: false, reason: "...", level: "organization" }
```

## Policy Resolution

When evaluating an action, the system:

1. **Collects** all applicable policies from root to leaf
2. **Merges** according to inheritance rules
3. **Evaluates** against the most specific matching rule
4. **Returns** decision with provenance (which level decided)

### Conflict Resolution

| Parent | Child | Result |
|--------|-------|--------|
| allow | allow | allow |
| allow | deny | deny (child wins) |
| allow | require_approval | require_approval |
| deny | allow | deny (deny always wins) |
| deny | deny | deny |

## Session Context Integration

Policies automatically load based on session context:

```yaml
# Session inherits from project → team → organization
session_context:
  organization: "acme-corp"
  team: "engineering"
  project: "api-gateway"
  session: "sess_abc123"

# Policy resolution path:
# ~/.openclaw/governance/organizations/acme-corp/policies.yaml
# ~/.openclaw/governance/teams/engineering/policies.yaml
# ~/.openclaw/governance/projects/api-gateway/policies.yaml
# ~/.openclaw/governance/sessions/sess_abc123/policies.yaml
```

## Available Tools

### evaluate

Evaluates an action against the inherited policy chain.

**Parameters:**
- `action` (string): Action type (http, shell, file, browser)
- `details` (object): Action-specific details
- `context` (object): Session context for policy resolution

**Returns:**
```typescript
{
  allowed: boolean,
  reason?: string,
  level: string,        // Which policy level made the decision
  policy?: string,      // Specific policy that matched
  requiresApproval?: boolean
}
```

### initPolicyLevel

Initializes a new policy level.

**Parameters:**
- `level` (string): organization, team, project, or session
- `name` (string): Identifier for this level
- `parent` (string, optional): Path to parent policy
- `path` (string): Where to create the policy

### validatePolicyChain

Validates a policy chain for conflicts or errors.

**Parameters:**
- `context` (object): Session context to validate

**Returns:**
```typescript
{
  valid: boolean,
  errors: string[],
  warnings: string[]
}
```

## Configuration

Set the governance root in your environment:

```bash
export GOVERNANCE_ROOT="~/.openclaw/governance"
```

Or in `openclaw.json`:

```json
{
  "skills": {
    "governance-inheritance": {
      "env": {
        "GOVERNANCE_ROOT": "~/.openclaw/governance"
      }
    }
  }
}
```

## Policy Examples

### Organization Level (Restrictive Base)

```yaml
level: organization
policies:
  http:
    - pattern: "*.company.internal"
      action: allow
    - pattern: "*"
      action: require_approval
  shell:
    - command: "*"
      action: require_approval
```

### Team Level (Engineering - More Permissive)

```yaml
level: team
parent: ../organization
inheritance:
  mode: merge
policies:
  http:
    - pattern: "*.github.com"
      action: allow
    - pattern: "*.npmjs.com"
      action: allow
  shell:
    - command: "git *"
      action: allow
    - command: "npm *"
      action: allow
    - command: "docker *"
      action: allow
```

### Project Level (Specific Overrides)

```yaml
level: project
parent: ../engineering
inheritance:
  mode: merge
policies:
  http:
    - pattern: "api.stripe.com"
      action: allow  # This project uses Stripe
  file:
    write:
      - path: "./dist/*"
        action: allow
```

## Integration with GovernClaw

This skill works alongside `governclaw-middleware`:

```typescript
// governclaw-middleware calls governance-inheritance for policy resolution
const policyResult = await context.tools.governanceInheritance.evaluate({
  action: "http",
  details: { method, url, headers },
  context: sessionContext
});

if (!policyResult.allowed) {
  return { blocked: true, reason: policyResult.reason };
}
```

## Best Practices

1. **Start restrictive at organization level** - Require approval for everything
2. **Grant specific permissions at lower levels** - Teams/projects opt into what they need
3. **Document exceptions** - Use `reason` field to explain why policies exist
4. **Regular audits** - Run `validatePolicyChain` to catch conflicts
5. **Version your policies** - Use the `version` field to track changes

## Error Handling

Always check for policy evaluation errors:

```typescript
const result = await context.tools.governanceInheritance.evaluate({...});

if (result.error) {
  // Policy chain misconfiguration
  console.error("Policy error:", result.error);
  return { error: "Governance misconfigured" };
}

if (!result.allowed) {
  // Policy blocked the action
  console.log("Blocked by", result.level, "policy:", result.reason);
}
```

## See Also

- `references/policy-schema.md` - Complete policy YAML schema
- `references/inheritance-algorithm.md` - Detailed inheritance logic
- `scripts/init_governance.py` - Initialize policy levels
- `scripts/validate_chain.py` - Validate policy chains
