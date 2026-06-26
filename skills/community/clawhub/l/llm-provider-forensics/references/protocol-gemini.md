# Gemini-Compatible Protocol Rules

## Catalog probes
Try in order:
- `GET /v1beta/models?key=...`
- `GET /v1/models?key=...`

## Inference probes
Try in order:
- `POST /v1beta/models/{model}:generateContent?key=...`
- `POST /v1/models/{model}:generateContent?key=...`

## Minimal body
```json
{
  "contents": [{"parts": [{"text": "Reply with exactly OK"}]}]
}
```

## Notes
- Gemini commonly uses API key query parameter auth.
- Some gateways translate Gemini models into OpenAI-compatible endpoints; if so, probe both.
- Record candidateCount / content / parts response structure.
