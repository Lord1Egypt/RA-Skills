# Common Kan.bn Workflows

Use these patterns when the user gives a natural-language goal instead of API-shaped instructions.

## 1. Create a new TODO in the right place

Use when the user says things like:

- "Add a todo to Kan.bn"
- "Create a reminder in my finance board"
- "Track this in my tasks"

Suggested flow:

1. Resolve workspace and board if the target is unclear
2. Resolve the target list
3. Run `todo-create`
4. Read back the card if the user wants confirmation details

## 2. Find a task by meaning, then mutate it

Use when the user names a task informally, such as:

- "Move my invoice task to done"
- "Mark the tax reminder P1"
- "Delete the task about water bill"

Suggested flow:

1. Run `search --query <keywords>`
2. Identify the most likely card
3. If multiple plausible matches remain, ask a clarifying question
4. Run the narrowest mutation command (`todo-move`, `todo-label-toggle`, `todo-delete`, or `todo-update`)

## 3. Update priority using labels

Priority lives in labels, not titles.

Suggested flow:

1. Inspect board labels if the P0-P4 label IDs are unknown
2. Toggle the desired priority label with `todo-label-toggle`
3. Avoid editing the task title just to show priority

## 4. Use lists as status

Treat lists as workflow state.

Examples:

- TODO -> work not started
- DOING -> in progress
- DONE -> completed

When the user asks to change status, prefer `todo-move` instead of a generic field update.

## 5. Use comments and checklists for personal organization

Use comments when the user wants notes, rationale, or updates attached to a task.

Use checklists when the user wants subtasks, progress tracking, or explicit completion state.

## 6. Ask only after cheap discovery fails

Prefer discovery commands before asking the user for raw IDs.

Good order:

1. `me`
2. `workspaces`
3. `boards`
4. `search`
5. Clarifying question only if ambiguity remains
