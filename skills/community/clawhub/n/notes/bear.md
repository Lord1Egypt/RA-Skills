# Bear

Fast markdown capture with a nested tag tree, driven through the `grizzly` CLI, which speaks Bear's x-callback-url interface. Apple platforms only, and the app must be running.

**Contents:** [Requirements](#requirements) · [The Token](#the-token) · [Operations](#operations) · [Flags That Matter](#flags-that-matter) · [Tag Tree](#tag-tree) · [Append-Only Reality](#append-only-reality) · [Fallback](#fallback) · [Bear Traps](#bear-traps)

**Before writing**, read `## Platform Facts` in `~/Clawic/data/notes/memory.md` for the tag roots already in use. Bear's tag tree is the whole retrieval model here; a new near-synonym root (`#meeting` beside `#meetings`) silently halves every future search.

## Requirements

macOS or iOS with Bear installed and **running**, plus the user's own installation of the `grizzly` CLI (`go install github.com/tylerwince/grizzly/cmd/grizzly@latest`). Nothing is installed on the user's behalf.

Bear not running is the most common failure: the callback never returns and the command times out rather than erroring clearly. Check that first.

## The Token

Some operations — `add-text`, `tags`, `open-note --selected` — require Bear's API token (Bear → Help → API Token). The user stores it themselves; the skill only references it.

- **The token is a secret**: it never enters `~/Clawic/data/`. Record the pointer instead — `keychain:bear-token` or `file:~/.config/grizzly/token` — in `## Platform Facts` (`memory-template.md`).
- Optional CLI config at `~/.config/grizzly/config.toml`:

```toml
token_file = "~/.config/grizzly/token"
callback_url = "http://127.0.0.1:42123/success"
timeout = "5s"
```

- The callback URL binds a local port. If a command hangs with Bear running, that port is taken — change it in the config before assuming the CLI is broken.

## Operations

```bash
# create, content on stdin
cat << 'EOF' | grizzly create --title "Pricing: three tiers stay" --tag meetings --tag product/pricing
# Pricing: staying at three tiers — 2026-07-26

## Decisions
- Three tiers stay; revisit at 500 customers — @alice

## Actions
- [ ] @alice: send the pricing deck — 2026-08-04
EOF

# empty note with tags
grizzly create --title "Inbox capture" --tag inbox < /dev/null

# read a note by id
grizzly open-note --id "NOTE_ID" --enable-callback --json

# append (token required) — the only way to change an existing note
echo "Follow-up: deck sent 2026-08-01" | grizzly add-text --id "NOTE_ID" --mode append --token-file ~/.config/grizzly/token

# list tags, search by tag
grizzly tags --enable-callback --json --token-file ~/.config/grizzly/token
grizzly open-tag --name "product/pricing" --enable-callback --json
```

## Flags That Matter

| Flag | Purpose |
|---|---|
| `--enable-callback` | Wait for Bear's response — required for anything that reads, otherwise the command returns before data arrives |
| `--json` | Machine-readable output; without it the response has to be parsed from text |
| `--dry-run` | Build the URL without executing — the safe way to check a destructive or unfamiliar call |
| `--print-url` | Show the x-callback-url, which is how you debug an encoding problem |
| `--token-file PATH` | Points at the token; never pass the token inline, it lands in shell history |

## Tag Tree

Bear has no folders: tags are the structure, and nested tags render as a tree.

| Type | Tags |
|---|---|
| meeting, 1-on-1, interview, retro | `#meetings`, plus `#meetings/YYYY-MM` |
| decision | `#decisions` |
| project update | `#projects`, plus `#projects/<name>` |
| journal | `#journal`, plus `#journal/YYYY-MM` |
| research | `#research`, plus the subject root |
| quick | `#inbox` |

- **Two levels maximum** (`tag_style: nested`), matching the corpus-wide rule in `retrieval.md`. Three levels is a folder tree pretending to be tags, and Bear's sidebar becomes unusable.
- **A tag inside the note body creates it**; there is no separate tag field. A `#word` typed mid-sentence becomes a tag — watch for accidental tags in pasted text.
- **Renaming a tag in Bear rewrites it in every note.** That is the correct way to run a tag merge here (`retrieval.md`), and it is not reversible in bulk.
- **`#inbox` is the triage queue** and is emptied on the 7-day cadence like any other inbox (`capture.md`).

## Append-Only Reality

The CLI can create and append, but not edit or delete note content. Consequences:

- **Corrections are appends**, dated: `Correction 2026-07-28: the threshold was 20%, not 15%.` A note whose top is wrong and whose bottom corrects it is confusing — put the correction under a `## Corrections` heading at the end and keep it there consistently.
- **Notes that change often should not be routed here.** `actions.md` and status notes belong in local files; Bear is for notes that are written once and read many times.
- **Deletion is a human action in the app.** Never imply a note was removed when only the CLI ran.
- Note ids are Bear's internal identifiers, stable per note; store one only when a later append is expected, and store it in the note's `Source` pointer, not loose.

## Fallback

If `grizzly` is missing, Bear is not running, or the token is absent for an operation that needs it: write locally, stamp `platform: local (fallback from bear)`, and say it in one line (SKILL.md Rule 1).

## Bear Traps

| Trap | Why it fails | Do instead |
|---|---|---|
| Running a command with Bear closed | The callback never returns; it reads as a CLI hang | Confirm the app is running first |
| Passing the token inline | It lands in shell history and in any log | `--token-file` only |
| Reading without `--enable-callback` | The command returns before Bear answers, so the result looks empty | Always pair reads with the flag |
| `#tags` inside pasted text | Creates tags nobody chose, permanently in the sidebar | Review pasted content for `#` before creating |
| Three-level tag trees | The sidebar becomes unnavigable and tags stop being remembered | Two levels |
| Routing frequently-edited notes here | Append-only means every edit is an append | Local files for anything mutable |
| Assuming a CLI delete removed the note | It did not; the note is still in Bear | Say what actually happened |
| Depending on Bear for the corpus of record | Apple-only, and export loses the nested-tag hierarchy | Durable notes in local or Obsidian (`migration.md`) |

**Write triggers for this file** — in the same turn: tag roots, the token pointer (never the token), the callback port and the app-running requirement to `## Platform Facts` in `~/Clawic/data/notes/memory.md`; the routing choice to `config.yaml` and `## Note Map`; every action item found in a Bear note to `actions.md` with `Source: bear:#tag/Title`; a tag merge run in Bear to `artifacts/tag-taxonomy.md`. Formats and thresholds: `memory-template.md`.
