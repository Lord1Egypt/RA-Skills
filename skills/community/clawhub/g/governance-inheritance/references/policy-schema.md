# Policy Schema Reference

Complete YAML schema for governance policy files.

## File Structure

```yaml
version: string      # Policy format version (e.g., "1.0")
level: string        # One of: organization, team, project, session
parent: string|null  # Path to parent policy file, or null for root

policies:            # Policy definitions
  http: [...]        # HTTP request policies
  shell: [...]       # Shell command policies
  file:              # File operation policies
    read: [...]
    write: [...]
  browser: [...]     # Browser automation policies

inheritance:         # Inheritance configuration
  mode: string       # merge | override | isolate
  exceptions: [...]  # Policy keys that don't inherit
  extensions: [...]  # Keys child can extend
```

## Policy Actions

Each policy rule has an `action` field:

| Action | Description |
|--------|-------------|
| `allow` | Permit the action without approval |
| `deny` | Block the action (always wins) |
| `require_approval` | Allow but require explicit user approval |
| `log` | Allow but log for audit |

## HTTP Policies

```yaml
http:
  - pattern: string        # URL pattern (glob syntax)
    action: allow|deny|require_approval
    scope: [string]        # Optional: limit to HTTP methods
    reason: string         # Optional: explanation for deny/require
    
  # Examples:
  - pattern: "*.internal.company.com"
    action: allow
    scope: ["GET", "POST"]
  
  - pattern: "*"
    action: deny
    reason: "External HTTP requires approval"
```

### Pattern Syntax

- `*` matches any sequence of characters
- `?` matches any single character
- `**` matches across path segments (in paths)

Examples:
- `*.github.com` - Any subdomain of github.com
- `api.*.com` - api.example.com, api.test.com, etc.
- `https://*` - Any HTTPS URL

## Shell Policies

```yaml
shell:
  - command: string        # Command pattern (glob syntax)
    action: allow|deny|require_approval
    reason: string
    
  # Examples:
  - command: "git *"
    action: allow
  
  - command: "rm -rf /*"
    action: deny
    reason: "Destructive command blocked"
  
  - command: "sudo *"
    action: require_approval
    reason: "Elevated privileges require approval"
```

### Command Pattern Matching

Patterns match against the full command string:
- `git *` matches `git status`, `git commit`, etc.
- `docker run *` matches `docker run ubuntu`, etc.
- `rm -rf /*` matches exactly that dangerous command

## File Policies

```yaml
file:
  read:
    - path: string         # Path pattern (glob syntax)
      action: allow|deny|require_approval
      reason: string
      
  write:
    - path: string
      action: allow|deny|require_approval
      reason: string

  # Examples:
  read:
    - path: "~/workspace/*"
      action: allow
    - path: "/etc/*"
      action: deny
      reason: "System files protected"
  
  write:
    - path: "~/workspace/*"
      action: allow
    - path: "*"
      action: require_approval
```

### Path Patterns

- `~` expands to user's home directory
- `*` matches files in that directory only
- `**` matches recursively

Examples:
- `~/workspace/*` - All files in workspace
- `~/workspace/**` - All files recursively in workspace
- `*.txt` - Any .txt file
- `/tmp/*` - Any file in /tmp

## Browser Policies

```yaml
browser:
  - pattern: string        # URL pattern
    action: allow|deny|require_approval
    scope: [string]        # Optional: actions (navigate, click, type, etc.)
    reason: string
    
  # Examples:
  - pattern: "*.internal.company.com"
    action: allow
    scope: ["navigate", "click"]
  
  - pattern: "*"
    action: require_approval
    reason: "Browser automation requires approval"
```

## Inheritance Configuration

```yaml
inheritance:
  # How child policies combine with parent
  mode: merge        # Options: merge, override, isolate
  
  # Policy keys that don't inherit from parent
  # Child must define these from scratch
  exceptions:
    - shell.sudo
    - file.write
  
  # Policy keys child is allowed to extend
  # Parent can restrict which policies children can modify
  extensions:
    - http.allowlist
    - shell.commands
```

### Inheritance Modes

| Mode | Description |
|------|-------------|
| `merge` | Child policies add to parent (default) |
| `override` | Child completely replaces parent for overlapping keys |
| `isolate` | Child doesn't inherit anything from parent |

## Policy Evaluation Order

1. Policies are loaded from root (organization) to leaf (session)
2. Each level's policies are merged according to inheritance mode
3. For each action, the most specific matching rule wins
4. `deny` always beats `allow`
5. Rules are evaluated in order within a policy section

## Example Complete Policy

```yaml
version: "1.0"
level: team
parent: ../organization/policies.yaml

policies:
  http:
    - pattern: "*.github.com"
      action: allow
      scope: ["GET", "POST"]
    
    - pattern: "*.npmjs.com"
      action: allow
      scope: ["GET"]
    
    - pattern: "api.stripe.com"
      action: require_approval
      reason: "Payment API access requires approval"
    
    - pattern: "*"
      action: deny
      reason: "Unknown external API"
  
  shell:
    - command: "git *"
      action: allow
    
    - command: "npm *"
      action: allow
    
    - command: "docker *"
      action: require_approval
      reason: "Container operations require approval"
    
    - command: "sudo *"
      action: deny
      reason: "Sudo not allowed"
  
  file:
    read:
      - path: "~/workspace/**"
        action: allow
      - path: "~/.openclaw/**"
        action: allow
      - path: "/etc/*"
        action: deny
        reason: "System configuration protected"
    
    write:
      - path: "~/workspace/**"
        action: allow
      - path: "~/Downloads/*"
        action: require_approval
      - path: "/usr/*"
        action: deny
        reason: "System directories protected"
  
  browser:
    - pattern: "*.github.com"
      action: allow
      scope: ["navigate", "click"]
    
    - pattern: "localhost:*"
      action: allow
    
    - pattern: "*"
      action: require_approval

inheritance:
  mode: merge
  exceptions:
    - shell.sudo
  extensions:
    - http.allowlist
    - file.read
```

## Validation Rules

A policy file must:

1. Have `version` field (semantic versioning)
2. Have `level` field with valid value
3. Have `policies` section (can be empty)
4. Have valid inheritance mode if specified
5. Reference valid parent path (if not null)

Policy rules must:

1. Have `action` field with valid value
2. Have appropriate pattern field for policy type:
   - `pattern` for http, browser
   - `command` for shell
   - `path` for file
3. Have `reason` if action is `deny` or `require_approval` (recommended)
