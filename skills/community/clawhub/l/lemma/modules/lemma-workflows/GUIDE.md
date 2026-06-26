---
name: lemma-workflows
description: "Use for Lemma workflow work: design process graphs, wire real function and agent names, choose the right start type, and verify runs through the current CLI."
---

# Lemma Workflows

Use this skill for workflow orchestration, trigger installs, and run lifecycle.

Workflows are for multi-step processes. They are the right abstraction when a pod needs branching, waiting, triggers, or sequencing across functions, agents, and human input.

## When To Use This Skill

Use `lemma-workflows` when the process:

- spans multiple stages
- includes branching or loops
- waits for user input, approval, or time
- should start on a schedule or external event
- coordinates functions and agents into one operating flow

Do not use a workflow for a single direct backend action that could be handled by a function or record API.

## Workflow Model

### Start types

Supported start types are:

- `MANUAL`
- `SCHEDULED`
- `EVENT`
- `DATASTORE_EVENT`

### Install mode

Workflow install scope is controlled by `mode`:

- `GLOBAL`: one pod-level install can power the workflow for the pod
- `USER`: each user installs their own instance (useful for user-scoped accounts/triggers)

### Node types

Supported node types are:

- `FORM`
- `AGENT`
- `FUNCTION`
- `DECISION`
- `LOOP`
- `WAIT_UNTIL`
- `END`

## Critical Facts

- `AGENT` node config requires a real `agent_name`.
- `FUNCTION` node config requires a real `function_name`.
- `input_mapping` entries should use explicit typed bindings such as `expression` or `literal`.
- `workflow install-create` is required for non-manual starts.
- Use `mode: "USER"` when each user must install; use `mode: "GLOBAL"` for pod-wide automation.
- Manual workflows that need user input should usually begin with a `FORM` node.

## FUNCTION Node Precondition

Before adding a `FUNCTION` node, document and verify a standalone function run example for that function.

Each example must include:

- exact `function_name`
- runnable `lemma function run ... --payload '{"input_data": ...}'` command
- sample response artifact path used to verify output shape

If a standalone function run example is missing, block graph authoring for that node.

## Build Order

Build workflows in this order:

1. design the SOP
2. create required tables, functions, and agents first
3. verify and document standalone function run examples for all `FUNCTION` nodes
4. capture the real function and agent names
5. create the workflow shell
6. upload the graph
7. install it if the start type is non-manual
8. run a realistic test

## Common Workflow Patterns

### Manual intake flow

Use when a user starts a process directly and provides input.
Typical pattern:

- `FORM`
- `FUNCTION`
- optional `AGENT`
- `END`

### Approval flow

Use when the process needs review and a conditional branch.
Typical pattern:

- `FORM`
- `FUNCTION` for initial write
- `DECISION`
- approval or rejection branch
- `END`

### Scheduled batch flow

Use when the process runs on a schedule and processes queued work.
Typical pattern:

- scheduled start
- `FUNCTION` or `AGENT`
- optional `LOOP`
- `END`

### Datastore-trigger flow

Use when table changes should trigger downstream automation.
Typical pattern:

- `DATASTORE_EVENT`
- `FUNCTION`
- optional `AGENT`
- `END`

## Canonical Workflow Create

```bash
lemma workflow create --pod-id <pod-id> --payload '{
  "name": "expense-intake",
  "description": "Collect an expense and persist it",
  "mode": "USER",
  "start": {"type": "MANUAL"}
}'
```

## Canonical Graph Update

Use the flat Typer command name:

```bash
lemma workflow graph-update expense-intake --pod-id <pod-id> --payload-file ./payloads/workflow-graph.json
```

Minimal manual graph pattern:

```json
{
  "start": {"type": "MANUAL"},
  "nodes": [
    {
      "id": "collect_input",
      "type": "FORM",
      "label": "Collect expense",
      "config": {
        "input_schema": {
          "type": "object",
          "properties": {
            "merchant": {"type": "string"},
            "amount": {"type": "number"}
          },
          "required": ["merchant", "amount"]
        }
      }
    },
    {
      "id": "save_expense",
      "type": "FUNCTION",
      "label": "Save expense",
      "config": {
        "function_name": "save-expense",
        "input_mapping": {
          "merchant": {"type": "expression", "value": "collect_input.merchant"},
          "amount": {"type": "expression", "value": "collect_input.amount"}
        }
      }
    },
    {
      "id": "end_flow",
      "type": "END",
      "label": "Done",
      "config": {}
    }
  ],
  "edges": [
    {"id": "e1", "source": "collect_input", "target": "save_expense"},
    {"id": "e2", "source": "save_expense", "target": "end_flow"}
  ]
}
```

## Run Lifecycle

```bash
lemma workflow get expense-intake --pod-id <pod-id>
lemma workflow list --pod-id <pod-id>
lemma workflow run-start expense-intake --pod-id <pod-id> --payload '{"merchant":"Swiggy","amount":88.5}'
lemma workflow run-get <run-id> --pod-id <pod-id>
lemma workflow run-list expense-intake --pod-id <pod-id>
lemma workflow run-resume <run-id> --pod-id <pod-id> --payload '{"merchant":"Swiggy","amount":88.5}'
```

## Verification Rules

Always validate a workflow with a realistic run.
Check:

- the run starts successfully
- node transitions make sense
- input mappings resolve correctly
- waiting states behave as expected
- downstream functions or agents are invoked correctly
- every `FUNCTION` node still maps to a documented standalone function run example

For non-manual starts, also verify install behavior and triggering conditions.

## Common Mistakes

- using old nested command forms like `workflow graph update`
- using `agent_id` or `function_id` inside node config
- guessing payload shapes instead of inspecting the live schema
- building the workflow before the referenced functions or agents exist
- skipping install for non-manual starts

## Inspect Operation Shapes First

```bash
lemma operation show workflow.create
lemma operation show workflow.graph.update
lemma operation show workflow.install.create
lemma operation show workflow.run.start
```

## Known CLI Behavior

Read shared CLI behavior notes in [`../lemma-main/references/known-cli-behavior.md`](../lemma-main/references/known-cli-behavior.md).

## Related Skills

Route to:

- `lemma-functions` for deterministic steps
- `lemma-agents` for judgment-heavy steps
- `lemma-integrations` for event-triggered flows tied to external apps
- `lemma-main` when the operating model still needs design work
