# Memory Management Rules

## MEMORY.md Purpose

High-level index, NOT a knowledge dump. Target: ~5K chars (max 10K).

## What Goes In MEMORY.md

✅ Human's preferences & working style
✅ Lessons learned (mistakes to avoid)
✅ Active projects INDEX (1-liner + wikilink to full docs)
✅ Key cross-project decisions
✅ Links to deep knowledge docs

❌ Detailed project timelines → `20-projects/*/timeline.md`
❌ Technical details → `30-knowledge/` docs
❌ Infrastructure → `TOOLS.md`
❌ Daily events → `10-journal/YYYY-MM-DD.md`
❌ Code snippets → `30-knowledge/`

## What "Update Memory" Means

1. **Always:** Update today's journal (`10-journal/YYYY-MM-DD.md`)
2. **If project changed:** Update `20-projects/*/overview.md`
3. **Only if new preference/lesson:** Update `MEMORY.md`

## Memory Search Flow

```
1. User asks about past work
2. memory_search("query")
3. MEMORY.md returns: "[[20-projects/name/overview|Name]] — Brief status"
4. Read full project docs via wikilink
5. Context loaded
```

## Maintenance

**Weekly:** Review journals, extract learnings, update project docs.
**When MEMORY.md > 10K chars:** Audit for detail creep, move specifics out.
