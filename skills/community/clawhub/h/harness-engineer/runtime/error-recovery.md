# ERROR RECOVERY

Structured error handling and recovery protocol for all agents.

## ERROR TAXONOMY

### Recoverable Errors (agent self-corrects)
| Category | Examples | Recovery |
|----------|---------|----------|
| Tool failure | File not found, command timeout | Agent reads error, tries alternative |
| Permission denial | Tool blocked by policy | Agent requests escalation or uses alternative tool |
| Rate limit | API throttled | Agent waits and retries (exponential backoff) |
| Test failure | Test does not pass | Agent analyzes failure, fixes code, re-tests |
| Integration failure | Cross-gap test fails | Agent fixes integration, re-tests |

### Fatal Errors (halt and surface to human)
| Category | Examples | Recovery |
|----------|---------|----------|
| Config corruption | CONFIG.yaml unparseable | Halt, surface error, wait for human fix |
| Protected file violation | Agent attempted to modify skill files | Halt, log violation, surface to human |
| Human halt | Human explicitly stopped the cycle | Write HANDOFF.md, stop |
| Budget exhaustion | Cost exceeded 120% of cycle budget | Write HANDOFF.md, surface summary |
| Max retries exceeded | Same error 3+ times on same task | Write HANDOFF.md, surface to human |

## STRUCTURED ERROR FORMAT

All errors surfaced to agents or humans use this format:
{
  "category": "tool_failure | permission_denial | rate_limit | test_failure | ...",
  "severity": "recoverable | fatal",
  "message": "<human-readable error description>",
  "suggested_action": "<what to do next>",
  "retry_count": 0,
  "source": "<tool_name or phase that produced the error>"
}

## AGENT SELF-CORRECTION RULES

When a recoverable error occurs:
1. READ the error message carefully. Do not retry blindly.
2. IDENTIFY the root cause: is this a transient issue or a systematic problem?
3. TRY an alternative: different tool, different approach, different parameters.
4. LOG the attempt in the tracking log (what failed, what was tried, result).
5. ESCALATE after 3 retries: surface to human with full context.

Fatal error protocol:
1. Write current state to HANDOFF.md
2. Log the error in PROGRESS.md
3. Append to MEMORY.md if the error reveals a harness gap
4. Halt. Wait for human.
