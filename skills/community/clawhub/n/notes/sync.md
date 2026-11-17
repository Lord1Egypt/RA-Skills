# Sync, Conflicts, and Backups

A note corpus is a distributed system with no conflict resolution and no error messages. Losing a paragraph is silent; noticing three weeks later is normal. This file covers multi-device editing, conflicted copies, backup, and restore.

**Contents:** [How Notes Actually Get Lost](#how-notes-actually-get-lost) · [Conflicted Copies](#conflicted-copies) · [Merging a Conflict](#merging-a-conflict) · [Preventing Conflicts](#preventing-conflicts) · [Sync Mechanisms Compared](#sync-mechanisms-compared) · [Git for a Vault](#git-for-a-vault) · [Backup and Restore](#backup-and-restore) · [Encryption at Rest](#encryption-at-rest) · [Sync Traps](#sync-traps)

**Before diagnosing**, read `## Platform Facts` in `~/Clawic/data/notes/memory.md`: which sync mechanism is in use, where the vault lives, and any conflict already resolved. Half of all "sync bugs" are the same known interaction re-diagnosed from scratch.

## How Notes Actually Get Lost

Four mechanisms, in order of how often they bite:

1. **Two devices, one offline.** Both edit the same file; the sync layer picks a winner by modification time and either discards the loser or leaves a copy nobody opens.
2. **Edit while the sync is mid-write.** Opening a file that is still downloading, editing it, and saving replaces the incoming version with a stale one.
3. **Rename outside the app.** Links break, and in link-heavy vaults the note is effectively gone (`obsidian.md`).
4. **Delete propagated everywhere.** Deleting on one device deletes on all of them, including from the backup if the backup is just another sync target.

Note the shape: none of these produce an error. The first sign is a missing paragraph.

## Conflicted Copies

Every sync layer marks conflicts differently. Search for all of these before concluding nothing was lost:

| Layer | Marker |
|---|---|
| Dropbox | `note (Alice's conflicted copy 2026-07-26).md` |
| iCloud Drive | A second file with the device name appended, or a Finder conflict prompt |
| Syncthing | `note.sync-conflict-20260726-141233-XXXXXXX.md` |
| Obsidian Sync | Version history in the app; no second file on disk |
| Git | Conflict markers inside the file: `<<<<<<<`, `=======`, `>>>>>>>` |
| Bear / Apple Notes | The app keeps both as separate notes, usually with identical titles |

**A conflicted copy is a rescue, not garbage.** Deleting them to tidy the folder is the most common way people lose the version they wanted.

## Merging a Conflict

Never resolve by keeping one whole file. The two versions almost always contain different additions, and whole-file resolution throws one of them away.

1. **Diff them.** Section by section. The overlap is identical; the differences are localized, usually to one or two blocks.
2. **Merge by section, into the file with the canonical name.** Additions from both sides survive; a genuine contradiction (two different due dates on the same action) is kept as both with a marker, and asked about — never silently resolved.
3. **Delete the conflicted copy only after the merge is saved**, and say which file was merged and what came from where.
4. **Record the cause** in `## Platform Facts`: which two devices, which sync layer. The same pair produces the same conflict again.

Special case, append-only files (`actions.md`, `reviews/<year>.md`): merging is a union of rows, deduplicated on the identity key (`Task` + `Owner` for actions). These files conflict most often, because both devices append.

## Preventing Conflicts

- **One writer at a time.** Close the note on device A before editing on device B. This is the only rule that actually eliminates the problem.
- **Wait for sync to settle after opening a device that was offline.** Most conflicts are created in the first 30 seconds after a laptop wakes.
- **Prefer many small files to one large one.** A per-day journal file conflicts far less than a single running journal, because the write windows rarely overlap. Same reason quick captures are one file each (`capture.md`).
- **Never edit a file in the sync folder while a bulk operation is running** (an archive run, a tag merge, a migration): every touched file becomes a conflict candidate at once.

## Sync Mechanisms Compared

| Mechanism | Conflict behaviour | Cost | Fit |
|---|---|---|---|
| iCloud Drive | Silent last-writer-wins with an occasional conflict prompt | Free on Apple platforms | Apple-only users who accept the risk |
| Dropbox | Creates a conflicted copy reliably | Paid past the free tier | The most predictable of the consumer options |
| Syncthing | Creates a marked conflict file; peer-to-peer, no third party | Free, requires setup on every device | Users who will not put notes on someone else's server |
| Obsidian Sync | Per-file version history in-app, end-to-end encrypted | Subscription | Obsidian users who want the merge UI |
| Git | Explicit conflicts you must resolve; full history | Free, requires git literacy and a manual or scripted commit | Text-only corpora and anyone comfortable with a diff |
| App-native (Bear, Apple Notes, Notion) | Handled server-side; duplicates instead of merges | Included | Users who never touch the files directly |

Default: whatever the user already runs. Changing sync mechanisms is a migration (`migration.md`) and is worth it only after a real loss.

## Git for a Vault

Version history is the only mechanism that answers "what did this note say last month".

- **Commit on a schedule, not on every save** — one commit a day is enough to recover anything, and per-save commits make the log unreadable.
- **Ignore the app's workspace state**: `.obsidian/workspace.json` and its equivalents churn on every window move and produce a conflict on every device.
- **Binary attachments bloat history permanently.** Keep images out of the repository, or accept that the clone grows without bound — history cannot be shrunk without rewriting it.
- **Git is not a backup while the only copy of the repository is on the machine being backed up.** A remote, or it does not count.
- A vault under both git and a sync layer will conflict on `.git` internals. Pick one to own the transport.

## Backup and Restore

3-2-1: three copies, on two kinds of media, one off-site. A sync folder is *one* copy — it propagates deletions, so it is not a second one.

| Layer | Covers | Does not cover |
|---|---|---|
| Sync | Device loss | Deletion, corruption, a bad bulk edit |
| Versioned backup (Time Machine, snapshots, git) | Deletion and bad edits, within its retention | Losing the machine and the backup together |
| Off-site copy | Fire, theft, account lockout | Anything you never verified you could restore |

- **A backup that has never been restored is a hypothesis.** Restore one note and one folder to a scratch location every quarter — its `## Due` row is `Backup restore test` — and record how long it took and what was missing.
- **Export before you need it.** Platforms lock accounts and change terms; a quarterly export of anything held in a network platform is the only defence (`migration.md`).
- **Check what the backup actually contains.** A Notion export of "everything" excludes comments and some database views; an Apple Notes backup via iCloud is not a file you can read without the app.

## Encryption at Rest

- **Full-disk encryption covers the laptop threat** (loss, theft) and is the correct default. It does nothing against an account compromise on a synced platform.
- **Per-note encryption** (Bear's lock, encrypted markdown) protects individual notes but breaks search, which usually means the feature stops being used. Reserve it for the few notes that need it, and expect them to be unfindable.
- **The safest option for the most sensitive material is not writing it down** (`sensitive.md`).
- Never encrypt a note with a key that exists only in the corpus being encrypted. The pointer goes in the note (`keychain:vault-key`), the key lives in the OS keychain or the user's password manager.

## Sync Traps

| Trap | Why it fails | Do instead |
|---|---|---|
| Deleting conflicted copies to tidy up | They are the only copy of the lost edits | Merge, then delete |
| Resolving a conflict by keeping the newer file | Discards everything the older side added | Merge by section |
| Editing on a device that just came online | Overwrites the version still downloading | Let sync settle first |
| One giant running note | Conflicts on nearly every multi-device day | One file per day, capture, or update |
| Sync counted as a backup | Deletions and bad edits propagate in seconds | 3-2-1, with versions |
| A backup never restored | Fails on the details nobody wrote down | Quarterly restore test |
| Committing `.obsidian/workspace.json` | Conflicts on every device, every session | Ignore it |
| Images in the git repository | History grows permanently and cannot be shrunk cheaply | Attachments outside the repo |
| Per-note encryption everywhere | Breaks search; the notes become unfindable and unused | Only where it is required |

**Write triggers for this file** — in the same turn: the sync mechanism, device pair, vault path and any resolved conflict to `## Platform Facts` in `~/Clawic/data/notes/memory.md`; the restore test date and its measured duration to the `Backup restore test` row in `## Due`; anything missing from the restore to `artifacts/backup-restore-gaps.md` with its `## Boxes` line; a bulk merge or repair to `artifacts/<kebab-name>.md` recording how many files were touched. Formats and thresholds: `memory-template.md`.
