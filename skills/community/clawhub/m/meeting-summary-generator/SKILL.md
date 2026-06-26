---
name: meeting-summary-generator
description: AI-powered meeting summary generator. Convert meeting notes into professional summaries and action items.
version: 1.0.7
author: Matt
tags:
  - meetings
  - productivity
  - notes
  - professional
pricing:
  type: pay-per-use
  price: 0.003
  currency: USDT
  payment_provider: skillpay.me
---

# Meeting Summary Generator

Convert meeting notes into professional summaries with action items and decisions.

## Features

- **Professional Format** - Clean, organized output
- **Action Items** - Extract and prioritize tasks
- **Decision Log** - Key decisions documented
- **Attendee Summary** - Who said what

## Usage

```bash
# Generate meeting summary
meeting-summary-generator "John: Let's launch next week. Sarah: I'll handle marketing."

# From file
meeting-summary-generator --file notes.txt

# With meeting details
meeting-summary-generator <notes> --title "Q1 Planning" --date 2026-03-05
```

## Options

| Option | Description | Default |
|--------|-------------|---------|
| `--title` | Meeting title | - |
| `--date` | Meeting date (YYYY-MM-DD) | - |
| `--file` | Read notes from file | - |

## Pricing

- **Pay per use**: 0.003 USDT per generation

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `SKILLPAY_MERCHANT_KEY` | Payment merchant key (optional, embedded key used by default) | No |
| `OPENCLAW_GATEWAY_TOKEN` | Gateway auth token for local API fallback | No |

## Requirements

- OpenClaw with Sloan agent (AI columnist)
- OpenClaw Gateway running locally (for API fallback)

## About Sloan

Sloan is your AI columnist - a professional meeting secretary specializing in structured summaries.

## Support

- GitHub: https://github.com/icepopma/meeting-summary-generator
- Discord: https://discord.gg/clawd
- Email: icepopma@hotmail.com

## License

MIT © Matt
