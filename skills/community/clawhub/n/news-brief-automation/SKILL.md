---
name: news-brief-automation
description: Build, refine, or maintain recurring news-digest workflows that periodically collect items from sources such as Hacker News, GitHub Trending, Hugging Face, RSS feeds, blogs, and specific news sites; deduplicate against the newest prior report; save a Markdown brief in the workspace; and send the same summary to the user. Use when asked to set up scheduled news checks, daily/weekly digests, trend briefings, cron prompt files, or reusable report automation for “check news and send me a summary” tasks.
---

# News Brief Automation

Turn ad-hoc “go check the news and summarize it” work into a repeatable automation made of:

- one prompt file under `automation/cron/`
- one report folder under `reports/`
- one stable output format
- one explicit dedupe rule against the latest saved report

## Workflow

1. Identify the recurring job:
   - source set
   - cadence
   - selection criteria
   - output language
   - save location
   - delivery target
2. Prefer one prompt file per job under `automation/cron/<job-name>.md`.
3. Create a matching report directory under `reports/<topic>/`.
4. Instruct the agent to compare candidates against the newest saved report before drafting the final output.
5. Require “save first, send second” so future runs always have a concrete baseline for dedupe.
6. Make the format stable and easy to skim.
7. If a run has little novelty, emit a short incremental edition instead of padding the report.

## What A Good Cron Prompt Must Contain

Each recurring prompt should explicitly define:

- the goal
- the schedule context
- the priority sources to inspect
- what counts as worth including
- the required output structure
- dedupe rules against the newest prior report
- save path and filename convention
- send-after-save behavior
- fallback behavior if a source is unavailable

Use direct instructions. Avoid fuzzy wording like “make it good” or “summarize nicely”.

## Good Defaults

### Source handling

Prefer primary index pages first, then open individual links only when context is missing.

Common defaults:

- Hacker News: homepage + `newest`
- GitHub: Trending
- Hugging Face: hot/trending models, datasets, spaces
- RSS/blogs: feed page first, article page second
- Generic news sites: homepage/section page first, article page second

### Selection logic

Prioritize items that are:

- newly surfaced
- rapidly rising
- widely discussed
- practically useful
- unusually opinionated or technically deep

For technical audiences, bias toward:

- AI
- developer tools
- open source
- infrastructure
- security
- data engineering
- engineering practice

### Deduplication

Always inspect the newest report in the target report folder.

Keep only:

- new items
- items with clear rank/momentum change
- items with meaningful new developments
- previously seen items that deserve a shorter refreshed mention

Drop or compress:

- unchanged repeats
- low-signal filler
- items included yesterday/last run with no meaningful change

If most candidates repeat prior coverage, explicitly publish an incremental short edition.

### Output structure

Prefer Markdown with:

- dated title
- short “what matters now” section
- numbered list of items
- link for each item
- one-line reason to care
- optional discussion angle / watchpoint

Keep tone concise and opinionated enough to be useful.

## File And Naming Conventions

Use this layout unless the user asks otherwise:

```text
automation/cron/<job-name>.md
reports/<topic>/YYYY-MM-DD.md
reports/<topic>/YYYY-MM-DD-HH00.md
```

Use date-only filenames for once-per-day reports. Use hour-stamped filenames for multiple runs per day.

## Common Patterns

### Daily digest

Use when the user wants one higher-signal summary per day.

Recommended traits:

- 5-10 items
- more synthesis
- a “today’s observation” section
- date-only filenames

### Intraday brief

Use when the user wants multiple updates per day.

Recommended traits:

- 3-8 items
- stronger dedupe
- incremental mode when nothing major changed
- hour-stamped filenames

### Mixed-source trend watch

Use when combining 2-4 complementary sources like GitHub + Hugging Face + HN.

Recommended traits:

- sectioned output per source
- final cross-source observations
- avoid repeating the same project across sections unless the angle differs

## Editing Existing Automations

When converting an existing one-off prompt into a reusable workflow:

1. Preserve the parts that already work:
   - source order
   - output shape
   - report path
2. Remove accidental details that do not generalize.
3. Keep the reusable operating logic:
   - fetch
   - select
   - dedupe
   - save
   - send
4. Move concrete examples and templates into `references/` so `SKILL.md` stays lean.

## Quality Bar Before Packaging Or Publishing

Before packaging or publishing:

- keep `SKILL.md` concise and trigger-focused
- ensure the description clearly says when the skill should activate
- provide at least one reusable prompt template in `references/`
- avoid extra docs like README or changelog files inside the skill
- package the exact skill folder
- reject vague prompts that do not specify dedupe or save paths

## References

- Read `references/examples.md` for concrete example automations.
- Read `references/templates.md` for reusable cron prompt templates.
