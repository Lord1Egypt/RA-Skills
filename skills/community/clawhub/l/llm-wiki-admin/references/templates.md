# LLM-Wiki 场景模板参考

> 生成文件时，将 `<!-- ... -->` 注释中的占位符替换为用户填写的实际内容。

---

## 公共基础组件（所有场景共用）

### BASE_SCHEMA_TYPES（基础页面类型表）
```
| entity     | wiki/entities/    | Named things (people, tools, organizations, datasets) |
| concept    | wiki/concepts/    | Ideas, techniques, phenomena, frameworks              |
| source     | wiki/sources/     | Papers, articles, talks, books, blog posts            |
| query      | wiki/queries/     | Open questions under active investigation             |
| comparison | wiki/comparisons/ | Side-by-side analysis of related entities             |
| synthesis  | wiki/synthesis/   | Cross-cutting summaries and conclusions               |
| overview   | wiki/            | High-level project summary (one per project)          |
```

### BASE_NAMING（命名规范）
```
- Files: `kebab-case.md`
- Entities: match official name where possible (e.g., `openai.md`, `gpt-4.md`)
- Concepts: descriptive noun phrases (e.g., `chain-of-thought.md`)
- Sources: `author-year-slug.md` (e.g., `wei-2022-cot.md`)
- Queries: question as slug (e.g., `does-scale-improve-reasoning.md`)
```

### BASE_FRONTMATTER（前置元数据规范）
所有页面必须包含 YAML frontmatter：
```yaml
---
type: entity | concept | source | query | comparison | synthesis | overview
title: Human-readable title
tags: []

created: YYYY-MM-DD
updated: YYYY-MM-DD
---
```

来源页面额外包含：
```yaml
authors: []
year: YYYY
url: ""
venue: ""
```

> ⚠️ **frontmatter 禁止使用 wikilink**：`original_file`、`source` 等字段若需引用其他页面，改为在正文中用 `[[wikilink]]` 标注，或改为普通字符串（如 `original_file: "Scrum_Master要做些啥？.md"`）。Obsidian 无法在 YAML 中渲染 `[[...]]`。

### BASE_INDEX_FORMAT
```
`wiki/index.md` lists all pages grouped by type. Each entry:
- [[page-slug]] — one-line description
```

### BASE_LOG_FORMAT
```
`wiki/log.md` records activity in reverse chronological order:
## YYYY-MM-DD
- Action taken / finding noted
```

### BASE_CROSSREF（跨引用规则）
```
- Use `[[page-slug]]` syntax to link between wiki pages
- Every entity and concept should appear in `wiki/index.md`
- Queries link to the sources and concepts they draw on
- Synthesis pages cite all contributing sources in the `## Related` section
```

### BASE_RELATED_SECTION（相关页面规范）

`related:` **不放在 YAML frontmatter 中**（Obsidian 无法渲染 wikilink）。改为在页面正文末尾用相关页面 section，**标题跟随 schema 语言**：

```markdown
## Related          ← 英文 schema 用此标题
## 相关页面         ← 中文 schema 用此标题（或 schema 中定义的名称）
- [[page-slug]] — 简短说明关联原因（可选）
- [[另一个页面]]
```

每个页面必须包含此 section，无关联时写 `（暂无）` 或 `N/A`。

### BASE_CONTRADICTION（矛盾处理）
```
When sources contradict each other:
1. Note the contradiction in the relevant concept or entity page
2. Create or update a query page to track the open question
3. Link both sources from the query page
4. Resolve in a synthesis page once sufficient evidence exists
```

---

## 场景 A：研究调研（research）🔬

`extraDirs: ["wiki/methodology", "wiki/findings", "wiki/thesis"]`

### schema.md
```markdown
# Wiki Schema — Research Deep-Dive

## Page Types

| Type | Directory | Purpose |
|------|-----------|---------|
| entity     | wiki/entities/    | Named things (people, tools, organizations, datasets) |
| concept    | wiki/concepts/    | Ideas, techniques, phenomena, frameworks |
| source     | wiki/sources/     | Papers, articles, talks, books, blog posts |
| query      | wiki/queries/     | Open questions under active investigation |
| comparison | wiki/comparisons/ | Side-by-side analysis of related entities |
| synthesis  | wiki/synthesis/   | Cross-cutting summaries and conclusions |
| overview   | wiki/             | High-level project summary (one per project) |
| thesis     | wiki/thesis/      | Working hypothesis and its evolution over time |
| methodology | wiki/methodology/ | Research methods, protocols, and study designs |
| finding    | wiki/findings/    | Individual empirical results or observations |

## Naming Conventions

- Files: `kebab-case.md`
- Entities: match official name where possible (e.g., `openai.md`, `gpt-4.md`)
- Concepts: descriptive noun phrases (e.g., `chain-of-thought.md`)
- Sources: `author-year-slug.md` (e.g., `wei-2022-cot.md`)
- Queries: question as slug (e.g., `does-scale-improve-reasoning.md`)
- Theses: hypothesis as slug (e.g., `scaling-improves-reasoning.md`)
- Methodologies: method name (e.g., `systematic-review.md`, `ablation-study.md`)
- Findings: descriptive slug (e.g., `larger-models-better-few-shot.md`)

## Frontmatter

All pages must include YAML frontmatter:

```yaml
---
type: entity | concept | source | query | comparison | synthesis | overview
title: Human-readable title
tags: []

created: YYYY-MM-DD
updated: YYYY-MM-DD
---
```

Thesis pages also include:
```yaml
confidence: low | medium | high
status: speculative | supported | refuted | settled
```

Finding pages also include:
```yaml
source: "[[source-slug]]"
confidence: low | medium | high
replicated: true | false | null
```

## Index Format

`wiki/index.md` lists all pages grouped by type. Each entry:
```
- [[page-slug]] — one-line description
```

## Log Format

`wiki/log.md` records activity in reverse chronological order:
```
## YYYY-MM-DD
- Action taken / finding noted
```

## Cross-referencing Rules

- Use `[[page-slug]]` syntax to link between wiki pages
- Every entity and concept should appear in `wiki/index.md`
- Queries link to the sources and concepts they draw on
- Synthesis pages cite all contributing sources in the `## Related` section
- Findings link back to their source via the `source:` frontmatter field
- Thesis pages reference supporting and refuting findings in the `## Related` section
- Methodology pages are cited by the findings that used them

## Contradiction Handling

When sources contradict each other:
1. Note the contradiction in the relevant concept or entity page
2. Create or update a query page to track the open question
3. Link both sources from the query page
4. Resolve in a synthesis page once sufficient evidence exists

## Research-Specific Conventions

- Keep the thesis pages updated as evidence accumulates — they are living documents
- Every finding should assess replication status when known
- Methodology pages explain the *why* (rationale) not just the *how*
- Distinguish between direct evidence and inference in finding pages

## Language Rule
- ALWAYS match the language of the source document. If the source is in Chinese, write in Chinese. If in English, write in English. Wiki page titles, content, and descriptions should all be in the same language as the source material.
```

### purpose.md
```markdown
# Project Purpose — Research Deep-Dive

## Research Question

<!-- State the central question this research aims to answer. Be specific and falsifiable. -->

>

## Hypothesis / Working Thesis

<!-- Your current best guess. This will evolve — update it as evidence accumulates. -->

>

## Background

<!-- What prior work or context motivates this research? What gap does it fill? -->

## Sub-questions

<!-- Break down the main question into tractable sub-questions. -->

1.
2.
3.
4.

## Scope

**In scope:**
-

**Out of scope:**
-

## Methodology

<!-- How will you investigate this? What types of sources or experiments are relevant? -->

-

## Success Criteria

<!-- How will you know when you have a satisfying answer? -->

-

## Current Status

> Not started — update this section as research progresses.
```

---

## 场景 B：阅读积累（reading）📚

`extraDirs: ["wiki/characters", "wiki/themes", "wiki/plot-threads", "wiki/chapters"]`

### schema.md
```markdown
# Wiki Schema — Reading a Book

## Page Types

| Type | Directory | Purpose |
|------|-----------|---------|
| entity      | wiki/entities/     | Named things (people, tools, organizations, datasets) |
| concept     | wiki/concepts/     | Ideas, techniques, phenomena, frameworks |
| source      | wiki/sources/      | Papers, articles, talks, books, blog posts |
| query       | wiki/queries/      | Open questions under active investigation |
| comparison  | wiki/comparisons/  | Side-by-side analysis of related entities |
| synthesis   | wiki/synthesis/    | Cross-cutting summaries and conclusions |
| overview    | wiki/              | High-level project summary (one per project) |
| character   | wiki/characters/   | People and figures in the book |
| theme       | wiki/themes/       | Recurring ideas, motifs, and symbolic threads |
| plot-thread | wiki/plot-threads/ | Storylines or narrative arcs being tracked |
| chapter     | wiki/chapters/     | Per-chapter notes and summaries |

## Naming Conventions

- Files: `kebab-case.md`
- Entities: match official name where possible
- Concepts: descriptive noun phrases
- Sources: `author-year-slug.md`
- Queries: question as slug
- Characters: character name in kebab-case (e.g., `elizabeth-bennet.md`)
- Themes: thematic noun phrase (e.g., `social-class-mobility.md`, `deception-vs-honesty.md`)
- Plot threads: arc description (e.g., `darcys-redemption-arc.md`)
- Chapters: `ch-NN-slug.md` (e.g., `ch-01-opening-scene.md`)

## Frontmatter

All pages must include YAML frontmatter:

```yaml
---
type: entity | concept | source | query | comparison | synthesis | overview
title: Human-readable title
tags: []

created: YYYY-MM-DD
updated: YYYY-MM-DD
---
```

Character pages also include:
```yaml
first_appearance: "Ch. N"
role: protagonist | antagonist | supporting | minor
```

Chapter pages also include:
```yaml
chapter: N
pages: "1-24"
```

## Index Format

`wiki/index.md` lists all pages grouped by type. Each entry:
```
- [[page-slug]] — one-line description
```

## Log Format

`wiki/log.md` records activity in reverse chronological order:
```
## YYYY-MM-DD
- Action taken / finding noted
```

## Cross-referencing Rules

- Use `[[page-slug]]` syntax to link between wiki pages
- Every entity and concept should appear in `wiki/index.md`
- Queries link to the sources and concepts they draw on
- Synthesis pages cite all contributing sources in the `## Related` section
- Chapter notes reference characters appearing in that chapter in the `## Related` section
- Theme pages link to the chapters where the theme is most prominent
- Plot thread pages list chapters that advance the arc

## Contradiction Handling

When sources contradict each other:
1. Note the contradiction in the relevant concept or entity page
2. Create or update a query page to track the open question
3. Link both sources from the query page
4. Resolve in a synthesis page once sufficient evidence exists

## Reading-Specific Conventions

- Chapter pages are written during or immediately after reading — capture fresh reactions
- Distinguish between plot summary and personal interpretation in chapter notes
- Theme pages should track *development* across the book, not just state that a theme exists
- Flag unresolved plot threads with status: `open` until resolved
- Note page numbers for important quotes to enable re-finding later

## Language Rule
- ALWAYS match the language of the source document. If the source is in Chinese, write in Chinese. If in English, write in English.
```

### purpose.md
```markdown
# Project Purpose — Reading

## Book Details

**Title:**
**Author:**
**Year:**
**Genre:**

## Why I'm Reading This

<!-- What drew you to this book? What do you hope to get from it? -->

## Key Themes to Track

<!-- What thematic threads do you expect or want to follow? -->

1.
2.
3.

## Questions Going In

<!-- What do you want answered or explored by the end? -->

1.
2.

## Reading Pace

**Started:**
**Target finish:**
**Current chapter:**

## First Impressions

<!-- Update after first chapter or first sitting. -->

>

## Final Takeaways

<!-- Fill in when finished. What did this book teach you? -->

>
```

---

## 场景 C：个人成长（personal）🌱

`extraDirs: ["wiki/goals", "wiki/habits", "wiki/reflections", "wiki/journal"]`

### schema.md
```markdown
# Wiki Schema — Personal Growth

## Page Types

| Type | Directory | Purpose |
|------|-----------|---------|
| entity     | wiki/entities/     | Named things (people, tools, organizations, datasets) |
| concept    | wiki/concepts/     | Ideas, techniques, phenomena, frameworks |
| source     | wiki/sources/      | Papers, articles, talks, books, blog posts |
| query      | wiki/queries/      | Open questions under active investigation |
| comparison | wiki/comparisons/  | Side-by-side analysis of related entities |
| synthesis  | wiki/synthesis/    | Cross-cutting summaries and conclusions |
| overview   | wiki/              | High-level project summary (one per project) |
| goal       | wiki/goals/        | Specific outcomes you are working toward |
| habit      | wiki/habits/       | Recurring behaviours and their tracking |
| reflection | wiki/reflections/  | Periodic reviews and lessons learned |
| journal    | wiki/journal/      | Freeform daily or session entries |

## Naming Conventions

- Files: `kebab-case.md`
- Goals: outcome as slug (e.g., `run-a-marathon.md`, `learn-spanish.md`)
- Habits: behaviour name (e.g., `daily-meditation.md`, `morning-pages.md`)
- Reflections: type + date (e.g., `weekly-2024-03.md`, `quarterly-2024-q1.md`)
- Journal: date slug (e.g., `2024-03-15.md`)

## Frontmatter

All pages must include YAML frontmatter:

```yaml
---
type: entity | concept | source | query | comparison | synthesis | overview
title: Human-readable title
tags: []

created: YYYY-MM-DD
updated: YYYY-MM-DD
---
```

Goal pages also include:
```yaml
target_date: YYYY-MM-DD
status: active | paused | achieved | abandoned
progress: 0-100
```

Habit pages also include:
```yaml
frequency: daily | weekly | monthly
streak: N
status: active | paused | dropped
```

Reflection pages also include:
```yaml
period: weekly | monthly | quarterly | annual
```

## Index Format

`wiki/index.md` lists all pages grouped by type. Each entry:
```
- [[page-slug]] — one-line description
```

## Log Format

`wiki/log.md` records activity in reverse chronological order:
```
## YYYY-MM-DD
- Action taken / finding noted
```

## Cross-referencing Rules

- Use `[[page-slug]]` syntax to link between wiki pages
- Reflection pages reference the goals and habits reviewed during that period
- Goals link to the habits that support them in the `## Related` section
- Journal entries can reference goals and reflections inline with `[[slug]]`

## Contradiction Handling

When sources contradict each other:
1. Note the contradiction in the relevant concept or entity page
2. Create or update a query page to track the open question
3. Link both sources from the query page
4. Resolve in a synthesis page once sufficient evidence exists

## Personal Growth Conventions

- Be honest in journal and reflection entries — this wiki is for you, not an audience
- Update goal progress fields regularly; stale data is worse than no data
- Distinguish between outcome goals (what you want) and process goals (what you will do)
- Reflect on *why* habits succeed or fail, not just whether they did
- Use the synthesis directory for cross-cutting insights that span multiple goals or periods

## Language Rule
- ALWAYS match the language of the source document. If the source is in Chinese, write in Chinese. If in English, write in English.
```

### purpose.md
```markdown
# Project Purpose — Personal Growth

## Focus Areas

<!-- What areas of your life or self are you actively working on? -->

1.
2.
3.

## Motivation

<!-- Why now? What prompted you to start this wiki? -->

## Current Goals (Summary)

<!-- High-level list — create detailed goal pages in wiki/goals/ -->

- [ ]
- [ ]
- [ ]

## Active Habits

<!-- High-level list — create detailed habit pages in wiki/habits/ -->

-
-

## Review Cadence

**Daily journal:** Yes / No
**Weekly reflection:**
**Monthly reflection:**
**Quarterly reflection:**

## Guiding Principles

<!-- What values or principles guide your growth work? -->

1.
2.
3.

## This Year's Theme

<!-- One phrase or sentence that captures your intention for the year. -->

>
```

---

## 场景 D：商业/团队（business）💼

`extraDirs: ["wiki/meetings", "wiki/decisions", "wiki/projects", "wiki/stakeholders"]`

### schema.md
```markdown
# Wiki Schema — Business / Team

## Page Types

| Type | Directory | Purpose |
|------|-----------|---------|
| entity      | wiki/entities/     | Named things (people, tools, organizations, datasets) |
| concept     | wiki/concepts/     | Ideas, techniques, phenomena, frameworks |
| source      | wiki/sources/      | Papers, articles, talks, books, blog posts |
| query       | wiki/queries/      | Open questions under active investigation |
| comparison  | wiki/comparisons/  | Side-by-side analysis of related entities |
| synthesis   | wiki/synthesis/    | Cross-cutting summaries and conclusions |
| overview    | wiki/              | High-level project summary (one per project) |
| meeting     | wiki/meetings/     | Meeting notes, agendas, and action items |
| decision    | wiki/decisions/    | Architectural or strategic decisions (ADR-style) |
| project     | wiki/projects/     | Project briefs, status, and retrospectives |
| stakeholder | wiki/stakeholders/ | People, teams, and organisations involved |

## Naming Conventions

- Files: `kebab-case.md`
- Entities: match official name where possible
- Concepts: descriptive noun phrases
- Sources: `author-year-slug.md`
- Meetings: `YYYY-MM-DD-slug.md` (e.g., `2024-03-15-sprint-planning.md`)
- Decisions: `NNN-slug.md` (e.g., `001-adopt-typescript.md`)
- Projects: descriptive slug (e.g., `payments-redesign.md`)
- Stakeholders: name or team in kebab-case (e.g., `alice-chen.md`, `platform-team.md`)

## Frontmatter

All pages must include YAML frontmatter:

```yaml
---
type: entity | concept | source | query | comparison | synthesis | overview
title: Human-readable title
tags: []

created: YYYY-MM-DD
updated: YYYY-MM-DD
---
```

Meeting pages also include:
```yaml
date: YYYY-MM-DD
attendees: []
action_items: []
```

Decision pages also include:
```yaml
status: proposed | accepted | deprecated | superseded
deciders: []
date: YYYY-MM-DD
supersedes: ""   # slug of ADR this replaces, if any
```

Project pages also include:
```yaml
status: planned | active | on-hold | complete | cancelled
owner: ""
start_date: YYYY-MM-DD
target_date: YYYY-MM-DD
```

## Index Format

`wiki/index.md` lists all pages grouped by type. Each entry:
```
- [[page-slug]] — one-line description
```

## Log Format

`wiki/log.md` records activity in reverse chronological order:
```
## YYYY-MM-DD
- Action taken / finding noted
```

## Cross-referencing Rules

- Use `[[page-slug]]` syntax to link between wiki pages
- Meeting notes reference attendees via `attendees:` frontmatter and `[[stakeholder-slug]]` links
- Decision pages link to the meetings where the decision was discussed
- Project pages link to their key decisions in the `## Related` section
- Stakeholder pages list projects and decisions they are involved in

## Contradiction Handling

When sources contradict each other:
1. Note the contradiction in the relevant concept or entity page
2. Create or update a query page to track the open question
3. Link both sources from the query page
4. Resolve in a synthesis page once sufficient evidence exists

## Business-Specific Conventions

- Write meeting notes during or within 24 hours — memory fades fast
- Action items must have a named owner and due date to be actionable
- Decision pages capture *context and consequences*, not just the decision itself
- Deprecated decisions should link to the decision that superseded them
- Projects should have a retrospective section added on completion

## Language Rule
- ALWAYS match the language of the source document. If the source is in Chinese, write in Chinese. If in English, write in English.
```

### purpose.md
```markdown
# Project Purpose — Business / Team

## Business Context

**Organisation / Team:**
**Domain:**
**Time period covered:**

## Objectives

<!-- What are the top-level business objectives this wiki supports? -->

1.
2.
3.

## Key Projects

<!-- High-level list — create detailed pages in wiki/projects/ -->

-
-

## Key Stakeholders

<!-- Who are the primary people or teams involved? -->

-
-

## Open Decisions

<!-- Decisions currently in flight — create ADR pages in wiki/decisions/ -->

-
-

## Metrics / Success Criteria

<!-- How does the team measure progress toward its objectives? -->

-

## Constraints and Risks

<!-- Known constraints (budget, time, org) and risks to track -->

-

## Review Cadence

**Weekly sync notes:**
**Monthly status update:**
**Quarterly retrospective:**
```

---

## 场景 E：通用（general）📄

`extraDirs: []`

### schema.md
```markdown
# Wiki Schema

## Page Types

| Type | Directory | Purpose |
|------|-----------|---------|
| entity     | wiki/entities/    | Named things (people, tools, organizations, datasets) |
| concept    | wiki/concepts/    | Ideas, techniques, phenomena, frameworks |
| source     | wiki/sources/     | Papers, articles, talks, books, blog posts |
| query      | wiki/queries/     | Open questions under active investigation |
| comparison | wiki/comparisons/ | Side-by-side analysis of related entities |
| synthesis  | wiki/synthesis/   | Cross-cutting summaries and conclusions |
| overview   | wiki/             | High-level project summary (one per project) |

## Naming Conventions

- Files: `kebab-case.md`
- Entities: match official name where possible (e.g., `openai.md`, `gpt-4.md`)
- Concepts: descriptive noun phrases (e.g., `chain-of-thought.md`)
- Sources: `author-year-slug.md` (e.g., `wei-2022-cot.md`)
- Queries: question as slug (e.g., `does-scale-improve-reasoning.md`)

## Frontmatter

All pages must include YAML frontmatter:

```yaml
---
type: entity | concept | source | query | comparison | synthesis | overview
title: Human-readable title
tags: []

created: YYYY-MM-DD
updated: YYYY-MM-DD
---
```

Source pages also include:
```yaml
authors: []
year: YYYY
url: ""
venue: ""
```

## Index Format

`wiki/index.md` lists all pages grouped by type. Each entry:
```
- [[page-slug]] — one-line description
```

## Log Format

`wiki/log.md` records activity in reverse chronological order:
```
## YYYY-MM-DD
- Action taken / finding noted
```

## Cross-referencing Rules

- Use `[[page-slug]]` syntax to link between wiki pages
- Every entity and concept should appear in `wiki/index.md`
- Queries link to the sources and concepts they draw on
- Synthesis pages cite all contributing sources in the `## Related` section

## Contradiction Handling

When sources contradict each other:
1. Note the contradiction in the relevant concept or entity page
2. Create or update a query page to track the open question
3. Link both sources from the query page
4. Resolve in a synthesis page once sufficient evidence exists

## Language Rule
- ALWAYS match the language of the source document. If the source is in Chinese, write in Chinese. If in English, write in English.
```

### purpose.md
```markdown
# Project Purpose

## Goal

<!-- What are you trying to understand or build? -->

## Key Questions

<!-- List the primary questions driving this project -->

1.
2.
3.

## Scope

**In scope:**
-

**Out of scope:**
-

## Thesis

<!-- Your current working hypothesis or conclusion (update as the project progresses) -->

> TBD
```