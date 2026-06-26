---
name: imini-imagegen
description: Use this skill when the user wants to generate raster images through the imini image generation API, including text-to-image and image-guided generation with public image URLs. If the user does not specify a model, ask them to choose between `google/nano-banana`, `google/nano-banana-pro`, and `google/nano-banana-2` before running generation. Do not use it for SVG/icon/front-end drawing work, or when the user is only discussing prompts without asking to actually run image generation.
metadata:
  {
    "openclaw":
      {
        "emoji": "🖼️",
        "homepage": "https://nexuslinelimited-1d434f54.mintlify.app/zh/api-reference/images/nano-banana",
        "requires": { "bins": ["python3"], "env": ["IMINI_IMAGE_API_KEY"] },
        "primaryEnv": "IMINI_IMAGE_API_KEY"
      }
  }
---

# IMINI ImageGen

Generate images through the imini image generation API using a local API key from environment variables. This skill supports text-to-image and image-guided generation with public image URLs, asks the user to choose a model when they did not specify one, then polls the async task until final images are ready and saved into the workspace.

## When To Use

Use this skill when:
- The user wants to generate an image, poster, cover, concept image, or other raster output.
- The user provides a prompt and wants you to actually call the imini API.
- The user provides one or more public image URLs as references for style or content guidance.

Do not use this skill when:
- The user wants SVG, icons, diagrams, or HTML/CSS visuals.
- The task is only to brainstorm or rewrite prompts without actually generating images.
- The only reference input is a local file path; v1 supports public URLs only.

## Configuration

The script reads configuration from environment variables. In OpenClaw, declare `IMINI_IMAGE_API_KEY` in the skill config so the registry and runtime requirements stay aligned.

- `IMINI_IMAGE_API_KEY` (required)
- `IMINI_IMAGE_API_BASE_URL` (optional, default `https://openapi.imini.ai/imini/router`)
- `IMINI_IMAGE_TIMEOUT` (optional, default `300`)
- `IMINI_IMAGE_POLL_INTERVAL` (optional, default `2`)

Do not put real keys into this skill directory, `SKILL.md`, or command arguments. Setup details live in [references/config.md](./references/config.md).

## Workflow

1. Confirm the request is actual image generation, not vector/UI drawing.
2. Collect the prompt.
3. Optionally collect:
   - `model`
   - `aspect_ratio`
   - public image URLs
   - reference mode if the user clearly wants `style` instead of default `asset`
4. If the user did not specify a model, ask before generating:

```text
Which model do you want to use?
1. google/nano-banana: faster and lower cost for standard image generation
2. google/nano-banana-pro: higher quality and higher resolution support
3. google/nano-banana-2: most capable option with more aspect ratios and resolutions

If you are not sure, I recommend starting with google/nano-banana.
```

Do not call the API until the user chooses a model, unless they explicitly ask you to use the default recommendation.

5. Run the bundled script:

```bash
python3 /absolute/path/to/imini-imagegen/scripts/generate_image.py \
  --model google/nano-banana \
  --prompt "A shiba inu wearing a spacesuit and standing on the moon, 3D cartoon style" \
  --aspect-ratio 1:1 \
  --out-dir output/imagegen
```

With references:

```bash
python3 /absolute/path/to/imini-imagegen/scripts/generate_image.py \
  --model google/nano-banana \
  --prompt "Keep the main composition and turn it into a cinematic poster with dramatic lighting" \
  --image-url "https://example.com/ref1.jpg" \
  --reference-type asset \
  --out-dir output/imagegen
```

6. Wait for the script to:
   - submit `POST /v1/images/generate`
   - poll `GET /v1/images/tasks/{task_id}`
   - download final `images[].url` results
7. Report:
   - final saved file paths
   - task status
   - failure reason if the task fails

## Input Rules

- `prompt` is required.
- Supported models:
  - `google/nano-banana`
  - `google/nano-banana-pro`
  - `google/nano-banana-2`
- If the user did not specify a model, ask them to choose before generating.
- If the user asks for a recommendation, prefer `google/nano-banana` as the default low-friction option.
- `resolution` defaults to `1K`. Higher values should only be used when the chosen model supports them.
- `aspect_ratio` is optional. Allowed values are documented in [references/api.md](./references/api.md).
- `--image-url` count limits depend on the chosen model.
- v1 accepts only public image URLs for references.
- `reference_type` defaults to `asset`; use `style` only when the user clearly wants style transfer behavior.

## Failure Handling

If generation fails, check in this order:

1. `IMINI_IMAGE_API_KEY` is present.
2. The API returned auth or validation errors.
3. Reference URLs are public and reachable.
4. The task status changed to `failed`.
5. The task timed out before completion.
6. The task succeeded but `images` was empty or downloads failed.

For API shapes, status values, and exact request fields, read [references/api.md](./references/api.md).
