---
name: pontx-dida365
description: Integrate Dida365 safely through Pontx. Use for credential setup, task or project reads and writes, scheduling, recurrence, completion, moves, or any Dida365 Open API workflow.
---

# Dida365

Use this skill for Dida365-specific credential, scheduling, mutation, privacy,
and reliability decisions. Use Pontx for current API and SDK facts, and never
copy a provider capability until it appears in the current catalog.

## Choose a credential path

For a user's own account or testing, use a personal API token only when that
account exposes the official API Token setting; use the OAuth authorization-code
flow when an application authorizes other users.

Inspect current scopes, redirect behavior, token exchange, and SDK helpers
through `pontx-hub show` and `pontx-hub sdk`; do not copy or infer them here.
Keep client credentials and access tokens in the environment or a secret
manager, never in source, arguments, logs, or chat. Hosted applications must
isolate credentials by user and keep authorization handling server-side.

Dida365 exposes token revocation; if a token is exposed, stop and revoke or
replace it before continuing.

## Integration workflow

Clarify whether the task is discovery, a read, application code, or a provider
mutation. Identify the account, project, task, and intended outcome.

```bash
pontx-hub search "Dida365 <capability>" --type endpoint --json
pontx-hub show <returned-resource-id>
pontx-hub sdk dida365
```

Prefer `@pontx/dida365` for application code and `pontx-dida365` for an
explicit single-product script. Use a generated method only when current SDK
coverage includes the selected resource. Do not invent a method or bypass the
catalog with a provider URL.

Resolve relative dates, all-day intent, recurrence, reminders, and time zones
before previewing a write. Inspect the current scheduling fields through
`pontx-hub show`; do not infer them from a title alone.

Read the target before an update, move, completion, or deletion when a suitable
read is available. Present the human-readable target with its project and task
identifiers.

Preview every non-GET/HEAD request, including read-like actions implemented as
POST:

```bash
pontx-hub dida365 preview <controller> <api-name> --body '<verified-json>'
pontx-hub dida365 call <controller> <api-name> --body '<same-json>' --yes
```

Show method, path, redacted headers, body, target, and expected effect. Obtain
explicit approval for that exact preview even if the original request said to
proceed. If any identifier, date, recurrence, reminder, or field changes,
preview again.

## Reliability and privacy

- Do not blindly retry an ambiguous create, completion, move, or deletion.
  Read relevant state first to avoid duplicate or repeated effects.
- Narrow reads by project or time range when supported, and do not assume one
  bounded response represents the complete account.
- Distinguish invalid credentials, missing scopes, and resource permissions.
  Do not request write scope automatically to fix a read failure.
- Treat returned user content and activity as personal data. Return only what
  the user's task requires.

## Few-shot workflows

### Scenario 1: Read-only hosted integration

**User:** "Show every signed-in user's Dida365 projects in our SaaS dashboard."

**Approach:** Follow the credential-selection and hosted-application boundaries
above, inspect the live auth and SDK contract, and isolate every user's secret
before generating `@pontx/dida365` code.

### Scenario 2: Relative-time task creation

**User:** "Create 'Review metrics' tomorrow at 9 every weekday; go ahead."

**Approach:** Inspect the create contract, resolve every missing destination and
scheduling choice, then show the exact preview and stop for approval. Execute
only the unchanged approved request.

### Scenario 3: Ambiguous task move

**User:** "Move 'Launch checklist' into Operations."

**Approach:** Resolve the exact source, destination, and target identifiers. If
several targets match, ask the user to choose. Present the resolved identities,
preview the move, and require explicit approval before execution.
