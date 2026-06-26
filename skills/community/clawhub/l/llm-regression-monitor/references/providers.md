# Providers — Setup Guide

This reference covers how to configure each LLM provider for use in `test_suite.yaml`.

---

## OpenAI

**Provider value in test_suite.yaml:** `openai`

### Required env var
```bash
export OPENAI_API_KEY=sk-...
```

### Supported models
| Model | Notes |
|---|---|
| `gpt-4o` | Most capable, higher cost |
| `gpt-4o-mini` | Recommended for monitoring (fast, cheap, reliable) |
| `gpt-3.5-turbo` | Legacy, available on older accounts |

### Verify setup
```bash
python -c "import llm_behave; p = llm_behave.get_provider('openai'); print(p.complete('Say hello'))"
```

---

## Anthropic

**Provider value in test_suite.yaml:** `anthropic`

### Required env var
```bash
export ANTHROPIC_API_KEY=sk-ant-...
```

### Supported models
| Model | Notes |
|---|---|
| `claude-opus-4-6` | Most capable |
| `claude-sonnet-4-6` | Balanced capability and cost |
| `claude-haiku-4-5` | Recommended for monitoring (fastest, cheapest) |

### Verify setup
```bash
python -c "import llm_behave; p = llm_behave.get_provider('anthropic'); print(p.complete('Say hello'))"
```

---

## Ollama (Local)

**Provider value in test_suite.yaml:** `ollama`

No API key required. Ollama runs locally on your machine.

### Setup
1. Install Ollama: https://ollama.com
2. Pull the model you want to test:
   ```bash
   ollama pull llama3
   ollama pull mistral
   ollama pull phi3
   ```
3. Confirm Ollama is running:
   ```bash
   ollama list
   ```

### Supported models
Any model available via `ollama list`. Common choices:

| Model | Notes |
|---|---|
| `llama3` | General purpose, good baseline |
| `mistral` | Strong at instruction following |
| `phi3` | Lightweight, fast on CPU |

### Default Ollama URL
`http://localhost:11434` — the scripts use this automatically. No configuration needed unless you changed the Ollama port.

### Override the URL (optional)
```bash
export OLLAMA_BASE_URL=http://localhost:11434
```

### Verify setup
```bash
python -c "import llm_behave; p = llm_behave.get_provider('ollama'); print(p.complete('Say hello', model='llama3'))"
```

---

## Custom Provider

**Provider value in test_suite.yaml:** `custom`

Use this when you have an internal LLM endpoint or a provider not natively supported by `llm-behave`.

### Required env vars
```bash
export CUSTOM_LLM_BASE_URL=https://your-internal-llm.example.com/v1
export CUSTOM_LLM_API_KEY=your-key-here    # omit if your endpoint has no auth
```

### Expected API format
The custom provider adapter expects an OpenAI-compatible `/chat/completions` endpoint. If your endpoint uses a different format, you will need to write a thin adapter — see the `llm-behave` documentation for the `BaseProvider` interface.

### Verify setup
```bash
python -c "import llm_behave; p = llm_behave.get_provider('custom'); print(p.complete('Say hello', model='your-model-name'))"
```

---

## Using Multiple Providers in One Suite

You can mix providers freely in a single `test_suite.yaml`. Each test specifies its own `provider` and `model`. All required env vars must be set before running the scripts.

```yaml
tests:
  - name: openai_test
    provider: openai
    model: gpt-4o-mini
    prompt: "..."

  - name: anthropic_test
    provider: anthropic
    model: claude-haiku-4-5
    prompt: "..."

  - name: local_test
    provider: ollama
    model: llama3
    prompt: "..."
```

---

## Environment Variable Summary

| Provider | Required env var | Optional env var |
|---|---|---|
| `openai` | `OPENAI_API_KEY` | — |
| `anthropic` | `ANTHROPIC_API_KEY` | — |
| `ollama` | *(none)* | `OLLAMA_BASE_URL` |
| `custom` | `CUSTOM_LLM_BASE_URL` | `CUSTOM_LLM_API_KEY` |

---

## Storing Keys Safely

Never commit API keys to version control. Recommended approaches:

**`.env` file + python-dotenv** (simplest for local use)
```bash
# .env
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
```
The scripts automatically load `.env` if present (via `python-dotenv`). Add `.env` to your `.gitignore`.

**Shell profile** (persists across sessions)
```bash
# ~/.bashrc or ~/.zshrc
export OPENAI_API_KEY=sk-...
```

**CI/CD secrets** — set as environment secrets in GitHub Actions, GitLab CI, etc. The scripts read from the environment directly and have no CI-specific code.
