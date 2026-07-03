# Model Throughput Tester

Benchmark LLM model throughput — measure tokens/s, latency, and output speed for any language model.

## Features

- **Auto Mode**: Test your current session model via `openclaw infer`, no API key needed
- **API Mode**: Direct benchmark against any OpenAI-compatible endpoint
- **Flexible**: Custom prompts, iteration counts, timeout controls
- **Reports**: Markdown + CSV output with per-iteration details

## Quick Start

```bash
# Auto mode — test current session model
python3 throughput.py --auto

# Test a specific model
python3 throughput.py --auto --model "gpt-4o"

# API mode — test against an endpoint
python3 throughput.py \
  --url "https://api.openai.com/v1" \
  --key "sk-xxx" \
  --models "gpt-4o-mini,gpt-4o" \
  --iterations 5
```

## Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `--auto` | off | Enable auto mode (uses openclaw infer) |
| `--model` | auto-detect | Model identifier |
| `--url` | — | API base URL (API mode) |
| `--key` | — | API key (API mode) |
| `--models` | — | Comma-separated model list (API mode) |
| `--iterations` | `3` | Test iterations per model |
| `--max-tokens` | `512` | Max output tokens |
| `--test-prompt` | built-in | Custom test prompt |
| `--timeout` | `60` | Request timeout (seconds) |
| `--output` | `throughput-report.md` | Output report filename |
| `--csv` | false | Also generate CSV output |

## Metrics

| Metric | Description |
|--------|-------------|
| **Tokens/s** | Throughput = Output Tokens / Elapsed Time |
| **Avg Latency** | Average single-request latency |
| **Avg Output Tokens** | Average output token count |
| **Error Rate** | Failed request ratio |

## Example Output

```
📊 Model Throughput Report
Mode: Auto (openclaw infer) | Iterations: 3

Summary
| Model             | Avg Tokens/s | Latency(s) | Output Tokens | Error |
|-------------------|-------------|------------|----------------|-------|
| zai/glm-5-turbo   | 57.9        | 20.6       | 979            | 0.0%  |
```

## How It Works

**Auto Mode**: Sends a test prompt via `openclaw infer model run`, measures wall-clock time from start to last token, then estimates token count from output text.

**API Mode**: Calls `/v1/chat/completions` with streaming disabled, reads `usage.completion_tokens` for precise token counts.

## Notes

- Auto mode throughput includes gateway routing overhead (~1-3% lower than direct API)
- Auto mode token counts are estimates; API mode uses precise values
- English prompts yield more accurate token estimates in auto mode
- Anti-cache: random seed suffix appended per iteration

## Prerequisites

- Python 3 (built-in on macOS)
- `openclaw` CLI (for auto mode)

## File Structure

```
~/.openclaw/workspace/skills/model-throughput-tester/
├── SKILL.md           # Agent trigger & execution guide
├── README.md          # This file
├── README.zh.md       # Chinese version
├── throughput.py      # Main script
└── throughput-report.md  # Generated reports (on demand)
```

## License

MIT-0
