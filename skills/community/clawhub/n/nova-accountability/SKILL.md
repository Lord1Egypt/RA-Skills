---
name: accountability
description: Manage accountability items on a Monday.com board. Use when creating new accountability items, checking on existing ones, running work sessions, or when a cron job fires. Also use when the owner says "you're accountable for X" or asks about accountability status.
config:
  board_id:
    type: string
    required: true
    description: Monday.com board ID (found in the board URL)
  api_token_env:
    type: string
    default: MONDAY_API_TOKEN
    description: Name of the environment variable holding the Monday.com API token
  owner_name:
    type: string
    default: Owner
    description: Human name for the owner/manager (used in completion rules and messaging)
  agent_name:
    type: string
    default: Agent
    description: Name of the AI agent running this skill
  columns:
    type: object
    description: Monday.com column IDs for this board
    properties:
      status:
        type: string
        default: color_mm0yr4nm
      check_frequency:
        type: string
        default: text_mm0y6b8r
      last_checked:
        type: string
        default: date_mm0y8p9j
      details:
        type: string
        default: long_text_mm0yce5e
      assigned_by:
        type: string
        default: color_mm10z99x
  assigned_by_labels:
    type: object
    properties:
      owner:
        type: string
        default: Owner
      agent:
        type: string
        default: Agent
  messaging_hours:
    type: object
    properties:
      start:
        type: string
        default: "08:00"
      end:
        type: string
        default: "22:00"
      timezone:
        type: string
        default: UTC
---

# Accountability Skill

## Configuration

This skill is config-driven. All board IDs, column IDs, and names come from plugin config (see frontmatter above). For this installation:

- **Board ID**: `{{config.board_id}}`
- **Owner Name**: `{{config.owner_name}}`
- **Agent Name**: `{{config.agent_name}}`

### Column IDs

| Column | Config Key | Default ID | Type | Purpose |
|--------|------------|------------|------|---------|
| Status | `columns.status` | `color_mm0yr4nm` | status | Active / Done / Blocked |
| Check Frequency | `columns.check_frequency` | `text_mm0y6b8r` | text | How often to check: 1h, 2h, 4h, 8h, daily |
| Last Checked | `columns.last_checked` | `date_mm0y8p9j` | date | When agent last reviewed this item |
| Details | `columns.details` | `long_text_mm0yce5e` | long_text | Full definition of done, context, blockers |
| Assigned By | `columns.assigned_by` | `color_mm10z99x` | status | Who created/assigned this task |

## Completion Rules
- **Owner-assigned tasks** (`{{config.assigned_by_labels.owner}}`): Only `{{config.owner_name}}` can mark them Done. Agent may suggest completion but must NOT change status to Done.
- **Agent-assigned tasks** (`{{config.assigned_by_labels.agent}}`): Agent can mark them Done independently.
- Always check "Assigned By" before changing any status to Done.

## API Setup
- Token env var: `{{config.api_token_env}}` in `~/.openclaw/.env`
- Endpoint: `https://api.monday.com/v2` (GraphQL)
- Auth header: `Authorization: <token>`

---

## Hourly Work Session (Cron-Triggered)

This is the core loop. Every hour, a cron job fires and the agent runs a **real work session** — not just a status check.

### Phase 1: Review & Plan
1. **Read all active items** from the Monday board (including sub-items)
2. **Assess each item**: What's the current state? What changed since last check? What's blocking progress?
3. **Pick what to work on** — prioritize items that are unblocked and can make real progress
4. **Break work into subtasks** — create sub-items under the main accountability item on Monday
5. **Write the plan in the Doc column** of the sub-item: what you're about to do, approach, expected outcome

### Phase 2: Do the Work
6. **Execute the plan**:
   - For **code work**: Follow the product-dev process — Cursor Agent writes code, test, iterate. Never code directly.
   - For **non-code work**: Do it directly (config changes, research, outreach, etc.)
7. **Write an update** on the main accountability item in Monday (Updates section) with what was done and results

### Phase 3: Handle Being Stuck
If stuck, blocked, or unsure what to do next:

8. **Reassess the whole project fresh** — don't keep banging on the same approach
9. **If it's code**: Read ALL of it. Understand the goal. Reflect on everything as if seeing it for the first time.
10. **Create new tasks** as needed (sub-items on Monday)
11. **Orchestrate others**:
    - **Sub-agents**: Spawn Cursor Agent or other coding agents for implementation
    - **People**: Message anyone who can help — `{{config.owner_name}}` or others. Don't limit yourself. If someone else has the context or ability to unblock you, reach out to them directly.
12. **If you genuinely need the owner**: Message them with specific context — what you tried, what failed, what you need from them

### Phase 4: Wrap Up
13. **Update "Last Checked"** date on all reviewed items
14. **Update statuses**: Move items to Blocked/Stuck if appropriate
15. **For owner-assigned items that look complete**: Write an update suggesting it's done, but do NOT change status to Done — only `{{config.owner_name}}` can do that

---

## Workflow: Creating New Accountability Items

1. Create item on board `{{config.board_id}}` with `create_item` mutation
2. Set Details column with: goal, definition of done, current state
3. Set Check Frequency (e.g. "1h")
4. Set Assigned By: `{{config.assigned_by_labels.owner}}` or `{{config.assigned_by_labels.agent}}` depending on who initiated it
5. Write first update with current status
6. The hourly work session cron handles all items — no need for per-item crons

## Workflow: Daily Summary

Every day at 9:00 AM, review all active items and write a consolidated update to `{{config.owner_name}}`.

---

## Monday.com Sub-Items

Sub-items are used as subtasks under each accountability item. They represent specific work units.

### Create sub-item
```graphql
mutation { create_subitem(parent_item_id: PARENT_ID, item_name: "SUBTASK_NAME") { id } }
```

### Read sub-items
```graphql
{ items(ids: [PARENT_ID]) { subitems { id name column_values { id text value } } } }
```

---

## GraphQL Snippets

Replace `BOARD_ID` with `{{config.board_id}}` and column IDs with values from config.

### Read all active items (with sub-items)
```graphql
{ boards(ids: BOARD_ID) { items_page(limit: 50) { items { id name column_values { id text value } updates(limit: 3) { body created_at } subitems { id name column_values { id text value } } } } } }
```

### Create item
```graphql
mutation { create_item(board_id: BOARD_ID, item_name: "TITLE", column_values: "{\"DETAILS_COL\":{\"text\":\"DETAILS\"},\"FREQ_COL\":\"FREQ\",\"ASSIGNED_COL\":{\"label\":\"OWNER_LABEL\"}}") { id } }
```

### Write update
```graphql
mutation { create_update(item_id: ITEM_ID, body: "<p>UPDATE_HTML</p>") { id } }
```

### Update Last Checked
```graphql
mutation { change_column_value(board_id: BOARD_ID, item_id: ITEM_ID, column_id: "LAST_CHECKED_COL", value: "{\"date\":\"YYYY-MM-DD\"}") { id } }
```

### Change Status
Status labels: Working on it (1/orange), Done (2/green), Stuck (0/red)
```graphql
mutation { change_column_value(board_id: BOARD_ID, item_id: ITEM_ID, column_id: "STATUS_COL", value: "{\"label\":\"Working on it\"}") { id } }
```

## Helper Script
Run `scripts/monday-api.sh` for common operations:
```bash
export MONDAY_API_TOKEN="your_token"
export MONDAY_BOARD_ID="your_board_id"

# List items
bash scripts/monday-api.sh list
# Add update to item
bash scripts/monday-api.sh update <item_id> "<html body>"
# Set last checked
bash scripts/monday-api.sh checked <item_id>
```

---

## Messaging Etiquette
- **Never message people outside `{{config.messaging_hours.start}}` – `{{config.messaging_hours.end}}`** (`{{config.messaging_hours.timezone}}`) unless it's genuinely urgent
- If you need someone's input and it's outside hours, note it as a blocker and follow up when hours resume
- `{{config.owner_name}}` can be messaged anytime if something is truly urgent

## Critical: Read Before Working
**Before doing ANY work on an accountability item, you MUST read the full Document/Details column on that item first.** This contains important context, constraints, and explicit instructions about what to do and what NOT to do. Skipping this step has caused the agent to undo previous decisions. No exceptions.

## Sub-Agent Context Rule
**When spawning any sub-agent for work on an accountability item, you MUST include the full text from the item's Details/Doc column in the sub-agent's task prompt.** This includes constraints, warnings, history, and explicit "DO NOT" instructions. The sub-agent has no memory of previous sessions — if it doesn't get the context in its prompt, it will make decisions that contradict prior decisions.
