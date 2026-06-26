---
name: git-as-memory
description: Git-backed memory policy and CLI workflow for OpenClaw, Hermes, Claude Code, Codex, and other agents. Use when an agent should remember durable user preferences, project decisions, conventions, lessons learned, or query/audit Git-native memory with gam.
---

# Git as Memory

Use `git-as-memory` as a durable, auditable memory layer for agents. It stores memory in a dedicated Git ref, not in the working tree.

Default ref:

```bash
refs/git-as-memory/memory/v1
```

Supported agents: OpenClaw, Hermes, Claude Code, Codex, or any agent that can run shell commands.

## Setup

Prefer `gam` if installed:

```bash
command -v gam
```

If missing, install one of:

```bash
npm install -g git-as-memory
pip install git-as-memory
```

No global install:

```bash
npx git-as-memory --help
python -m git_as_memory.cli --help
```

All commands require a Git repo. If `--repo` is omitted, use the current working repo.

Initialize once per repo; it is idempotent:

```bash
gam init --repo /path/to/repo
```

## Memory Policy

Write memory only for stable, reusable information.

Write when:

- The user explicitly says to remember something.
- A stable user preference appears.
- A project convention, workflow, or decision is discovered.
- A recurring bug, workaround, tool behavior, or operational lesson is learned.
- A session produces a compact conclusion that future agents should reuse.

Do not write:

- Secrets, API keys, passwords, tokens, cookies, credentials, private auth material.
- Large raw transcripts or noisy logs.
- One-off task details with no future value.
- Unverified guesses unless `--type hypothesis`.
- Content that belongs in source files, docs, issues, or tests instead of memory.

Before writing:

1. Search for related memory first:
   ```bash
   gam search "<keywords>" --repo /path/to/repo
   ```
2. If a related memory exists, update the same stable id.
3. If not, create a concise new memory.
4. Always include `--source` explaining where the memory came from.

After writing, report the memory key:

```text
<type>/<id>
```

## Types

Use a small, consistent type set:

- `entity`: user, project, organization, tool, or other entity preference/profile.
- `semantic`: durable fact, rule, convention, decision, or technical lesson.
- `episodic`: compact summary of a task/session/event.
- `working`: short-lived task context that may be deleted later.
- `hypothesis`: unverified inference that should be confirmed before acting on strongly.

## Id Rules

Use stable kebab-case ids. Prefer names that future agents can guess.

Good:

```text
user-preference-concise-answers
project-release-workflow
openclaw-memory-policy
git-as-memory-storage-layout
```

Avoid random ids unless there is no stable concept.

## Core Commands

### Write

```bash
gam write "User prefers concise technical answers with concrete commands." \
  --repo /path/to/repo \
  --type entity \
  --id user-preference-concise-answers \
  --tag user \
  --tag preference \
  --source "User corrected the agent for over-explaining and asked for practical output."
```

Multi-line:

```bash
printf '%s\n' "Decision summary..." | gam write --stdin \
  --repo /path/to/repo \
  --type semantic \
  --id project-decision-example \
  --source "Summarized from the current implementation session."
```

### Read

Use `read` when you know the key:

```bash
gam read entity/user-preference-concise-answers --repo /path/to/repo
```

`show` is equivalent when using id plus optional type:

```bash
gam show user-preference-concise-answers --type entity --repo /path/to/repo
```

### Search

Use `search` for content lookup:

```bash
gam search "release workflow" --repo /path/to/repo
gam search "concise answers" --repo /path/to/repo --json
```

Search is local substring matching over memory content, tags, metadata, and source text.

### Glob

Use `glob` for memory key lookup, not arbitrary working-tree files. It matches `<type>/<id>` and bare ids:

```bash
gam glob "entity/*" --repo /path/to/repo
gam glob "user-*" --repo /path/to/repo
gam glob "*release*" --repo /path/to/repo
```

Use `--files` only for debugging the underlying Git tree:

```bash
gam glob "entity/*" --files --repo /path/to/repo
```

### List

```bash
gam list --repo /path/to/repo
gam list --repo /path/to/repo --json
```

### History and Audit

```bash
gam history user-preference-concise-answers --type entity --repo /path/to/repo
```

Direct Git inspection:

```bash
git -C /path/to/repo log --oneline refs/git-as-memory/memory/v1
git -C /path/to/repo ls-tree -r --name-only refs/git-as-memory/memory/v1
```

### Delete

Prefer soft delete:

```bash
gam delete user-preference-concise-answers --type entity --repo /path/to/repo
```

Use `purge` only when the user explicitly asks to remove the current visible files:

```bash
gam purge user-preference-concise-answers --type entity --repo /path/to/repo
```

## Agent Workflow

When starting a task in a repo:

1. If memory may matter, run targeted search:
   ```bash
   gam search "<project/tool/user keywords>" --repo /path/to/repo
   ```
2. Read only relevant matches.
3. Do not bulk-load all memory unless the user asks for an audit.

When a durable lesson appears:

1. Decide if it meets the write policy.
2. Search for duplicates.
3. Write or update one stable memory id.
4. Report the key and a one-line summary.

When the user asks "what do you remember?":

1. Use `gam list`, `gam glob`, or `gam search`.
2. Use `gam read` for relevant keys.
3. Include `gam history` only if provenance or evolution matters.

## Output Discipline

After a memory write, respond briefly:

```text
Remembered: entity/user-preference-concise-answers
```

If you decide not to write memory, say why only when useful:

```text
Not writing memory: this is a one-off task detail.
```
