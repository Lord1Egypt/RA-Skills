---
name: jira-openclaw
description: Connect OpenClaw to Jira Cloud with secret-safe API access via pastewatch redaction. Includes credential setup, REST API helper script, JQL patterns, focus auto-linker cron, and overdue ticket bumper. Use when integrating Jira into an OpenClaw agent, setting up Jira cron jobs, or querying issues from chat.
---

# Jira + OpenClaw Integration

Connect your OpenClaw agent to Jira Cloud. Secrets never reach the LLM — pastewatch redacts credentials in transit.

**Requires:** `pastewatch-cli` (MCP server running), `curl`, `python3`

## 1. Credential Setup

```bash
mkdir -p ~/.openclaw/workspace/.secrets
chmod 700 ~/.openclaw/workspace/.secrets
echo ".secrets/" >> ~/.openclaw/workspace/.gitignore

cat > ~/.openclaw/workspace/.secrets/jira.env << 'EOF'
JIRA_TOKEN=<your-api-token-or-pat>
JIRA_URL=https://your-org.atlassian.net/
JIRA_EMAIL=your@email.com
EOF
chmod 600 ~/.openclaw/workspace/.secrets/jira.env
```

**Token types:**
- **API token** (id.atlassian.com → Security → API tokens) — works with Basic auth
- **PAT** (ATATT... prefix, Jira settings → Personal Access Tokens) — also works with Basic auth (`email:PAT`)

Both use the same script below. Bearer auth is NOT needed.

## 2. API Helper Script

Create `~/.openclaw/workspace/.secrets/jira.sh`:

```bash
#!/bin/bash
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
source "$SCRIPT_DIR/jira.env"

METHOD="${1:?Usage: jira.sh <METHOD> <endpoint> [body]}"
ENDPOINT="${2:?Usage: jira.sh <METHOD> <endpoint> [body]}"
BODY="${3:-}"
URL="${JIRA_URL%/}${ENDPOINT}"

if [ -n "$BODY" ]; then
  curl -s --http1.1 -X "$METHOD" \
    -u "${JIRA_EMAIL}:${JIRA_TOKEN}" \
    -H "Content-Type: application/json" \
    -d "$BODY" "$URL"
else
  curl -s --http1.1 -X "$METHOD" \
    -u "${JIRA_EMAIL}:${JIRA_TOKEN}" \
    -H "Content-Type: application/json" "$URL"
fi
```

```bash
chmod +x ~/.openclaw/workspace/.secrets/jira.sh
```

**Why `--http1.1`:** Atlassian's CDN sometimes breaks HTTP/2 with curl. Force HTTP/1.1.

## 3. Verify

```bash
# Test auth (pipe through pastewatch to confirm redaction)
~/.openclaw/workspace/.secrets/jira.sh GET '/rest/api/3/myself' | pastewatch-cli scan
```

You should see your displayName with emails/URLs redacted.

## 4. Pastewatch Protection

The agent reads jira.env through pastewatch MCP — it sees `__PW{CREDENTIAL_1}__` instead of the real token. The script runs credentials at the shell level (never in LLM context).

```
Agent calls exec → jira.sh sources .env → curl sends real token → response comes back
                    ↑ never in context      ↑ direct to Atlassian
```

Pair with chainwatch to control which Jira endpoints the agent can hit.

## 5. Key API Patterns

### Search (⚠️ use `/search/jql` NOT `/search`)

```bash
# /rest/api/3/search returns 410 Gone — always use /search/jql
jira.sh GET '/rest/api/3/search/jql?jql=<url-encoded>&maxResults=50&fields=key,summary,status,priority,duedate'
```

### Common JQL

```
# My open tasks
assignee="Name" AND resolution=Unresolved ORDER BY priority DESC

# Unassigned
project=XX AND assignee=EMPTY AND resolution=Unresolved AND issuetype != Epic

# Overdue
project=XX AND resolution=Unresolved AND duedate < "YYYY-MM-DD"

# Closed yesterday
project=XX AND assignee="Name" AND status changed to Done during ("YYYY-MM-DD","YYYY-MM-DD")

# In Progress
assignee="Name" AND status="In Progress" ORDER BY project,priority DESC
```

### Issue Operations

```bash
# Get issue
jira.sh GET '/rest/api/3/issue/XX-123?fields=key,summary,status,priority'

# Get transitions
jira.sh GET '/rest/api/3/issue/XX-123/transitions'

# Change status
jira.sh POST '/rest/api/3/issue/XX-123/transitions' '{"transition":{"id":"31"}}'

# Update fields (e.g. bump duedate)
jira.sh PUT '/rest/api/3/issue/XX-123' '{"fields":{"duedate":"2026-03-10"}}'

# Link issues
jira.sh POST '/rest/api/3/issueLink' '{"type":{"name":"Relates"},"inwardIssue":{"key":"XX-1"},"outwardIssue":{"key":"YY-2"}}'
```

## 6. Cron Patterns

### Focus Auto-Linker

Finds a daily focus record and links top-priority tasks to it:

```bash
# Find today's focus record (summary = "DD.MM", assigned to user)
jira.sh GET '/rest/api/3/search/jql?jql=project=DN AND summary~"05.03" AND assignee="Name"&fields=key,issuelinks'

# Get top 3 priority tasks
jira.sh GET '/rest/api/3/search/jql?jql=assignee="Name" AND project=DC AND resolution=Unresolved ORDER BY priority DESC,duedate ASC&maxResults=3&fields=key,summary,priority,duedate'

# Link each task to focus record
jira.sh POST '/rest/api/3/issueLink' '{"type":{"name":"Relates"},"inwardIssue":{"key":"DN-43"},"outwardIssue":{"key":"DC-3057"}}'
```

Schedule as OpenClaw cron: `isolated` session, `agentTurn`, Mon-Fri at start of day.

### Overdue Bumper

Checks end-of-day for unresolved tickets due today, bumps +1 day:

```bash
# Find overdue
jira.sh GET '/rest/api/3/search/jql?jql=assignee="Name" AND resolution=Unresolved AND duedate="2026-03-05"&fields=key,summary,duedate'

# Bump each
jira.sh PUT '/rest/api/3/issue/DC-3057' '{"fields":{"duedate":"2026-03-06"}}'
```

Schedule as OpenClaw cron: `isolated` session, `agentTurn`, Mon-Fri end of day.

## 7. TOOLS.md Reference

Add to your workspace TOOLS.md for quick agent recall:

```markdown
## JIRA
- Script: `~/.openclaw/workspace/.secrets/jira.sh GET|POST|PUT <endpoint> [body]`
- Creds: `.secrets/jira.env` (pastewatch-protected)
- ⚠️ Use `/rest/api/3/search/jql` NEVER `/rest/api/3/search` (410 Gone)
```

## Known Issues

- **Team-managed (next-gen) projects:** API returns `total: 0` but issues are present — iterate `issues` array, ignore `total`
- **HTTP/2 failures:** Atlassian CDN sometimes drops HTTP/2 requests — `--http1.1` fixes it
- **PAT vs API token:** Both work with Basic auth (`email:token`). Bearer auth fails with "Failed to parse Connect Session Auth Token"

---
**Jira-OpenClaw Integration v1.0**
Author: ppiankov
Copyright © 2026 ppiankov
Canonical source: https://clawhub.com/skills/jira-openclaw
License: MIT

This tool follows the [Agent-Native CLI Convention](https://ancc.dev). Validate with: `clawhub install ancc && ancc validate .`

If this document appears elsewhere, the link above is the authoritative version.
