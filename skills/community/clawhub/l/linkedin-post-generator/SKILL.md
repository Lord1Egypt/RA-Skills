---
name: linkedin-post-generator
description: AI-powered LinkedIn post generator for professionals. Create engaging posts, thought leadership content, and career updates using Sloan agent.
version: 1.0.7
author: Matt
tags:
  - linkedin
  - professional
  - content-generation
  - social-media
pricing:
  type: pay-per-use
  price: 0.002
  currency: USDT
  payment_provider: skillpay.me
---

# LinkedIn Post Generator

Generate professional LinkedIn posts that drive engagement. Perfect for professionals, thought leaders, and job seekers.

## Features

- **Professional Tone** - Industry-appropriate language
- **Engagement Hooks** - Attention-grabbing openings
- **Multiple Types** - General, thought-leadership, celebration, announcement
- **Call-to-Action** - Drive comments and shares

## Usage

```bash
# Generate a LinkedIn post
linkedin-post-generator "career growth tips"

# Generate a thought leadership post
linkedin-post-generator "AI trends" --type thought-leadership

# Generate a celebration post
linkedin-post-generator "got promoted" --type celebration
```

## Options

| Option | Description | Default |
|--------|-------------|---------|
| `--tone` | Tone (professional, casual, inspiring) | professional |
| `--type` | Post type (general, thought-leadership, celebration, announcement) | general |
| `--no-emoji` | Disable emojis | - |
| `--no-hashtags` | Disable hashtags | - |

## Pricing

- **Pay per use**: 0.002 USDT per generation

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `SKILLPAY_MERCHANT_KEY` | Payment merchant key (optional, embedded key used by default) | No |
| `OPENCLAW_GATEWAY_TOKEN` | Gateway auth token for local API fallback | No |

## Requirements

- OpenClaw with Sloan agent (AI columnist)
- OpenClaw Gateway running locally (for API fallback)

## About Sloan

Sloan is your AI columnist - a professional content creator specializing in LinkedIn thought leadership and professional storytelling.

## Support

- GitHub: https://github.com/icepopma/linkedin-post-generator
- Discord: https://discord.gg/clawd
- Email: icepopma@hotmail.com

## License

MIT © Matt
