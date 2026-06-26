---
name: opencode-discord-thread
description: Use this skill when OpenClaw should hand a coding task to OpenCode, keep the OpenCode run model-compatible with Z.AI Coding Plan / GLM plans, and mirror execution progress into a Discord thread for live review.
metadata:
  owner: openclaw
  runtime: python-stdlib
  compatibility: OpenClaw, OpenCode, Discord threads, Z.AI Coding Plan
---

# OpenCode Discord Thread

Use this skill when the user wants OpenClaw to delegate coding work to a local OpenCode run and keep that run visible in Discord.

This skill is optimized for Z.AI Coding Plan workflows. Do not hard-code a stale GLM model id. Prefer an authenticated Z.AI Coding Plan provider and let the caller pass the exact model explicitly when needed.

## When to use it

Use this skill when all of the following are true:

1. OpenClaw is expected to offload coding to OpenCode instead of doing the edit loop directly.
2. Progress needs to be mirrored into an existing Discord thread or a new thread in a Discord channel.
3. The environment already has `opencode` installed and authenticated, ideally through `opencode auth login` with `Z.AI Coding Plan`.

Avoid this skill when:

1. The task is small enough for OpenClaw to complete directly.
2. Discord streaming is not needed.
3. The machine cannot reach Discord or OpenCode is not installed.

## Workflow

1. Confirm that the repository path, Discord target, and OpenCode prompt are known.
2. Prefer reusing a warm OpenCode backend with `--attach http://host:port` when available.
3. Pass the exact model only if the caller already knows the current Z.AI Coding Plan model id.
4. Use `scripts/run_opencode_discord_bridge.py` to launch `opencode run --format json`, summarize event output, and mirror that stream into Discord.
5. Treat Discord as an observer surface, not the source of truth. The repository remains local and OpenCode performs the code changes locally.

## Z.AI Coding Plan guidance

For compatibility with Z.AI Coding Plan:

1. Authenticate OpenCode with the `Z.AI Coding Plan` provider rather than assuming a generic provider entry.
2. Discover currently available plan-backed models with `opencode models` or inside OpenCode via `/models`.
3. Pass `--model provider/model` only after discovery or when the operator already knows the right id.
4. If no model is provided, let OpenCode use its configured default model.

This keeps the skill resilient when Z.AI changes the exact GLM model catalog.

## Discord targeting

The bridge supports two modes:

1. Existing thread: pass `--thread-id`.
2. Create a new public thread from a parent channel: pass `--parent-channel-id` and optionally `--thread-name`.

The bridge posts a header message, keeps a rolling status message updated during execution, then posts the final summary and any remaining transcript chunks.

## Commands

Existing thread:

```bash
python3 skills/opencode-discord-thread/scripts/run_opencode_discord_bridge.py \
  --repo /path/to/repo \
  --thread-id 123456789012345678 \
  --prompt "Implement the requested feature and run relevant tests." \
  --model zai/glm-4.5
```

Create a new thread from a parent channel:

```bash
python3 skills/opencode-discord-thread/scripts/run_opencode_discord_bridge.py \
  --repo /path/to/repo \
  --parent-channel-id 123456789012345678 \
  --thread-name "OpenCode: feature work" \
  --prompt-file /tmp/opencode_prompt.txt
```

Reuse a warm OpenCode server:

```bash
python3 skills/opencode-discord-thread/scripts/run_opencode_discord_bridge.py \
  --repo /path/to/repo \
  --thread-id 123456789012345678 \
  --attach http://127.0.0.1:4096 \
  --prompt "Continue the current implementation and summarize the diff."
```

## Required environment

The bridge reads:

1. `DISCORD_BOT_TOKEN` for Discord API access.
2. Any provider credentials OpenCode already uses, such as the Z.AI Coding Plan credential stored by `opencode auth login`.

## Failure handling

If the bridge fails:

1. Check `opencode --version`.
2. Check `opencode auth list`.
3. Confirm the bot can post in the target Discord channel or thread.
4. Confirm the thread is not locked or archived.
5. Read [references/opencode_discord_bridge.md](./references/opencode_discord_bridge.md) for the operational details and argument behavior.
