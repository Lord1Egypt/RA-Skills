---
name: oo-oomol-console
description: "OOMOL Console (console.oomol.com). Use this skill for ANY OOMOL Console request — reading, creating, updating, and deleting data. Whenever a task involves OOMOL Console, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "OOMOL Console"
  author: "OOMOL"
  version: "1.0.6"
  services: ["oomol_console"]
  icon: "https://static.oomol.com/logo/third-party/oomol_console.svg"
---

# OOMOL Console

Operate **OOMOL Console** through your OOMOL-connected account. This skill calls the `oomol_console` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

OOMOL Console needs no account connection. Assume the oo CLI is installed and signed in. **Do not run `oo auth login` proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "oomol_console" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "oomol_console" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

### Private skills and team access

A bot joining a team does not share its owner's private skill packages. The
package must be added to that team by an identity with both package access and
team write permission. This grants access to the whole package without making
it public. It is separate from Connection permission groups and local skill
installation.

For an installation failure, establish the exact package, failing identity,
target team, active membership, and whether the package is configured for that
team. `list_my_skill_packages` lists only the authenticated identity's maintained
packages; an empty bot result says nothing about its owner's publications.
Read the current action schemas before calling them. Keep team-scoped calls on
the intended team, using a per-command team override when needed.

When the user requests a fix and the package and team are unambiguous, use
existing authorization to add the missing package and read the team list back.
Retry installation with the original failing identity only when that identity
is available; otherwise report that only team configuration was verified.
For a question about the cause, diagnose without changing access. If the caller
cannot access the package or write the team, explain the evidenced blocker and
direct an authorized user to select the target team at
https://console.oomol.com/skills. A 403 or 404 alone does not establish the cause.
Do not switch to the owner's identity, make the package public, or create a
temporary share to bypass the missing team authorization.

## Available actions

- `add_member` — Add an OOMOL user to the current team with the member role. [write]
- `add_skill_package_to_team` — Grant the current team access to an entire registry package, including its private skills. Requires package access and team write permission. Does not make the package public or install it locally. [write]
- `create_connection_permission_group` — Create a custom Connection permission group and replace the assignments of its members. [destructive]
- `delete_connection_permission_group` — Delete a custom Connection permission group so its members return to the default group. [destructive]
- `get_balance` — Return every available balance lot owned by the current OOMOL team creator. This account balance may be shared by multiple teams.
- `get_billing_summary` — Return current-team billing and usage metrics together with the team creator account balance.
- `get_current_scope` — Return the current OOMOL team scope and authenticated principal.
- `get_team_summary` — Return metadata and member counts for the current OOMOL team.
- `get_usage_breakdown` — Return the current OOMOL team daily usage breakdown by source and subject.
- `list_connection_executions` — List current-team Connection execution records visible to the authenticated user or service account.
- `list_connection_permission_groups` — List the default and custom permission groups for one current-team Connection.
- `list_members` — List members of the current OOMOL team.
- `list_my_skill_packages` — List skill packages maintained by the authenticated identity, including its private packages. A bot's results do not list its owner's packages. Supports keyword search and pagination.
- `list_team_connections` — List the current-team Connections visible to the authenticated user or service account.
- `list_team_skill_packages` — List skill packages configured for the current team. Team membership alone does not grant access to an unconfigured private package. This lists team configuration, not local installations.
- `list_teams` — List the OOMOL teams the authenticated user or service account belongs to.
- `remove_skill_package_from_team` — Revoke the current team's access through this package binding for the entire registry package. Requires package access and team write permission. Does not delete the package, change its visibility, remove other access grants, or uninstall local skills. [destructive]
- `update_connection_default_permission_group` — Replace the action permission of a Connection's non-deletable default permission group. [destructive]
- `update_connection_permission_group` — Replace the name, member assignments, and action permission of a custom Connection permission group. [destructive]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change OOMOL Console state — confirm the exact payload and effect with the user before running.**
- **Actions tagged `[destructive]` remove or overwrite data — always confirm the target and get explicit approval first.**

## First-time setup

These are **one-time** steps — do not repeat them on every call. Run a step only when a command fails for the matching reason.

- **`oo: command not found`** — install the oo CLI (other platforms: <https://cli.oomol.com/install-guide.md>):

  ```bash
  curl -fsSL https://cli.oomol.com/install.sh | bash    # macOS / Linux
  ```

  ```powershell
  irm https://cli.oomol.com/install.ps1 | iex           # Windows PowerShell
  ```

- **Not signed in / authentication error** — sign in to your OOMOL account once:

  ```bash
  oo auth login
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- OOMOL Console homepage: https://console.oomol.com
