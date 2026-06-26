# Migration Guide

Use this prompt when the user provides an existing Feishu Base.

## Goal

Determine whether the Base is:

- already a headteacher workspace
- a subject-teacher database
- or a generic Base that needs manual mapping

## Required command

```bash
python3 tools/migration_inspector.py feishu --base-token "<base-token>" --format markdown
```

## Interpretation rules

### Subject-teacher base

Typical signals:

- a mixed `学生信息` table with score columns
- a generic `学生记录` table with text student references
- subject-specific assessment columns such as quizzes, stages, or ranking summaries

Recommendation:

- copy and refactor
- do not overwrite in place

### Headteacher workspace

Typical signals:

- separate student master, score, event, communication, schedule, and artifact tables
- relation-based student references instead of plain name text

Recommendation:

- connect directly

### Generic or unknown

Recommendation:

- inspect manually
- generate a schema mapping before migration
