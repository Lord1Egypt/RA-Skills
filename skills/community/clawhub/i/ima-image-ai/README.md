# IMA Image AI

Official runtime for IMA image generation.

Use it for:

- `text_to_image`
- `image_to_image`
- style transfer
- reference-image continuity

## Quick Start

### Minimal Path (3 Steps)

```bash
python3 scripts/ima_runtime_setup.py --install
```

```bash
export IMA_API_KEY="ima_your_key_here"
```

```bash
python3 scripts/ima_runtime_cli.py \
  --task-type text_to_image \
  --prompt "a cinematic mountain sunset" \
  --output-json
```

If you want to verify the environment before the first generation:

```bash
python3 scripts/ima_runtime_doctor.py --output-json
```

### Full Bootstrap Flow

1. Run bootstrap/setup:

```bash
python3 scripts/ima_runtime_setup.py
```

If dependencies are missing, rerun with:

```bash
python3 scripts/ima_runtime_setup.py --install
```

2. Set your API key:

```bash
export IMA_API_KEY="ima_your_key_here"
```

Then rerun setup to verify the local environment:

```bash
python3 scripts/ima_runtime_setup.py
```

3. Run the self-check when you want API/catalog diagnostics:

```bash
python3 scripts/ima_runtime_doctor.py --output-json
```

## Typical First-Use Scenarios

### 1. Inspect Live Models

```bash
python3 scripts/ima_runtime_cli.py --task-type text_to_image --list-models --output-json
```

Use this when you want the current live model IDs before choosing one manually.

### 2. First Prompt-Only Generation

Text to image with the recommended default model picked automatically:

```bash
python3 scripts/ima_runtime_cli.py \
  --task-type text_to_image \
  --prompt "a cinematic mountain sunset" \
  --output-json
```

Use this when you want the fastest path to a first successful run.

If you want to override the model manually without editing placeholders, fetch a live `model_id` first:

```bash
MODEL_ID="$(python3 scripts/ima_runtime_cli.py --task-type text_to_image --list-models --output-json | python3 -c 'import json,sys; print(json.load(sys.stdin)[0][\"model_id\"])')"
python3 scripts/ima_runtime_cli.py \
  --task-type text_to_image \
  --model-id "$MODEL_ID" \
  --prompt "a cinematic mountain sunset" \
  --output-json
```

For `image_to_image`, the same pattern works with the image catalog:

```bash
MODEL_ID="$(python3 scripts/ima_runtime_cli.py --task-type image_to_image --list-models --output-json | python3 -c 'import json,sys; print(json.load(sys.stdin)[0][\"model_id\"])')"
python3 scripts/ima_runtime_cli.py \
  --task-type image_to_image \
  --model-id "$MODEL_ID" \
  --prompt "turn this into an oil painting" \
  --input-images ./example.png \
  --output-json
```

### 3. First Image-to-Image Restyle

Image to image with one local reference image:

```bash
python3 scripts/ima_runtime_cli.py \
  --task-type image_to_image \
  --prompt "turn this into an oil painting" \
  --input-images ./example.png \
  --output-json
```

Use this when the user already has one source image and wants a style transfer or continuity pass.

## Tuning And Troubleshooting

- Parameter tuning examples: `capabilities/image/references/parameter-tuning.md`
- Detailed usage scenarios: `capabilities/image/references/scenarios.md`
- Failure diagnosis and recovery: `references/operations/troubleshooting.md`

## Rules

- Always use `scripts/ima_runtime_cli.py` as the entrypoint.
- Use `scripts/ima_runtime_setup.py` first on a new machine.
- Use `scripts/ima_runtime_doctor.py` for setup and environment checks.
- `--output-json` is machine-parseable JSON only.
- `image_to_image` requires at least one input image.
- `aspect_ratio` and `n` are currently passed through `--extra-params`, not dedicated CLI flags.
- When both `size` and `aspect_ratio` are present, the runtime keeps both and lets backend validation decide.
- If you omit `--model-id`, the runtime uses the recommended default for that task type.
- Auto-selected default models are not written back as long-term user preferences.
- Model IDs are resolved against the live product list before task creation.

## Read Next

- `SKILL.md`
- `references/README.md`
- `capabilities/image/CAPABILITY.md`
- `references/operations/troubleshooting.md`
- `capabilities/image/references/parameter-tuning.md`
