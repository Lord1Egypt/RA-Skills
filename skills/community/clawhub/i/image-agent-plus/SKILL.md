---
name: image-agent-plus
description: "Use image-agent-plus CLI to generate images, prioritizing image2 for high-quality text and prompt-following, with Codex/Gemini fallback."
version: 2.0.5
license: Apache-2.0
homepage: https://github.com/webkubor/image-agent-plus
store: https://clawhub.ai/webkubor/image-agent-plus
author: webkubor
compatibility:
  platforms:
    - codex
    - openclaw
    - hermes
metadata:
  openclaw:
    emoji: "🎨"
    requires:
      bins: ["node"]
    install:
      - id: node-brew
        kind: brew
        formula: node
        bins: ["node"]
        label: "Install Node.js (brew)"
---

# image-agent-plus

Direct CLI invocation. No HTTP server required.

![AI 时代，我们应该沉淀下来的是什么](https://raw.githubusercontent.com/webkubor/image-agent-plus/main/skills/image-agent-plus/assets/ai-era-editorial-poster.png)

## Showcase

The image above was generated locally from this prompt:

```text
AI 时代，我们应该沉淀下来的是什么，中文社论海报
```

It is included as a ClawHub store preview so users can see the intended output style before installing the skill.

## What Went Wrong During Setup

We first tried to treat Codex image generation like a normal nested CLI provider. That was wrong.

The working Codex flow is:

1. Generate the image inside the active Codex session.
2. Codex saves the result under `~/.codex/generated_images/<session>/ig_*.png`.
3. Run `image-agent-plus collect-codex` to copy the latest generated image into your chosen output path.

Do not rely on nested `codex exec` for image generation. It can hang or fail because the interactive Codex image tool event is not the same as a normal non-interactive shell command.

## Runtime Rule

Before asking for an API key, run:

```bash
image-agent-plus check
```

If an OpenAI API key (`IMAGE_AGENT_OPENAI_API_KEY` or `OPENAI_API_KEY`) is set, the tool defaults to image2. If Codex CLI or Gemini CLI is installed (no OpenAI key), use those without API keys. API keys are only for direct provider API mode or for machines without local runtimes.

## Quick Start

```bash
image-agent-plus generate \
  --prompt "一只橘猫坐在雨天窗台上，电影感光线" \
  --aspect-ratio "16:9"
```

## Common Commands

```bash
image-agent-plus check

# Default: image2 via OpenAI (when API key available)
image-agent-plus generate \
  --prompt "AI 时代，我们应该沉淀下来的是什么，中文社论海报" \
  --aspect-ratio "16:9"

# Fallback: Codex CLI (no API key needed)
image-agent-plus generate \
  --prompt "AI 时代，我们应该沉淀下来的是什么，中文社论海报" \
  --provider codex \
  --aspect-ratio "16:9"
```

For Codex image generation, use the active Codex image tool first. After Codex reports `Generated Image` and saves under `~/.codex/generated_images`, run:

```bash
image-agent-plus collect-codex
```

## Options

| Flag | Description |
|------|-------------|
| `--prompt` | Image description, required |
| `--provider` | `openai`, `codex`, or `gemini` |
| `--filename` | Output file path. If omitted, save to `~/Desktop/image-agent-plus-output/` |
| `--aspect-ratio` | `16:9`, `9:16`, `1:1`, `4:3`, `3:4`, `21:9` |
| `--model` | Provider model ID. Do not pass this for default Codex CLI image generation |
| `--output-count` | Number of images, 1-8 |

## Codex Collection

```bash
image-agent-plus collect-codex --filename ~/Desktop/output.png
```

If `--filename` is omitted, the copied image goes to `~/Desktop/image-agent-plus-output/`.

## Environment

Prefer local runtime. For image2 direct API mode, configure the OpenAI key in your normal shell or agent secret manager before running the CLI.

Legacy `NANOBANANA_*` variables are accepted as fallback reads by the CLI.
