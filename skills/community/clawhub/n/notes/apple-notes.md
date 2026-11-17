# Apple Notes

Best-in-class capture on Apple devices, worst-in-class automation. Driven through the `memo` CLI, which talks to Notes.app; there is no public API for note content.

**Contents:** [Requirements](#requirements) · [Operations](#operations) · [Writing a Formatted Note](#writing-a-formatted-note) · [Folders](#folders) · [What It Cannot Do](#what-it-cannot-do) · [Fallback](#fallback) · [Apple Notes Traps](#apple-notes-traps)

**Before routing anything here**, read `## Platform Facts` in `~/Clawic/data/notes/memory.md` for the folder names that already exist. Creating a second folder that differs by a capital letter splits the corpus in a place with no search across folders.

## Requirements

macOS, Notes.app, and the user's own installation of the `memo` CLI (`brew tap antoniorodr/memo && brew install antoniorodr/memo/memo`). Nothing is installed on the user's behalf; if the CLI is absent, fall back and say so.

First run prompts for Automation access to Notes.app (System Settings → Privacy & Security → Automation). Denying it makes every command fail with a permissions error rather than a missing-binary error — check the prompt before debugging anything else.

## Operations

```bash
memo notes                      # list all
memo notes -f "Work"            # list one folder
memo notes -s "keyword"         # fuzzy search
memo notes -a "Note Title"      # create (opens the editor)
memo notes -e                   # edit, interactive selection
memo notes -m                   # move between folders, interactive
memo notes -d                   # delete, interactive
memo notes -ex                  # export to HTML/markdown
```

Interactive selection means these cannot be chained without a terminal a human is watching. Anything scripted is limited to list, search, and create.

## Writing a Formatted Note

`memo notes -a` opens an editor rather than accepting content on stdin, so the content is prepared first and pasted:

```bash
cat > /tmp/note.md << 'EOF'
# Pricing: staying at three tiers — 2026-07-26

**Present:** Alice, Bob

## Decisions
- Three tiers stay; revisit at 500 customers — @alice, effective 2026-07-26

## Actions
- [ ] @alice: send the pricing deck — 2026-08-04
EOF
pbcopy < /tmp/note.md
memo notes -a "2026-07-26 Pricing three tiers"
```

- **Delete the temp file after pasting.** `/tmp` is world-readable on a shared machine, and a meeting note left there outlives the session.
- **Put the date in the title**, because Apple Notes sorts by modification and shows no filename. Without it, the note is dated by whenever it was last touched.
- Markdown is rendered on paste for headings and lists; tables are not supported and arrive as plain text. Keep tables out of notes routed here — use bullets with a date suffix instead.

## Folders

One folder per note type, matching the local layout so a note keeps its identity when routing changes:

| Type | Folder |
|---|---|
| meeting, 1-on-1, interview, retro | Meetings |
| decision | Decisions |
| project update | Projects |
| journal | Journal |
| quick | Quick Notes |

Folders are created by the user in Notes.app; the CLI does not create them. Verify the exact spelling with `memo notes -f "<name>"` before the first write and record it in `## Platform Facts`.

## What It Cannot Do

| Limit | Consequence |
|---|---|
| No bulk plain-text export | Migration is note by note through the app (`migration.md`) |
| Notes with images or attachments cannot be edited by the CLI | Any note the user illustrates becomes read-only to automation |
| No tags reachable from the CLI | Retrieval here is by folder and full-text search only |
| Interactive prompts for edit, move, delete | Nothing destructive can be scripted, which is a feature |
| No stable note id exposed | Links into a note are not reliable; `Source` pointers use `apple-notes:<Title>` |
| No table rendering | Structured content degrades to plain text |

Everything above pushes the same conclusion: Apple Notes is a **capture** platform. Route `quick` here and fold captures into local at triage (`capture.md`); route anything that must be found in three years to local or Obsidian.

## Fallback

If `memo` is missing, Notes.app is not installed, or Automation access is denied: write locally, stamp the note `platform: local (fallback from apple-notes)`, and say it in one line (SKILL.md Rule 1). Never leave the user believing a note reached an app it never reached.

## Apple Notes Traps

| Trap | Why it fails | Do instead |
|---|---|---|
| Assuming a missing note means a CLI bug | Automation permission was denied; the error looks unrelated | Check Privacy & Security → Automation first |
| Two folders differing by case | Notes are split with no cross-folder view | Verify the exact name before the first write |
| Leaving the note in `/tmp` | Readable by anyone on the machine, and it survives the session | Delete after pasting |
| Titles without a date | Sorted by modification, so a reread reorders the corpus | Date in the title |
| Routing decisions or research here | No export path, no tags, no stable links | Local or Obsidian for anything durable |
| Building a table in a note routed here | Renders as unaligned plain text | Bullets with the date inline |

**Write triggers for this file** — in the same turn: folder names, the CLI's presence, and any Automation-permission fact to `## Platform Facts` in `~/Clawic/data/notes/memory.md`; the routing choice to `config.yaml` and `## Note Map`; every action item found in an Apple Note to `actions.md` with `Source: apple-notes:<Title>`; a fallback that stuck to `## Note Map`. Formats and thresholds: `memory-template.md`.
