---
title: Contributing Guide
tier: 1
tags: [contributing, guidelines, writing-standards, review-checklist]
---

# Contributing Guide

How to add or update reference files in this skill.

---

## File Naming Convention

| Prefix | Tier | Category |
|--------|------|----------|
| (no prefix) | 1 | Core files (key-rules, disambiguation) |
| `*-ref.md` | 2-4 | DDL reference files |
| `_*.md` | 1 | Meta files (scope, examples, contributing, sections) |

### Reference File Naming

Use descriptive, topic-based names:
```
table-ddl-ref.md     # Table DDL reference
index-ddl-ref.md     # Index DDL reference
constraint-ref.md    # Constraint reference
type-ref.md          # Data type reference
```

---

## Frontmatter Standard

Every reference file MUST include frontmatter:

```yaml
---
title: Brief Descriptive Title
tier: 1|2|3|4
tags: [specific, relevant, keywords]
---
```

### Tier Assignment

| Tier | Read Frequency | Content Type |
|------|---------------|--------------|
| 1 | Always | Core rules, scope, examples, contributing |
| 2 | High | Table, index, constraint, type DDL |
| 3 | Medium | View, sequence, partitioning, retention |
| 4 | Low | Trigger, procedure, database, privilege |

### Tags Guidelines

- Include specific keywords users might search for
- Include KWDB-specific terms (TAGS, PRIMARY TAGS, RETENTIONS)
- Include SQL keywords relevant to the topic
- Keep under 15 tags per file
- Use lowercase, hyphenated form

---

## Content Structure

Every reference file should follow this structure:

```markdown
---
title: ...
tier: ...
tags: [...]
---

# Title

Brief description. When to read this file.

## Syntax / Main Section
[SQL syntax examples with comments]

## When to Use
[Decision table or guidelines]

## Common Mistakes (Error vs Correct)
| Wrong | Right | Why |
|-------|-------|-----|

## Validation
[SHOW commands to verify]

## Design Checklist
- [ ] Checklist items
```

---

## Writing Standards

### 1. Show Concrete Examples

**Good:** Complete, runnable SQL
```sql
CREATE TABLE orders (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    amount DECIMAL(12,2) NOT NULL CHECK (amount >= 0)
);
```

**Bad:** Abstract description
```
Create a table with appropriate types and constraints.
```

### 2. Error-First Structure

Always show the wrong pattern first, then the correct one:

```markdown
**Incorrect:**
```sql
-- What's wrong and why
```

**Correct:**
```sql
-- Why this is better
```
```

### 3. Use Semantic Names

**Good:** `users`, `orders`, `customer_id`, `created_at`
**Bad:** `table1`, `col1`, `field`, `t`

### 4. Explain Why, Not What

```sql
-- Good: explains reasoning
price DECIMAL(10,2) NOT NULL  -- DECIMAL prevents precision loss for money

-- Bad: obvious comment
price DECIMAL(10,2) NOT NULL  -- set price as decimal
```

### 5. KWDB-Specific Notes

When KWDB behavior differs from standard SQL or PostgreSQL, call it out explicitly:

```markdown
**KWDB Note:** Time-series tables require TAGS syntax, not standard CREATE TABLE.
```

---

## Adding a New Reference

1. Choose the file name and tier
2. Copy the content structure above
3. Fill in syntax, examples, and mistakes
4. Add frontmatter with title, tier, and tags
5. Update `SKILL.md` tier reference table
6. Add test prompts to `assets/demo-prompts.md`

---

## Review Checklist

Before submitting a new or updated reference:

- [ ] Frontmatter: title, tier, tags are present and accurate
- [ ] Tier matches the read frequency
- [ ] Tags include specific, searchable keywords
- [ ] At least 1 Incorrect/Correct SQL example pair
- [ ] SQL uses semantic names (not table1, col1)
- [ ] Comments explain why, not what
- [ ] Validation commands included
- [ ] Design checklist included
- [ ] KWDB-specific notes where applicable
- [ ] No DML/query examples (only DDL)
- [ ] Listed in SKILL.md tier references
