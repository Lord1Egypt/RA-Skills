---
name: neckr0ik-socialposter
version: 1.0.0
description: Automate social media posting across Twitter, LinkedIn, Facebook, Instagram. Schedule posts, track engagement, auto-reply. Use when you need to manage social media presence.
---

# Social Media Automation

Multi-platform social media automation.

## What This Does

- **Post Scheduling** — Schedule posts for optimal times
- **Multi-Platform** — Twitter, LinkedIn, Facebook, Instagram
- **Content Calendar** — Plan weeks/months ahead
- **Auto-Reply** — Respond to mentions automatically
- **Analytics** — Track engagement and growth

## Quick Start

```bash
# Schedule a tweet
neckr0ik-socialposter post --platform twitter --content "Hello world!" --schedule "2026-03-07 09:00"

# Schedule multi-platform post
neckr0ik-socialposter post --platform twitter,linkedin --content "Blog post alert!" --schedule "2026-03-07 10:00"

# View scheduled posts
neckr0ik-socialposter calendar --days 7

# Auto-reply to mentions
neckr0ik-socialposter auto-reply --platform twitter --keywords "thanks,thank you" --response "You're welcome!"
```

## Supported Platforms

| Platform | Post | Schedule | Reply | Analytics |
|----------|------|----------|-------|-----------|
| Twitter/X | ✅ | ✅ | ✅ | ✅ |
| LinkedIn | ✅ | ✅ | ✅ | ✅ |
| Facebook | ✅ | ✅ | ✅ | ✅ |
| Instagram | ✅ | ✅ | 🟡 | ✅ |
| Threads | ✅ | ✅ | ✅ | 🟡 |
| Bluesky | ✅ | ✅ | ✅ | 🟡 |

## Commands

### post

Create and schedule posts.

```bash
neckr0ik-socialposter post [options]

Options:
  --platform <list>     Comma-separated platforms (twitter,linkedin,facebook,instagram)
  --content <text>      Post content
  --media <files>       Media files to attach
  --schedule <datetime> Schedule time (ISO format)
  --timezone <tz>       Timezone for schedule
```

### calendar

View scheduled posts.

```bash
neckr0ik-socialposter calendar [options]

Options:
  --days <n>            Days to show (default: 7)
  --platform <name>      Filter by platform
  --status <status>     Filter by status (scheduled, posted, failed)
```

### auto-reply

Set up automatic replies.

```bash
neckr0ik-socialposter auto-reply [options]

Options:
  --platform <name>     Platform name
  --keywords <list>    Trigger keywords (comma-separated)
  --response <text>     Response template
  --probability <n>     Probability of replying (0-1)
```

### analytics

View engagement analytics.

```bash
neckr0ik-socialposter analytics [options]

Options:
  --platform <name>     Platform name
  --period <days>        Time period (default: 30)
  --export <format>     Export format (csv, json)
```

### connect

Connect social media accounts.

```bash
neckr0ik-socialposter connect --platform <name>
```

## Content Calendar

Plan your content ahead:

```bash
# Add to calendar
neckr0ik-socialposter calendar add --content "Monday motivation" --platform twitter --day monday --time 09:00
neckr0ik-socialposter calendar add --content "Tech tip" --platform linkedin --day wednesday --time 14:00
neckr0ik-socialposter calendar add --content "Weekend vibes" --platform instagram --day friday --time 17:00

# View weekly calendar
neckr0ik-socialposter calendar view --week
```

## Auto-Reply Templates

Create smart auto-replies:

```yaml
# replies.yaml
- name: thanks-reply
  platform: twitter
  keywords:
    - thanks
    - thank you
    - appreciation
  response: "You're welcome! 🙏"
  probability: 0.8
  
- name: question-reply
  platform: linkedin
  keywords:
    - how do
    - how to
    - what is
  response: "Great question! Check out our FAQ: [link]"
  probability: 0.5
  
- name: support-reply
  platform: all
  keywords:
    - help
    - support
    - issue
  response: "I've noted your concern. Our team will reach out shortly."
  probability: 1.0
```

## Optimal Posting Times

Get recommended posting times:

```bash
neckr0ik-socialposter optimize --platform twitter

# Output:
# Best times to post on Twitter:
#   Monday: 09:00, 12:00, 17:00
#   Tuesday: 10:00, 13:00, 18:00
#   Wednesday: 09:00, 12:00, 15:00
#   ...
```

## Engagement Tracking

```bash
# Track post engagement
neckr0ik-socialposter track --post-id <id>

# Track account growth
neckr0ik-socialposter growth --platform twitter --days 30

# Compare platforms
neckr0ik-socialposter compare --days 30
```

## Rate Limits

The skill respects platform rate limits:

| Platform | Posts/Day | DMs/Day |
|----------|------------|---------|
| Twitter | 2,400 | 1,000 |
| LinkedIn | 100 | 30 |
| Facebook | 25 | - |
| Instagram | 25 | 50 |

## Configuration

```bash
# Set API credentials
neckr0ik-socialposter config set twitter.api_key <key>
neckr0ik-socialposter config set twitter.api_secret <secret>
neckr0ik-socialposter config set linkedin.access_token <token>

# Set default timezone
neckr0ik-socialposter config set timezone "America/Mexico_City"
```

## Use Cases

### 1. Content Calendar

Plan and schedule a week of posts:

```bash
# Create daily posts for a week
for day in monday tuesday wednesday thursday friday; do
  neckr0ik-socialposter post \
    --platform twitter,linkedin \
    --content "$(cat ${day}-content.txt)" \
    --schedule "2026-03-${day_num} 09:00"
done
```

### 2. Auto-Engagement

Automatically engage with your audience:

```bash
# Auto-thank for mentions
neckr0ik-socialposter auto-reply \
  --platform twitter \
  --keywords "mentioned,recommended,recommended" \
  --response "Thanks for the mention! 🙏"
```

### 3. Analytics Report

Generate monthly report:

```bash
neckr0ik-socialposter analytics --period 30 --export csv > monthly-report.csv
```

## See Also

- `references/platforms.md` — Platform-specific notes
- `references/rate-limits.md` — Rate limit details
- `scripts/social.py` — Main implementation