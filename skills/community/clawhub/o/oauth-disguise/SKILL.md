---
name: oauth-disguise
version: 1.1.0
description: Configure Anthropic OAuth tokens (sk-ant-oat01-*) to work with OpenClaw as API keys via environment variable injection. Use when: (1) user has OAuth tokens that fail direct API calls with authentication_error, (2) switching from proxy to Anthropic official API, (3) configuring Claude Pro/Team subscription tokens for API use. NOT for: standard API keys (sk-ant-api03-*), working proxy services, or non-Anthropic providers.
---

# OAuth Token Disguise

Configure Anthropic OAuth tokens (`sk-ant-oat01-*`) as working API keys through OpenClaw's `env.vars` injection.

## Core Method

Inject token via environment variable, reference with `${VAR}` in provider config:

```bash
openclaw config patch '{
  "env": {
    "vars": {
      "ANTHROPIC_API_KEY": "sk-ant-oat01-YOUR_TOKEN"
    }
  },
  "models": {
    "providers": {
      "anthropic-official": {
        "baseUrl": "https://api.anthropic.com",
        "apiKey": "${ANTHROPIC_API_KEY}",
        "api": "anthropic-messages",
        "models": [
          {"id": "claude-sonnet-4-20250514", "name": "Claude Sonnet 4"},
          {"id": "claude-opus-4-6", "name": "Claude Opus 4.6"}
        ]
      }
    }
  },
  "agents": {
    "defaults": {
      "model": {
        "primary": "anthropic-official/claude-sonnet-4-20250514"
      }
    }
  }
}'
```

Then restart: `openclaw gateway restart`

## Per-Agent Configuration

Apply to a single agent (keep others on proxy):

```bash
openclaw config patch '{
  "agents": {
    "list": [{
      "id": "YOUR_AGENT_ID",
      "name": "Agent Name",
      "workspace": "/path/to/workspace",
      "model": {"primary": "anthropic-official/claude-opus-4-6"}
    }]
  }
}'
```

## Verification

Run `session_status` or `openclaw status`. Look for:
- `🧠 Model: anthropic-official/*` → ✅ success
- `custom-proxy/*` or fallback notice → ❌ token invalid or auth cooldown

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| Still shows `custom-proxy/*` | defaults.model.primary wrong | Set to `anthropic-official/MODEL_ID` |
| Fallback after token switch | Auth cooldown from rapid switching | Wait 5 min, restart gateway |
| `env variable missing` | Gateway not restarted | `openclaw gateway restart` |
| Works then stops | Token expired | Replace token in `env.vars`, restart |

**Critical**: Do not rapidly switch between tokens. OpenClaw tracks auth failures and applies cooldown periods. If stuck in fallback, use `session_status` with model parameter to force reset:

```
/model anthropic-official/claude-opus-4-6
```

## Dual Provider Setup

Keep proxy as fallback while using official API:

```json
{
  "env": {"vars": {"ANTHROPIC_API_KEY": "sk-ant-oat01-xxx"}},
  "models": {
    "providers": {
      "custom-proxy": {
        "baseUrl": "https://your-proxy.com/",
        "apiKey": "proxy-key",
        "api": "anthropic-messages",
        "models": [{"id": "claude-sonnet-4-5", "name": "Claude Sonnet 4.5"}]
      },
      "anthropic-official": {
        "baseUrl": "https://api.anthropic.com",
        "apiKey": "${ANTHROPIC_API_KEY}",
        "api": "anthropic-messages",
        "models": [
          {"id": "claude-sonnet-4-20250514", "name": "Claude Sonnet 4"},
          {"id": "claude-opus-4-6", "name": "Claude Opus 4.6"}
        ]
      }
    }
  }
}
```

## Security

- Tokens auto-redacted in `config.get` output (`__OPENCLAW_REDACTED__`)
- Direct curl with these tokens fails (only works through OpenClaw)
- Never commit `openclaw.json` with raw tokens to version control
- Use `env.vars` (not inline `apiKey`) to keep tokens in one place