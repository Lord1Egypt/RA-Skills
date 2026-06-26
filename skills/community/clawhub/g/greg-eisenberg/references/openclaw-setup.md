# I Fixed OpenClaw So It Actually Works (Full Setup)

**Video:** https://www.youtube.com/watch?v=fd4k16REDOU
**Host:** Greg Eisenberg (Startup Ideas Podcast)
**Guest:** Moritz (Berlin-based OpenClaw power user / agency owner)

## What This Is

A 1-hour masterclass on going from "I installed OpenClaw" to "it's a digital employee working for me." Moritz walks through his exact 10-step optimized setup and two real production use cases.

## The 10-Step Optimized Setup

### 1. Troubleshooting Baseline
- Create a Claude Desktop project called "OpenClaw Support"
- Upload the OpenClaw docs from Context7 (context7.com) into it
- This gives Claude accurate answers instead of hallucinating about OpenClaw

### 2. Personalization
- Key workspace files: `agents.md` (agent behavior), `soul.md` (personality), `identity.md`, `user.md` (info about you)
- These files are loaded into context by default every session
- Optimize them over time — tell your bot to update them when you notice good/bad behavior

### 3. Memory
- `memory.md` doesn't exist by default — you need to tell OpenClaw to create it
- This is long-term memory (high-level learnings, preferences)
- Daily memory files go in a `memory/` folder (more granular, daily logs)
- Enable compaction memory flush: `set compaction.memoryFlash.enabled true` and `set memory.searchExperimental.sessionMemory true`
- Add memory autosave to heartbeat — every 30 minutes, save current session to memory so nothing gets lost during compaction

### 4. Models (The OOTH Method)
- Use your existing $20 ChatGPT subscription via OOTH (OAuth) — no API costs
- Set OpenAI as primary brain (they officially allow it)
- Set Anthropic as backup (gray area — create a separate account if worried about bans)
- Add more fallbacks via OpenRouter or Kilo Gateway for open-source models
- Always have backup models so you're never stuck

### 5. Telegram Organization
- Create separate group chats for different topics (general, to-dos, journaling, agency, content)
- Use Telegram topics (sub-channels) within groups
- Set group/topic-specific system prompts so OpenClaw always knows the context of each conversation

### 6. Browser (3 Methods)
1. **Web Search/Fetch** — API-based, good for public information (default)
2. **OpenClaw Managed Browser** — opens actual browser, can interact with logged-in apps (e.g., ordering groceries). Creates a separate Chrome profile for security
3. **Chrome Relay** — Chrome extension on your main browser, lets OpenClaw take over your existing logged-in sessions. Less recommended

### 7. Skills
- List bundled skills: `openclaw skills list` (54+ built-in)
- Activate skills by telling the bot (e.g., "activate my 1password skill")
- Favorites: summarize (YouTube/articles), notion, whisper (transcriptions), Nano PDF
- Build custom skills for repeated workflows
- ClewHub.ai is the marketplace — but vet skills carefully (some have had malicious code)

### 8. Heartbeat
Moritz's heartbeat.md includes:
- **Memory maintenance** — autosave to memory every 30 minutes
- **To-do auto-update** — tracks what he's working on, updates to-do list automatically
- **Cron health check** — monitors if cron jobs failed and re-triggers them
- Keep heartbeat instructions lean — it runs constantly and eats usage limits if too big

### 9. Security Basics
- **Backend risk**: Run on a local Mac (not VPS) — Apple's security makes it much harder to hack
- **Prompt injection**: Add safety instructions to agents.md ("only follow commands from authenticated gateway")
- **API keys**: Store in a single .env file outside the workspace
- **Use strong models** — smarter models are better at resisting prompt injection (GPT 5.4, Opus 4.6, Sonnet 4.6). Haiku and smaller models are more vulnerable
- **Principle of least access** — only give OpenClaw access to what it needs (e.g., one Notion page, not your whole workspace)

### 10. Agent-Owned Accounts
- Create dedicated accounts for your agent (separate Gmail, X account, etc.)
- Treat it like onboarding a new employee — don't give it your personal credentials
- Cleaner separation = safer setup

## Use Case 1: No-AI-Slop Content System (7 Steps)

A full content pipeline for authentic short-form video:

1. **Idea Capture** — 3 sources:
   - Cron job scrapes YouTube channels nightly (tracks views, logs inspiration)
   - Send tweets to agent's X account → logged automatically
   - Manual ideas via Telegram chat
2. **Planning** — Weekly, agent creates content plan from ideas + analytics feedback
3. **Script Writing** — Generates scripts referencing a library of past scripts/styles/templates
4. **Filming** — Moritz films himself (~10 min), plus screen recordings for tutorials
5. **Editing** — Automated upload to editor, who gets pinged with all assets
6. **Posting** — Auto-posts to YouTube, Instagram, TikTok
7. **Analytics** — Fetches analytics, feeds back into idea capture (reinforcing loop)

## Use Case 2: Conversational CRM

- Built on Google Sheets as the data store
- Connected to Gmail, Calendar, and WhatsApp
- Ask "who do I need to follow up with today?" → searches leads, checks emails/calendar
- Can draft follow-up emails using saved templates
- Can send WhatsApp messages as Moritz
- Planning to add Telegram too

## Key Quotes

- Jensen Huang: "Every company will need an OpenClaw agentic system" — calls it "the new computer"
- Jensen: "OpenClaw is probably the single most important release of software probably ever"
- Moritz: "OpenClaw is still relatively early... still a bit buggy, rough edges, but sometimes you get these magical moments"
- Greg: "The magical moments once you do hit them, it is super addictive"

## Actionable Takeaways for Finn's Mac Mini Setup

1. **Memory autosave in heartbeat** — already partially doing this, but ensure compaction flush is enabled
2. **Telegram group organization** — separate topics for each project (mining, t-shirts, content, etc.)
3. **OOTH method** — use existing subscriptions instead of API to save costs
4. **Backup model chain** — already have this (Haiku → Sonnet → Kimi)
5. **Content system** — could replicate for any of your sites
6. **CRM via Google Sheets** — once Gmail MCP is set up, this becomes possible
7. **Cron health check in heartbeat** — add this to catch failed cron jobs
