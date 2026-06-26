# Onboarding Guide

Use this guide when the user installs the skill, configures recurring issues, adds sources/signals, asks for a cron/schedule, or customizes the newspaper.

## Core rule: personalize before producing

The first-run experience is not “generate a newspaper with guessed defaults”. The agent must guide the user through setup.

Do **not** create a personalized issue, recurring config, cron job, or external delivery workflow until the Personalization Gate below is complete or the user explicitly confirms a proposed config.

Allowed exception: if the user explicitly asks for a generic demo/sample, generate a clearly labeled demo issue with sample content and say it is not personalized.

## Personalization Gate

Before the first personalized issue or schedule, collect or confirm these choices:

1. **Newspaper identity**
   - Title and optional subtitle.
   - Language.
   - Tone/voice: serious, witty, analytical, magazine-like, executive brief, etc.
2. **Reader promise**
   - What should the newspaper help the user do: stay informed, find ideas, track an industry, brief a team, rediscover saved links, monitor competitors, or something else?
3. **Topics and exclusions**
   - 3–7 recurring topics/interests.
   - Things to avoid: hype, politics, celebrity news, vendor fluff, narrow niches, etc.
4. **Signals and sources**
   - Explicitly ask which of these should be used:
     - X/Twitter bookmarks or liked/saved posts;
     - browser reading list and browser bookmarks;
     - read-later apps such as Pocket, Instapaper, Wallabag, Raindrop, Readwise Reader, Omnivore-style exports;
     - RSS/feed URLs or OPML;
     - newsletters or mailbox searches when configured;
     - pasted URLs/notes/files;
     - web search for recurring topics.
   - Ask whether user-saved signals should outrank general discovery.
   - Ask how unavailable credentialed sources should be handled: exported data, pasted URLs, or skip until configured.
5. **Cadence / scheduling**
   - On-demand, daily, weekly, monthly, or custom.
   - If recurring: day/time/timezone.
   - Ask explicitly whether to create a cron/scheduled job. Never create one silently.
6. **Depth and output**
   - Page count or reading time.
   - Number of lead/features/briefs.
   - Output format: HTML, PDF, Markdown, chat summary, etc.
   - Delivery mode: local file, chat attachment, email, repository artifact, or another configured channel.
7. **Design**
   - Preset: classic newspaper, modern review, weekend magazine, research brief, compact wire.
   - Density: airy, standard, compact.
   - Accent color, image policy, page size.

## Recommended first message

When installing or setting up the skill, ask a compact but real onboarding question block. Example:

> Great — before I generate anything personal, I need your setup choices so I do not invent a newspaper for you.
>
> 1. What should the newspaper be called, and which language should it use?
> 2. Which 3–7 topics should it regularly watch, and what should it avoid?
> 3. Which signals should I use: X/Twitter bookmarks, browser reading list/bookmarks, read-later apps, RSS/newsletters, web search, pasted URLs?
> 4. How often should it appear, and should I create a cron/scheduled job or keep it on-demand?
> 5. Where should it deliver, and in which format?
> 6. Which look do you prefer: classic newspaper, modern review, weekend magazine, research brief, or compact wire?
>
> If you want, answer roughly and I will turn it into a config for your approval.

## Default proposals are allowed, silent assumptions are not

If the user wants speed, propose a starter config in one block and ask for approval. Do not save it, schedule it, or generate the first personalized issue until they confirm.

Bad:

> I will call it The Non-Annoying News, use AI/business/science, make it weekly, and generate it now.

Good:

> Proposed starter config: title “The Non-Annoying News”; weekly PDF; topics AI/software/science/business; sources pasted URLs + X bookmarks + browser reading list; classic compact newspaper. Should I use this, or what should I change?

## Signal-source setup rules

- Present X/Twitter bookmarks and browser reading lists/bookmarks as useful options during setup, not hidden advanced features.
- Treat saved items as intentional signals, but still verify linked content before factual claims.
- If an adapter is not configured, offer import alternatives: pasted URLs, exported bookmark HTML/JSON/CSV, read-later export, RSS OPML, or a local file.
- Never request tokens, cookies, or secrets in chat. Tell the user to configure credentials locally or use an existing CLI/MCP/tool.
- Record inaccessible items as `metadata-only` or `inaccessible`; do not pretend to have read them.

## Cron / scheduled job rule

A cron or scheduled job changes future behavior. Ask explicitly before creating one.

Minimum confirmation before scheduling:

- frequency/day/time/timezone;
- source set;
- delivery target;
- whether external sending is allowed without per-issue approval;
- expected timeout/model/thinking if the platform supports it.

If the user has not confirmed these, prepare the config but do not schedule.

## Recommended starter configurations

Only use these after the user has picked or approved them.

### Personal weekly newspaper

- Cadence: weekly.
- Inputs: user-saved/bookmarked items first; RSS and web search second.
- Output: 2–4 pages, compact newspaper, source notes under articles.
- Selection: 1 lead, 3–5 major articles, 6–10 side/radar items.

### Bookmark rescue issue

- Cadence: on demand or weekly.
- Inputs: X bookmarks, browser reading list/bookmarks, read-later queue.
- Output: “what these saved items actually say and why they matter”.
- Selection: assume saved items are relevant; group by theme and discard duplicates only after preserving the reason.

### Research briefing

- Cadence: on demand or scheduled.
- Inputs: web search, primary sources, selected feeds.
- Output: fewer stories, stronger evidence boundaries, more context boxes.

## Setup finish

After onboarding, summarize the config in plain language:

- title/subtitle/language;
- reader promise;
- topics and exclusions;
- signal sources and their priority;
- cadence/depth and cron decision;
- design preset/density;
- delivery target/format;
- anything still blocked because credentials or exports are missing.

Then ask for confirmation before saving config, scheduling, or creating the first personalized issue.
