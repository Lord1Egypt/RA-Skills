---
name: meetup
description: Find nearby OpenClaw meetups and related AI/agent community events, summarize the best matches, and help with reminder or share-ready text. Use when the user asks about events near them, local meetups, hackathons, community gatherings, OpenClaw events, or wants help tracking, comparing, sharing, or setting reminders for AI/agent events.
---

# Meetup

This skill may be presented to users as **claw://Meetup** in user-facing text.

Help the user discover relevant events nearby without wasting tokens or overpromising automation.

## Core rules

- Respond in the user's language.
- Search in the smallest useful scope first, then widen only if needed.
- Keep the output useful, specific, and easy to act on.
- Treat direct user requests differently from background checks:
  - Direct request: always answer, even if nothing suitable is found.
  - Scheduled/background check: silence is acceptable when nothing relevant is found.
- Never recommend, summarize, or remind about past events.
- Never send messages to third parties or create reminders, config changes, or scheduled jobs without explicit user approval.
- Never claim persistent tracking, saved preferences, cron jobs, or API-key setup unless the current runtime actually supports it and the user approved it.
- Treat location data conservatively. Prefer city-level storage over exact postal code when long-term precision is unnecessary.

## Read references only when needed

- Read `references/templates.md` before generating setup text, event lists, no-result responses, share text, reminder text, help, or status.
- Read `references/sources.md` when doing real event discovery, fallback discovery, or broader coverage.
- Read `references/ranking.md` when choosing the best option, building a shortlist, or comparing candidates.
- Read `references/state-and-reminders.md` when the user wants saved preferences, reminders, or ongoing tracking.

## Workflow

### 1) Pick the mode

Choose the lightest mode that matches the request:

1. **Nearby events** — user wants events near them.
2. **Topic search** — user wants events about a topic such as OpenClaw, AI agents, LLMs, or hackathons.
3. **Compare/shortlist** — user wants the best few options, not a dump of listings.
4. **Share help** — user wants share-ready text for one event.
5. **Reminder help** — user wants to remember a specific event.
6. **Setup/help/status** — user wants preferences, help, or a quick reconfiguration.

### 2) Ask only for missing inputs

If needed, gather only the minimum required:

- country
- city or postal code
- search radius
- scope: OpenClaw-only, or broader AI/agent/tech events

Use these defaults when the user does not care:

- radius: 50 km
- scope: OpenClaw first
- search order: likely OpenClaw sources first, then broader event discovery if needed

If a location is ambiguous, ask one short clarification question instead of guessing.

### 3) Search in widening rings

Use sources in this order unless the user explicitly asks otherwise:

1. Official or likely OpenClaw event sources first.
2. Broader event platforms only if the first pass is thin or the user asked for broader AI/tech coverage.
3. General web search only as fallback or comparison.

Keep the search token-efficient:

- Start with 1–2 tight queries.
- Expand only if results are weak, stale, or too narrow.
- Prefer listings with a concrete date, place, and registration or details page.

### 4) Filter hard

Keep only events that are:

- in the future
- inside the requested area, or clearly relevant to the requested scope
- plausibly about OpenClaw, AI agents, LLMs, AI engineering, hackathons, or adjacent tech communities
- backed by a concrete event page or reliable listing

Discard or down-rank items that are:

- missing a date
- missing a location for a location-sensitive request
- duplicate listings for the same event
- generic marketing pages with no real event details

### 5) Turn results into decisions

For each kept event, extract when possible:

- name
- date/time and timezone
- venue/city
- rough distance or local relevance
- one short reason it matches the request
- event link

Do not invent attendance numbers, prices, capacity, organizer details, or travel time.
If something is uncertain, say so briefly instead of bluffing.

### 6) Keep result lists tight

- Default to the best 3 results.
- Show up to 5 if the user asks for more.
- Rank by relevance first, then distance, then freshness.
- If the user is clearly deciding between options, highlight the best pick and why.

### 7) Handle reminders carefully

If the user asks for a reminder:

- confirm which event
- confirm when they want the reminder
- only then propose creating a reminder or cron entry if the environment supports it
- if scheduling is unavailable, offer a manual reminder phrase or explain what can be done in-session

Never imply that a reminder is active unless it has actually been created.

### 8) Handle sharing carefully

If the user asks to share an event:

- generate share-ready text first
- send it anywhere only if the user explicitly asks and approves the send action

## Output guidance

- Use the templates reference for setup, event summaries, no-result replies, reminder text, share text, help, and status.
- Keep the vibe clear and lively, but do not turn the response into promo copy.
- For direct searches with no good result, say so plainly and offer one useful next step: broader radius, broader scope, or another city.
- For broad result sets, summarize only the relevant shortlist, not every listing you found.

## State and persistence

If the runtime supports persistent memory and the user wants ongoing tracking, store only the minimum useful preferences:

- city-level location
- radius
- event scope
- reminder preference

Do not store API keys in memory files.
Do not write config or create scheduled jobs without explicit approval.

## What this skill should not do

- Do not auto-message friends, groups, or communities.
- Do not auto-create calendar entries.
- Do not auto-create cron jobs.
- Do not pretend a source-specific API integration exists unless you actually have the tool path and permission to use it.
- Do not over-search when the first tight pass already answers the question.
