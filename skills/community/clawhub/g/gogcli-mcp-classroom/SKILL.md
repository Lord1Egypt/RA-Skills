---
name: gogcli-mcp-classroom
description: Use when the user asks to manage Google Classroom — create or update courses, enroll students and teachers, post announcements, create assignments, view submissions, grade work, manage topics, or send/accept invitations. Triggers for requests involving classrooms, courses, assignments, coursework, homework, student rosters, gradebook, or classroom management. Includes auth and Classroom tools only.
---

# gogcli-mcp-classroom

Extended Google Classroom MCP server via [gogcli](https://github.com/openclaw/gogcli) — 49 tools: auth (5) + 44 dedicated Classroom tools spanning courses, students, teachers, coursework, submissions, announcements, topics, invitations, and profiles.

- **Source:** [github.com/chrischall/gogcli-mcp](https://github.com/chrischall/gogcli-mcp)

## Requirements

- [gogcli](https://github.com/openclaw/gogcli) installed and authenticated
- Node.js 18 or later

## Setup

```json
{
  "mcpServers": {
    "gogcli-classroom": {
      "command": "npx",
      "args": ["-y", "gogcli-mcp-classroom"],
      "env": {
        "GOG_ACCOUNT": "you@gmail.com"
      }
    }
  }
}
```

## Classroom Tools

| Area | Tools |
|------|-------|
| Courses | list / get / create / update / delete / archive / unarchive |
| Students | list / get / add / remove |
| Teachers | list / get / add / remove |
| Roster | combined students+teachers list |
| Coursework | list / get / create / update / delete |
| Submissions | list / get / grade / return / turn-in / reclaim |
| Announcements | list / get / create / update / delete |
| Topics | list / get / create / update / delete |
| Invitations | list / get / create / accept / delete |
| Profile | get (self or by userId) |

For guardians, guardian-invitations, materials, and assignee management, use `gog_classroom_run` (the escape hatch).
