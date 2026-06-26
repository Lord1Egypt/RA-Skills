# Payment Link Reader

Fetch product information from GStable payment links. This skill calls the GStable API to retrieve payment link details and returns product names, descriptions, prices, and supported payment tokens.

## What It Does

- Accepts a payment link ID (`lnk_xxx`) or full payment URL
- Fetches product details from GStable API
- Returns structured JSON with products and supported payment tokens
- Designed for AI assistants to parse and summarize payment link content

## Requirements

- **Node.js** 18+ (for `fetch` and ES modules)
- **npm** or **pnpm**
- No API keys required (uses public GStable API)

## Installation

### Via ClawHub

```bash
clawhub install payment-link-reader
cd ~/.openclaw/skills/payment-link-reader
npm install
```

### Manual

1. Copy the `payment-link-reader` directory to `~/.openclaw/skills/` or `./skills/`
2. Run `npm install`

## How to Use

```bash
# By link ID
npm run get-link -- lnk_BUDBgiGTWejFs8v0FbdpR3iJ83CG1tua

# By full URL
npm run get-link -- "https://pay.gstable.io/link/lnk_xxx"
```

## Examples

**Input:**
```bash
npm run get-link -- lnk_BUDBgiGTWejFs8v0FbdpR3iJ83CG1tua
```

**Output (JSON):**
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

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `GSTABLE_API_BASE_URL` | No | API base URL. Default: `https://aipay.gstable.io/api/v1` |

## API Reference

| Field | Value |
|-------|-------|
| Endpoint | `GET /payment/link/:linkId` |
| Base URL | `https://aipay.gstable.io/api/v1` |
| Link ID format | `lnk_[a-zA-Z0-9_]+` |
| Docs | [GStable - Get Payment Link](https://docs.gstable.io/zh-Hans/docs/api/ai-payment/get-payment-link/) |

## Troubleshooting

| Issue | Solution |
|-------|----------|
| `Error: Please provide a valid link_id` | Ensure input is `lnk_xxx` format or a valid payment URL |
| `API Error: ...` | Check network, verify link ID exists, or try different base URL via `GSTABLE_API_BASE_URL` |
| `Invalid response: missing lineItems` | API returned unexpected format; link may be invalid or API changed |
| `command not found: tsx` | Run `npm install` in the skill directory |

## Publishing to ClawHub

Before publishing, exclude `node_modules` and `.git`:

```bash
rsync -av --exclude=.git --exclude=node_modules ./payment-link-reader/ /tmp/payment-link-reader-pub/
clawhub publish /tmp/payment-link-reader-pub --slug payment-link-reader --name "Payment Link Reader" --version 1.0.0 --tags latest --changelog "Initial release"
```

## License

MIT
