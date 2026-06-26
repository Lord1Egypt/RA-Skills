# Prospect Analyzer

**Analyze any company's website. Find content gaps. Score the opportunity. Get a ready-to-use outreach angle.**

An OpenClaw skill that turns a domain name into a qualified lead report — with specific content weaknesses, competitor analysis, and a personalized hook for cold outreach.

## What It Does

Give it a domain. It:

1. Visits the company's website and figures out what they do
2. Finds their blog (or confirms they don't have one)
3. Audits recent posts for quality, frequency, and SEO basics
4. Checks what competitors are publishing
5. Scores the prospect 1-10 on fit, budget signals, and content gap size
6. Generates a specific outreach angle you can use in a cold email

## Example

```
> Analyze lemonsqueezy.com as a prospect

Score: 7/10 — Warm Lead
Blog has 1 visible post. Competitors (Stripe, Paddle) publish weekly.
$2500% revenue growth in 2023, 15k+ merchants. Clear content gap
around "merchant of record" and payment infrastructure topics.

Outreach angle: "Your blog hasn't been updated since October.
Meanwhile Paddle published 12 guides on merchant-of-record topics
last quarter. Those are your customers searching."
```

## Install

```bash
clawhub install prospect-analyzer
```

Or paste this repo link into your OpenClaw chat and ask it to install.

## Setup

1. Install the skill
2. Make sure browser is enabled in your OpenClaw config
3. (Optional) Create `PROSPECT_CONFIG.md` in your workspace with your business context — what you sell, who you target, your pricing range. This makes outreach angles specific to your service.

## Usage

Message your agent:
- `Analyze [domain.com] as a prospect`
- `Qualify [company] for outreach`
- `Check the content on [domain.com]`

## Part of the DriftMango SDR Kit

This is the free skill from a complete autonomous prospecting pipeline:

| Skill | What It Does | Availability |
|-------|-------------|-------------|
| **prospect-analyzer** | Content gap analysis + lead scoring | ✅ Free (this skill) |
| market-scanner | Auto-discovers prospects from Product Hunt, Google, IndieHackers | 🔒 Full kit |
| outreach-composer | Turns analyses into 3-email cold sequences | 🔒 Full kit |
| content-writer | Produces blog posts, landing pages, email sequences from briefs | 🔒 Full kit |
| editor | Quality-gates content before client delivery | 🔒 Full kit |

**Full pipeline:** [driftmango.com/sdr-kit](https://driftmango.com/sdr-kit)

## Model Recommendations

| Model | Quality | Cost per Analysis |
|-------|---------|-------------------|
| Claude Haiku 4.5 | Good | ~$0.02 |
| Claude Sonnet 4.6 | Excellent | ~$0.08 |
| GPT-5 | Good | ~$0.05 |
| DeepSeek V3.2 | Acceptable | ~$0.005 |

Haiku is the sweet spot for most users. Sonnet if you want the best outreach angles.

## License

MIT-0 (ClawHub standard)
