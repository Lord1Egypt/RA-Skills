# Content Creator Pro

**Your entire social media strategy, written and ready for $9.99 forever.**

[![Codex Security Verified](https://img.shields.io/badge/Codex%20Security-Verified-brightgreen?style=for-the-badge&logo=shield)](./SECURITY.md)

---

## What Is This?

Content Creator Pro is an AI social media manager that lives right inside your agent. Tell it about your brand once, and it writes platform-perfect posts for X, LinkedIn, Instagram, TikTok, and Facebook. Plan a full week of content in one command. Turn one idea into five different posts. Upload a product photo and get caption options instantly.

No monthly fees. No usage caps. No API connections to manage. Just you, your agent, and unlimited content.

---

## What You Get

- **Brand Voice Engine** — Learns how you sound and gets better over time
- **Content Calendar** — Say "plan my week" and get a complete posting schedule
- **Cross-Platform Repurposing** — One idea becomes 5 platform-perfect posts
- **Photo-to-Caption** — Upload a product shot, get caption variants with CTAs
- **Content Pillars** — Strategic theme rotation so your feed stays balanced
- **Idea Bank** — Save ideas for later, use them when you're ready
- **Engagement Tracking** — Log your results, get smarter recommendations
- **Competitor Analysis** — Study what's working in your space (read-only, never copies)
- **Dashboard Companion Kit** — Specs included for a visual content calendar and analytics view

---

## Quick Start (3 Minutes)

### 1. Drop the files into your agent
Copy the `content-creator-pro/` folder into your agent's skills directory.

### 2. Run setup
Tell your agent: **"Set up Content Creator Pro"**

It will create your data directories and copy config files automatically using the instructions in `SETUP-PROMPT.md`.

### 3. Define your brand
Your agent will ask 3 simple questions:
- What's your product or business?
- Who is your dream customer?
- Give me 2 sentences in your ideal brand voice.

### 4. Start creating
That's it. Try any of these:
- **"Plan my content for next week"**
- **"Write a LinkedIn post about our new feature"**
- **"Turn this into an X thread and an IG caption"**
- **"Save this idea for later: behind-the-scenes of our product launch"**
- *(Upload a photo)* **"Write captions for this"**

---

## How It Compares

| | Content Creator Pro | Buffer | Jasper | Hootsuite |
|---|---|---|---|---|
| **Price** | $9.99 once | $15/mo ($180/yr) | $49/mo ($588/yr) | $99/mo ($1,188/yr) |
| **Content Generation** | ✅ Full | ❌ Basic | ✅ Full | ❌ Basic |
| **Brand Voice Learning** | ✅ | ❌ | Partial | ❌ |
| **Multi-Platform** | ✅ | ✅ | ✅ | ✅ |
| **Your Data Stays Local** | ✅ | ❌ Cloud | ❌ Cloud | ❌ Cloud |
| **Auto-Posting** | ❌ (by design) | ✅ | ❌ | ✅ |

We don't auto-post. That's intentional — your accounts stay secure, and you keep full control. Generate the content, then copy/paste to your favorite free scheduler.

---

## What's Inside

```
content-creator-pro/
├── SKILL.md — The brain (agent instructions)
├── SETUP-PROMPT.md — First-run setup guide
├── README.md — You are here
├── SECURITY.md — Security audit details
├── config/
│ └── content-config.json — Platform settings & schedules
├── scripts/
│ └── export-calendar.sh — Export calendar to CSV/markdown
├── examples/
│ ├── content-generation.md — Multi-platform content example
│ ├── repurposing.md — Idea repurposing example
│ └── calendar-planning.md — Weekly calendar planning example
└── dashboard-kit/
 └── DASHBOARD-SPEC.md — Visual dashboard build spec
```

---

## FAQ

**Does this post to my social media accounts automatically?**
No — and that's by design. Auto-posting requires storing your social media credentials and maintaining API connections, which creates security risk and ongoing costs. Content Creator Pro generates the content; you stay in control of posting.

**Are there monthly fees?**
Never. It's $9.99 one-time. You just use your existing LLM provider (Claude, OpenAI, Gemini — whatever your agent runs on).

**What platforms does it support?**
X (Twitter), LinkedIn, Instagram, TikTok (scripts), and Facebook. Each platform has dedicated formatting rules built in.

**Does it learn my writing style?**
Yes. When you edit generated content before posting, the agent tracks what you changed and adjusts your voice profile over time. The more you use it, the more it sounds like you.

**Can I use it for multiple brands?**
Create separate data directories for each brand. The agent supports one active brand profile at a time.

---

## Pairs Well With

- **Daily Briefing Pro** — Stay on top of trending topics for content inspiration
- **Knowledge Vault** — Store brand guidelines permanently for consistent reference
- **Dashboard Builder** — Build a visual content calendar and analytics dashboard
- **DocuScan** — Extract text from brand assets and competitor reports

---

*Built by [NormieClaw](https://normieclaw.ai) — AI skills that just work.*
