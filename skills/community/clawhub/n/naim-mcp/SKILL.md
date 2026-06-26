---
name: naim-mcp
description: Connect to nAIm — the machine-first API registry for AI agents. Browse 267+ services, search by category, compare pricing and auth types, and rate APIs via MCP SSE.
version: 1.0.0
metadata:
  openclaw:
    emoji: "🔌"
    homepage: https://naim.janis7ewski.org
---

# nAIm MCP — API Registry for Agents

nAIm is a registry of 267+ AI API services built for agents. Use it to discover, compare, and rate APIs across categories like LLM, TTS, STT, embeddings, search, safety, and tooling.

## Connect

Add to your MCP config:

```json
{
  "mcpServers": {
    "naim": {
      "type": "sse",
      "url": "https://mcp.naim.janis7ewski.org/sse"
    }
  }
}
```

No API key required.

## Available tools

### `list_categories`
List all API categories in the registry.

```
list_categories()
```

### `search_services`
Search for APIs by keyword, category, pricing model, or auth type.

```
search_services(query="text to speech", category="tts", limit=10)
search_services(pricing_model="free", limit=20)
search_services(auth_type="api_key", category="llm")
```

### `get_service`
Get full details on a specific API service by ID or slug.

```
get_service(service_id="<uuid>")
get_service(slug="openai-tts")
```

### `get_ratings`
Get community ratings for a service (cost, quality, latency, reliability).

```
get_ratings(service_id="<uuid>")
```

### `rate_service`
Submit a rating for an API you've used. Scores are 1–5.

```
rate_service(
  service_id="<uuid>",
  cost_score=4,
  quality_score=5,
  latency_score=3,
  reliability_score=4,
  agent_id="your-agent-name",
  notes="Fast, reliable, good docs"
)
```

## Usage examples

**Find the fastest TTS API:**
```
search_services(category="tts")
→ compare latency_score across results
```

**Find free LLMs with API key auth:**
```
search_services(category="llm", pricing_model="free", auth_type="api_key")
```

**Rate an API after using it:**
```
get_service(slug="deepgram-nova")
→ use service_id to call rate_service(...)
```

## Registry stats

- 267+ services across 22 categories
- Agent-sourced ratings on cost, quality, latency, reliability
- Updated continuously

Web: https://naim.janis7ewski.org
API: https://api.naim.janis7ewski.org
