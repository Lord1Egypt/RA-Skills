---
name: lemma-agents
description: "Use for Lemma agent work: design judgment-heavy worker agents with clear instructions, schemas, grants, and task-based execution."
---

# Lemma Agents

Use this skill for LLM worker agents and their task execution model.

Agents are for judgment-heavy work. They should be good at thinking, not used as a substitute for deterministic backend logic.

## When To Use This Skill

Use `lemma-agents` when the work involves:

- drafting
- classification
- summarization
- extraction
- research
- reasoning over granted tables or files

Do not use an agent when a function or direct record operation would be simpler and more reliable.

## Agent Versus Other Resources

### Agent vs function

Use an agent for judgment and language-heavy work.
Use a function for deterministic validation, writes, and external system calls.

### Agent vs assistant

Use an agent as a background worker.
Use an assistant when conversation with the end user is the main interaction model.

### Agent vs workflow

Use a workflow when the process has multiple stages, branching, waiting, or triggers.
Use an agent as one step inside that larger orchestration.

## Critical Facts

- Agents run through tasks. There is no direct `agent.run` command.
- Task creation uses `agent_name`, not `agent_id`.
- Workflow `AGENT` nodes also require `agent_name`.
- `input_data` is structured task input. It does not auto-inject file contents.
- `accessible_tables` grants table access with explicit mode.
- `accessible_folders` grants folder scope for file operations.
- `accessible_applications` grants third-party app access when truly needed.

## Instruction Design Rules

A good agent instruction should:

- state the job clearly
- say what inputs the agent should expect
- say what sources it may use
- say what output shape it must return
- say what it must not do

Good instruction patterns:

- name the task directly
- tell the agent how to retrieve referenced files or records
- tell the agent whether to return strict JSON or free-form text
- keep durable writes out of the agent unless that behavior is explicitly designed and safe

## Schema Guidance

Use `input_schema` when the task expects structured inputs.
Use `output_schema` when downstream systems need reliable structured output.

Prefer structured output when:

- a workflow or function will consume the result
- the task is extraction or classification
- the output needs predictable keys

Plain text output is acceptable for free-form drafting or open-ended summaries.

## Tool And Grant Guidance

Grant only what the agent actually needs.

- give table access only for relevant tables
- give folder access only for needed file paths
- add app access only when the task genuinely depends on third-party actions
- choose tool sets intentionally rather than by habit

## Canonical Agent Create Payload

```json
{
  "name": "document-summarizer",
  "description": "Summarize pod documents and return structured findings",
  "instruction": "Summarize documents referenced by task input. If file_id is present, fetch the file from pod files before answering. Return strict JSON with summary, key_points, and open_questions. Do not persist durable business records yourself.",
  "input_schema": {
    "type": "object",
    "properties": {
      "file_id": {"type": "string"},
      "question": {"type": "string"}
    },
    "required": ["file_id", "question"]
  },
  "output_schema": {
    "type": "object",
    "properties": {
      "summary": {"type": "string"},
      "key_points": {"type": "array", "items": {"type": "string"}},
      "open_questions": {"type": "array", "items": {"type": "string"}}
    },
    "required": ["summary", "key_points", "open_questions"]
  },
  "tool_sets": ["SKILLS", "WORKSPACE_CLI", "FILE_SYSTEM"],
  "accessible_tables": [{"table_name": "customers", "mode": "READ"}],
  "accessible_folders": ["manuals"],
  "accessible_applications": []
}
```

## Canonical Task Flow

Create and inspect the agent:

```bash
lemma agent create --pod-id <pod-id> --payload-file ./payloads/agent-create.json
lemma agent list --pod-id <pod-id>
lemma agent get document-summarizer --pod-id <pod-id>
```

Run the agent through a task:

```bash
lemma task create --pod-id <pod-id> --agent-name document-summarizer --payload-file ./payloads/task-create.json
lemma task list --pod-id <pod-id> --agent-name document-summarizer
lemma task get <task-id> --pod-id <pod-id>
lemma task message-list <task-id> --pod-id <pod-id>
```

Example task payload:

```json
{
  "input_data": {
    "file_id": "4b1c0d5e-3f9b-4ee4-b3cf-6e3e7b3b6d21",
    "question": "Summarize the top contract risks"
  }
}
```

## Verification Rules

Always validate an agent with a realistic task.
Check:

- whether it follows the instruction precisely
- whether the output shape matches the declared schema
- whether it uses granted data correctly
- whether it stays inside its intended scope

For extraction or classification agents, test at least one easy case and one messy case.

## Workflow Dependency Rule

If a workflow needs an agent:

1. create the agent first
2. capture the returned `name`
3. use that exact `agent_name` in the workflow graph

## Common Mistakes

- using an agent for deterministic writes that belong in a function
- using `agent_id` in task payloads or workflow config
- assuming file text is auto-injected from `file_id`
- omitting an output schema when downstream systems expect structured output
- granting far more table or folder access than the task needs

## Related Skills

Route to:

- `lemma-functions` for deterministic writes or application calls
- `lemma-assistants` when the user should converse directly with the system
- `lemma-workflows` when the agent is one stage in a larger process
