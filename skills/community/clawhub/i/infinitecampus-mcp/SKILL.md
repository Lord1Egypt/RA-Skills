---
name: infinitecampus-mcp
description: This skill should be used when the user asks about Infinite Campus (Campus Parent) data for their student(s). Triggers on phrases like "check grades", "what's my kid's GPA", "any new assignments", "attendance record", "message the teacher", "Campus Parent inbox", "infinite campus", or any request involving school grades, assignments, attendance, messages, or documents in Infinite Campus.
---

# infinitecampus-mcp

MCP server for Infinite Campus Campus Parent — read student grades, attendance, assignments, and messages; download documents; and send messages.

- **npm:** [npmjs.com/package/infinitecampus-mcp](https://www.npmjs.com/package/infinitecampus-mcp)
- **Source:** [github.com/chrischall/infinitecampus-mcp](https://github.com/chrischall/infinitecampus-mcp)

## Setup

### Option A — npx (recommended)

Add to `.mcp.json` in your project or `~/.claude/mcp.json`:

```json
{
  "mcpServers": {
    "infinitecampus": {
      "command": "npx",
      "args": ["-y", "infinitecampus-mcp"],
      "env": {
        "IC_BASE_URL": "https://campus.yourdistrict.k12.example.us",
        "IC_DISTRICT": "your-district-appname",
        "IC_USERNAME": "parent@example.com",
        "IC_PASSWORD": "yourpassword"
      }
    }
  }
}
```

### Option B — from source

```bash
git clone https://github.com/chrischall/infinitecampus-mcp
cd infinitecampus-mcp
npm install && npm run build
```

## Authentication

Two paths — the MCP tries them in priority order:

1. **Username/password.** Set `IC_USERNAME` + `IC_PASSWORD` along with `IC_BASE_URL` + `IC_DISTRICT`.
2. **fetchproxy fallback.** Install the [fetchproxy 0.3.0 extension](https://github.com/chrischall/fetchproxy), sign into your IC portal in the browser, and leave `IC_USERNAME` / `IC_PASSWORD` unset. `IC_BASE_URL` + `IC_DISTRICT` are still required so the MCP knows which host to read cookies from.

`IC_BASE_URL` is your district's portal URL; `IC_DISTRICT` is the app-name path segment from that URL. Set `IC_DISABLE_FETCHPROXY=1` to opt out of the fallback (headless / CI).

## Tools (prefix `ic_`)

### Students & teachers
- `ic_list_students` — list students linked to your parent account
- `ic_list_teachers` — list teachers for a student

### Academics
- `ic_list_grades(studentId)` — class grades
- `ic_list_recent_grades(studentId)` — recently graded items
- `ic_list_assignments(studentId)` — current assignments
- `ic_list_assessments(studentId)` — test scores

### Attendance
- `ic_list_attendance(studentId)` — attendance summary
- `ic_list_attendance_events(studentId)` — individual absence/tardy events
- `ic_list_school_days(studentId)` — calendar days

### Behavior & fees
- `ic_list_behavior(studentId)` — behavior incidents
- `ic_list_fees(studentId)` — outstanding fees
- `ic_list_food_service(studentId)` — cafeteria balance

### Messaging
- `ic_list_messages` — inbox
- `ic_get_message(id)` — read a message
- `ic_list_documents(studentId)` / `ic_download_document(id)` — documents

## Notes

- Set `IC_NAME` if you want a friendly name other than the district appname.
- Auto-discovers the CUPS (Campus Unified Portal Services) layout from the base URL — no extra config needed for most districts.
