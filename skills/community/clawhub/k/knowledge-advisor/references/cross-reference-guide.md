# Cross-Reference Guide

How to build and maintain cross-references between books in the knowledge base.

## When to Cross-Reference

After every ingestion, check the new book's frameworks against existing books for:
1. **Same concept, different name** — Two books describe the same idea with different labels
2. **Complementary frameworks** — Frameworks that work well together
3. **Opposing approaches** — Books that disagree on the same topic
4. **Shared domain** — Frameworks from different books in the same application area

## How to Identify Cross-References

1. Read the new book's `frameworks.md` and `principles.md`
2. Read `_index.md` to see existing frameworks
3. For each new framework, check:
   - Does any existing framework address the same trigger situations?
   - Does any existing framework use similar terminology?
   - Does any existing framework contradict this one?
4. Read the matching existing framework files to confirm the connection

## Cross-Reference Format

In `_cross-references.md`:

```markdown
## [Topic]

### [Framework A] ([Book A]) ↔ [Framework B] ([Book B])
**Relationship:** [complementary | overlapping | contrasting]
**How they connect:** [1-2 sentences]
```

## Types of Relationships

### Complementary
Frameworks that work well together or cover different aspects of the same problem.
```
STATE Method (Crucial Conversations) ↔ Care-Challenge Matrix (Radical Candor)
Relationship: complementary
How: STATE provides the conversation mechanics; Radical Candor provides the relational stance.
```

### Overlapping
Frameworks that address the same problem with similar approaches.
```
Mutual Purpose (Crucial Conversations) ↔ Start With Why (Start With Why)
Relationship: overlapping
How: Both emphasize establishing shared purpose before action, from different angles.
```

### Contrasting
Frameworks that offer different or opposing approaches to the same problem.
```
Top-Down Strategy (Book A) ↔ Emergent Strategy (Book B)
Relationship: contrasting
How: Book A advocates planned strategy; Book B argues strategy emerges from action.
```

## Cross-Language Cross-References

When referencing frameworks from books in different languages:
- Use the framework name in its original language + English translation
- The relationship description should be in the language of the `_cross-references.md` file (typically English for mixed-language KBs)

```markdown
### STATE Method (Crucial Conversations) ↔ 面子管理 (Face Management) (《華人領導力》)
**Relationship:** complementary
**How:** STATE addresses Western-style direct dialogue; 面子管理 adds the face-saving dynamics critical in Chinese professional contexts.
```

## Maintenance

- Cross-references are regenerated after each ingestion
- When a book is removed, its cross-references are also removed
- Cross-references do not need manual maintenance unless the user explicitly corrects one
