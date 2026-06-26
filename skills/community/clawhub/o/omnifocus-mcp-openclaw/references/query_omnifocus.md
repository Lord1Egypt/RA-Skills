# `query_omnifocus` Reference

Use `query_omnifocus` for fast, targeted OmniFocus reads.

## Top-Level Parameters

- `entity`: one of `tasks`, `projects`, `folders`
- `filters`: optional narrowing rules
- `fields`: optional list of returned fields
- `limit`: optional max result count
- `sortBy`: optional sort field
- `sortOrder`: optional `asc` or `desc`
- `includeCompleted`: include completed items when needed
- `summary`: return counts instead of full details

## Common Filters

### Container filters

- `projectId`: exact project ID
- `projectName`: case-insensitive partial match
- `folderId`: exact folder ID
- `inbox`: `true` for inbox-only, `false` to exclude inbox

### Status filters

Task statuses commonly used:
- `Next`
- `Available`
- `Blocked`
- `DueSoon`
- `Overdue`
- `Completed`
- `Dropped`

Project statuses commonly used:
- `Active`
- `OnHold`
- `Done`
- `Dropped`

### Tag and flag filters

- `tags`: exact tag names, case-sensitive, OR logic
- `flagged`: true or false

### Date filters

Relative ranges:
- `dueWithin`
- `deferredUntil`
- `plannedWithin`

Exact day offsets:
- `dueOn`
- `deferOn`
- `plannedOn`

Day offsets are integer offsets from today:
- `0` means today
- `1` means tomorrow
- `-1` means yesterday when supported by the tool/server behavior

### Note filters

- `hasNote`: true or false

## Good Defaults

- Ask only for fields you need, such as `name`, `projectName`, `dueDate`, `tags`, `flagged`
- Add `limit` for any query that could return many tasks
- Use `summary: true` for counting or coarse status checks
- Sort by `dueDate` when discussing urgency
- Sort by `modificationDate` when looking for stale or recently changed work

## Example Shapes

### Tasks due today

```json
{
  "entity": "tasks",
  "filters": { "dueOn": 0 },
  "fields": ["name", "projectName", "dueDate"],
  "sortBy": "dueDate"
}
```

### Flagged tasks due this week

```json
{
  "entity": "tasks",
  "filters": { "flagged": true, "dueWithin": 7 },
  "fields": ["name", "projectName", "dueDate"],
  "sortBy": "dueDate",
  "sortOrder": "asc"
}
```

### Count active projects

```json
{
  "entity": "projects",
  "filters": { "status": ["Active"] },
  "summary": true
}
```

### Inbox triage view

```json
{
  "entity": "tasks",
  "filters": { "inbox": true },
  "fields": ["name", "note", "flagged"],
  "limit": 50
}
```

## Escalate To Other Tools

Switch away from `query_omnifocus` when:
- the user wants a full dump: use `dump_database`
- the user needs tag discovery: use `list_tags`
- the user needs perspective discovery or inspection: use `list_perspectives` or `get_perspective_view`
- the user wants changes applied: use the add, edit, remove, or batch tools
