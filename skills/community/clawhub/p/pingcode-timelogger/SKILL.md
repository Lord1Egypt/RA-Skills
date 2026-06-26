---
name: pingcode-timelogger
description: Automate PingCode timesheet filling — create sub-tasks and log work hours. Use when asked to fill PingCode timesheets, log work hours, create work items, or auto-generate timesheets from Git commits. Triggers on "fill PingCode", "log hours", "PingCode timesheet", "fill timesheet", "工时填报", "填工时", "PingCode填报", "根据Git提交填工时".
---

# PingCode TimeLogger

Automate PingCode timesheet: create sub-tasks under a parent work item, set properties, and log work hours. Supports manual task lists and auto-generation from Git commits.

## Setup

Config lives at `~/.openclaw/skills/pingcode-timelogger/config.yaml`. Read it first on every invocation.

If config doesn't exist, guide the user through first-time setup:
1. Copy the template from `references/config-template.yaml` in this skill directory
2. User fills in their PingCode URL, cookie, project info, and optionally Git credentials
3. Validate by making a test API call to PingCode

### Config Structure

```yaml
pingcode:
  url: https://company.pingcode.com    # PingCode instance URL
  cookie_file: ./cookies.txt           # Path to cookie file (relative to config dir)
  project_id: ""                       # Project _id (24-char hex)
  default_parent_id: ""                # Default parent work item _id
  user_id: ""                          # Assignee user _id
  task_type_id: ""                     # "任务" type _id
  completed_state_id: ""               # "已完成" state _id

git:
  provider: github                     # github or gitlab
  url: https://api.github.com          # API base URL
  token_file: ./git-token.txt          # Path to token file (relative to config dir)
  username: ""                         # Git username
  repos: []                            # Repos to scan, e.g. ["owner/repo1"]

defaults:
  work_category: 研发                   # 研发/设计/部署/测试/文档/产品/调研/其他
  assignee_name: ""                    # Display name for confirmation messages
```

## Authentication

Two strategies, with automatic fallback:

### Strategy 1: API Direct (Primary)
Read cookie from `cookie_file` in config. Use `credentials: 'include'` or `Cookie` header for all API calls.

### Strategy 2: Browser Automation (Fallback)
If API calls fail (401/403), fall back to browser automation:
1. Open PingCode URL in browser
2. Check if user is logged in
3. If not, ask user to log in manually
4. Operate via browser UI

Always try API first. Only fall back to browser when API auth fails.

## Core Workflow

### Step 0: User Confirmation (Mandatory)

Before creating anything, **always** present the full plan to the user and wait for explicit confirmation:

1. Parse user input (task table or description)
2. Organize into the correct structure (see Task Structure below)
3. Output a clear summary: which story → which tasks → which sub-tasks → hours per item
4. **Wait for user to say OK** before executing
5. During execution, report progress in real-time (don't batch all updates to the end)

### Task Structure

Two modes depending on the project:

#### Mode A: Flat (e.g., SMA project)
Simple parent → child tasks. Each task is a direct sub-item under the parent story/task.

#### Mode B: Phased (e.g., RD-IT project)
Three-level structure aligned with delivery phases:

```
Story (需求)
├── 前端开发 (task)         ← phase node, sub-tasks underneath
│   ├── sub-task: feature A
│   └── sub-task: feature B
├── 后端开发 (task)         ← phase node, sub-tasks underneath
│   └── sub-task: API work
├── 自测 (task)             ← phase node, usually no children
├── 联调 (task)             ← phase node
├── 研发自扫 (task)         ← phase node
├── 产品文档 (task)         ← phase node
├── PRD文档 (task)          ← phase node
├── 测试 (task)             ← phase node, may have children (test cases, test report)
├── 上线准备 (task)         ← phase node, may have children (manual, release plan)
└── 上线文档梳理 (task)     ← phase node
```

**Rules for Mode B**:
- All phase nodes are **sibling tasks** under the story (not nested)
- **Only 前端开发 and 后端开发** have sub-tasks for specific dev work
- Other phases (自测, 联调, 文档, etc.) are usually single tasks
- 测试 and 上线准备 **may** have sub-tasks if there are multiple deliverables
- **Work hours go on the lowest level**: sub-tasks if they exist, otherwise directly on the phase task
- Estimated hours (`estimated_workload`) = registered hours (same value)
- If a phase task already exists under the story, reuse it; don't create duplicates

**Determining the mode**: Check the project identifier prefix (SMA → Mode A, RD-IT → Mode B). If unclear, ask the user.

### Locate Target Parent

User provides one of:
- **PingCode URL**: Extract work item ID from URL path, e.g. `https://company.pingcode.com/pjm/projects/SMA/work-items/SMA-348` → look up `SMA-348`
- **Work item identifier**: e.g. `SMA-348` → `GET /api/agile/work-items/SMA-348` to get `_id`
- **Nothing specified**: Use `default_parent_id` from config

For **Mode B**, also check existing children of the story:
```
GET {pingcode_url}/api/agile/work-items/{story_id}/children
```
Reuse existing phase tasks (e.g., if "后端开发" already exists, create sub-tasks under it).

### Create Sub-Tasks

For each task in the list:

```
POST {pingcode_url}/api/agile/work-item
Cookie: <from cookie_file>

{
  "property_values": [
    {"key": "title", "value": "<task title>"},
    {"key": "type", "value": "<task_type_id from config>"},
    {"key": "project_id", "value": "<project_id from config>"},
    {"key": "assignee", "value": "<user_id from config>"},
    {"key": "parent_id", "value": "<parent _id>"},
    {"key": "due", "value": null},
    {"key": "phase", "value": null}
  ]
}
```

Note: Endpoint is `/api/agile/work-item` (singular), NOT `/api/agile/work-items`.

### Set Date and Status

```
PUT {pingcode_url}/api/agile/work-items/{_id}/property
Cookie: <from cookie_file>

# Set start date:
{"key": "start", "value": {"date": <unix_timestamp>}}

# Set end date:
{"key": "due", "value": {"date": <unix_timestamp>}}
```

Batch set status to completed:
```
POST {pingcode_url}/api/agile/work-items/state
Cookie: <from cookie_file>

{
  "state_id": "<completed_state_id from config>",
  "work_item_ids": ["id1", "id2", ...],
  "bypass": 0
}
```

### Set Estimated Workload

```
PUT {pingcode_url}/api/agile/work-items/{_id}/property
Cookie: <from cookie_file>

{"key": "estimated_workload", "value": <hours_as_number>}
```

**⚠️ The value is in HOURS (not seconds). Do NOT multiply by 3600.**

Set estimated workload = registered hours (same value) on every task/sub-task that has hours logged.

### Log Work Hours

```
POST {pingcode_url}/api/ladon/workload/register
Cookie: <from cookie_file>

{
  "principal_type": "work_item",
  "principal_id": "<task_id>",
  "man_hour": <hours>,
  "remaining_workload": 0,
  "register_date": <cst_midnight_unix_ts>,
  "work_category_id": "<category_id>",
  "work_content": "<task description>",
  "pilot_id": "<project_id>"
}
```

**⚠️ `pilot_id` is required — set it to the project's `_id` (same as `project_id`).**

**work_category_id mapping** — read `references/category-ids.md` for the full list. Common: 研发=`5cb7e7fffda1ce4ca0050002`.

**register_date**: Must be CST (UTC+8) midnight timestamp. Formula: `new Date('YYYY-MM-DDT00:00:00+08:00').getTime() / 1000`

**Distribute hours across weekdays** (Mon–Fri). Never pile all hours on one day.

## Git Commit Auto-Fill

When user says "根据Git提交填工时" or similar:

1. Read Git config from `config.yaml` (provider, token, repos)
2. Ask user for: target date range, total work hours for the period
3. Fetch commits via Git API — see `references/git-integration.md`
4. Group commits by day and summarize into task titles
5. Distribute hours proportionally across days based on commit count
6. Confirm task list with user before creating
7. Execute standard workflow (create tasks → set properties → log hours)

## Important Rules

- **Always confirm** the full task list with user before creating anything
- **Report progress in real-time** — don't wait until the end to send all updates
- **API endpoint is singular**: `/api/agile/work-item` for creation
- **Never use Bearer token** — PingCode auth requires Cookie
- **Status flow**: Only use "已完成", never "关闭". Must go: 打开→进行中→已完成 (two steps)
- **Type matters**: Tasks (type=4) can have hours logged directly. User Stories (type=3) cannot — must create task sub-items under them
- **estimated_workload unit is HOURS** — do NOT multiply by 3600
- **pilot_id is required** for workload register — use the project_id
- **Read-only for production data**: Never delete or modify existing work items without explicit user confirmation

## Error Handling

| Error | Action |
|-------|--------|
| 401/403 on API | Switch to browser fallback |
| Cookie expired | Ask user to re-export cookie or log in via browser |
| Parent is Epic (type=2) | Cannot create task directly under Epic; find or create a User Story first |
| work_category_id missing | Required field since 2026-04; always include it |
| pilot_id not found | Add `pilot_id: <project_id>` to workload register request |
| estimated_workload too large | Unit is hours, not seconds; do NOT multiply by 3600 |

## First-Time Setup Guide

If config file doesn't exist, walk user through setup:

1. Create config directory: `mkdir -p ~/.openclaw/skills/pingcode-timelogger`
2. Copy template: read `references/config-template.yaml` and save to config dir
3. User fills in PingCode URL
4. Guide user to export cookies (browser DevTools → Application → Cookies → copy all for the PingCode domain, or use a cookie export extension)
5. Help user find project_id, task_type_id, state_ids by browsing PingCode API or UI
6. Optionally configure Git integration
7. Test with a dry-run (show what would be created without actually creating)
