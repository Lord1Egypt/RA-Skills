# Accountability Skill

Track and drive real work sessions on a Monday.com board. An AI agent reads all active items hourly, assesses state, picks tasks, executes work (or delegates), and writes updates — not just status pings.

## What It Does

Every hour (or at your configured frequency), the agent:
1. Reads all active items + sub-items from your Monday board
2. Assesses each item: state, blockers, what changed
3. Picks the most actionable item and breaks it into sub-tasks
4. Executes: writes code via Cursor Agent, makes config changes, sends messages
5. Writes updates back to Monday with results
6. Updates "Last Checked" on all items

## Installation

```bash
clawhub install accountability
```

## Configuration

Add to your `openclaw.json` config (or `.openclaw/.env`):

```json
{
  "skills": {
    "accountability": {
      "board_id": "YOUR_MONDAY_BOARD_ID",
      "api_token_env": "MONDAY_API_TOKEN",
      "owner_name": "Roy",
      "agent_name": "Nova",
      "columns": {
        "status": "color_mm0yr4nm",
        "check_frequency": "text_mm0y6b8r",
        "last_checked": "date_mm0y8p9j",
        "details": "long_text_mm0yce5e",
        "assigned_by": "color_mm10z99x"
      },
      "assigned_by_labels": {
        "owner": "Roy",
        "agent": "Nova"
      },
      "messaging_hours": {
        "start": "08:00",
        "end": "22:00",
        "timezone": "Asia/Jerusalem"
      }
    }
  }
}
```

### Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `MONDAY_API_TOKEN` | ✅ | Your Monday.com API v2 token |
| `MONDAY_BOARD_ID` | ✅ | Board ID to operate on (overrides config) |
| `MONDAY_COL_STATUS` | optional | Status column ID (default from config) |
| `MONDAY_COL_LAST_CHECKED` | optional | Last-checked column ID (default from config) |

### Getting Your Board ID

Open your board in Monday.com. The URL will look like:
`https://yourworkspace.monday.com/boards/1234567890`

The number at the end is your Board ID.

### Getting Your API Token

1. Go to `https://yourworkspace.monday.com/apps/manage/tokens`
2. Create a new token with `boards:read` and `boards:write` scopes

## Board Setup

The skill expects these columns on your Monday board:

| Column | Type | Purpose |
|--------|------|---------|
| Status | Status | Active / Done / Blocked / Working on it |
| Check Frequency | Text | How often to check: 1h, 2h, 4h, 8h, daily |
| Last Checked | Date | When the agent last reviewed this item |
| Details | Long Text | Goal, definition of done, context, blockers |
| Assigned By | Status | Who owns this: owner or agent |

### Auto-Setup (Coming Soon)

A future version will auto-create the board and columns if they don't exist. For now, create them manually and configure the column IDs in your config.

## Completion Rules

- **Owner-assigned tasks**: Only the owner can mark them Done. The agent writes "suggesting completion" updates but does NOT change status.
- **Agent-assigned tasks**: The agent can mark them Done independently.

## Cron Setup

The skill is designed to run on a schedule. Recommended: every 1 hour.

```json
{
  "cron": {
    "schedule": { "kind": "every", "everyMs": 3600000 },
    "payload": { "kind": "systemEvent", "text": "Hourly accountability work session. Read the accountability skill and follow the Hourly Work Session process exactly." }
  }
}
```

## Helper Script

The skill includes `scripts/monday-api.sh` for common operations:

```bash
# Set required env vars
export MONDAY_API_TOKEN="your_token"
export MONDAY_BOARD_ID="your_board_id"

# List all items
bash scripts/monday-api.sh list

# Add update to item
bash scripts/monday-api.sh update 1234567 "<p>Update text</p>"

# Set last checked to today
bash scripts/monday-api.sh checked 1234567

# Change status
bash scripts/monday-api.sh status 1234567 "Done"
```

## Design Principles

- **Real work, not status theater** — the agent should execute, not just report
- **Stuck = reassess** — if blocked, don't keep trying the same thing; step back and rethink
- **Delegate when blocked** — spawn sub-agents for code, message people who can unblock
- **Respect hours** — don't message people outside configured hours (unless urgent)
- **Owner controls completion** — agent never marks owner tasks as Done unilaterally
