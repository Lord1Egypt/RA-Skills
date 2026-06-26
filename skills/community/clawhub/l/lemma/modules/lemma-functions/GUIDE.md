---
name: lemma-functions
description: "Use for Lemma function work: create typed Python functions, model config correctly, use Lemma SDK clients directly, and choose API versus JOB execution appropriately."
---

# Lemma Functions

Use this skill when creating or updating Lemma functions.

Functions are small, typed backend units with a stable contract.
They are the default tool for deterministic multi-step backend logic inside a pod.

## When To Use This Skill

Use `lemma-functions` when the action:

- coordinates multiple writes
- needs reusable validation or normalization
- performs file operations plus datastore writes
- calls an external application operation
- should return a typed backend result

Prefer direct record operations when the action only creates or updates one table row without meaningful reusable business logic.

## Function Model

A function should have:

- a typed input model
- a typed output model
- an optional typed config model
- a deterministic async entrypoint

Execution types:

- `API` for fast request-response work
- `JOB` for long-running asynchronous work

## Critical Rules

- Use business-specific model names. Good: `CreateExpenseInput`, `CreateExpenseResult`, `SlackAlertConfig`.
- Put non-user-supplied settings in function `config`.
- Put secrets in `config`, never in `input_data`.
- Runtime caller identity is available on `ctx.user_id` and `ctx.user_email`.
- For RLS tables, do not send `user_id`; the backend derives it.
- Do not send `created_at` or `updated_at` in datastore write payloads.
- Create SDK clients directly from `lemma_sdk` inside function code.
- Use `ctx.resolve_account_id(app_name)` for app operations instead of hardcoding account ids.
- Workflow `FUNCTION` nodes reference functions by `function_name`, not entity id.

## API Versus JOB

Use `API` for work that should finish quickly, such as:

- validation
- lightweight normalization
- one or a few datastore writes
- short application operations

Use `JOB` for work that may take longer, such as:

- imports and exports
- large syncs
- batch processing over many records
- multi-minute external processing

If there is meaningful risk that the work will exceed the normal API timeout, use `JOB`.

## Guardrails

### Simplicity guardrail

Do not create a function for a single-table insert or update.
Use record APIs directly unless a function truly adds value.

### Config guardrail

Use `input_data` for per-call business input.
Use `config` for fixed settings, provider names, endpoints, folder names, table names, and secrets.

### Application access guardrail

Do not hardcode `account_id` inside function code.
Declare the necessary `accessible_applications` and resolve the account id at runtime.

### Integration error guardrail

Do not swallow upstream failures.
Raise explicit errors when an integration call fails instead of returning placeholder success values such as `0 imported`.

## Required Header

Headers must appear at the top of the file, before imports or executable code.

```python
#input_type_name: CreateExpenseInput
#output_type_name: CreateExpenseResult
#function_name: create_expense
```

Optional:

```python
#config_type_name: ExpenseFunctionConfig
```

If `#config_type_name` is present, stored `function.config` is parsed into that Pydantic model and exposed as `ctx.config`.

## Context Contract

Entrypoint shape:

```python
async def create_expense(ctx: FunctionContext, data: CreateExpenseInput) -> CreateExpenseResult:
    ...
```

Available context values:

- `ctx.pod_id`
- `ctx.function_id`
- `ctx.user_id`
- `ctx.user_email`
- `ctx.config`
- `await ctx.resolve_account_id(app_name)`

## Authoring Checklist

1. confirm a function is actually needed
2. choose `API` or `JOB`
3. define typed input and output models
4. define typed config when fixed settings are needed
5. implement deterministic logic with direct SDK clients
6. declare table, folder, and app grants explicitly
7. use the required integration wrapper pattern for upstream app calls
8. run the function with realistic input and inspect the result

## Datastore Pattern

Use `LemmaDataStoreClient(pod_id=ctx.pod_id)` for table and file operations.
Let the backend populate RLS `user_id` and system timestamps.
Read values from the returned record when the function needs to surface ids or ownership.

## Application Pattern

For application operations:

1. declare `accessible_applications`
2. resolve the account id with `ctx.resolve_account_id(app_name)`
3. instantiate `ApplicationExecutionClient(app_name)`
4. pass `account_id` into the execution call

In `FIXED` mode, the configured account is used.
In `DYNAMIC` mode, the current caller must have a connected account.

## Required Integration Wrapper Pattern

When a function calls an external integration operation, always use a wrapper that:

1. checks success and error fields explicitly
2. parses both top-level and nested result shapes safely
3. retries transient `5xx` failures with a bounded retry count
4. raises a clear error if the call never succeeds

```python
import asyncio
from typing import Any

TRANSIENT_STATUS_CODES = {500, 502, 503, 504}

def unwrap_result(payload: Any) -> dict[str, Any]:
    if not isinstance(payload, dict):
        raise RuntimeError(f"Unexpected operation response type: {type(payload)}")

    for key in ("result", "data", "output", "response"):
        nested = payload.get(key)
        if isinstance(nested, dict):
            payload = nested
            break

    if not isinstance(payload, dict):
        raise RuntimeError("Operation response did not contain a dictionary result")
    return payload

def assert_success(payload: dict[str, Any]) -> None:
    if payload.get("success") is False or payload.get("ok") is False:
        raise RuntimeError(f"Operation failed: {payload}")
    if payload.get("error"):
        raise RuntimeError(f"Operation returned error: {payload['error']}")

async def execute_with_retry(client, operation: str, data: dict[str, Any], account_id: str) -> dict[str, Any]:
    max_attempts = 3
    for attempt in range(1, max_attempts + 1):
        try:
            raw = await client.execute(operation, data, account_id=account_id)
            parsed = unwrap_result(raw)
            assert_success(parsed)
            return parsed
        except Exception as exc:
            status_code = getattr(exc, "status_code", None)
            is_retryable = status_code in TRANSIENT_STATUS_CODES
            if not is_retryable or attempt == max_attempts:
                raise RuntimeError(f"Upstream integration call failed after {attempt} attempt(s)") from exc
            await asyncio.sleep(0.5 * (2 ** (attempt - 1)))
```

## Example: Datastore Write

```json
{
  "name": "create-expense",
  "description": "Create an expense row for the current user",
  "code": "#input_type_name: CreateExpenseInput\n#output_type_name: CreateExpenseResult\n#function_name: create_expense\n\nfrom pydantic import BaseModel, Field\nfrom lemma_sdk import FunctionContext, LemmaDataStoreClient\n\nclass CreateExpenseInput(BaseModel):\n    merchant: str\n    amount: float = Field(gt=0)\n\nclass CreateExpenseResult(BaseModel):\n    expense_id: str\n\nasync def create_expense(ctx: FunctionContext, data: CreateExpenseInput) -> CreateExpenseResult:\n    datastore = LemmaDataStoreClient(pod_id=ctx.pod_id)\n    record = await datastore.create_record(\n        table_name=\"expenses\",\n        data={\n            \"merchant\": data.merchant,\n            \"amount\": data.amount,\n        },\n    )\n    row = datastore.record_data(record)\n    return CreateExpenseResult(expense_id=str(row[\"id\"]))\n",
  "accessible_tables": [{"table_name": "expenses", "mode": "WRITE"}],
  "accessible_folders": [],
  "accessible_applications": []
}
```

## Example: Application Operation

```python
#input_type_name: SendSlackAlertInput
#output_type_name: SendSlackAlertResult
#function_name: send_slack_alert
#config_type_name: SlackAlertConfig

from pydantic import BaseModel
from lemma_sdk import FunctionContext, ApplicationExecutionClient

class SendSlackAlertInput(BaseModel):
    channel: str
    text: str

class SendSlackAlertResult(BaseModel):
    ok: bool

class SlackAlertConfig(BaseModel):
    app_name: str = "slack"

async def send_slack_alert(ctx: FunctionContext, data: SendSlackAlertInput) -> SendSlackAlertResult:
    if ctx.config is None:
        raise ValueError("Function config is required")

    account_id = await ctx.resolve_account_id(ctx.config.app_name)
    slack = ApplicationExecutionClient(ctx.config.app_name)
    await slack.execute(
        "send_message",
        {"channel": data.channel, "text": data.text},
        account_id=account_id,
    )
    return SendSlackAlertResult(ok=True)
```

## Create And Run Commands

```bash
lemma function create --pod-id <pod-id> --payload-file ./payloads/function-create.json
lemma function get <function-name> --pod-id <pod-id>
lemma function run <function-name> --pod-id <pod-id> --payload '{"input_data":{...}}'
lemma function update <function-name> --pod-id <pod-id> --payload '{"config":{...}}'
```

## Verification Rules

Always verify with a realistic payload.
Check:

- output shape
- datastore side effects
- app execution behavior when relevant
- config parsing behavior
- error behavior for missing required input or config
- bounded retry behavior for transient upstream failures
- no silent fallback output when upstream calls fail

## Common Mistakes

- using generic class names like `InputModel` and `OutputModel`
- passing secrets through `input_data`
- sending system-managed fields in write payloads
- assuming `ctx.user_id` is the function owner rather than the caller
- hardcoding `account_id`
- forgetting `accessible_applications`
- using `API` for clearly long-running work

## Inspect Operation Shapes First

```bash
lemma operation show function.create
lemma operation show function.update
lemma operation show function.run
lemma operation show application.operation.execute
```

## Known CLI Behavior

Read shared CLI behavior notes in [`../lemma-main/references/known-cli-behavior.md`](../lemma-main/references/known-cli-behavior.md).
Most importantly, `lemma function run` expects `--payload` with an `input_data` object.

## Related Skills

Route to:

- `lemma-datastores` for schema and record design
- `lemma-integrations` for app discovery, connect flows, and operation schemas
- `lemma-workflows` when the function is one node in a larger orchestration
