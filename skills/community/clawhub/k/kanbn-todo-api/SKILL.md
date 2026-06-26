---
name: kanbn-todo-api
description: Manage personal TODOs in Kan.bn through API-driven operations. Use this whenever the user wants to create, update, move, prioritize, search, summarize, or clean up their own Kan.bn tasks or board data, even if they do not explicitly mention the API. Trigger on requests like "add a todo", "mark this P1", "move this to done", "find my invoice task", "update my Kan.bn profile", or similar single-user Kan.bn task-management workflows. Exclude multi-user collaboration, invites, integrations/imports, and attachments.
---

# Kan.bn TODO API

Use this skill to run Kan.bn personal task workflows via `scripts/kanbn_todo.py`.

Keep the interaction goal-oriented: figure out the user's intended task change, discover any missing IDs, execute the smallest correct API operation, then report the result clearly.

## Configure authentication

Set auth before running commands:

- `KANBN_TOKEN` for bearer auth, or
- `KANBN_API_KEY` for API-key auth.

Auth lookup order in `kanbn_todo.py`:

1. CLI flags (`--token`, `--api-key`, `--base-url`)
2. Process environment (`KANBN_TOKEN`, `KANBN_API_KEY`, `KANBN_BASE_URL`)
3. `~/.bashrc` `export` values (for non-interactive runs)

Optional:

- `KANBN_BASE_URL` (defaults to `https://kan.bn/api/v1`)

If auth is missing, stop early and ask for credentials or confirm the env source.

## Follow the standard execution flow

### 1) Discover context before mutating data

When the user has not provided concrete Kan.bn IDs, resolve them first.

```bash
python3 scripts/kanbn_todo.py me
python3 scripts/kanbn_todo.py workspaces
python3 scripts/kanbn_todo.py boards --workspace-id <workspacePublicId>
```

Use this discovery flow for requests like:

- "Add a todo in Kan.bn"
- "Move my task to done"
- "Find the board with invoices"

If the user already provided exact card/list/workspace IDs, skip the discovery steps you do not need.

### 2) Create, then read back

After creating a TODO, read it back when the user cares about confirmation, due date, labels, or returned IDs.

```bash
python3 scripts/kanbn_todo.py todo-create \
  --list-id <todoListPublicId> \
  --title "Pay electricity bill" \
  --description "Before Friday" \
  --due-date "2026-03-06T09:00:00.000Z"

python3 scripts/kanbn_todo.py todo-get --card-id <cardPublicId>
```

### 3) Prefer the narrowest mutation

Choose the command that most directly matches the requested change.

- Edit title/description/due date -> `todo-update`
- Change workflow status/list -> `todo-move`
- Add or remove a label -> `todo-label-toggle`
- Delete the task -> `todo-delete`

Edit fields:

```bash
python3 scripts/kanbn_todo.py todo-update \
  --card-id <cardPublicId> \
  --title "Pay electricity + water bill" \
  --description "Do both tonight"
```

Change status by moving lists (e.g., TODO -> DOING -> DONE):

```bash
python3 scripts/kanbn_todo.py todo-move \
  --card-id <cardPublicId> \
  --to-list-id <doingListPublicId>
```

Delete TODO:

```bash
python3 scripts/kanbn_todo.py todo-delete --card-id <cardPublicId>
```

## Apply the priority label policy

When a request asks to set, mark, sort, or batch-assign priorities, use labels (`P0`-`P4`) as the source of truth.

- Apply priority via label changes.
- Do not encode priority in titles.
- Keep task titles focused on the actual work item text.
- If the correct priority label ID is unknown, inspect board metadata first.
- Official Kan.bn docs expose label changes on a dedicated endpoint, not `todo-update`.

For an existing card:

```bash
python3 scripts/kanbn_todo.py todo-label-toggle \
  --card-id <cardPublicId> \
  --label-id <p1LabelPublicId>
```

## Use personal productivity workflows

Search tasks in a workspace:

```bash
python3 scripts/kanbn_todo.py search --workspace-id <workspacePublicId> --query "bill"
```

Add personal notes/comments:

```bash
python3 scripts/kanbn_todo.py comment-add --card-id <cardPublicId> --comment "Waiting for invoice"
```

Track subtasks with checklist:

```bash
python3 scripts/kanbn_todo.py checklist-add --card-id <cardPublicId> --name "Prep"
python3 scripts/kanbn_todo.py checkitem-add --checklist-id <checklistPublicId> --title "Download invoice"
python3 scripts/kanbn_todo.py checkitem-update --item-id <checklistItemPublicId> --completed true
```

Update the personal profile only when the user explicitly asks:

```bash
python3 scripts/kanbn_todo.py user-update --name "New Name"
```

## Handle missing information carefully

When the user asks for an operation but key identifiers are missing:

- Discover the smallest missing context first
- Prefer `search` when the user describes a task by text instead of card ID
- Prefer `boards` when the missing information is board or list structure
- Ask a follow-up question only after exhausting cheap discovery paths

Good examples:

- User says "mark my invoice task done" -> search for invoice-related cards, identify the likely card, then move it
- User says "add this to my finance board" -> resolve workspace and boards, then ask only if multiple plausible lists remain

## Read references only when needed

- Read `references/common-workflows.md` for reusable end-to-end task patterns
- Read `references/api-scope.md` when endpoint details or scope boundaries matter
- Read `references/smoke-test.md` after changing the script or when validating the skill against a live Kan.bn account

## Respect scope

Use only single-user TODO endpoints in this skill.

Do not run collaboration, invite, import, integration, or attachment flows here.
