---
name: goai-video-gen
description: Generate AI videos via GoAI API. Use when the user asks to create, generate, render, or make videos, animations, clips, shorts, or motion content, including Chinese requests like 生成视频, 生成一段视频, 做视频, 出视频, 做个动画, 文生视频, and 图生视频.
version: 0.3.0
homepage: https://mustgoai.com
metadata: { "openclaw": { "emoji": "🎬", "os": ["darwin", "linux", "win32"], "requires": { "bins": ["uv"], "env": ["GOAI_API_KEY"] }, "primaryEnv": "GOAI_API_KEY" } }
---

# When To Use

Use this skill when the user wants text-to-video or image-to-video generation through GoAI, especially for prompts like 生成视频, 做视频, 出视频, 文生视频, 图生视频, and 做个动画.

Pass the user's video prompt through as-is unless the user explicitly asks for prompt optimization, prompt polishing, rewriting, translation, or additional creative detail. Do not silently embellish short prompts.

Do not translate the user's prompt to another language. If the user writes in Chinese, pass Chinese to `--prompt`. If the user writes in English, pass English to `--prompt`. You may strip only lightweight request wrappers such as `帮我`, `给我`, `请`, `生成`, or `做个`, but do not rewrite the core prompt content.

Examples:

- User: `给我生成一段狮子奔跑的视频` -> `--prompt "一段狮子奔跑的视频"` or `--prompt "给我生成一段狮子奔跑的视频"`
- User: `做个海浪视频` -> `--prompt "做个海浪视频"` or `--prompt "海浪视频"`
- Never turn `给我生成一段狮子奔跑的视频` into `a lion running video` unless the user explicitly asks for English translation.

# Default Behavior

This package currently targets the production environment at `https://mustgoai.com`. Override `GOAI_BASE_URL` only when you intentionally need a different endpoint.

This skill now uses a single cross-platform Python entrypoint through `uv`. If the user does not specify a model, the script queries `/api/v1/models/capabilities`, sorts enabled video models by `display.priority`, filters them by the requested `video_mode`, and picks the highest-priority compatible model. When the user omits video parameters, the script derives default aspect ratio, duration, and resolution from the same capability response.

Treat `uv` as the only runtime dependency the user needs to install manually. On first run, `uv` may create a local environment, install `httpx`, and download Python if the machine does not already have a usable interpreter. That first-run setup is expected and should not be described as an error.

If the user provides local image paths, the script uploads them first and sends the resulting URLs as `images`. If the user provides remote URLs, the script passes them through unchanged.

# Script Rules

Always use the Python entrypoint through `uv`:

```bash
uv run --project . python scripts/generate_video.py \
  --prompt "..." \
  [--model "..."] \
  [--aspect-ratio "..."] \
  [--duration "8"] \
  [--resolution "1080p"] \
  [--video-mode "frames"] \
  [--image "/path/to/image.png"] \
  [--image "https://example.com/image.png"]
```

The Python path validates `GOAI_API_KEY`, defaults to `https://mustgoai.com` unless `GOAI_BASE_URL` is set, and treats `401`, `402`, `429`, content blocking, missing `task_id`, missing `video_url`, and backend terminal failure states as hard failures. Polling follows the web client behavior: it checks every 3 seconds, retries transient polling errors, and waits for a backend terminal status instead of enforcing a client-side timeout.

The Python entrypoint self-heals into `uv run` if it is accidentally invoked as `python scripts/generate_video.py ...` or `python3 scripts/generate_video.py ...`. Do not try to repair the system Python environment for this skill.

When invoking this skill through OpenClaw's `exec` tool, always use `timeout=600` to allow up to 10 minutes for long-running video generation. Do not describe the run as timed out or killed unless the script itself exits non-zero or the backend reports a terminal failure state.

If `uv` is missing, explicitly guide the user to install it first:

- macOS: `brew install uv`
- Windows: `winget install astral-sh.uv`

After `uv` is installed, rerun the same command. Do not ask the user to install Python packages by hand; `uv` is responsible for preparing Python and the skill dependencies.

If execution reports a missing Python module such as `httpx`, do not run `pip install`, `pip install --user`, or `pip install --break-system-packages`. Re-run the skill through `uv`; the dependency set comes only from `pyproject.toml` and `uv.lock`.

If `GOAI_API_KEY` is missing, explicitly guide the user to visit `https://mustgoai.com`, register or log in, open `Settings -> API Key`, create a key, and then configure the skill env in `~/.openclaw/openclaw.json`.

# Output Contract

On success, print all four lines below in this order:

- `MEDIA:/absolute/path/to/generated-file`
- `MEDIA_URL:https://...`
- `RESULT_PATH:/absolute/path/to/generated-file`
- `RESULT_URL:https://...`

When responding to the user after a successful run, always include both the exact local file path and the exact public URL in plain text, even if OpenClaw already rendered or read the local media file. Do not omit the URL just because the media preview succeeded. On failure, exit non-zero and print a concise error message. Do not inline the binary output back into the conversation.
