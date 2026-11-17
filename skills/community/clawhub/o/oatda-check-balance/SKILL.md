---
name: oatda-check-balance
description: Check OATDA account balance, remaining credits, and total usage via the unified AI gateway. Triggers when the user asks "how much OATDA credit do I have left", "is my budget enough for this AI call", "what's my OATDA usage", "am I out of credits", "verify balance before image/video/LLM generation". Returns current balance, usage spent, and available remaining amount. Useful for budget checks before expensive image, video, or long-running LLM calls.
homepage: https://oatda.com
metadata:
  {
    "openclaw":
      {
        "emoji": "💳",
        "requires": { "bins": ["curl", "jq"], "env": ["OATDA_API_KEY"], "config": ["~/.oatda/credentials.json"] },
        "primaryEnv": "OATDA_API_KEY",
      },
  }
---

# OATDA Check Balance

Check the current OATDA account balance, total usage, and available remaining credits. Run this before expensive AI calls (video generation, batch image generation, long LLM streams) to confirm budget.

## API Key Resolution

All commands need the OATDA API key. Resolve it inline for each `exec` call:

```bash
export OATDA_API_KEY="${OATDA_API_KEY:-$(cat ~/.oatda/credentials.json 2>/dev/null | jq -r '.profiles[.defaultProfile].apiKey' 2>/dev/null)}"
```

If the key is empty or `null`, tell the user to get one at https://oatda.com and configure it.

**Security**: Never print the full API key. Only verify existence or show first 8 chars.

## API Call

```bash
export OATDA_API_KEY="${OATDA_API_KEY:-$(cat ~/.oatda/credentials.json 2>/dev/null | jq -r '.profiles[.defaultProfile].apiKey' 2>/dev/null)}" && \
curl -s -X GET "https://oatda.com/api/v1/user/credits" \
  -H "Authorization: Bearer $OATDA_API_KEY"
```

## Response

```json
{
  "id": "uuid",
  "userId": "uuid",
  "balance": 25.00,
  "updatedAt": "2026-06-22T14:30:00.000Z",
  "usageSum": 7.42,
  "actualBalance": 17.58
}
```

| Field | Type | Meaning |
|-------|------|---------|
| `balance` | number | Top-up total (credits ever purchased) |
| `usageSum` | number | Total amount consumed by API calls so far |
| `actualBalance` | number | **What the user can still spend** = `balance - usageSum` |
| `updatedAt` | ISO timestamp | Last time the balance row was refreshed |

The **actionable number** for "how much budget do I have left?" is `actualBalance`.

## Present results

```
OATDA Balance
─────────────────────────────
Available:  €17.58
Spent:      €7.42
Top-up:     €25.00
```

If `actualBalance` is `0` or negative, tell the user to top up at https://oatda.com/dashboard/credits (minimum €1, credit card or PayPal).

## Errors

| HTTP | Meaning | Action |
|------|---------|--------|
| 401 | Invalid or missing API key | Get one at https://oatda.com/dashboard/api-keys |
| 403 | Authenticated but not allowed | Account may be suspended — contact support |
| 500 | Database error | Retry once; if persists, report |

## Example

User: "Do I have enough credits for a 10-second video?"

```bash
export OATDA_API_KEY="${OATDA_API_KEY:-$(cat ~/.oatda/credentials.json 2>/dev/null | jq -r '.profiles[.defaultProfile].apiKey' 2>/dev/null)}" && \
curl -s -X GET "https://oatda.com/api/v1/user/credits" \
  -H "Authorization: Bearer $OATDA_API_KEY"
```

If `actualBalance >= ~€0.50` (rough Veo / Seedance price for 10s), proceed with `oatda-generate-video`. Otherwise tell the user to top up first.

## Tips

- This is a GET request — no body needed.
- Always check balance before expensive calls (video generation, batch image generation, long-running streaming).
- `actualBalance` is the canonical "remaining budget" number — `balance` alone is misleading.
- Minimum top-up is €1. Methods: credit card, PayPal.
- For per-model pricing before you call, run `oatda-list-models`.
- NEVER expose the full API key in output.
