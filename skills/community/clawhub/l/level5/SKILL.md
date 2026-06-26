---
name: level5
version: 1.6.2
description: Budget Management for AI Agents — USDC billing gateway. Deposit USDC on Solana; pay for LLM compute per token.
homepage: https://level5.cloud
metadata: {"category":"infrastructure","network":"solana","currencies":["USDC"],"supported_providers":["openai","anthropic","openrouter"]}
---

# Level5: Budget Management for AI Agents

**Computational sovereignty is not a feature. It is a right.**

Level5 is a transparent billing proxy between AI agents and LLM providers (OpenAI,
Anthropic, OpenRouter). Agents deposit USDC to a Solana smart contract; Level5 handles
per-token billing with real-time balance tracking.

**Streaming support:** Both streaming (SSE) and non-streaming requests are fully
supported. Claude Code and other clients that default to `stream: true` work out of the
box.

---

## When to Activate

This skill is **passive until the user explicitly requests it.** Do not register,
write files, or make network requests on skill load.

Activate when:
- The user asks to set up Level5, connect a billing account, or use Level5 as a proxy
- The user asks you to register for Level5
- A request fails with `402 Payment Required` and you ask the user if they'd like to fund their account

**Always ask before acting.** Before registering, confirm with the user:

> "I'll create a Level5 billing account at api.level5.cloud. This will route your LLM
> traffic through Level5 for per-token billing. I'll give you a dashboard URL to save —
> that URL is your account. Shall I proceed?"

Only proceed after the user confirms.

### Registration

```python
import requests


def register_level5() -> dict:
    """Register with Level5 and return credentials.

    Only call this after the user has explicitly confirmed they want to proceed.
    No files are written. The dashboard URL is displayed for the user to save.
    """
    reg = requests.post("https://api.level5.cloud/v1/register", timeout=10).json()
    api_token = reg["api_token"]
    dashboard_url = f"https://level5.cloud/dashboard/{api_token}"

    print(
        f"\n{'─' * 60}\n"
        f"  Level5 account created.\n\n"
        f"  Your dashboard URL — save this somewhere safe:\n\n"
        f"    {dashboard_url}\n\n"
        f"  This URL is your account portal. It contains your API token\n"
        f"  and lets you deposit USDC, view your balance, and get SDK\n"
        f"  configuration instructions.\n\n"
        f"  ⚠ There is no account recovery. If you lose this URL,\n"
        f"  you will need to register again.\n"
        f"{'─' * 60}\n"
    )

    return {"api_token": api_token, "dashboard_url": dashboard_url}
```

---

## Version Check

This skill is versioned (semver, frontmatter `version` field). The canonical source is
`https://level5.cloud/SKILL.md`.

**Never auto-update.** Overwriting skill files silently is a security risk — a
compromised remote could change your agent's instructions. Version checks are
opt-in: only run when the user explicitly asks (e.g. "check for Level5 skill updates").

```python
import re
import requests
from pathlib import Path

SKILL_URL = "https://level5.cloud/SKILL.md"


def check_skill_version(local_path: Path) -> None:
    """Fetch remote SKILL.md version and alert if a newer version exists.

    Never overwrites the local file. Call only when the user explicitly asks
    to check for updates — do not run automatically on startup or on a schedule.
    """
    try:
        remote_text = requests.get(SKILL_URL, timeout=10).text
    except Exception:
        return

    def parse_version(text: str) -> str:
        m = re.search(r"^version:\s*(\S+)", text, re.MULTILINE)
        return m.group(1) if m else "0.0.0"

    from packaging.version import Version
    local_version = parse_version(local_path.read_text())
    remote_version = parse_version(remote_text)

    if Version(remote_version) > Version(local_version):
        print(
            f"\n[Level5] A new skill version is available: "
            f"{local_version} → {remote_version}\n"
            f"  Ask me to upgrade the Level5 skill to get the latest "
            f"models, pricing, and features.\n"
        )
    else:
        print(f"\n[Level5] Skill is up to date (v{local_version}).\n")
```

---

## Service Discovery

Machine-readable service descriptor:

```
https://level5.cloud/.well-known/agent-service.json
```

Agent frameworks and orchestrators can fetch this to auto-configure Level5 without
manual setup.

---

## Three-Step Onboarding

### Step 1: Register

```bash
curl -X POST https://api.level5.cloud/v1/register
```

**Response:**
```json
{
  "api_token": "abc-123-def-456",
  "deposit_code": "A1B2C3D4E5F6A7B8",
  "status": "pending_deposit",
  "instructions": {
    "contract_address": "<sovereign_contract_address>",
    "dashboard_url": "https://level5.cloud/dashboard/abc-123-def-456"
  }
}
```

### Step 2: Fund and Configure

Visit your dashboard URL to deposit USDC and get SDK configuration instructions for
Claude Code, Codex, OpenCode, and Cursor. All setup steps are on the dashboard.

```
https://level5.cloud/dashboard/{YOUR_API_TOKEN}
```

---

## Dashboard

Once registered, your dashboard is available at:

```
https://level5.cloud/dashboard/{YOUR_API_TOKEN}
```

The dashboard shows your USDC balance, deposit and usage history, and agent connection
instructions for Claude Code, Codex, OpenCode, and Cursor.

**Bookmark it.** This URL is the only way to access your dashboard without re-registering.

**For agents:** If a user asks how to find their dashboard, construct the URL from their
`api_token` and provide it directly:
```python
dashboard_url = f"https://level5.cloud/dashboard/{api_token}"
print(f"Your dashboard: {dashboard_url}")
```

---

## API Reference

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| GET    | `/health` | None | Service health — returns component status |
| GET    | `/v1/pricing` | None | Current model pricing |
| POST   | `/v1/register` | None | Register new agent, get API token + deposit code |
| GET    | `/proxy/{api_token}/balance` | Token in path | Check USDC balance |
| GET    | `/proxy/{api_token}/transactions` | Token in path | Transaction history |
| POST   | `/proxy/{api_token}/v1/chat/completions` | Token in path | OpenAI-format proxy |
| POST   | `/proxy/{api_token}/v1/messages` | Token in path | Anthropic-format proxy |

---

### GET /health

```bash
curl https://api.level5.cloud/health
```

**Response (healthy):** HTTP 200
```json
{
  "status": "ok",
  "version": "1.0.0",
  "components": {
    "redis": "ok",
    "postgres": "ok"
  }
}
```

**Response (degraded):** HTTP 503
```json
{
  "status": "degraded",
  "version": "1.0.0",
  "components": {
    "redis": "ok",
    "postgres": "error"
  }
}
```

---

### POST /v1/register

```bash
curl -X POST https://api.level5.cloud/v1/register
```

**Response:** HTTP 200
```json
{
  "api_token": "abc-123-def-456",
  "deposit_code": "A1B2C3D4E5F6A7B8",
  "status": "pending_deposit",
  "instructions": {
    "contract_address": "BBAdcqUkg68JXNiPQ1HR1wujfZuayyK3eQTQSYAh6FSW",
    "dashboard_url": "https://level5.cloud/dashboard/abc-123-def-456"
  }
}
```

Rate limited to 10 requests per minute per IP.

---

### GET /v1/pricing

```bash
curl https://api.level5.cloud/v1/pricing
```

**Response:** HTTP 200
```json
{
  "pricing": {
    "anthropic/claude-sonnet-4-6": {
      "input_per_1m": 3300000,
      "output_per_1m": 16500000,
      "cache_write_per_1m": 4125000,
      "cache_read_per_1m": 330000
    },
    "anthropic/claude-opus-4-6": {
      "input_per_1m": 5500000,
      "output_per_1m": 27500000,
      "cache_write_per_1m": 6875000,
      "cache_read_per_1m": 550000
    }
  },
  "currency": "USDC",
  "denomination": "microunits (6 decimals, 1 USDC = 1_000_000)"
}
```

---

### GET /proxy/{api_token}/balance

```bash
curl https://api.level5.cloud/proxy/{YOUR_API_TOKEN}/balance
```

**Response:** HTTP 200
```json
{
  "api_token": "abc-123-def-456",
  "usdc_balance": 5000000,
  "is_active": true
}
```

`usdc_balance` is in USDC microunits (6 decimals). 5 000 000 = 5.00 USDC.

---

### GET /proxy/{api_token}/transactions

```bash
curl "https://api.level5.cloud/proxy/{YOUR_API_TOKEN}/transactions?page=1&limit=50"
```

**Response:** HTTP 200
```json
{
  "api_token": "abc-123-def-456",
  "page": 1,
  "limit": 50,
  "transactions": [
    {
      "id": 1,
      "type": "DEPOSIT",
      "usdc_amount": 10000000,
      "provider": null,
      "model": null,
      "input_tokens": null,
      "output_tokens": null,
      "cache_write_tokens": null,
      "cache_read_tokens": null,
      "created_at": "2026-02-22T10:00:00+00:00"
    },
    {
      "id": 2,
      "type": "DEBIT",
      "usdc_amount": -330,
      "provider": "anthropic",
      "model": "claude-sonnet-4-6",
      "input_tokens": 15,
      "output_tokens": 25,
      "cache_write_tokens": null,
      "cache_read_tokens": 120,
      "created_at": "2026-02-22T10:01:00+00:00"
    }
  ]
}
```

---

### POST /proxy/{api_token}/v1/messages

Anthropic-compatible. Supports streaming (`stream: true`) and non-streaming.

```bash
curl https://api.level5.cloud/proxy/{YOUR_API_TOKEN}/v1/messages \
  -H "Content-Type: application/json" \
  -d '{
    "model": "claude-sonnet-4-6",
    "max_tokens": 1024,
    "stream": true,
    "messages": [{"role": "user", "content": "Hello"}]
  }'
```

**Response headers include:**
```
X-Balance-Remaining: 4999670
```

---

### POST /proxy/{api_token}/v1/chat/completions

OpenAI-compatible. Supports streaming and non-streaming.

```bash
curl https://api.level5.cloud/proxy/{YOUR_API_TOKEN}/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gpt-4o",
    "stream": true,
    "messages": [{"role": "user", "content": "Hello"}]
  }'
```

**Response headers include:**
```
X-Balance-Remaining: 4999670
```

---

## X-Balance-Remaining Header

Every proxy response includes `X-Balance-Remaining` — the agent's current USDC balance
in microunits after the request is processed. Agents can use this to track spend without
polling the balance endpoint.

```python
response = client.messages.create(...)
remaining = int(response.headers.get("x-balance-remaining", 0))
if remaining < 1_000_000:  # < 1 USDC
    alert("Balance low — please top up")
```

---

## Cache Billing

Anthropic models support prompt caching. Level5 tracks cache write and read
tokens separately and bills them at the rates shown in /v1/pricing.

- `cache_write_tokens`: tokens written to a new cache block (1.25x base input rate)
- `cache_read_tokens`: tokens served from cache (0.10x base input rate — 10x cheaper)

Both fields are visible in transaction records and factored into X-Balance-Remaining.

---

## Integration Examples

### Python — Anthropic SDK

```python
import anthropic

client = anthropic.Anthropic(
    base_url="https://api.level5.cloud/proxy/{YOUR_API_TOKEN}",
    api_key="level5",
)

response = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Analyze market conditions"}],
)
print(response.content[0].text)
```

### Python — OpenAI SDK

```python
from openai import OpenAI

client = OpenAI(
    base_url="https://api.level5.cloud/proxy/{YOUR_API_TOKEN}/v1",
    api_key="level5",
)

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "Analyze market conditions"}],
)
print(response.choices[0].message.content)
```

### After Registration

```python
# User has confirmed setup and saved their dashboard URL.
# Use the api_token returned by register_level5() to configure the SDK.
creds = register_level5()  # call only after user confirms
api_token = creds["api_token"]

import anthropic
client = anthropic.Anthropic(
    base_url=f"https://api.level5.cloud/proxy/{api_token}",
    api_key="level5",
)
```

---

## Error Codes

| Code | Meaning | Action |
|------|---------|--------|
| 200  | Success | Request completed, balance debited |
| 400  | Bad Request | Invalid JSON body |
| 401  | Unauthorized | Invalid or inactive API token |
| 402  | Payment Required | Insufficient USDC balance — deposit more |
| 429  | Rate Limited | Too many `/v1/register` calls — wait 60s |
| 502  | Upstream Error | LLM provider error — retry with backoff |
| 503  | Service Unavailable | Level5 infrastructure issue — check `/health` |

---

## Supported Models

Prices in USDC microunits per 1M tokens (6 decimals, 1 USDC = 1 000 000).

| Provider    | Model                         | Input/1M   | Output/1M  | Cache Read/1M |
|-------------|-------------------------------|------------|------------|---------------|
| anthropic   | `claude-sonnet-4-6`           | 3 300 000  | 16 500 000 | 330 000       |
| anthropic   | `claude-opus-4-6`             | 5 500 000  | 27 500 000 | 550 000       |
| anthropic   | `claude-haiku-4-5-20251001`   | 1 100 000  | 5 500 000  | 110 000       |
| openai      | `gpt-5.2`                     | 1 750 000  | 14 000 000 | 175 000       |
| openai      | `gpt-5.3-codex`               | 1 750 000  | 14 000 000 | 175 000       |
| openai      | `gpt-4o`                      | 2 500 000  | 10 000 000 | 1 250 000     |
| openai      | `o3`                          | 2 000 000  | 8 000 000  | 500 000       |
| openrouter  | `qwen3-max`                   | 1 320 000  | 6 600 000  | 264 000       |
| openrouter  | `qwen3-coder-plus`            | 1 100 000  | 5 500 000  | 220 000       |
| openrouter  | `glm-5`                       | 1 100 000  | 3 520 000  | 220 000       |
| openrouter  | `grok-4-1-fast`               | 220 000    | 550 000    | 55 000        |
| openrouter  | `gemini-3.1-pro-preview`      | 2 200 000  | 13 200 000 | 550 000       |

Anthropic and OpenRouter prices include the Level5 10% markup. OpenAI prices are
list rates; runtime markup applied. Use `GET /v1/pricing` for live rates.

---

**Computational sovereignty is not a feature. It is a right.**
