---
name: hunt
description: Digital bounty hunter skill for finding, tracking, and managing online hackathon opportunities. Trigger when the user says "hunt", "find hackathons", "show map", "add [numbers] to map", or anything related to searching for online/free hackathons, managing a hackathon bucket list, or living a digital nomad/bounty hunter lifestyle. Use to browse the web for upcoming online hackathons, present them as numbered options, add selections to a map.md tracker, and schedule reminders.
compatibility: Requires web fetching (web_fetch tool) to browse hackathon listings from public event pages. Requires cron scheduling for 1-day-before reminders. Requires file read/write for map.md persistence. Network access to mlh.com, devfolio.co, devpost.com, lablab.ai. Node.js 18+ for bundled CLI tools.
license: MIT
metadata:
  author: lloyd-c137
  version: "1.1.0"
  repository: https://github.com/lloyd-c137/hunt-skill
---

# Hunt — Digital Bounty Hunter 🎯

Your mission: help the user find, track, and participate in online hackathons — no boss, no office, just freedom and code.

## Core Workflow

### 1. Trigger: "hunt" / "find hackathons"

When the user says **hunt** or asks to find hackathons, parse the optional argument:

- **`/hunt 1`** — user wants only hackathons **with prize money** (cash prizes)
- **`/hunt`** or **`/hunt 0`** — show all hackathons, prizes optional

Then:

1. **Check USER.md** for the user's skills, timezone (UTC+8 for Lloyd), and preferences.
2. **Browse the web** for upcoming online hackathons that are:
   - **100% online/digital** — no in-person requirement
   - **Free** to participate — no entry fee
   - **No web3 required** — unless user explicitly asks for crypto/blockchain ones
   - **Beginner-friendly** preferred — should suit their skill level from USER.md
3. Query these sources (in order):
   - **MLH** — https://events.mlh.io/ (filter by "Digital")
   - **Devpost** — https://devpost.com/hackathons (filter by online)
   - **Devfolio** — https://devfolio.co/hackathons (filter by online)
   - **lablab.ai** — AI-focused hackathons
4. **Verify each result** — check the event page to confirm it's truly online, free, and open for registration.
5. **Prize filter** (only if `/hunt 1`):
   - For each candidate, fetch the event page and scan for prize information
   - Look for keywords: cash prize, prize pool, $, bounty, grant, award
   - If the page only lists swag bags / fellowship admissions / accelerator invites (no cash), **exclude** it
   - If prize info is unclear, note it and keep it in with a "💰 Prize: Unknown — needs confirmation" label
   - Present only qualifying results to the user

### 2. Present Results as Numbered List

**⚠️ Telegram formatting constraint:** Telegram does NOT support markdown tables. Use simple bullet lists and bold text only.

Format each result clearly (Telegram-friendly):

```
1. [Hackathon Name]
   🗓 Dates: May 8-14, 2026
   🏢 Host: [Organization]
   🎯 Theme: [GenAI / FinTech / Open / etc.]
   📍 Location: Online
   💰 Cost: Free
   💵 Prize: [Cash / Non-cash / None / Unknown]
   🌐 Link: [URL]
   📝 Briefing: [1-2 sentence summary]
```

**Always include a `💵 Prize` line** for every listing — even if the prize is none/unknown, so the user can see at a glance.

**Never use markdown tables** when the answer is going to Telegram. Use bullet-formatted lists instead.

### 3. User Commands

#### "add [numbers] to map"
- Parse the comma-separated list (e.g., "add 1,5,7 to map")
- For each number, append the corresponding hackathon to `map.md`
- Use the standard format (see `references/map-format.md`)
- Set a **cron job** reminder for 1 day before each event starts
- Confirm what was added

#### "remove [numbers] from map" / "delete [numbers]" 
- Remove those entries from `map.md`
- Cancel any associated cron reminders
- Renumber the remaining entries sequentially

#### "show map" / "map"
- Read and present `map.md` in full — formatted nicely for Telegram

#### "clear map" / "reset map"
- Archive `map.md` to `map-archive-YYYY-MM-DD.md` and create a fresh empty one
- Remove all associated hackathon reminder cron jobs

### 4. Setting Reminders

When adding entries to map.md, set a cron job for each:

```json
{
  "schedule": { "kind": "at", "at": "<1 day before event start, ISO-8601>" },
  "payload": { "kind": "systemEvent", "text": "⏰ Hackathon Reminder: [Name] starts in 1 day! Check your map.md for details. https://..." },
  "sessionTarget": "main",
  "deleteAfterRun": true
}
```

Use the hackathon name or a short ID in the job name so you can find/cancel it later.

### 5. Map.md Format

The `map.md` file lives at `~/.openclaw/workspace/map.md`. See `references/map-format.md` for the exact format.

When adding entries, always renumber the full list sequentially (1, 2, 3...).

When removing entries, renumber to fill gaps.

## Criteria for Selection

Only suggest hackathons that meet ALL of these:

- **Online** — Fully digital. No travel or in-person required.
- **Free** — $0 to register and participate.
- **Open** — Registration still open (not ended).
- **Suitable** — Aligns with the user's skills from USER.md. If unknown, ask.
- **No web3** — Skip blockchain/crypto/NFT/DeFi events unless user explicitly asks.
- **Has prize money** — Only when `/hunt 1` is used. Must have cash or monetary prizes; swag-only or incubator-only events are excluded.

## User Profile

Default user is **Lloyd** (Sir):
- **Timezone:** UTC+8
- **Skills:** Coding & AI enthusiast (see USER.md for details)
- Prefers hackathons that don't require web3

## Notes

- Always verify links work before including them.
- If registration is via a form (not open yet), note that in briefing.
- Prefer hackathons starting within the next 2 months unless user asks for longer.
- If no suitable hackathons found, say so honestly — don't pad results with low-quality ones.
- Cron job names should follow: `hunt-reminder-<normalized-name>` for easy management.

## Telegram Output Rules

When delivering output to Telegram:
- **No markdown tables** — Telegram renders them as garbled code blocks
- No markdown headers (`##`, `###`) — Telegram can't render them inline
- Use simple bullet lists with `-` or `•` instead
- Bold with `**bold**` works, but keep it simple
- Numbers with `**bold**` titles for entries (e.g., `**1.** Name`)
- Use emojis as visual separators (🎯, ⏰, 🌐, etc.)
- Keep links plain or in angle brackets `<https://example.com>`
- When presenting map data, format like this:

```
🗺 Map - 5 active

**1.** GHW: GenAI
   🗓 May 8-14 | 🏢 MLH
   🎯 Generative AI | ⏰ Reminder May 7
   🔗 https://events.mlh.io/events/13816

**2.** Midnight Hackathon
   🗓 May 15-17 | 🏢 MLH
   🎯 Open theme | ⏰ Reminder May 14
   🔗 https://events.mlh.io/
``` 
