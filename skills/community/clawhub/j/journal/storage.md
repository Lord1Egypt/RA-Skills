# Storage — Files, Tags, Search, Encryption, Backup, Migration

Scope: the corpus as files on a disk. A journal is the one archive that cannot be reconstructed from anywhere else, which changes every trade-off below.

**Contents:** [Naming And Layout](#naming-and-layout) · [Frontmatter](#frontmatter) · [Tag Hygiene](#tag-hygiene) · [Search](#search) · [Encryption](#encryption) · [Backup](#backup) · [Sync Conflicts](#sync-conflicts) · [Migrating Out Of An App](#migrating-out-of-an-app) · [Changing The Layout Later](#changing-the-layout-later)

**Before changing anything structural**, read `## Boxes` in `~/Clawic/data/journal/memory.md` and `entries_path`, `entry_naming` in `config.yaml`. A layout change that half-runs leaves a corpus that neither scheme can search.

## Naming And Layout

```
<entries_path>/
├── 2025/
│   └── 2025-11-03.md
└── 2026/
    ├── 2026-07-25.md
    ├── 2026-07-26.md
    └── 2026-07-26-page1.jpg
```

- **`YYYY-MM-DD` filenames, always.** Sorts chronologically in every tool, parses in every language, and never becomes ambiguous between locales. A title in the filename ("bad-day.md") is unsortable and unfindable.
- **One folder per year** (default `YYYY/YYYY-MM-DD`). A flat folder is fine to about 500 files and then every listing operation becomes unpleasant; a month level (`YYYY/MM/`) is only worth it above roughly ten entries a day.
- **One file per day** (Rule 5). Multiple entries append `## HH:MM`. Per-entry files break "what did I write on the 3rd" and multiply the sync-conflict surface.
- **Attachments share the date prefix**: `2026-07-26-page1.jpg`, next to the entry, referenced by filename. Never a separate media folder — the pairing is what survives a move.
- **Plain markdown, plain UTF-8, no proprietary container.** The format's job is to be readable in thirty years by something that does not exist yet.
- Reviews, decisions, work logs, and artifacts live outside `entries/`, in their own boxes (`memory-template.md`), because they have different reread policies and different retention.

## Frontmatter

Optional, and stays optional. Add it when the user asks for tags or ratings, never pre-emptively.

```yaml
---
date: 2026-07-26
tags: [work, sleep]
mood: 3          # scale from config.yaml; the series lives in ~/Clawic/data/health/mood.md
practice: morning-pages
audio: 2026-07-26-note.m4a
---
```

- **`practice` is the field that earns its keep**: it is what lets `patterns.md` exclude never-reread material from analysis. Without it, exclusion means reading the entries to decide, which defeats the purpose.
- `mood` is duplicated deliberately — the entry keeps it for context, the shared health series keeps it for analysis. The shared series wins on conflict.
- Never add a field retroactively to old entries. A field that exists for 2026 and not 2025 is honest; a backfilled guess is invented data.
- No location, weather, or device fields unless the user asks. Each one is a metadata trail on a private document.

## Tag Hygiene

Tags are an index, and an index with forty terms used once each is worse than no index.

- **Ceiling of ~12 active tags.** Past that, retrieval by tag stops working because nobody remembers which tag they used.
- **Retire**: a tag with **<3 uses after 3 months** is deleted from the entries that carry it and from the vocabulary. It was a thought, not a category.
- **Merge**: two tags co-occurring on **>70% of the entries that carry either** are one tag. Keep the user's more natural word, rewrite the other.
- **Tag the recurring, not the interesting.** A tag exists to answer "show me all the X entries" later. If that question will never be asked, no tag.
- Store the active vocabulary in `## Themes` in `memory.md`, so tagging is consistent across sessions and `patterns.md` counts the same clusters every month.
- Tags are not a mood scale, a rating, or a to-do state. Those are fields.

## Search

Plain files mean the corpus is searchable with ordinary text tools, which is most of the reason to keep it in plain files.

```bash
# every entry mentioning a word, filenames only (dates)
grep -ril "interview" ~/Clawic/data/journal/entries/

# a date range: March 2025
grep -ril "interview" ~/Clawic/data/journal/entries/2025/2025-03-*.md

# by tag, when frontmatter is in use
grep -rl "tags:.*work" ~/Clawic/data/journal/entries/

# with two lines of context, newest first
grep -ri -A2 "the move" ~/Clawic/data/journal/entries/ | sort -r
```

- `grep -i` for case, `-r` for recursion, `-l` for filenames only — dates *are* the result for most journal questions.
- Windows without a POSIX shell: the same queries in PowerShell via `Select-String -Path ... -Pattern ...`.
- **Searching is reading.** Everything found is subject to `agent_read_scope`, `## Read Scope`, and `no_go_file` (`privacy.md`); a grep hit inside an excluded entry is not reportable.
- Accents, curly quotes, and dashes vary by input method — search a stem without the accented character (`Zur`, not `Zurich` spelled with an umlaut) when a match seems impossibly absent.

## Encryption

Honest trade-offs; there is no free option.

| Approach | Protects against | Costs |
|---|---|---|
| Full-disk encryption (FileVault, BitLocker, LUKS) | A lost or stolen device | Nothing, and it is already available. **The default, and enough for most people** |
| Encrypted container or volume for the journal folder | Another user of the same logged-in machine | Must be mounted to write; an unmounted container means a missed entry |
| Per-file encryption (age, gpg) | Backup providers and sync services reading the content | Kills grep, kills every review and analysis, and one lost passphrase destroys the corpus permanently |
| Nothing | — | Any process, backup, or person with file access reads everything |

- **Full-disk encryption plus honest folder placement covers the realistic threat model.** Per-file encryption is usually the wrong trade for a journal, because the analysis and the reread are the whole value.
- **Never store the passphrase** anywhere under `~/Clawic/data/` — not in config, not in memory, not in an entry. Pointer only: `keychain:journal-vault`, `1password:Personal/Journal`.
- The threat that per-file encryption actually addresses is a cloud sync provider. Compare it against simply not syncing the journal folder, which is cheaper and loses nothing but convenience.
- If the device is shared with someone the entries are about, encryption is a partial answer at best — see the abuse row in SKILL.md Red Flags and `privacy.md`.

## Backup

The journal is unrecoverable if lost: unlike code, notes, or photos, there is no second source it can be rebuilt from.

- **Versioned, not mirrored.** A backup that only holds the current state cannot undo an accidental overwrite or a bad bulk rename, which are the two ways journals are actually lost.
- **A sync folder is not a backup** (Traps). Deletions and corruption propagate to every device in seconds, and that is sync working correctly.
- **Three copies, two media, one off-site** — the standard shape, and for a folder of text files it costs almost nothing.
- **Restore, do not assume.** Once a quarter, restore three random entries from different years into a scratch folder and compare them byte for byte. An untested backup is a hypothesis. Put it in `## Due`.
- Back up the whole `~/Clawic/data/journal/` folder, not just `entries/`: reviews, decisions, work log, and artifacts are equally unrecoverable.
- If the backup destination is a cloud provider, that is a copy of the journal in someone else's custody — a deliberate decision, worth stating once, and the case for an encrypted archive at the backup boundary rather than per-file encryption at rest.

## Sync Conflicts

Two devices writing the same day file is the normal collision, not an edge case.

- Symptom: `2026-07-26 (conflicted copy).md`, `2026-07-26.sync-conflict-....md`, or a merged file with duplicated paragraphs and no warning.
- **Resolve by concatenation, never by choosing a side.** Both halves are real writing that someone did. Merge under two `## HH:MM` headings in time order and delete the conflict file only after the merge is saved.
- Prevention that works: one device is the journaling device; the others read. Prevention that does not work: remembering to close the app.
- Never let an automatic conflict resolver pick a winner on this folder. Exclude the journal from any tool with that behaviour.

## Migrating Out Of An App

| Source | Export | Survives | Usually lost |
|---|---|---|---|
| Day One | JSON or plain text with a media folder | Text, dates, tags, most metadata | Rich formatting, some per-entry metadata, media links unless rewritten |
| Obsidian / Logseq / any markdown vault | Already files | Everything | Nothing — this is a copy, not a migration |
| Notion | Markdown + CSV with an attachments folder | Text, page titles, attachments | Databases become CSV, links become long file paths, timestamps degrade |
| Apple Notes | No bulk export; per-note export or a scripted pass | Text | Formatting, attachment fidelity, creation timestamps |
| Google Docs / Word | Per-document export | Text | Comments, revision history, dates unless in the body |
| Paper notebooks | Photograph and transcribe (`capture.md`) | What you transcribe | The rest, permanently — do the oldest first |

Procedure, in order, and do not shorten it:

1. Export to the most open format offered, even if it is uglier.
2. Convert to `YYYY-MM-DD.md` files. **The entry date comes from the content's date, not the file's creation time** — an export sets every file's ctime to today, and that mistake is unrecoverable once the source is gone.
3. **Round-trip check on three random entries** from different years: text intact, non-ASCII characters intact, date correct, attachments present and referenced.
4. Only then archive the source export. **Never delete the original app's data until the round-trip passes**, and keep the raw export file indefinitely — it costs a few megabytes and it is the only fallback.
5. Record the migration date and what was lost in `## Practice` of `memory.md`. Six months later, nobody remembers whether the 2019 gap is a migration artifact or a year of not writing.

## Changing The Layout Later

- A rename of every file is a single operation and must run to completion. Half-renamed corpora fail every search with no error.
- Copy first, verify the new tree's file count and total byte size against the old, and only then remove the original.
- **Changing `entry_naming` never applies to only new entries.** A mixed corpus is worse than either scheme.
- Update `entries_path` in `config.yaml` in the same turn as the move, or the next entry lands in the abandoned tree.

**Write in the same turn:** the active tag vocabulary and merges or retirements, to `## Themes` in `memory.md`; a layout, path, or naming change, to `config.yaml` plus a dated line in `## Practice`; a migration with its date and what was lost, to `## Practice`; backup-restore drills and tag pruning, to `## Due`; an encryption or backup passphrase, nowhere — pointer only. Formats: `memory-template.md`.
