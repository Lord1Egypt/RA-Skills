# Migration — Moving a Corpus Between Apps

Every note app is left eventually. What determines whether that costs an afternoon or a year is what the corpus was written in, not which app it is leaving.

**Contents:** [Decide Before Migrating](#decide-before-migrating) · [The Restore Test](#the-restore-test) · [Export Fidelity](#export-fidelity) · [What Breaks, and the Fix](#what-breaks-and-the-fix) · [Migration Procedure](#migration-procedure) · [Importing Into a Corpus](#importing-into-a-corpus) · [Staying Portable](#staying-portable) · [Migration Traps](#migration-traps)

**Before starting**, read `## Note Map` and `## Platform Facts` in `~/Clawic/data/notes/memory.md` and any prior `artifacts/migration-*.md`. A half-finished migration from last year is the most expensive thing to discover mid-run.

## Decide Before Migrating

Migration is justified by one of four things. "The new app looks nicer" is not one of them.

- **The current app cannot do something the work requires** (offline, sharing, a platform the user now lives on).
- **Lock-in risk has become concrete**: price change, account risk, a product direction that removes export.
- **Retrieval has failed structurally** and the fix is a different data model, not better titles.
- **The corpus must outlive the tool** — decisions, contracts, research.

Otherwise, migrating a corpus is a large, lossy operation whose only certain outcome is that some notes get worse.

Partial migration is usually the right answer: move the types that need the new app, leave the rest. The routing table (`config.yaml`) exists precisely so that different types can live in different places.

## The Restore Test

Never migrate a corpus on the strength of an export claim. Test one note first, end to end, and pick a hard one: nested lists, a table, an attachment, a wikilink, a checkbox, an accented character, and a code block.

1. Export that single note from the source.
2. Import it into the target.
3. Compare it to the original, field by field, including frontmatter.
4. Write what was lost into `artifacts/migration-<source>-to-<target>.md`.

Whatever broke on one note breaks on all of them, silently, at scale. This test costs ten minutes and is the difference between a migration and a data-loss event.

## Export Fidelity

Roughly ordered by how much survives. Verify against the current app version — export formats change and this is a snapshot, not a guarantee.

| Source | Export gives you | Typically survives | Typically lost |
|---|---|---|---|
| Local markdown | The files themselves | Everything | Nothing |
| Obsidian | The vault, already plain markdown | Text, frontmatter, attachments, folder tree | Plugin-specific syntax (dataview queries, callout variants), graph state |
| Bear | Markdown or textbundle per note | Text, tags as `#tag` lines, attachments in textbundle | Nested-tag hierarchy as folders, note ids, encrypted notes |
| Notion | Markdown + CSV zip, or HTML | Page text, top-level structure, files | Database views and filters, relations and rollups (flattened to text), comments, nested databases, backlinks |
| Apple Notes | Per-note export via the app; no bulk plain-text export | Text and attachments, one note at a time | Bulk anything, folder structure, tags, checklists as markdown |
| Evernote | ENEX (XML) or HTML | Text, attachments, notebook names, created/updated dates | Markdown structure, checkboxes as markdown, reminders, some tables |

Two structural rules follow from that table:

- **Anything modelled as a database rather than a document flattens.** Notion relations, rollups and views are the classic loss: they exist in the app, not in the export.
- **Attachments are the failure point.** Most exporters rewrite attachment paths; check that a note's image still resolves after import, on one note, before running the rest.

## What Breaks, and the Fix

| Breakage | Cause | Fix |
|---|---|---|
| `[[wikilinks]]` resolve to nothing | Target does not implement them, or filenames changed | Convert to relative markdown links during the migration, in one pass |
| Every note has the same import date | Exporter drops created/updated timestamps | Write the real date into frontmatter `date:` before import; the filesystem date is now fiction |
| Tags disappear | Target uses folders, or a different tag syntax | Map tags to frontmatter `tags:` — the portable form that survives every subsequent move |
| Checkboxes become plain text | HTML or ENEX round-trip | Regex pass to restore `- [ ]` / `- [x]` |
| Accented characters or emoji mangled | Encoding assumed non-UTF-8 | Force UTF-8 on export and import; verify on the test note |
| Filenames truncated or illegal | Target OS or app restricts length and characters | Slugify before import: lowercase, hyphens, ≤60 characters |
| Two notes with the same title collide | Source allowed duplicate titles | Append the date to the slug, never a numeric suffix — `2026-07-26_pricing` beats `pricing-2` |
| Nested tags flatten | Target supports one level | Decide before import: `product/pricing` → `product-pricing`, or promote the root to a folder |
| Action items lost in the noise | They were only in note bodies | Extract to `actions.md` before migrating, not after (`action-items.md`) |

## Migration Procedure

1. **Freeze writes to the source**, and say so. Notes created mid-migration are the ones that go missing.
2. **Export everything**, keep the untouched export archive as the rollback, and never edit it in place.
3. **Run the restore test** on one hard note. Fix the pipeline before the bulk run.
4. **Transform**: filenames, frontmatter, links, tags, dates. One pass per transformation, so each can be verified.
5. **Import**, then **count**. Source note count versus target note count, stated out loud. A migration that does not end with a count did not verify anything.
6. **Spot-check ten notes** across types: oldest, newest, longest, one with an attachment, one with a table, one with links.
7. **Keep the source read-only for one full review cycle** (a month). Deleting the old app the same week is how the gap is discovered too late.
8. **Update routing** in `config.yaml` and `## Note Map`, and record the fidelity findings in the artifact.

## Importing Into a Corpus

Bringing someone else's notes, an old export, or a second vault into an existing corpus:

- **Import into a quarantine folder first** (`import-<source>/`), never straight into the type folders. An import that mixes with the live corpus cannot be undone.
- **Deduplicate against what exists** on title plus date before promoting anything. Re-importing an export that was already imported is the most common corpus corruption.
- **Retitle to the claim convention as they are promoted** (SKILL.md Rule 2). Imported notes carry the old naming, and a corpus with two naming schemes searches like two corpora.
- **Promote in batches by type**, and update `corpus` in `## Status` after each. An import of 400 notes that lands all at once makes the index and the tag thresholds meaningless overnight.

## Staying Portable

The cheapest migration is the one prepared for in advance:

- **Plain markdown files with frontmatter** are the only format every target accepts without loss.
- **Metadata in frontmatter, not in app features.** A tag in `tags:` survives every move; a tag in the app's tag system survives some.
- **Relative links over wikilinks** for anything expected to outlive the current app (`retrieval.md`).
- **No app-specific syntax in notes that matter.** A decision written with plugin-rendered callouts is a decision that reads as noise in five years.
- **Quarterly export of anything held in a network platform**, verified by opening one file. Its `## Due` row sits next to the backup restore test (`sync.md`).

## Migration Traps

| Trap | Why it fails | Do instead |
|---|---|---|
| Trusting the export claim | "Exports to markdown" hides which fields do not | Restore test on one hard note |
| Migrating without counting | Missing notes are discovered a year later, if ever | Count source versus target, out loud |
| Deleting the source immediately | The gap surfaces after the account closes | Read-only for a full review cycle |
| Editing the export archive in place | The rollback is gone | Transform copies only |
| Importing straight into live folders | Cannot be undone, and duplicates merge into the corpus | Quarantine folder, then promote |
| Numeric suffixes for title collisions | `pricing-2` tells nobody anything | Date in the slug |
| Keeping wikilinks in a corpus that just moved | Every link is dead and nothing reports it | Convert links in one pass |
| Leaving imported notes with old titles | Two naming schemes, so search works half the time | Retitle on promotion |
| Migrating the app but not the actions | Commitments were in note bodies and are now unreachable | Extract to `actions.md` first |

**Write triggers for this file** — in the same turn: the plan, the fidelity findings, the counts and the spot-check result to `~/Clawic/data/notes/artifacts/migration-<source>-to-<target>.md` with its `## Boxes` line; new routing to `config.yaml` and `## Note Map`; new vault paths, database ids and folder maps to `## Platform Facts`; the updated note count to `corpus` in `## Status`; the quarterly export cadence to the `## Due` table; every commitment extracted during the migration to `actions.md`. Formats and thresholds: `memory-template.md`.
