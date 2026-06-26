# NanoGPT /models API

Source: https://docs.nano-gpt.com/api-reference/endpoint/models.md

## Endpoints
```
GET /api/v1/models                              # All visible text models
GET /api/v1/models?detailed=true                # Includes pricing, capabilities, context_length
GET /api/subscription/v1/models                 # Subscription-included models only
GET /api/paid/v1/models                         # Paid/premium models only
```

## Basic model object
```json
{
  "id": "openai/gpt-5.2",
  "object": "model",
  "created": 1736966400,
  "owned_by": "openai"
}
```

## Detailed model object (detailed=true)
```json
{
  "id": "openai/gpt-5.2",
  "object": "model",
  "created": 1736966400,
  "owned_by": "openai",
  "name": "GPT-5.2",
  "description": "OpenAI's flagship general-purpose model",
  "context_length": 128000,
  "max_output_tokens": 16384,
  "capabilities": {
    "vision": true,
    "reasoning": false,
    "tool_calling": true,
    "parallel_tool_calls": true,
    "structured_output": true,
    "pdf_upload": true
  },
  "pricing": {
    "prompt": 2.50,
    "completion": 10.00,
    "currency": "USD",
    "unit": "per_million_tokens"
  },
  "icon_url": "/icons/OpenAI.svg",
  "cost_estimate": "$",
  "category": "flagship"
}
```

## Key notes
- Auth-optional for listing — invalid/missing key still returns model list (but omits user-specific pricing)
- `context_length` = max input tokens, `max_output_tokens` = max output tokens
- Model availability changes — always use `/api/v1/models` as source of truth
- Separate endpoints for image/video/audio models: `/api/v1/image-models`, `/api/v1/video-models`, `/api/v1/audio-models`

## Capabilities flags
| Flag | Description |
|---|---|
| `vision` | Image inputs |
| `reasoning` | Extended thinking |
| `tool_calling` | Function/tool calling |
| `parallel_tool_calls` | Multiple tool calls in one turn |
| `structured_output` | JSON/output modes |
| `pdf_upload` | PDF/document inputs |
