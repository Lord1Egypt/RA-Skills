# Inheritance Algorithm Reference

Detailed explanation of how policy inheritance works.

## Overview

The inheritance algorithm resolves policies from the broadest (organization) to the most specific (session) level, merging rules according to inheritance configuration.

## Policy Chain Resolution

### Step 1: Build the Chain

Given a session context:
```yaml
organization: "acme-corp"
team: "engineering"
project: "api-gateway"
session: "sess_abc123"
```

The system builds a chain:
```
~/.openclaw/governance/
├── organizations/acme-corp/policies.yaml  (root)
├── teams/engineering/policies.yaml
├── projects/api-gateway/policies.yaml
└── sessions/sess_abc123/policies.yaml     (leaf)
```

### Step 2: Load and Validate Each Level

Each policy file is loaded and validated:
- YAML syntax check
- Required fields present
- Valid level values
- Parent references resolve correctly

### Step 3: Merge Policies

Policies are merged from root to leaf based on `inheritance.mode`:

#### Merge Mode (default)

Child policies are **added** to parent policies. For each action type:

```
Parent:  [A, B, C]
Child:   [D, E]
Result:  [A, B, C, D, E]
```

Child rules are appended after parent rules, so child rules are checked first during evaluation (more specific wins).

#### Override Mode

Child completely replaces parent for overlapping keys:

```
Parent policies.http:  [A, B, C]
Child policies.http:   [D, E]
Result policies.http:  [D, E]

Parent policies.shell: [X, Y]
Child has no shell:    [X, Y]  (preserved)
```

#### Isolate Mode

Child doesn't inherit anything:

```
Parent: [A, B, C]
Child:  [D, E]
Result: [D, E]  (parent ignored)
```

## Rule Evaluation

Once merged, rules are evaluated for each action:

### Evaluation Order

Rules are checked in order (child rules before parent rules). First match wins.

```yaml
# Merged policy (child rules first)
http:
  # From session (most specific)
  - pattern: "api.stripe.com"
    action: allow
  
  # From project
  - pattern: "*.stripe.com"
    action: require_approval
  
  # From team
  - pattern: "*.github.com"
    action: allow
  
  # From organization (broadest)
  - pattern: "*"
    action: deny
```

### Action Precedence

When rules conflict, this precedence applies:

1. **Deny always wins** - If any matching rule denies, action is blocked
2. **Most specific match** - Longer/more specific patterns take precedence
3. **First match** - When specificity is equal, first rule wins
4. **Default deny** - If no rules match, action is blocked (in strict mode)

### Specificity Calculation

Pattern specificity is calculated as:

```python
def specificity(pattern):
    # More literal characters = more specific
    # Fewer wildcards = more specific
    literal_chars = len(pattern.replace('*', '').replace('?', ''))
    wildcard_count = pattern.count('*') + pattern.count('?')
    return (literal_chars, -wildcard_count)
```

Examples:
- `api.github.com` → (14, 0) = very specific
- `*.github.com` → (11, -1) = less specific
- `*github*` → (7, -2) = least specific

## Exception Handling

The `inheritance.exceptions` list prevents certain policy keys from inheriting:

```yaml
# Parent (organization)
policies:
  shell:
    - command: "sudo *"
      action: require_approval

# Child (team)
inheritance:
  mode: merge
  exceptions:
    - shell.sudo  # Don't inherit shell sudo rules

policies:
  shell:
    - command: "sudo apt *"
      action: allow  # Team allows specific sudo
```

Result: Team can `sudo apt install` but not other sudo commands.

## Extension Points

The `inheritance.extensions` list allows the parent to control what children can modify:

```yaml
# Parent
inheritance:
  extensions:
    - http.allowlist  # Child can only add to http allowlist

policies:
  http:
    - pattern: "*.internal.com"
      action: allow
  shell:
    - command: "rm *"
      action: deny

# Child tries to override shell
policies:
  shell:
    - command: "rm *"
      action: allow  # ERROR: shell not in extensions
```

## Conflict Detection

The validator detects potential conflicts:

### Type 1: Parent Deny / Child Allow

```yaml
# Parent denies
- pattern: "*.external.com"
  action: deny

# Child allows
- pattern: "api.external.com"
  action: allow  # Warning: overrides parent deny
```

This generates a warning because the child is overriding a security-critical deny.

### Type 2: Inheritance Mode Mismatch

```yaml
# Parent has mode: isolate
# Child expects to inherit
```

This is valid but may be unintentional.

### Type 3: Missing Parent

```yaml
parent: ../nonexistent/policies.yaml
```

This is an error - parent must exist.

## Caching

For performance, merged policies can be cached:

```python
# Cache key based on context
cache_key = hash((org, team, project, session))

# Check cache before rebuilding chain
if cache_key in policy_cache:
    return policy_cache[cache_key]

# Build and cache
merged = build_policy_chain(context)
policy_cache[cache_key] = merged
return merged
```

Cache invalidation:
- File modification time changes
- Explicit cache clear command
- TTL expiration (e.g., 5 minutes)

## Edge Cases

### Circular References

```yaml
# A/policies.yaml
parent: ../B/policies.yaml

# B/policies.yaml
parent: ../A/policies.yaml  # ERROR: circular
```

Detected during validation - max depth exceeded.

### Missing Levels

```yaml
context:
  organization: "acme"
  # No team specified
  project: "api"
```

Chain: org → project (skips team). Valid - missing levels are ignored.

### Empty Policies

```yaml
policies: {}  # Empty but valid
```

Inherits everything from parent (if merge mode).

### Null Parent

```yaml
parent: null  # Root level
```

Valid for organization level. Error for other levels (should have parent).

## Algorithm Pseudocode

```python
def resolve_policies(context):
    # Build chain
    chain = []
    for level in ['organization', 'team', 'project', 'session']:
        path = get_policy_path(context, level)
        if path.exists():
            chain.append(load_policy(path))
    
    if not chain:
        return default_deny_policy()
    
    # Merge from root to leaf
    merged = {}
    for policy in chain:
        merged = merge_policies(merged, policy)
    
    return merged

def merge_policies(parent, child):
    mode = child.get('inheritance', {}).get('mode', 'merge')
    exceptions = child.get('inheritance', {}).get('exceptions', [])
    
    if mode == 'isolate':
        return child['policies']
    
    if mode == 'override':
        # Child replaces parent for keys it defines
        result = dict(parent['policies'])
        for key, value in child['policies'].items():
            result[key] = value
        return result
    
    # Merge mode (default)
    result = {}
    all_keys = set(parent['policies'].keys()) | set(child['policies'].keys())
    
    for key in all_keys:
        if key in exceptions:
            # Don't inherit this key
            result[key] = child['policies'].get(key, [])
        elif key in child['policies']:
            # Child rules come first (more specific)
            child_rules = child['policies'][key]
            parent_rules = parent['policies'].get(key, [])
            result[key] = child_rules + parent_rules
        else:
            # Only in parent
            result[key] = parent['policies'][key]
    
    return result

def evaluate_action(policies, action_type, action_details):
    rules = policies.get(action_type, [])
    
    # Sort by specificity (most specific first)
    rules = sorted(rules, key=specificity, reverse=True)
    
    for rule in rules:
        if matches(rule, action_details):
            if rule['action'] == 'deny':
                return {'allowed': False, 'reason': rule.get('reason')}
            elif rule['action'] == 'require_approval':
                return {'allowed': True, 'requires_approval': True}
            else:  # allow
                return {'allowed': True}
    
    # No match - default deny
    return {'allowed': False, 'reason': 'No matching policy'}
```
