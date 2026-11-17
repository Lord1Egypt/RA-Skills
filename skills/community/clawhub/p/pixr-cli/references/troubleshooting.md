# Troubleshooting

## Models Do Not List

1. Verify `PIXR_API_KEY` is set.
2. Run `pixr models --no-interactive`.

If the API key is missing, set it first:

```bash
export PIXR_API_KEY=your_api_key   # or the env var named by --api-key-env
```

## Config Looks Wrong

Inspect runtime state:

```bash
pixr config --json
```

Check:

1. CLI flags
2. environment variables
3. saved config
4. discovered files

## Saved Defaults Not Applying

1. inspect `~/.pixr/config.json`
2. run `pixr model`
3. run `pixr save-dir`

## End-To-End Smoke Test

```bash
pixr model gemini-2.5-flash-image
pixr save-dir --set "~/Pictures/pixr"
pixr generate --save-to ./tmp "test prompt"
```

## Dimension Or Format Output Looks Wrong

Use:

```bash
pixr generate -w 1600 -h 840 -f webp "test prompt"
```

Remember:

- width only preserves aspect ratio
- height only preserves aspect ratio
- width plus height forces an exact final size

## Provider errors

- `Unknown provider` or `Invalid base URL`: use `gemini`, `openai`, `openrouter`, or `fal`, and a full `http(s)` URL (include `/v1` for OpenAI-compatible APIs).
- `No model is set`: no model is built in. List with `pixr models [--search <text>]`, then pass `--model <name>` or run `pixr model <name>`.
- `does not accept input images`: the model cannot edit; check `pixr models --info <model>`.
- A `warning: ... does not list the parameter` means the model's live schema lacks that `--param`; it may be ignored.
- `request failed (401/403)`: check the key and which env var `--api-key-env` points to.
