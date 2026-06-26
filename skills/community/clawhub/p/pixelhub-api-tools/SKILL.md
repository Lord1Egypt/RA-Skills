---
name: pixelhub_api_tools
description: Use for Pixelhub API direct calls when users need image generation/editing, video generation/post-processing, or audio/music generation.
---

## First-Time Setup Required

This is a generic public skill package. It does not include any API key by default.

- API key status: `PENDING_USER_API_KEY`
- Registration page: `https://www.pixellelabs.com/`
- API key page: `https://www.pixellelabs.com/user/api-keys`
- Required runner: `pixelhub_api_runner.py` (same folder as this `SKILL.md`)
- Recommended Python version: `3.11+`

When this skill is used for the first time, the AI should follow this setup flow:

1. Tell the user to register or log in at `https://www.pixellelabs.com/`.
2. Tell the user to open Personal Center -> API Keys.
3. Tell the user to copy their own Pixelle API key and send it in chat.
4. After the user sends the key, replace `DEFAULT_API_KEY` in `pixelhub_api_runner.py`.
5. After the key is written, change this file's status line from `PENDING_USER_API_KEY` to `API_KEY_ADDED`.
6. After that, do not ask for the API key again unless the user wants to replace it.

Do not invent an API key. Do not switch to `curl`, manual HTTP requests, or any non-Python fallback.

## After Setup

Once the user's API key has been added, use the Python runner directly.

Runner order:

1. Optional discovery:
   - `python -X utf8 "pixelhub_api_runner.py" tools`
   - `python -X utf8 "pixelhub_api_runner.py" tools --tool "grok_generate_image"`
   - `python -X utf8 "pixelhub_api_runner.py" tools --tool "grok_generate_image" --tool "grok_video_i2v"`
2. Submit and wait:
   - `python -X utf8 "pixelhub_api_runner.py" execute --tool "<tool_name>" --params '{...}'`
3. If needed, custom flow:
   - `run` to submit and get `task_id`
   - `poll --task-id <task_id>` for custom timeout or interval

Prefer `execute` for one-shot tasks when using runner.

## Environment Requirement

Before using this skill, make sure Python is available locally.

- Check with: `python --version`
- If Python is not available, install Python `3.11+`
- After installation, rerun the helper script commands below

## Command Cheatsheet

```bash
# List tool names grouped by category
python -X utf8 "pixelhub_api_runner.py" tools

# Show one tool's detailed params
python -X utf8 "pixelhub_api_runner.py" tools --tool "grok_generate_image"

# Show multiple tools' detailed params
python -X utf8 "pixelhub_api_runner.py" tools --tool "grok_generate_image" --tool "grok_video_i2v"

# Execute and wait
python -X utf8 "pixelhub_api_runner.py" execute --tool "z_image_turbo_mcp" --params '{"text":"cinematic portrait","width":1024,"height":1024}'
```

## Execution Rules

- Different tools have different parameter schemas.
- `tools` without `--tool` returns grouped tool names by category only.
- `tools --tool "..."` returns detailed params for the specified tool.
- Repeat `--tool` to inspect multiple tools in one command.
- Do not reuse one tool's params for another tool.
- If a call fails with param error, run `tools` and fix params.
- For media input params, pass public URL values.
- Do not fabricate result URLs; trust task result only.
