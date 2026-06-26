---
name: lemma-assistants
description: "Use for Lemma assistant work: design pod-scoped conversational assistants with clear instructions, safe action boundaries, and the right supporting resources."
---

# Lemma Assistants

Use this skill for pod-scoped conversational assistants.

Assistants are the user-facing conversational surface of a pod. They should help users understand data, answer questions, and trigger the right deterministic systems safely.

## When To Use This Skill

Use `lemma-assistants` when:

- conversation is the primary interaction model
- users need to ask questions about pod data or files
- users need a guided way to trigger actions
- the system should combine retrieval, explanation, and controlled action-taking

## Assistant Versus Other Resources

### Assistant vs agent

Use an assistant for user-facing conversation.
Use an agent for background reasoning work.

### Assistant vs function

Use a function for deterministic backend logic and writes.
An assistant may call or coordinate that logic, but should not replace it.

### Assistant vs workflow

Use a workflow when the action spans multiple stages, waiting states, or triggers.
The assistant can be the front door that launches or explains the workflow.

### Assistant vs desk

Use a desk when humans need a full application with queues, forms, detail views, and navigation.
Use an assistant when conversation is the best primary interface.
Many pods should have both.

## Critical Facts

- Assistants are first-class pod resources.
- `accessible_tables` grants table access with explicit mode.
- `accessible_folders` grants folder scope for file operations.
- `accessible_applications` controls which third-party apps the assistant may use.
- If the assistant must trigger deterministic writes or orchestration, pair it with functions and workflows.

## Instruction Design Rules

A good assistant instruction should say:

- who the assistant serves
- what data and files it may use
- what actions it may trigger
- when it must ask for confirmation
- what tone or operating style it should use

Prefer explicit behavioral rules over vague personality instructions.

## Confirmation Rules

Assistants should ask for confirmation before:

- durable writes
- outbound communication
- app operations with external side effects
- workflow launches that create meaningful downstream impact

Assistants can answer read-only questions directly when the granted data is sufficient.

## Canonical Assistant Create Payload

```json
{
  "name": "sales-copilot",
  "description": "User-facing assistant for account executives",
  "instruction": "Help users answer questions about granted tables and folders, summarize next actions, and ask for confirmation before any write or outbound action.",
  "tool_sets": ["USER_INTERACTION", "SKILLS", "WORKSPACE_CLI"],
  "accessible_tables": [
    {"table_name": "customers", "mode": "READ"},
    {"table_name": "orders", "mode": "READ"}
  ],
  "accessible_folders": ["manuals"],
  "accessible_applications": []
}
```

## Conversation Lifecycle

Create and inspect the assistant:

```bash
lemma assistant create --pod-id <pod-id> --payload-file ./payloads/assistant-create.json
lemma assistant list --pod-id <pod-id>
lemma assistant get sales-copilot --pod-id <pod-id>
lemma assistant update sales-copilot --pod-id <pod-id> --payload '{"instruction":"Updated instruction"}'
```

Conversation commands:

```bash
lemma conversation list --pod-id <pod-id>
lemma conversation create --pod-id <pod-id> --payload '{"title":"Support session","assistant_id":"<assistant-id>"}'
lemma conversation get <conversation-id> --pod-id <pod-id>
lemma conversation message-send <conversation-id> --pod-id <pod-id> --payload '{"content":"Hello"}'
lemma conversation message-list <conversation-id> --pod-id <pod-id>
```

## Recommended Split

- assistant: user-facing conversation
- agent: background reasoning worker
- function: deterministic logic and writes
- workflow: orchestration across time
- desk: structured web app for repeatable human workflows

## Verification Rules

Always test an assistant with realistic user prompts.
Check:

- whether it answers read-only questions correctly
- whether it asks for confirmation before risky actions
- whether it stays within granted scope
- whether it routes deterministic actions to functions or workflows appropriately

Test at least one informational query and one action-oriented prompt.

## Common Mistakes

- using the assistant as a replacement for functions or workflows
- granting write access without clear confirmation behavior
- making instructions too vague about side effects
- giving the assistant broad app access without a real use case
- treating an assistant like a background worker instead of a conversational surface

## Related Skills

Route to:

- `lemma-agents` for background reasoning tasks
- `lemma-functions` for deterministic actions and writes
- `lemma-workflows` for multi-step orchestration
- `lemma-desks` when the pod also needs a full operator UI
