# Memory Defragmentation Rules

## Core Principles

1. **Never delete, only archive** — Content might be useful later
2. **Always backup before changes** — Can recover from mistakes
3. **Keep tiering consistent** — HOT = small + frequent, COLD = large + rare
4. **Prefer merge over delete** — Consolidate duplicates into one entry

## Tiering Rules

### HOT Tier (memory.md, ~/self-improving/memory.md)
- Max 100 lines
- Max 50 entries
- Review monthly
- Keep only: confirmed preferences, active rules, current projects

### WARM Tier (domains/, projects/)
- Max 200 lines per file
- Max 50 entries per file
- Review quarterly
- Keep: domain patterns, project specifics, semi-permanent notes

### COLD Tier (archive/)
- Unlimited size
- Review semi-annually
- Keep: old decisions, stale info, reference material

## Entry Age Rules

| Age | Action |
|-----|--------|
| 0-30 days | HOT - actively used |
| 30-90 days | WARM - review for promotion/demotion |
| 90+ days | COLD - archive unless still relevant |

## Duplicate Detection

Entries are considered duplicates if:
- Exact same text (case-insensitive)
- Same concept expressed differently
- References to same topic

## Merge Strategy

1. Keep entry with most context
2. If equal, keep most recent
3. Note merge in log

## Stale Entry Markers

These indicate an entry should be archived:
- "obsolete"
- "deprecated"
- "superseded"
- "no longer relevant"
- Date older than 90 days without update
- "archived" marker

## Formatting Standards

HOT files should have:
```
# Memory (HOT Tier)

## Preferences
- [preference]

## Patterns
- [pattern]

## Rules
- [rule]

---
*Updated: YYYY-MM-DD*
```

## Defragmentation Checklist

- [ ] Backup created
- [ ] Stale entries identified
- [ ] Duplicates found
- [ ] Tier violations flagged
- [ ] Plan reviewed and approved
- [ ] Changes executed
- [ ] Verification passed
- [ ] Original files retained for 24h
