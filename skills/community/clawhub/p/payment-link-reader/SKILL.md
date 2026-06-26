---
name: payment-link-reader
description: Fetch product info by payment link ID. Calls GStable API to get payment link details, returns product name, description, price, and supported payment tokens. Ideal for AI assistants parsing payment links and displaying product information.
metadata: {"openclaw":{"emoji":"🔗","homepage":"https://docs.gstable.io/zh-Hans/docs/api/ai-payment/get-payment-link/","requires":{"bins":["node"]},"install":[{"id":"npm-install","kind":"shell","command":"npm install","label":"Install payment-link-reader (npm)"}]}}
---

# Payment Link Reader

A skill that fetches product information from a GStable Payment Link. It calls the [GStable API - Get Payment Link](https://docs.gstable.io/zh-Hans/docs/api/ai-payment/get-payment-link/) endpoint and returns product details and supported payment methods.

## Flow

```
Call API (GET /payment/link/:linkId)
        ↓
Return product info (name, description, price, payment tokens)
```

## Installation (OpenClaw)

```bash
clawhub install payment-link-reader
cd ~/.openclaw/skills/payment-link-reader
npm install
```

For manual installation, copy the `payment-link-reader` directory to `~/.openclaw/skills/` or `./skills/`, then run `npm install`.

## Usage

```bash
# Fetch product info by link_id
npm run get-link -- <link_id>
```

**Example:**
```bash
npm run get-link -- lnk_BUDBgiGTWejFs8v0FbdpR3iJ83CG1tua
```

**Output format (JSON):**
```json
{
  "linkId": "lnk_xxx",
  "linkName": "Premium Membership",
  "products": [
    {
      "name": "Premium Plan",
      "description": "Unlock all features",
      "imageUrl": "https://example.com/image.png",
      "quantity": 1,
      "unitPriceUSD": "1.00",
      "attributes": [{ "name": "Duration", "value": "1 Month" }]
    }
  ],
  "supportedPaymentTokens": [
    {
      "symbol": "USDC",
      "chainName": "Polygon",
      "chainId": "137",
      "amountInUSD": "3.00"
    }
  ]
}
```

## API Reference

| Field | Description |
|-------|-------------|
| **Endpoint** | `GET /payment/link/:linkId` |
| **Base URL** | `https://aipay.gstable.io/api/v1` (override via `GSTABLE_API_BASE_URL`) |
| **Parameters** | `link_id` required, format `lnk_xxx` |
| **Documentation** | [Get Payment Link | GStable Docs](https://docs.gstable.io/zh-Hans/docs/api/ai-payment/get-payment-link/) |

## Agent Invocation Example

When the user provides a payment link or link_id, the Agent should run the following in the skill root directory:

```bash
npm run get-link -- <link_id>
```

**Conversation example:**

```
User: What's in this payment link lnk_BUDBgiGTWejFs8v0FbdpR3iJ83CG1tua?

Agent: [cd {baseDir} && npm run get-link -- lnk_BUDBgiGTWejFs8v0FbdpR3iJ83CG1tua]
       "This payment link contains: Premium Plan (1.00 USD each), supports USDC on Polygon, total 3.00 USD"
```

**Note:** `{baseDir}` is the skill directory path. Ensure `npm install` has been run before execution.

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `GSTABLE_API_BASE_URL` | No | API base URL, default `https://aipay.gstable.io/api/v1` |

## Response Format

When responding to the user, summarize the payment link information in a readable format including:

- Product name
- Product description
- Unit price
- Supported payment tokens
- Blockchain network

## Use Cases

- AI assistant parsing user-shared payment links
- Displaying product list from payment links
- Fetching supported chains and token info
- Validating link before payment
