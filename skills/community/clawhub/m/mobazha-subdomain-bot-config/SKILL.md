---
name: subdomain-bot-config
description: Set up a custom domain and Telegram Bot for a Mobazha store. Use when the user wants to configure DNS, TLS, or a Telegram Mini App storefront.
---

# Subdomain & Telegram Bot Configuration

Set up a custom domain for your Mobazha store and connect a Telegram Bot for your storefront Mini App.

## Part A: Custom Domain Setup

### For Docker Standalone Stores

If you deployed with the Docker standalone installer:

**Option 1: Set domain during installation**

```bash
curl -sSL https://get.mobazha.org/standalone | sudo bash -s -- --domain shop.example.com
```

**Option 2: Add domain to an existing store**

1. Point your domain's DNS A record to the VPS IP address
2. Wait for DNS propagation (usually 1-5 minutes)
3. Run:

```bash
mobazha-ctl set-domain shop.example.com
```

The store automatically obtains a TLS certificate from Let's Encrypt.

### For Native Binary Stores

Start (or restart) with the domain flag:

```bash
mobazha start --domain shop.example.com
```

### DNS Setup

At your domain registrar (Cloudflare, Namecheap, GoDaddy, etc.), create an **A record**:

| Type | Name | Value | TTL |
|------|------|-------|-----|
| A | shop (or @) | `<VPS_IP>` | Auto / 300 |

If using a subdomain like `shop.example.com`, the "Name" field should be `shop`.
If using the root domain `example.com`, the "Name" field should be `@`.

### Verify

After DNS propagation:

```bash
# Check DNS resolution
dig +short shop.example.com

# Check HTTPS
curl -sI https://shop.example.com | head -5
```

## Part B: Telegram Bot Setup

Mobazha stores can be accessed as a Telegram Mini App via a Telegram Bot. This lets buyers browse and purchase directly inside Telegram.

### Step 1: Create a Bot with BotFather

1. Open Telegram and message [@BotFather](https://t.me/BotFather)
2. Send `/newbot`
3. Choose a display name (e.g., "My Store")
4. Choose a username (e.g., `my_store_bot`) — must end with `bot`
5. BotFather will reply with a **Bot Token** — save it securely

### Step 2: Configure the Mini App URL

Tell BotFather where your store frontend lives:

1. Send `/mybots` to BotFather
2. Select your bot
3. Choose **Bot Settings** → **Menu Button**
4. Set the URL to your store:
   - SaaS store: `https://app.mobazha.org/tma?store=<your-peer-id>`
   - Standalone store: `https://shop.example.com/tma`

### Step 3: Configure the Bot in Your Store

In your store admin panel:

1. Go to **Admin → Settings → Telegram**
2. Enter the Bot Token from BotFather
3. Save

This enables:

- Order notifications in Telegram
- Buyer can message you through the bot
- Mini App storefront accessible via the bot's menu button

### Step 4: Set Bot Description & Photo

Back in BotFather:

1. Send `/mybots` → select your bot
2. **Edit Bot** → **Edit Description**: describe your store
3. **Edit Bot** → **Edit About Text**: short store summary
4. **Edit Bot** → **Edit Botpic**: upload your store logo

### Step 5: Share Your Bot

Your Telegram storefront is now live at:

```
https://t.me/<bot_username>
```

Share this link anywhere — buyers tap the menu button to open your Mini App store.

## Credential Handling

- **Ask for explicit user consent** before connecting to any server or entering credentials
- If the user shares a BotFather token, use it only for the immediate configuration task
- Never store, log, or display credentials after use
- Remind the user to keep tokens and passwords private
- The agent must not transmit credentials to any party other than the intended target
