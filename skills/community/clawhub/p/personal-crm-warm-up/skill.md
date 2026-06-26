---
name: Personal-CRM-Warm-Up
description: Identifies contacts you haven't reached out to recently and suggests low-pressure ways to reconnect.
commands:
  - name: warm_up_check
    description: Scans your contacts and returns people you should reach out to, sorted by urgency.
    arguments:
      - name: limit
        type: integer
        required: false
        description: How many suggestions to return. Default 3.
      - name: category
        type: string
        required: false
        description: Filter by contact category. One of "Inner Circle", "Professional", "Friend", "Casual".
    returns: A Markdown table with contact name, category, days since last interaction, a reconnection hook, and a drafted message.
---

## What It Does

This skill acts as a personal networking assistant. It reads a local `contacts.json` file, figures out which relationships have gone cold based on configurable time thresholds per category, and gives you a prioritized list of people to reach out to — complete with drafted reconnection messages so you don't have to stare at a blank screen.

Use it as a lightweight, local-first CRM with zero cloud dependencies and no data leaving your machine.

## How It Works

The scoring engine is simple but effective:

1. **Load** contacts from `contacts.json` (or a custom path passed to the handler).
2. **Score** each contact by calculating `days since last interaction − category threshold`. A positive value means the contact is overdue.
3. **Filter and sort** — only overdue contacts are returned, ranked from most overdue to least.
4. **Draft** a reconnection message for each overdue contact using their `lastTopic` as a conversation hook. Messages are deterministic (same contact always gets the same template) so the outreach feels consistent.

## Category Thresholds

Each contact category has a default threshold (in days) before it's considered overdue. These defaults are designed around typical relationship cadences:

| Category | Default | Rationale |
|---|---|---|
| Inner Circle | 30 days | Close relationships degrade fastest when neglected |
| Friend | 60 days | Monthly-ish is enough to stay current |
| Professional | 90 days | Quarterly touchpoints are standard for network maintenance |
| Casual | 120 days | Acquaintances need less frequent contact |

Override any threshold with environment variables:

```
CRM_INNER_CIRCLE_DAYS=30
CRM_PROFESSIONAL_DAYS=90
CRM_FRIEND_DAYS=60
CRM_CASUAL_DAYS=120
```

## Command Reference

### `warm_up_check`

Runs the full scoring pipeline and returns a Markdown report with a summary table and drafted messages.

**Arguments:**

| Argument | Type | Default | Description |
|---|---|---|---|
| `limit` | integer | 3 | Maximum number of overdue contacts to return |
| `category` | string | (all) | Restrict results to one category: `"Inner Circle"`, `"Professional"`, `"Friend"`, `"Casual"` |

**Output format:**

The command returns a Markdown document with two sections:

- A **summary table** with columns: Name, Category, Days Since Last Interaction, Overdue By (days past threshold), and Hook (truncated last topic for quick context).
- **Draft messages** — one per overdue contact, tailored to their preferred contact method (email, Slack, or text) and referencing the last topic discussed.

When no contacts are overdue, the command returns: `All caught up! No contacts are overdue for a warm-up.`

**Examples:**

```bash
# Default: top 3 most overdue contacts
node handler.js warm_up_check

# Get up to 5 suggestions
node handler.js warm_up_check --limit 5

# Focus on professional network only
node handler.js warm_up_check --category "Professional"

# Combine filters
node handler.js warm_up_check --limit 10 --category "Inner Circle"
```

## Contact Data Format

Each contact in `contacts.json` is an object with these fields:

```json
{
  "name": "Jane Doe",
  "category": "Inner Circle",
  "lastInteractionDate": "2026-03-15",
  "lastTopic": "Discussed her upcoming trip to Japan",
  "contactMethod": "text"
}
```

| Field | Type | Required | Description |
|---|---|---|---|
| `name` | string | Yes | Full name of the contact |
| `category` | string | Yes | One of `"Inner Circle"`, `"Professional"`, `"Friend"`, `"Casual"` |
| `lastInteractionDate` | string | Yes | ISO date (`YYYY-MM-DD`) of the last meaningful interaction |
| `lastTopic` | string | Yes | Short description of what you last discussed — used as the reconnection hook in drafted messages |
| `contactMethod` | string | Yes | Preferred outreach channel: `"email"`, `"slack"`, or `"text"` |

Contacts with an unrecognized category fall back to the `Casual` threshold.

## Design Decisions

- **Local-only, no network calls**: All data stays in `contacts.json` on disk. No API keys, no cloud sync, no telemetry.
- **Deterministic drafts**: The message template for a given contact is selected by a hash of their first name, so the same person always gets the same style of message. This avoids jarring inconsistency if you run the check multiple times.
- **Threshold-based, not ML**: The scoring is intentionally simple math (days elapsed minus threshold). This makes the behavior predictable and debuggable — you always know why someone appeared on the list.
