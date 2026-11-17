# planify-cli Reference

Base invocation (pick the one that matches the install):

```bash
# Flatpak
flatpak run --command=io.github.alainm23.planify.cli io.github.alainm23.planify <command>

# Built from source
io.github.alainm23.planify.cli <command>
```

All commands print JSON to stdout, so results pipe cleanly into `jq`.

## add

Create a new task.

```bash
planify-cli add --content "Buy groceries" --project "Personal" --priority 1 --due 2025-01-15
```

| Option          | Short | Description                                         |
|-----------------|-------|-----------------------------------------------------|
| `--content`     | `-c`  | Task content (required)                             |
| `--description` | `-d`  | Task description                                    |
| `--project`     | `-p`  | Project name (defaults to Inbox)                    |
| `--project-id`  | `-i`  | Project ID (preferred over name — avoids ambiguity) |
| `--section`     | `-s`  | Section name                                        |
| `--priority`    | `-P`  | 1 = high, 2 = medium, 3 = low, 4 = none             |
| `--due`         | `-D`  | Due date (`YYYY-MM-DD`)                             |
| `--labels`      | `-l`  | Comma-separated label names                         |
| `--parent-id`   | `-a`  | Parent task ID (creates a subtask)                  |
| `--pin`         |       | Pin the task (`true`/`false`)                       |

## list-projects

List all projects.

```bash
planify-cli list-projects
```

Returns a JSON array of projects with their IDs. Run this before any
command that needs `--project-id`, or whenever a cached ID lookup misses.

## list

List tasks in a project.

```bash
planify-cli list --project "Personal"
```

| Option         | Short | Description                      |
|----------------|-------|----------------------------------|
| `--project`    | `-p`  | Project name (defaults to Inbox) |
| `--project-id` | `-i`  | Project ID (preferred over name) |

## update

Edit an existing task.

```bash
planify-cli update --task-id "abc123" --content "Updated task" --complete true
```

| Option          | Short | Description                               |
|-----------------|-------|-------------------------------------------|
| `--task-id`     | `-t`  | Task ID to update (required)              |
| `--content`     | `-c`  | New task content                          |
| `--description` | `-d`  | New description                           |
| `--project`     | `-p`  | Move to project by name                   |
| `--priority`    | `-P`  | 1 = high, 2 = medium, 3 = low, 4 = none   |
| `--due`         | `-D`  | Due date (`YYYY-MM-DD`)                   |
| `--labels`      | `-l`  | Comma-separated label names               |
| `--complete`    |       | Mark complete/incomplete (`true`/`false`) |
| `--pin`         |       | Pin/unpin the task (`true`/`false`)       |

`--task-id` should always come from a prior `add`, `list`, or cache lookup
in this session — never guessed.

## backup

Export everything (tasks, projects, sections, labels, sources) as JSON.
Only run this when the user explicitly asks for a backup or export.

```bash
planify-cli backup --output ~/backup.json
```

| Option     | Short | Description                           |
|------------|-------|---------------------------------------|
| `--output` | `-o`  | Output file path (defaults to stdout) |

Useful for scripted/cron backups, but this skill should never schedule or
trigger one on its own — the user drives when their data gets exported.

## Common one-liners

```bash
# High-priority task with labels
planify-cli add -c "Fix login bug" -p "Work" -P 1 -D 2025-04-10 -l "bug,urgent"

# Subtask
planify-cli add -c "Write unit tests" -p "Work" --parent-id "abc123"

# Complete a task
planify-cli update --task-id "abc123" --complete true

# Move a task to another project
planify-cli update --task-id "abc123" --project "Personal"

# List project names only
planify-cli list-projects | jq '.[].name'
```
