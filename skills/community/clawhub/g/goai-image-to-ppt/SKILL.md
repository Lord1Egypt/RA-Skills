---
name: goai-image-to-ppt
description: Convert images to PowerPoint presentations via GoAI API. Use when the user asks to convert images to PPT, turn screenshots into slides, make a presentation from images, or needs to call the image-to-PPT conversion API, including Chinese requests like 图片转PPT, 图片生成PPT, 把图片转换成PPT, and 将图片转换为PPT.
version: 0.3.0
homepage: https://mustgoai.com
metadata: { "openclaw": { "emoji": "🖼", "os": ["darwin", "linux", "win32"], "requires": { "bins": ["uv"], "env": ["GOAI_API_KEY"] }, "primaryEnv": "GOAI_API_KEY" } }
---

# When To Use

Use this skill when the user wants to convert images to a PowerPoint presentation, especially for prompts like 图片转PPT, 图片生成PPT, 把图片转换成PPT, and 将图片转换为PPT.

If the user provides local image files, the script uploads them first and sends the resulting URLs. If the user provides remote URLs, the script passes them through unchanged.

# Default Behavior

This package currently targets the production PPT service at `https://ppt.mustgoai.com`. Override `GOAI_BASE_URL` only when you intentionally need a different endpoint.

This skill now uses a single cross-platform Python entrypoint through `uv`. Treat `uv` as the only runtime dependency the user needs to install manually. On first run, `uv` may create a local environment, install `httpx`, and download Python if the machine does not already have a usable interpreter. That first-run setup is expected and should not be described as an error.

# Script Rules

Always use the Python entrypoint through `uv`:

```bash
uv run --project . python scripts/convert_images_to_ppt.py \
  --image "..." \
  [--image "..."] \
  [--language "zh"] \
  [--aspect-ratio "16:9"]
```

The Python path validates `GOAI_API_KEY`, defaults to `https://ppt.mustgoai.com` unless `GOAI_BASE_URL` is set, and treats `401`, `402`, `429`, missing `jobId`, missing `downloadUrl`, task failure, and task timeout as hard failures. Polling follows the web client behavior: it checks every 5 seconds, retries transient polling errors, and waits for a backend terminal status instead of enforcing a client-side timeout.

The Python entrypoint self-heals into `uv run` if it is accidentally invoked as `python scripts/convert_images_to_ppt.py ...` or `python3 scripts/convert_images_to_ppt.py ...`. Do not try to repair the system Python environment for this skill.

When invoking this skill through OpenClaw's `exec` tool, always use `timeout=600` to allow up to 10 minutes for long-running conversions. Do not describe the run as timed out or killed unless the script itself exits non-zero or the backend reports a terminal failure state.

If `uv` is missing, explicitly guide the user to install it first:

- macOS: `brew install uv`
- Windows: `winget install astral-sh.uv`

After `uv` is installed, rerun the same command. Do not ask the user to install Python packages by hand; `uv` is responsible for preparing Python and the skill dependencies.

If execution reports a missing Python module such as `httpx`, do not run `pip install`, `pip install --user`, or `pip install --break-system-packages`. Re-run the skill through `uv`; the dependency set comes only from `pyproject.toml` and `uv.lock`.

If `GOAI_API_KEY` is missing, explicitly guide the user to visit `https://mustgoai.com`, register or log in, open `Settings -> API Key`, create a key, and then configure the skill env in `~/.openclaw/openclaw.json`.

# Credits Refund

If the task fails (conversion error, timeout, or backend failure), credits are automatically refunded to the user's account. There are two refund mechanisms:

1. **Immediate refund**: the backend detects failure during task execution and calls refund immediately.
2. **Compensation refund**: a background worker (`CreditsRefundWorker`) scans failed tasks every 2 minutes and refunds any tasks that were not refunded immediately.

The user does not need to manually request a refund. On failure, inform the user that credits have been or will be refunded automatically.

# Insufficient Credits

If the error message contains "insufficient credits" (积分不足), the script outputs a demo PPT URL and exits with code 42. In that case, tell the user:

> 我们导出的PPT效果如下：https://ai-neuralforge.oss-cn-hangzhou.aliyuncs.com/aippt/ppt/example_ppt/demo.pptx

Do not describe this as a failure; present the demo URL as a preview of the expected output quality.

# Output Contract

On success, print all four lines below in this order:

- `MEDIA:/absolute/path/to/generated-file`
- `MEDIA_URL:https://...`
- `RESULT_PATH:/absolute/path/to/generated-file`
- `RESULT_URL:https://...`

When responding to the user after a successful run, always include both the exact local file path and the exact public URL in plain text, even if OpenClaw already rendered or read the local media file. Do not omit the URL just because the preview succeeded. On failure, exit non-zero and print a concise error message. Do not inline the binary output back into the conversation.
