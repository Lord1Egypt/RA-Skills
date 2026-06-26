---
name: newsletter-creator-pack
description: Automates the four highest-ROI tasks for newsletter writers and content creators — content repurposing, sponsorship outreach, subscriber reactivation, and performance analysis. Built for solo creators, newsletters, podcasters, and YouTubers monetizing their audience.
version: 1.0.0
tags:
  - newsletter
  - creator
  - content
  - repurposing
  - sponsorship
  - monetization
  - automation
---

# Newsletter & Creator Pack

A complete automation suite for content creators and newsletter operators.
Handles the four workflows that directly drive revenue — without hiring a team.

## When to use this skill

Use this skill when the user asks about any of the following:
- Repurposing a newsletter, blog post, or video into other formats
- Writing cold outreach to potential sponsors
- Re-engaging subscribers who haven't opened in 30–90 days
- Analyzing which content is performing and why
- Writing subject lines that get opened
- Turning a single piece of content into a week's worth of posts

---

## Workflow 1: Content Repurposing Engine

Take one piece of content and turn it into a full week of distribution.

### Input
- The original content (newsletter issue, blog post, video transcript, or podcast notes)
- The creator's primary platform (newsletter, YouTube, Twitter/X, LinkedIn, Instagram, TikTok)
- Tone: professional / casual / educational / entertaining

### Output — 7 assets from 1 piece of content
1. **Twitter/X thread** — 5–8 tweets, hook tweet first, ends with CTA
2. **LinkedIn post** — 150–250 words, professional framing, 3–5 line breaks for readability
3. **Short-form video script** — 45–60 seconds, hook in first 3 words, for TikTok/Reels/Shorts
4. **Email subject line variants** — 5 options (curiosity, benefit, question, number, bold claim)
5. **Instagram caption** — 100–150 words + 10 relevant hashtags
6. **Quote graphic text** — 3 pull-quote candidates, under 15 words each
7. **Community/Discord post** — casual version for community sharing

### Rules
- Maintain the creator's voice — ask for a sample of their writing before generating
- Never water down the insight — the repurposed version should be as valuable as the original
- Each format should feel native to its platform, not copy-pasted
- Refer to references/repurposing-by-platform.md for platform-specific formatting rules

### Instructions for the agent
1. Ask for the original content and their primary platform
2. Ask for 2–3 sentences describing their tone/audience
3. Generate all 7 assets
4. Ask which formats they want saved to file

---

## Workflow 2: Sponsorship Outreach Generator

Research and write personalized cold outreach to potential newsletter/podcast sponsors.

### What to research for each prospect
- Their current advertising channels (are they running newsletter ads?)
- Their target customer (matches your audience?)
- Recent product launches or campaigns
- Estimated budget signals (funded startup vs bootstrapped?)

### Email structure
- **Subject line:** Under 8 words, specific to their business
- **Opening:** One sentence referencing something specific about them (not generic flattery)
- **Pitch:** 2–3 sentences — your audience size, demographic, and why it's their customer
- **Proof:** One data point (open rate, click rate, or a previous sponsor result)
- **Ask:** Soft CTA — "Would a quick 10-minute call make sense?" not "Buy my ad slot"
- **Length:** Under 150 words total

### Pricing tiers to reference
- Newsletter under 1k subscribers: $50–150/issue
- 1k–5k: $150–500/issue
- 5k–25k: $500–2,000/issue
- 25k+: $2,000–10,000/issue

### Instructions for the agent
1. Ask for: newsletter name, subscriber count, niche, average open rate
2. Ask for up to 5 prospect company names or URLs
3. Research each prospect using web search
4. Generate one personalized email per prospect
5. Generate a follow-up email for each (to send 5 days later if no reply)

---

## Workflow 3: Subscriber Reactivation Campaign

Re-engage subscribers who haven't opened in 30–90 days before they churn.

### The reactivation sequence (3 emails)
- **Email 1 — "Here's what you missed":** Curated best-of digest. Value first, no guilt.
- **Email 2 — "Quick question":** 1-sentence reply request. "What would make this more useful?" Highest reply rate of any email type.
- **Email 3 — "Should I remove you?":** Permission-based. Clean your list or win them back.

### Rules for Email 3 (the permission email)
- Subject: "Should I remove you from [Newsletter Name]?"
- Body: 3 sentences max. Honest, no manipulation.
- Include one-click re-subscribe confirmation link placeholder
- This email cleans dead weight AND often re-activates 5–15% of lapsed readers

### Subject line formulas by email
- Email 1: "The 3 best things from [Newsletter] this month"
- Email 2: "Quick question, {first_name}"
- Email 3: "Should I remove you from [Newsletter Name]?"

### Instructions for the agent
1. Ask for: newsletter name, niche, top 3 recent posts/topics
2. Ask for subscriber first name placeholder preference
3. Generate all 3 emails
4. Offer to generate 5 subject line variants for each

---

## Workflow 4: Content Performance Analyst

Analyze newsletter or content metrics and produce an actionable insight report.

### What to analyze (user provides the data)
- Open rates by issue
- Click rates by issue
- Subject lines used
- Topics covered
- Day/time of send

### Output report structure
```
CONTENT PERFORMANCE REPORT
Newsletter: [name]
Period: [date range]
Issues analyzed: [n]

TOP PERFORMERS
- Best open rate: [issue] — [rate]% — Why it worked: [insight]
- Best click rate: [issue] — [rate]% — Why it worked: [insight]

PATTERNS FOUND
- Subject line patterns that beat average: [list]
- Topics that drive highest engagement: [list]
- Best send day/time: [day, time]

WHAT TO DO THIS WEEK
- [Specific action 1]
- [Specific action 2]
- [Specific action 3]

WHAT TO STOP DOING
- [Specific action 1]
```

### Instructions for the agent
1. Ask user to paste their metrics (CSV, table, or plain text — any format)
2. Parse and analyze the data
3. Generate the report
4. End with 3 specific subject line recommendations based on their best performers

---

## Output and file management
- Save all generated content to ~/Documents/drew2_workspace/output/[newsletter-name]/
- Subdirectories: repurposed/, outreach/, reactivation/, reports/
- Name files by date: YYYY-MM-DD-type.md
- Confirm save location before writing
