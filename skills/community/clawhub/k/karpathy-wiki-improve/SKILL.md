---
name: karpathy-wiki-improve
description: "Karpathy LLM Wiki pattern implementation — full ingest/query/relink/lint/DeepResearch pipeline, automatic knowledge graph maintenance, URL-level source traceability. Use when: user says 'organize bookmarks', 'research X', 'run lint', 'relink', or needs a personal knowledge graph."
---

# karpathy-wiki — OpenClaw Implementation

Based on Andrej Karpathy's [LLM Wiki pattern](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f).

---

## Trigger Keywords (Activation)

Activate this skill when the user says anything like:
- "organize bookmarks" / "digest this link"
- "research X" / "help me research"
- "run lint" / "lint check"
- "relink" / "build connections"
- "wiki" / "knowledge graph"
- "Deep Research"

---

## wiki Root

```
wiki_root: /path/to/your/wiki  # configure to your local path
```

```
<wiki_root>/
├── raw/
│   ├── sources/          # raw bookmarks/docs (immutable)
│   └── assets/           # images and resources
├── wiki/
│   ├── entities/        # entity pages (people, products, companies, sites, books)
│   ├── concepts/        # concept pages (tech, theory, methodology)
│   ├── comparisons/     # comparison pages
│   ├── synthesis/       # synthesis/overview pages
│   ├── index.md         # wiki index (entry point)
│   ├── log.md           # operation log (append-only)
│   └── overview.md      # global overview
├── purpose.md           # wiki goal definition (wiki constitution)
└── schema.md            # structure conventions
```

---

## Core Principles

1. **sources/ is read-only** — LLM only writes wiki/, never modifies raw sources
2. **wikilink cross-references** — `[[page-slug]]` syntax for page connections
3. **YAML frontmatter** — every page has type/tags/related/sources
4. **Bidirectional links enforced** — every write to related must sync back-link
5. **Two-phase Ingest** — Analysis → Generation
6. **URL-level traceability** — sources contain specific URLs, not just filenames
7. **Lint-driven** — periodic health checks, graph stays clean
8. **Deep Research** — knowledge gaps auto-discovered and filled

---

## Page Type Taxonomy (entity vs concept boundary)

| Type | Definition | Examples |
|------|------------|----------|
| **entity** | Named, discrete things | people/products/companies/sites/books/tools |
| **concept** | Abstract ideas/theories/methodologies | indexing principles, microservices, DI |
| **comparison** | Multi-option comparisons | Vue vs React, MySQL vs PostgreSQL |
| **synthesis** | Comprehensive overview | tech stack panorama, annual summary |

**Boundary Rules**:
- If it has a specific name → entity ("pdai.tech", "Effective Java")
- If it's abstract/generic → concept ("MySQL indexing", "dependency injection")
- Avoid having both entity and concept for the same topic

---

## Naming Convention

```
entity:
  blogs/sites: use domain or person name
    → mysql-zhu-shuangyin
    → pdai-tech
    → jon-index-blog
  books: use simplified book title
    → effective-java

concept:
  use core terms in kebab-case
    → mysql-innodb
    → jwt-json-web-token
    → dependency-injection

comparison:
  → mysql-postgresql-comparison
  → vue-vs-react

synthesis:
  → go-web-dev-overview
  → 2026-learning-roadmap-summary
```

**Rules**:
- All lowercase, hyphen-separated
- No mixed Chinese/English
- Unique slugs, no duplicates

---

## YAML Frontmatter (Required Fields)

```yaml
---
type: entity | concept | comparison | synthesis
title: Page Title
created: YYYY-MM-DD
updated: YYYY-MM-DD
tags: [tag1, tag2]
related: [page-slug-1, page-slug-2]  # forward reference (back-link auto-added)
sources:
  - file: bookmarks_xxx.md
    urls:
      - https://example.com/article1
      - https://example.com/article2
---
```

**sources.urls is mandatory** — URL-level traceability is a core principle.

---

## Quality Thresholds

Every concept/comparison page **must have**:

| Requirement | Description |
|--------------|-------------|
| One-line definition | frontmatter title or page header `>` |
| Core principles ≥ 3 | body contains at least 3 substantial points |
| Related pages ≥ 1 | related field is non-empty |
| Source URLs | sources.urls is non-empty |
| Back-links added | every page in related back-links to this page |

Every entity page **must have**:

| Requirement | Description |
|--------------|-------------|
| One-line description | frontmatter title |
| Key features ≥ 2 | body has substantive descriptions |
| Related pages ≥ 1 | related field non-empty |
| Source URLs | sources.urls is non-empty |

---

## Page Templates

### Entity Page

```markdown
---
type: entity
title: Entity Name
created: YYYY-MM-DD
updated: YYYY-MM-DD
tags: [tags]
related: [page-slug-1, page-slug-2]
sources:
  - file: bookmarks_xxx.md
    urls:
      - https://example.com
---

# Entity Name

> One-line description (used in index.md summary).

## Overview
Main content and background.

## Key Features
- Feature 1
- Feature 2

## Related
- [[page-slug]] — reason (back-link auto-added)

## Sources
- [Article Title](https://example.com) — source description
```

### Concept Page

```markdown
---
type: concept
title: Concept Name
created: YYYY-MM-DD
updated: YYYY-MM-DD
tags: [tags]
related: [page-slug-1, page-slug-2]
sources:
  - file: bookmarks_xxx.md
    urls:
      - https://example.com/article1
---

# Concept Name

> One-line definition.

## Core Principles
- Principle 1
- Principle 2
- Principle 3

## Use Cases
- Use case 1

## Related
- [[page-slug]] — reason

## Counter-arguments / Data Gaps
- Known limitations
- Uncovered aspects

## Sources
- [Article Title](https://example.com) — source description
```

### Comparison Page

```markdown
---
type: comparison
title: A vs B
created: YYYY-MM-DD
updated: YYYY-MM-DD
tags: [tag1, tag2]
related: [page-slug-a, page-slug-b]
sources:
  - file: bookmarks_xxx.md
    urls:
      - https://example.com/comparison
---

# A vs B

> One-line summary: A is better for X, B is better for Y.

## Overview
Why these two are compared and when this comparison matters.

## Comparison Dimensions

| Dimension | A | B |
|-----------|---|---|
| Dimension 1 | detail | detail |
| Dimension 2 | detail | detail |

## When to Choose A
- Scenario 1
- Scenario 2

## When to Choose B
- Scenario 1
- Scenario 2

## Related
- [[page-slug-a]] — A's entity
- [[page-slug-b]] — B's entity

## Sources
- [Source Title](https://example.com) — source description
```

### Synthesis Page

```markdown
---
type: synthesis
title: Topic Overview
created: YYYY-MM-DD
updated: YYYY-MM-DD
tags: [tag1, tag2]
related: [page-slug-1, page-slug-2]
sources:
  - file: bookmarks_xxx.md
    urls:
      - https://example.com/overview
---

# Topic Overview

> One-line summary of this knowledge domain.

## Scope
What this synthesis covers.

## Key Concepts
- [[concept-1]] — brief description
- [[concept-2]] — brief description

## Key Entities
- [[entity-1]] — brief description

## Landscape
- Trend or pattern 1
- Trend or pattern 2

## Knowledge Gaps
- What needs deeper research

## Related
- [[page-slug-1]] — reason

## Sources
- [Source Title](https://example.com) — source description
```

---

## Operations

### Ingest (Collection & Digestion)

**Phase 1 — Analysis**

```
## Key Entities
Identified entities

## Key Concepts
Identified core concepts

## Main Arguments & Findings
Key arguments and findings

## Connections to Existing Wiki
Relations to existing wiki pages

## Contradictions & Tensions
Conflicts with existing knowledge

## Coverage Gaps
What was mentioned but not covered deeply?
What related topics are missing?

## Recommendations
New/update which pages
```

**Phase 2 — Generation**

1. Create/update target pages (with urls in sources)
2. **Sync related + back-link** (bidirectional link enforcement)
3. Verify pages meet quality thresholds
4. Update index.md
5. Append to log.md

**Output format** — always write exactly this structure, no deviations:

```
## Ingest Plan

### Pages to create/update
| Action | File | Summary |
|---------|------|---------|
| CREATE | wiki/concepts/page-slug.md | 1-line description |
| UPDATE | wiki/entities/backlink-target.md | add related: page-slug |

### Back-link sync
- [[A]] → add B to related → check B has A, add if missing

### index.md update
- Add: `- [[page-slug]] — 1-line description (concept/entity)`

### log.md entry
- `[YYYY-MM-DD] Ingest: N pages, sources: bookmarks_xxx.md`
```

**Phase 2 execution**: follow the plan exactly. Write files using the templates in Page Templates section.

---

### Query

**Always follow this priority when answering:**

1. **Read index.md** → find candidate pages by tag/topic match
2. **Read candidate pages** → extract claims + sources.urls
3. **web_fetch top sources** → verify critical claims (flag ⚠️ if can't reach)
4. **Synthesize** → answer with confidence annotation (✅/⚠️/❌)
5. **Cite sources** → always include the specific URL that confirmed each claim

**When wiki has no relevant page**: fall back to web_search, then optionally ingest the result to wiki.

---

### Relink (Automatic Relationship Discovery)

**Trigger**: batch ingest complete / periodic heartbeat

**Process**:

```
1. Scan all wiki/*.md tags and body text
2. Extract core topics from each page
3. Find page pairs sharing tags/topics
4. Analyze relationship strength pairwise
5. Generate recommended link list (candidate)
6. User confirms before writing (back-link sync)
```

**Execution steps**:

```bash
# 1. Collect all related pairs (shared tags)
grep -r "^tags:" wiki/concepts/ wiki/entities/ | analyze

# 2. List orphan pages
for f in wiki/**/*.md; do
  related=$(grep "^related:" "$f")
  inbound=$(grep -r "^\* \[\[$(basename $f .md)\]\]" wiki/)
  [ -z "$related" ] && [ -z "$inbound" ] && echo "$f is orphan"
done

# 3. LLM generates relink suggestion report
#    Format:
#    [[page-A]] <--> [[page-B]]  reason: shared tag MySQL B+tree
#    [[page-C]] --> [[page-D]]   reason: C mentions D but not linked
```

**Write rules**:
- Update A's related to add B
- Update B's related to add A
- Append to log.md

---

### Lint (Health Check) — Enhanced

**Trigger**: user request / periodic heartbeat

**Scan dimensions** (6):

| # | Dimension | Description |
|---|-----------|-------------|
| 1 | **Orphan pages** | No related pages, no inbound links |
| 2 | **Dangling references** | related references non-existent slugs |
| 3 | **One-way links** | A→B but B→A missing |
| 4 | **Contradiction detection** | Same claim described differently across pages |
| 5 | **Quality threshold** | Page fails minimum quality (no urls/no related/principles<3) |
| 6 | **Naming drift** | Slug style inconsistent (mixed case/mixed Chinese-English) |

**Lint report format**:

```markdown
## Lint Report — YYYY-MM-DD

### Orphan Pages (N)
- [[page]] — no related, no inbound

### One-way Links (N)
- [[A]] → [[B]] (B not back-linking A)

### Dangling References (N)
- [[page]] references non-existent [[nonexistent]]

### Quality Failures (N)
- [[page]] — missing urls source
- [[page]] — empty related

### Contradictions (N)
- [[page-A]] says: X is Y
- [[page-B]] says: X is Z

### Naming Issues (N)
- [[page]] — slug has uppercase/mixed Chinese-English

### Recommended Actions
1. [Priority 1]
2. [Priority 2]
```

---

### Deep Research

**Trigger**: lint finds Coverage Gaps / user says "research X"

**Process**:

```
1. Discover knowledge gap
   lint report "missing coverage" items
   user says "research XXX"

2. Generate 3-5 search queries
   Format: each query should be specific enough to return distinct results
   Example gap "MySQL MVCC":
     → "MySQL MVCC multi-version concurrency control principles"
     → "MySQL MVCC undo log implementation"
     → "MySQL MVCC ReadView isolation levels"

3. Multi-source search
   Execute web_search for each query (max 5 queries)
   Collect top 3 results per query

4. Ingest results
   Write raw search results to raw/sources/deep-research-YYYYMMDD.md
   Execute full ingest pipeline

5. relink + lint
   Complete bidirectional links
   Run lint to verify health
```

**Deep Research output**:
```markdown
## Research Report: [Topic]

### Gap Identified
[What was missing]

### Search Queries Used
1. query text → N results
2. query text → N results

### Key Findings
- Finding 1 [source](url)
- Finding 2 [source](url)

### New Pages Created
- [[new-page-1]] — 1-line description
- [[new-page-2]] — 1-line description

### Recommendations
- [next research direction]
```

---

## purpose.md (Wiki Constitution)

Every wiki should have `purpose.md` defining:

```markdown
# purpose.md

## Goal
Who is this wiki for? What problem does it solve?

## Core Questions
What core questions must this wiki answer?

## Scope
What domains are covered?
What is explicitly excluded?

## Evolution Direction
Near-term (3 months): fill gaps in which domains?
Mid-term (6 months): what state to achieve?
Long-term (1 year): what is the ideal wiki form?

## Quality Standards
What is the minimum quality threshold?
```

---

## Source Traceability Chain

```
User bookmarks (Chrome export)
  ↓
raw/sources/bookmarks_xxx.md  (immutable)
  ↓  Ingest writes
wiki/xxx.md
  sources:
    - file: bookmarks_xxx.md
      urls:
        - https://example.com  ← specific URL
  ↓  Query time
OpenClaw reads wiki → reads sources.urls → web_fetch original URL → verify
```

---

## Use Cases

- User asks technical question (check wiki first, then search)
- User says "help me digest this link"
- User requests "organize my collected content on XXX"
- User requests "run lint"
- User requests "relink"
- User requests "research X" (Deep Research)
- Periodic heartbeat triggers lint + relink + quality check

---

## Confidence Annotations

| Annotation | Meaning |
|------------|---------|
| `✅ Verified` | wiki content matches original URL source |
| `⚠️ Inferred` | wiki content is LLM inference based on source, not direct quote |
| `❌ Disputed` | wiki content contradicts source, needs verification |

---

## Bidirectional Link Write Rules (Enforced)

**Every time you modify the related field**:

```
When writing A's related to add B:
  1. Add B to A's related: [...]
  2. Check if B's related already has A
  3. If not, add A as back-link
  4. If yes, skip
```

**Prohibited**:
- ❌ Write A→B only, skip B→A
- ❌ Leave related empty with no links added
- ❌ sources has only file, no urls

---

## Common Mistakes

| Mistake | Why it's wrong | Correct approach |
|---------|----------------|------------------|
| Create entity + concept for same topic | Double maintenance, confuses graph | Pick one: named → entity, abstract → concept |
| Skip back-link when adding related | One-way links break graph traversal | Always sync back-link when modifying related |
| Use Chinese in slugs | Breaks tooling, inconsistent | Use pinyin or English, not `mysql-suo-yin` |
| Put only filename in sources | Loses URL-level traceability | Always include `urls: [https://...]` |
| Leave concept page with < 3 core principles | Fails quality threshold | Force extraction of ≥ 3 substantive points |
| Write ingest output as prose description | Hard to execute, format inconsistent | Always use structured Ingest Plan format (table + steps) |

## File Setup Reminder

On first wiki setup, you must create:
- `purpose.md` — wiki constitution (goal, scope, quality standards)
- `schema.md` — structure conventions (naming rules, page templates)
- `wiki/index.md` — entry point with domain overview
- `wiki/log.md` — operation log (append-only)

Without these, lint and relink cannot run properly.

---

## Author

[zhangmengyang/karpathy-wiki-improve](https://github.com/zhangmengyang/karpathy-wiki-improve)
