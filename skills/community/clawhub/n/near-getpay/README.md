# 💳 NEAR GetPay - Crypto Payment Pages Made Easy

Accept cryptocurrency payments (NEAR, USDC, USDT) through a beautiful hosted payment page with PingPay or HOT PAY integration.

[![OpenClaw Skill](https://img.shields.io/badge/OpenClaw-Skill-blue)](https://openclaw.ai)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)

## 🌟 Features

- ✨ **Beautiful payment UI** - Mobile-responsive with preset amounts
- 💰 **Multi-token support** - Accept NEAR, USDC, or USDT
- 🔄 **Dual provider** - Works with PingPay or HOT PAY
- 🌐 **Public URLs** - Automatic tunnel via localhost.run
- 🧙 **Setup wizard** - Guides first-time users step-by-step
- 🔒 **Secure** - No private keys needed, HTTPS enforced
- 🎯 **Smart token selection** - Once token selected, other options hide (HOT PAY flow)

## 💡 How It Works

### PingPay Flow
1. User selects token (NEAR/USDC/USDT)
2. Enters amount or picks preset
3. Clicks "Pay Now" → Redirects to PingPay checkout

### HOT PAY Flow
1. User sees only configured tokens (those with item_ids)
2. Selects token → **Other tokens hide automatically**
3. Enters amount → Redirects to specific HOT PAY link for that token
4. Each token has its own checkout URL (configured in HOT PAY dashboard)

## 🚀 Quick Start

### 1. Clone & Install

```bash
cd ~/.openclaw/skills
git clone https://github.com/yourusername/near-getpay.git
cd near-getpay
npm install
```

### 2. Configure Provider

**Choose ONE (or both):**

#### Option A: PingPay (Recommended)

1. Sign up at [pingpay.io](https://pingpay.io)
2. Set your NEAR wallet in Dashboard → Settings
3. Get API key from Dashboard → Settings → API Keys
4. Add to `.env`:

```env
RECIPIENT_ADDRESS=your-account.near
PAYMENT_PROVIDER=pingpay
PINGPAY_API_KEY=your_api_key_here
```

#### Option B: HOT PAY

1. Visit [HOT PAY Admin](https://pay.hot-labs.org/admin/overview)
2. Create payment links for each token (NEAR, USDC, USDT)
3. Set your NEAR wallet as recipient for each link
4. Copy each `item_id` and add to `.env`:

```env
RECIPIENT_ADDRESS=your-account.near
PAYMENT_PROVIDER=hotpay
HOTPAY_NEAR_ITEM_ID=your_near_item_id
HOTPAY_USDC_ITEM_ID=your_usdc_item_id
HOTPAY_USDT_ITEM_ID=your_usdt_item_id
```

### 3. Start Server

```bash
./start.sh
```

You'll see output like:

```
✅ GetPay server running on port 3000
🌐 PUBLIC URL:
   https://abc123xyz.lhr.life

📱 Share this link to receive payments!
```

### 4. Accept Payments!

Share the generated URL and start receiving crypto payments instantly.

## 📸 Screenshots

### Payment Page
![Payment Page](https://via.placeholder.com/600x400?text=Beautiful+Payment+UI)

### Setup Wizard
![Setup Wizard](https://via.placeholder.com/600x400?text=First-Time+Setup+Wizard)

## ⚠️ Important: Recipient Configuration

**The recipient address (where payments go) is set at the provider level:**

- **PingPay**: Dashboard → Settings → Wallet Address
- **HOT PAY**: Set when creating each payment link

The `RECIPIENT_ADDRESS` in `.env` is **only for display** on your payment page.

## 🎯 Use Cases

- 💝 Accept donations on your website
- 🛍️ Sell digital products
- ☕ "Buy me a coffee" in crypto
- 💰 Freelance payments
- 🎁 Gift registries
- 📱 Mobile-friendly tipping

## 🔗 API - Generate Payment Links

**NEW:** Use the `/quick-link` endpoint to instantly generate both payment page and direct checkout links!

### Endpoint

```
GET /quick-link?amount={amount}&token={token}
```

### Example

```bash
curl "https://your-domain.lhr.life/quick-link?amount=5&token=USDC"
```

### Response

```json
{
  "success": true,
  "amount": 5,
  "token": "USDC",
  "recipient": "your-account.near",
  "provider": "pingpay",
  "links": {
    "paymentPage": "https://your-domain.lhr.life/?amount=5&token=USDC",
    "directCheckout": "https://pay.pingpay.io/checkout?sessionId=cs_..."
  }
}
```

### Use Cases

- **Share both links with customers** (beautiful UI + fallback)
- **Programmatically generate payment links** for invoices
- **Embed in your app/bot** to create checkout sessions
- **Pre-fill payment amounts** from your backend

### Supported Tokens

- `NEAR` - NEAR Protocol
- `USDC` - USD Coin (on NEAR)
- `USDT` - Tether (on NEAR)

**Example usage:**
```bash
# $10 USDC payment
curl "/quick-link?amount=10&token=USDC"

# 5 NEAR payment
curl "/quick-link?amount=5&token=NEAR"

# $25 USDT payment
curl "/quick-link?amount=25&token=USDT"
```

## 🛠️ OpenClaw Integration

This skill works seamlessly with OpenClaw. Example conversation:

```
You: Create a payment page for me

Agent: I'll set up GetPay for you. Do you have PingPay or HOT PAY?

You: What's easier?

Agent: PingPay is simpler! Here's what to do:
       1. Sign up at pingpay.io
       2. Add your wallet in settings
       3. Get an API key
       Share the key and I'll handle the rest!

You: Here's my key: sk_live_abc123...

Agent: Perfect! Starting your payment server...
       ✅ Live at: https://xyz789.lhr.life
       Share this link to accept payments!
```

## 📖 Documentation

- [SKILL.md](SKILL.md) - Complete skill documentation
- [OpenClaw Docs](https://docs.openclaw.ai) - OpenClaw documentation
- [PingPay Docs](https://pingpay.io/docs) - PingPay API reference
- [HOT PAY Docs](https://pay.hot-labs.org/admin) - HOT PAY dashboard

## 🔧 Configuration

### Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `RECIPIENT_ADDRESS` | ✅ | Display name (actual recipient set in provider dashboard) |
| `PAYMENT_PROVIDER` | ✅ | `pingpay` or `hotpay` |
| `PINGPAY_API_KEY` | For PingPay | Your PingPay API key |
| `HOTPAY_NEAR_ITEM_ID` | For HOT PAY | NEAR payment link item_id |
| `HOTPAY_USDC_ITEM_ID` | For HOT PAY | USDC payment link item_id |
| `HOTPAY_USDT_ITEM_ID` | For HOT PAY | USDT payment link item_id |
| `PORT` | ❌ | Server port (default: 3000) |

### Custom Tunnel

Don't like localhost.run? Edit `start-tunnel.ts` to use:

- ngrok
- Cloudflare Tunnel
- localtunnel
- Your own reverse proxy

## 🎨 Customization

### Change Preset Amounts

Edit `server-simple.ts`:

```typescript
tokens: [
  {
    symbol: 'NEAR',
    presets: [1, 5, 10, 25]  // Your amounts
  }
]
```

### Branding

Update colors, fonts, and text in the HTML templates in `server-simple.ts`.

### Add Tokens

Add more tokens to the config (requires provider support):

```typescript
{
  symbol: 'ETH',
  chain: 'NEAR',
  decimals: 18,
  presets: [0.01, 0.05, 0.1]
}
```

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| "No provider configured" | Visit `/setup` page for instructions |
| "Permission denied" (SSH) | Run `ssh-keygen -t rsa -f ~/.ssh/id_rsa -N ""` |
| "Tunnel closed" | Restart server (localhost.run has timeouts) |
| "Token not configured" | Create payment link for that token in HOT PAY |
| Provider errors | Verify API key / item_ids are correct |

## 🔐 Security Best Practices

- ✅ Never commit `.env` to git
- ✅ Use environment variables for secrets
- ✅ Rotate API keys periodically
- ✅ Use HTTPS (enforced by tunnels)
- ✅ Verify webhook signatures (HOT PAY)

## 📦 Sharing

### Install from GitHub

```bash
cd ~/.openclaw/skills
git clone https://github.com/yourusername/near-getpay.git
cd near-getpay
npm install
```

### Skill Package

```bash
openclaw skill pack
openclaw skill install near-getpay.skill
```

### Clawhub

Upload to [Clawhub](https://clawhub.com) for one-click installation.

## 🤝 Contributing

PRs welcome! Areas that need help:

- [ ] More payment providers (Stripe Crypto, Coinbase Commerce)
- [ ] Better analytics/dashboard
- [ ] Email notifications
- [ ] Custom domain support
- [ ] Multi-language support

## 📝 License

MIT - See [LICENSE](LICENSE)

## 🙏 Credits

- [NEAR Protocol](https://near.org) - Blockchain infrastructure
- [PingPay](https://pingpay.io) - Payment gateway
- [HOT PAY](https://pay.hot-labs.org) - Payment links
- [OpenClaw](https://openclaw.ai) - AI agent framework
- [localhost.run](https://localhost.run) - Free tunneling

## 📬 Support

- 🐛 Issues: [GitHub Issues](https://github.com/yourusername/near-getpay/issues)
- 💬 Discord: [OpenClaw Community](https://discord.com/invite/clawd)
- 📧 Email: your@email.com

---

**Made with 🐾 for OpenClaw**
