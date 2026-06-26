# Scaling Patterns

## Volume Thresholds

| Scale | Entries | Strategy |
|-------|---------|----------|
| Early | < 20 signals | Single memory.md, minimal namespacing |
| Growing | 20–100 | Split into domains/, basic indexing |
| Established | 100–500 | Full domain × type hierarchy, compaction |
| Mature | > 500 | Archive yearly decisions, summary-only HOT |

## Namespace Structure: Domain × Type

Both dimensions exist simultaneously. A single decision can match both a domain and a type.

```
HOT: memory.md (global risk profile + framework prefs)
  │
  ├── DOMAIN warmth (product / tech / business / personal)
  │     → Load when domain detected in conversation
  │     → Provides: weights, framework defaults, domain-specific patterns
  │
  └── TYPE warmth (strategic / tactical / operational)
        → Load when decision type detected
        → Provides: depth of analysis, recommended add-ons, time horizons
```

**How to handle conflicts:** Domain wins for preference (what to care about); Type wins for process (how deep to go).

## When to Split a New Namespace File

Create a new `domains/{name}.md` when:
- A domain has 10+ domain-specific signals
- User explicitly separates contexts ("for product decisions..." / "when it comes to my personal life...")
- Domain file exceeds 200 lines

Create a new `types/{name}.md` when:
- A decision type has 10+ type-specific patterns
- User distinguishes decision depth explicitly ("quick call" = operational, "long-term bet" = strategic)

## Compaction Rules

### Merge Similar Signals
```
BEFORE (3 entries):
- [03-01] "Reversibility matters" (tech decision)
- [03-05] "Can we undo this?" (tech decision)
- [03-10] "What's the exit strategy?" (tech decision)

AFTER (1 entry):
- tech: prioritize reversibility (confirmed 3x, 03-01 to 03-10)
```

### Summarize Verbose Retrospective Lessons
```
BEFORE:
- When evaluating new technology, we underestimated the team ramp-up,
  we were too optimistic about timeline, and we didn't account for
  integration complexity with existing systems.

AFTER:
- New tech adoption: 2× timeline buffer; check integration complexity early
```

### Archive Decision Records
When moving to COLD:
```
## Archived [YYYY-MM]

### Decision: [slug] (made [date], archived [date])
- Domain: tech
- Outcome: ⚠️ partial
- Key lesson: archived to archive/YYYY.md
- Reason: 90 days elapsed, lessons extracted to domains/tech.md
```

## Index Maintenance

`index.md` tracks all active namespaces:
```markdown
# Decision Making Index

## HOT (always loaded)
- memory.md: 42 lines, updated 2026-03-15

## WARM Domain (load on domain match)
- domains/product.md: 34 lines
- domains/tech.md: 67 lines
- domains/business.md: 22 lines

## WARM Type (load on type match)
- types/strategic.md: 45 lines
- types/tactical.md: 28 lines

## Decision Records (load on retrospective)
- decisions/: 8 files

## COLD (archive)
- archive/2025.md: 134 lines

Last compaction: 2026-03-01
Next scheduled: 2026-04-01
```

## Recovery Patterns

### Context Lost
If agent loses context mid-session:
1. Re-read memory.md (HOT)
2. Check index.md for relevant namespaces
3. Ask user: "What domain and type is this decision? (product/tech/business/personal + strategic/tactical/operational)"
4. Load matching files and continue

### Contradiction Recovery
If memory entries contradict each other:
1. Surface both to user: "I have two conflicting preferences recorded for [domain]. Which is current?"
2. Archive the outdated one with timestamp
3. Confirm the current one remains active
4. Log reversal in reversals.md

### Decision Record Not Found
If a user references a decision that has no record:
1. Try to reconstruct from reversals.md and domains/ patterns
2. Create new record with best-available context
3. Mark as "reconstructed" — do not treat reconstructed info as confirmed
