# OpenClaw Growth Pack Examples

## Example A: Fix 401 after valid key

Symptoms:
- `HTTP 401: invalid access token or token expired`
- key is valid in provider console

Checks:
1. Ensure `baseUrl` is `https://coding.dashscope.aliyuncs.com/v1`.
2. Ensure provider API key is in `models.providers.bailian.apiKey`.
3. Ensure no stale override in `~/.openclaw/agents/main/agent/models.json`.
4. Restart gateway.

```powershell
openclaw gateway restart
```

## Example B: Fix dashboard unauthorized mismatch

Symptoms:
- `unauthorized: gateway token mismatch`

Fix:
1. Set same value in `gateway.auth.token` and `gateway.remote.token`.
2. Paste same token into dashboard Control UI.
3. Restart gateway.

## Example C: Anti-stall validation

Goal: verify agent can finish a multi-step task.

Test task:
1. Create a folder.
2. Create one markdown file.
3. Write a summary block with evidence.

Pass condition:
- response contains execution evidence (artifact path or command result summary), not planning-only text.

## Example D: Minimal daily autonomy loop

Daily routine:
1. Read `tasks/QUEUE.md`.
2. Execute one concrete next step.
3. Append one line in `memory/YYYY-MM-DD.md` with evidence.

Weekly routine:
1. Review 7 memory files.
2. Extract repeated failures.
3. Add one local rule to prevent recurrence.
