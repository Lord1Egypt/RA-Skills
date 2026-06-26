# Model Registry

## Supported Models

| Key | Provider | Model ID | Label | Input $/1M | Output $/1M |
|-----|----------|----------|-------|-----------|------------|
| opus | Bedrock | `global.anthropic.claude-opus-4-6-v1` | Claude Opus 4.6 | $15.00 | $75.00 |
| sonnet | Bedrock | `global.anthropic.claude-sonnet-4-6` | Claude Sonnet 4.6 | $3.00 | $15.00 |
| haiku | Bedrock | `us.anthropic.claude-haiku-4-5-20251001-v1:0` | Claude Haiku 4.5 | $0.80 | $4.00 |
| gemini3pro | Gemini | `gemini-3.1-pro-preview` | Gemini 3.1 Pro | $2.00 | $12.00 |
| gemini3flash | Gemini | `gemini-3.1-flash-lite-preview` | Gemini 3.1 Flash-Lite | $0.25 | $1.50 |
| paddleocr | PaddleOCR | `paddleocr` | PaddleOCR | Free | Free |

> **Note on Opus model ID:** Use the `global.` prefix (`global.anthropic.claude-opus-4-6-v1`), not the bare `anthropic.claude-opus-4-6-v1`. The `global.*` inference profile routes across regions and is required for newer models.

## Adding New Models

Edit the `MODELS` dict in `scripts/run_benchmark.py`. Each entry needs:

```python
'my_model': {
    'provider': 'bedrock',           # bedrock | gemini | paddleocr
    'model_id': 'global.my.model',   # API model identifier
    'label': 'My Model Name',        # Display name for reports
    'input_price': 3.0,              # Cost per 1M input tokens (USD)
    'output_price': 15.0,            # Cost per 1M output tokens (USD)
    'required_env': [],              # Env vars required; [] for bedrock
},
```

## Provider Setup

### Bedrock (Claude models)
- Requires AWS credentials with `bedrock-runtime:Converse` permission
- Set `AWS_REGION` env var (default: `us-west-2`)
- Model IDs use inference profile prefixes:
  - `global.*` — cross-region routing (recommended for Opus, Sonnet)
  - `us.*` — US-only routing (Haiku)
  - Bare IDs (`anthropic.*`) will **fail** for newer models — always use prefixed IDs

### Gemini (Google AI Studio)
- Set `GOOGLE_API_KEY` environment variable
- Free tier: ~15 RPM, 1500 RPD
- Paid tier: standard Google AI pricing
- SDK: `pip install google-genai`

### PaddleOCR (Optional)
- Requires an external HTTP endpoint serving the PaddleOCR API
- Set `PADDLEOCR_ENDPOINT` — if **not set**, this model is **automatically skipped** (no error)
- Optionally set `PADDLEOCR_TOKEN` for authenticated endpoints
- Self-hosted option: `pip install paddlepaddle paddleocr` + wrap in a simple Flask API

## Benchmark Findings (2026-03-14, product packaging images)

Human-verified accuracy ranking:
1. **Gemini 3.1 Pro — 98.7%** — Best accuracy, $0.006/image
2. **Claude Opus 4.6 — 92.3%** — Missed weight, ratio detail, 7 OZ
3. **Gemini 3.1 Flash — 89.7%** — Fast (9.7s), missed fine print
4. **Claude Sonnet 4.6 — 88.5%** — Stable structured output
5. **PaddleOCR — 67.9%** — Free, character errors on packaging
6. **Claude Haiku 4.5 — 42.3%** — Poor Chinese OCR, garbled output
