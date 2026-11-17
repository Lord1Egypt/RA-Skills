---
name: git-distributed-todo
slug: git-distributed-todo
displayName: Git Distributed Todo
description: Coordinate shared Todo tasks and consolidated reminders across Hermes, OpenClaw, ChatGPT/Codex, WorkBuddy, and other agents through Git.
version: 1.1.0
---

# Git Distributed Todo

Coordinate independent AI agents through a shared Git repository without requiring a public IP, central database, or always-on coordination service. Keep each agent runtime's private/internal state local.

## Core rules

- Store one task per JSON file under `tasks/`; never make every agent edit one shared `todos.json`.
- Give every participating agent a stable lowercase ID such as `nas-agent`, `dev-agent`, or `workbuddy-laptop`.
- Set `created_by` to the creating agent and `executor` to the agent responsible for lifecycle updates.
- Treat the executor as the task's single lifecycle writer after creation.
- Designate exactly one agent as the user-facing notifier. Other agents must not independently send due-task reminders.
- Record successful notification in `receipts/<notifier>/`; never update task files merely to mark a reminder as sent.
- Sync before decisions and writes. Treat Git as eventually consistent, not transactional.
- Assign an executor explicitly. Do not build a competing-worker claim queue on Git.

Never synchronize an agent runtime's internal databases, sessions, memories, cron state, credentials, or home directory through this skill.

## Requirements

Require:

- Git with access to the same remote repository from every host.
- Python 3.10+.
- A Git commit identity (`user.name` and `user.email`) on every host.
- A shell/command execution capability in the agent host.

Git hosting requires only outbound fetch/push access. Private GitHub/GitLab/other Git hosting therefore works when none of the agent machines has a public IP. A LAN-only bare repository also works when every host can reach it.

For host-specific installation locations and invocation notes, read `references/compatibility.md` only when installing or adapting this skill to a particular agent runtime.

## Quick start (one-time setup)

After installing the skill, run the setup wizard once on each participating host:

```bash
python3 "$SKILL_DIR/scripts/git_todo.py" setup
```

It asks for (or accepts via flags):

- `--repo` — where the shared Todo clone lives (default `~/shared-todo`; created if missing)
- `--agent` — this host's stable lowercase agent id (default: hostname-derived)
- `--remote` — the shared Git remote URL; leave blank to create a local bare repo next to the working tree for single-host use

Agent-friendly non-interactive variant:

```bash
python3 "$SKILL_DIR/scripts/git_todo.py" setup \
  --repo ~/shared-todo --agent nas-agent --remote git@github.com:me/todo.git
```

Setup initializes the repository, publishes the initial commit to the remote, and records the agent id in `.git-distributed-todo.json`. That recorded id is used as a fallback whenever `AGENT_TODO_ID` is unset, so later commands work with no environment variables at all. `bootstrap` remains available for repositories created outside `setup`.

## Configure each agent

`setup` is the supported path — it configures the repo, the remote, and the agent id in one step. If you prefer environment variables instead, set them per host:

```bash
export AGENT_TODO_REPO=/absolute/path/to/shared-todo-clone
export AGENT_TODO_ID=nas-agent
```

Use a different `AGENT_TODO_ID` on every agent. Legacy `HERMES_TODO_REPO` and `HERMES_TODO_AGENT` variables remain accepted for backward compatibility.

Never store Git tokens, passwords, SSH private keys, messaging credentials, or private conversation transcripts in task files or commits. Use the host's normal Git credential mechanism.

## Resolve the bundled CLI

Resolve the directory containing this `SKILL.md` using the host runtime's skill-directory mechanism. Run `scripts/git_todo.py` from that directory. The CLI emits JSON for reliable agent parsing.

Examples below use `SKILL_DIR` as a conceptual variable; do not assume the host literally defines that environment variable.

Initialize a new shared Todo repository once (see Quick start; `setup` also asks for the remote and the agent id):

```bash
python3 "$SKILL_DIR/scripts/git_todo.py" setup
# or, on a repo you already created and pushed yourself:
python3 "$SKILL_DIR/scripts/git_todo.py" bootstrap
```

Create a task assigned to this agent:

```bash
python3 "$SKILL_DIR/scripts/git_todo.py" create \
  --title "Check NAS SMART status" \
  --executor nas-agent \
  --due-at "2026-08-07T09:00:00+08:00" \
  --priority high
```

Delegate work to another agent:

```bash
python3 "$SKILL_DIR/scripts/git_todo.py" create \
  --title "Build Android release" \
  --executor dev-agent \
  --due-at "2026-08-07T18:00:00+08:00"
```

List an agent's open work:

```bash
python3 "$SKILL_DIR/scripts/git_todo.py" list --executor dev-agent --status todo,doing
```

Start and complete assigned work:

```bash
python3 "$SKILL_DIR/scripts/git_todo.py" start <task-id>
python3 "$SKILL_DIR/scripts/git_todo.py" complete <task-id> --result "assembleRelease succeeded"
```

## Consolidate reminders

Only the designated notifier should run the reminder loop.

Query all due, open, notification-enabled tasks across every agent:

```bash
python3 "$SKILL_DIR/scripts/git_todo.py" due --notifier nas-agent
```

Combine the returned `tasks` array into exactly one user-facing digest. Include the executor label so the user can see which agent/machine owns each task. Send nothing when `count` is zero.

Only after the combined message is successfully delivered, record receipts for every delivered task. Pass multiple IDs together so the digest creates one managed update:

```bash
python3 "$SKILL_DIR/scripts/git_todo.py" mark-notified <task-id-1> <task-id-2> --notifier nas-agent
```

Do not create equivalent due-task notification schedules on every host. A failover notifier may exist, but keep it disabled until the primary notifier is unavailable.

## Task lifecycle

Use:

`todo -> doing -> done`

Allow `todo` or `doing` to become `cancelled`. Do not silently reopen `done` or `cancelled`; create a new task for new work.

The CLI enforces executor ownership for lifecycle writes. If the wrong agent is asked to start, complete, or cancel a task, route the request to the declared executor instead of overriding ownership.

## Consistency and failures

The CLI pulls before normal shared-state operations and commits/pushes managed changes. If another host pushes first, it fetches, rebases, and retries the push up to three times.

If a rebase produces a content conflict, the CLI aborts the rebase and reports the conflict. Never force-push as automatic recovery.

Resolve conflicts by preserving completed work and the newest intentional user change while respecting executor ownership, then sync normally.

If the Git remote is unreachable, do not claim another agent has seen a local change. A local commit may remain unpublished until a later successful sync. Use `--no-sync` only for deliberate cached/local inspection; normally require a successful sync before acting on cross-host state.

Reminder delivery is at-least-once, not exactly-once. If message delivery succeeds but receipt publishing fails, a later notifier run can repeat the reminder. Prefer an occasional duplicate over incorrectly marking an undelivered reminder as delivered. Avoid overlapping notifier runs.

## Boundaries

Do not use this skill as a high-frequency distributed queue or lock. Use a real database/message queue when the workflow requires sub-second dispatch, strong consistency, many competing workers, or transactional claiming.

Do not synchronize agent databases or private runtime state through Git, NFS, SMB, Syncthing, or similar mirroring. Synchronize only the portable task records created by this workflow.
