# Playbooks

Playbooks are parameterized runbooks for common operations. When you find yourself doing the same thing 3+ times, create a playbook.

## Format

```markdown
# Operation Name

## Parameters
- param1: description (required/optional)

## Prerequisites
- [ ] Check item

## Steps
1. Exact command or action
2. ...

## Rollback
- What to do if it fails

## History
- Created: YYYY-MM-DD
- Last used: YYYY-MM-DD
```

## Frequency Tracking

The `frequency.json` file tracks how often operations are performed. When an operation appears 3+ times without a playbook, the system suggests creating one.

```json
{
  "_meta": {"description": "Operation frequency tracker"},
  "operations": {
    "deploy-to-server": {"count": 5, "lastUsed": "2026-03-19", "hasPlaybook": true},
    "debug-network": {"count": 2, "lastUsed": "2026-03-18", "hasPlaybook": false}
  }
}
```
