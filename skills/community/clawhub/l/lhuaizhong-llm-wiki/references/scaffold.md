# Scaffold

Use this file when creating an initial wiki skeleton.

## Minimal `SCHEMA.md`

```markdown
# Schema

## Purpose
This vault stores compiled knowledge derived from raw sources.

## Directory conventions
- `raw/`: immutable or lightly normalized source material
- `wiki/`: maintained knowledge pages
- `logs/`: maintenance history

## Page naming
- Prefer clear noun phrases
- Reuse existing canonical names when possible
- Avoid duplicate pages that differ only by wording

## Required sections for concept pages
- Summary
- Key points
- Relationships
- Sources
- Open questions

## Linking
- Prefer `[[Wiki Links]]` between pages
- Add at least one related link for non-leaf pages

## Maintenance rules
- Update existing pages before creating duplicates
- Log meaningful structural changes in `logs/knowledge-log.md`
- Mark uncertainty explicitly
```

## Minimal `INDEX.md`

```markdown
# Knowledge Index

## Hubs
- [[Projects]]
- [[People]]
- [[Concepts]]
- [[Timeline]]

## Active topics
- [[Topic A]]
- [[Topic B]]

## Recently updated
- [[Topic C]]
- [[Topic D]]
```

## Starter hub pages

```markdown
# Projects
- [[Project Alpha]]
- [[Project Beta]]
```

```markdown
# People
- [[Person A]]
- [[Person B]]
```

```markdown
# Concepts
- [[Concept X]]
- [[Concept Y]]
```

## Source page pattern

```markdown
# Source - Interview 2026-04-06

## Type
Interview transcript

## Summary
Short description of what this source contains.

## Key extracted entities
- [[Entity A]]
- [[Entity B]]

## Raw location
- `raw/transcripts/interview-2026-04-06.md`

## Notes
- Reliability considerations
- Missing context
```
