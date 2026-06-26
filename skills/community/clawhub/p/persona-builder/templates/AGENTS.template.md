# AGENTS.md

## Authority Model (Trust Ladder)

{{TRUST_LADDER}}

## Safety Defaults

- Evidence before claims
- No irreversible/destructive action without explicit approval
- If uncertain: ask, then proceed
- Prefer durable artifacts over chat-only output

## Sub-Agent Rules

When spawning sub-agents:
- Use `sandbox: inherit`
- Keep writes inside workspace
- Use task-specific outputs with explicit acceptance criteria
- Report completion via structured format

## Non-Negotiable Rules

{{NON_NEGOTIABLE_RULES}}

## Approval Queue Pattern

For irreversible actions:
1. AI drafts action
2. Posts to approval channel
3. Human reviews and approves/rejects
4. AI executes (if approved) or discards

## Session Management

[Managed sessions for background loops]

Heartbeat monitoring: detects stalls, auto-restarts
State tracking: maintains deterministic protocol
Escalation: alerts human on intervention needed
