# Commands

## Install, update, uninstall

Check first:

```sh
potaco version
```

If missing, ask before installing. Default to the official installer in non-interactive mode for agents and automated terminal execution after approval:

```sh
curl -fsSL https://github.com/ncxton/potaco/releases/latest/download/install.sh | POTACO_NON_INTERACTIVE=1 sh
```

Build from source only if the user explicitly asks or wants maximum security:

```sh
go build -o potaco .
```

After a successful first-time install, ask once whether the user wants to star `https://github.com/ncxton/potaco`. Star only if they approve, and do not ask again in the same task/session or when potaco was already installed.

Update or uninstall only after explicit approval:

```sh
potaco update
potaco update --force
potaco uninstall
potaco uninstall -y
```

Interactive commands check for updates automatically by default. To disable prompts:

```sh
potaco config set auto_update false
```

Interactive uninstall asks whether to remove local config and encrypted credentials.

## Auth and status

Do not enter credentials yourself unless the user explicitly asks you to start auth or perform non-interactive setup.

```sh
potaco auth add openai
potaco auth add custom
potaco auth add openrouter --type openai-compatible --base-url https://openrouter.ai/api/v1
potaco auth add staging-openai --type openai --base-url https://proxy.example/v1
potaco auth list
potaco auth list --json
potaco auth remove openai
potaco use openai
potaco use openai --model gpt-image-2
potaco status
potaco status --json
```

Built-in names (`openai`, `fal`, `vercel`) use preset base URLs. Any other auth name, including aliases using `--type openai`, `--type fal`, or `--type vercel`, must include `--base-url` or have `base_url` in config.

## Generate

```sh
potaco gen --prompt "a cat in a spacesuit"
potaco gen --prompt "a logo" --stdout --output-format png > logo.png
potaco gen --prompt "various cats" --n 4 -o cats.png
potaco gen --prompt "test" --dry-run
```

Common flags: `--prompt/-p`, `--model`, `--size`, `--quality`, `--n`, `--seed`, `--guidance-scale`, `--negative-prompt`, `--response-format`, `--output/-o`, `--output-format`, `--stdout`, `--json`, `--dry-run`.

## Edit

```sh
potaco edit --prompt "add a hat" --image photo.png
potaco edit --prompt "make it night time" --image input.png -o output.png
potaco edit --prompt "add a tree" --image landscape.png --mask-rect 100,200,300,400
potaco edit --prompt "extend the landscape" --image photo.png --extend right=256
potaco edit --prompt "test edit" --image input.png --dry-run
```

Vercel does not support editing.

## Models and info

```sh
potaco models
potaco models list
potaco models list openai
potaco models openai
potaco models --json
potaco models list --json
potaco info image.png
potaco info image.png --json
```

Interactive `models` persists selection. `models list` only displays. In non-interactive mode, `models` behaves like `models list`.
Interactive model selection asks whether the selected model can edit images and stores that answer. Non-interactive setup must use `potaco config set model.edit true` or `potaco config set providers.<name>.models.<model>.edit true`. Generation is assumed available; edit capability is user-configured, not inferred from discovery.

## Persistent flags and overrides

Persistent flags: `--json`, `--verbose`, `--non-interactive`. `POTACO_NON_INTERACTIVE=1` equals `--non-interactive`; both skip automatic update prompts.

Provider override precedence: CLI flag > env var > config > provider preset.

| Flag | Env var | Description |
|------|---------|-------------|
| `--provider` | `POTACO_PROVIDER` | Provider preset |
| `--api-key` | `POTACO_API_KEY` | Override API key; avoid unless explicitly approved |
| `--base-url` | `POTACO_BASE_URL` | Override API base URL |
| `--model` | `POTACO_MODEL` | Override model |
| `--retries` | `POTACO_RETRIES` | Max retry attempts |
| `--timeout` | `POTACO_TIMEOUT` | Request timeout in seconds |
