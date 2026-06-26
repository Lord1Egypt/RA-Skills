---
name: openclaw-context-upgrade
description: Diagnose and upgrade OpenClaw conversation context limits, especially moving a chat from ~272k to 1M. Use when the user asks to enlarge context, make GPT-5.4 use 1M context, change `agents.defaults.contextTokens`, verify why a chat still shows 272k after changes, or execute the full workflow of model selection + config patch + restart + fresh session + status verification.
---

# OpenClaw Context Upgrade

## Check current state first

1. Run `session_status` and record:
   - current model
   - current `Context`
   - whether the session already shows `1.0m`
2. If the user is only asking "why isn't it 1M yet", diagnose first. Do not change config blindly.

## Inspect the exact config path before editing

1. Inspect `agents.defaults.contextTokens` with `gateway` `config.schema.lookup`.
2. If model selection matters, also inspect `agents.defaults.model`.
3. Use `gateway` `config.patch` for changes.
4. Do not tell the user to run `openclaw` CLI for this workflow.

## Upgrade workflow

1. Make sure the target session is using a high-context model.
   - Prefer model alias `GPT-5.4` for this workflow.
   - During verification, avoid relying on fallback behavior.
   - If needed, use `session_status` with a session model override to pin the current session to `GPT-5.4`.

2. Raise the default context budget.
   - Set `agents.defaults.contextTokens = 1000000`.
   - If the user's goal is future sessions, patch defaults.
   - If the user only wants diagnosis, explain the change without applying it.

3. Let the restart happen.
   - `gateway config.patch` restarts OpenClaw automatically.
   - Always include a clear `note` so the user gets a useful completion message after restart.

4. Force a fresh chat session.
   - Tell the user to use `/new` or `/reset`.
   - Old chats often keep the earlier session budget and mislead verification.

5. Verify after the fresh session starts.
   - Run `session_status` again.
   - Success looks like `Context: .../1.0m` or similar.

## Diagnose common failure modes

### Still shows `.../272k`

Check these in order:

1. The chat was not restarted with `/new` or `/reset`.
2. The session is still on the wrong model or a fallback model.
3. The provider/model pair is returning a lower real cap.
4. The config patch did not target `agents.defaults.contextTokens` correctly.

## Tell the truth about limits

- Do not promise 1M if the provider is actually returning a smaller cap.
- OpenClaw can request a larger budget, but it cannot exceed the model/provider limit in reality.
- If verification still shows `272k`, say that plainly and explain whether the blocker is session reuse, model mismatch, or provider cap.

## Default reply pattern

Use this sequence when answering:

1. State the current observed limit.
2. Give the exact fix order:
   - pin model to `GPT-5.4`
   - set `agents.defaults.contextTokens = 1000000`
   - restart
   - `/new` or `/reset`
   - verify with `session_status`
3. End with the caveat that provider limits still win.
