---
name: comfyui-safe-connector
description: Safe ComfyUI image generation. Use saved or ad-hoc server profiles, paste/upload raw workflow JSON, submit, poll, and serve downloaded outputs locally.
metadata: {"openclaw":{"emoji":"🖼️","requires":{"anyBins":["python3"]},"primaryEnv":"COMFYUI_API_KEY","skillKey":"comfyui-safe-connector"}}
user-invocable: true
allowed-tools: exec read
---

# ComfyUI Safe Connector

Small safe runner for ComfyUI.

## What it does
- Connects to a remembered server profile or ad-hoc connection settings
- Accepts a workflow as a pasted JSON string, uploaded file, stdin, or built-in template
- Submits the workflow to ComfyUI
- Polls until done and downloads **all** output images
- Saves images under `generated/`
- Returns downloaded file paths and browser view URLs for each output

## Workflow keywords
Saved workflows can include keywords in their `.meta.json`. Use the keyword, not the prompt, to pick the right template.

Examples:
- `IL-Ikastrious` → `anime`, `cartoon`, `illustration`, `ikastrious`
- use for anime/cartoon image requests

## Main command
Run from the skill root:

```bash
./comfy.sh --health
./comfy.sh --list-profiles
./comfy.sh --save-profile home --base-url http://127.0.0.1 --port 8188
./comfy.sh --gen --workflow-file /path/to/workflow.json
./comfy.sh --gen --workflow-stdin < workflow.json
./comfy.sh --gen --workflow-json '{...json...}'
./comfy.sh --poll <prompt_id>
./comfy.sh --watch <prompt_id>
```

`comfy.sh` is the supported entrypoint (instead of calling the Python runner directly).

## Server profiles
Profiles live in:

`~/.config/openclaw/comfyui-runner.json`

Supported fields:
- `servers` (list of server entries)
- `base_url`
- `port`
- `api_key`
- `username`
- `password`
- `default_server`
- `default_workflow`

Use:
- `--profile NAME` to use one for this run
- `--save-profile NAME` to remember the current connection
- `--set-profile NAME` to make a saved profile active
- `--set-default-server NAME` to set the default server
- `--set-default-workflow NAME` to set the default workflow
- `--delete-profile NAME` to remove one

Env vars override saved profiles:
- `COMFYUI_PROFILE`
- `COMFYUI_BASE_URL`
- `COMFYUI_PORT`
- `COMFYUI_API_KEY`
- `COMFYUI_USERNAME`
- `COMFYUI_PASSWORD`

## Workflow input
Preferred for this skill:
- `--workflow-file` for uploaded JSON files
- `--workflow-stdin` for pasted JSON
- `--workflow-json` for direct JSON strings

Built-in templates still work via the positional template id, but raw JSON is the default safe path.
If a keyword matches exactly one saved workflow, you can pass the keyword instead of the template id.

## Output
- `poll` / `watch` write downloaded files to `generated/`
- return JSON includes `view_url`, `local_path`, and `outputs[]`
- image files can be sent directly into Discord or another channel if you want delivery there
- server profiles are remembered in `~/.config/openclaw/comfyui-runner.json`

## Safety
- No shell interpolation of workflow contents
- JSON is parsed, not executed
- API key support is optional
- Use only trusted ComfyUI servers
