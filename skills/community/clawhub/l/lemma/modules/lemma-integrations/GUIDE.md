---
name: lemma-integrations
description: "Use for Lemma integration work: discover app capabilities, connect accounts, inspect schemas, configure workload access, and execute third-party operations safely."
---

# Lemma Integrations

Use this skill for third-party app catalog work, connected accounts, trigger discovery, and runtime operation execution.

Integrations are how pods interact with external systems such as Slack, Gmail, GitHub, or Salesforce.

## When To Use This Skill

Use `lemma-integrations` when the work involves:

- listing available applications
- inspecting operations or triggers
- creating connect requests
- checking connected accounts
- executing third-party operations
- deciding between dynamic and fixed app access
- installing app-triggered workflows

## Core Model

- Integrations are global user-scoped resources, not pod resources.
- Pod workloads access apps through `accessible_applications`.
- Access `mode` is `DYNAMIC` or `FIXED`.
- `account_id` is required for `FIXED` access.
- For trigger-based workflows, you often need both an `application_trigger_id` and an install-time `account_id`.

## Default Rule

Never guess an operation payload.
Inspect the live schema first.

## Mandatory Pre-Function Smoke Test

Before writing or updating any function that calls an integration operation, run a smoke test and save real artifacts.

1. capture the live operation schema with `operation get`
2. execute the operation once with a realistic payload
3. save both outputs under `./artifacts/integrations/<app>/<operation>/`
4. block function coding until both artifacts exist and are parseable

Example:

```bash
mkdir -p ./artifacts/integrations/gmail/send_message
lemma integration operation get gmail send_message \
  > ./artifacts/integrations/gmail/send_message/operation-get.json
lemma integration operation execute gmail send_message \
  --account-id <account-id> \
  --payload-file ./payloads/send-message.json \
  > ./artifacts/integrations/gmail/send_message/operation-execute.json
```

## Standard Lifecycle

1. list the application
2. inspect operations or triggers
3. run operation smoke tests and save sample schema and response artifacts
4. create a connect request if no account exists
5. have the user complete the authorization URL
6. list accounts again
7. configure workload access with `DYNAMIC` or `FIXED`
8. execute the operation or install the trigger-based workflow

## Discovery Commands

```bash
lemma integration list --limit 100
lemma integration get gmail
lemma integration operation list gmail
lemma integration operation get gmail send_message
lemma integration trigger list github
lemma integration trigger get github_pull_request_opened
lemma integration account list github
```

## Connect Request

```bash
lemma integration connect-request create gmail
```

## Dynamic Versus Fixed Access

### DYNAMIC

Use `DYNAMIC` when the runtime should use the current caller's connected account.
This is common for user-facing assistants, desks, and functions that act on behalf of the current user.

### FIXED

Use `FIXED` when the workload should always use one designated service account or connected account.
This is common for back-office automation and shared operational flows.

## Canonical Operation Execute

```bash
lemma integration operation execute gmail send_message \
  --account-id <account-id> \
  --payload-file ./payloads/send-message.json
```

## Runtime Patterns

### Function runtime

Use `ctx.resolve_account_id(app_name)` inside functions and declare `accessible_applications` explicitly.

### Assistant runtime

Grant only the applications the assistant truly needs.
Require confirmation before external side effects.

### Desk runtime

Use the SDK client to list and execute operations with explicit `accountId` where required.

```ts
import { getClient } from "@/lib/client";

const client = getClient();
const ops = await client.integrations.operations.list("gmail");
const result = await client.integrations.operations.execute(
  "gmail",
  "send_message",
  { to: "finance@example.com" },
  { accountId: "<account-id>" },
);
```

### Workflow runtime

For app-triggered workflows, inspect the real trigger payload before designing mappings.
Install the workflow only after you know the trigger id and account id you need.

## Verification Rules

Always verify integrations with live state.
Check:

- the target app exists and the expected operation or trigger is present
- the needed account is connected
- the workload access mode matches the intended behavior
- the operation succeeds with a realistic payload
- smoke-test artifacts exist before function coding starts

## Troubleshooting

- if you need the app id, start with `lemma integration list`
- if execution fails, inspect the exact live schema again before changing payloads
- if no account exists, create a connect request instead of assuming auth is already complete
- if `FIXED` mode is used, confirm the configured `account_id` is correct

## Common Mistakes

- guessing operation payloads
- assuming an account is already connected
- using `FIXED` without an `account_id`
- treating integrations as pod-local resources
- authoring event mappings before inspecting the live trigger payload

## Known CLI Behavior

Read shared CLI behavior notes in [`../lemma-main/references/known-cli-behavior.md`](../lemma-main/references/known-cli-behavior.md) before writing commands or payloads.

## Related Skills

Route to:

- `lemma-functions` for backend app execution
- `lemma-assistants` when users trigger app actions conversationally
- `lemma-workflows` for trigger-based automation
- `lemma-desks` when the app interaction belongs in a full UI
