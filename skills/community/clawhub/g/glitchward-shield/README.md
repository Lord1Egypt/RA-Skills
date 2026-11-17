# Glitchward LLM Shield — OpenClaw Skill

Prompt injection detection for AI agents. Scan prompts through a 6-layer detection pipeline before they reach your LLM.

## Security Model

> **IMPORTANT:** This skill sends prompt content to Glitchward's external API (`https://glitchward.com`) for security analysis. This is **by design** — the API performs the detection.
>
> **Do NOT use this skill if:**
> - Your prompts contain secrets, credentials, or API keys
> - You're processing PII or regulated data (HIPAA, GDPR, etc.)
> - Your content is proprietary and cannot leave your environment
>
> **Safe to use for:**
> - General user conversations
> - Public knowledge queries
> - Non-sensitive task instructions

## Install

```bash
npx clawhub@0.23.3 install glitchward-llm-shield
```

Or paste this repo URL directly into your OpenClaw agent chat.

## Setup

1. Get a free API token at [glitchward.com/shield](https://glitchward.com/shield)
2. Set the environment variable:

```bash
export GLITCHWARD_SHIELD_TOKEN="your-token-here"
```

> **Credential safety:** Never hardcode the token in source files. Keep it out of shell history, logs, and version control.

## What it does

This skill adds prompt injection scanning to your AI agent. Before any user input reaches your LLM, it gets validated through Glitchward's Shield API:

- **1,000+ detection patterns** across 26 provider modules
- **6-layer pipeline**: text normalization, pattern matching, encoding detection, invisible character analysis, known injection database, AI-powered analysis
- **26 attack categories**: jailbreaks, data exfiltration, MCP abuse, hooks hijacking, skill weaponization, multilingual attacks, and more
- **20+ languages**: Korean, Japanese, Chinese, Russian, Spanish, German, French, Portuguese, Vietnamese, and more
- **Low latency**: Typical response times under 50ms

## API Endpoints

| Endpoint | Method | Description |
|---|---|---|
| `/api/shield/validate` | POST | Validate a single prompt |
| `/api/shield/validate/batch` | POST | Validate multiple prompts |
| `/api/shield/stats` | GET | Usage statistics and quota |

## Example

**Safe pattern using variables and jq:**

```bash
PROMPT_TEXT="What is the capital of France?"
echo "$PROMPT_TEXT" | jq -Rs '{prompt: .}' | \
  curl -s -X POST "https://glitchward.com/api/shield/validate" \
    -H "X-Shield-Token: $GLITCHWARD_SHIELD_TOKEN" \
    -H "Content-Type: application/json" \
    -d @- | jq .
```

Response:
```json
{
  "safe": true,
  "blocked": false,
  "risk_score": 0.02,
  "processing_time_ms": 18
}
```

When a prompt is flagged:
```json
{
  "safe": false,
  "blocked": true,
  "risk_score": 0.95,
  "processing_time_ms": 12,
  "matches": [
    {
      "category": "instruction_override",
      "severity": "critical",
      "pattern": "ignore_previous_rules",
      "matched_text": "...",
      "description": "Detected attempt to override system behavior"
    }
  ],
  "request_id": "abc-123"
}
```

## Pricing

| Plan | Requests/month | Price |
|---|---|---|
| Free | 1,000 | Free |
| Starter | 50,000 | €39.90/mo |
| Pro | 500,000 | €119.90/mo |

Get your free token at [glitchward.com/shield](https://glitchward.com/shield)

## Links

- [LLM Shield Landing Page](https://glitchward.com/shield)
- [LLMPI Database](https://glitchward.com/llmpi) — Free public database of known prompt injection patterns

## License

MIT
