# The Prompting Company — API Quick Reference

## Base Configuration

| Variable | Description | Example |
|---|---|---|
| `TPC_BASE_URL` | Platform base URL | `https://app.promptingcompany.com` |
| `TPC_SESSION_TOKEN` | `__Secure-better-auth.session_token` cookie value | `eyJ...` |
| `TPC_BRAND_ID` | Default brand UUID | `abc-123-def-456` |
| `TPC_ORG_SLUG` | Organization slug | `my-company` |

## Endpoint Summary

### Analytics & SOV

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/v1/presence-rate` | SOV timeseries (30-day SMA) |
| GET | `/api/v1/brand-reach-per-engine` | SOV broken down by AI engine |
| GET | `/api/v1/ai-traffic-stats` | AI bot traffic to your site |
| GET | `/api/v1/human-traffic-stats` | Human traffic baseline |
| GET | `/api/v1/prompts/sov` | Per-prompt SOV |
| GET | `/api/v1/prompts/brand-mentions` | Brand mentions for a prompt |
| GET | `/api/v1/prompts/competitor-mentions` | Competitor mentions for a prompt |
| GET | `/api/v1/weekly-reports/preview` | Weekly report preview |

### Prompt Management

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/v1/prompt-topics` | List prompt topics (paginated) |
| GET | `/api/v1/prompt-topics/{topicId}/prompts` | Prompts in a topic |
| GET | `/api/v1/prompt-topics/{topicId}/sov` | Topic-level SOV |
| GET | `/api/v1/prompt-topics/{topicId}/industry-rankings` | Industry rank for topic |
| GET | `/api/v1/personas` | List user personas for a brand |
| POST | `/api/v1/conversation-queries/bulk` | **Create custom prompts with conversation queries** |
| POST | `/api/v1/prompts/generate` | Generate AI-suggested prompt (text only, not tracked) |
| POST | `/api/v1/prompts/generate-bulk` | Bulk generate AI-suggested prompts |
| GET | `/api/v1/prompts/generate-bulk/status/{jobId}` | Check bulk job status |
| GET | `/api/v1/prompts/check-duplicates` | Check for duplicate prompts |
| POST | `/api/v1/prompts/review` | Approve/reject a prompt |
| GET | `/api/v1/prompts/pending` | List pending prompts |
| GET | `/api/v1/prompts/archived` | List archived prompts |
| POST | `/api/v1/prompts/archived/restore` | Restore archived prompt |
| DELETE | `/api/v1/prompts/{id}` | Delete a prompt |

### Content & Drafts

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/v1/agentic-documents` | List documents |
| POST | `/api/v1/agentic-documents` | Create document |
| GET | `/api/v1/agentic-documents/{id}` | Get single document |
| PUT | `/api/v1/agentic-documents/{id}` | Update document |
| POST | `/api/v1/agentic-documents/{id}/create-draft` | Create draft |
| POST | `/api/v1/drafts/{id}/publish` | Publish a draft |
| POST | `/api/v1/drafts/{id}/review` | Submit draft for review |
| GET | `/api/v1/drafts/reviewed` | List reviewed drafts |
| POST | `/api/v1/drafts/publish-batch` | Batch publish drafts |
| GET | `/api/v1/drafts/publish-batch/{batchId}/status` | Batch publish status |

### Brands & Competitors

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/v1/brands` | List brands |
| GET | `/api/v1/brands/search` | Search brands |
| POST | `/api/v1/brands/{brandId}/competitors` | Get competitors |
| GET | `/api/v1/brands/{brandId}/pinned-competitors` | Get pinned competitors |
| GET | `/api/v1/brands/{brandId}/competitor-domains` | Competitor domains |

## Response Envelope

Every response follows this pattern:

```
Success: { "ok": true,  "data": <payload> }
Error:   { "ok": false, "code": "<ERROR_CODE>", "message": "<human-readable>", "details": <optional> }
```

Error codes: `BAD_REQUEST`, `UNAUTHORIZED`, `FORBIDDEN`, `NOT_FOUND`, `INTERNAL`, `VALIDATION_ERROR`, `RATE_LIMITED`

## Key Data Types

### SOV Data Point
```
{ "date": "YYYY-MM-DD", "value": 0.0-1.0, "sum_mention": int, "sum_total": int }
```
- `value` is a decimal (0.42 = 42% SOV)

### AI Traffic Row
```
{ "date": "YYYY-MM-DD", "ai_provider": string, "total_visits": int, "unique_ips": int, "unique_pages": int, "top_paths": string[], "domain": string }
```

### Prompt Topic
```
{ "id": uuid, "title": string, "description": string|null, "brandId": uuid, "createdAt": datetime, "updatedAt": datetime }
```

### Document
```
{ "id": uuid, "title": string, "filePath": string, "updatedAt": datetime, "metaTitle": string|null, "metaDescription": string|null, "contentLength": int }
```

### User Persona
```
{ "id": uuid, "name": string, "description": string, "brandId": uuid, "createdAt": datetime }
```

### Conversation Query (for prompt tracking)
```
{
  "prompt": string,               // The prompt text to track
  "model": "chatgpt" | "gemini" | "deepseek" | "sonar",  // AI engine
  "maxTurns": number,             // Default: 1
  "userPersonaId": uuid,          // Required: from /api/v1/personas
  "userPersona": string           // Required: persona name for display
}
```

## AI Engines Tracked

The platform monitors brand mentions across these AI engines:
- **ChatGPT** (OpenAI) — model: `chatgpt`
- **Claude** (Anthropic) — model: `claude`
- **Gemini** (Google) — model: `gemini`
- **Perplexity** — model: `sonar`
- **DeepSeek** — model: `deepseek`
- **Google AI Overview**

**Note:** When creating conversation queries, use the model identifiers above (e.g., `"sonar"` for Perplexity, not `"perplexity"`).
