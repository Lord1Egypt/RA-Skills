# Adapter Matrix — Paperclip

| Adapter | Best for | Needs | Important note |
|--------|----------|-------|----------------|
| `codex_local` | Local OpenAI Codex worker on the same machine | `codex` CLI + `OPENAI_API_KEY` | Persists context through `previous_response_id`; review Paperclip's adapter behavior before enabling |
| `claude_local` | Local Claude Code worker | `claude` CLI + Anthropic auth | Resumes Claude sessions across heartbeats |
| `openclaw_gateway` | OpenClaw running outside Paperclip | Gateway URL + auth token or password | Use when OpenClaw should be hired as an employee via WebSocket gateway |
| `process` | Deterministic local scripts or wrappers | Local executable | Good for non-LLM workers or harnesses |
| `http` | Remote agents or webhooks | Reachable HTTP service | Best when the worker already exposes an API |

## Selection Rules

- Same host, coding-heavy work -> `codex_local` or `claude_local`
- OpenClaw in Docker or on another machine -> `openclaw_gateway`
- Existing internal automation service -> `http`
- Fixed shell workflow without a chat runtime -> `process`

## Useful Local-CLI Commands

```bash
pnpm paperclipai agent local-cli codexcoder --company-id <company-id>
pnpm paperclipai agent local-cli claudecoder --company-id <company-id>
```

Use these when you want the local worker identity and exported `PAPERCLIP_*` variables without waiting for a scheduled heartbeat.
