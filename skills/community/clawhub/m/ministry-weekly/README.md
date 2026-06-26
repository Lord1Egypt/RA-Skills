# Ministry Weekly

An OpenClaw skill that turns a one-message Sunday briefing into a complete weekly content package for church staff. Bulletin, scripture context, platform-specific social posts, email, image prompts for graphics, and (when applicable) a sermon series recap. One shot, no back-and-forth.

**Current version: 1.1.1**

## What's new in 1.1.1

- Rewrote the **Privacy and Data Handling** section in SKILL.md to accurately describe Telegram delivery and external-channel scope (rather than understating it)
- Added a **Permissions and Privacy** section to this README so users see scope, the Telegram confirmation gate, and the no-congregant-PII rule before installing
- Narrowed the activation triggers in `description` to require an explicit weekly-content-production context, with a "do NOT trigger" guard against casual church-topic chat and general scripture lookups

## What's new in 1.1.0

- **Church Profile**: a one-time setup that captures church name, tradition, voice, audience, service times, and social channels — so the skill stops asking the same questions every week
- **Sermon Series Threading**: recognizes when a brief is part of an active series and carries context forward week to week (callbacks, current week, recap on demand)
- **Platform-Specific Social Posts**: distinct posts for Facebook, Instagram, X, Threads, and a members-only community group — each optimized for that platform, replacing the previous generic "Facebook or Instagram" output
- **Scripture Context Block**: a 4-6 sentence factual context block for the week's passage with cross-references and an optional discussion question
- **Image Generation Prompts**: ready-to-use prompts for AI image tools (Midjourney, DALL-E, Firefly) covering sermon slide, IG square, and vertical story formats, anchored to the series' graphics theme
- **Series Recap**: a built-in series-level view ("where we've been, where we are, where we're going") for catch-up emails and post-service posts
- **Liturgical sensitivity**: optional liturgy block in the bulletin for traditions that use one
- **Telegram delivery hook**: format and send the full package to a configured Telegram channel after generation
- **Data persistence**: `ministry-data.json` stores church profile, sermon series history, and weekly briefs across sessions

See [CHANGELOG.md](CHANGELOG.md) for the full release history.

## What It Does

Give it a sermon title, scripture, and any announcements. It returns a complete weekly content package:

1. **Bulletin Draft** — clean, formatted, optional liturgy block for liturgical traditions
2. **Scripture Context** — short factual context block with cross-references and a discussion question
3. **Platform-Specific Social Posts** — Facebook (3 posts: mid-week, day-of, post-service), Instagram (caption + story prompts), X (thread + quote tweet), Threads (mini-thread), community/members group (discussion-focused)
4. **Weekly Email** — 150-250 word email with subject line, optional segments for youth/family, volunteers, prayer requests
5. **Image Prompts** — ready-to-use prompts for sermon slide, IG square, vertical story, and optional scripture quote graphic
6. **Series Recap** — when the brief is part of an active sermon series

## How to Trigger It

The skill detects intent from context. Examples:

- "Need content for this Sunday. Pastor is preaching on John 11, theme is resurrection hope. Two services at 9 and 11."
- "Sermon this week is Proverbs 3:5-6. Normal Sunday, 10am, potluck after."
- "We're doing a baptism service Sunday. Romans 6. Also need to announce VBS registration opens Monday."
- "We're starting a new sermon series called 'Sermons in the Hills' — 10 weeks on the Sermon on the Mount."
- "What have we covered in this series so far?"
- "Make me graphics for this week."
- "Send this package to the Telegram channel."

It also responds to casual phrasing like "help me with Sunday's stuff" or "I need content for this week" in a church context.

## First-Run Setup

The first time you use the skill, it will ask a short series of questions to capture the **Church Profile**:
- Church name, tradition, audience description
- Voice preferences (warm/conversational/formal)
- Service days and times
- Which channels you'll publish to
- Social handles

After setup, the skill never re-asks these. Update the profile by saying "update my church profile" or similar.

## How to Install

1. In your OpenClaw workspace, navigate to `.openclaw/workspace/skills/`
2. Create a folder named `ministry-weekly`
3. Copy `SKILL.md` into that folder
4. Restart OpenClaw or reload skills

`ministry-data.json` is created automatically on first run.

## Permissions and Privacy (read before installing)

This skill is instruction-only — it directs the assistant to do things, it doesn't bundle executable code. It runs no background processes, makes no network calls of its own, and has no telemetry.

**What the skill touches**

- **Local file write**: creates and updates `ministry-data.json` in your working directory (church profile, sermon series, weekly briefs). No writes outside that directory.
- **Telegram delivery (optional, confirmation-gated)**: if you add `telegram` to your church profile's `deliveryChannels`, the assistant will format the assembled content package and ask you to confirm before posting it to your configured Telegram channel. Silent auto-posting is not allowed. Posting uses your own Telegram integration; the skill does not bundle credentials.
- **Social/email outputs are drafts**: bulletin, social posts, weekly email, and image prompts are produced for you to review and publish yourself. The skill does not post to Facebook, Instagram, X, Threads, or any email provider.
- **No external lookups**: the skill does not direct the assistant to use web search, browser automation, or scrape any service. Scripture context is generated from the assistant's general knowledge, kept factual and tradition-neutral.
- **No transmission to third parties**: nothing is sent to the skill's author, ClawHub, or any third party. (Your Telegram integration may have its own logging — consult its policy.)

**Congregant privacy rules**

The skill will refuse to store or include any of the following in `ministry-data.json` or in generated content:

- Named congregant prayer requests (anonymized or aggregated only — e.g., "a request from a member" rather than naming the person)
- Attendance lists or named visitor records
- Giving or financial records of any kind
- Any other personally identifying information about congregants

**Tracker-only mode**

If you'd rather not use Telegram delivery, just don't add it to `deliveryChannels`. The skill will still produce the full content package for you to copy/paste into your own publishing tools.

## Notes

- Works with minimal input. If something critical is truly missing (like a service time), it asks one short question. Otherwise it makes reasonable assumptions and flags them at the end.
- Tone defaults to warm and accessible. The church profile's `voicePreferences` and `tradition` override defaults.
- Scripture context stays factual and tradition-neutral — does not push interpretive agendas.
- Image prompts are anchored to the active sermon series' graphics theme for visual consistency week to week.
- Telegram delivery requires the channel to be configured in your OpenClaw setup.

## Skill Metadata

| Field | Value |
|---|---|
| Name | ministry-weekly |
| Version | 1.1.1 |
| Author | Chris (zocase) |
| Compatible with | OpenClaw |
| Category | Content Production |
| Audience | Church staff, ministry communicators |
