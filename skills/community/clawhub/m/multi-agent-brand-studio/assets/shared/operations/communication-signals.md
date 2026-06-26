# Communication Signals — Standard Vocabulary

All agents use these signals to flag status in their output.

## Signal Definitions

| Signal | Meaning | Leader Action |
|--------|---------|---------------|
| `[READY]` | Standard delivery — complete and confident | Normal quality review |
| `[NEEDS_INFO]` | Agent needs more context before continuing | Gather info (ask owner, check shared/, or delegate), re-brief |
| `[BLOCKED]` | Agent cannot complete the task | Assess why, try alternative approach or different agent, or escalate |
| `[LOW_CONFIDENCE]` | Output delivered but agent flags uncertainty | Review more carefully, consider Researcher verification or Reviewer |
| `[SCOPE_FLAG]` | Task is bigger than expected or prerequisites missing | Reassess scope with owner before proceeding |

## Approval-Specific Signals

Used by Reviewer and in the approval pipeline:

| Signal | Meaning |
|--------|---------|
| `[APPROVE]` | Deliverable meets requirements, ready for owner review |
| `[REVISE]` | Material issues found, specific fixes listed |
| `[PENDING APPROVAL]` | Deliverable awaiting approval before next step (content, code, or any output) |

## Session Management Signals

Used in persistent A2A sessions (`sessions_send`):

| Signal | Meaning | Who Sends | Leader Action |
|--------|---------|-----------|---------------|
| `[KB_PROPOSE]` | Agent proposes a shared knowledge base update | All agents (including Reviewer) | Parse proposal; apply directly if from owner-confirmed context, ask owner if from agent inference |
| `[MEMORY_DONE]` | Agent has finished writing its own memory files | All agents except Reviewer | Safe to route next step or next task |
| `[CONTEXT_LOST]` | Agent's session was compacted, context lost | All agents | Re-send current task state from `tasks/T-{id}.md` |

## Internal vs Owner-Facing

- Raw callbacks, duplicate callbacks, and transport chatter are internal signals — NOT owner-facing delivery.
- Owner delivery = using `message` tool to send/edit to the task's `route`.
- Step already ✅ and duplicate callback arrives → silently ignore, no duplicate notification.

## Notification Event Mapping (Leader)

Leader edits the status message on every callback. Separate new messages only for:

| Event | Typical Trigger |
|-------|------------------|
| `NEEDS_INFO` | Agent callback `signal: [NEEDS_INFO]` |
| `BLOCKED` | Agent callback `signal: [BLOCKED]` |
| `DONE` | Task reaches completed state (Result Delivery Template) |

### KB_PROPOSE Format

```
[KB_PROPOSE]
- file: shared/brands/{brand_id}/content-guidelines.md
  action: append
  content: "Audience prefers gentle tone; avoid imperative CTAs"
  source: revision-feedback (task-id or context description)
  brand: {brand_id} (optional — auto-inferred from file path if omitted)
[/KB_PROPOSE]
```

Fields:
- `file` — target shared/ file path
- `action` — `append`, `update`, or `create`
- `content` — the proposed text
- `source` — where the insight came from (revision-feedback, web-research, review-observation, etc.)
- `brand` — _(optional)_ brand ID this proposal relates to; auto-inferred from file path if omitted

### Notes

- `[KB_PROPOSE]` is a text signal in the agent's response, not a file write operation. Even Reviewer (read-only) can propose.
- `[MEMORY_DONE]` confirms the agent has completed its own memory writes. Reviewer never sends this (cannot write files).
- `[CONTEXT_LOST]` triggers Leader to re-send task context. Agent should read its own MEMORY.md first to recover what it can.

## Usage Rules

- Include the signal at the **top** of your response
- Include one primary signal explicitly in callbacks (`[READY]`, `[BLOCKED]`, etc.)
- Only use one primary signal per response (session management signals like `[MEMORY_DONE]` and `[KB_PROPOSE]` can accompany a primary signal)
- Signals are for Leader consumption — they drive routing and escalation decisions
