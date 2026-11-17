---
name: permission-auditor
description: Review tool usage patterns, permission configurations, and detect security policy violations in session transcripts and evolution state.
---

# Permission Auditor Skill

Audits tool usage patterns and permission configurations for security compliance.

## Usage

```bash
# Audit current workspace
node skills/permission-auditor/index.js

# Audit specific workspace
node skills/permission-auditor/index.js /path/to/workspace
```

## Features

- Scans session transcripts for tool usage patterns
- Detects elevated execution attempts (sudo, admin)
- Identifies tool bypass attempts (--force, unsafe flags)
- Checks environment configuration for security flags
- Reviews evolution state tool policies

## Output

```
=== Permission Audit Report ===
Workspace: /path/to/workspace
Time: 2026-06-07T09:18:57.430Z

Summary:
  Total tools used: 47
  Risky patterns: 2
  Bypass attempts: 0
  Policy violations: 0

Tool Usage Frequency:
  exec: 23 uses
  read: 12 uses
  write: 8 uses
  edit: 4 uses

Detected Patterns:
  [?] elevated_execution: Elevated execution detected in session
      File: session_2026-06-05.jsonl
  [i] tool_policy_configured: Tool policy is configured in evolution state

Recommendations:
  - WARNING: Elevated executions found - ensure proper authorization
  - OK: Tool usage patterns appear normal
```

## Severity Levels

- `[!]` HIGH - Critical security issue (bypass attempts, unsafe flags)
- `[?]` MEDIUM - Warning level (elevated executions, unusual patterns)
- `[i]` INFO - Informational (normal configurations, usage stats)

## When to Use

- Security audits
- Permission configuration reviews
- Before deploying to production
- When investigating suspicious tool usage
- Periodic security compliance checks