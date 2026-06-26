# Journal Pipeline

Autonomous content pipeline for travel editorial sites. Combines SEO research, editorial writing, quality enforcement, and CMS publishing into one loop.

## What It Does

Runs as a PRD-driven loop — pick the next article from your content calendar, execute 7 phases, publish, repeat.

1. **STRATEGY** — Keyword research, competitive gap analysis, article type selection
2. **RESEARCH** — Stay data collection from Payload CMS, external source verification
3. **WRITE** — Editorial draft via `/elite-copywriter` delegation
4. **SEO** — Keyword optimization, AI citation blocks, internal linking
5. **REVIEW** — 8-criterion quality gate (8.0/10 minimum)
6. **PUBLISH** — Direct to Payload CMS with Lexical JSON
7. **SYNC** — Progress tracking, sitemap verification, git commit

## Requirements

- Payload CMS instance with blog-posts and stays collections
- API key with write access
- Content calendar in markdown format
- `/elite-copywriter` skill installed (for delegation)

## Install

```
claude skill install journal-pipeline
```

## Usage

```bash
# Full autonomous pipeline — reads calendar, picks next article
/journal-pipeline

# Specific topic
/journal-pipeline best cabins near Yellowstone

# Research only
/journal-pipeline --research-only

# Draft only, stop after brief
/journal-pipeline --draft-only
```

## Configuration

| File | Purpose |
|---|---|
| `KEYWORD_RESEARCH_AND_CONTENT_CALENDAR.md` | Content pillars and monthly schedule |
| `scripts/ralph/prd.json` | Sprint state persistence |
| `scripts/ralph/progress.txt` | Running log of completed sprints |

## License

MIT
