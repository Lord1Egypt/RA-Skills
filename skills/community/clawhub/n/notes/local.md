# Local Markdown

The default, and the only platform with no dependency, no account, and no export problem. Everything is a file in `~/Clawic/data/notes/`.

**Contents:** [Layout](#layout) · [Frontmatter](#frontmatter) · [Searching](#searching) · [Renaming Safely](#renaming-safely) · [Attachments](#attachments) · [Editors and Mobile](#editors-and-mobile) · [Local Traps](#local-traps)

**Before writing**, read `## Conventions` in `~/Clawic/data/notes/memory.md`: the filename pattern and the frontmatter field set are already decided, and a note that departs from them is a note the greps will miss.

## Layout

```
~/Clawic/data/notes/
├── config.yaml        # declared preferences
├── memory.md          # corpus state, box index, due dates
├── actions.md         # the one tracker
├── index.md           # created at 30 notes
├── meetings/          # YYYY-MM-DD_topic-slug.md
├── decisions/         # YYYY-MM-DD_topic-slug.md
├── projects/          # YYYY-MM-DD_project-status.md
├── journal/           # YYYY-MM-DD.md   (older years in journal/<year>/)
├── research/          # source-slug.md
├── quick/             # YYYY-MM-DD_HH-MM_topic.md
├── reviews/           # <year>.md
├── templates/         # only the types the user reshaped
└── artifacts/         # long texts read whole
```

Every folder is created with its first file, never in advance. Naming rules and the reasoning behind them: `retrieval.md`.

## Frontmatter

Frontmatter is what makes a plain-file corpus queryable without an index, and it is the metadata that survives every future migration (`migration.md`). Minimum set:

```yaml
---
date: 2026-07-26          # ISO always; the filesystem date lies after any copy, sync, or restore
type: meeting             # one of the nine types
title: "Pricing: staying at three tiers"    # the claim (SKILL.md Rule 2)
tags: [product, pricing]  # the portable form of a tag
---
```

Optional by type: `attendees`, `absent`, `project`, `source`, `status`, `supersedes`, `platform`, `review`.

- **Quote any title containing a colon.** `title: Pricing: three tiers` is invalid YAML and silently breaks every frontmatter grep — and claim titles contain colons constantly.
- **Dates unquoted and ISO** (`2026-07-26`), so they sort and parse.
- **Lists in flow style** (`[a, b]`): one line per field greps cleanly, a block list does not.

## Searching

Search order, and the rename that follows a full-text-only hit: `retrieval.md`.

```bash
# titles and filenames
ls ~/Clawic/data/notes/meetings/ | grep -i pricing
grep -ri '^title:.*pricing' ~/Clawic/data/notes/

# by tag, by person, by project
grep -rl '^tags:.*pricing' ~/Clawic/data/notes/
grep -rl '^attendees:.*alice' ~/Clawic/data/notes/
grep -rl '^project: atlas' ~/Clawic/data/notes/

# full text with context
grep -ri --include='*.md' -n -C2 'three tiers' ~/Clawic/data/notes/

# a date range
ls ~/Clawic/data/notes/*/2026-07-*.md
```

`rg` is faster on large corpora; `grep` exists everywhere. Use whichever is installed rather than asking.

## Renaming Safely

Plain files have no link index, so a rename is two steps in one turn:

1. Find inbound links first: `grep -rl 'old-slug' ~/Clawic/data/notes/`.
2. Move the file, then update every hit.

Skipping step 2 leaves dead links that surface only at the monthly sweep (`retrieval.md`). Prefer relative markdown links (`../decisions/2026-07-14_pricing-tiers.md`) over wikilinks here: they resolve in any editor, on a phone, and after a migration.

## Attachments

- **Next to the note, in `<type>/attachments/`**, linked relatively — copying the folder elsewhere still works.
- **Name the attachment after its content**, never `IMG_4821.png`: the filename is the only searchable part of a binary.
- **Keep binaries out of a git-versioned corpus**; history grows permanently and cannot be shrunk cheaply (`sync.md`).

## Editors and Mobile

- **Any editor works**, which is the point: the corpus must never depend on one.
- **Mobile capture is the real gap.** Options by friction: a synced folder plus any markdown editor; a native app used only for `quick/` and folded into local weekly (`capture.md`); or dictation into the agent. Whichever is chosen is recorded in `## Note Map`.
- **A file left open in an editor on one device while another edits it** is the standard conflict recipe (`sync.md`).

## Local Traps

| Trap | Why it fails | Do instead |
|---|---|---|
| Unquoted colon in a title | Invalid YAML; every frontmatter grep silently misses the note | Quote titles containing colons |
| Trusting the filesystem date | Copy, sync, or restore rewrites it | `date:` in frontmatter |
| Renaming without checking inbound links | Dead links found a month later, cause forgotten | Grep, move, update, same turn |
| Wikilinks in plain files | Resolve nowhere outside a wikilink-aware app | Relative markdown links |
| Spaces and accents in filenames | Break shell pipelines and some sync clients | Lowercase, hyphens, ASCII slug |
| A folder per subject | A note has three subjects and one folder | Folder by type (`retrieval.md`) |
| One global attachments folder | The note and its image drift apart on any move | `<type>/attachments/` |

**Write triggers for this file** — in the same turn: the note to its type folder with complete frontmatter; any filename or frontmatter convention that got settled to `## Conventions` in `~/Clawic/data/notes/memory.md`; the updated `corpus` count in `## Status` after a create or an archive; new entries in `index.md` if it exists. Formats and thresholds: `memory-template.md`.
