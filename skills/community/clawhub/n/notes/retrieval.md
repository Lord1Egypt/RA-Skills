# Retrieval — Finding the Note Again

Every note is written once and found zero or more times. This file is about raising that number: naming, tags, links, indexes, search order, and the maintenance that keeps the corpus honest.

**Contents:** [Search Order](#search-order) · [Naming](#naming) · [Tags](#tags) · [Folders](#folders) · [Links and Maps](#links-and-maps) · [The Index](#the-index) · [Monthly Sweep](#monthly-sweep) · [Archiving](#archiving) · [When Nothing Is Found](#when-nothing-is-found) · [Retrieval Traps](#retrieval-traps)

**Before searching**, read `index.md` if `## Boxes` names it, and `## Conventions` in `~/Clawic/data/notes/memory.md`. The tag vocabulary and the filename pattern determine which search will work; guessing at them turns a two-second lookup into a full-text crawl.

## Search Order

Always the same four steps, cheapest first. Stop at the first hit.

1. **Title.** Filename and frontmatter `title`. If the corpus follows Rule 2, this resolves most lookups.
2. **Tag or person.** `index.md` if it exists; otherwise a frontmatter grep.
3. **Full text.** `grep -ri` over the corpus, plus the search command of each configured platform (`local.md` and the platform files).
4. **Time.** The date range around a remembered event — the last resort, because dates are what people misremember.

**The diagnostic that improves the corpus**: if step 3 was the only step that worked, the title was wrong. Rename the note to state the claim, in the same turn, using the platform's own rename so links survive (`obsidian.md`). Skipping the rename guarantees the same note is hard to find next time.

Search across platforms returns results with their source prefix, so the user knows which app to open:

```
"pricing"
local:    2026-07-26_product-sync — "Pricing: staying at three tiers"
notion:   Q3 Pricing Review (Notes DB)
bear:     #product/pricing — "Tier experiments"
```

## Naming

- **`YYYY-MM-DD_topic-slug.md`** with `filename_pattern: date-first`: directory order is chronological, and a series (`_product-sync`) stays greppable. `title-first` inverts it for corpora browsed by subject in a file tree; pick one and record it in `## Conventions`, because a mixed corpus sorts usefully by neither.
- **Journal is `YYYY-MM-DD.md`**, no slug. It is the one type where the date *is* the subject.
- **Quick captures carry a time**: `YYYY-MM-DD_HH-MM_topic.md`. Two captures on one subject on one day collide otherwise.
- **Slug of 2-5 words, lowercase, hyphens.** Long slugs get truncated in every UI that shows filenames; the full claim lives in `title`.
- **Never rename to fix a typo in a slug** unless links are updated in the same operation. A cosmetic rename that breaks four backlinks is a net loss.

## Tags

Tags exist to cut across folders. That is their only job, and it sets their limits.

- **A tag matching >10% of the corpus does not discriminate** — at 64 notes, a tag on 7+ of them is a candidate for promotion to a note type, a folder, or a project. Check at the monthly sweep.
- **A tag used once is a typo or an orphan.** Merge it into the nearest existing tag or delete it. Singleton tags are most of what makes a tag list unusable.
- **Working ceiling ~20 live tags.** Past that, nobody remembers the vocabulary, so new notes get new near-synonyms (`#pricing`, `#price`, `#pricing-2026`) and retrieval degrades to full-text.
- **Nested tags only where the platform supports them** (Bear, Obsidian): `#product/pricing`, two levels maximum. Three levels is a folder tree pretending to be tags. Governed by `tag_style`.
- **One vocabulary, recorded.** The live tag list belongs in `## Conventions` (or `index.md` once it exists) — a vocabulary that exists only in the user's head grows synonyms every week.
- **Tags are not statuses.** `#todo`, `#wip`, `#done` rot instantly because nobody updates a tag; status belongs in frontmatter or in `actions.md`.

## Folders

- **One dimension only: note type** (`meetings/`, `decisions/`, `journal/`, `projects/`, `research/`, `quick/`). A note has exactly one type and several subjects; putting the subject in the folder tree loses every subject but one.
- **No nesting beyond type**, except archives (`journal/2025/`). A tree deep enough to browse is a tree deep enough to misfile into.
- **Platform folders and notebooks mirror the types**, so a note keeps its identity when routing changes: Apple Notes folders, Bear tag roots, Notion `Type` property, Evernote notebooks.
- **A folder with fewer than three notes after six months is not a category** — fold it back.

## Links and Maps

- **A link earns its place by being followed.** Link the decision a meeting implements, the source a claim comes from, the project a status belongs to. Linking every mention of every noun produces a graph nobody navigates.
- **Wikilinks (`[[note]]`) only where the platform resolves them** — Obsidian, Bear, Logseq. In plain markdown read outside an app, relative paths (`../decisions/2026-07-14_pricing-tiers.md`) are the portable form and survive migration (`migration.md`).
- **A map-of-content note** — a hand-written index for one subject — earns its place when a tag exceeds ~20 notes and the tag listing stops being readable. Before that it is duplication with a maintenance cost.
- **Backlinks are the reason to link at all.** In a platform with no backlink support, a one-way link buys much less, so spend the effort on titles and tags instead.

## The Index

`index.md` is created at 30 notes (SKILL.md Rule 7) and updated in the same turn a note is created, renamed, or archived. Structure and the 20-row cap on `## Recent`: `memory-template.md`.

- **Under 30 notes, `grep -r` wins outright**: it is instant, always current, and costs nothing to maintain. A hand index at that size is pure overhead and goes stale within a week.
- **An index that is refreshed "later" is worse than no index**, because it is trusted. If it cannot be updated in the same turn, do not create it.
- **The index is derived data.** It can always be rebuilt from frontmatter, so it is never the only home for anything — no fact lives exclusively in the index.

## Monthly Sweep

Its `## Due` row is `Tag + orphan-link sweep`. Four passes, in order:

1. **Tag audit.** Any tag over the 10% threshold → promote. Any singleton → merge or delete. Record the merges in `artifacts/tag-taxonomy.md` so the same merge is not undone next quarter.
2. **Dead links.** Every `[[link]]` and relative path that resolves to nothing: fix, or remove and say what it pointed at. Renames done outside the app are the usual cause (`obsidian.md`).
3. **Orphans.** Notes with no inbound link and no tag. Either they get a tag or they were never worth keeping — decide, do not defer.
4. **Duplicates.** Two notes with near-identical titles: merge into the older file (its links are already established), leave a one-line pointer in the newer, then delete it.

Record the counts in the monthly rollup (`journal.md`): "23 notes, 2 tags merged, 4 dead links, 1 duplicate merged."

## Archiving

Governed by `archive_after_months` (default 12).

- **Archive by moving, never by deleting**: `journal/2025/`, `quick/archive/`. Search still reaches it; browsing does not trip over it.
- **Only journal and quick notes archive on age.** Decisions, research and project notes are ageless — a decision from 2021 is exactly the thing someone needs when the question returns.
- **The archive run updates `corpus` in `## Status`** and, if it exists, `index.md`. An archive that leaves the index pointing at moved files is the worst of both.

## When Nothing Is Found

In order, out loud:

1. Say what was searched — which platforms, which terms. A search that silently covered only local files produces a false "it does not exist".
2. Try the synonym set: the person's name, the project, the month, the counterpart's company.
3. Check the platforms that are *configured but not currently reachable* (app not running, key missing) and say they were skipped — this is the single most common false negative.
4. If it genuinely does not exist, say so and offer to create it. Never reconstruct a note from memory and present it as found.

## Retrieval Traps

| Trap | Why it fails | Do instead |
|---|---|---|
| Topic titles | Every search returns everything | Claim titles (SKILL.md Rule 2) |
| Finding a note by full text and moving on | The title stays wrong and the next search is just as slow | Rename in the same turn |
| A tag per idea | 300 tags equals no tags | 10% and singleton rules |
| Tags used as statuses | Never updated, so always wrong | Frontmatter or `actions.md` |
| Subject folders | A note has three subjects and one folder | Folder by type only |
| Linking every noun | A graph too dense to navigate | Link what will be followed |
| Wikilinks in a corpus that will be exported | They resolve nowhere outside the app | Relative paths for portability (`migration.md`) |
| Index from note one | Stale in a week and trusted anyway | Rule 7 |
| Deleting instead of archiving | The one search that needed it happens next year | Move, do not delete |
| Reporting "not found" after searching one platform | The note exists and the user stops trusting search | Say what was searched and what was skipped |

**Write triggers for this file** — in the same turn: a settled naming, tag or folder convention to `## Conventions` in `~/Clawic/data/notes/memory.md`; the index to `index.md` at 30 notes, with its `## Boxes` line; every rename, merge or archive reflected in `index.md` and in the `corpus` count in `## Status`; the sweep result to the monthly block in `reviews/<year>.md` and the date to the `Tag + orphan-link sweep` row in `## Due`; a taxonomy decision and its rejected alternative to `artifacts/tag-taxonomy.md`. Formats and thresholds: `memory-template.md`.
