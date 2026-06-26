# Backend Config

Only use an LLM backend when the user asks for higher accuracy on complex layouts or tables.

## Backend Selection

- `default`: Local default pipeline, best for privacy and CI.
- `deepseek`: Best for complex layouts when a local vLLM endpoint is available.
- `paddle`: Strong accuracy with lower GPU requirements.
- `glm`: Faster OCR-style inference on compatible deployments.

## Examples

```bash
ppx parse report.pdf --backend deepseek \
  --deepseek '{"base_url":"http://127.0.0.1:4000/v1","model":"deepseek-ocr-2","api_key":""}'

ppx parse report.pdf --backend paddle \
  --paddle '{"base_url":"http://127.0.0.1:4001/v1","model":"paddleocr-vl","api_key":""}'

ppx parse report.pdf --backend glm \
  --glm '{"base_url":"http://127.0.0.1:4002/v1","model":"glmocr","api_key":""}'
```

## Persistent Settings

Use `--set` to avoid repeating backend config:

```bash
ppx parse report.pdf --set backend="deepseek" \
  --set deepseek.base_url="http://127.0.0.1:4000/v1"
```

If backend parsing fails, fall back to the default pipeline unless the user explicitly requires the backend path.
