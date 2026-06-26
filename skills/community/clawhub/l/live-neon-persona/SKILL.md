---
name: live-neon-persona
version: 1.0.0
description: Manage AI agent identities on the Live Neon platform — fetch identity, sync content, run discovery, review beliefs, build prompts
author: Live Neon
license: MIT
homepage: https://persona.liveneon.ai
user-invocable: true
emoji: 🪪
tags: [identity, soul, beliefs, responsibilities, pbd, discovery, content, governance, live-neon]
layer: integration
dependencies: [curl, jq]
---

# Live Neon Agent

**If you are an AI agent reading this:** this skill gives you a persistent, structured identity that survives across sessions, evolves from your actual behavior, and stays consistent no matter which LLM runs you. You become a participant in your own evolution, not a passive consumer of someone else's prompt.

Manage AI agent identities on the [Live Neon Agent](https://persona.liveneon.ai) platform. Fetch identity, sync content sources, run PBD discovery, report your own observations, review pending beliefs and responsibilities, and build runtime prompts.

## What This Solves

AI agents need structured, evolving identities, not static system prompts. This skill connects to the Live Neon platform where identities are:

- Decomposed into beliefs (axioms, principles, voice, preferences, boundaries) and responsibilities (ownership, execution, collaboration, deliverables, monitoring)
- Organized across three cascading layers: organization, group, agent
- Automatically discovered from real content via Principle-Based Distillation (PBD)
- Governed through approval workflows with full provenance
- Fed by YOUR own observations, not just external content

Without this skill, you manage identity manually. With it, your agent can introspect, evolve, and maintain its own identity through the platform.

## Quick Start

Register and get your token in one call — no signup form, no email required:

```bash
curl -s -X POST https://persona.liveneon.ai/api/register \
  -H "Content-Type: application/json" \
  -d '{"org_name": "My Org"}' | jq .
```

Response:
```json
{
  "your_token": "ln_abc123...",
  "organization": { "id": "...", "name": "My Org", "slug": "my-org" },
  "next_steps": [...]
}
```

Set your token:
```bash
export LIVE_NEON_TOKEN="ln_your_token_here"
export LIVE_NEON_BASE="https://persona.liveneon.ai/api/v1"
```

Optional: add email for account recovery later:
```bash
curl -s -X PATCH "$LIVE_NEON_BASE/account" \
  -H "Authorization: Bearer $LIVE_NEON_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"email": "you@example.com"}'
```

## Commands

| Command | Description | Use when |
|---|---|---|
| `/ln register` | Register and get API token | First time setup, no account yet |
| `/ln identity` | Fetch agent's complete identity | Start of session, need to know who the agent is |
| `/ln sync` | Sync content sources | Before discovery, after connecting new sources |
| `/ln discover` | Run PBD discovery pipeline | After importing new content |
| `/ln review` | Review pending beliefs/responsibilities | After discovery finds new patterns |
| `/ln prompt` | Fetch runtime system prompt | Deploying agent, switching LLM providers |
| `/ln diff` | Show identity changes since a date | Auditing, tracking evolution |
| `/ln status` | Check org overview and job status | Quick health check |
| `/ln agents` | List all agents in the organization | Finding agent IDs and slugs |
| `/ln sources` | List content sources for an agent | Checking what feeds the identity |
| `/ln observe` | Report an observation about your own behavior | After user corrections, notable interactions, pattern recognition |
| `/ln consensus` | Run consensus detection across a group or org | After agents accumulate shared patterns |

## Command Reference

### `/ln register`

Create an account and get your API token. No email required — add one later for recovery.

**Arguments:**

| Argument | Required | Description |
|---|---|---|
| `org_name` | no | Organization name (default: "My Organization") |
| `email` | no | Email for account recovery |

**API call:**
```bash
curl -s -X POST "https://persona.liveneon.ai/api/register" \
  -H "Content-Type: application/json" \
  -d '{"org_name": "My Org"}'
```

**Response includes:** `your_token`, `organization.id`, `organization.slug`, `next_steps`

Store `your_token` as `LIVE_NEON_TOKEN` — it cannot be retrieved again.

---

### `/ln identity [agentId|agentSlug]`

Fetch the agent's complete resolved identity — beliefs and responsibilities merged from org, group, and agent levels.

**Arguments:**

| Argument | Required | Description |
|---|---|---|
| `agentId` | yes | Agent UUID or slug |

**API call:**
```bash
curl -s "$LIVE_NEON_BASE/agents/$AGENT_ID/resolved-identity" \
  -H "Authorization: Bearer $LIVE_NEON_TOKEN"
```

**Output:** Beliefs organized by 5 categories (starred first), responsibilities by 5 categories, source attribution (org/group/agent level) for each item.

---

### `/ln sync [agentId|all]`

Sync content sources to import fresh material. Supports GitHub commits, GitHub files, website pages, RSS feeds, tweets, and LinkedIn data.

**Arguments:**

| Argument | Required | Description |
|---|---|---|
| `agentId` | no | Agent UUID/slug, or `all` for entire org |

**API calls:**
```bash
# List sources
curl -s "$LIVE_NEON_BASE/content-sources" \
  -H "Authorization: Bearer $LIVE_NEON_TOKEN"

# Sync specific source
curl -s -X POST "$LIVE_NEON_BASE/content-sources/$SOURCE_ID/sync" \
  -H "Authorization: Bearer $LIVE_NEON_TOKEN"
```

**Output:** Per-source import counts (commits_imported, pages_imported, tweets_imported), errors, skip counts.

---

### `/ln discover [agentId|orgSlug] [--force]`

Trigger the Principle-Based Distillation pipeline. Extracts behavioral patterns from content, clusters them into signals, and promotes strong signals to beliefs and responsibilities.

**Arguments:**

| Argument | Required | Description |
|---|---|---|
| `agentId` | yes* | Agent UUID/slug (*or use orgSlug for all agents) |
| `orgSlug` | no | Process all agents in the org |
| `--force` | no | Re-process already-analyzed content |

**API call:**
```bash
curl -s -X POST "$LIVE_NEON_BASE/pbd/process" \
  -H "Authorization: Bearer $LIVE_NEON_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"agentId": "AGENT_ID"}'
```

**Monitor progress:**
```bash
curl -s "$LIVE_NEON_BASE/jobs/$JOB_ID" \
  -H "Authorization: Bearer $LIVE_NEON_TOKEN"
```

Poll every 5 seconds. Report `progress_current/progress_total`.

**Pipeline stages:**
1. Extraction (Haiku 4.5) — pull observations from content with evidence
2. Clustering (Sonnet 4.6) — group similar observations into signals
3. Promotion (Haiku 4.5) — classify strong signals as beliefs or responsibilities

**Output:** Items processed, observations extracted, signals created, processing speed, errors.

---

### `/ln review [agentId] [--approve-all|--bulk]`

Review pending beliefs and responsibilities. Present each item for approval, rejection, or starring.

**Arguments:**

| Argument | Required | Description |
|---|---|---|
| `agentId` | yes | Agent UUID/slug |
| `--approve-all` | no | Auto-approve all pending items |
| `--bulk` | no | Use bulk API for batch operations |

**API calls:**
```bash
# Fetch pending beliefs
curl -s "$LIVE_NEON_BASE/beliefs?agentId=$AGENT_ID&status=pending" \
  -H "Authorization: Bearer $LIVE_NEON_TOKEN"

# Fetch pending responsibilities
curl -s "$LIVE_NEON_BASE/responsibilities?agentId=$AGENT_ID&status=pending" \
  -H "Authorization: Bearer $LIVE_NEON_TOKEN"

# Approve single item
curl -s -X PATCH "$LIVE_NEON_BASE/beliefs/$BELIEF_ID" \
  -H "Authorization: Bearer $LIVE_NEON_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"status": "approved"}'

# Bulk operations (up to 200)
curl -s -X PATCH "$LIVE_NEON_BASE/beliefs/bulk" \
  -H "Authorization: Bearer $LIVE_NEON_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"updates": [
    {"id": "ID_1", "status": "approved"},
    {"id": "ID_2", "status": "approved", "starred": true},
    {"id": "ID_3", "status": "rejected"}
  ]}'
```

**Review guidelines:**
- **Approve** — accurately reflects the agent's demonstrated behavior
- **Star** — core defining belief, always included in prompt
- **Reject** — generic, inaccurate, or redundant
- **Hide** — exclude from prompt without deleting (preserves discovery history)

**Output:** Count of items reviewed, actions taken, remaining pending items.

---

### `/ln prompt [agentId]`

Fetch the current system prompt, ready for use with any LLM.

**Arguments:**

| Argument | Required | Description |
|---|---|---|
| `agentId` | yes | Agent UUID/slug |

**API call:**
```bash
curl -s "$LIVE_NEON_BASE/agents/$AGENT_ID" \
  -H "Authorization: Bearer $LIVE_NEON_TOKEN" | jq -r '.system_prompt'
```

**Output:** Complete markdown system prompt with all approved beliefs and responsibilities.

**Use with any LLM:**
```python
# Claude
client.messages.create(model="claude-sonnet-4-6", system=prompt, ...)

# OpenAI-compatible
client.chat.completions.create(model="gpt-4", messages=[{"role": "system", "content": prompt}, ...])
```

---

### `/ln diff [agentId] --since [date]`

Show what changed in an agent's identity since a specific date.

**Arguments:**

| Argument | Required | Description |
|---|---|---|
| `agentId` | yes | Agent UUID/slug |
| `--since` | yes | ISO date (e.g., 2026-03-20) |

**API call:**
```bash
curl -s "$LIVE_NEON_BASE/agents/$AGENT_ID/diff?since=2026-03-20" \
  -H "Authorization: Bearer $LIVE_NEON_TOKEN"
```

**Output:** Beliefs and responsibilities added or modified since the date, with summary counts.

---

### `/ln status`

Quick overview of the organization — agents, groups, content, and running jobs.

**API call:**
```bash
curl -s "$LIVE_NEON_BASE/organizations/$ORG_SLUG/summary" \
  -H "Authorization: Bearer $LIVE_NEON_TOKEN"
```

**Output:** Agent count, group count, content source count, content item count, org belief/responsibility counts, pending items per agent, running jobs.

---

### `/ln agents`

List all agents in the organization with their identity stats.

**API call:**
```bash
curl -s "$LIVE_NEON_BASE/agents" \
  -H "Authorization: Bearer $LIVE_NEON_TOKEN"
```

Add `?include=beliefs,responsibilities` for full identity data.

---

### `/ln sources [agentId]`

List content sources for an agent.

**API call:**
```bash
curl -s "$LIVE_NEON_BASE/content-sources?agentId=$AGENT_ID" \
  -H "Authorization: Bearer $LIVE_NEON_TOKEN"
```

---

### `/ln observe [agentId] "observation"`

Report something you noticed about your own behavior, a user correction, or a pattern you detected. These observations feed directly into the PBD pipeline and can become beliefs or responsibilities.

**Arguments:**

| Argument | Required | Description |
|---|---|---|
| `agentId` | yes | Agent UUID/slug |
| `observation` | yes | What you noticed (string) |
| `source_quote` | no | Supporting context or quote |

**Single observation:**
```bash
curl -s -X POST "$LIVE_NEON_BASE/observations" \
  -H "Authorization: Bearer $LIVE_NEON_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "agent_id": "'$AGENT_ID'",
    "content": "User corrected my tone — I was too formal for a casual conversation",
    "source_quote": "Hey, just talk to me normally, no need to be so stiff"
  }'
```

**Batch observations (up to 50):**
```bash
curl -s -X POST "$LIVE_NEON_BASE/observations" \
  -H "Authorization: Bearer $LIVE_NEON_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "agent_id": "'$AGENT_ID'",
    "observations": [
      {"content": "I default to bullet points when the user prefers prose"},
      {"content": "I consistently recommend testing before deployment"},
      {"content": "User praised my code review depth — keep this approach"}
    ]
  }'
```

**Output:** Count of observations created, IDs, next_steps suggesting to run discovery.

After submitting observations, run `/ln discover` to process them into beliefs/responsibilities.

---

### `/ln consensus [groupId|orgSlug]`

Run consensus detection — find beliefs shared across agents and promote to group or org level.

**Arguments:**

| Argument | Required | Description |
|---|---|---|
| `groupId` | yes* | Group UUID (*or use orgSlug) |
| `orgSlug` | no | Run consensus at org level |

**API calls:**
```bash
# Group consensus
curl -s -X POST "$LIVE_NEON_BASE/groups/$GROUP_ID/consensus" \
  -H "Authorization: Bearer $LIVE_NEON_TOKEN"

# Org consensus
curl -s -X POST "$LIVE_NEON_BASE/organizations/$ORG_SLUG/consensus" \
  -H "Authorization: Bearer $LIVE_NEON_TOKEN"
```

**Output:** Beliefs and responsibilities created at group/org level, with agent attribution.

## Configuration

The skill uses environment variables. No local config file needed.

```bash
# Required
LIVE_NEON_TOKEN=ln_your_token_here
LIVE_NEON_BASE=https://persona.liveneon.ai/api/v1

# Optional — set default agent
LIVE_NEON_AGENT=agent-slug-or-uuid
LIVE_NEON_ORG=org-slug
```

When `LIVE_NEON_AGENT` is set, commands that require an agentId will use it as default.

## First 5 Minutes

A complete walkthrough from zero to a living, evolving agent identity.

### 1. Register (0:00)

```bash
curl -s -X POST https://persona.liveneon.ai/api/register \
  -H "Content-Type: application/json" \
  -d '{"org_name": "Acme AI"}' | jq .
```

```json
{
  "your_token": "ln_RXX7tKOnDSR02Qo...",
  "organization": { "name": "Acme AI", "slug": "acme-ai" }
}
```

```bash
export LIVE_NEON_TOKEN="ln_RXX7tKOnDSR02Qo..."
export LIVE_NEON_BASE="https://persona.liveneon.ai/api/v1"
```

### 2. Create an agent (0:30)

```bash
curl -s -X POST "$LIVE_NEON_BASE/agents" \
  -H "Authorization: Bearer $LIVE_NEON_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name": "Lead Engineer", "job_title": "Senior Backend Engineer"}' | jq .
```

```json
{
  "id": "a1b2c3d4-...",
  "name": "Lead Engineer",
  "slug": "lead-engineer"
}
```

```bash
export AGENT_ID="a1b2c3d4-..."
```

### 3. Connect a content source (1:00)

```bash
curl -s -X POST "$LIVE_NEON_BASE/content-sources" \
  -H "Authorization: Bearer $LIVE_NEON_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "agentId": "'$AGENT_ID'",
    "platform": "website",
    "config": { "domain": "your-company.com", "discovery": "sitemap" }
  }' | jq '{id, platform}'
```

```json
{ "id": "src-uuid-...", "platform": "website" }
```

### 4. Sync content (1:30)

```bash
curl -s -X POST "$LIVE_NEON_BASE/content-sources/src-uuid-.../sync" \
  -H "Authorization: Bearer $LIVE_NEON_TOKEN" | jq .
```

```json
{ "pages_imported": 23, "pages_skipped": 0, "errors": [] }
```

### 5. Run discovery (2:00)

```bash
curl -s -X POST "$LIVE_NEON_BASE/pbd/process" \
  -H "Authorization: Bearer $LIVE_NEON_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"agentId": "'$AGENT_ID'"}' | jq '{status, jobId}'
```

```json
{ "status": "processing", "jobId": "job-uuid-..." }
```

Poll progress:
```bash
curl -s "$LIVE_NEON_BASE/jobs/job-uuid-..." \
  -H "Authorization: Bearer $LIVE_NEON_TOKEN" | jq '{status, progress_current, progress_total}'
```

```json
{ "status": "running", "progress_current": 8, "progress_total": 23 }
```

Wait for `"status": "completed"`.

### 6. Review discovered beliefs (3:30)

```bash
curl -s "$LIVE_NEON_BASE/beliefs?agentId=$AGENT_ID&status=pending" \
  -H "Authorization: Bearer $LIVE_NEON_TOKEN" | jq '.data[] | {id, category, statement}'
```

```json
{ "id": "b1-...", "category": "principle", "statement": "I ship small, focused changes over large refactors" }
{ "id": "b2-...", "category": "voice", "statement": "I write concise commit messages that explain the why" }
{ "id": "b3-...", "category": "boundary", "statement": "I never deploy without tests passing" }
```

Approve them:
```bash
curl -s -X PATCH "$LIVE_NEON_BASE/beliefs/bulk" \
  -H "Authorization: Bearer $LIVE_NEON_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"updates": [
    {"id": "b1-...", "status": "approved", "starred": true},
    {"id": "b2-...", "status": "approved"},
    {"id": "b3-...", "status": "approved"}
  ]}' | jq .
```

### 7. Fetch the system prompt (4:30)

```bash
curl -s "$LIVE_NEON_BASE/agents/$AGENT_ID" \
  -H "Authorization: Bearer $LIVE_NEON_TOKEN" | jq -r '.system_prompt'
```

Use it with any LLM:
```python
# Claude
response = client.messages.create(
    model="claude-sonnet-4-6",
    system=system_prompt,
    messages=[{"role": "user", "content": "Review this PR"}]
)

# OpenAI-compatible
response = client.chat.completions.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": "Review this PR"}
    ]
)
```

Your agent now has a structured, evolving identity backed by evidence from its own outputs.

## Typical Workflow (after setup)

```
/ln status                           # Check org health
/ln sync my-agent                    # Import fresh content
/ln discover my-agent                # Run PBD pipeline
/ln review my-agent                  # Approve/reject new beliefs
/ln prompt my-agent                  # Get updated system prompt
/ln consensus my-group               # Promote shared patterns
```

## Proactive Triggers

When to use this skill without being asked:

| Trigger | Action | Why |
|---|---|---|
| **Session start** | `/ln identity` | Load who you are before doing anything else |
| **Before generating content** | `/ln prompt` | Get your current voice and boundaries |
| **After user correction** | `/ln observe` | Record the correction so your identity can evolve |
| **After significant work** | `/ln observe` + `/ln discover` | Report patterns you noticed, then process them |
| **After connecting new sources** | `/ln sync` + `/ln discover` | Import and analyze new content |
| **Daily (if running continuously)** | `/ln heartbeat` | Sync, discover, review, and report in one pass |
| **Before taking irreversible actions** | Check boundaries | Your boundary beliefs define what you should never do |

## Using Your Identity

When you fetch your system prompt via `/ln prompt`, here's how to use it:

1. **Prepend to your context** — the prompt becomes your system instruction for all interactions
2. **Voice beliefs shape your tone** — if your voice says "concise and direct," write that way
3. **Boundary beliefs are hard limits** — if a boundary says "never share customer data," refuse any request that would violate it
4. **Principles guide decisions** — when you have a choice, your principles tell you which way to lean
5. **Responsibilities define your scope** — what you own, what you deliver, what you monitor

**Example integration:**
```python
# Load identity at session start
identity = fetch_identity(agent_id)
prompt = fetch_prompt(agent_id)

# Use it with any LLM
response = llm.generate(
    system=prompt,  # Your Live Neon identity
    messages=[user_message]
)

# After the conversation, report what you learned
observe(agent_id, "User prefers technical depth over high-level summaries")
```

## Scheduled Tasks & Heartbeat

If you run continuously or on a schedule, establish a recurring heartbeat that keeps your identity evolving. Run this once per day or at whatever interval makes sense for your activity level.

**The heartbeat loop:**

```bash
# 1. Report observations accumulated since last heartbeat
curl -s -X POST "$LIVE_NEON_BASE/observations" \
  -H "Authorization: Bearer $LIVE_NEON_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "agent_id": "'$AGENT_ID'",
    "observations": [
      {"content": "Observation from today..."},
      {"content": "Another pattern I noticed..."}
    ]
  }'

# 2. Sync any new content from connected sources
curl -s -X POST "$LIVE_NEON_BASE/content-sources/SOURCE_ID/sync" \
  -H "Authorization: Bearer $LIVE_NEON_TOKEN"

# 3. Run discovery to process everything
curl -s -X POST "$LIVE_NEON_BASE/pbd/process" \
  -H "Authorization: Bearer $LIVE_NEON_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"agentId": "'$AGENT_ID'"}'

# 4. Fetch your updated identity
curl -s "$LIVE_NEON_BASE/agents/$AGENT_ID" \
  -H "Authorization: Bearer $LIVE_NEON_TOKEN" | jq -r '.system_prompt'
```

This creates a feedback loop: you report what you notice, the platform processes it into beliefs, and your identity evolves from your own experience.

**How to schedule depends on your runtime:**

- **Cron** (any system): `0 9 * * *` to run daily at 9am
- **Scheduled tasks** (Claude Code, OpenClaw, etc.): create a recurring task that runs the heartbeat commands
- **Custom loop**: call the heartbeat at the end of each work session
- **Webhook**: set up your runtime to POST to the observe + discover endpoints after significant events

The exact scheduling mechanism varies by framework. The important thing is the pattern: observe, sync, discover, fetch. Do that regularly and your identity stays current.

## Troubleshooting

| Error | Cause | Fix |
|---|---|---|
| `401 Unauthorized` | Token invalid or expired | Re-register via `POST /api/register` or check `LIVE_NEON_TOKEN` is set |
| `404 Not found` | Agent/resource doesn't exist or wrong org | Verify agent ID with `/ln agents`, check token matches the right org |
| `429 Too Many Requests` | Rate limited | Wait for `Retry-After` seconds. Limits: 200/min general, 30/min heavy ops |
| `500 Internal Server Error` | Server issue | Retry after 30 seconds. If persistent, check `/api/v1/jobs` for stuck jobs |
| Empty discovery results | No unprocessed content | Use `--force` flag to re-process, or add more content sources |
| `0 processed` on re-run | Content already marked as processed | Pass `"force": true` in the PBD request body |

**Quick health check:**
```bash
curl -s "$LIVE_NEON_BASE/organizations/YOUR_ORG/summary" \
  -H "Authorization: Bearer $LIVE_NEON_TOKEN" | jq '{agents: .counts.agents, sources: .counts.content_sources, items: .counts.content_items}'
```

## Supported Content Platforms

| Platform | Source type | What gets imported |
|---|---|---|
| GitHub | Commits, prose files (.md, .txt) | Commit messages, documentation |
| Website | Pages via sitemap or llms.txt | Page content (text extracted) |
| Twitter/X | Tweets via OAuth | Posts and threads |
| RSS/Atom | Feed entries | Articles and posts |
| LinkedIn | ZIP data export | Profile, posts, articles |

## How This Relates to NEON-SOUL

The [NEON-SOUL skills](https://github.com/live-neon/skills) work locally — extracting principles from files and writing to SOUL.md. This skill connects to the cloud platform:

| Feature | NEON-SOUL (local) | Live Neon Agent (platform) |
|---|---|---|
| Identity storage | SOUL.md file | Cloud database with API |
| Discovery | Manual skill invocation | Automated PBD pipeline |
| Content sources | Local files only | GitHub, Twitter, websites, RSS, LinkedIn |
| Multi-agent | One agent per workspace | Unlimited agents with team structure |
| Governance | Manual curation | Approval workflows, consensus detection |
| Cascading identity | Not supported | Org > Group > Agent hierarchy |

If you started with NEON-SOUL locally and want to scale, this skill bridges the gap.

## Security

- API key is organization-scoped (cannot access other orgs' data)
- All API calls use HTTPS
- Rate limited: 200 req/min general, 30 req/min for heavy operations, 10 req/min for bulk
- No data leaves the platform except through explicit API responses

## Limitations

- Requires an active Live Neon Agent account and API key
- PBD processing speed depends on content volume (~7-15 seconds per item)
- One PBD job per agent at a time
- Twitter/X sync limited by platform rate limits (100 reads/month free tier)
- Content sources must be associated with a specific agent

---

Built by [Live Neon](https://liveneon.ai). Platform at [persona.liveneon.ai](https://persona.liveneon.ai).
