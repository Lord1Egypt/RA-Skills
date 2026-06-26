---
name: gpt-image-2-toolkit
description: Install, verify, repair, and diagnose GPT-Image-2 support for OpenClaw so agents can use model refs like hnbc/gpt-image-2 through the built-in image_generate tool. Use when a user wants to add GPT-Image-2 image generation, re-install the skill on another machine, or fix errors like 'No image-generation provider registered for hnbc'.
---

# GPT-Image-2 for OpenClaw

Use this skill when the user wants GPT-Image-2 image generation available through OpenClaw's built-in `image_generate` tool.

## What this skill does

- Installs a plugin package into the global OpenClaw extensions directory
- Registers provider id `hnbc`
- Exposes model `hnbc/gpt-image-2`
- Verifies installation from file, local runtime, and tool perspectives
- Diagnoses the common split-brain case where disk/runtime sees `hnbc` but the running gateway tool view does not
- Reminds you that a running gateway may need a restart before the tool sees the new provider

## When to use

- "给 OpenClaw 加一个 GPT-Image-2 图像能力"
- "让 image_generate 支持 hnbc/gpt-image-2"
- "修复 No image-generation provider registered for hnbc"
- "把这个能力做成别的 agent / 机器可安装的形式"
- "检查 GPT-Image-2 provider 为什么工具侧看不到"

## Core workflow

### Install
1. Run `scripts/install.sh`.
2. Run `scripts/self-check.sh`.
3. Note: bundled `hnbc` under `/usr/lib/node_modules/openclaw/dist/extensions/hnbc` is also a valid source; missing `~/.openclaw/extensions/hnbc` alone does not prove the provider is absent.

### Verify
Check both sides:
1. Local runtime/plugin registry
2. `image_generate(action="list")`

### Diagnose mismatch
If local runtime sees `hnbc` but `image_generate list` does not:
- explain that the currently running gateway likely still holds an old provider registry
- ask before restarting the gateway
- do **not** restart without explicit user approval
- after restart, verify again and test a real generation

### Deep diagnosis
If anything is unclear, run `scripts/diagnose.sh`.
If you need extra interpretation guidance, read `references/troubleshooting.md`.

## Recommended validation order

1. `scripts/self-check.sh`
2. `image_generate(action="list")`
3. If missing from tool list, compare with local runtime using `scripts/diagnose.sh`
4. After install or restart, run `scripts/e2e-check.sh`
5. Test a real generation with `model="hnbc/gpt-image-2"`

For next-version release guidance, read `references/release-1.0.1.md`.

## Important compatibility notes

- `hnbc/gpt-image-2` supports generation, not edit.
- Supported sizes: `1024x1024`, `1024x1536`, `1536x1024`
- Supported aspect ratios: `1:1`, `2:3`, `3:2`
- Do **not** pass `resolution`; HNBC currently rejects resolution overrides.
- Auth should come from either:
  - `HNBC_API_KEY`, or
  - `models.providers.hnbc.apiKey`, or
  - an auth profile for provider `hnbc`

## Files bundled with this skill

- `assets/plugin/` — the plugin package files
- `scripts/install.sh` — installs the plugin into the global OpenClaw extensions dir
- `scripts/self-check.sh` — verifies required files and manifest/package basics
- `scripts/diagnose.sh` — prints a fuller runtime diagnosis
- `scripts/e2e-check.sh` — runs a post-install validation checklist
- `references/troubleshooting.md` — quick error-to-fix map
- `references/release-1.0.1.md` — next release checklist and publish command

## Verification checklist

- `scripts/self-check.sh` returns `STATUS=ok`
- `image_generate(action="list")` shows `hnbc (default gpt-image-2)`
- generating with `model="hnbc/gpt-image-2"` works
- no `resolution` parameter is sent during generation
