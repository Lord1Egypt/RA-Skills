---
name: lightningprox
description: Pay-per-use AI gateway via Bitcoin Lightning. No API keys, no account — pay sats, get inference. Supports Anthropic (claude-opus-4-6, claude-sonnet-4-6, claude-haiku-4-5-20251001), OpenAI (gpt-4o, gpt-4.1, gpt-4.1-mini and more), Together.ai (Llama 3.3, DeepSeek V4, Qwen), Mistral, and Google Gemini 2.5. L402 protocol or spend token auth.
acceptLicenseTerms: true
metadata:
  clawdbot:
    emoji: "⚡"
    homepage: https://lightningprox.com
    requires:
      env:
        - LIGHTNINGPROX_SPEND_TOKEN
---

# LightningProx — Lightning-Native AI Gateway

Pay-per-use access to AI models across 5 providers via Bitcoin Lightning micropayments. No API keys. No subscriptions. No accounts. Pay sats, get inference. Implements the L402 payment protocol.

## When to Use

- Accessing AI models without provider API keys
- Autonomous agent inference with Lightning payments
- Comparing responses across multiple providers
- Low-cost inference via open models (Llama 3.3, DeepSeek V4, Qwen)
- Vision tasks (multimodal via image_url)
- Reasoning tasks (mistral-medium-3-5, Qwen3.5-397B)

## Supported Models

| Provider | Models (use exact IDs in API calls) |
|----------|--------------------------------------|
| Anthropic | `claude-opus-4-6`, `claude-sonnet-4-6`, `claude-haiku-4-5-20251001` |
| OpenAI | `gpt-4`, `gpt-4-turbo`, `gpt-3.5-turbo`, `gpt-4.1`, `gpt-4.1-mini`, `gpt-4o`, `gpt-4o-mini` |
| Together.ai | `meta-llama/Llama-3.3-70B-Instruct-Turbo`, `deepseek-ai/DeepSeek-V4-Pro`, `Qwen/Qwen2.5-7B-Instruct-Turbo`, `Qwen/Qwen3.5-397B-A17B` |
| Mistral | `mistral-large-latest`, `mistral-small-latest`, `mistral-medium-3-5` |
| Google | `gemini-2.5-flash`, `gemini-2.5-pro` |

## Payment Flow

### Option A — Spend Token (recommended for repeat use)
```bash
# 1. Top up at lightningprox.com/topup — pay Lightning invoice, get token
# 2. Use token directly
curl -X POST https://lightningprox.com/v1/messages \
  -H "Content-Type: application/json" \
  -H "X-Spend-Token: $LIGHTNINGPROX_SPEND_TOKEN" \
  -d '{
    "model": "claude-sonnet-4-6",
    "messages": [{"role": "user", "content": "Hello"}],
    "max_tokens": 1000
  }'
```

### Option B — L402 Pay-per-request (standard protocol)
```bash
# 1. Send request without credentials → receive HTTP 402
curl -si -X POST https://lightningprox.com/v1/messages \
  -H "Content-Type: application/json" \
  -d '{"model": "gemini-2.5-flash", "messages": [{"role": "user", "content": "Hello"}], "max_tokens": 100}'
# Response header: WWW-Authenticate: L402 macaroon="eyJ...", invoice="lnbc..."

# 2. Pay the bolt11 invoice from your Lightning wallet

# 3. Retry with L402 credential (macaroon from header + preimage from wallet)
curl -X POST https://lightningprox.com/v1/messages \
  -H "Content-Type: application/json" \
  -H "Authorization: L402 <macaroon>:<preimage>" \
  -d '{"model": "gemini-2.5-flash", "messages": [{"role": "user", "content": "Hello"}], "max_tokens": 100}'
```

## Drop-in OpenAI SDK Replacement

```bash
npm install lightningprox-openai
```

```javascript
// Before: import OpenAI from 'openai'
import OpenAI from 'lightningprox-openai'
const client = new OpenAI({ apiKey: process.env.LIGHTNINGPROX_SPEND_TOKEN })

// Everything else stays identical:
const response = await client.chat.completions.create({
  model: 'claude-sonnet-4-6',
  messages: [{ role: 'user', content: 'Hello' }]
})
```

Two lines change. Nothing else does.

## Check Available Models
```bash
curl https://lightningprox.com/v1/models
# or
curl https://lightningprox.com/api/capabilities
```

## Security Manifest

| Permission | Scope | Reason |
|------------|-------|--------|
| Network | lightningprox.com | API calls for AI inference |
| Env Read | LIGHTNINGPROX_SPEND_TOKEN | Authentication for prepaid requests |

## Trust Statement

LightningProx is operated by LPX Digital Group LLC. Payment = authentication. No data stored beyond request logs. No accounts, no KYC. Operated at lightningprox.com.
