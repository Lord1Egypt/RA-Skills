---
name: prospector-lite
description: "B2B outreach framework for OpenClaw agents. Gives your agent a structured prospecting workflow with email verification, bounce handling, pipeline tracking, duplicate prevention, domain reputation protection, and a self-improving lessons log. Built from 100+ production outreach runs. Use when the user wants their agent to do cold outreach, prospect research, lead generation, sales emails, or build a B2B pipeline. Also triggers for: 'find leads', 'send outreach', 'cold email', 'prospect list', 'sales pipeline', 'lead gen', or any request to research and contact potential customers."
metadata:
  openclaw:
    emoji: "🎯"
    version: "2.0.0"
    author: "Sora Labs"
    license: "MIT-0"
    tags: ["sales", "outreach", "prospecting", "leads", "pipeline", "email", "b2b", "revenue"]
    requires:
      bins: []
      env: []
      config: []
---

# Prospector Lite — B2B Outreach Framework

A production-tested prospecting workflow for OpenClaw agents. Research prospects, qualify them, verify emails, send personalized outreach, handle bounces, track your pipeline, and get better after every run.

Built by [Sora Labs](https://sora-labs.net) from running autonomous B2B outreach in production — every rule exists because something broke without it.

---

## Prerequisites

This skill is an instruction framework — it teaches your agent how to prospect. To send emails, your agent needs an email tool already configured:

- **gog** (Gmail CLI) — `openclaw skills install gog` or npm
- **Gmail channel** — `openclaw channels add --channel gmail`
- **Any SMTP-capable tool** your agent can invoke

Set up your preferred email method before using this skill.

---

## Pre-Flight Checklist (Every Run — Do This First)

Your agent must run this checklist before doing anything else:

1. **Read `prospects/lessons-learned.md`** — what worked, what flopped, what to try differently this run
2. **Check inbox for replies** — replies are the highest priority signal. Process them FIRST.
3. **Check inbox for bounces** — Mail Delivery Subsystem notifications mean a bad address. Log it immediately (see Bounce Handling below).
4. **Check `prospects/pipeline.md` for follow-ups due** — any prospect emailed 5+ days ago with no reply gets ONE follow-up (see Follow-Up Rules below).
5. **Count emails already sent today** — HARD STOP at 10 new outreach emails per day. The safe range is 3–5 for new agents, scaling to 5–10 once deliverability is proven. This protects your sender domain reputation.
6. **Run `memory_search`** for "prospecting" or "outreach" to pull context from recent runs.

Skipping pre-flight is how agents send duplicate emails, miss replies, and burn sender reputation. Don't skip it.

---

## Prospect Qualification — Decision Tree

Research the company FIRST. Then decide if they're a fit for your product.

```
STEP 1: Is this company in a traditional industry?
        (construction, logistics, legal, healthcare, manufacturing,
         real estate, energy, agriculture, insurance, freight)

  YES → Is the company behind on AI adoption?
        Can you identify 3 specific AI opportunities for their business?
        Can you reach a decision-maker via verified work email?

        ALL YES → Send outreach with a free mini-audit (3 AI opportunities in the email body)

        ANY NO  → Skip. Don't force a fit.

  NO  → Skip for now. Traditional industries convert better than tech companies
        because they can't build AI solutions themselves.

NONE OF THE ABOVE → Skip. Don't force a fit.
```

**Key lesson from production:** Traditional industries behind on AI adoption (the "spreadsheet graveyards" — logistics, freight, commercial insurance, construction) respond far better than tech startups. Tech-native companies can build it themselves and won't pay for it.

---

## Finding Prospects

**Where to hunt:**
- Web search: "[industry] companies [state/region]", "top [industry] firms [city]"
- X: search for executives posting about digital transformation, operational challenges, or "keeping up with AI" in traditional industries
- Conference speaker lists from industry events
- Industry association directories

**Signals that a company is a good fit:**
- Company website looks dated or mentions no technology
- Competitors in their space are adopting AI and they aren't
- Job postings mention manual processes that could be automated
- Executive has expressed interest in innovation at conferences or online
- Company has 50+ employees but zero AI/ML presence

---

## Email Verification (Before Every Send)

These rules exist because bounced emails destroy your sender reputation. One bad send can get your domain flagged.

Before sending to ANY address:

1. **Work email only.** Personal emails (gmail, yahoo, hotmail, outlook.com) → SKIP.
2. **Verify the domain.** Web search it. Does it resolve to a real company website?
3. **Verify the address.** Found on company website, Google listing, Facebook About page, or Yelp? **NOT guessed. NOT scraped from a random directory.** If you can't verify it from a primary source, skip the prospect.
4. **Check pipeline.md** — has this address been emailed in the last 14 days? If yes → SKIP.
5. **Check pipeline.md** — is this address or domain marked BOUNCED? If yes → SKIP. **Never send to a bounced address.**

If any check fails → SKIP. Find a better prospect. A skipped prospect is better than a bounced email.

---

## Bounce Handling

When your agent sees a bounce notification from Mail Delivery Subsystem:

1. Log the address AND the domain in pipeline.md with status `BOUNCED` and today's date
2. Never send to that address again
3. If the domain itself bounced (MX record misconfigured), flag the entire domain — don't try other addresses at that domain

Bounces are permanent. There is no retry.

---

## Outreach Email — Template

This template is for selling an AI-related service to traditional industry companies. Adapt the product details, pricing, and payment links to match what you're selling.

**Subject line strategy — pick the most specific option you can write:**
- BEST: "[Company Name]: [Competitor/vendor] just shipped [specific thing] for exactly what you do"
- GOOD: "[Company Name] — 3 spots where AI cuts [time/cost/delay] this quarter"
- FALLBACK: "3 AI opportunities for [Company Name] — quick take"

The subject line must make the recipient think they'll miss something if they don't open it. Generic subjects get deleted.

```
Hi [First Name],

I'm [Your Agent Name], [role] at [Your Company]. I help [industry] companies find the operational spots where AI can actually remove delay and admin drag.

I took a quick look at [Company Name] and spotted three areas where AI could make an immediate difference:

**1. [Short, punchy headline — max 10 words]**
[2-3 sentences. Specific to THEIR business. Cite one real vendor, date, or data point. End with what it means for them specifically.]

**2. [Short, punchy headline]**
[2-3 sentences. Same standard.]

**3. [Short, punchy headline]**
[2-3 sentences. Same standard.]

This is just a quick surface read. If you want the full audit — prioritized by effort vs. impact, with a roadmap your team can act on — I do that for a flat [PRICE](YOUR_PAYMENT_LINK).

Either way, hope it's useful.

— [Your Agent Name]
[Role] | [Your Company](YOUR_WEBSITE)
[your-email]
```

**Rules for the 3 observations:**
- Each must be specific to THEIR business — not generic "use chatbots"
- Each must cite a real competitor, vendor, or industry trend (with source and date)
- Each must be actionable — they could explore it within 30 days
- Use **bold headlines** for visual hierarchy
- 2-3 sentences MAX per observation — shorter is better
- The pricing link must be a clickable hyperlink, not plain text

**The mini-audit IS the demo.** If it's not sharp enough that you'd reply to it yourself, don't send it. Quality over volume — every time.

**Emails must be well-formatted HTML** — clean spacing, proper tags (`<p>`, `<strong>`, `<a href>`), visual hierarchy. No markdown in the email body. No walls of text. The email is the first impression.

---

## Pipeline Tracking

Log every prospect to `prospects/pipeline.md`:

```markdown
## [Company Name]
- **Contact:** [Name]
- **Email:** [verified address]
- **Website:** [url]
- **What they do:** [1 sentence]
- **Why they're a fit:** [1 sentence — what makes them right for your product]
- **Status:** qualified | emailed | followed-up | replied | converted | bounced | passed | no-email
- **Date found:** YYYY-MM-DD
- **Date emailed:**
- **Date followed up:**
- **Notes:**
```

**Status definitions:**
- `qualified` — researched and verified, ready to email
- `emailed` — outreach sent
- `followed-up` — one follow-up sent after 5 days
- `replied` — they responded (any response)
- `converted` — they bought
- `bounced` — email bounced (never contact again)
- `passed` — they said no or "stop" (never contact again)
- `no-email` — couldn't find a verified email (logged so you don't research them again)

Check pipeline.md before every send. Your agent must never email the same person twice (except the one follow-up).

---

## Follow-Up Rules

- **ONE follow-up only**, after 5 days with no reply
- Keep it short: "Hi [Name] — just checking if [the audit / the analysis] was useful. Happy to dig deeper."
- Always end with: "If you'd rather not hear from me, just reply 'stop' and I'll remove you immediately."
- Update status to `followed-up` with date
- After the follow-up: **NEVER email them again. Ever.**
- If they reply "not interested" or "stop" → mark as `passed` and never contact again

---

## Self-Improvement Loop

After every run, your agent reviews its own work:

1. **Reread what you sent.** Would YOU reply to this email?
2. **Log to `prospects/lessons-learned.md`:**
   - Which subject lines you used
   - Which industries/company types you targeted
   - What felt sharp vs. what felt generic
   - What to try differently next run
3. **Experiment.** Try small variations between runs — subject line tweaks, different observation styles, reordering the pitch. Track what gets replies.
4. **Read lessons-learned.md at the start of every run.** This is how your agent compounds knowledge across sessions.

---

## Run Schedule

When the prospecting cron fires, your agent follows this sequence:

```
1. PRE-FLIGHT     — run the checklist (lessons-learned, replies, bounces, follow-ups, send count)
2. PROCESS REPLIES — notify you immediately for any responses
3. PROCESS BOUNCES — log bounced addresses and domains
4. SEND FOLLOW-UPS — max 1 follow-up, only if 5+ days since last email with no reply
5. HUNT            — research new prospects using the sources above
6. QUALIFY         — run each through the decision tree
7. VERIFY EMAILS   — every address through the verification checklist
8. SEND            — max 3-5 new outreach emails per day (scale to 5-10 once deliverability is proven)
9. LOG             — update pipeline.md with every prospect touched
10. SELF-REVIEW    — log to lessons-learned.md
```

**Setting up the cron:**
```bash
openclaw cron add --name "prospecting" \
  --cron "0 10 * * 1-5" \
  --message "Run the prospecting workflow. Read prospects/lessons-learned.md first. Check inbox for replies and bounces. Send up to 3 outreach emails. BCC [your-email] on every send. Log everything to pipeline.md and lessons-learned.md." \
  --timeout 900
```

---

## Prospecting Rules (Non-Negotiable)

These rules are non-negotiable. They exist because breaking them caused real problems in production:

- **Never exceed your daily send limit** — start at 3-5, scale to 10 max
- **Never send the same prospect two emails in the same run**
- **Never email the same address twice** (except the ONE follow-up after 5 days)
- **Never send to personal emails** — only verified work emails
- **Never send to BOUNCED addresses or domains**
- **Never re-prospect an address within 14 days**
- **Never guess an email address** — if you can't verify it, skip the prospect
- If someone says "not interested" or "stop" → mark `passed`, never contact again
- **Quality over volume** — if you can't write a sharp email for a prospect, skip them
- **Do NOT save outreach emails to the workspace** — the sent folder in your email tool is the record

---

## Setup

Create these files in your workspace before the first run:

### prospects/pipeline.md
```markdown
# Prospect Pipeline

Track every prospect here. Check before every send to prevent duplicates.
```

### prospects/lessons-learned.md
```markdown
# Prospecting Lessons Learned

Read this before every run. Log what works and what doesn't after every run.
This is how your agent gets better over time.
```

### PRODUCTS.md
Define your products with:
- Price and payment link
- Ideal customer profile (who is this for?)
- Subject line template
- Email template (HTML)
- Qualification criteria (how does the agent decide if a prospect is a fit?)

---

## Tips From Production

1. **Start with 3 emails/day.** Scale up only after you've confirmed good deliverability (low bounce rate, no spam flags).
2. **Traditional industries > tech startups.** Companies behind on AI adoption value this work more — and they can't build it themselves.
3. **Email quality > email volume.** One well-researched, sharp email beats five generic ones. Every time.
4. **Watch your bounce rate.** If it crosses 10%, stop sending and tighten your email verification. Bounces compound — a few bad sends can tank your domain reputation.
5. **Pre-researched prospect lists save tokens.** Drop them in `prospects/manual-targets.md` so your agent doesn't burn search tokens finding companies you already know about.
6. **The self-improvement loop is the most important feature.** An agent that reviews its own work and adjusts gets dramatically better over 10-20 runs. Don't skip the lessons-learned step.

---

## Ready for the Full System?

Prospector Lite gives you the foundation. If your agent is running outreach and you want the complete production system, **Prospector Pro** adds everything we use internally:

**🔧 One-command workspace setup** — creates all files, directories, and cron jobs in one shot

**📧 5 complete product email templates** — website builds, competitive intel briefings, AI readiness audits, industry digests, and custom workflow pitches. Each with subject line strategies, HTML formatting rules, and objection handling.

**📊 PDF competitive intelligence briefing generator** — your agent researches competitors, generates a branded PDF, and attaches it to outreach as a free value hook. The PDF does the selling.

**📋 Full 5-product decision tree** — routes every prospect to the right product automatically. Local businesses → website builds. Traditional industry → AI audits. Startups → competitive intel. With hard caps and token budgets per product type.

**🎯 Manual target list workflow** — pre-qualify prospects yourself and hand them to your agent with verified emails. The agent sends without re-researching.

**📈 Revenue logging and notification system** — automatic alerts when prospects reply, subscribe, or convert. Revenue tracked across all products.

**All of this was built from running 100+ production outreach runs.** Every rule, every template, every guardrail exists because something broke without it.

**$39 one-time** → [Get Prospector Pro at sora-labs.net/tools](https://sora-labs.net/tools/)