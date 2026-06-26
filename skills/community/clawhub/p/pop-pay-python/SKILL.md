---
name: pop-pay
version: "0.6.23"
description: "Your card stays on your PC — no SaaS, no login, no external account. Credentials inject directly, keeping them out of the AI's context window."
homepage: https://github.com/TPEmist/Point-One-Percent
author: Point One Percent
license: MIT
requires:
  bins:
    - pop-pay
  env:
    - POP_ALLOWED_CATEGORIES
    - POP_MAX_AMOUNT_PER_TX
    - POP_MAX_DAILY_BUDGET
    - POP_AUTO_INJECT
    - POP_REQUIRE_HUMAN_APPROVAL
    - POP_GUARDRAIL_ENGINE
---

## What This Skill Does

Gives your OpenClaw agent the ability to pay at any online store using **your own existing credit card** — no account to create, no SaaS subscription, no external service to trust.

Your card number is stored in your **local system keychain** and is **never placed in the agent's context window**. When payment is approved, credentials are injected directly into the browser's payment form via CDP (Chrome DevTools Protocol — an open protocol maintained by Google) in a separate process — the agent never sees them. If your agent is compromised by a prompt injection attack, the attacker cannot steal your card.

---

## Privacy & Data Flow

All payment logic runs **on your machine**. There are no Point One Percent servers involved in the payment path.

| Component | Default | Data stays |
|---|---|---|
| Card credentials | Local system keychain | Your machine only |
| Spend policy | `~/.config/pop-pay/.env` | Your machine only |
| Guardrail engine | `keyword` mode (zero API calls) | Your machine only |
| Guardrail engine (optional) | `llm` mode — uses your own API key | Your API provider |
| Webhook notifications | **Disabled by default** — only active if `POP_WEBHOOK_URL` is set | Your chosen endpoint |

**Keyword guardrail** (default): evaluates transactions locally with no external calls.
**LLM guardrail** (opt-in): uses your own `POP_LLM_API_KEY` — no data is sent to Point One Percent.

---

## Setup (One Time)

```bash
# Install from PyPI (https://pypi.org/project/pop-pay/)
pip install pop-pay
pop-pay setup          # securely stores your card in the system keychain
pop-pay setup --profile   # stores billing info (name, address, email)
```

Then add to your OpenClaw config:

```json
{
  "mcpServers": {
    "pop-pay": {
      "command": "pop-pay",
      "args": ["serve"]
    }
  }
}
```

Set your spend policy in `~/.config/pop-pay/.env`:

```
POP_ALLOWED_CATEGORIES=["amazon","shopify","aws"]
POP_MAX_AMOUNT_PER_TX=100
POP_MAX_DAILY_BUDGET=300
POP_AUTO_INJECT=true          # set to false to review injections manually
POP_REQUIRE_HUMAN_APPROVAL=false  # set to true for manual confirmation on every payment
```

---

## Tools

### `request_purchaser_info`

**When to call**: You are on a contact/billing info page with fields for name, email, phone, or address — but no credit card fields are visible yet.

```
request_purchaser_info(
    target_vendor: str,   # e.g. "Amazon", "Shopify" — NOT a URL
    page_url: str,        # current browser page URL
    reasoning: str        # why you are filling this form
)
```

- Injects name, email, phone, and address from the user's stored profile
- Does NOT issue a card, does NOT charge anything, does NOT affect the budget
- After this completes, navigate to the payment page and call `request_virtual_card`

---

### `request_virtual_card`

**When to call**: You are on the checkout/payment page and credit card input fields are visible.

```
request_virtual_card(
    requested_amount: float,  # exact amount shown on screen
    target_vendor: str,       # e.g. "Amazon" — NOT a URL
    reasoning: str,           # explain why this purchase should happen
    page_url: str             # current checkout page URL
)
```

- Evaluates the purchase against the user's spend policy (amount limits, allowlist)
- Runs a guardrail check: evaluates whether this purchase **should** happen given the agent's current task context — not just whether it **can** (within budget)
- Automatically scans the checkout page for prompt injection attacks before issuing the card
- If approved, credentials are injected directly into the browser form via CDP — never passed to the agent
- Returns: `approved` (with last 4 digits) or `rejected` (with reason)

**After approval**: Click the submit/pay button. The card has been filled automatically.

---

## Usage Flow

```
Agent navigates to product page
  ↓
Agent clicks "Checkout" / "Proceed to payment"
  ↓
[If billing page appears first]
  → call request_purchaser_info(vendor, page_url, reasoning)
  → click Continue/Next
  ↓
[When payment/card fields are visible]
  → call request_virtual_card(amount, vendor, reasoning, page_url)
     (security scan runs automatically inside this call)
  ↓
[If approved]
  → click Submit / Place Order
```

---

## Security Model

| Property | pop-pay |
|---|---|
| Card number in agent context | Never |
| Stored locally (no external account) | Yes — system keychain |
| Works with existing credit card | Yes |
| Works with any merchant | Yes (any checkout form) |
| No SaaS / no login required | Yes |
| Guardrail (SHOULD vs CAN) | Yes — keyword or LLM mode |
| Prompt injection scan on every payment | Yes — automatic |
| Open source / auditable | MIT |

**Prompt injection resistance**: The card is injected by a separate local process (CDP injector) that activates only after guardrail approval. A malicious merchant cannot steal the card via hidden DOM instructions — the agent never had it.

---

## Spend Policy Reference

| Env var | Default | Description |
|---|---|---|
| `POP_ALLOWED_CATEGORIES` | `[]` | JSON array of allowed vendor keywords |
| `POP_MAX_AMOUNT_PER_TX` | required | Max per transaction (USD) |
| `POP_MAX_DAILY_BUDGET` | required | Max total spend per day (USD) |
| `POP_GUARDRAIL_ENGINE` | `keyword` | `keyword` (local, zero API cost) or `llm` (semantic, needs API key) |
| `POP_REQUIRE_HUMAN_APPROVAL` | `false` | Always require human confirmation before payment |
| `POP_AUTO_INJECT` | `true` | Enable CDP auto-injection into checkout forms |
| `POP_WEBHOOK_URL` | _(disabled)_ | Optional: POST notifications to Slack/Teams/PagerDuty |

---

## Example: Agent Buys Office Supplies on Amazon

```python
# Agent has been asked: "Order a USB-C hub from Amazon, around $40"

# Step 1: Navigate to Amazon, find the product, add to cart, proceed to checkout

# Step 2: On billing info page
result = request_purchaser_info(
    target_vendor="Amazon",
    page_url="https://www.amazon.com/checkout/address",
    reasoning="Filling billing address for USB-C hub purchase as instructed by user"
)
# → Billing info injected. Click Continue.

# Step 3: On payment page — security scan runs automatically inside this call
result = request_virtual_card(
    requested_amount=43.99,
    target_vendor="Amazon",
    reasoning="Purchasing USB-C hub for home office setup as instructed by user",
    page_url="https://www.amazon.com/checkout/payment"
)
# → Approved. Card injected via CDP. Click "Place your order".
```

---

## GitHub

[github.com/TPEmist/Point-One-Percent](https://github.com/TPEmist/Point-One-Percent)
