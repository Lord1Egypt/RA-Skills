---
name: ourproject
description: Manage your ourproject.app workspace — projects, tasks, finance, CRM, and more — directly from your OpenClaw agent
---

# OurProject Skill for OpenClaw 🦞

Connect your [ourproject.app](https://ourproject.app) account to your OpenClaw agent. Query your projects, tasks, finances, bills, CRM clients, and notifications — all through natural conversation.

## Setup

### 1. Get your API Key

1. Login to [ourproject.app](https://ourproject.app)
2. Go to **Integrations → API Keys**
3. Click **"Generate API Key"**
4. Copy the key (starts with `op_`) — it's only shown once!

### 2. Configure the skill

Run the setup script:

```bash
node scripts/setup.js
```

It will ask for your API key and verify the connection.

To re-test anytime:

```bash
node scripts/test.js
```

### 3. Done!

You can now ask your OpenClaw agent things like:
- "What are my current projects?"
- "Any tasks due today?"
- "Show me upcoming bills"
- "Give me a daily summary"
- "How's my finance looking?"
- "Any unread notifications?"

## Available Commands

### Quick Commands

| Command | What it does |
|---------|-------------|
| `node scripts/summary.js` | Complete daily summary |
| `node scripts/projects.js` | List all projects |
| `node scripts/tasks.js` | List pending tasks |
| `node scripts/deadlines.js [days]` | Tasks with deadlines (default: 3 days) |
| `node scripts/bills.js [days]` | Upcoming bills (default: 7 days) |
| `node scripts/finance.js` | Finance overview |
| `node scripts/notifications.js` | Unread notifications count |
| `node scripts/test.js` | Test API connection |

### API Query (Advanced)

```bash
node scripts/api.js GET /projects
node scripts/api.js GET /tasks
node scripts/api.js GET /finance/dashboard
node scripts/api.js GET /crm/analytics/overview
node scripts/api.js POST /notes '{"title":"From OpenClaw","content":"Hello!"}'
```

## What Data Can You Access?

| Module | Endpoints | Scope Needed |
|--------|-----------|-------------|
| Projects | List, view details | `read` |
| Tasks | List, status, deadlines | `read` |
| Notes | List, create, update | `read`, `write` |
| Finance | Summary, accounts, transactions | `read` |
| Bills | List, upcoming, reminders | `read` |
| CRM | Dashboard, clients, reminders | `read` |
| Notifications | Count, list | `read` |
| Assets | Dashboard, items | `read` |

## Conversation Examples

When a user asks about their workspace, use the appropriate script:

- **"How are my projects going?"** → `node scripts/projects.js`
- **"Any bills due soon?"** → `node scripts/bills.js`
- **"What tasks are due today?"** → `node scripts/deadlines.js 1`
- **"Give me today's summary"** → `node scripts/summary.js`
- **"What's my current balance?"** → `node scripts/finance.js`
- **"Any notifications?"** → `node scripts/notifications.js`

## Troubleshooting

- **"Invalid API key"** → Re-run `node scripts/setup.js` with a new key
- **"Connection error"** → Make sure ourproject.app is accessible
- **"Scope error"** → Generate a new key with the required scopes

## Links

- Website: [ourproject.app](https://ourproject.app)
