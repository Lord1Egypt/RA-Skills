# Evernote

Usually the source of a migration rather than a destination. Driven through the `clinote` CLI, which is thin; the corpus, the OCR over scans, and the notebook structure are what keep users here.

**Contents:** [Requirements](#requirements) · [Operations](#operations) · [Notebooks](#notebooks) · [Writing a Note](#writing-a-note) · [What It Loses](#what-it-loses) · [Getting Out](#getting-out) · [Fallback](#fallback) · [Evernote Traps](#evernote-traps)

**Before writing**, read `## Platform Facts` in `~/Clawic/data/notes/memory.md` for the notebook names in use. Evernote allows two notebooks with near-identical names, and a note filed in the wrong one is found only by full-text search.

## Requirements

An Evernote account and the user's own installation of `clinote` (`go install github.com/TcM1911/clinote@latest`), authenticated once with `clinote login`. Nothing is installed on the user's behalf.

- The auth token `clinote login` stores is a secret: it is never copied into `~/Clawic/data/`. Record only that authentication exists and where, as a pointer (`file:~/.config/clinote/...`), in `## Platform Facts`.
- Note content sent through `clinote` leaves the machine. Never route a type here that the user has not routed here.

## Operations

```bash
clinote notebook list
clinote note list --notebook "Meetings"
clinote note search "pricing"
clinote note view --title "Product Sync 2026-07-26"
clinote note create --title "..." --file /tmp/note.md --notebook "Meetings"
clinote note delete --title "..."
```

Notes are addressed by **title**, not by a stable id, so two notes with the same title are ambiguous to every command including `delete`. Titles here always carry the date (`2026-07-26 Pricing three tiers`).

## Notebooks

One notebook per type, matching the local layout: `Meetings`, `Decisions`, `Projects`, `Journal`, `Research`, `Inbox`. Notebooks are created by the user in the app; verify the exact name with `clinote notebook list` before the first write and record it in `## Platform Facts`.

Evernote tags exist but are not reliably reachable from the CLI. Treat notebook plus title as the retrieval model here, which is another reason the title must be the claim (SKILL.md Rule 2).

## Writing a Note

Content goes in from a file, which keeps markdown intact better than inline `--content`:

```bash
cat > /tmp/note.md << 'EOF'
# Pricing: staying at three tiers — 2026-07-26

**Present:** Alice, Bob

## Decisions
- Three tiers stay; revisit at 500 customers — @alice, effective 2026-07-26

## Actions
- [ ] @alice: send the pricing deck — 2026-08-04
EOF
clinote note create --title "2026-07-26 Pricing three tiers" --file /tmp/note.md --notebook "Meetings"
```

Delete the temp file afterwards — `/tmp` is readable by anyone on the machine and the note outlives the session.

## What It Loses

| Feature | Reality through the CLI |
|---|---|
| Markdown structure | Converted to Evernote's HTML-based format; headings and lists survive, nested structure often does not |
| Checkboxes | `- [ ]` becomes plain text, not an Evernote to-do |
| Tables | Frequently mangled; avoid in notes routed here |
| Tags | Not reliably settable or readable |
| Stable ids | Not exposed; titles are the address |
| Reminders and saved searches | App-only, invisible to the CLI |

The practical consequence: notes routed to Evernote are **read-mostly text**. Action items extracted from them still go to `actions.md` like everything else, because the checkbox will not survive.

## Getting Out

Export produces ENEX (XML) or HTML. What survives and what does not, plus the restore test that must run first: `migration.md`.

- **Export per notebook**, not the whole account at once: a single huge ENEX is slower to convert and harder to verify.
- **Attachments are embedded base64 in ENEX** — the file is large and the images must be extracted during conversion, which is where most conversions quietly fail.
- **Created and updated dates are in the ENEX** and should be written into frontmatter `date:` during conversion, or the whole corpus arrives dated today.
- Keep the account read-only for a full month after migrating (`migration.md`).

## Fallback

If `clinote` is missing, login has expired, or the service is unreachable: write locally, stamp `platform: local (fallback from evernote)`, and say it in one line (SKILL.md Rule 1).

## Evernote Traps

| Trap | Why it fails | Do instead |
|---|---|---|
| Duplicate titles | Every command that addresses by title becomes ambiguous, including delete | Date in the title, always |
| Expecting markdown to round-trip | The HTML conversion is lossy in both directions | Read-mostly text; structure lives in the local copy |
| Relying on checkboxes as the task list | They do not survive the conversion | `actions.md` (`action-items.md`) |
| Notebooks with near-identical names | Notes split across two, found only by full text | Verify with `notebook list` first |
| Leaving the note in `/tmp` | Readable on a shared machine, survives the session | Delete after creating |
| Exporting the whole account in one pass | Huge ENEX, slow conversion, unverifiable result | Per notebook |
| Migrating and closing the account the same week | Gaps surface after access is gone | Read-only for a month |

**Write triggers for this file** — in the same turn: notebook names, the auth pointer (never the token) and any CLI limitation encountered to `## Platform Facts` in `~/Clawic/data/notes/memory.md`; the routing choice to `config.yaml` and `## Note Map`; every action item found in an Evernote note to `actions.md` with `Source: evernote:<Title>`; a migration plan and its fidelity findings to `artifacts/migration-evernote-to-<target>.md` with its `## Boxes` line. Formats and thresholds: `memory-template.md`.
