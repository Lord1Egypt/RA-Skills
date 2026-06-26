# Kimi API Patterns

## Official Base URL

Use the official Moonshot API base URL:

`https://api.moonshot.ai/v1`

Required headers:
- `Authorization: Bearer $MOONSHOT_API_KEY`
- `Content-Type: application/json`

## Health Check

```bash
KIMI_BASE_URL="https://api.moonshot.ai/v1"

curl -s "${KIMI_BASE_URL}/models" \
  -H "Authorization: Bearer $MOONSHOT_API_KEY" | jq '.data | map(.id)'
```

## Minimal Chat Completion

```bash
curl -s "${KIMI_BASE_URL}/chat/completions" \
  -H "Authorization: Bearer $MOONSHOT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "MODEL_ID",
    "messages": [
      {"role":"system","content":"Be concise and accurate."},
      {"role":"user","content":"Summarize these release notes in 3 bullets."}
    ],
    "temperature": 0.2
  }' | jq -r '.choices[0].message.content'
```

## Strict JSON Pass

Use a second deterministic pass when the first answer needs reasoning freedom:

```bash
curl -s "${KIMI_BASE_URL}/chat/completions" \
  -H "Authorization: Bearer $MOONSHOT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "MODEL_ID",
    "messages": [
      {"role":"system","content":"Return strict JSON with keys label, confidence, action."},
      {"role":"user","content":"Ticket: Customer cannot log in after password reset."}
    ],
    "temperature": 0
  }' | jq -r '.choices[0].message.content' | jq
```

## Minimal Redaction Pass

Before sending sensitive text externally, remove obvious secrets and IDs first:

```bash
sed -E \
  -e 's/(api[_-]?key|token|secret)=([^[:space:]]+)/\1=REDACTED/g' \
  -e 's/[0-9]{12,}/REDACTED_ID/g' \
  incident.txt > incident.redacted.txt
```

## Retry Rules

- Retry transient `429` and `5xx` with capped exponential backoff.
- Do not retry malformed JSON forever; shrink the task or add a normalization pass.
- Save one fallback model route for recurring workflows after the primary route is proven.
