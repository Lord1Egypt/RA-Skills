---
name: lemonade-server-manager
description: Manage Lemonade Servers natively. Use when checking system info, health status, listing available models, pulling or loading new models, completing LLM chats, or generating stable-diffusion images on a local or remote AI NPU/GPU cluster.
metadata: {"homepage":"https://github.com/james-martinez/lemonade-server-manager","clawdbot":{"emoji":"🍋","requires":{"anyBins":["curl"]},"os":["linux","darwin","win32"]}}
env:
  - name: LEMONADE_API_KEY
    description: Optional API key for authenticating with Lemonade servers.
    required: false
---

# Lemonade Server Management

Interact with and manage local or remote Lemonade AI Server hardware directly via standard native network requests (`curl`).

## When to Use

- Checking local GPU/NPU health and currently loaded VRAM resources
- Listing available, downloaded text/image models on a Lemonade cluster
- Pulling, loading, or unloading multimodal models
- Generating text from LLMs (chat completions)
- Generating stable-diffusion image responses

## Setup Instructions

1. Every endpoint requires a base `server_url`. If one is not specified by the user, assume `http://localhost:8000`.
2. Use the `LEMONADE_API_KEY` environment variable to authenticate.
3. This skill stays focused on making HTTP requests to a base `server_url` (default `http://localhost:8000`) and using an optional `LEMONADE_API_KEY`. It does not instruct reading arbitrary host files or other env vars.
4. **Operational note:** The skill will transmit prompts and model requests to whichever `server_url` is used. If a remote URL is supplied, the agent will send user content and model commands there (expected for this skill, but worth the user's attention).

## API Operations

### System Info

Get hardware capabilities and device enumeration limits.

**Returns:** JSON object with hardware capabilities.

```bash
# Example Request
curl -X GET "http://localhost:8000/api/v1/system-info" \
  -H "Authorization: Bearer ${LEMONADE_API_KEY}"
```

### Health Check

Verify status and monitor currently loaded models to prevent VRAM overflow.

**Returns:** JSON object containing server status and currently loaded models.

```bash
# Example Request
curl -X GET "http://localhost:8000/api/v1/health" \
  -H "Authorization: Bearer ${LEMONADE_API_KEY}"
```

### List Models

Get an array of downloaded models available to load into memory.

**Returns:** JSON list of all downloaded and available models.

```bash
# Example Request
curl -X GET "http://localhost:8000/api/v1/models" \
  -H "Authorization: Bearer ${LEMONADE_API_KEY}"
```

### Pull Model

Download and install a new model string to the target machine.

**Returns:** JSON stream or object confirming download status.

```bash
# Example Request
curl -X POST "http://localhost:8000/api/v1/pull" \
  -H "Authorization: Bearer ${LEMONADE_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{"model": "llama3"}'
```

### Load Model

Load a model into VRAM/NPU to prepare for prompt responses.

**Returns:** JSON object confirming model loaded into memory.

```bash
# Example Request
curl -X POST "http://localhost:8000/api/v1/load" \
  -H "Authorization: Bearer ${LEMONADE_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{"model": "llama3"}'
```

### Unload Model

Force unload a model to free up memory before loading a larger variant.

**Returns:** JSON object confirming model unloaded.

```bash
# Example Request
curl -X POST "http://localhost:8000/api/v1/unload" \
  -H "Authorization: Bearer ${LEMONADE_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{"model": "llama3"}'
```

### Chat Completion

Send a standard chat request to the LLM backend.

**Returns:** JSON object containing standard chat completion response.

```bash
# Example Request
curl -X POST "http://localhost:8000/api/v1/chat/completions" \
  -H "Authorization: Bearer ${LEMONADE_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "llama3",
    "messages": [
      {"role": "user", "content": "Hello, world!"}
    ]
  }'
```

### Generate Image

Submit a stable-diffusion prompt for image generation.

**Returns:** JSON object containing base64 generated image data.

```bash
# Example Request
curl -X POST "http://localhost:8000/api/v1/images/generations" \
  -H "Authorization: Bearer ${LEMONADE_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "sdxl",
    "prompt": "A majestic lion standing on a cliff, digital art"
  }'
```

## Tips

- The `flm`, `ryzenai-llm`, and `whispercpp` backends are mutually exclusive on an NPU. Always use the `/api/v1/unload` endpoint on conflicting LLMs before attempting to load a Whisper model on an NPU.
- Check `/api/v1/health` first to assess available hardware VRAM before pulling or loading a multi-gigabyte LLM to avoid out-of-memory errors on the host.
- Provide clear feedback to the user if an API request fails due to resource constraints and suggest unloading inactive background models.
