# Smoke Test

Use this checklist after changing `scripts/kanbn_todo.py` or the surrounding skill workflow.

## Goal

Confirm that the CLI still parses arguments correctly, loads auth configuration as expected, and can reach the most important read/write flows.

## Safe local parser check

Run the built-in self-test first. It performs no network requests.

```bash
python3 scripts/kanbn_todo.py self-test
```

Expected result:

- JSON output with `ok: true`
- parser checks for `me`, `search`, `todo-create`, and `todo-label-toggle`
- auth-source preview fields present

## Live API smoke test

Only run this when valid Kan.bn credentials are available.

### 1. Read-only checks

```bash
python3 scripts/kanbn_todo.py me
python3 scripts/kanbn_todo.py workspaces
```

### 2. Pick a workspace and inspect boards

```bash
python3 scripts/kanbn_todo.py boards --workspace-id <workspacePublicId>
```

### 3. Create a disposable TODO

```bash
python3 scripts/kanbn_todo.py todo-create \
  --list-id <todoListPublicId> \
  --title "Smoke test task" \
  --description "Delete after verification"
```

### 4. Read it back

```bash
python3 scripts/kanbn_todo.py todo-get --card-id <cardPublicId>
```

### 5. Clean up

```bash
python3 scripts/kanbn_todo.py todo-delete --card-id <cardPublicId>
```

## Failure hints

- Missing auth -> confirm `KANBN_TOKEN` or `KANBN_API_KEY`
- Empty board/list context -> re-run discovery flow from the skill
- Unexpected HTTP errors -> inspect the returned JSON `details` payload before changing the skill logic
