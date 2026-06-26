# OpenRouter Page Structure Reference

## Model Page Structure

**URL Pattern**: `https://openrouter.ai/{model_id}`
Example: `https://openrouter.ai/arcee-ai/trinity-large-preview:free`

### Expiration Notice

**Format**: `<span>Going away April 22, 2026</span>`

**Patterns to match**:
1. English: `Going away April 22, 2026`
2. Chinese: `Going away 2026 年 4 月 22 日`

**Regex patterns**:
```python
# English format
r"Going away\s+(\w+)\s+(\d{1,2}),?\s+(\d{4})"

# Chinese format
r"Going away\s+(\d{4})[年\-]\s*(\d{1,2})[月\-]\s*(\d{1,2})[日]?"
```

### Fetch Method

- **Layer 1**: `requests` + `BeautifulSoup` (works for this page)
- User-Agent: Chrome 144 on macOS
- Response: ~200KB HTML

## Free Models List Page

**URL**: `https://openrouter.ai/models?max_price=0`

**Note**: This is a dynamic React/Next.js page. Content is loaded via JavaScript.

**Fetch options**:
1. **bb-browser adapter** (preferred) - `bb-browser site openrouter/free-models --json --openclaw`
2. `requests` - Returns initial HTML (no model list)
3. `browser` tool - Can render JavaScript

## Internal API

**Endpoint**: `GET /api/frontend/models`

Returns JSON array of all models. Filter by `endpoint.is_free === true` for free models.

**Response structure**:
```json
{
  "data": [
    {
      "slug": "google/gemma-4-26b-a4b-it",
      "name": "Google: Gemma 4 26B A4B (free)",
      "endpoint": {
        "is_free": true,
        "provider_slug": "google-ai-studio"
      },
      "context_length": 262144
    }
  ]
}
```

## bb-browser Adapters

**Location**: `~/.bb-browser/sites/openrouter/`

### `openrouter/free-models`
```bash
bb-browser site openrouter/free-models --json --openclaw
```
Returns: `{"count": N, "models": [{"slug", "name", "author", "context_length", "url"}]}`

### `openrouter/model-expiry`
```bash
bb-browser site openrouter/model-expiry google/gemma-4-26b-a4b-it:free --json --openclaw
```
Returns: `{"model": "...", "going_away": "YYYY-MM-DD"|null, "url": "..."}`

## API Endpoints

**`GET /api/models`**: Returns HTML (not JSON) - not useful for programmatic access

## Testing

```bash
# Test fetch on known expiring model
python3 scripts/fetch-page.py https://openrouter.ai/arcee-ai/trinity-large-preview:free --verbose

# Test full check
python3 scripts/check-models.py --verbose
```

## Notes

- OpenRouter does not have a public API for model listings
- Free models are identified by `:free` suffix in model ID
- Expiration notices appear ~1-2 weeks before service ends
- Page structure may change - monitor and update patterns as needed
