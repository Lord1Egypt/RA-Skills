# OpenCode Discord Bridge Reference

This skill ships one helper script:

- `scripts/run_opencode_discord_bridge.py`

It is intentionally stdlib-only so it can run on a minimal OpenClaw host.

## What it does

1. Validates the OpenCode and Discord inputs.
2. Reuses an existing Discord thread or creates a new public thread from a parent channel.
3. Runs `opencode run --format json` in the target repository.
4. Extracts human-readable summaries from the raw event stream without depending on a single fragile event schema.
5. Periodically edits a status message in Discord so the thread behaves like a live execution console.
6. Posts the final outcome and any buffered transcript text when the run exits.

## Key arguments

- `--repo`: working directory for the OpenCode run.
- `--prompt`: inline prompt text.
- `--prompt-file`: path to a file containing the prompt.
- `--thread-id`: reuse an existing Discord thread.
- `--parent-channel-id`: create a new public thread from a message in this channel.
- `--thread-name`: thread title when a new thread is created.
- `--attach`: attach to a warm `opencode serve` instance.
- `--model`: optional `provider/model` id.
- `--agent`: optional OpenCode agent id.
- `--session`: continue a specific OpenCode session.
- `--continue-last`: continue the last OpenCode session.
- `--opencode-arg`: repeated passthrough flags appended to the `opencode run` invocation.

## Operational notes

- The bridge updates one rolling status message to reduce Discord spam.
- Large outputs are chunked to stay under Discord message limits.
- If the raw JSON format changes, the bridge still degrades to generic event summaries instead of failing hard.
- When using Z.AI Coding Plan, prefer passing the current model id explicitly only after discovery via `opencode models`.

## Example

```bash
export DISCORD_BOT_TOKEN=...

python3 skills/opencode-discord-thread/scripts/run_opencode_discord_bridge.py \
  --repo "$PWD" \
  --parent-channel-id 123456789012345678 \
  --thread-name "OpenCode live run" \
  --prompt "Implement the requested change, keep tests green, and summarize the result." \
  --model zai/glm-4.5 \
  --opencode-arg=--share
```
