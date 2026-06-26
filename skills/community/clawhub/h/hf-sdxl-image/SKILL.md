---
name: hf-sdxl-image
description: Generate an image from a text prompt through the Hugging Face Inference API using stabilityai/stable-diffusion-xl-base-1.0 and the HUGGINGFACE_TOKEN environment variable. Use when the user asks to generate, draw, create, make, or render an image or illustration from text, especially when they mention Hugging Face, SDXL, or Stable Diffusion XL. Save the generated image to a temporary local path, let OpenClaw send it to the current conversation window, and remove the temporary file after successful delivery unless the user explicitly asks to keep a saved copy.
---

# HF SDXL Image

Generate a single image from a text prompt with the Hugging Face router endpoint. The skill defaults to stabilityai/stable-diffusion-xl-base-1.0 and can be switched to another compatible Hugging Face Inference API model by setting HF_IMAGE_MODEL.

## Chat-oriented workflow

When you ask to generate an image:

1. Convert your request into a prompt.
2. Run `scripts/generate_hf_sdxl.py` with the `--output /tmp/openclaw/` argument.
3. The script saves the image to a temporary path and prints the file path to stdout.
4. Send the image back through the **current conversation provider's required image/file-send format**.
5. After successful delivery, delete the temporary file unless the user explicitly asked to keep it.

## Provider-specific delivery rule

This skill only generates and saves an image file. **It does not define a universal send format.**

When returning the image in chat, always follow the **current session provider's required outbound media format**. Different providers may require different delivery methods, wrappers, or tools. Do **not** assume that simply reading a local file path, pasting a path, or relying on one provider's auto-routing behavior will work on another provider.

Required behavior:

- Detect the current session provider/channel before sending.
- Use that provider's correct media-send path and syntax.
- If the provider requires a provider-specific wrapper or message format for images, use it.
- If the provider does not reliably auto-send images from a local file read, do not rely on that fallback.
- Treat image delivery as provider-specific, not skill-generic.

Examples of what to avoid:

- Do not assume `read` on an image path will always send the image correctly.
- Do not assume Telegram-style or QQ-style delivery rules apply to other providers.
- Do not claim success until the image has actually been sent through the current provider's proper format.

## Strong trigger examples

Use this skill for requests like:

- "生成一张图片：夕阳下的海边小镇"
- "画一张赛博朋克风格的城市夜景"
- "帮我做一张封面图，主题是 AI 和机器人"
- "用 Hugging Face 生成一张可爱的熊在图书馆读书"
- "用 SDXL 出一张未来感海报"
- "create an illustration of a scholar bear reading in a grand library"

## Command

Default delivery workflow:

python3 scripts/generate_hf_sdxl.py "a cozy cyberpunk alley at night, cinematic lighting" --wait-for-model --output /tmp/openclaw/

With a model override:

HF_IMAGE_MODEL=stabilityai/stable-diffusion-3-medium-diffusers python3 scripts/generate_hf_sdxl.py "a cozy cyberpunk alley at night, cinematic lighting" --wait-for-model --output /tmp/openclaw/

Use a temporary directory for normal chat delivery. Only point `--output` at a persistent user-chosen location when the user explicitly asks to save or export the image.

## Behavior

- Sends POST https://router.huggingface.co/hf-inference/models/<model-id>
- Reads the bearer token from HUGGINGFACE_TOKEN
- Reads the model id from HF_IMAGE_MODEL when set; otherwise uses stabilityai/stable-diffusion-xl-base-1.0
- Sends JSON with inputs set to the prompt
- Requests image output with a single supported Accept header value
- Requires `--output` and saves the generated image to that path or directory
- Prints the saved file path to stdout so OpenClaw can send the file to the current conversation
- Only generates and stores the image locally; provider-specific outbound delivery must be handled by the caller according to the active chat provider
- Uses a temporary local file as the standard transport step for reliable delivery
- Expects OpenClaw to delete temporary files after a successful send
- Fails loudly when the API returns JSON or an HTTP error

## Parameters

- Positional prompt: image prompt text
- --output: required output file path or directory; use a temporary directory for normal chat delivery, or a persistent location only when the user explicitly requests a saved file
- --timeout: HTTP timeout in seconds; defaults to 180
- --wait-for-model: set options.wait_for_model=true so cold starts wait instead of failing fast

## Troubleshooting

### Missing token

If the script says Missing HUGGINGFACE_TOKEN environment variable., export the token before running it.

export HUGGINGFACE_TOKEN=hf_xxx

### Optional model override

To switch to another compatible Hugging Face Inference API model, set HF_IMAGE_MODEL.

export HF_IMAGE_MODEL=stabilityai/stable-diffusion-3-medium-diffusers

If HF_IMAGE_MODEL is unset, the script uses stabilityai/stable-diffusion-xl-base-1.0.

### 401 or 403

The token is missing, invalid, expired, or does not have permission for the endpoint.

### 503 or model loading errors

Retry with --wait-for-model.

### JSON instead of an image

Read the full JSON error body and surface it to the user. Do not pretend generation succeeded.

### Storage policy

The default policy is temporary-file delivery.

- Generate into a temporary local path for normal chat delivery
- Return the saved file path so OpenClaw can send the file to the current conversation
- Delete the temporary file immediately after successful delivery
- Keep a persistent local copy only when the user explicitly asks for that behavior

## Resource

### scripts/generate_hf_sdxl.py

Use this script for deterministic generation and repeatable testing.
