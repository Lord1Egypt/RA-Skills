---
name: llm-wiki
description: Build, maintain, query, archive, and audit a Markdown / Obsidian knowledge Wiki continuously maintained by an LLM. Use this skill to initialize a personal knowledge base; import raw materials grouped by source under source/ into wiki/; organize articles, papers, book notes, interviews, and meeting notes; maintain source pages, entity pages, concept pages, synthesis pages, comparison pages, and query archive pages; update index.md and log.md; answer questions based on the Wiki and archive answers with long-term value; check broken links, orphan pages, duplicate concepts, outdated conclusions, unlabeled contradictions, encoding corruption, and organizational disorder.
---

# LLM Wiki

## Goal

Maintain a Markdown / Obsidian Wiki that is accumulative, linkable, and evolvable. Whenever importing material or answering a question, do not merely generate a summary. Instead, compile new knowledge into existing pages: update entities, concepts, synthesized judgments, comparisons, and query archives so the Wiki becomes more valuable through continued use.

## Default Three-Layer Structure

```text
source/          # Raw material layer: factual sources, read-only by default
wiki/            # Knowledge compilation layer: structured Wiki maintained by the LLM
schema/SKILL.md  # Convention layer: this skill / schema
```

### Knowledge Root Directory

The `Knowledge/` root directory should contain only a small number of structural entry points and tool files. Do not place ordinary knowledge pages there.

Recommended root contents:

```text
Knowledge/
  source/
  wiki/
  schema/
  verify_wiki.py   # Optional compatibility wrapper delegating to schema/scripts/verify_wiki.py
  README.md        # Optional: minimal entry point
```

The root directory should not contain:

- Single-source summaries;
- Concept pages;
- Synthesis pages;
- Topic maps;
- Temporary organization reports.

If a root entry point is needed, create a minimal `Knowledge/README.md` that only links to:

- `[[Knowledge/wiki/README]]`
- `[[Knowledge/wiki/index]]`
- `[[Knowledge/wiki/syntheses/Knowledge Wiki Topic Map]]`
- `[[Knowledge/wiki/log]]`
- `[[Knowledge/source]]`

Principle: the root directory is for “entry points”; `wiki/` is for “knowledge”.

### source/

- Raw materials are read-only by default. Do not rewrite their body text.
- Preserve original titles, authors, URLs, dates, clipping metadata, image references, and similar source information.
- If original materials need to be renamed or supplemented with metadata, ask the user for confirmation first.

### wiki/

Use English for the default directory names in the English schema:

```text
wiki/
  index.md      # Main index; keep the English file name
  log.md        # Operation log; keep the English file name
  README.md     # Wiki documentation; keep the English file name
  sources/
  entities/
  concepts/
  syntheses/
  comparisons/
  queries/
```

Conventions:

- Except for agreed convention files such as `index.md`, `log.md`, `README.md`, and `schema/SKILL.md`, use readable English directory and file names whenever possible.
- Terminological proper nouns may remain in English or use mixed Chinese-English naming, for example `AI Agent.md`, `OpenClaw.md`, `Claude Code.md`, or `Harness Engineering.md`.
- Use canonical plural English directories such as `sources/`, `concepts/`, and `entities/`. If historical empty duplicates are found, clean them up. If they contain content, migrate that content into the canonical directories and update links.
- File names should be readable, clickable, and maintainable over the long term. Avoid machine-style prefixes such as `source-*`, `concept-*`, or `synthesis-*`.

## Page Types

### Source Pages: `wiki/sources/`

Use source pages to summarize and locate a single source. A source page should include:

- Source information: original file, URL, author, and date.
- A one-sentence summary.
- The question this source helps answer: this must be extracted as a unique question from the original text; **do not reuse generic descriptions across pages**.
- Key structure / section clues.
- Knowledge points worth preserving: these must be concrete judgments extracted from the original text; **do not use generic guidance such as “if the article discusses X, preferentially connect it to Y”**.
- Related concept / entity / synthesis pages.
- Follow-up close-reading tasks.

### Entity Pages: `wiki/entities/`

Use entity pages for people, organizations, products, projects, tools, and similar objects. Entity pages hold facts and background; they should not carry excessively long arguments.

- Create entity pages only for knowledge objects: people, organizations, products, projects, tools, and similar items should enter the entity layer only when they themselves are analysis objects or when they carry reusable facts. Do not create an entity page merely because someone is the author of a source. Do not maintain article-author lists on entity pages. Keep author information in the source page's source information or in `source/` metadata.

Recommended structure: `Positioning → Key information (structured fact table) → Core capabilities / product features → Role in the knowledge base → Related sources → Related pages`

### Concept Pages: `wiki/concepts/`

Use concept pages for methods, patterns, theories, problem framings, frameworks, and similar ideas. Prefer reusing and updating existing concept pages to avoid synonym duplication.

Recommended structure: `Definition → Core understanding / judgments → Relationship to neighboring concepts → Related sources → Related pages`

**Anti-template rules**:

- Each concept page's “Relationship to neighboring concepts” section must explain concrete relationships one by one. **Do not use generic template paragraphs such as “it gathers views scattered across multiple sources into a reusable concept.”**
- Each concept page should include at least: a clear definition, 2+ unique core judgments, and relationship explanations with 2+ related concepts.

### Synthesis Pages: `wiki/syntheses/`

Use synthesis pages for cross-source judgments, frameworks, thematic overviews, case matrices, architecture analyses, and similar compiled knowledge.

Each synthesis page should include at least: a core judgment, multi-source synthesis (not single-source retelling), and cross-references to 3+ source pages.

### Comparison Pages: `wiki/comparisons/`

Use comparison pages to distinguish easily confused concepts, products, paradigms, or solutions, for example `Reasoner vs Agent.md`.

Recommended structure:

1. One-sentence conclusion;
2. Definitions of the compared objects;
3. Comparison table;
4. Decision method / usage scenarios;
5. Common misconceptions;
6. Relationship to the knowledge-base main threads;
7. Related sources;
8. Related pages.

Minimum quality requirements:

- Column names in comparison tables must not use generic placeholders such as `A / B`; write the concrete objects being compared.
- The page must explain “when to choose A and when to choose B”.
- The page must link to at least 2 concept pages or synthesis pages.
- Do not reuse generic paragraphs such as “when discussing model capability, first determine...” that could be applied to any comparison page.

### Topic Map Pages: `wiki/syntheses/`

A topic map page is a type of synthesis page. It organizes the Wiki's long-term reading paths and thematic main threads. Do not place it in the `Knowledge/` root directory.

Recommended locations:

- `wiki/syntheses/Knowledge Wiki Topic Map.md`
- Or a topic-specific name, such as `wiki/syntheses/Agent Engineering Topic Map.md`

A topic map should include:

- The Wiki's current core question;
- 3-9 thematic main threads;
- Recommended reading order for each thread;
- Entry concept pages, key synthesis pages, core source pages, and related comparison pages;
- Page-type usage notes;
- Follow-up organization priorities.

Division of responsibilities with `index.md`:

- `index.md` keeps the full entry list and page catalog;
- The topic map is responsible for knowledge structure, reading paths, and thematic navigation;
- Do not make `index.md` carry too much explanatory content, otherwise it will become an overly long essay.

### Query Pages: `wiki/queries/`

Archive question-and-answer outputs with long-term value as reusable pages. A query page should answer a clear question and link back to related source, concept, and synthesis pages.

## Core Workflows

### Initialize the Wiki

1. Scan the directories, file types, and source groupings under `source/`.
2. Create or update `wiki/index.md`, `wiki/log.md`, and `wiki/README.md`.
3. Create source pages for the first batch of materials.
4. Extract entity, concept, synthesis, and comparison pages.
5. Update the index and log.
6. Check broken links, encoding corruption, duplicate directories, and empty directories.

### Import Materials

1. Read `wiki/index.md` first to locate existing related pages.
2. Read the new source and extract its summary, key structure, entities, concepts, and reusable judgments.
3. Create or update the source page.
4. Update existing entity pages, concept pages, and synthesis pages. Prefer updating existing pages; do not lightly create duplicate concepts.
5. Mark relationships: supports, supplements, revises, contradicts, or needs verification.
6. Update `wiki/index.md` and `wiki/log.md`.
7. Run broken-link and encoding-corruption checks.

### Topic Batch Import

When importing 5 or more materials under the same topic in one batch, do not only create multiple source pages. Establish a topic structure as well.

Steps:

1. Determine whether a corresponding synthesis page or topic-map entry already exists;
2. Create a source page for each source;
3. Create or update a topic synthesis page, for example:
   - `Claude Code Source Architecture Map`
   - `Agent-Era Startup Methodology`
4. Extract shared concepts and entities; avoid creating duplicate concepts for every source;
5. Present the batch as a group in `index.md`;
6. Add the topic's reading path to the topic map;
7. Record the batch in `log.md` by topic, rather than as a per-file operation ledger.

### Answer Questions Based on the Wiki

1. Read `wiki/index.md` first.
2. Then read relevant pages. Do not scan the entire Wiki by default.
3. Cite Wiki page links in the answer.
4. If the answer has long-term value, archive it under `wiki/queries/` or update a synthesis page.
5. Update `wiki/log.md`.

### Wiki-Layer Reorganization / Thematic Refactoring

Use this when `source/` already contains many imported materials, `wiki/` has grown in page count, and the user wants to improve navigability, thematic clustering, and long-term maintainability.

Steps:

1. Run the audit script or equivalent checks first, confirming:
   - source coverage;
   - broken links;
   - index coverage;
   - UTF-8 issues;
   - thin pages / template remnants.
2. Read `wiki/index.md`, `wiki/README.md`, `wiki/log.md`, and existing synthesis pages.
3. Identify the Wiki's thematic main threads; do not organize mechanically by source directory.
4. If the page count is large, create or update a topic map page, for example: `wiki/syntheses/Knowledge Wiki Topic Map.md`.
5. Clarify the division of responsibilities between `index.md` and the topic map:
   - `index.md`: full catalog;
   - topic map: reading paths, thematic main threads, and knowledge architecture.
6. Prioritize refactoring:
   - weak comparison pages;
   - thin concept pages;
   - synthesis pages with unclear thematic ownership;
   - long lists in `index.md` that are hard to navigate.
7. Update `README.md`, `index.md`, and `log.md`.
8. Finally rerun broken-link, coverage, index, and encoding checks.

### Enrich Existing Pages

1. Read the target page and related sources.
2. If the existing sources are insufficient to support a complete concept, external information may be searched and added with attribution.
3. After enrichment, update the page's `updated` date.
4. Check bidirectional-link completeness.

## Page Quality Audit

Regularly check for thin pages and template remnants. Passing broken-link checks does not mean the knowledge quality is sufficient.

### Thin Page Identification

The following pages should be reviewed first:

- Concept pages under 800 characters;
- Entity pages under 800 characters;
- Synthesis pages under 1200 characters;
- Comparison pages under 1000 characters;
- Source pages that only have summaries and lack “the question this source helps answer” and “knowledge points worth preserving”.

A thin page does not necessarily have to be expanded, but it must be judged:

- Is it only a temporary placeholder?
- Should it be merged into an existing page?
- Should it be upgraded into a full concept page?
- Should it simply be deprioritized in the index or topic map?

### Template Remnant Check

Search especially for:

- “it answers a long-term question”;
- “if the article discusses”;
- A generic “Why it matters” section;
- “to be added”;
- “TODO”;
- `A / B` placeholder column names;
- Generic “How to use this comparison” paragraphs.

When template remnants are found, rewrite them into concrete judgments based on the original source materials and related pages. Do not merely delete the heading.

## Audit Script

The publishable audit script for the current Knowledge Wiki is located at:

```bash
python3 Knowledge/schema/scripts/verify_wiki.py
```

For compatibility with existing commands, this vault also keeps a root-level wrapper:

```bash
python3 Knowledge/verify_wiki.py
```

When publishing the skill, package `Knowledge/schema/scripts/verify_wiki.py` as `scripts/verify_wiki.py` inside the skill package, together with `SKILL.md`; the root-level wrapper is only a convenience entry point for this vault.

Run the audit script after every batch import, refactor, rename, or topic-map update.

Passing criteria:

- `Sources without ziliao: 0`
- `Broken wikilinks: 0`
- `Pages not in index.md: 0`
- `UTF-8 issues: 0`

If script output conflicts with human judgment, human inspection takes precedence, but the reason must be recorded in `wiki/log.md`.

Do not mechanically create low-quality source pages merely to pass the script. Source pages still need to meet the minimum quality standard for source pages.

## `index.md` Specification

`wiki/index.md` is the navigation entry point. Recommended structure:

```markdown
# Knowledge Wiki Index

## Quick Links

## Sources

## Entities

## Concepts

## Syntheses

## Comparisons

## Queries
```

Each record should preferably include:

```markdown
- [[Knowledge/wiki/concepts/Context Engineering]] — one-sentence description; status: evolving.
```

## `log.md` Specification

`wiki/log.md` is a date-based timeline for phase-level changes, not an overly granular operation ledger. Update principles:

- **Merge by date**: imports, refactors, queries, and maintenance performed on the same day should be merged under `## YYYY-MM-DD｜Topic Overview` whenever possible, using `###` to group by topic.
- **Record phase-level results**: preserve key sources, key newly created or updated pages, core conclusions, and important maintenance decisions. Do not append a separate entry for every small operation.
- **Create separate detail pages when needed**: place bulk mappings, long audit checklists, image migration tables, complex experiment logs, and similar details in the corresponding synthesis page or under `wiki/queries/`. `log.md` should only link to a summary.
- **Rewrite the same-day section when updating multiple times in one day**: prefer editing and merging the existing section for the day instead of appending fragmented entries.
- **Preserve follow-up direction**: a short “Current To-Dos / Follow-Up Directions” list may be maintained at the end, but keep it concise.

Recommended format:

```markdown
## YYYY-MM-DD｜Topic Overview

### Topic One

- Import/update scope: ...
- Created/updated: [[Knowledge/wiki/...]], [[Knowledge/wiki/...]]
- Key conclusion: ...

### Topic Two

- ...

## Current To-Dos / Follow-Up Directions

- [ ] ...
```

Common topics:

- Initialization and structural adjustment.
- Topic-based source import.
- Concept / synthesis page deepening.
- Query archiving.
- Audit and maintenance.
- Schema / skill rule updates.

## Frontmatter Recommendations

Source page:

```yaml
---
type: source
tags: [source-summary]
source_file: "[[Knowledge/source/...]]"
source_name:
author:
url:
created: YYYY-MM-DD
updated: YYYY-MM-DD
status: initialized
---
```

Entity page:

```yaml
---
type: entity
tags: [entity]
created: YYYY-MM-DD
updated: YYYY-MM-DD
status: evolving
---
```

Concept page:

```yaml
---
type: concept
tags: [concept]
created: YYYY-MM-DD
updated: YYYY-MM-DD
status: evolving
---
```

Synthesis page:

```yaml
---
type: synthesis
tags: [synthesis]
created: YYYY-MM-DD
updated: YYYY-MM-DD
status: evolving
---
```

Comparison page:

```yaml
---
type: comparison
tags: [comparison]
created: YYYY-MM-DD
updated: YYYY-MM-DD
status: evolving
---
```

Query page:

```yaml
---
type: query
tags: [query]
created: YYYY-MM-DD
updated: YYYY-MM-DD
status: archived
---
```

## External Search Boundaries

By default, prioritize internal materials under `Knowledge/source/` and `Knowledge/wiki/`. Do not use external search to replace existing sources.

External search may be used when:

- The user explicitly asks for the latest information;
- A concept page needs a standard definition or official documentation;
- Facts in a source are time-sensitive and may affect the conclusion;
- The latest status of a product, model, company, paper, or regulation needs to be verified.

When using external search:

- Prefer official sources, papers, and original announcements;
- Add external source links to the page;
- Distinguish “the original source's viewpoint” from “externally verified facts”;
- Do not mix unverified web information into stable conclusions.

## Link Rules

- Use Obsidian Wiki links: `[[Knowledge/wiki/concepts/Context Engineering]]`.
- When linking to vault files, use paths relative to the vault root. Do not use absolute paths.
- After renaming files, batch-update all `[[...]]` links.
- When responding to the user, prefer clickable Wiki links whenever possible.
- **Bidirectional link principle**: when concept A references concept B, B's page should also include a backlink to A. Concept pairs with blurry boundaries (such as Harness / Environment, Vibe Coding / Agentic coding) should explain their relationship on both pages.

## Encoding Safety Rules

Chinese content must be written as UTF-8. In Windows / PowerShell environments, writing Chinese directly with PowerShell here-strings, `Add-Content`, or `Set-Content` can easily produce question-mark corruption.

Prefer:

- Use `apply_patch` to modify Markdown;
- Or create a `.py` script and write text with `Path.write_text(..., encoding="utf-8")`;
- Or verify file content with Python `read_text(..., encoding="utf-8")`.

Avoid:

- Writing large Chinese blocks directly inside PowerShell command strings;
- Judging whether a file is corrupted based only on terminal display output.

After every batch write, check for:

- Repeated question marks;
- Unicode replacement characters;
- Typical mojibake markers;
- Broken links.

## Images and Attachments

- Do not batch-download external images in `source/` by default, unless the user requests it or the image is critical for long-term understanding.
- If images need to be localized, download them to the vault attachment location and convert the Markdown image syntax to an Obsidian image embed: `![[image.png]]`.
- The raw material layer is read-only by default. Confirm before localizing images or rewriting original materials.

## Safety Principles

- Do not overwrite the user's original materials.
- Do not delete non-empty directories unless you have confirmed that their contents have been migrated or the user explicitly requested deletion.
- Before bulk moves or renames, create a mapping. After execution, check broken links.
- Explicit user preferences override this schema, for example directory naming, whether reports should be kept, or whether `README.md` should keep its English name.
