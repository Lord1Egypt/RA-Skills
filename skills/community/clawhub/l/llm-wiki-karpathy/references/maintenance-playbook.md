# Maintenance Playbook

Use this playbook when the wiki has grown enough that structure drift starts to hurt trust or navigation.

## When To Run A Maintenance Pass

Run a pass when:

- a large batch of raw sources landed
- the wiki is answering well but feels hard to navigate
- the same ideas keep appearing in outputs without dedicated pages
- users report stale, missing, or contradictory notes
- `wiki/index.md` or collection indexes no longer help orient the corpus

## Core Checks

### 1. Source Coverage

Check whether new files in `raw/` are missing corresponding pages in `wiki/sources/`.

Look for:

- unprocessed raw items
- raw files with no manifest record
- raw files with no source page
- source pages that are too shallow to support reuse

### 2. Derived Page Gaps

Check whether the wiki is missing obvious durable pages.

Look for:

- repeated ideas that deserve a `concept` page
- repeated named items that deserve an `entity` page
- repeated cross-source tradeoff or comparison work that deserves a `synthesis` page

### 3. Grounding Quality

Check whether pages remain source-grounded.

Look for:

- weak `Evidence` sections
- `source_refs` that do not correspond to real source pages
- outputs that overstate confidence
- derived pages that sound plausible but cannot be traced back to sources

### 4. Navigation Quality

Check whether generated and human-facing navigation still works.

Look for:

- stale `wiki/index.md`
- missing collection indexes
- pages with no meaningful `Related Notes`
- large clusters of pages that are hard to discover from search or indexes

### 5. Promotion Quality

Check whether the wiki is still treating outputs appropriately.

Look for:

- valuable answers trapped only in `wiki/outputs/`
- recurring question-specific notes that should become durable wiki pages
- concepts or entities repeatedly recreated in multiple outputs

## Cleanup Strategy

Prefer small targeted passes over dramatic rewrites.

Recommended order:

1. run `kb_lint`
2. restore missing source pages and missing generated indexes
3. repair broken `source_refs` or bad canonical paths
4. promote the highest-value repeated ideas into `concept/entity/synthesis` pages
5. rebuild indexes and re-check search quality

## Improvement Ideas

Once the basics are healthy, useful next upgrades include:

- backlink-aware orphan reports
- contradiction or tension candidate reports
- stale-page reports based on update history
- stronger prompts for promoting outputs into durable pages
- workflow wrappers for wiki curation, not only raw-source compilation

Only build tools that remove repeated wiki-maintenance work for the agent.

## Deliverable Format

When reporting a maintenance pass, include:

- the highest-signal issues found
- the pages created or updated
- which problems remain unresolved
- the next one to three highest-value pages or fixes
