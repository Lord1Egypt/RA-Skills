# MiniMax API Reference

## Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `MINIMAX_API_KEY` | Yes | - | API key from MiniMax platform |
| `MINIMAX_API_HOST` | No | `https://api.minimaxi.com/anthropic` | API endpoint |

## Functions

### web_search(query, count=10)

Performs web search using MiniMax search API.

**Parameters:**
- `query` (str): Search query string
- `count` (int): Maximum number of results (default: 10)

**Returns:**
```json
{
  "success": true,
  "result": {
    "organic": [...],
    "related_searches": [...]
  }
}
```

### understand_image(prompt, image_source)

Analyzes images using MiniMax VLM (Vision Language Model).

**Parameters:**
- `prompt` (str): Analysis prompt/question
- `image_source` (str): Image file path or URL

**Returns:**
```json
{
  "success": true,
  "result": "analysis text"
}
```

### chat(message, system=None, model="MiniMax-M2.7", temperature=1.0, max_tokens=4096, stream=False, history=None)

LLM conversation with MiniMax models.

**Parameters:**
- `message` (str): User message
- `system` (str): System prompt (optional)
- `model` (str): Model name (default: MiniMax-M2.7)
- `temperature` (float): Sampling temperature 0.0-1.0 (default: 1.0)
- `max_tokens` (int): Max tokens to generate (default: 4096)
- `stream` (bool): Enable streaming (default: False)
- `history` (list): Conversation history

**Returns:**
```json
{
  "success": true,
  "result": {
    "content": "response text",
    "thinking": "reasoning content",
    "usage": {...},
    "stop_reason": "stop reason"
  }
}
```

### translate(text, target_lang="English", source_lang="auto", model="MiniMax-M2.7", temperature=1.0, max_tokens=4096)

Translates text between languages.

**Parameters:**
- `text` (str): Text to translate
- `target_lang` (str): Target language (default: English)
- `source_lang` (str): Source language or "auto" (default: auto)
- `model` (str): Model name (default: MiniMax-M2.7)
- `temperature` (float): Temperature (default: 1.0)
- `max_tokens` (int): Max tokens (default: 4096)

**Returns:**
```json
{
  "success": true,
  "result": {
    "translated_text": "translated text",
    "source_lang": "detected or specified source",
    "target_lang": "target language"
  }
}
```

## API Endpoints

| Endpoint | Purpose |
|----------|---------|
| `POST /v1/coding_plan/search` | Web search |
| `POST /v1/coding_plan/vlm` | Image understanding |
| `POST /v1/messages` | LLM inference |

## Error Codes

| Code | Description |
|------|-------------|
| 0 | Success |
| -1 | General error |
| -2 | API key invalid |
| -3 | Rate limit exceeded |
| -4 | Model not found |
