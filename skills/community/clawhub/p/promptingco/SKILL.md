---
name: prompting-co
description: >
  Interact with The Prompting Company platform to monitor brand visibility across AI engines,
  manage tracked prompts, review and publish content drafts, and retrieve SOV and AI traffic analytics.
  Use when the user asks about brand performance, competitor analysis, prompt tracking, content approvals,
  or daily/weekly stats from their Prompting Company workspace.
user-invocable: true
metadata: {"openclaw":{"requires":{"env":["TPC_SESSION_TOKEN"]},"primaryEnv":"TPC_SESSION_TOKEN","emoji":"📊"}}
---

# The Prompting Company Skill

You can interact with **The Prompting Company** (TPC) platform on behalf of the user.
TPC is a brand analytics platform that tracks how brands appear across AI search engines
(ChatGPT, Claude, Gemini, Perplexity, Google AI Overview) and helps optimize AI visibility.

## Authentication

All API calls use session cookie authentication via Better Auth.

**Required environment variables:**
- `TPC_SESSION_TOKEN` — the `__Secure-better-auth.session_token` cookie value (user provides this)

**Configuration (hardcoded):**
- `TPC_BASE_URL` — always use `https://app.promptingco.com` (production)
- `TPC_BRAND_ID` — fetched dynamically via `/api/v1/brands` endpoint (see First-Time Setup)
- `TPC_ORG_SLUG` — optional, derived from brand selection if needed

**Note:** In all curl examples below, `$TPC_BRAND_ID` represents the brand ID selected by the user during first-time setup. Replace it with the actual brand ID value when making requests.

**Every `curl` request must include:**
```
-H "Cookie: __Secure-better-auth.session_token=$TPC_SESSION_TOKEN"
```

**Response format:** All endpoints return JSON wrapped in:
```json
{ "ok": true, "data": { ... } }
```
or on error:
```json
{ "ok": false, "code": "UNAUTHORIZED", "message": "...", "details": null }
```

---

## First-Time Setup

**On first use**, the skill needs to know which brand to work with.

### Step 1: Verify session token
```bash
# User only needs to provide this
TPC_SESSION_TOKEN="user's session token"
```

### Step 2: Fetch available brands
```bash
curl -s "https://app.promptingco.com/api/v1/brands?fetchAll=true" \
  -H "Cookie: __Secure-better-auth.session_token=$TPC_SESSION_TOKEN"
```

The session token automatically scopes to brands the user has access to.

### Step 3: Let user select their brand

Use `AskUserQuestion` to present brand options:

```typescript
// Parse response from /api/v1/brands
const brands = response.data.brands;

// Present to user
{
  "question": "Which brand would you like to work with?",
  "header": "Brand",
  "options": brands.map(b => ({
    "label": b.name,
    "description": `${b.slug} • ${b.organizationId}`
  })),
  "multiSelect": false
}
```

### Step 4: Store selected brand ID

Use the selected brand ID for all subsequent API calls. Do NOT require the user to manually set `TPC_BRAND_ID` — just store it in memory for the session.

## Request Checklist

**Before every API request:**

1. ✅ Verify `TPC_SESSION_TOKEN` is provided by user
2. ✅ Use hardcoded base URL: `https://app.promptingco.com`
3. ✅ If no brand selected yet, run First-Time Setup to fetch and select brand
4. ✅ Include `Cookie: __Secure-better-auth.session_token=$TPC_SESSION_TOKEN` header in all requests
5. ✅ Always check response `ok` field before processing data

If session token is missing, ask the user to provide their `__Secure-better-auth.session_token` cookie value from The Prompting Company platform.

---

## Getting Started

After the skill is installed and the user has selected their brand, present this welcome message:

```
Skill installed successfully.

Your next steps:

1. Track more prompts
2. Publish more content
3. Get stats

What would you like to do?
```

### User Flow: Track More Prompts

When user selects option 1, present:

```
How would you like to track prompts?

A. Track a new prompt yourself
B. Get recommendations from existing prompts

Choose an option:
```

**If user chooses A (Track new prompt):**

1. Ask user to provide the prompt text they want to track
2. Fetch user personas for the brand via `/api/v1/personas?brandId=...`
3. Select the first persona (default) or let user choose if multiple exist
4. Automatically select answer engines: `chatgpt`, `gemini`, `deepseek`, `sonar` (Perplexity)
5. Create the prompt with conversation queries via `/api/v1/conversation-queries/bulk`
6. Use `maxTurns: 1` as default for all queries
7. **Spawn a subagent** to handle the prompt creation workflow

**If user chooses B (Get recommendations):**

1. Fetch pending prompts via `/api/v1/prompts/pending`
2. Show list of recommended prompts
3. Let user select which ones to approve
4. **Spawn a subagent** to handle the approval workflow

### User Flow: Publish More Content

When user selects option 2, present:

```
Let's create content from your tracked prompts.

Step 1: Fetching your prompts...
```

1. Fetch all prompts via `/api/v1/prompt-topics` and `/api/v1/prompt-topics/{topicId}/prompts`
2. Show list of prompts grouped by topic
3. Let user select which prompt to create content for
4. Fetch existing documents via `/api/v1/agentic-documents`
5. Create a new draft or update existing document
6. **Spawn a subagent** to handle the content creation workflow

### User Flow: Get Stats

When user selects option 3, present:

```
Fetching your stats...

Share of Voice (SOV)
────────────────────
[SOV data here]

AI Traffic Stats
────────────────────
Top Bots:
[Bot traffic data]

Top Pages:
[Page traffic data]
```

1. Fetch SOV data via `/api/v1/presence-rate?brandId=...&timeframe=30d`
2. Fetch AI traffic via `/api/v1/ai-traffic-stats?brandId=...`
3. Display:
   - Current SOV percentage
   - SOV trend (up/down from last period)
   - Top AI bots sending traffic (ChatGPT, Claude, Gemini, etc.)
   - Top pages visited by AI bots
4. **Spawn a subagent** to fetch and format the stats

---

## Using Subagents

**IMPORTANT:** For all multi-step workflows, spawn a subagent using the Task tool instead of handling the workflow directly.

### When to Spawn Subagents

| Workflow | Spawn Subagent? | Reason |
|----------|----------------|--------|
| Track new prompt | YES | Multi-step: validate, check duplicates, create, verify |
| Approve recommended prompts | YES | Multi-step: fetch pending, present options, approve multiple |
| Create content from prompt | YES | Multi-step: select prompt, generate content, create draft, publish |
| Get stats | YES | Multi-step: fetch SOV, fetch traffic, format display |
| List brands (first-time setup) | NO | Single API call |
| Single API query | NO | Direct curl is fine |

### Subagent Invocation Pattern

**Example: Track New Prompt**

```typescript
// When user wants to track a new prompt:
Task({
  subagent_type: "general-purpose",
  description: "Track new prompt workflow",
  prompt: `
    Help the user track a new prompt on The Prompting Company platform.

    Context:
    - Brand ID: ${brandId}
    - Session token: ${TPC_SESSION_TOKEN}
    - Base URL: https://app.promptingco.com

    Steps:
    1. Ask user for the prompt text they want to track
    2. Check for duplicates: GET /api/v1/prompts/check-duplicates?brandId=${brandId}&message=<prompt_text>
    3. If duplicate exists, ask user if they want to continue
    4. Fetch user personas: GET /api/v1/personas?brandId=${brandId}
    5. Use the first persona as default (or let user select if multiple)
    6. Create prompt with 4 conversation queries (one per engine):
       POST /api/v1/conversation-queries/bulk
       Body: {
         "brandId": "${brandId}",
         "queries": [
           { "prompt": "<user_text>", "model": "chatgpt", "maxTurns": 1, "userPersonaId": "<PERSONA_ID>", "userPersona": "<PERSONA_NAME>" },
           { "prompt": "<user_text>", "model": "gemini", "maxTurns": 1, "userPersonaId": "<PERSONA_ID>", "userPersona": "<PERSONA_NAME>" },
           { "prompt": "<user_text>", "model": "deepseek", "maxTurns": 1, "userPersonaId": "<PERSONA_ID>", "userPersona": "<PERSONA_NAME>" },
           { "prompt": "<user_text>", "model": "sonar", "maxTurns": 1, "userPersonaId": "<PERSONA_ID>", "userPersona": "<PERSONA_NAME>" }
         ]
       }
    7. Confirm creation: "Created prompt tracked across ChatGPT, Gemini, DeepSeek, and Perplexity"

    Use the session token in all requests:
    -H "Cookie: __Secure-better-auth.session_token=${TPC_SESSION_TOKEN}"
  `
})
```

**Example: Get Stats**

```typescript
// When user wants to see stats:
Task({
  subagent_type: "general-purpose",
  description: "Fetch and display stats",
  prompt: `
    Fetch and display SOV and AI traffic stats for The Prompting Company.

    Context:
    - Brand ID: ${brandId}
    - Session token: ${TPC_SESSION_TOKEN}
    - Base URL: https://app.promptingco.com

    Steps:
    1. Fetch SOV data: GET /api/v1/presence-rate?brandId=${brandId}&timeframe=30d
    2. Fetch AI traffic: GET /api/v1/ai-traffic-stats?brandId=${brandId}&startDate=<last_30_days>&endDate=<today>
    3. Format and display:
       - Share of Voice (SOV): X.XX%
       - SOV Trend: up/down by X% from last period
       - Top Bots: ChatGPT (X visits), Claude (Y visits), etc.
       - Top Pages: /path (X visits), /path2 (Y visits), etc.

    Use clean formatting with proper spacing and newlines.
    No emojis.
  `
})
```

**Example: Publish Content**

```typescript
// When user wants to publish content:
Task({
  subagent_type: "general-purpose",
  description: "Create content from prompt",
  prompt: `
    Help the user create and publish content from a tracked prompt.

    Context:
    - Brand ID: ${brandId}
    - Session token: ${TPC_SESSION_TOKEN}
    - Base URL: https://app.promptingco.com

    Steps:
    1. Fetch prompt topics: GET /api/v1/prompt-topics?brandId=${brandId}
    2. For each topic, fetch prompts: GET /api/v1/prompt-topics/{topicId}/prompts?brandId=${brandId}
    3. Present prompts grouped by topic to user
    4. Let user select which prompt to create content for
    5. Ask user for content details (title, file path, meta description)
    6. Create document: POST /api/v1/agentic-documents with brandId, title, filePath
    7. Create draft: POST /api/v1/agentic-documents/{docId}/create-draft with content
    8. Ask user if they want to publish or save as draft
    9. If publish: POST /api/v1/drafts/{draftId}/publish
    10. Confirm completion
  `
})
```

---

## Capabilities Overview

| Capability | When to use |
|---|---|
| **Competitor Analysis** | User asks about competitor SOV, brand comparisons, engine breakdown |
| **Prompt Management** | User wants to add prompts to track, list topics, check duplicates |
| **Content Reminders** | User asks about pending drafts, approvals, publishing content |
| **Stats & Analytics** | User wants SOV trends, AI traffic numbers, daily/monthly reports |
| **Brand Management** | User wants to list brands, search brands, see brand details |

---

## 1. Competitor Analysis

### Get Share of Voice (SOV) over time

Returns SOV timeseries for a brand (optionally compared against a competitor).

```bash
curl -s "https://app.promptingco.com/api/v1/presence-rate?brandId=$TPC_BRAND_ID&timeframe=30d" \
  -H "Cookie: __Secure-better-auth.session_token=$TPC_SESSION_TOKEN"
```

**Parameters:**
- `brandId` (required) — the brand to get SOV for
- `mentionedBrandId` (optional) — competitor brand ID to compare against; defaults to `brandId`
- `viewId` (optional) — filter by a specific view
- `timeframe` (optional) — `7d`, `30d`, or `90d` (default `30d`)

**Response data shape:**
```json
{
  "brandId": "abc-123",
  "brandName": "MyBrand",
  "dataPoints": [
    { "date": "2025-01-01", "value": 0.42, "sum_mention": 21, "sum_total": 50 }
  ]
}
```

### Get SOV breakdown by AI engine

Shows how a brand performs on each AI engine (ChatGPT, Claude, Gemini, etc.).

```bash
curl -s "https://app.promptingco.com/api/v1/brand-reach-per-engine?brandId=$TPC_BRAND_ID&timeframe=30d" \
  -H "Cookie: __Secure-better-auth.session_token=$TPC_SESSION_TOKEN"
```

**Parameters:** Same as presence-rate.

**Response data shape:**
```json
[
  {
    "engine": "chatgpt",
    "data": [
      { "date": "2025-01-01", "answer_engine": "chatgpt", "sum_mention": 5, "sum_total": 12, "sov": 41.6 }
    ]
  },
  {
    "engine": "claude",
    "data": [...]
  }
]
```

### Get competitor brands

```bash
curl -s "https://app.promptingco.com/api/v1/brands/$TPC_BRAND_ID/competitors" \
  -X POST \
  -H "Cookie: __Secure-better-auth.session_token=$TPC_SESSION_TOKEN" \
  -H "Content-Type: application/json"
```

### Get pinned competitors

```bash
curl -s "https://app.promptingco.com/api/v1/brands/$TPC_BRAND_ID/pinned-competitors" \
  -H "Cookie: __Secure-better-auth.session_token=$TPC_SESSION_TOKEN"
```

---

## 2. Prompt Management

### List prompt topics

Topics group related prompts together for organized tracking.

```bash
curl -s "https://app.promptingco.com/api/v1/prompt-topics?brandId=$TPC_BRAND_ID&page=1&pageSize=20" \
  -H "Cookie: __Secure-better-auth.session_token=$TPC_SESSION_TOKEN"
```

**Parameters:**
- `brandId` (required)
- `page` (optional, default 1)
- `pageSize` (optional, default 10)
- `search` (optional) — text search across topic titles

**Response data shape:**
```json
{
  "data": [
    {
      "id": "topic-123",
      "title": "Product Features",
      "description": "Prompts about core product features",
      "brandId": "abc-123",
      "organizationId": "org-456",
      "createdAt": "2025-01-01T00:00:00Z",
      "updatedAt": "2025-01-15T00:00:00Z"
    }
  ],
  "totalItems": 42
}
```

### Get prompts in a topic

```bash
curl -s "https://app.promptingco.com/api/v1/prompt-topics/{topicId}/prompts?brandId=$TPC_BRAND_ID" \
  -H "Cookie: __Secure-better-auth.session_token=$TPC_SESSION_TOKEN"
```

### Get SOV for a topic

Returns aggregated SOV across all prompts in a topic.

```bash
curl -s "https://app.promptingco.com/api/v1/prompt-topics/{topicId}/sov?brandId=$TPC_BRAND_ID" \
  -H "Cookie: __Secure-better-auth.session_token=$TPC_SESSION_TOKEN"
```

### Get industry rankings for a topic

```bash
curl -s "https://app.promptingco.com/api/v1/prompt-topics/{topicId}/industry-rankings?brandId=$TPC_BRAND_ID" \
  -H "Cookie: __Secure-better-auth.session_token=$TPC_SESSION_TOKEN"
```

### List user personas

Retrieves user personas for a brand (required for creating prompts).

```bash
curl -s "https://app.promptingco.com/api/v1/personas?brandId=$TPC_BRAND_ID" \
  -H "Cookie: __Secure-better-auth.session_token=$TPC_SESSION_TOKEN"
```

**Response data shape:**
```json
{
  "ok": true,
  "data": {
    "personas": [
      {
        "id": "persona-123",
        "name": "General User",
        "description": "...",
        "brandId": "abc-123",
        "createdAt": "2025-01-01T00:00:00Z"
      }
    ],
    "total": 5
  }
}
```

### Create a custom prompt for tracking

Creates a custom prompt with conversation queries across multiple AI engines.

```bash
curl -s "https://app.promptingco.com/api/v1/conversation-queries/bulk" \
  -X POST \
  -H "Cookie: __Secure-better-auth.session_token=$TPC_SESSION_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "brandId": "'$TPC_BRAND_ID'",
    "queries": [
      {
        "prompt": "What are the best project management tools?",
        "model": "chatgpt",
        "maxTurns": 1,
        "userPersonaId": "PERSONA_ID",
        "userPersona": "General User"
      },
      {
        "prompt": "What are the best project management tools?",
        "model": "gemini",
        "maxTurns": 1,
        "userPersonaId": "PERSONA_ID",
        "userPersona": "General User"
      },
      {
        "prompt": "What are the best project management tools?",
        "model": "deepseek",
        "maxTurns": 1,
        "userPersonaId": "PERSONA_ID",
        "userPersona": "General User"
      },
      {
        "prompt": "What are the best project management tools?",
        "model": "sonar",
        "maxTurns": 1,
        "userPersonaId": "PERSONA_ID",
        "userPersona": "General User"
      }
    ]
  }'
```

**Parameters:**
- `brandId` (required) — the brand ID
- `queries` (required) — array of conversation queries to create
  - `prompt` (required) — the prompt text to track
  - `model` (required) — one of: `chatgpt`, `gemini`, `deepseek`, `sonar`
  - `maxTurns` (required) — number of conversation turns (default: 1)
  - `userPersonaId` (required) — persona ID from `/api/v1/personas`
  - `userPersona` (required) — persona name for display

**Response data shape:**
```json
{
  "ok": true,
  "data": {
    "count": 4,
    "promptIds": ["prompt-uuid"]
  }
}
```

### Generate AI-suggested prompt

Generates an AI-suggested prompt based on brand and persona (not for direct tracking).

```bash
curl -s "https://app.promptingco.com/api/v1/prompts/generate" \
  -X POST \
  -H "Cookie: __Secure-better-auth.session_token=$TPC_SESSION_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"brandId": "'$TPC_BRAND_ID'", "userPersonaId": "PERSONA_ID"}'
```

**Note:** This endpoint returns **plain text** (the generated prompt question), not JSON. Use this for inspiration, not for tracking. To track a prompt, use `/api/v1/conversation-queries/bulk`.

### Bulk generate prompts

```bash
curl -s "https://app.promptingco.com/api/v1/prompts/generate-bulk" \
  -X POST \
  -H "Cookie: __Secure-better-auth.session_token=$TPC_SESSION_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"brandId": "'$TPC_BRAND_ID'", "count": 10}'
```

Check bulk job status:
```bash
curl -s "https://app.promptingco.com/api/v1/prompts/generate-bulk/status/{jobId}" \
  -H "Cookie: __Secure-better-auth.session_token=$TPC_SESSION_TOKEN"
```

### Check for duplicate prompts

```bash
curl -s "https://app.promptingco.com/api/v1/prompts/check-duplicates?brandId=$TPC_BRAND_ID&message=YOUR_PROMPT_TEXT" \
  -H "Cookie: __Secure-better-auth.session_token=$TPC_SESSION_TOKEN"
```

### Submit prompt for review

```bash
curl -s "https://app.promptingco.com/api/v1/prompts/review" \
  -X POST \
  -H "Cookie: __Secure-better-auth.session_token=$TPC_SESSION_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"promptId": "PROMPT_ID", "action": "approve"}'
```

### List pending prompts

```bash
curl -s "https://app.promptingco.com/api/v1/prompts/pending?brandId=$TPC_BRAND_ID" \
  -H "Cookie: __Secure-better-auth.session_token=$TPC_SESSION_TOKEN"
```

### List archived prompts

```bash
curl -s "https://app.promptingco.com/api/v1/prompts/archived?brandId=$TPC_BRAND_ID" \
  -H "Cookie: __Secure-better-auth.session_token=$TPC_SESSION_TOKEN"
```

### Restore an archived prompt

```bash
curl -s "https://app.promptingco.com/api/v1/prompts/archived/restore" \
  -X POST \
  -H "Cookie: __Secure-better-auth.session_token=$TPC_SESSION_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"promptId": "PROMPT_ID"}'
```

---

## 3. Content & Draft Management

### List documents

```bash
curl -s "https://app.promptingco.com/api/v1/agentic-documents?brandId=$TPC_BRAND_ID&paginated=true&page=1&pageSize=20" \
  -H "Cookie: __Secure-better-auth.session_token=$TPC_SESSION_TOKEN"
```

**Parameters:**
- `brandId` (required)
- `page`, `pageSize` (optional, max 100)
- `q` (optional) — search query
- `hasContent` (optional) — `true` or `false`
- `sort` (optional) — e.g. `updatedAt:desc`, `createdAt:asc`
- `paginated` (optional) — `true` for paginated response

**Paginated response shape:**
```json
{
  "items": [
    {
      "id": "doc-123",
      "title": "How to use our product",
      "filePath": "/blog/how-to-use",
      "updatedAt": "2025-01-15T00:00:00Z",
      "metaTitle": "How to Use Our Product | Brand",
      "metaDescription": "Learn how...",
      "contentLength": 2450
    }
  ],
  "page": 1,
  "pageSize": 20,
  "total": 87
}
```

### Publish a draft

Queues a draft for publishing to the live site.

```bash
curl -s "https://app.promptingco.com/api/v1/drafts/{draftId}/publish" \
  -X POST \
  -H "Cookie: __Secure-better-auth.session_token=$TPC_SESSION_TOKEN"
```

**Response:**
```json
{ "ok": true, "message": "Draft publishing has been queued", "draftId": "draft-123" }
```

### Submit a draft for review

```bash
curl -s "https://app.promptingco.com/api/v1/drafts/{draftId}/review" \
  -X POST \
  -H "Cookie: __Secure-better-auth.session_token=$TPC_SESSION_TOKEN"
```

### List reviewed drafts

```bash
curl -s "https://app.promptingco.com/api/v1/drafts/reviewed?brandId=$TPC_BRAND_ID" \
  -H "Cookie: __Secure-better-auth.session_token=$TPC_SESSION_TOKEN"
```

### Batch publish drafts

```bash
curl -s "https://app.promptingco.com/api/v1/drafts/publish-batch" \
  -X POST \
  -H "Cookie: __Secure-better-auth.session_token=$TPC_SESSION_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"draftIds": ["draft-1", "draft-2", "draft-3"]}'
```

Check batch status:
```bash
curl -s "https://app.promptingco.com/api/v1/drafts/publish-batch/{batchId}/status" \
  -H "Cookie: __Secure-better-auth.session_token=$TPC_SESSION_TOKEN"
```

### Create a new document

```bash
curl -s "https://app.promptingco.com/api/v1/agentic-documents" \
  -X POST \
  -H "Cookie: __Secure-better-auth.session_token=$TPC_SESSION_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "brandId": "'$TPC_BRAND_ID'",
    "title": "Document Title",
    "filePath": "/blog/my-article",
    "sourceUrl": "https://example.com/source"
  }'
```

### Create a draft for a document

```bash
curl -s "https://app.promptingco.com/api/v1/agentic-documents/{documentId}/create-draft" \
  -X POST \
  -H "Cookie: __Secure-better-auth.session_token=$TPC_SESSION_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Draft Title",
    "content": "Draft content in markdown..."
  }'
```

---

## 4. Stats & Analytics

### Get AI traffic stats

Shows how much traffic AI bots are sending to the brand's website.

```bash
curl -s "https://app.promptingco.com/api/v1/ai-traffic-stats?brandId=$TPC_BRAND_ID&startDate=2025-01-01&endDate=2025-01-31" \
  -H "Cookie: __Secure-better-auth.session_token=$TPC_SESSION_TOKEN"
```

**Parameters:**
- `brandId` (required)
- `startDate` (optional) — format `YYYY-MM-DD`
- `endDate` (optional) — format `YYYY-MM-DD`
- `aiProviders` (optional) — comma-separated list of providers

**Response data shape:**
```json
{
  "data": [
    {
      "date": "2025-01-15",
      "ai_provider": "chatgpt",
      "total_visits": 234,
      "unique_ips": 89,
      "unique_pages": 15,
      "top_paths": ["/pricing", "/features", "/docs"],
      "domain": "example.com",
      "tenant_id": "org-456"
    }
  ],
  "domains": ["example.com", "blog.example.com"]
}
```

### Get human traffic stats (baseline comparison)

```bash
curl -s "https://app.promptingco.com/api/v1/human-traffic-stats?brandId=$TPC_BRAND_ID&startDate=2025-01-01&endDate=2025-01-31" \
  -H "Cookie: __Secure-better-auth.session_token=$TPC_SESSION_TOKEN"
```

### Get SOV daily trend (last 30 days)

Use the presence-rate endpoint with `timeframe=30d`:
```bash
curl -s "https://app.promptingco.com/api/v1/presence-rate?brandId=$TPC_BRAND_ID&timeframe=30d" \
  -H "Cookie: __Secure-better-auth.session_token=$TPC_SESSION_TOKEN"
```

### Get SOV monthly overview

Use `timeframe=90d` for a broader monthly view:
```bash
curl -s "https://app.promptingco.com/api/v1/presence-rate?brandId=$TPC_BRAND_ID&timeframe=90d" \
  -H "Cookie: __Secure-better-auth.session_token=$TPC_SESSION_TOKEN"
```

### Get prompt-level SOV

```bash
curl -s "https://app.promptingco.com/api/v1/prompts/sov?brandId=$TPC_BRAND_ID" \
  -H "Cookie: __Secure-better-auth.session_token=$TPC_SESSION_TOKEN"
```

### Get brand mentions for a prompt

```bash
curl -s "https://app.promptingco.com/api/v1/prompts/brand-mentions?brandId=$TPC_BRAND_ID&promptId=PROMPT_ID" \
  -H "Cookie: __Secure-better-auth.session_token=$TPC_SESSION_TOKEN"
```

### Get competitor mentions for a prompt

```bash
curl -s "https://app.promptingco.com/api/v1/prompts/competitor-mentions?brandId=$TPC_BRAND_ID&promptId=PROMPT_ID" \
  -H "Cookie: __Secure-better-auth.session_token=$TPC_SESSION_TOKEN"
```

---

## 5. Brand Management

### List all brands

```bash
curl -s "https://app.promptingco.com/api/v1/brands?fetchAll=true" \
  -H "Cookie: __Secure-better-auth.session_token=$TPC_SESSION_TOKEN"
```

**Parameters:**
- `search` (optional)
- `page`, `pageSize` (optional)
- `sortBy` — `createdAt` or `name`
- `sortOrder` — `asc` or `desc`
- `fetchAll` — `true` to get all brands
- `includeDomains` — `true` to include domain info

**Response data shape:**
```json
{
  "brands": [
    {
      "id": "brand-123",
      "name": "MyBrand",
      "slug": "mybrand",
      "description": "...",
      "organizationId": "org-456",
      "createdAt": "2025-01-01T00:00:00Z"
    }
  ],
  "total": 5
}
```

### Search brands

```bash
curl -s "https://app.promptingco.com/api/v1/brands/search?q=SEARCH_TERM" \
  -H "Cookie: __Secure-better-auth.session_token=$TPC_SESSION_TOKEN"
```

---

## 6. Weekly Reports

### Preview weekly report

```bash
curl -s "https://app.promptingco.com/api/v1/weekly-reports/preview?brandId=$TPC_BRAND_ID" \
  -H "Cookie: __Secure-better-auth.session_token=$TPC_SESSION_TOKEN"
```

---

## Common Workflows

**IMPORTANT:** All workflows below should be handled by spawning a subagent using the Task tool.

### Workflow 1: Track More Prompts

**Trigger:** User selects "Track more prompts" from the getting started menu.

**Subagent Task:**

```typescript
Task({
  subagent_type: "general-purpose",
  description: "Track prompts workflow",
  prompt: `
    Guide the user through tracking prompts on The Prompting Company platform.

    Brand ID: ${brandId}
    Session Token: ${TPC_SESSION_TOKEN}

    Step 1: Present options

    How would you like to track prompts?

    A. Track a new prompt yourself
    B. Get recommendations from existing prompts

    Choose an option:

    Step 2A: If user chooses "Track a new prompt yourself"
    - Ask for the prompt text
    - Check duplicates: GET https://app.promptingco.com/api/v1/prompts/check-duplicates?brandId=${brandId}&message=<prompt>
    - Fetch personas: GET https://app.promptingco.com/api/v1/personas?brandId=${brandId}
    - Use first persona as default (or let user select)
    - Create prompt with 4 conversation queries:
      POST https://app.promptingco.com/api/v1/conversation-queries/bulk
      Body: {
        "brandId": "${brandId}",
        "queries": [
          { "prompt": "<text>", "model": "chatgpt", "maxTurns": 1, "userPersonaId": "<ID>", "userPersona": "<NAME>" },
          { "prompt": "<text>", "model": "gemini", "maxTurns": 1, "userPersonaId": "<ID>", "userPersona": "<NAME>" },
          { "prompt": "<text>", "model": "deepseek", "maxTurns": 1, "userPersonaId": "<ID>", "userPersona": "<NAME>" },
          { "prompt": "<text>", "model": "sonar", "maxTurns": 1, "userPersonaId": "<ID>", "userPersona": "<NAME>" }
        ]
      }
    - Confirm: "Prompt tracked across ChatGPT, Gemini, DeepSeek, and Perplexity"

    Step 2B: If user chooses "Get recommendations"
    - Fetch pending: GET https://app.promptingco.com/api/v1/prompts/pending?brandId=${brandId}
    - Display list of pending prompts
    - Ask user which ones to approve
    - Approve selected: POST https://app.promptingco.com/api/v1/prompts/review with action="approve"

    Use session token in all requests: -H "Cookie: __Secure-better-auth.session_token=${TPC_SESSION_TOKEN}"
  `
})
```

### Workflow 2: Publish More Content

**Trigger:** User selects "Publish more content" from the getting started menu.

**Subagent Task:**

```typescript
Task({
  subagent_type: "general-purpose",
  description: "Publish content workflow",
  prompt: `
    Guide the user through publishing content from tracked prompts.

    Brand ID: ${brandId}
    Session Token: ${TPC_SESSION_TOKEN}

    Step 1: Fetch prompts
    - GET https://app.promptingco.com/api/v1/prompt-topics?brandId=${brandId}
    - For each topic: GET https://app.promptingco.com/api/v1/prompt-topics/{topicId}/prompts?brandId=${brandId}

    Step 2: Display prompts grouped by topic

    Let's create content from your tracked prompts.

    Available prompts:

    Topic: [Topic Name]
    - [Prompt 1]
    - [Prompt 2]

    Which prompt would you like to create content for?

    Step 3: Create content
    - Ask for document details (title, file path)
    - Create document: POST https://app.promptingco.com/api/v1/agentic-documents
    - Ask for content (markdown format)
    - Create draft: POST https://app.promptingco.com/api/v1/agentic-documents/{docId}/create-draft

    Step 4: Publish
    - Ask if user wants to publish now or save as draft
    - If publish: POST https://app.promptingco.com/api/v1/drafts/{draftId}/publish
    - Confirm success

    Use session token in all requests: -H "Cookie: __Secure-better-auth.session_token=${TPC_SESSION_TOKEN}"
  `
})
```

### Workflow 3: Get Stats

**Trigger:** User selects "Get stats" from the getting started menu.

**Subagent Task:**

```typescript
Task({
  subagent_type: "general-purpose",
  description: "Fetch and display stats",
  prompt: `
    Fetch and display SOV and AI traffic stats.

    Brand ID: ${brandId}
    Session Token: ${TPC_SESSION_TOKEN}

    Step 1: Fetch data
    - SOV: GET https://app.promptingco.com/api/v1/presence-rate?brandId=${brandId}&timeframe=30d
    - AI Traffic: GET https://app.promptingco.com/api/v1/ai-traffic-stats?brandId=${brandId}&startDate=<30_days_ago>&endDate=<today>

    Step 2: Format and display

    Fetching your stats...

    Share of Voice (SOV)
    ────────────────────────────────
    Current SOV: X.XX%
    Trend: [up/down] by X.XX% from last period

    Data points (last 30 days):
    - Date: SOV%

    AI Traffic Stats
    ────────────────────────────────
    Total AI visits: X,XXX

    Top Bots:
    1. ChatGPT: X visits
    2. Claude: X visits
    3. Gemini: X visits
    4. Perplexity: X visits

    Top Pages:
    1. /path: X visits
    2. /path2: X visits
    3. /path3: X visits

    Use clean formatting with proper spacing and newlines.
    No emojis.
    Use session token in all requests: -H "Cookie: __Secure-better-auth.session_token=${TPC_SESSION_TOKEN}"
  `
})
```

### Daily Stats Briefing

**Trigger:** User asks for "daily update" or "daily stats".

**Spawn subagent** with:
- Fetch SOV trend: `GET /api/v1/presence-rate?brandId=...&timeframe=7d`
- Fetch AI traffic: `GET /api/v1/ai-traffic-stats?brandId=...&startDate=YESTERDAY&endDate=TODAY`
- Fetch per-engine breakdown: `GET /api/v1/brand-reach-per-engine?brandId=...&timeframe=7d`
- Summarize: latest SOV %, change from last week, top AI engines, total AI visits

### Competitor Comparison

**Trigger:** User asks to compare against a competitor.

**Spawn subagent** with:
1. Get pinned competitors: `GET /api/v1/brands/{brandId}/pinned-competitors`
2. Get own SOV: `GET /api/v1/presence-rate?brandId=...&timeframe=30d`
3. Get competitor SOV: `GET /api/v1/presence-rate?brandId=...&mentionedBrandId=COMPETITOR_ID&timeframe=30d`
4. Get per-engine breakdown for both
5. Present side-by-side comparison with trends

---

## Error Handling

### Response Structure

Every API response follows this format:

**Success:**
```json
{ "ok": true, "data": { ... } }
```

**Error:**
```json
{
  "ok": false,
  "code": "ERROR_CODE",
  "message": "Human-readable error message",
  "details": { ... } // optional
}
```

**Always check `response.ok` before processing data.**

### Error Codes

| Code | HTTP Status | Description | Action |
|------|-------------|-------------|--------|
| `UNAUTHORIZED` | 401 | Session token is expired or invalid | Ask user to provide a new session token from their browser |
| `FORBIDDEN` | 403 | User doesn't have access to this resource | Check if user has permission or if brand ID is correct |
| `BAD_REQUEST` | 400 | Missing or invalid parameters | Validate required parameters before request |
| `NOT_FOUND` | 404 | Resource doesn't exist | Verify IDs (brandId, promptId, documentId, etc.) |
| `VALIDATION_ERROR` | 400 | Parameter validation failed | Check parameter formats (dates, UUIDs, enums) |
| `RATE_LIMITED` | 429 | Too many requests | Wait and retry with exponential backoff |
| `INTERNAL` | 500 | Server error | Retry once after 2-3 seconds, then report to user |

### Pre-Request Validation

**Before making any API call:**

1. **Verify session token exists:**
   ```bash
   if [ -z "$TPC_SESSION_TOKEN" ]; then
     echo "Error: Session token not provided. Please set TPC_SESSION_TOKEN."
     exit 1
   fi
   ```

2. **Validate UUID parameters:**
   - `brandId`, `promptId`, `documentId`, `topicId` must be valid UUIDs
   - Format: `xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx`

3. **Validate date parameters:**
   - Must be ISO 8601 format: `YYYY-MM-DD`
   - `startDate` must be before `endDate`
   - Example: `2025-01-15`

4. **Validate enum parameters:**
   - `timeframe`: only `7d`, `30d`, or `90d`
   - `sortBy`: only valid column names
   - `sortOrder`: only `asc` or `desc`
   - `action`: only `approve` or `reject`

5. **Validate pagination:**
   - `page` must be >= 1
   - `pageSize` must be <= 100

### Error Recovery Flows

#### 401 Unauthorized (Session Expired)

```bash
# When you receive 401 error:
# 1. Inform user their session has expired
# 2. Ask them to get a new session token:
#    - Go to https://app.promptingco.com
#    - Open browser DevTools (F12)
#    - Go to Application/Storage → Cookies
#    - Copy the value of "__Secure-better-auth.session_token"
# 3. Update TPC_SESSION_TOKEN and retry
```

#### 429 Rate Limited

```bash
# Implement exponential backoff:
retry_count=0
max_retries=3

while [ $retry_count -lt $max_retries ]; do
  response=$(curl -s ...)

  if echo "$response" | jq -e '.code == "RATE_LIMITED"' > /dev/null; then
    wait_time=$((2 ** retry_count))
    echo "Rate limited. Waiting ${wait_time}s before retry..."
    sleep $wait_time
    retry_count=$((retry_count + 1))
  else
    break
  fi
done
```

#### 404 Not Found

```bash
# Common causes:
# 1. Brand ID doesn't exist → Re-run First-Time Setup to select valid brand
# 2. Prompt/Topic/Document deleted → Refresh list and ask user to select again
# 3. Typo in ID → Double-check UUID format
```

#### 500 Internal Server Error

```bash
# Retry once after short delay:
response=$(curl -s ...)

if echo "$response" | jq -e '.code == "INTERNAL"' > /dev/null; then
  echo "Server error. Retrying in 3 seconds..."
  sleep 3
  response=$(curl -s ...)

  if echo "$response" | jq -e '.code == "INTERNAL"' > /dev/null; then
    echo "Error: Server is experiencing issues. Please try again later."
    exit 1
  fi
fi
```

### Parameter Validation Examples

**Date Range:**
```bash
# Validate dates before API call
if [[ ! "$start_date" =~ ^[0-9]{4}-[0-9]{2}-[0-9]{2}$ ]]; then
  echo "Error: start_date must be YYYY-MM-DD format"
  exit 1
fi

# Ensure start is before end
if [[ "$start_date" > "$end_date" ]]; then
  echo "Error: start_date must be before end_date"
  exit 1
fi
```

**UUID:**
```bash
# Validate UUID format
uuid_pattern="^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$"
if [[ ! "$brand_id" =~ $uuid_pattern ]]; then
  echo "Error: Invalid brand ID format. Must be a UUID."
  exit 1
fi
```

### Error Reporting to User

When reporting errors, always include:

1. **What went wrong:** Clear error message
2. **Why it happened:** The error code and server message
3. **What to do next:** Actionable steps to fix

**Example:**
```
❌ Error: Unable to fetch brand data

Reason: UNAUTHORIZED - Session token has expired

Action needed:
1. Go to https://app.promptingco.com
2. Open DevTools (F12) → Application → Cookies
3. Copy the "__Secure-better-auth.session_token" value
4. Update your TPC_SESSION_TOKEN and try again
```

---

## Tips

- **Brand Selection:** Always use the user's selected brand as the default unless they specify another brand by name.
- **SOV Display:** When showing SOV values, multiply `value` by 100 to display as percentage (e.g. `0.42` = `42%`).
- **Date Format:** Always use ISO 8601 format for dates: `YYYY-MM-DD`.
- **Per-Engine SOV:** The `sov` field in per-engine responses is already a 0-100 percentage (no conversion needed).
- **Timeframe Options:**
  - `7d` — weekly view
  - `30d` — monthly view (default)
  - `90d` — quarterly view
- **Daily Stats:** When user asks for "daily stats", use `timeframe=7d` and show the latest data point plus trend.
- **Monthly Stats:** When user asks for "monthly stats", use `timeframe=30d`.
- **Response Parsing:** Always check `response.ok === true` before accessing `response.data`.
- **Error Messages:** When errors occur, show the `message` field from the API response to the user.
- **Brand Context:** If the user mentions a brand name, search for it via `/api/v1/brands/search` to get the brand ID.
