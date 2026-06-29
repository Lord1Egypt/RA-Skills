---
name: guishu-gpt-image-2
description: Generate images with Guishu Token gpt-image-2 through the OpenAI-compatible images endpoint. Use when the user wants Guishu gpt-image-2 image generation, an OpenClaw image skill, scripted image creation, local image output, prompt-to-image tests, customer demos, or a gallery of generated images through https://api.llm-token.cn/v1/images/generations.
---

# Guishu GPT Image 2

Generate images through the Guishu Token OpenAI-compatible image endpoint.

## Quick Start

Use the bundled script. It reads the API key from environment variables in this order:

1. `LLM_TOKEN_API_KEY`
2. `GUI_SHU_TOKEN_KEY`
3. `OPENAI_API_KEY`

```bash
export LLM_TOKEN_API_KEY="sk-..."
python3 {baseDir}/scripts/generate.py \
  --prompt "a clean product poster for a blue smart speaker, studio lighting" \
  --size 1024x1024 \
  --quality high \
  --n 1
```

The default endpoint is:

```text
https://api.llm-token.cn/v1/images/generations
```

The default model is:

```text
gpt-image-2
```

## Workflow

1. Read `references/gpt-image-2-api.md` when you need endpoint details, supported request fields, timeout guidance, or customer-facing setup notes.
2. Prepare one specific image prompt. Keep prompts concrete about subject, style, composition, camera, lighting, color, and output use.
3. Run `scripts/generate.py`. Prefer `--response-format b64_json` so the script can save files locally without depending on temporary URLs.
4. Inspect the saved output directory. The script writes generated images, `prompts.json`, `request.json`, and `index.html`.
5. If the request times out after a long wait, do not automatically retry. High-resolution requests can take 70-150 seconds and may still be billable upstream.

## Useful Commands

```bash
# Dry-run without sending a billable request.
python3 {baseDir}/scripts/generate.py --prompt "test prompt" --dry-run

# Tall portrait.
python3 {baseDir}/scripts/generate.py \
  --prompt "ultra realistic portrait photo, natural light, shallow depth of field" \
  --size 1024x1792 \
  --quality high

# Multiple prompts from a text file, one prompt per line.
python3 {baseDir}/scripts/generate.py --prompt-file ./prompts.txt --n 1

# Custom endpoint if the gateway changes.
python3 {baseDir}/scripts/generate.py \
  --endpoint https://api.llm-token.cn/v1/images/generations \
  --model gpt-image-2 \
  --prompt "minimal app icon, white background"
```

## Safety and Cost Notes

- Do not print API keys. Prefer environment variables over command-line `--api-key`.
- Avoid blind retries after long timeouts. Ask the user before retrying a request that may already have been processed.
- For casual users, recommend the web UI first: `https://image2.gpt-agent.cc/`.
- For automation or agent workflows, use the script and save local outputs.
