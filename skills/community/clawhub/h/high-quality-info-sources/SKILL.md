---
name: high-quality-info-sources
description: Build, curate, score, and maintain high-quality information source lists for AI, technology, business, or any topic. Use when the user asks to create a skill for trusted sources, make a watchlist of people/sites/accounts to follow, filter noisy sources into a smaller high-signal set, turn a link dump into a reusable monitoring system, or design a repeatable workflow for tracking official accounts, researchers, critics, and market signals.
---

# High-Quality Info Sources

Build a small, high-signal information radar instead of a giant attention landfill.

## Core workflow

1. Clarify the monitoring goal.
2. Group sources by role, not by popularity.
3. Prefer primary sources over commentary.
4. Keep the default list small.
5. Add a review rule so the list stays useful.

## Clarify the monitoring goal

Start by identifying what the user actually wants to track:

- breaking product/model releases
- research progress
- developer ecosystem changes
- market/industry moves
- critical or skeptical takes
- company-specific monitoring

If the user does not specify, assume they want a balanced monitoring set with:

- official release channels
- technical interpreters
- industry operators
- critics / risk voices

## Group by source role

Do not return a flat pile of links unless explicitly requested. Organize sources into roles such as:

- **Official / primary** — company accounts, labs, docs, release blogs
- **Builders / operators** — founders, engineers, product leads
- **Explainers** — people who interpret developments clearly
- **Critics / risk voices** — people who stress test hype and assumptions
- **Aggregators** — useful only if they add speed or coverage without too much noise

Default ordering:

1. official / primary
2. builders / operators
3. explainers
4. critics / risk voices
5. aggregators

## Quality filter

Prefer sources that satisfy most of these:

- close to the event
- high signal-to-noise ratio
- technically or operationally informed
- consistent over time
- not purely engagement bait
- useful for decisions, not just amusement

Penalize sources that are:

- mostly reposting others
- chronically sensational
- vague and uncheckable
- redundant with better primary sources

## Output patterns

Choose one of these depending on the request.

### 1. Small radar list

Use for users who want the minimum viable watchlist.

Format:

- category
- source name / handle
- why it matters
- what to watch for

Aim for 8-15 sources.

### 2. Extended source map

Use when the user wants broad coverage.

Format:

- grouped categories
- 3-8 entries per category
- short note on each entry
- note on which ones are must-watch vs optional

### 3. Monitoring system

Use when the user wants an operational workflow.

Include:

- the core source list
- refresh cadence
- how to prune the list
- how to summarize findings into notes / Notion / docs

## Maintenance rules

When building a reusable source system, include these rules:

- keep a **core list** and an **overflow list**
- review monthly or when signal quality drops
- remove duplicates aggressively
- cap the default list so attention remains scarce and valuable
- promote only sources that repeatedly produce useful first-order information

## AI-specific default lens

When the user asks for AI information sources and gives no stronger constraint, combine:

- frontier labs
- open-source model players
- infrastructure / hardware players
- respected technical voices
- skeptical / governance voices

Read `references/ai-sources.md` for a starter set and selection logic.

## Tone and judgment

Be opinionated. A source list is a filter, not a census.

Prefer:

- “Follow these 10 first”
- “These 5 are optional”
- “This one is noisy but useful for early chatter”

Avoid pretending all sources are equally good.
