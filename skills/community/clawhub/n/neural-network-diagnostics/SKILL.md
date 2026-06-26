---
name: neural-network-ops
description: Diagnoses and tunes LLM providers (Groq, OpenRouter, Ollama), resolves rate limits/timeouts, and selects stable primary/fallback models. Use when the bot is silent, responses are slow, provider errors appear, or model routing/fallbacks need adjustment.
---

# Neural Network Ops

## Purpose

Keep OpenClaw responsive by managing model providers, routing, and fallback behavior.

## Fast Triage

Run these checks first:

```bash
systemctl is-active openclaw-gateway ollama
journalctl -u openclaw-gateway -n 40 --no-pager
free -h
```

Focus on these log patterns:
- `rate limit reached`
- `Model context window too small`
- `Unknown model`
- `No endpoints available`
- `sendMessage failed`
- `embedded run timeout`
- `Removed orphaned user message`

## Routing Policy

Use this default priority for production:
1. `groq/llama-3.3-70b-versatile` (fastest cloud path)
2. `openrouter/xiaomi/mimo-v2-pro` (high quality backup)
3. `openrouter/meta-llama/llama-3.3-70b-instruct:free`
4. `ollama/qwen2.5:7b` (last-resort local fallback)

Avoid 35B local models on 30GB RAM CPU servers for real-time Telegram replies.

## Stable Model Constraints

For local Ollama fallbacks:
- `contextWindow >= 16000`
- Keep `maxTokens` moderate (1024-2048) for latency
- Pre-warm after restart if local fallback is expected

Example local provider entry:

```json
{
  "id": "qwen2.5:7b",
  "name": "Qwen 2.5 7B (local)",
  "contextWindow": 32768,
  "maxTokens": 2048
}
```

## Recovery Playbook

### 1) Bot silent in Telegram

```bash
journalctl -u openclaw-gateway --since '10 min ago' --no-pager
```

If `sendMessage failed`, check network/provider errors first, then restart:

```bash
systemctl restart openclaw-gateway
```

### 2) Repeated `orphaned user message`

```bash
systemctl stop openclaw-gateway
rm -rf /root/.openclaw/.openclaw/agents/main/sessions/*
echo '{}' > /root/.openclaw/.openclaw/agents/main/sessions/sessions.json
chmod 600 /root/.openclaw/.openclaw/agents/main/sessions/sessions.json
systemctl start openclaw-gateway
```

### 3) Groq/OpenRouter rate limits

- Keep Groq as primary, but ensure at least one non-free fallback.
- For OpenRouter 404 privacy/policy errors, adjust data-policy settings in OpenRouter dashboard.
- Do not loop retries endlessly; rely on fallback chain.

### 4) Local fallback too slow

- Restart Ollama cleanly and warm one small model.
- Do not keep multiple heavy runners resident.

```bash
systemctl restart ollama
curl -s -X POST http://127.0.0.1:11434/api/chat \
  -H 'Content-Type: application/json' \
  -d '{"model":"qwen2.5:7b","messages":[{"role":"user","content":"hi"}],"stream":false}'
```

## Output Format

When reporting health, return:

```markdown
## Status
- Gateway: <active/inactive>
- Telegram provider: <connected/stalled>
- Primary model: <provider/model>
- Fallback chain: <ordered list>

## Findings
- <most critical issue first>
- <secondary issues>

## Actions Applied
- <exact changes made>

## Next Step
- <single user action to verify>
```

## Guardrails

- Never expose raw API keys in replies.
- Never execute irreversible financial actions automatically.
- Ask for explicit confirmation before account registrations or external postings.
- Prefer reversible config changes and keep backups before major edits.
