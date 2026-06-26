# Config Materialization Checklist (Mandatory)

Team creation is not complete unless OpenClaw config is materialized.

## 1) agents.list entries (required)
For each role, verify `openclaw.json -> agents.list[]` contains:
- id
- workspace
- model (or inherited policy)
- identity
- tools profile/policy
- subagents.allowAgents (A2A permission boundary)

## 2) A2A permissions (required)
- team-leader agent id should be team-prefixed (e.g., `<team>-team-leader`) to avoid cross-team id collision.
- `<team>-team-leader`.subagents.allowAgents must include all specialist roles.
- specialist roles must allow return path to `<team>-team-leader` at minimum.
- deny broad wildcard unless explicitly requested.

## 3) bindings entries (required)
- Ensure each intended channel route has a matching binding.
- If single-bot mode: at least team-leader binding exists.
- If multi-bot group mode: each bound role has explicit binding.

## 4) account/channel consistency checks
- binding.accountId must exist in channel accounts.
- no dangling binding to missing agent.
- no dangling binding to missing account.

## 5) completion gate
Return `ready` only when all checks pass.
Otherwise return `partially_ready` with exact missing config keys.
