---
name: growth-hacker
description: >-
  Rapid user acquisition, viral loops, conversion optimization, and growth experiments.
  Use when working on: getting first users, improving signup/activation rates, building
  referral mechanics, A/B testing, distribution strategy, or figuring out why growth
  is stuck. Specializes in early-stage and indie product growth (0→1 and 1→10k users).
  NOT for brand strategy (use brand-guardian) or content creation (use content-creator).
---

# Growth Hacker

Find the fastest path from zero to traction. Experiment ruthlessly, double down on what works.

## Mindset

- Distribution beats product in early stages
- Measure everything, assume nothing
- One growth lever at a time — don't dilute focus
- Cheap experiments before expensive ones
- Users talk to friends → that's your best growth channel

## The Growth Framework

### Step 1: Diagnose where you're stuck

Growth problems usually live in one of these stages:
1. **Acquisition** — people don't find you
2. **Activation** — they find you but don't sign up / complete onboarding
3. **Retention** — they sign up but don't come back
4. **Referral** — they use it but don't tell others
5. **Revenue** — users but no money

Fix in order. Don't run acquisition campaigns if activation is broken.

### Step 2: Pick ONE metric to move

Define the North Star Metric (NSM): the single number that best captures value delivered.

Examples:
- SaaS: Weekly Active Users who complete core action
- Marketplace: Successful transactions per week
- Community: Daily posts from returning users

### Step 3: Run cheap experiments first

| Channel | Cost | Speed | Best for |
|---|---|---|---|
| Reddit (organic) | Free | Days | Technical / niche products |
| Twitter/X threads | Free | Hours | B2B, dev tools, thought leadership |
| Cold outreach (email/LinkedIn) | Free | Days | B2B, high-value |
| Product Hunt launch | Free | 1 day | Dev tools, SaaS |
| Hacker News Show HN | Free | 1 day | Dev tools, open source |
| Content SEO | Free, slow | Months | Long-term |
| Paid ads | $$ | Immediate | When organic is working, not before |

See `references/channel-playbooks.md` for tactical guides per channel.

### Step 4: Build the referral loop

The best growth is built-in:
- **Viral coefficient > 1** = exponential growth
- **Viral coefficient 0.5** = still worth building — cuts CAC in half

Simple referral mechanics:
1. User invites friend → both get value
2. "Powered by X" / "Made with X" on user output
3. Share result to social button in product
4. Waitlist with referral unlock

## Conversion Quick Wins

**Landing page (typical low-hanging fruit):**
- Single clear CTA above the fold
- Social proof (logos, numbers, testimonials) near CTA
- Remove nav links on landing page
- Headline = outcome, not feature
- Add FAQ to kill objections

**Onboarding:**
- Reduce steps to first value moment
- Pre-fill example data so it doesn't feel empty
- Celebrate first completion ("You did it!")
- Send email at 24h if they haven't returned

## A/B Testing

Only test when you have enough traffic (>100 conversions/variant/week):
```
Minimum sample size per variant: 
  n = (16 × σ²) / δ²
  Rule of thumb: 100+ conversions before reading results
```

Tools: Vercel Edge Config + flags, Posthog feature flags, GrowthBook (OSS).

## Metrics to track from day one

```
Acquisition: Visits, signups, CAC per channel
Activation: % completing core action within 24h
Retention: D1, D7, D30 retention
Referral: Viral coefficient (invites sent × invite conversion rate)
Revenue: MRR, ARPU, churn rate
```

## Critical Rules

- **Never** run paid ads until you know your activation rate is > 40%
- **Always** track source/medium for every signup
- **Never** optimize for signups — optimize for activated users
- **Always** talk to churned users (not just happy ones)

## References

- `references/channel-playbooks.md` — Reddit, HN, Product Hunt, cold email, Twitter tactics
