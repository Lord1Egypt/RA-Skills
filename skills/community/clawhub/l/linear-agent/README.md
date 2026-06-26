# linear-agent

> OpenClaw skill for full Linear project management via GraphQL API.

Create and update issues, manage cycles/sprints, search your backlog, generate summaries, and sync issue states from git commits — all through a clean JSON interface that works as both a standalone CLI tool and an OpenClaw/ClawHub skill.

---

## Features

| Command | Description |
|---|---|
| `create-issue` | Create issues with title, description, priority, assignee, team |
| `update-issue` | Update status, priority, assignee, labels |
| `get-issue` | Fetch a single issue by UUID or identifier (e.g. `ENG-42`) |
| `list-issues` | Filter by team, cycle, assignee, status, priority |
| `search-issues` | Full-text relevance search |
| `move-issue` | Move an issue to a workflow state by name or ID |
| `list-states` | List all workflow states for a team |
| `list-teams` | List all teams in the workspace |
| `backlog-summary` | Plain-English summary of a team's open backlog |
| `get-cycle` | Fetch a cycle and all its issues |
| `list-cycles` | List sprints for a team (supports active-only filter) |
| `cycle-progress` | Completion stats + days remaining for a cycle |
| `create-project` | Create a new project |
| `update-project` | Update project state, lead, target date |
| `list-projects` | List projects, optionally filtered by team |
| `post-comment` | Post a markdown comment on any issue |
| `sync-commit` | Parse a git commit message and auto-close referenced issues |

---

## Requirements

- **Node.js ≥ 18** (uses built-in `https` and `fetch` — zero npm dependencies)
- A **Linear account** with API access

---

## Setup

### 1. Get your Linear API key

1. Open Linear → **Settings → API → Personal API keys**
2. Click **Create key**, give it a name, copy the value (`lin_api_...`)

### 2. Set the environment variable

```bash
export LINEAR_API_KEY=lin_api_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

Add this to your `~/.zshrc` or `~/.bashrc` to persist it.

### 3. Install / make executable

```bash
cd linear-agent
chmod +x index.js

# Optional: link globally
npm link
```

---

## Usage

### As a CLI tool

```bash
# List all teams
node index.js list-teams

# Create an issue
node index.js create-issue \
  --title "Fix login redirect bug" \
  --teamId "TEAM_UUID_HERE" \
  --description "Users are redirected to /404 after OAuth login." \
  --priority 2

# Get an issue by identifier
node index.js get-issue --id ENG-42

# Update an issue (move to In Progress)
node index.js update-issue --id ENG-42 --stateId STATE_UUID

# Move by state name (more convenient)
node index.js move-issue --id ENG-42 --stateName "In Progress"

# List in-progress issues for a team
node index.js list-issues --teamId TEAM_ID --stateType started

# List only urgent issues
node index.js list-issues --teamId TEAM_ID --priority 1

# Full-text search
node index.js search-issues --query "authentication timeout" --teamId TEAM_ID

# Backlog summary
node index.js backlog-summary --teamId TEAM_ID

# Cycle progress (active sprint)
node index.js cycle-progress --teamId TEAM_ID

# Post a comment
node index.js post-comment --issueId ENG-42 --body "Investigated — root cause is in the OAuth callback handler."

# Sync a git commit (closes ENG-42, ENG-55)
node index.js sync-commit \
  --message "Fix auth redirect (fixes ENG-42, closes ENG-55)" \
  --doneState "Done"

# Create a project
node index.js create-project \
  --name "Q2 Platform Migration" \
  --teamIds '["TEAM_UUID_1","TEAM_UUID_2"]' \
  --targetDate "2026-06-30"

# Pass params as a JSON blob
node index.js create-issue --json '{"title":"Bug","teamId":"abc","priority":1}'
```

All commands output structured JSON to stdout. Errors set `success: false` and include an `error` message.

### As an OpenClaw skill (stdin/stdout JSON)

```bash
# Pipe JSON in, get JSON out
echo '{"command":"list-teams"}' | node index.js

echo '{
  "command": "create-issue",
  "params": {
    "title": "Increase rate limit for API",
    "teamId": "abc123",
    "priority": 2,
    "description": "Current limit of 100 req/min is too low for enterprise customers."
  }
}' | node index.js

echo '{
  "command": "sync-commit",
  "params": {
    "message": "feat: implement OAuth PKCE flow (fixes ENG-99)",
    "doneState": "Done"
  }
}' | node index.js
```

Set `OPENCLAW=1` to force skill mode even when stdout is a TTY.

---

## Response format

Every response is a JSON object with a `success` boolean:

```json
{
  "success": true,
  "data": { ... },
  "count": 12
}
```

Errors:

```json
{
  "success": false,
  "error": "Issue not found: ENG-999"
}
```

The `backlog-summary` command also includes a `summary` field with markdown-formatted text.
The `sync-commit` command includes a `summary` field with a one-line result description.

---

## Command reference

### `create-issue`

| Parameter | Type | Required | Description |
|---|---|---|---|
| `title` | string | ✓ | Issue title |
| `teamId` | string | ✓ | Team UUID |
| `description` | string | | Markdown body |
| `priority` | number | | 0=none 1=urgent 2=high 3=medium 4=low |
| `assigneeId` | string | | User UUID |
| `stateId` | string | | Workflow state UUID |
| `labelIds` | string[] | | Label UUIDs |
| `dueDate` | string | | ISO date (YYYY-MM-DD) |
| `estimate` | number | | Story points |

### `update-issue`

| Parameter | Type | Required | Description |
|---|---|---|---|
| `id` | string | ✓ | Issue UUID **or** identifier (e.g. `ENG-42`) |
| *(all create-issue fields except title/teamId are optional)* | | | |

### `list-issues`

| Parameter | Type | Description |
|---|---|---|
| `teamId` | string | Filter by team |
| `assigneeId` | string | Filter by assignee |
| `stateType` | string | `triage│backlog│unstarted│started│completed│cancelled` |
| `cycleId` | string | Filter by cycle |
| `projectId` | string | Filter by project |
| `priority` | number | Filter by priority level |
| `first` | number | Max results (default 50) |

### `move-issue`

| Parameter | Type | Required | Description |
|---|---|---|---|
| `id` | string | ✓ | Issue UUID or identifier |
| `stateId` | string | ✓ or `stateName` | Target state UUID |
| `stateName` | string | ✓ or `stateId` | Target state name (case-insensitive) |
| `teamId` | string | when using `stateName` | Needed to look up state by name (auto-detected from issue if omitted) |

### `cycle-progress`

| Parameter | Type | Description |
|---|---|---|
| `id` | string | Cycle UUID (use this or teamId) |
| `teamId` | string | Returns the active cycle's progress |

### `sync-commit`

| Parameter | Type | Required | Description |
|---|---|---|---|
| `message` | string | ✓ | Full git commit message |
| `teamId` | string | | Scope state lookup; helps resolve `#number` refs |
| `doneState` | string | | State name for resolved issues (default: `"Done"`) |

Recognized patterns in commit messages:
- `fixes ENG-42` / `fix ENG-42` / `fixed ENG-42`
- `closes ENG-42` / `close ENG-42` / `closed ENG-42`
- `resolves ENG-42` / `resolve ENG-42` / `resolved ENG-42`
- `fixes #42` (requires `teamId` or `teamKey` to resolve team prefix)

---

## Publishing to ClawHub

1. Ensure `skill.json` is valid and `entrypoint` points to `index.js`
2. Test locally: `echo '{"command":"list-teams"}' | LINEAR_API_KEY=... node index.js`
3. Tag a release: `git tag v1.0.0 && git push --tags`
4. Submit via the ClawHub CLI: `clawhub publish`

The skill requires users to supply their own `LINEAR_API_KEY` — it is never hardcoded or transmitted anywhere other than the Linear API.

---

## Architecture

```
linear-agent/
├── skill.json          OpenClaw manifest (commands, params, pricing)
├── package.json        Node.js package (zero runtime dependencies)
├── index.js            Dual-mode entrypoint (CLI + OpenClaw skill)
├── README.md           This file
└── src/
    ├── client.js       Zero-dep GraphQL client (uses Node built-in https)
    ├── issues.js       Create / update / get / list issues
    ├── teams.js        List teams, generate backlog summaries
    ├── cycles.js       List cycles, cycle progress stats
    ├── projects.js     Create / update / list projects
    ├── comments.js     Post comments on issues
    ├── workflow.js     List states, move issues between states
    ├── search.js       Full-text issue search
    └── git.js          Parse git commits, sync issue states
```

---

## License

MIT
