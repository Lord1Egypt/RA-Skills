# 03 — Permission Guard

> Not every agent should be allowed to do everything.

## Concept

A Permission Guard sits between the agent's intent and the actual tool execution. It evaluates each operation request against a set of rules and returns one of three decisions:

- **ALLOW** — Operation proceeds without interruption
- **DENY** — Operation is blocked, agent receives an error
- **CONFIRM** — Operation requires OTC confirmation before proceeding

```
Agent: "I want to delete /var/log/app.log"
  │
  ▼
Permission Guard:
  ├── Check role: "ops-agent" → has file operations
  ├── Check scope: /var/log/ → within allowed paths
  ├── Check action: delete → requires confirmation for non-temp files
  │
  └── Decision: CONFIRM
      └── Trigger OTC flow
```

## Rule Structure

### Rule Definition

```yaml
rules:
  - name: "allow-read-anywhere"
    action: ALLOW
    conditions:
      operation: read
      path: "*"
    
  - name: "confirm-delete-non-temp"
    action: CONFIRM
    conditions:
      operation: delete
      path_not: "/tmp/*"
    
  - name: "deny-system-modification"
    action: DENY
    conditions:
      operation: [write, delete, chmod]
      path: ["/etc/*", "/usr/*", "/bin/*", "/sbin/*"]

  - name: "confirm-external-communication"
    action: CONFIRM
    conditions:
      operation: [send_email, send_message, post_api]
      target: "*"

  - name: "deny-destructive-commands"
    action: DENY
    conditions:
      operation: exec
      command_pattern: 
        - "rm -rf /"
        - "mkfs.*"
        - "dd if=/dev/zero"
        - ":(){:|:&};:"
```

### Rule Evaluation Order

Rules are evaluated **top-down, first match wins**:

1. Explicit DENY rules (highest priority — absolute blocks)
2. CONFIRM rules (operations needing human approval)
3. ALLOW rules (permitted operations)
4. **Default: DENY** (fail closed — anything not explicitly allowed is denied)

## Role-Based Access Control (RBAC)

### Defining Roles

```yaml
roles:
  researcher:
    description: "Read-only research and analysis"
    allowed_operations:
      - read_file
      - web_search
      - web_fetch
      - summarize
    max_concurrent: 5
    
  developer:
    description: "Code development within project directories"
    allowed_operations:
      - read_file
      - write_file
      - exec_command
      - git_operations
    scope:
      paths: ["~/projects/*"]
      excluded_paths: ["~/projects/*/secrets/*"]
    requires_confirmation:
      - exec_command  # Shell commands always need review
    
  ops-agent:
    description: "Infrastructure operations with guardrails"
    allowed_operations:
      - read_file
      - exec_command
      - deploy
      - restart_service
    scope:
      environments: ["staging"]
      excluded_environments: ["production"]
    requires_confirmation:
      - deploy
      - restart_service
    
  admin:
    description: "Full access with confirmation for destructive ops"
    allowed_operations: ["*"]
    requires_confirmation:
      - delete_file
      - modify_permissions
      - external_communication
      - deploy_production
```

### Role Assignment

```yaml
agents:
  - name: "research-bot"
    role: researcher
    
  - name: "backend-dev"
    role: developer
    scope_override:
      paths: ["~/projects/backend/*"]
    
  - name: "deploy-bot"
    role: ops-agent
    scope_override:
      environments: ["staging", "production"]
    requires_confirmation:
      - deploy  # Inherited from role
      - any_production_operation  # Added for this agent
```

## Scope Enforcement

### Path-Based Scoping

```python
def check_path_scope(operation_path, allowed_paths, excluded_paths):
    """Verify the operation target is within allowed scope."""
    
    # Normalize and resolve symlinks
    real_path = os.path.realpath(operation_path)
    
    # Check excluded paths first (deny takes priority)
    for excluded in excluded_paths:
        if fnmatch.fnmatch(real_path, excluded):
            return DENY, f"Path {real_path} is in excluded scope"
    
    # Check allowed paths
    for allowed in allowed_paths:
        if fnmatch.fnmatch(real_path, allowed):
            return ALLOW, f"Path {real_path} is within allowed scope"
    
    # Default: deny
    return DENY, f"Path {real_path} is outside agent scope"
```

### Environment-Based Scoping

```python
def check_environment_scope(target_env, allowed_envs):
    """Prevent agents from touching environments they shouldn't."""
    if target_env not in allowed_envs:
        return DENY, f"Agent not authorized for {target_env} environment"
    
    # Production always requires confirmation, regardless of role
    if target_env == "production":
        return CONFIRM, "Production operations require confirmation"
    
    return ALLOW, f"Environment {target_env} is within scope"
```

### Network-Based Scoping

```python
def check_network_scope(target_url, allowed_domains, blocked_domains):
    """Control which external services the agent can reach."""
    domain = urlparse(target_url).hostname
    
    if domain in blocked_domains:
        return DENY, f"Domain {domain} is blocked"
    
    if allowed_domains and domain not in allowed_domains:
        return DENY, f"Domain {domain} is not in allowlist"
    
    return ALLOW, f"Domain {domain} is permitted"
```

## Integration with OTC

When the Permission Guard returns CONFIRM, it triggers the OTC flow:

```python
def execute_with_guard(operation, agent_role):
    # Step 1: Check permissions
    decision, reason = permission_guard.evaluate(operation, agent_role)
    
    if decision == DENY:
        audit_log.record("DENIED", operation, reason)
        raise PermissionError(f"Operation denied: {reason}")
    
    if decision == CONFIRM:
        audit_log.record("CONFIRM_REQUIRED", operation, reason)
        
        # Step 2: Generate and send OTC
        subprocess.run(["bash", "generate_code.sh"], check=True)
        subprocess.run(["bash", "send_otc_email.sh", 
                        operation.description, 
                        operation.session_id], check=True)
        
        # Step 3: Wait for user input
        user_code = await get_user_input()
        
        # Step 4: Verify
        result = subprocess.run(["bash", "verify_code.sh", user_code])
        if result.returncode != 0:
            audit_log.record("CONFIRM_FAILED", operation)
            raise PermissionError("Confirmation code mismatch")
        
        audit_log.record("CONFIRMED", operation)
    
    # Step 5: Execute (ALLOW or confirmed CONFIRM)
    result = operation.execute()
    audit_log.record("EXECUTED", operation, result)
    return result
```

## Practical Implementation Tips

### Start Simple

Don't try to implement every permission rule on day one. Start with:

1. **Block the catastrophic** — Deny formatting disks, wiping directories
2. **Confirm the external** — OTC for emails, messages, API calls  
3. **Allow the safe** — Read operations, local file creation

Then iterate based on what your agent actually does.

### Log Before You Block

Before enforcing new DENY rules, run them in **audit-only mode** for a week. This reveals:
- False positives (legitimate operations that would be blocked)
- Missing rules (operations that should be blocked but aren't)
- Usage patterns that inform better rule design

### Keep Rules Readable

Your future self (and your teammates) will need to understand and modify these rules. Prefer explicit, named rules over complex regex patterns.

```yaml
# Good: Clear intent
- name: "block-production-drops"
  action: DENY
  conditions:
    operation: sql_execute
    query_pattern: "DROP TABLE"
    environment: production

# Bad: Clever but opaque
- name: "rule-47"
  action: DENY
  conditions:
    command_regex: "^(?:sudo\\s+)?(?:rm|dd|mkfs|fdisk)\\s+.*(?:/dev/|/etc/|/var/)"
```
