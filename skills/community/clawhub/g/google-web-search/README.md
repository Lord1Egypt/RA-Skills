# Google Web Search (Gemini Grounding)

Real-time web search using Gemini API's `google_search` grounding tool.

## Features

- ✅ Real-time web search with grounded citations
- ✅ Natural language answers (no JSON parsing needed)
- ✅ Configurable Gemini model selection
- ✅ Simple Python API

## Quick Start

### 1. Set API Key

```bash
export GEMINI_API_KEY=your_key_here
```

Get your API key at [Google AI Studio](https://aistudio.google.com/app/apikey)

### 2. Use in OpenClaw

```python
from skills.google-web-search.scripts.example import get_grounded_response

# Ask a question
answer = get_grounded_response("What is the weather in Seoul today?")
print(answer)
# Output: Natural language answer with citations
```

### 3. Optional: Change Model

```bash
export GEMINI_MODEL=gemini-3-pro-preview
```

Supported models:
- `gemini-2.5-flash-lite` (default) - Fast & cheap
- `gemini-3-flash-preview` - Latest flash
- `gemini-3-pro-preview` - More capable

## Use Cases

- 📰 Real-time news and events
- 💹 Current prices (stocks, crypto, etc.)
- 🌤️ Weather forecasts
- 📊 Latest statistics and data
- 🔍 Any information requiring recent sources

## How It Works

This skill uses Gemini's **grounding with Google Search** tool, which:
1. Executes a Google search for your query
2. Processes the search results
3. Generates a natural language answer
4. Includes verifiable citations

**Key advantage:** You get curated answers instead of raw search results.

## Requirements

- Python ≥ 3.11
- `google-genai` ≥ 1.50.0
- `pydantic-settings` ≥ 2.0.0

## Installation

The skill auto-installs Python dependencies using one of:

1. **[uv](https://github.com/astral-sh/uv)** (if available) - A fast Python package manager by Astral (creators of Ruff)
2. **pip** (fallback) - Standard Python package installer

```bash
# The install command checks for uv first, falls back to pip:
# command -v uv >/dev/null && uv sync || pip install -r requirements.txt
```

To install manually:
```bash
cd skills/google-web-search
pip install -r requirements.txt
```

## Credentials

This skill requires **one** environment variable:

| Variable | Required | Description |
|----------|----------|-------------|
| `GEMINI_API_KEY` | ✅ Yes | Your Gemini API key from [Google AI Studio](https://aistudio.google.com/app/apikey) |
| `GEMINI_MODEL` | ❌ No | Model to use (default: `gemini-2.5-flash-lite`) |

**Security tip:** Create a restricted API key with minimal permissions (only Gemini API access needed).

## License

Same as OpenClaw project
