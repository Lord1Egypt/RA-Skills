---
name: ollang-qc-eval
description: Run a QC (Quality Control) evaluation on an Ollang order to get AI-powered quality scores for accuracy, fluency, tone, and cultural fit. Use when the user wants to assess translation quality.
---

# Ollang QC Evaluation

Run an AI-powered quality control evaluation on a completed order. Scores accuracy, fluency, tone, and cultural fit.

## Authentication

All requests require the `X-Api-Key` header. The API key is read from the `OLLANG_API_KEY` environment variable. If not set, instruct the user to run: `export OLLANG_API_KEY=<your-api-key>` (get it from https://lab.ollang.com).

## Endpoint

**POST** `https://api-integration.ollang.com/integration/orders/{orderId}/qc`

### Path Parameters
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `orderId` | string | Yes | The completed order to evaluate |

### Request Body (JSON)
| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `accuracy` | boolean | `true` | Evaluate translation accuracy |
| `fluency` | boolean | `true` | Evaluate language fluency |
| `tone` | boolean | `true` | Evaluate tone consistency |
| `culturalFit` | boolean | `true` | Evaluate cultural appropriateness |
| `customPrompt` | string | — | Additional evaluation instructions |
| `callbackUrl` | string | — | HTTPS webhook URL for async results |

## Response (200)
```json
{
  "success": true,
  "message": "string",
  "evalId": "string",
  "creditsUsed": 0,
  "isProcessing": true,
  "textSummary": "string",
  "scores": [
    { "name": "accuracy", "score": 92, "details": "..." },
    { "name": "fluency", "score": 85, "details": "..." },
    { "name": "tone", "score": 90, "details": "..." },
    { "name": "culturalFit", "score": 88, "details": "..." }
  ],
  "segmentEvals": [
    {
      "segmentId": "string",
      "scores": [{ "name": "accuracy", "score": 95 }],
      "comments": "string"
    }
  ]
}
```

## Example (curl)
```bash
# Full evaluation with all metrics
curl -X POST https://api-integration.ollang.com/integration/orders/ORDER_ID/qc \
  -H "X-Api-Key: $OLLANG_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "accuracy": true,
    "fluency": true,
    "tone": true,
    "culturalFit": true,
    "callbackUrl": "https://your-server.com/webhook/qc-results"
  }'

# Custom evaluation with specific focus
curl -X POST https://api-integration.ollang.com/integration/orders/ORDER_ID/qc \
  -H "X-Api-Key: $OLLANG_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "accuracy": true,
    "fluency": false,
    "tone": false,
    "culturalFit": false,
    "customPrompt": "Focus on technical terminology accuracy"
  }'
```

## Behavior

1. Read the API key from the `OLLANG_API_KEY` environment variable. If not set, tell the user to set it with: `export OLLANG_API_KEY=<your-api-key>`
2. Ask for the `orderId` if not provided
3. Ask which metrics to evaluate (default: all four enabled)
4. Ask if they want a `callbackUrl` for async results (useful for large orders)
5. Submit the evaluation request
6. If `isProcessing` is true, inform the user results will be ready shortly or sent to the callback
7. If results are immediate, display scores in a readable format with summary

## Error Codes
- `400` - Order not eligible for QC (wrong type or status)
- `401` - Invalid or missing API key
- `403` - Access denied
- `404` - Order not found
