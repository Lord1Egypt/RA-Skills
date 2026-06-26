# File Layout

## Purpose

Define a local-file storage model for layered conversational memory.

## Root Layout

```text
memory/
  session-state.yaml
  working-buffer.md
  daily/
    YYYY-MM-DD.md
  topics/
    technology.yaml
    career.yaml
    investing.yaml
    research.yaml
    life.yaml
    meta.yaml
  objects/
    papers/
    concepts/
    frameworks/
    decisions/
    preferences/
    open-questions/
  reflections/
    YYYY-MM-DD.md
  indexes/
    manifest.json
```

## File Roles

### `session-state.yaml`
Runtime state for the current or recent session.

Suggested fields:
```yaml
session_id: auto
active_domains: []
active_objects: []
current_goal: ""
recent_constraints: []
last_updated: ""
```

### `working-buffer.md`
Danger-zone buffer when context gets long. Append raw snippets or summaries after the context threshold is reached.

### `daily/YYYY-MM-DD.md`
Daily append-only capture of meaningful events, decisions, corrections, and stable preferences discovered during the day.

### `topics/*.yaml`
Routing cards. Keep them short. They should answer:
- what this theme means for the user
- which subtopics matter
- what was discussed recently
- which related themes are nearby

### `objects/**`
Durable knowledge objects. Separate by coarse type to keep lookup and maintenance simple.

### `reflections/YYYY-MM-DD.md`
Results of daily/periodic reflection. This can document promotions, merges, and stale-memory cleanup decisions.

### `indexes/manifest.json`
Optional generated index containing path, object id, type, domain, summary, tags, and timestamps for faster lookup.

## Naming

- Use kebab-case for filenames.
- Use stable ids inside files, even if filenames later change.
- Prefer one object per file.

## Object Types

Recommended object types for this user context:
- paper
- concept
- framework
- decision
- preference
- open-question
- career-goal
- tech-issue

## Required Object Fields

```yaml
id: object/stable-id
type: paper|concept|framework|decision|preference|open-question
domain: technology|career|investing|research|life|meta
title: Human readable title
summary: Short decisive abstract used for summary-first recall
status: draft|discussed|stable|archived
confidence: low|medium|high
last_discussed: YYYY-MM-DD
```

## Optional Object Fields

```yaml
why_it_matters: Why this should ever be recalled
tags: []
relations: {}
user_takeaways: []
source_refs: []
created_at: ISO8601
updated_at: ISO8601
```
