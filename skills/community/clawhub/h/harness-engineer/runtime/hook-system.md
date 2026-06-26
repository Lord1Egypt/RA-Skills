# HOOK SYSTEM

Lifecycle hooks and tool-use hooks for extending harness behavior.

## HOOK POINTS

### Lifespan Hooks (run once per lifecycle event)
| Hook | When | Purpose |
|------|------|---------|
| on-start | Session init complete, before Phase 1 | Human acknowledgment, session setup |
| on-plan-complete | MASTER-PLAN approved, before implement | Human plan approval gate |
| on-cycle-complete | All phases done, final review passed | Surface cycle summary to human |
| on-error | Unrecoverable error during any phase | Surface error, request guidance |
| on-halt | System stopped (human or automatic) | Surface halt reason, state dump |

### Tool-Use Hooks (run on every tool invocation)
| Hook | When | Purpose |
|------|------|---------|
| pre-tool-use | Before tool execution | Security policy, audit, custom validation |
| post-tool-use | After tool execution | Audit logging, result validation, metrics |

## PROTOCOL

### Lifespan Hooks
Implemented by the host platform (Claude Code hooks, OpenClaw lifecycle events).
The skill defines WHAT hooks exist and their purpose. The platform defines HOW.

Each lifespan hook:
  - Receives: event type, cycle ID, session state summary
  - Returns: ACK (continue) or BLOCK (with reason, halt cycle)

### Tool-Use Hooks (for platform support)
When a tool-use hook is configured:

  Input (via stdin, JSON):
    {
      "event": "pre_tool_use" | "post_tool_use",
      "tool_name": "write_file",
      "tool_input": { ... },
      "agent": "implementer",
      "cycle_id": "NNN",
      "timestamp": "ISO8601"
    }

  Exit codes:
    0 = ALLOW (proceed with tool execution)
    1 = ERROR (retry, transient failure)
    2 = DENY (block tool execution, return denial reason to agent)

  Output (via stdout):
    {
      "decision": "allow" | "deny",
      "reason": "<human-readable explanation>",
      "modified_input": { ... }  // optional: hook can modify tool input
    }

### Examples

Security policy hook (pre-tool-use):
  - Intercepts all write_file calls
  - Checks if target path is in the protected paths list
  - Exit 2 if protected, 0 otherwise

Audit log hook (post-tool-use):
  - Logs every tool call to docs/generated/tool-logs/
  - Records: tool name, input hash, success/failure, duration

Custom validation hook (pre-tool-use):
  - Intercepts run_unit_tests
  - Checks if tests are being run on modified files (not unrelated tests)
  - Exit 2 if test scope doesn't match changes
