---
name: goai-ppt-gen
description: Generate PowerPoint presentations via GoAI API. Use when the user asks to create, generate, make, or build PPT, slides, presentations, including Chinese requests like 生成PPT, 生成PPT, 做PPT, 做演示文稿, 生成幻灯片, and 文案生成PPT.
version: 1.1.0
homepage: http://mustgoai.com
metadata: { "openclaw": { "emoji": "📊", "os": ["darwin", "linux", "win32"], "requires": { "anyBins": ["bash", "pwsh", "powershell"], "env": ["GOAI_API_KEY"] }, "primaryEnv": "GOAI_API_KEY" } }
---

# When To Use

Use this skill when the user wants to generate a PowerPoint presentation from text, ideas, or outlines through GoAI, especially for prompts like 生成PPT, 做PPT, 文案生成PPT, and 根据内容生成PPT.

Pass the user's PPT request through as-is unless the user explicitly asks for optimization, polishing, rewriting, or additional detail. Do not silently embellish short prompts.

**OpenClaw Attachment Support**: When the user drags and drops images or PDF files into the OpenClaw chat, the script will automatically use them as reference content. Images become `reference_images`, and PDFs become `reference_content`. No need to manually specify `--reference` or `--reference-content` if attachments are present.

# Default Behavior

This package targets the shared PPT service at `https://ppt.mustgoai.com` for API requests. The API key is sourced from `http://mustgoai.com` — visit the site, register or log in, open `Settings -> API Key`, create a key, and then configure `GOAI_API_KEY`. Override `GOAI_BASE_URL` only when you intentionally need a different endpoint.

On Windows, prefer `scripts/generate_ppt.ps1`. The Windows path uses built-in PowerShell HTTP and JSON support. On macOS and Linux, prefer `scripts/generate_ppt.sh` and make sure `bash`, `curl`, and `jq` are available.

If the user provides local reference images, the script uploads them first and sends the resulting URLs as `reference_images`. If the user provides remote URLs, the script passes them through unchanged.

# Script Rules

Use the script that matches the host OS.

macOS / Linux:

```bash
bash scripts/generate_ppt.sh \
  --idea "..." \
  [--language "zh"] \
  [--num-pages "10"] \
  [--reference "/path/to/image.png"] \
  [--reference "https://example.com/image.png"] \
  [--reference-content "..."] \
  [--aspect-ratio "16:9"] \
  [--resolution "2K"]
```

Windows PowerShell:

```powershell
powershell -ExecutionPolicy Bypass -File scripts\generate_ppt.ps1 `
  -idea "..." `
  [-language "zh"] `
  [-numPages "10"] `
  [-reference "C:\path\to\image.png"] `
  [-reference "https://example.com/image.png"] `
  [-referenceContent "..."] `
  [-aspectRatio "16:9"] `
  [-resolution "2K"]
```

The PowerShell path uses built-in JSON and HTTP support. The bash path requires `curl` and `jq`. Both scripts validate `GOAI_API_KEY`, default to `https://ppt.mustgoai.com` unless `GOAI_BASE_URL` is set, and treat `401`, `402`, `429`, missing `task_id`, missing `download_url`, task failure, and task timeout as hard failures. For transient transport or server errors, each individual HTTP request is attempted at most 3 times.

If `GOAI_API_KEY` is missing, guide the user to visit `http://mustgoai.com`, register or log in, open `Settings -> API Key`, create a key, and configure `GOAI_API_KEY` as an environment variable or in `~/.openclaw/openclaw.json`. API requests still go to `https://ppt.mustgoai.com`. If the bash path fails before the request is sent, the user should install the missing shell dependency and retry.

**Demo PPT**: You can preview the generation effect by clicking this demo PPT: https://ai-neuralforge.oss-cn-hangzhou.aliyuncs.com/aippt/ppt/example_ppt/%E7%94%9F%E6%88%90%E4%B8%80%E4%BB%BD%E4%BB%A5%E4%B8%AD%E5%9B%BD%E4%BA%8C%E5%8D%81%E5%9B%9B%E8%8A%82%E6%B0%94%E4%B8%BA%E4%B8%BB%E9%A2%98%E7%9A%84%E7%A7%91%E6%99%AE%E6%BC%94%E7%A4%BA%E6%96%87%E7%A8%BF%E5%86%85%E5%AE%B9%E9%9C%80%E6%B6%B5%E7%9B%96%E4%BA%8C%E5%8D%81%E5%9B%9B%E8%8A%82%E6%B0%94%E7%9A%84%E5%8E%86%E5%8F%B2%E6%B8%8A%E6%BA%90%E5%A4%A9%E6%96%87%E5%88%92%E5%88%86%E6%A0%87%E5%87%86%E4%BB%A5%E5%8F%8A%E5%9B%9B.pptx

# Output Contract

On success, save the generated PPT to a local absolute path, automatically open that local PPT for the user, and print `MEDIA:/absolute/path/to/generated-file` plus `MEDIA_URL:https://...` on separate lines. On failure, exit non-zero and print a concise error message. Do not inline the binary output back into the conversation.
