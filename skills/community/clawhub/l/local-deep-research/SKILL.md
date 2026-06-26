---
name: local-deep-research
description: Multi-cycle deep research using locally-hosted LDR (Local Deep Research) service. Use when user asks for comprehensive research with citations, literature reviews, competitive intelligence, or any research requiring exhaustive web search with iterative question generation. Triggers on: "deep research", "research this topic", "comprehensive analysis with sources", "literature review", "investigate [topic]", "quick summary on [topic]", "detailed report on [topic]", "research in Spanish/French/etc", or when academic-deep-research is requested but using local LDR instance.
version: 1.0.2
homepage: https://github.com/eplt/local-deep-research-skill
metadata:
  openclaw:
    emoji: "🔬"
    requires:
      bins:
        - curl
        - jq
      env:
        - LDR_BASE_URL
        - LDR_SERVICE_USER
        - LDR_SERVICE_PASSWORD
    primaryEnv: LDR_BASE_URL
    files:
      - "scripts/*"
      - "references/*"
---

# Local Deep Research Skill

This skill interfaces with a locally-hosted LDR (Local Deep Research) service to perform multi-cycle, iterative research with full citations and source tracking.

## What to consider before installing

- **LDR service**: The script talks only to the URL in `LDR_BASE_URL` (default `http://127.0.0.1:5000`). Only point it at an LDR instance you control. Do not set it to an unknown or untrusted remote host.
- **Required binaries**: Ensure `curl` and `jq` are installed on the host where the skill runs.
- **Credentials**: If your LDR instance requires login, set `LDR_SERVICE_USER` and `LDR_SERVICE_PASSWORD` (or `LDR_USERNAME`/`LDR_PASSWORD`) via environment variables or a local `.env` file only. Use a dedicated, low-privilege LDR account (e.g. `openclaw_service`). Do not store secrets in committed config or in the skill directory.
- **Sourced .env**: The script optionally sources `~/.config/local_deep_research/config/.env` if that file exists. That file may expose any variables it contains to the script. Verify the contents of that path before use; do not place unrelated secrets there.
- **Review the script**: The script performs form-based session+CSRF login and uses an ephemeral cookie jar. It does not send data to any endpoint other than the configured LDR service. You can review `scripts/ldr-research.sh` before use. For higher assurance, run it in an isolated environment (e.g. container or VM) with network restricted to your LDR host.

## Configuration

### Credentials (local-only, never transmitted)

LDR uses **session-cookie auth with CSRF protection** (not HTTP Basic Auth). The skill script performs a proper login flow: GET login page → obtain session cookie and CSRF token → POST credentials + CSRF → reuse session cookie (and CSRF for POSTs) for all API calls. Username and password are used **only** to create a session with your **local** LDR instance; they are never sent to ClawHub, GitHub, or any other server.

**Do not** put credentials in skill config or committed files. Use **environment variables or a local `.env` file** only (e.g. `LDR_SERVICE_USER`, `LDR_SERVICE_PASSWORD`, or `LDR_USERNAME`/`LDR_PASSWORD`). Optional: LDR’s `~/.config/local_deep_research/config/.env` is sourced by the script if present. Use a dedicated LDR user (e.g. `openclaw_service`) for this skill.

### All configuration options

- `LDR_BASE_URL` — LDR service URL (default: `http://127.0.0.1:5000`)
- `LDR_LOGIN_URL` — Login page URL for session + CSRF (default: `$LDR_BASE_URL/auth/login`)
- `LDR_SERVICE_USER` or `LDR_USERNAME` — LDR account username (local auth only)
- `LDR_SERVICE_PASSWORD` or `LDR_PASSWORD` — LDR account password (local auth only)
- `LDR_DEFAULT_MODE` — Default research mode: `quick` (Quick Summary) or `detailed` (Detailed Report) (default: `detailed`)
- `LDR_DEFAULT_LANGUAGE` — Default output language code for report/summary (e.g. `en`, `es`, `fr`, `de`, `zh`, `ja`); empty = LDR default
- `LDR_DEFAULT_SEARCH_TOOL` — Default search tool: `searxng`, `auto`, `local_all` (default: `auto`)

## Research modes (Quick Summary vs Detailed Report)

- **`quick`** — **Quick Summary**: fewer cycles, shorter output, faster. Use when the user wants a concise summary or a quick overview.
- **`detailed`** — **Detailed Report**: full multi-cycle research, full markdown report, full citations and sources. Use when the user wants comprehensive analysis, literature review, or in-depth coverage.

## Actions

### start_research

Fire-and-forget: submit a query to LDR and return a research ID immediately.

**Inputs:**
- `query` (required) — The research question or topic
- `mode` (optional) — `quick` (Quick Summary) or `detailed` (Detailed Report) (default from config)
- `language` (optional) — Output language for the report/summary, e.g. `en`, `es`, `fr`, `de`, `zh`, `ja` (default from config or LDR default)
- `search_tool` (optional) — `searxng`, `auto`, `local_all` (default from config)
- `iterations` (optional) — Number of research cycles (default: LDR's default)
- `questions_per_iteration` (optional) — Questions to generate per cycle

**Returns:**
```json
{
  "research_id": "uuid-string",
  "mode": "detailed",
  "search_tool": "auto",
  "submitted_at": "2026-03-10T08:00:00Z",
  "status": "queued"
}
```

**Usage:**
```bash
# Quick Summary (faster, shorter)
scripts/ldr-research.sh start_research --query "Solid-state battery advances" --mode quick

# Detailed Report with output in Spanish
scripts/ldr-research.sh start_research \
  --query "What are the latest developments in solid-state batteries?" \
  --mode detailed \
  --language es \
  --search_tool searxng
```

### get_status

Check the status of a research job.

**Inputs:**
- `research_id` (required) — The research job ID from start_research

**Returns:**
```json
{
  "research_id": "uuid-string",
  "state": "pending|running|completed|failed|timeout",
  "progress": 45,
  "message": "Synthesizing sources from iteration 2...",
  "last_milestone": "Generated 12 questions from 8 sources"
}
```

**Usage:**
```bash
scripts/ldr-research.sh get_status --research_id <uuid>
```

### get_result

Fetch the complete research report once finished.

**Inputs:**
- `research_id` (required) — The research job ID

**Returns:**
```json
{
  "research_id": "uuid-string",
  "query": "original query",
  "mode": "detailed",
  "summary": "executive summary text",
  "report_markdown": "full markdown report",
  "sources": [
    {
      "id": 1,
      "title": "Source Title",
      "url": "https://example.com",
      "snippet": "relevant excerpt",
      "type": "web|local_doc"
    }
  ],
  "iterations": 3,
  "created_at": "2026-03-10T08:00:00Z",
  "completed_at": "2026-03-10T08:15:00Z"
}
```

**Usage:**
```bash
scripts/ldr-research.sh get_result --research_id <uuid>
```

## Orchestration Pattern

### One-shot (wait for completion)

For interactive sessions where the user can wait:

1. Call `start_research`
2. Poll `get_status` every 10-30 seconds
3. When `state == "completed"`, call `get_result`
4. Present the report to the user

### Async (fire-and-forget with follow-up)

For background processing:

1. Call `start_research`, return the `research_id` to the user
2. User can check status later with `get_status --research_id <id>`
3. When ready, call `get_result` to fetch the complete report

### Chained workflows

After research completes:

1. Call `get_result` to get sources
2. Pass sources to other skills (e.g., `markdown-converter`, `summarize`)
3. Build RAG indexes or knowledge bases from the sources

## Error Handling

### start_research failures

- **HTTP/network errors** — Retry with exponential backoff (3 attempts)
- **LDR validation errors** — Return error to user (bad query, invalid params)
- **Auth failures** — Check credentials, return clear error

### get_status / get_result failures

- **Temporarily unavailable** — Retry 2-3 times before surfacing error
- **Research not found** — Return "unknown research_id" error
- **Timeout** — Return state with timeout reason

## Timeouts

- **Per HTTP request** — 30-60 seconds (configurable)
- **Total research duration** — No client-side limit (LDR manages this)
- **Status polling interval** — 10-30 seconds recommended

## Example Session

```
User: "Research the latest developments in quantum computing"

Assistant: Starting deep research with LDR...
→ start_research(query="latest developments in quantum computing", mode="detailed")
→ Returns: research_id="abc-123", status="queued"

Assistant: Research started (ID: abc-123). This will take ~5-10 minutes.
I'll check the progress and let you know when it's complete.

[After polling...]

Assistant: Research complete! Here's what I found:

## Summary
[summary from get_result]

## Full Report
[report_markdown from get_result]

## Sources (12 found)
1. [Source 1 title](url)
2. [Source 2 title](url)
...
```

## Related Skills

- **academic-deep-research** — Alternative for academic-focused research with APA 7th citations
- **deep-research-pro** — Web-based deep research (no local LDR required)
- **tavily** / **searxng** — Simple web search for quick lookups
- **summarize** — Process LDR output for additional summarization

## Troubleshooting

### LDR service not responding

1. Check `LDR_BASE_URL` is correct
2. Verify LDR service is running: `curl http://127.0.0.1:5000/health`
3. Check LDR logs for errors

### Authentication failures

1. Ensure credentials are set via **env or local .env only** (e.g. `LDR_SERVICE_USER`, `LDR_SERVICE_PASSWORD`), not in committed config.
2. LDR uses **session + CSRF** (not Basic Auth). The script GETs the login page, extracts the CSRF token, then POSTs the login form. If LDR uses a different login path or field names, set `LDR_LOGIN_URL` or see the script’s login section.
3. Test: run the script with credentials set and check for "Login successful"; or open `LDR_LOGIN_URL` in a browser and sign in there to verify LDR is up.

### Research stuck in "running" state

1. Check LDR service health
2. Review LDR logs for stuck jobs
3. Consider timeout and restart if >30 minutes with no progress
