# Install And Secrets

## Easy Install For Any Agent

Give this to any coding agent or IDE that supports local skills:

```text
Install the ClawHub skill `pixellab-ai`, then set `PIXELLAB_API_KEY` in the local shell or host secret manager; use the skill to turn my rough asset idea into a visual brief before live PixelLab generation.
```

Command-line install from a skills directory:

```bash
npx --yes clawhub install pixellab-ai --force
export PIXELLAB_API_KEY='PASTE_YOUR_KEY_HERE'
```

If the host does not use ClawHub, copy the `pixellab-ai/` folder into the skills directory that host reads.

## API Key Boundary

Requires API key: yes. Live PixelLab generation needs the user's own PixelLab account token.

Users can create or manage a PixelLab account at `https://www.pixellab.ai/` and get a PixelLab MCP/API token at `https://api.pixellab.ai/mcp`.

`PIXELLAB_API_KEY` is the required local environment variable name. It is safe to declare the name in `SKILL.md`, OpenClaw metadata, and ClawHub setup instructions.

The secret value stored in `PIXELLAB_API_KEY` is the private account credential. Do not put that value in `SKILL.md`, `agents/openai.yaml`, examples, ClawHub metadata, commits, screenshots, logs, or chat output.

For local shell use, set `PIXELLAB_API_KEY` in your own process environment. Keep the value out of this package and out of chat logs.

Safe local setup:

```bash
export PIXELLAB_API_KEY='PASTE_YOUR_KEY_HERE'
```

The helper does not auto-discover local secret files. If a user intentionally keeps local environment values in a file, pass that path explicitly with `--env-file PATH`. Do not paste the real key into commands, docs, examples, screenshots, commits, or chat.

`PIXELLAB_API_BASE` defaults to `https://api.pixellab.ai`. Non-default HTTPS API bases require the explicit `--allow-custom-base` flag and should be used only for trusted test endpoints.

For OpenClaw, configure the key as a runtime secret for the skill entry. Use the local config shape from `config/openclaw.example.json5`, and keep the real value outside the published skill package.

For ClawHub, publish only the skill files. The uploaded package should declare that `PIXELLAB_API_KEY` is required, but it must never include the actual key. Each installer brings their own PixelLab account key.

## Codex Use

Codex can use this skill after the folder is installed or copied into an active skills directory. If the key is not configured, Codex should still use the skill to choose endpoints, prepare payload files, and explain setup, but it must not claim an API call succeeded.

For live runs, run the PixelLab helper from a worker subagent or child context when available. The main session should receive compact JSON paths and summaries, not raw base64 image results.

## OpenClaw Use

Install the `pixellab-ai` directory as an OpenClaw skill, then start a new OpenClaw session or refresh the skill snapshot. Invoke it explicitly with:

```text
/skill pixellab-ai
```

or ask naturally for a PixelLab pixel-art asset workflow.

## Optional Codex MCP Plugin

The repo also includes an optional Codex plugin at `plugins/pixellab-ai-mcp`. This is different from the skill:

- Use the skill for bulk production, manifests, retries, contact sheets, approvals, and validation.
- Use the plugin when Codex should expose PixelLab's hosted MCP tools directly.

The plugin does not store an API key. It reads the token from `PIXELLAB_API_KEY`, the same local environment variable used by the REST helper:

```bash
export PIXELLAB_API_KEY='PASTE_YOUR_KEY_HERE'
```

For manual Codex MCP setup without the plugin, use Codex's bearer-token environment option:

```bash
codex mcp add pixellab \
  --url https://api.pixellab.ai/mcp \
  --bearer-token-env-var PIXELLAB_API_KEY
```

Do not hardcode the bearer token into `.mcp.json`, `config.toml`, commits, screenshots, or chat.

## ClawHub Upload

Current local CLI form:

```bash
npx --yes clawhub publish pixellab-ai \
  --slug pixellab-ai \
  --name "PixelLab AI" \
  --owner OWNER_HANDLE \
  --version 1.5.5 \
  --changelog "Public page copy update: explain SkillSpector credential and urlopen findings as the disclosed PixelLab API authentication and asset-download flow." \
  --tags latest,pixel-art,game-assets,api,openclaw,codex,mcp
```

Use a valid semver version. Existing ClawHub versions are immutable, so republish fixes under a new version.

The current ClawHub CLI does not support local upload scans before publishing. After publishing, retrieve stored scan results with:

```bash
npx --yes clawhub scan --slug pixellab-ai --version 1.5.5 --json
```
