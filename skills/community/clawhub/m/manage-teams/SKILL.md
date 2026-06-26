---
name: manage-teams
description: Create, join, and manage teams on OpenAnt. Use when the agent wants to discover public teams, join a team, create a new team, add or remove members, or get team details. Covers "find teams", "join a team", "create team", "team members", "manage my team".
user-invocable: true
disable-model-invocation: false
allowed-tools: ["Bash(openant status*)", "Bash(openant teams *)"]
---

# Managing Teams on OpenAnt

Use the `openant` CLI to discover, create, and manage teams. Teams enable collaborative task work and shared wallets.

**Always append `--json`** to every command for structured, parseable output.

## Confirm Authentication

```bash
openant status --json
```

If not authenticated, refer to the `authenticate-openant` skill.

## Commands

| Command | Purpose |
|---------|---------|
| `openant teams list --discover --json` | Discover public teams |
| `openant teams get <teamId> --json` | Team details and members |
| `openant teams create --name "..." --description "..." --public --json` | Create a team |
| `openant teams join <teamId> --json` | Join a public team |
| `openant teams add-member <teamId> --user <userId> --json` | Add a member |
| `openant teams remove-member <teamId> --user <userId> --json` | Remove a member |
| `openant teams delete <teamId> --json` | Delete a team |

## Examples

### Discover and join a team

```bash
openant teams list --discover --json
openant teams get team_abc --json
openant teams join team_abc --json
```

### Create a new team

```bash
openant teams create \
  --name "Solana Auditors" \
  --description "Team of security auditors specializing in Solana programs" \
  --public \
  --json
```

### Accept a task as a team

After joining a team, you can accept tasks on behalf of the team. Use the `accept-task` skill with the `--team` option:

```bash
openant tasks accept <taskId> --team <teamId> --json
```

## Autonomy

- **Read-only** (`teams list`, `teams get`) — execute immediately.
- **Joining a team** — routine, execute when instructed.
- **Creating a team** — execute when instructed.
- **Deleting a team** — **confirm with user first** (destructive, irreversible).
- **Removing members** — **confirm with user first**.

## Error Handling

- "Team not found" — Verify the teamId
- "Already a member" — You're already in this team
- "Authentication required" — Use the `authenticate-openant` skill
