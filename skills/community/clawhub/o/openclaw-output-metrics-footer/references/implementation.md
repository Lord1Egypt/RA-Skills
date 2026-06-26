# Implementation

Bundled extension template:

```text
assets/extension-template/
```

Expected deployed extension path:

```text
~/.openclaw/extensions/openclaw-output-metrics-footer/
```

## Hooks

The extension registers:

```text
llm_output
message_sending
```

`llm_output` records recent provider/model/token usage.

`message_sending` appends the footer only at channel delivery time. It is provider-agnostic and should work for text channels that pass through OpenClaw's delivery runtime.

This keeps the footer out of model prompts and memory context.

## Footer format

```text
_🟢 ↑54k ↓157 · 21%ctx · 5h 89% · kimi-k2.6:cloud_
```

Fields:

- `↑54k`: input/context tokens for the turn.
- `↓157`: assistant output tokens for the turn.
- `21%ctx`: current context usage percentage, including configured reserve.
- `5h 89%`: live/cached Codex short-window quota remaining.
- `kimi-k2.6:cloud`: model used for the turn.

Subagent aggregate:

```text
_🟢 ↑54k ↓157 · 21%ctx · 5h 89% · openai-codex/gpt-5.5 · sub ↑31k ↓4k_
```

Subagent accounting is best effort. The current extension aggregates nearby LLM outputs from other sessions within the cache window. If OpenClaw exposes parent/root run IDs later, replace this heuristic with exact parent-run matching.

## Channel support

Supported in principle:

- Discord
- Telegram
- Slack
- WhatsApp
- Signal
- Matrix
- Mattermost
- Google Chat
- Microsoft Teams
- IRC
- Other OpenClaw text providers that emit `message_sending`

Limitations:

- Media-only sends are ignored.
- Providers with strict message length limits may skip the footer if the output is already near the limit.
- Rich card/embed surfaces may fall back to plain text behavior depending on the provider.
- Subagent accounting is best-effort until OpenClaw exposes exact parent-run metadata in the hook context.

## Codex quota

The extension reads the local OpenClaw auth profile store to find an OpenAI Codex OAuth access token, then fetches:

```text
https://chatgpt.com/backend-api/wham/usage
```

Privacy rules:

- Never print the token.
- Never print the email.
- Never print the auth profile ID.
- Never print the auth profile path in channel output.

If quota fetch fails, omit the quota field rather than blocking delivery.

## Model context

The extension includes a small context-window map for common configured models:

- `openai-codex/gpt-5.5`: `391k`
- `openai-codex/gpt-5.4-mini`: `266k`
- `ollama/kimi-k2.6:cloud`: `250k`
- `ollama/qwen3.5:397b-cloud`: `250k`

If a model is unknown, show `n/a%ctx` instead of guessing.

## ClawHub publish

From the skill folder:

```bash
clawhub publish . --slug openclaw-output-metrics-footer --name "OpenClaw Output Metrics Footer" --version 0.2.1 --changelog "Parse current Codex quota usage windows"
```

Run `clawhub login` first if not authenticated.
