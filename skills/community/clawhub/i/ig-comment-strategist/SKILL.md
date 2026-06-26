---
name: ig-comment-strategist
version: 1.0.0
description: AI analyzes Instagram reels/posts and generates 8 categories of high-performing comments designed to maximize visibility, drive replies, and build authentic connections.
category: Social Media
tags: [instagram, social-media, engagement, growth, comments]
author: Cod3Black <support@cod3black.agency>
repository: https://github.com/cod3black/ig-comment-strategist
license: MIT
pricing:
  oneTime: 49
  subscription: 9
  currency: USD
requirements:
  - Termux (Android) or Linux environment
  - Node.js v16+
  - OpenClaw agent system
  - SMTP credentials (for email reports, optional)
---

# Instagram Reel Comment Strategist

Turn Instagram content into engagement gold.

## The Science Behind It

- **10-axis virality formula** (emotional triggers, specificity, reply potential, curiosity gaps, naturalness, authority signals)
- **Industry-aware tone matching**
- **Anti-spam detection** (avoids pod language, emoji spam, generic praise)
- **Confidence scoring** (0-100%) for every comment

## 8 Comment Categories Generated

1. **Short high-visibility** (scroll-stoppers)
2. **Insightful** (shows you actually watched)
3. **Curiosity/open-loop** (invites replies)
4. **Authority-building** (positions expertise)
5. **Relatable/human** (personal connection)
6. **Slightly polarizing** (safe debate)
7. **"About to blow up"** (early social proof)
8. **Community-building** (conversation starters)

## Perfect For

- Growth hackers building personal brands
- Social media managers handling multiple accounts
- Agencies managing influencer campaigns
- Anyone tired of writing "Great post! 🔥"

## What's Included

- Single URL analysis with email reports
- Batch processing for multiple URLs
- Confidence scoring on every comment
- Top-N filtering (get just the best 3-5)
- Combined reports for campaign tracking
- Virality mechanism explanations

## Results

- Comments get 3-5x more replies than generic praise
- Build authentic connections with creators
- Increase profile visibility through strategic engagement

## Quick Start

```bash
# Analyze a single reel/post
node scripts/analyze-and-comment.js --url "https://instagram.com/reel/ABC123"

# Batch analyze multiple URLs
node scripts/batch-analyze.js --file urls.txt --output report.json

# Get top 3 comments only
node scripts/analyze-and-comment.js --url "https://instagram.com/reel/XYZ789" --top 3

# Send analysis via email
node scripts/analyze-and-comment.js --url "https://instagram.com/reel/DEF456" --email your@email.com
```

## Requirements

- Termux (Android) or Linux environment
- Node.js v16+
- OpenClaw agent system
- SMTP credentials (for email reports, optional)

## Support

Email: support@cod3black.agency
