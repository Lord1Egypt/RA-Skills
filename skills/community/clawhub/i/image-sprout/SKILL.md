---
name: image-sprout
description: >
  Generate and iterate on images using Image Sprout projects. Creates consistent
  outputs from reference images, style guides, and subject guides. Use when an
  agent or user needs repeatable image generation with saved context.
user-invocable: true
metadata: '{"openclaw":{"requires":{"bins":["image-sprout"]},"homepage":"https://github.com/tmchow/image-sprout"}}'
---

# image-sprout

Generate and iterate on images with consistent style and subject identity. Image Sprout turns reusable project context — reference images, derived guides, and persistent instructions — into repeatable outputs.

## 1. OpenRouter Key Setup

Image Sprout stores its OpenRouter key on disk. Set it once per machine:

```bash
image-sprout config set apiKey <your-openrouter-key>
image-sprout config show    # confirm key is set (does not reveal the raw key)
```

How the calling environment stores or injects that key is outside this skill's scope.

## 2. The Project Model

Three context layers drive every generation:

- **Visual Style** — consistent look and feel across outputs
- **Subject Guide** — consistent subject identity across outputs
- **Instructions** — persistent generation constraints (watermarks, framing, branding)

Two reference pools:

- **Shared refs** — drive both guides (default, simplest)
- **Split refs** — separate style and subject pools (advanced; use `--role style` or `--role subject` when adding)

Understanding this model prevents the most common agent mistake: generating without saved context and wondering why outputs are inconsistent.

## 3. Core CLI Workflow

```bash
# Create a project
image-sprout project create <name>

# Add references (3+ recommended; more refs = better derivation)
image-sprout ref add --project <name> ./ref1.png ./ref2.png ./ref3.png

# Optional: persistent instructions
image-sprout project update <name> --instructions "Watermark bottom-right: subtle."

# Derive guides from refs
image-sprout project derive <name> --target both   # or: style, subject

# Check readiness before generating
image-sprout project status <name> --json

# Generate (--count controls images per run: 1, 2, 4, 6; default is 4)
image-sprout project generate <name> --prompt "hero in neon rain"
image-sprout project generate <name> --prompt "hero in neon rain" --count 1

# Inspect results
image-sprout run latest --project <name> --json

# Delete a session and all its runs/images
image-sprout session delete --project <name> <session-id>
```

Top-level aliases for convenience:

```bash
image-sprout generate --project <name> --prompt "hero in neon rain"   # same as project generate
image-sprout analyze --project <name> --target both                    # same as project derive
```

## 4. JSON Output — the Agent Pattern

Always use `--json` for structured output:

```bash
image-sprout project show <name> --json
image-sprout project status <name> --json
image-sprout run latest --project <name> --json
image-sprout run list --project <name> --json --limit 5
```

Use `--value PATH` to pluck a single field:

```bash
image-sprout run latest --project <name> --json --value images[0].path
```

This is how agents hand image paths to downstream tools. Run images land in image-sprout's internal app data directory — use `run latest --json --value images[0].path` to get the path and leave what to do with it to the calling workflow.

## 5. Parallel-Safe Usage

`image-sprout project use <name>` sets a shared "current project" state on disk. When multiple agents or processes run concurrently, this state can collide. **Always pass `--project <name>` explicitly** — never rely on the current project shortcut in agent workflows.

## 6. Web UI — Agent Awareness

The web app runs over the same on-disk store as the CLI. Agents won't use it directly, but should know it exists so they can offer it to users when interactive review is appropriate.

```bash
image-sprout web              # launches local app
image-sprout web --open       # also opens in default browser
image-sprout web --port 8080  # custom port (default: 4310)
```

Useful for:
- reviewing and comparing generated images visually
- setting up a project interactively before handing off to CLI/agent use
- iterating on outputs via the canvas interface

**Security: do not expose the web UI to the public internet.** The server has no authentication. Safe options are localhost only, or a private network like Tailscale. The risk is public internet exposure — LAN and tailnet access are fine.

## 7. Model Management

```bash
image-sprout model list
image-sprout model set-default google/gemini-3.1-flash-image-preview
image-sprout model add openai/gpt-5-image
image-sprout model restore-defaults
```

Default generation model is **Nano Banana 2** (`google/gemini-3.1-flash-image-preview`). Custom models must accept image input and produce image output via OpenRouter.

Guide derivation uses a separate configurable analysis model (default: `google/gemini-3.1-flash-image-preview`):

```bash
# Set a persistent analysis model
image-sprout config set analysisModel google/gemini-2.5-flash

# Override per-derive
image-sprout project derive <name> --target both --analysis-model google/gemini-2.5-flash
```
