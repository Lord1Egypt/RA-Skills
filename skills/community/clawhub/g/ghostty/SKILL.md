---
name: ghostty
description: "Your always-on digital self — monitors all your communication channels in parallel, learns your writing style, drafts replies in your voice, and routes them to the right channel with one-click approval. Use when: (1) setting up an AI proxy that acts as you when offline, (2) monitoring email, calendar, Slack, WhatsApp, Signal, Telegram in parallel, (3) drafting replies that sound exactly like you not generic AI, (4) building a persistent voice/style profile from your sent messages, (5) routing urgent messages to WhatsApp and formal replies to email, (6) escalating only what matters based on sender importance. Triggers on: be my digital self, always-on proxy, ghost me, respond as me, my AI twin, digital alter ego."
---

# Ghostty — Your Always-On Digital Self

Ghostty is an always-on AI proxy that acts as you when you're unavailable. It watches your channels, learns your voice, drafts replies, and escalates intelligently.

## Core Loop

```
1. MONITOR   → Spawn sub-agents watching email, calendar, Slack, WhatsApp
2. LEARN     → Build voice profile from your sent messages (ongoing)
3. DRAFT     → When meaningful event detected, draft reply in YOUR voice
4. ROUTE     → Send via the right channel (urgent → WhatsApp, formal → email)
5. ESCALATE  → Only interrupt you when it truly matters
```

## Step 1 — First Time Setup: Build Your Voice Profile

Before Ghostty can draft as you, it needs to learn your style. Run the profile builder:

```
scripts/profile_builder.py --source <email-folder or messages-export> --output ghostty/voice-profile.md
```

The builder analyzes:
- Average sentence length and structure
- Common phrases and fillers
- Greeting and sign-off patterns
- Formality level (1-10)
- Preferred punctuation style
- Tone indicators (confident, warm, terse, etc.)

Store the profile at `ghostty/voice-profile.md` in your workspace. Update it monthly as your style evolves.

## Step 2 — Set Up Channel Monitors

Spawn a persistent sub-agent for each channel you want Ghostty to watch. Use `mode="session"` so they run continuously.

**Email (Gmail/Outlook):**
```
sessions_spawn(
  task="You monitor the email inbox for important messages. 
  Rules: (1) Only act on emails from people in the PRIORITY_SENDERS list in ghostty/config.md, 
  (2) For each important email, draft a reply using the voice profile at ghostty/voice-profile.md, 
  (3) Send the draft to the escalation channel (WhatsApp/Signal) with [APPROVE] prefix for one-click send, 
  (4) Mark as TODO in ghostty/pending-drafts.md
  Run continuously. Check every 15 minutes.",
  runtime="subagent",
  mode="session",
  label="ghostty-email"
)
```

**WhatsApp/Signal:**
```
sessions_spawn(
  task="You monitor WhatsApp messages. 
  Rules: (1) Only respond to DND-mode messages or explicit @ghostty mentions, 
  (2) Draft replies using voice profile at ghostty/voice-profile.md, 
  (3) If sender is in PRIORITY_SENDERS, send directly. Otherwise queue for approval.
  Run continuously.",
  runtime="subagent",
  mode="session",
  label="ghostty-whatsapp"
)
```

**Calendar:**
```
sessions_spawn(
  task="You monitor the Google Calendar / Outlook calendar.
  Rules: (1) Alert via WhatsApp 1 hour before any calendar event, 
  (2) If a meeting is about to start and you haven't joined, alert again, 
  (3) If someone invites you to a meeting and you're not available (based on ghostty/availability.md), draft a polite decline using your voice profile.
  Run continuously.",
  runtime="subagent",
  mode="session",
  label="ghostty-calendar"
)
```

## Step 3 — Escalation Rules

Edit `ghostty/config.md` to define:
- `PRIORITY_SENDERS` — list of people who always get a response
- `URGENT_KEYWORDS` — words that trigger immediate WhatsApp alert
- `IGNORE_SENDERS` — newsletters, bots, noise to skip
- `RESPONSE_WINDOW_MINUTES` — how long before drafting (default: 60)
- `APPROVAL_CHANNEL` — where to send drafts for approval (default: WhatsApp)

## Step 4 — Drafting in Your Voice

When a monitor detects something worth responding to:

```
1. Read ghostty/voice-profile.md — get style params
2. Read ghostty/config.md — get context (relationship, ongoing projects, preferences)
3. Fetch the incoming message — understand what it's about
4. Draft reply — apply voice profile (tone, length, phrases, formality)
5. If sender is PRIORITY — send directly
6. If not — queue to ghostty/pending-drafts.md and send preview to WhatsApp
```

**Voice drafting rules:**
- Short replies: aim for same length as you typically write
- Matching tone: if you use "Hey mate" don't use "Dear Sir"
- Reference context: mention anything ongoing (projects, prior emails)
- Signature: include your sign-off style from the voice profile

## Step 5 — One-Click Approval

When a draft is sent to WhatsApp:

```
[Ghostty] Reply to John re: Q4 proposal

Hey John, yeah happy to jump on Tuesday — 3pm works from my end. 
I'll send over the deck beforehand so we can dive straight in.

[APPROVE to send] [EDIT then send] [SKIP]
```

Respond with "APPROVE" on WhatsApp → Ghostty sends the email/WhatsApp reply.

## File Structure

```
ghostty/
├── voice-profile.md      # Your style fingerprint — generated by profile_builder.py
├── config.md             # Priority senders, keywords, escalation rules
├── availability.md       # When you're reachable, timezone, DND hours
├── pending-drafts.md     # Queue of drafts awaiting approval
└── sent-log.md           # History of what Ghostty sent on your behalf
```

## Reference Files

- `references/voice-profile.md` — detailed voice profiling methodology
- `references/channel-monitors.md` — channel-specific setup (Gmail, WhatsApp, Calendar, Slack)
- `references/draft-engine.md` — how to draft contextually in your voice
- `references/delivery-router.md` — escalation logic, urgency routing, approval flows
- `scripts/profile_builder.py` — analyze sample messages, output voice profile markdown

## Safety

- Ghostty never sends without approval UNLESS the sender is in PRIORITY_SENDERS
- All sent drafts are logged in `ghostty/sent-log.md`
- DND hours from `ghostty/availability.md` are respected — no pings during sleep hours
- Review `ghostty/pending-drafts.md` at least once daily
