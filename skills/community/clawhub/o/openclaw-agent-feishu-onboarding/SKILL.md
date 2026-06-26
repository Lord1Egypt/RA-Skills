---
name: openclaw-agent-feishu-onboarding
description: Create OpenClaw agents and onboard Feishu routing with explicit multi-step confirmations. Use when the user needs to (1) define a new agent role and workspace, (2) collect and confirm Feishu route fields including peer.id, (3) apply account/peer bindings, and (4) validate routing and rollback safely.
---

# OpenClaw Agent Feishu Onboarding

Standardize creation of new OpenClaw agents and Feishu route binding.
Use this skill for operational execution with strict confirmations.

## Runtime Prerequisites
- Required binaries:
  - `openclaw` (CLI available in PATH)
  - `python` (3.x, used by `scripts/validate_feishu_bindings.py`)
- Preflight checks:
  - `openclaw --version`
  - `python --version`
- Data access behavior:
  - Reads local OpenClaw config (`openclaw.json` / `OPENCLAW_CONFIG_PATH`)
  - May write local agent and routing state (`agents.list[]`, `bindings[]`)
  - Do not run on machines where local config access is not permitted

## Core Scope
- Create a new agent (`agents.list` + workspace + identity).
- Confirm Feishu route target fields before any write.
- Bind routing using `bindings.match` with `channel/accountId/peer`.
- Verify final route and provide rollback steps.

## Required Inputs
- Agent intent:
  - Agent purpose and responsibility boundary.
  - Explicit out-of-scope items.
- Agent spec:
  - `agentId` (lowercase, digits, hyphen).
  - `workspace` path.
  - `model` id.
  - Identity object in `agents.list[]`:
    - use `identity` object (for example `identity.name`, `identity.emoji`, `identity.theme`)
    - do not rely on top-level `name` only
- Feishu route spec:
  - `match.channel`: `feishu`
  - `match.accountId`: for example `main`
  - `match.peer.kind`: `group` (or `dm` when needed)
  - `match.peer.id`: Feishu session id (group id like `oc_xxx` or dm id)

## Hard Validation Gates (Must Pass)
- `agents.list[]` entry for new agent must include `identity` object.
- `identity.name` must be set for human-readable routing/debug checks.
- `match.accountId` must be one of `channels.feishu.accounts` keys (for example `main`).
- Never put Feishu group/session id (`oc_xxx`) into `match.accountId`.
- Group routing must include `match.peer = { kind: "group", id: "oc_xxx" }`.
- If routing is for a specific group but `match.peer` is missing, abort and correct config before continuing.
- Before write, print the final binding object and require explicit confirmation.

## Multi-Step Confirmation Protocol
Do not skip confirmations. Ask and confirm in this exact order.

1. Confirmation A: Agent Goal
   - Confirm what this agent should do.
   - Confirm what this agent must not do.
2. Confirmation B: Agent Configuration
   - Confirm `agentId`, `workspace`, model, identity fields.
   - Confirm naming conventions and collision check (`agentId` uniqueness).
3. Confirmation C: Feishu Routing Target
   - Confirm `accountId`.
   - Confirm `peer.kind`.
   - Confirm `peer.id` (explicitly state this is the Feishu session id).
   - Confirm whether this is a precise peer binding or account-level fallback.
4. Confirmation D: Execution Approval
   - Summarize all fields in one compact block.
   - Ask for final go/no-go before writing config.

## Execution Workflow
1. Discover current state:
   - `openclaw agents list`
   - `openclaw config get agents.list --json`
   - `openclaw config get channels.feishu.accounts --json`
   - `openclaw directory groups list --channel feishu --account <account-id> --query "<keyword>" --json`
   - `openclaw config get bindings --json`
2. Create agent:
   - `openclaw agents add ...`
   - Optional: `openclaw agents set-identity ...`
3. Apply routing:
   - Use `openclaw agents bind` for account-scoped binding when needed.
   - Ensure peer-precise rule exists in top-level `bindings[]` with `match.peer`.
4. Validate:
   - `python -X utf8 ./scripts/validate_feishu_bindings.py --config <openclaw.json-path>`
   - `openclaw config validate --json`
   - ensure target `agents.list[]` entry has `identity.name`
   - Check `bindings[]` entry content and ordering.
   - Ensure every group-targeted rule has `match.peer.kind = "group"` and `match.peer.id = "oc_xxx"`.
5. Reload/restart gateway if required by deployment policy.

## Routing Rules
- `peer` rule is the precise route key for a specific Feishu conversation.
- Use `match.peer.id` to bind a specific session (group `oc_xxx`).
- If both peer-level and account-level bindings exist, keep peer rule first.
- Avoid broad fallback rules until peer-specific routes are confirmed.
- Wrong example (forbidden): `match.accountId: "oc_xxx"` without `match.peer`.

Agent list entry should follow this shape:

```json
{
  "id": "data-analyst",
  "workspace": "C:\\Users\\Administrator\\.openclaw\\workspace-dataAnalysis",
  "agentDir": "C:\\Users\\Administrator\\.openclaw\\agents\\data-analyst\\agent",
  "identity": {
    "name": "data-analyst"
  }
}
```

Canonical peer binding object:

```json
{
  "agentId": "<agent-id>",
  "match": {
    "channel": "feishu",
    "accountId": "main",
    "peer": {
      "kind": "group",
      "id": "oc_xxx"
    }
  }
}
```

## Safety and Rollback
- Never delete agents unless explicitly requested.
- Before changing `bindings`, capture current `bindings` snapshot.
- If wrong route is applied, revert to previous binding set and re-validate.
- Prefer reversible, explicit changes and post-change verification.

## Why It Still Routes to `main`
- Binding did not match the real incoming `peer.id` (most common).
- `bindings[]` was written but gateway runtime did not reload the latest config.
- `match.accountId` mismatched current Feishu account key.
- Target agent exists but `agents.list[]` entry is malformed (missing required fields such as `identity` object expected by your convention).
- Message arrived in a different conversation than the configured group.

## References
- Command examples and rollback snippets: [commands.md](./references/commands.md)
- Chinese runbook and confirmation checklist: [usage-zh.md](./references/usage-zh.md)
- Auto-check script: [validate_feishu_bindings.py](./scripts/validate_feishu_bindings.py)
