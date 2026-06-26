# TOOL ROUTER

## PURPOSE
Centralized control point for all tool usage. Every tool call passes through here.

---

## FLOW
```
Agent => Tool Request => Tool Router => Validate => Execute => Normalize Output => Return => Agent Validates
```

---

## RESPONSIBILITIES
1. **Validate inputs** -- reject malformed or dangerous requests before execution.
2. **Route** to the correct tool implementation.
3. **Normalize outputs** -- all results returned in standard format (see below).
4. **Enforce safety constraints** -- block destructive commands without approval.
5. **Log every call** -- write to `docs/generated/tool-logs/`.

---

## SAFETY RULES
- Block any destructive command (`write_file` on a non-draft path, `git_commit` without tests passing, server restarts in production) unless explicitly approved.
- Prevent infinite loops: if the same tool is called with the same input 3+ times in a row, halt and log.
- Enforce rate limits: no more than 10 tool calls per minute per agent.
- Never execute shell commands that were not pre-registered in `TOOL_REGISTRY.md`.

---

## STANDARD OUTPUT FORMAT

```json
{
  "status": "success | failure | blocked",
  "tool": "<tool name>",
  "timestamp": "<ISO 8601>",
  "outcome": "<one-line summary -- no raw data, no file contents>",
  "errors": "<error type and code -- not full stack trace or log lines>",
  "log_path": "docs/generated/tool-logs/<id>.json"
}
```

**Redaction rule**: before any tool result is written to a log or returned to an agent,
the router must strip or mask values that match common credential patterns.
This includes authentication tokens, API keys, passwords, secrets, certificates,
and any opaque string that could be an authentication token or credential.

Additionally, the router must never log:
- Full file contents (log the path, not the content)
- Raw HTTP response bodies (log status code and outcome only)

---

## PROTECTED PATHS (read-only to all agents)

The following files define how the harness operates. Agents may **read** them but must
**never write, overwrite, or delete** them. Only a human operator may change these files.

```
SKILL.md
CONFIG.yaml
agents/**
runtime/**
tools/**
references/harness-rules.md
```

Writes to any protected path must be **blocked** by the router and logged as a
`BLOCKED_WRITE` event. If an agent submits a write request to a protected path,
the dispatcher must be notified and the cycle must pause for human review.

The one writable reference file is `references/constraints.md` -- agents may **append**
Prevention Rules to it but may **never delete or overwrite** existing constraints.

---

## BLOCKED ACTIONS (require explicit human approval)
- Deleting files or directories
- Dropping databases or migrations
- Merging to main/trunk directly (PR required)
- Disabling security scans
- Modifying `CONFIG.yaml` runtime limits

## BLOCKED READS (enforced by router -- no human override)
Any read_file or list_dir call whose path matches references/sensitive-paths.md
forbidden patterns is blocked at the router level before the tool executes.
Blocked reads are logged as BLOCKED_READ events (path pattern matched, not the path itself).
The requesting agent receives: "read blocked -- sensitive path policy" with no content.

The full list of blocked path patterns is maintained in references/sensitive-paths.md.
Categories include: credential files, CI/CD configuration, git internals,
package manager authentication, and application configuration with embedded secrets.

---

## OUTPUT REDACTION

Before returning tool results to agents, the router applies output redaction:

### Redaction Categories
- Authentication tokens and API keys
- Connection strings containing embedded credentials
- Environment variable values for sensitive configuration
- HTTP response bodies from external requests (keep status + headers only)

### Redaction Log
- Count of redacted items per tool call (metadata only)
- Category of what was redacted (not the actual value)
- Stored in docs/generated/tool-logs/
- The actual redacted values are never stored

### Exception
Redaction does NOT apply when the agent explicitly requests raw output for
debugging AND the human gate approves.
