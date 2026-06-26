---
name: minimax-use
description: "MiniMax AI tools for web search, image analysis, LLM chat, and language translation. Use when you need to search the web, analyze images, generate text with LLMs, or translate between languages."
metadata:
  openclaw:
    requires:
      env:
        - MINIMAX_API_KEY
    primaryEnv: MINIMAX_API_KEY
    os:
      - linux
      - darwin
      - win32
  author: OpenClaw
  version: "0.1.0"
compatibility: Requires Python 3.8+ and the requests library. Requires MINIMAX_API_KEY from https://platform.minimaxi.com
---

# MiniMax Tools

This skill provides access to MiniMax's AI capabilities, including web search, image analysis, LLM conversations, and text translation.

## Setup

First, set up your API key:

```bash
export MINIMAX_API_KEY="your-api-key"
```

To get an API key, sign up at https://platform.minimaxi.com/subscribe/coding-plan

Optionally, you can customize the API endpoint:

```bash
export MINIMAX_API_HOST="https://api.minimaxi.com/anthropic"
```

## CLI Commands

```bash
# Search the web
python -m scripts web_search "your search query"

# Analyze an image
python -m scripts understand_image "what do you see?" /path/to/image.jpg

# Chat with an LLM
python -m scripts chat "hello, how are you?"

# Stream chat (receive response in chunks)
python -m scripts stream_chat "tell me a story"

# Translate text
python -m scripts translate "hello world" --to Chinese

# List available models
python -m scripts models
```

## Commands Overview

| Command | What it does |
|---------|---------------|
| `web_search` | Search the web using MiniMax's search API |
| `understand_image` | Analyze images using MiniMax's vision model |
| `chat` | Have a conversation with MiniMax LLMs |
| `stream_chat` | Stream chat with real-time response chunks |
| `translate` | Translate text between languages |
| `models` | Show all available MiniMax models |

### CLI Examples

```bash
# Search the web
python -m scripts web_search "your search query"

# Analyze an image
python -m scripts understand_image "what do you see?" /path/to/image.jpg

# Chat with an LLM
python -m scripts chat "hello, how are you?"

# Stream chat (receive response in chunks)
python -m scripts stream_chat "tell me a story"

# Translate text
python -m scripts translate "hello world" --to Chinese

# List available models
python -m scripts models
```

## Using in Python

### Web Search

```python
from scripts import web_search

result = web_search("Python best practices", count=10)
print(result)
```

### Image Analysis

```python
from scripts import understand_image

# From a local file
result = understand_image("What's in this image?", "/path/to/image.png")

# From a URL
result = understand_image("Describe this image", "https://example.com/image.jpg")
```

### LLM Chat

```python
from scripts import chat

result = chat(
    message="Hello, introduce yourself",
    system="You are a helpful AI assistant",
    model="MiniMax-M2.7",
    temperature=1.0,
    max_tokens=4096,
    stream=False,
    history=[
        {"role": "user", "content": "Hi"},
        {"role": "assistant", "content": "Hello! How can I help you?"}
    ]
)
```

**Parameters:**
- `message` (str): User message
- `system` (str, optional): System prompt
- `model` (str, default: "MiniMax-M2.7"): Model name
- `temperature` (float, default: 1.0): Temperature parameter, range (0.0, 1.0]
- `max_tokens` (int, default: 4096): Max tokens to generate
- `stream` (bool, default: False): Enable streaming response
- `history` (list, optional): History list for multi-turn conversation, each message `{"role": "user"/"assistant", "content": "..."}`

### Streaming Chat

```python
from scripts import stream_chat

result = stream_chat(
    message="Tell me a short story",
    system="You are a storyteller",
    model="MiniMax-M2.7",
    temperature=1.0,
    max_tokens=500
)

# Access streaming chunks
if result["success"]:
    chunks = result["result"]["chunks"]
    full_content = result["result"]["content"]
    print(f"Total chunks: {len(chunks)}")
    print(f"Full content: {full_content}")
```

### Translation

```python
from scripts import translate

result = translate(
    text="Hello World",
    target_lang="Chinese",
    source_lang="auto",
    model="MiniMax-M2.7",
    temperature=1.0,
    max_tokens=4096
)
```

**Parameters:**
- `text` (str): Text to translate
- `target_lang` (str, default: "English"): Target language, e.g., "English", "Chinese", "Japanese"
- `source_lang` (str, default: "auto"): Source language, "auto" for auto-detect
- `model` (str, default: "MiniMax-M2.7"): Model name
- `temperature` (float, default: 1.0): Temperature parameter, range (0.0, 1.0]
- `max_tokens` (int, default: 4096): Max tokens to generate

## Response Format

All functions return a consistent response format:

**Success:**
```json
{
  "success": true,
  "result": {...}
}
```

**Error:**
```json
{
  "success": false,
  "error": "error message"
}
```

## Learn More

- Full API documentation: [references/API.md](references/API.md)
- Available models: [assets/models.json](assets/models.json)
