---
name: mac-reminder-bridge
description: "Manage macOS Reminders.app from Docker via HTTP bridge. Use when user says: set/add/create a reminder, remind me to X, cancel/delete a reminder, mark reminder done/complete, update/edit a reminder, show/list my reminders. Requires listener.py running on Mac at port 5000."
metadata:
  {
    "openclaw": {
      "emoji": "🔔",
      "requires": { "bins": ["curl"] }
    }
  }
---

# Skill: Mac Reminder Bridge

Control macOS Reminders.app from inside Docker via HTTP.
Base URL: `http://host.docker.internal:5000`

---

## When to use

| User intent | Endpoint |
|-------------|----------|
| "Remind me to / Set a reminder / Add a reminder" | POST `/add_reminder` |
| "Cancel / Delete my reminder to ..." | POST `/delete_reminder` |
| "Done with / Mark ... as complete" | POST `/complete_reminder` |
| "Unmark / reopen reminder ..." | POST `/complete_reminder` with `completed:false` |
| "Update / Change / Edit my reminder ..." | POST `/update_reminder` |
| "What are my reminders / Show reminders" | GET `/list_reminders` |
| "What lists do I have" | GET `/list_lists` |

---

## POST /add_reminder

```json
{
  "task":      "Buy groceries",
  "list":      "Shopping",
  "due":       "2025-12-31 09:00",
  "remind_at": "2025-12-31 08:50",
  "notes":     "Get milk and eggs",
  "priority":  "high"
}
```

- `task` required; all others optional
- `due` / `remind_at` format: `YYYY-MM-DD HH:MM`
- `priority`: `none` | `low` | `medium` | `high`
- `list`: leave empty to use the default list

---

## POST /update_reminder

```json
{
  "task":         "Buy groceries",
  "fuzzy":        false,
  "new_task":     "Buy organic groceries",
  "new_due":      "2025-12-31 10:00",
  "new_notes":    "Also get juice",
  "new_priority": "medium"
}
```

- `task` identifies which reminder to update
- Set `new_due` to `""` to clear the due date
- Only include the fields you want to change

---

## POST /delete_reminder

```json
{ "task": "Buy groceries", "fuzzy": false, "list": "" }
```

- `fuzzy: true` → match by "contains" (useful when unsure of exact wording)
- `list`: leave empty to search ALL lists

---

## POST /complete_reminder

```json
{ "task": "Buy groceries", "completed": true, "fuzzy": false }
```

- `completed: false` → un-check / reopen the reminder

---

## GET /list_reminders

```
GET /list_reminders
GET /list_reminders?list=Shopping
GET /list_reminders?completed=true
GET /list_reminders?completed=all
```

Returns structured JSON with task, due, notes, priority, completed, list.

---

## GET /list_lists

Returns all lists with pending/total counts and the default list name.

---

## GET /health

Check if listener is running and has Reminders permission.

---

## Agent step-by-step

### Adding a reminder
1. Extract: `task` (required), `due`, `remind_at`, `notes`, `priority`, `list`
2. POST `/add_reminder`
3. Confirm: "✅ Reminder set: <task>" + due date if applicable

### Deleting a reminder
1. Extract task name; use `fuzzy: true` if unsure of exact wording
2. POST `/delete_reminder`
3. Check `count`: if 0, say "⚠️ No reminder found matching '<task>'"

### Updating a reminder
1. Extract current name and what to change
2. POST `/update_reminder` with only the changed fields
3. Confirm what was changed

### Listing reminders
1. GET `/list_reminders` (add `?list=X` if user specifies a list)
2. Format results clearly, grouping by list if multiple lists present

### Health check before important ops
```bash
curl http://host.docker.internal:5000/health
```

### Auth header (if BRIDGE_SECRET is set)
```
X-Bridge-Secret: <secret>
```
