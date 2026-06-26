# iHRFlow HR Assistant

> AI-powered recruitment management: search talent, manage positions, schedule interviews, drive hiring pipelines.

## What is iHRFlow?

[iHRFlow](https://ihrflow.com) is an all-in-one talent management platform covering the full recruitment lifecycle — from creating job requirements, resume screening, interview scheduling, evaluation feedback, to offer management.

This OpenClaw Skill enables AI assistants to interact with iHRFlow via the MCP protocol, handling day-to-day HR tasks through natural language.

## Architecture

```
OpenClaw Agent
    ↓  exec {baseDir}/scripts/mcp-call.sh
Helper Script (curl + jq)
    ↓  JSON-RPC 2.0 over Streamable HTTP
iHRFlow MCP Server (ihrflow.com/mcp)
    ↓  SecurityMiddleware (API Key + Rate Limit)
    ↓  login tool → JWT per-user session
iHRFlow Backend API
```

The skill acts as an MCP Client. The agent calls a helper script that encapsulates all protocol details — JSON-RPC framing, SSE parsing, session management. No plugins required.

## Features

### 20 MCP Tools

| Category | Tools |
|----------|-------|
| **Auth** | `login` |
| **Candidates** | `search_candidates`, `get_resume_detail`, `add_resume_note`, `recommend_candidate_for_position` |
| **Positions** | `list_positions`, `get_position_detail`, `get_position_candidates`, `update_position_status`, `create_recruitment_need` |
| **Interviews** | `list_interviews`, `get_interview_detail`, `create_interview`, `cancel_interview`, `reschedule_interview` |
| **Pipeline** | `update_screening_status` |
| **Evaluation** | `submit_interview_feedback` |
| **Search** | `search_talent` (AI semantic search) |
| **Stats** | `get_recruitment_statistics`, `get_today_schedule` |

### 2 MCP Resources

- `ihrflow://recruitment/overview` — Recruitment stats summary
- `ihrflow://positions/active` — Active positions list

### HR Domain Intelligence

- Full screening funnel knowledge (HR screening → exam → dept → interview → final)
- 6 predefined workflow templates (daily briefing, talent sourcing, interview lifecycle, etc.)
- Chinese interaction, English enum values

## Directory Structure

```
ihrflow-skill/
  SKILL.md                   # Lean skill definition (~500 words)
  scripts/
    mcp-call.sh              # MCP Client wrapper (init, login, call, resource)
  references/
    api-reference.md         # Full tool parameter tables & response schemas
  README.md                  # This file
  clawhub.json               # ClawHub marketplace metadata
  CHANGELOG.md               # Version history
```

## Prerequisites

- iHRFlow backend deployed with MCP Server running
- `curl` and `jq` installed on the host
- OpenClaw installed (no plugins required)

## Setup

### 1. Install Skill

**From ClawHub:**
```bash
clawhub install ihrflow-hr
```

**Manual install:**
```bash
cp -r ihrflow-skill/ ~/.openclaw/workspace/skills/ihrflow-hr/
```

### 2. Configure Environment

Add to `~/.openclaw/openclaw.json`:

```json5
{
  skills: {
    entries: {
      "ihrflow-hr": {
        enabled: true,
        env: {
          IHRFLOW_MCP_URL: "https://ihrflow.com/mcp",
          IHRFLOW_USERNAME: "your-username",
          IHRFLOW_PASSWORD: "your-password",
          IHRFLOW_TENANT_ID: "your-tenant-id",
          IHRFLOW_API_KEY: "your-mcp-api-key"
        }
      }
    }
  }
}
```

Or use `~/.openclaw/.env`:

```bash
IHRFLOW_MCP_URL=https://ihrflow.com/mcp
IHRFLOW_USERNAME=hr_admin
IHRFLOW_PASSWORD=your-password
IHRFLOW_TENANT_ID=my-company
IHRFLOW_API_KEY=your-mcp-api-key
```

| Variable | Required | Description |
|----------|----------|-------------|
| `IHRFLOW_MCP_URL` | yes | MCP endpoint URL |
| `IHRFLOW_USERNAME` | yes | iHRFlow username |
| `IHRFLOW_PASSWORD` | yes | iHRFlow password |
| `IHRFLOW_TENANT_ID` | no | Tenant ID (multi-tenant deployments) |
| `IHRFLOW_API_KEY` | no | Transport-layer API key (optional for LAN) |

### 3. Verify

```bash
# Check MCP Server is running
curl -s https://ihrflow.com/healthz
# Expected: {"status":"ok"}
```

## Example Conversations

### Daily Briefing

```
User: Help me see today's schedule
AI:   [calls get_today_schedule + get_recruitment_statistics + resource ihrflow://positions/active]

📅 Today's Schedule (2026-03-12)
| Time  | Event      | Candidate | Position       |
|-------|------------|-----------|----------------|
| 10:00 | Tech Interview | Zhang San | Sr Java Dev |
| 14:00 | HR Interview   | Li Si     | Product Manager |

📊 Recruitment Overview
- Active positions: 12
- This week's interviews: 8
- Pending screening: 23 resumes
```

### Find Candidates

```
User: Find candidates for the "Senior Python Engineer" position
AI:   [calls get_position_detail → search_talent → get_resume_detail]

Found 5 matching candidates:
| Name    | Match | Exp | Key Skills          |
|---------|-------|-----|---------------------|
| Wang Wu | 92%   | 5yr | Python, Django, microservices |
| Zhao Liu| 87%   | 4yr | Python, FastAPI, K8s |
...

Shall I recommend them to this position?
```

### Advance Pipeline

```
User: Wang Wu passed HR screening, please advance
AI:   [calls update_screening_status(resume_id="xxx", action="hr_approve")]

✅ Wang Wu passed HR screening, now in department review stage.
Progress: HR ✅ → Dept 🔄 → Interview ⏳ → Final ⏳
```

## Troubleshooting

### "Auth failed" / 401 Error

The MCP Server requires an API key for transport security. Verify `IHRFLOW_API_KEY` is correctly configured. For LAN deployments where the MCP server has no API key set, this variable can be omitted.

### "Not logged in" / "Session expired"

The skill auto-initializes and logs in on first tool call. If you see session errors, tell the AI "re-login to iHRFlow" — it will re-run the init + login sequence.

### MCP Server Not Responding

1. Check server health: `curl https://ihrflow.com/healthz`
2. Check server logs: `docker logs ihrflow-mcp-server`
3. Verify the MCP_URL in your env config matches the actual server address

### No Search Results

- `search_candidates` and `search_talent` use semantic search — try different descriptions
- Verify the backend database contains resume data

## License

MIT
