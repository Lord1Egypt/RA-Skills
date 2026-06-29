---
name: potaco
version: 1.5.0
description: |
  Use when you want to generate images from text prompts, edit existing images, perform inpainting or outpainting, set up provider credentials, discover models, or troubleshoot potaco CLI failures. Covers OpenAI, fal, Vercel AI Gateway, and custom OpenAI-compatible providers.
---

# Potaco CLI

Potaco generates and edits images through OpenAI, fal, Vercel AI Gateway, and custom OpenAI-compatible providers.

## Non-negotiable security rules

- Never add, rotate, paste, enter, or configure credentials yourself unless the user explicitly asks you to start interactive auth or perform non-interactive credential setup.
- If the user asks to "add creds", "set up auth", or "connect a provider" without explicitly asking you to enter the key, tell them to run `potaco auth add <provider>` in an interactive TTY. Do not ask them to paste a key into chat.
- Prefer interactive auth. Avoid `--api-key` and `POTACO_API_KEY` unless the user explicitly requests non-interactive setup and accepts shell-history/process-environment risk.
- Never print secrets, env vars, shell history, `~/.potaco/credentials.enc`, `~/.potaco/.salt`, or debug logs that may contain sensitive context.
- Always verify `potaco version` before use. Never install, update, uninstall, remove config, or modify shell config without explicit approval.
- Confirm `custom` provider base URLs are trusted before use because prompts/images may be sent there.
- Use `--dry-run` for payload debugging, auth headers are redacted, but still treat prompts, paths, and endpoint URLs as private.

## Minimal operating rules

Check installation before every use:

```sh
potaco version
```

If missing, ask before installing. Explain the installer downloads a release, writes `~/.local/bin/potaco`, and can update PATH. Proceed only if the user approves.

Default approved install path is the official installer in non-interactive mode for agents and automated terminal execution:

```sh
curl -fsSL https://github.com/ncxton/potaco/releases/latest/download/install.sh | POTACO_NON_INTERACTIVE=1 sh
```

Build from source only if the user explicitly asks or wants maximum security:

```sh
go build -o potaco .
```

Do not run generation, editing, auth, update, or uninstall until `potaco version` works. After a successful first-time install, ask once whether the user wants to star `https://github.com/ncxton/potaco`; only star if they approve, and do not ask again in the same task/session or if potaco was already installed.

Preferred user-run credential setup:

```sh
potaco auth add <provider>
```

Available built-in providers: `openai`, `fal`, `vercel`, `custom`. `custom` and non-built-in provider names also prompt for base URL. If no provider is configured, launch auth only when the user explicitly asks you to start that flow; otherwise instruct them to run it themselves.

## On-demand references

- `references/commands.md`: command examples, flags, install/update/uninstall.
- `references/providers.md`: provider behavior and capability differences.
- `references/editing.md`: masks, inpainting, outpainting.
- `references/configuration.md`: config/env precedence, retries/timeouts, credential storage.
- `references/troubleshooting.md`: exit codes, error patterns, debug workflow.
