---
name: modelslab-chat-generation
description: Chat with LLM models using ModelsLab's OpenAI-compatible Chat Completions API. Supports 60+ models including DeepSeek R1, Meta Llama, Google Gemini, Qwen, and Mistral with streaming, function calling, and structured outputs.
---

# ModelsLab Chat/LLM Generation

Send chat completions to 60+ LLM models through a single OpenAI-compatible endpoint.

## When to Use This Skill

- Chat with AI models (DeepSeek, Llama, Gemini, Qwen, Mistral)
- Build conversational AI applications
- Generate text completions with system prompts
- Use function/tool calling with LLMs
- Stream responses for real-time output
- Get structured JSON responses

## API Endpoint

**Chat Completions**: `POST https://modelslab.com/api/v7/llm/chat/completions`

The endpoint follows the OpenAI chat completions format, making it easy to switch from OpenAI or use the OpenAI SDK.

## Quick Start

```python
import requests

def chat(message, api_key, model="meta-llama-3-8B-instruct"):
    """Send a chat completion request.

    Args:
        message: The user message
        api_key: Your ModelsLab API key
        model: LLM model ID (use modelslab models search --feature llmaster to find models)
    """
    response = requests.post(
        "https://modelslab.com/api/v7/llm/chat/completions",
        json={
            "key": api_key,
            "model_id": model,
            "messages": [
                {"role": "user", "content": message}
            ],
            "max_tokens": 200,
            "temperature": 0.7
        }
    )

    data = response.json()

    if "choices" in data:
        return data["choices"][0]["message"]["content"]
    else:
        raise Exception(f"Error: {data.get('message', 'Unknown error')}")

# Usage
reply = chat(
    "Explain quantum computing in simple terms.",
    "your_api_key"
)
print(reply)
```

## With System Prompt

```python
def chat_with_system(system_prompt, message, api_key, model="meta-llama-3-8B-instruct"):
    """Chat with a system prompt for role/behavior control."""
    response = requests.post(
        "https://modelslab.com/api/v7/llm/chat/completions",
        json={
            "key": api_key,
            "model_id": model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": message}
            ],
            "max_tokens": 500,
            "temperature": 0.7
        }
    )

    data = response.json()
    if "choices" in data:
        return data["choices"][0]["message"]["content"]

# Usage
reply = chat_with_system(
    "You are a Python expert. Give concise code examples.",
    "How do I read a CSV file?",
    "your_api_key"
)
```

## Multi-Turn Conversation

```python
def conversation(messages, api_key, model="meta-llama-3-8B-instruct"):
    """Send a multi-turn conversation."""
    response = requests.post(
        "https://modelslab.com/api/v7/llm/chat/completions",
        json={
            "key": api_key,
            "model_id": model,
            "messages": messages,
            "max_tokens": 500,
            "temperature": 0.7
        }
    )
    return response.json()

# Multi-turn example
messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "What is Python?"},
    {"role": "assistant", "content": "Python is a high-level programming language..."},
    {"role": "user", "content": "Show me a hello world example."}
]

result = conversation(messages, "your_api_key")
print(result["choices"][0]["message"]["content"])
```

## OpenAI SDK Compatibility

You can use the official OpenAI Python SDK by changing the base URL and API key:

```python
from openai import OpenAI

client = OpenAI(
    base_url="https://modelslab.com/api/v7/llm",
    api_key="your_modelslab_api_key"
)

response = client.chat.completions.create(
    model="meta-llama-3-8B-instruct",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Hello!"}
    ],
    max_tokens=100,
    temperature=0.7
)

print(response.choices[0].message.content)
```

## cURL Example

```bash
curl -X POST "https://modelslab.com/api/v7/llm/chat/completions" \
  -H "Content-Type: application/json" \
  -d '{
    "key": "your_api_key",
    "model_id": "meta-llama-3-8B-instruct",
    "messages": [
      {"role": "user", "content": "Say hello in one sentence."}
    ],
    "max_tokens": 50,
    "temperature": 0.7
  }'
```

## Discovering LLM Models

```bash
# Search all chat/LLM models
modelslab models search --feature llmaster

# Search by provider
modelslab models search --search "deepseek"
modelslab models search --search "llama"
modelslab models search --search "gemini"

# Get model details
modelslab models detail --id meta-llama-3-8B-instruct
```

## Popular LLM Model IDs

### Meta Llama
- `meta-llama-3-8B-instruct` — Llama 3 8B (fast, efficient)
- `meta-llama-Llama-3.3-70B-Instruct-Turbo` — Llama 3.3 70B (powerful)
- `meta-llama-Meta-Llama-3.1-405B-Instruct-Turbo` — Llama 3.1 405B (largest)

### DeepSeek
- `deepseek-ai-DeepSeek-R1-Distill-Llama-70B` — DeepSeek R1 (reasoning)
- `deepseek-ai-DeepSeek-V3` — DeepSeek V3 (general purpose)

### Google
- `gemini-2.0-flash-001` — Gemini 2.0 Flash (fast)
- `gemini-2.5-pro` — Gemini 2.5 Pro (capable)

### Qwen
- `Qwen-Qwen2.5-72B-Instruct-Turbo` — Qwen 2.5 72B
- `Qwen-Qwen2.5-Coder-32B-Instruct` — Qwen 2.5 Coder

### Mistral
- `mistralai-Mixtral-8x7B-Instruct-v0.1` — Mixtral 8x7B
- `mistralai-Mistral-Small-24B-Instruct-2501` — Mistral Small

## Key Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `model_id` | string | Yes | LLM model identifier (alias: `model`) |
| `messages` | array | Yes | Array of message objects with `role` and `content` |
| `temperature` | float | No | Sampling temperature (0-2, default varies by model) |
| `max_tokens` | integer | No | Maximum tokens to generate |
| `top_p` | float | No | Nucleus sampling (0-1) |
| `top_k` | integer | No | Top-k sampling |
| `frequency_penalty` | float | No | Frequency penalty (-2 to 2) |
| `presence_penalty` | float | No | Presence penalty (-2 to 2) |
| `streaming` | boolean | No | Enable streaming responses (alias: `stream`) |
| `n` | integer | No | Number of completions (1-10) |
| `stop` | array | No | Stop sequences (max 4) |
| `seed` | integer | No | Random seed for reproducibility |
| `tools` | array | No | Function/tool definitions |
| `tool_choice` | string | No | Tool selection strategy |
| `response_format` | object | No | `{"type": "json_object"}` for JSON mode |

## Response Format

The response follows the OpenAI chat completions format:

```json
{
  "id": "gen-...",
  "model": "meta-llama-3-8B-instruct",
  "object": "chat.completion",
  "created": 1771658583,
  "choices": [
    {
      "index": 0,
      "finish_reason": "stop",
      "message": {
        "role": "assistant",
        "content": "Hello! How can I help you today?"
      }
    }
  ],
  "usage": {
    "prompt_tokens": 17,
    "completion_tokens": 10,
    "total_tokens": 27
  }
}
```

## Error Handling

```python
def safe_chat(message, api_key, model="meta-llama-3-8B-instruct"):
    """Chat with error handling."""
    try:
        response = requests.post(
            "https://modelslab.com/api/v7/llm/chat/completions",
            json={
                "key": api_key,
                "model_id": model,
                "messages": [{"role": "user", "content": message}],
                "max_tokens": 200
            }
        )
        data = response.json()

        if "choices" in data:
            return data["choices"][0]["message"]["content"]
        elif data.get("status") == "error":
            raise Exception(data.get("message", "Unknown error"))
        else:
            raise Exception(f"Unexpected response: {data}")

    except requests.exceptions.RequestException as e:
        raise Exception(f"Network error: {e}")

try:
    reply = safe_chat("Hello!", "your_api_key")
    print(reply)
except Exception as e:
    print(f"Chat failed: {e}")
```

## Resources

- **API Documentation**: https://docs.modelslab.com/uncensored-chat-api/overview
- **Model Browser**: https://modelslab.com/models
- **Get API Key**: https://modelslab.com/dashboard/api-keys
- **CLI Tool**: https://github.com/ModelsLab/modelslab-cli

## Related Skills

- `modelslab-model-discovery` - Find and filter models
- `modelslab-account-management` - Manage API keys and billing
- `modelslab-image-generation` - Generate images from text
