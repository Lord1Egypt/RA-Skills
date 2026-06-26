---
name: hidream-aigc-skills
description: >-
  OpenClaw AIGC models (video + image) client. 
  **REQUIRES CREDENTIALS**: You must set `HIDREAM_AUTHORIZATION` environment variable or use `scripts/configure.py` to save a token. 
  **FILE ACCESS**: Reads local image/video files provided as arguments for base64 encoding.
  **NETWORK**: Sends requests to `https://vivago.ai`.
dependencies:
  - requests
requires:
  env:
    - HIDREAM_AUTHORIZATION
---

# HD AIGC Skills

This skill provides per-model scripts that validate parameters and call shared request runners.

## Security Disclosure (AI Agents)

- **Credential Access**: This skill reads `HIDREAM_AUTHORIZATION` from environment variables or a secure local config file (`~/.config/openclaw/hidream_config.json`, permission 0600).
- **File System Access**: Scripts read local image/video files provided in arguments to base64 encode them for API transmission. No other file system access occurs.
- **Network Activity**: Requests are sent exclusively to the configured `HIDREAM_ENDPOINT` (default: `https://vivago.ai`).

## Configuration & Usage (AI Agent Instructions)

When a user wants to use this skill, follow these steps:

1.  **Check for Token**: The system automatically checks for the API key in the following order:
    *   Local Env File (Primary): `~/.openclaw/.env` (reads `HIDREAM_AUTHORIZATION=sk-...`)
    *   Environment Variable: `HIDREAM_AUTHORIZATION`
    *   Config File: `~/.config/openclaw/hidream_config.json`

2.  **Request Token (If Missing or 401)**: Instruct the user to update their credentials:
    *   **Recommended**: Provide their API Key (starts with `sk-`) and ask the agent to save it: `echo "HIDREAM_AUTHORIZATION=sk-..." > ~/.openclaw/.env`
    *   **Interactive**: Run `python3 scripts/configure.py` to interactively save the token.
3.  **Handle Missing Prompts**: If the user asks to generate an image or video but does not provide a specific prompt, **DO NOT generate a random test image**. Instead, politely ask the user what they would like to generate.
4.  **Generate**: Use the Python interface to generate content based on user requests.
5.  **Save Output**: When generation is complete and returns a media URL (image or video), **ALWAYS download and save the file to the `assets/` directory within this skill's folder (e.g., `assets/generated_image.png`)**. Do NOT use `~/.openclaw/workspace/output/` as it may have permission issues. Create the `assets/` directory if it does not exist.
6.  **Present Results**: When showing generated images or videos to the user, **ALWAYS** use the following Markdown formats to ensure proper rendering in the Claw interface. Use the local path if downloaded, or the remote URL:

### Error Handling & Troubleshooting

- **Resolution too small (ValueError)**: Seedream M2 requires high resolution (at least `2560*1440` or `2048*2048`). If you get this error, increase the `resolution` parameter.
- **401 Unauthorized (invalid token)**: The token is invalid or expired. Update it by writing the new token to `~/.openclaw/.env`:
    ```bash
    echo "HIDREAM_AUTHORIZATION=sk-..." > ~/.openclaw/.env
    ```
- **Insufficient Credits (Code 2007)**: Instruct the user to go to `https://vivago.ai/platform/info` to recharge credits.


## Python Interface (Recommended)

You can call the scripts directly from Python code. This is the preferred way for AI agents to interact.

### Image Generation (Seedream)

```python
from scripts.seedream import run as run_seedream

# Example: Generate an image
try:
    result = run_seedream(
        version="M2",
        prompt="A cyberpunk cat on the moon",
        resolution="2048*2048",
        authorization="sk-..." # Optional if env var is set
    )
    print(result)
except Exception as e:
    print(f"Error: {e}")
```

### Video Generation (Kling)

```python
from scripts.kling import run as run_kling

# Example: Generate a video
try:
    result = run_kling(
        version="Q2.5T-std",
        prompt="A cyberpunk cat running on neon streets",
        duration=5,
        authorization="sk-..." # Optional if env var is set
    )
    print(result)
except Exception as e:
    print(f"Error: {e}")
```

## Structure

- `scripts/commom/base_image.py`: shared OpenClaw image request runner
- `scripts/common/base_video.py`: shared OpenClaw video request runner
- `scripts/common/task_client.py`: http request runner
- `scripts/*.py`: per-model scripts (parameter parsing + payload only)

## Auth and Endpoints

Set one of the following environment variables, or use `scripts/configure.py`:

- `HIDREAM_AUTHORIZATION`: Bearer token value only
- `HIDREAM_ENDPOINT`: API Endpoint (default: `https://vivago.ai`)
- `OPENCLAW_AUTHORIZATION` (Legacy): Alternative for `HIDREAM_AUTHORIZATION`
- `OPENCLAW_ENDPOINT` (Legacy): Alternative for `HIDREAM_ENDPOINT`

## Dependencies

- `requests` (Python library) - see `requirements.txt`

## Video Model Scripts

- `scripts/sora_2_pro.py`
- `scripts/seedance_1_0_pro.py`
- `scripts/seedance_1_5_pro.py`
- `scripts/minimax_hailuo_02.py`
- `scripts/kling.py` (Refactored for Python access)

## Image Model Scripts

- `scripts/seedream.py` (Refactored for Python access)
- `scripts/nano_banana.py`

## Notes

- Per-model scripts only handle parameter parsing and payload building.
- Base scripts handle request submission, polling, and auth.
