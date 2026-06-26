---
name: Lead Radar
version: 1.3.5
description: >
  Every morning, scans Reddit, Hacker News, Indie Hackers, Stack Overflow,
  Quora, Hashnode, Dev.to, GitHub, and Lobsters for people actively asking
  for what you sell. Delivers the top 10 buying-intent leads to your Telegram
  with a pre-drafted reply. Powered by Gemini 2.5 Flash.
author: bencpnd
category: marketing
tags: [leads, sales, marketing, reddit, prospecting, automation, daily, telegram]
entry: index.js
cron: "0 8 * * *"
channels:
  - telegram
install: "npm install"
config:
  - key: OFFER_DESCRIPTION
    label: "What do you sell? (1-2 sentences)"
    type: text
    required: true
    example: "I sell a CRM tool for freelance designers. Target: freelancers struggling to track clients and invoices."
  - key: LEAD_RADAR_LICENSE_KEY
    label: "License Key (get one at lead-radar.pro)"
    type: secret
    required: true
  - key: TELEGRAM_CHAT_ID
    label: "Your Telegram Chat ID"
    type: text
    required: true
  - key: TELEGRAM_BOT_TOKEN
    label: "Telegram Bot Token (from @BotFather)"
    type: secret
    required: true
trial_days: 3
---

# Lead Radar

**Stop cold outreach. Start warm conversations.**

Lead Radar scans 9 social platforms every morning for people actively asking for what you sell — then delivers the top 10 buying-intent leads straight to your Telegram, each with a pre-drafted reply ready to send.

## How It Works

1. **You describe your offer** — e.g. "I sell a CRM for freelance designers"
2. **Gemini 2.5 Flash generates smart keywords** tailored to your niche
3. **9 sources are scanned** for posts matching those keywords (Reddit, Hacker News, Indie Hackers, Stack Overflow, Quora, Hashnode, Dev.to, GitHub Discussions, and Lobsters)
4. **Each post is scored 0-10** for buying intent using AI — filtering out noise and keeping only real opportunities
5. **Top 10 leads are delivered to Telegram** every morning at 8am, each with:
   - The original post title and snippet
   - A direct link to the conversation
   - An intent score with explanation
   - A pre-drafted reply you can copy-paste

## What Gets Detected

Lead Radar finds posts like:
- "Looking for a tool that does X" — direct buying intent
- "How do you handle Y?" — pain point that your product solves
- "We switched from Z and need an alternative" — active comparison shopping
- "Any recommendations for...?" — open to suggestions

## Sources

| Platform | Method |
|----------|--------|
| Reddit | API with automatic fallback chain (3 strategies) |
| Hacker News | Algolia search API |
| Indie Hackers | Jina web scraping |
| Stack Overflow | Public API |
| Quora | Jina web scraping |
| Hashnode | GraphQL API |
| Dev.to | Public API |
| GitHub Discussions | REST API |
| Lobsters | JSON feeds with local filtering |

## Source Health Monitoring

If any source goes down (rate-limited, blocked, or temporarily unavailable), Lead Radar:
- Continues scanning all other sources normally
- Appends a warning to your Telegram message listing which sources are down
- Shows scan stats: how many posts were scanned across how many active sources

## Smart Pre-Filtering

Before running AI scoring, Lead Radar pre-filters posts by keyword relevance. This means only genuinely relevant posts get scored, keeping the pipeline fast (under 60 seconds). AI scoring is included in your subscription — no separate API key needed.

## Setup (2 minutes)

### 1. Get a License Key
Visit [lead-radar.pro](https://lead-radar.pro) and start your 3-day free trial ($9/month after). Your key will be emailed to you instantly.

### 2. Create a Telegram Bot
Open Telegram, search for [@BotFather](https://t.me/BotFather), send `/newbot`, and follow the prompts. Copy the bot token it gives you (looks like `123456:ABC-DEF...`).

### 3. Get Your Telegram Chat ID
Search for [@userinfobot](https://t.me/userinfobot) in Telegram, send it any message — it replies with your Chat ID (a number like `123456789`). Copy it.

### 4. Fill in Your Settings
After installing the skill in OpenClaw, go to Lead Radar settings and enter:

| Field | What to enter |
|-------|---------------|
| `LEAD_RADAR_LICENSE_KEY` | Your license key from step 1 |
| `TELEGRAM_BOT_TOKEN` | The bot token from step 2 |
| `TELEGRAM_CHAT_ID` | Your chat ID from step 3 |
| `OFFER_DESCRIPTION` | Describe what you sell in 1-2 sentences (e.g. "I sell a CRM for freelance designers") |

No AI API keys needed — Gemini scoring is included in your subscription.

### 5. Wait for 8am
Lead Radar scans automatically every morning at 8am. Your first leads will arrive in Telegram tomorrow.

## Pricing

- **3-day free trial** — full access, no credit card charge
- **$9/month** — cancel anytime from your [billing portal](https://billing.stripe.com/p/login/3cI4gy83O4xoaKp431bZe00)

## FAQ

**How many leads will I get per day?**
It depends on your niche. Most users see 3-10 warm leads daily. Broader niches (like "project management") get more; narrow niches (like "CRM for pet groomers") get fewer but higher quality.

**Can I customize the scanning time?**
The default is 8am daily. You can change the cron schedule in your OpenClaw config.

**What if Reddit blocks my IP?**
Lead Radar has a 3-strategy fallback chain for Reddit. If one method gets blocked, it automatically switches to the next. Source health monitoring will notify you in Telegram if any source goes down.

**What data leaves my machine?**
Lead Radar executes on your machine via OpenClaw but relies on external services to function. Here is every outbound call it makes:
- **Source platforms** — fetches publicly available posts from Reddit (old.reddit.com, Pullpush.io), Hacker News (Algolia API), Indie Hackers & Quora (via r.jina.ai proxy), Stack Overflow (Stack Exchange API), Hashnode (GraphQL API), Dev.to (public API), GitHub (REST API), and Lobsters (JSON feeds). These are read-only requests; no user credentials or personal data are included in these calls.
- **License server** — validates your LEAD_RADAR_LICENSE_KEY and returns a vendor-provided GEMINI_API_KEY (users do not need their own). Only your license key is transmitted; your OFFER_DESCRIPTION is not sent to the license server.
- **Google Gemini API** — sends post snippets and your OFFER_DESCRIPTION to Google's generative AI for intent scoring, using the vendor-provided API key. This means your offer description and scraped post content are processed by Google under the vendor's API account.
- **Telegram API** — sends your daily lead digest to your chat via your TELEGRAM_BOT_TOKEN
No data is stored on any remote server by the skill itself. Your OFFER_DESCRIPTION and post snippets are sent to Google Gemini for scoring but are not persisted by Lead Radar.

**By installing and running Lead Radar, you consent to:** your OFFER_DESCRIPTION and publicly scraped post snippets being sent to Google's Gemini API for scoring; your license key being validated against our license server each run; and your lead digest being sent to the Telegram API. All four required secrets (license key, bot token, chat ID, offer description) are stored locally in your OpenClaw environment and are only transmitted to the services described above.
