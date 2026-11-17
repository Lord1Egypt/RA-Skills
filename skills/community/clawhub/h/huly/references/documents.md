# Documents — nested wiki content with snapshots and controlled workflow

Documents are the second knowledge primitive. Use them only when the user explicitly asks for nested wiki organization, versioned snapshots, ControlledDocument/e-signature workflow, or training — or when Cards genuinely cannot represent what they want (see `references/cards.md` for the decision matrix).

---

## Decision: Documents vs Cards (recap)

| Use Documents when…                                | Use Cards when in doubt.              |
| -------------------------------------------------- | ------------------------------------- |
| Nested parent/child hierarchy needed (wiki-style)  | Flat-by-Type organization             |
| Versioned snapshots per doc required               | Custom typed attributes per MasterTag |
| ControlledDocument / e-signature workflow (TraceX) | Quick captures, records, notes        |
| Training workflow (Trainee / TrainingRequest)      | Structured / kanban-style             |

If the user said "create a document" or "make a wiki page" → use Documents.

---

## Before you create a document: confirm teamspace and parent

```bash
huly teamspace list --json | jq -r '.[].name'
huly document list --teamspace "Engineering" --json | jq -r '.[].title'
```

**Auto-creation:** if no teamspace exists, the CLI auto-creates a `General` teamspace on first `huly document create`. Don't be surprised by the auto-created entity if you were expecting an empty workspace.

---

## Document commands

### Discover

```bash
huly document list --json
huly document list --teamspace "Engineering" --json
huly document list --teamspace "Engineering" --title-search "deploy" --json   # case-insensitive regex
huly document list --content-search "kubectl" --json                          # case-insensitive regex; best-effort
huly document list --teamspace X --limit 100 --offset 0 --json               # in-memory slice

huly document get "My design doc" --json       # by title
huly document get <doc-ref> --json              # by id (resolved against document:class:Document)
huly document get <doc-ref> --markdown          # body as Markdown
```

`--title-search` and `--content-search` are MongoDB-style regex (case-insensitive). They are best-effort — for serious fulltext use `huly ws queryAll` (Elasticsearch-backed).

### Create

```bash
huly document create \
  --title "Architecture decision: queue system" \
  --teamspace "Engineering" \
  --body "# Decision\nWe will use NATS over Kafka because…\n\n## Consequences\n…" \
  --parent "Architecture decisions"   # optional, by title or ref; OR --parent <ref>
huly document create \
  --title "…" \
  --body-file ./content.md           # alternative to --body; mutually exclusive
```

**Smart defaults silently applied:**

- `teamspace`: `--teamspace <name>` → `HULY_TEAMSPACE` env → index lookup → exact name → first available → **auto-create `General`** if no teamspaces exist.
- `parent`: ref-resolved against documents within the teamspace; falls back to title-match (exact, lowercased) within the teamspace. Ambiguous titles throw `Ambiguous`.
- `space`: `teamspace._id`.
- `rank: '0|aaaaa:'`.
- `archived: false` unless `--archived` is set.
- `content: body ?? ''`.

**Auto-creation:** a `General` teamspace with `{description: "Default teamspace (auto-created)", private: false}` is auto-created if `findAll` returns zero. ONE auto-create per workspace; subsequent creates use the new space.

**`--body` vs `--body-file`:** mutually exclusive. Validation: `ambiguous body input`.

**Stored as prosemirror markup:** `document create --body` uploads a prosemirror-JSON blob (via `client.markup.uploadMarkup`) referencing the new document's content field. The blob ref is stored in `doc.content`; the ydoc is created lazily on first read/edit. `--markdown` round-trips correctly. Web-UI-created docs that use embed / mention nodes may not round-trip cleanly via the CLI — these require `huly ws tx` to manipulate.

### Update

```bash
huly document update <ref> --title "New title"
huly document update <ref> --body "Full new body"          # full replace
huly document update <ref> --body-file ./new.md
huly document update <ref> --old-text "old line" --new-text "new line"   # targeted single
huly document update <ref> --old-text "X" --new-text "Y" --replace-all     # all occurrences
huly document update <ref> --archived                    # archives (cannot unarchive via this flag)
```

**Mutually exclusive on update:**

- `--body` + `--body-file` → error.
- `--body` + (`--old-text` + `--new-text`) → error.
- `--body-file` + (`--old-text` + `--new-text`) → error.

**Targeted substitution:**

- `--old-text` appears 0 times → `NotFound: old-text not found in document`.
- `--old-text` appears ≥ 2 times without `--replace-all` → `Ambiguous: N occurrences of --old-text — pass --replace-all`.
- `--old-text` appears ≥ 2 times with `--replace-all` → replaces all.

**`--archived` flag:** presence = true. There is no value (the CLI currently exposes only archive, not unarchive, via this flag). **Unarchive is only possible via raw RPC** (`huly ws updateDoc` to clear `archived`); the recipe below is the only path, but it bypasses CLI safety checks. Confirm with the user out loud before invoking.

### Move / reparent

> **Advanced — confirm with the user before invoking.** The CLI's `huly document update` does NOT accept `--parent`. Reparenting requires raw RPC; the recipe below is the only path.

```bash
huly ws updateDoc '["document:class:Document", "<space>", "<doc-id>", {"$set":{"parent":"<new-parent-id>"}}]'
```

### Delete

```bash
huly document delete <ref>
huly document delete <ref1> <ref2> <ref3> --yes      # REQUIRED --yes for multiple
```

Snapshots are cascade-deleted server-side. There is no `--dry-run` preview.

### Snapshots (versioned history)

```bash
huly document snapshots <ref> --json
huly document snapshot <ref> --snapshot-id <sid> --json
huly document snapshot <ref> --snapshot-id <sid> --markdown
```

The CLI only LISTS and GETS snapshots; creation is implicit via the platform's snapshot-on-edit policy. There is no `huly document create-snapshot` command.

### Inline comments

```bash
huly document inline-comments <ref> --json
```

Lists only. The CLI has NO command to create, reply to, or resolve inline comments. Web UI or raw RPC required for those operations.

**Critical:** resolving an inline comment thread DELETES all replies in it. Cannot be undone.

---

## Teamspace commands

```bash
huly teamspace list --json
huly teamspace get "Engineering" --json
huly teamspace create --name "Engineering" --description "…" --type public --private false
huly teamspace update "Engineering" --name "Engineering v2" --description "…"
huly teamspace delete "Engineering" --yes
huly teamspace delete "A" "B" --yes
```

**Smart defaults:**

- `type: 'public'` (free-text; CLI doesn't validate against enum despite help text suggesting `public|private`).
- `private: false` unless `--private`.
- `archived: false`.
- `members: []`, `owners: []`.

**Cascade-on-delete:** cascades to every Document, DocumentSnapshot, etc. in the teamspace.

**`--type` vs `--private`:** two independent fields. `--type "private"` (string) sets `type`; `--private` (boolean) sets `private`. Both can be set; they mean different things.

---

## Server-side side effects you cannot avoid

### `@mention` in body creates backlinks + inbox notifications

The CLI's `document create --body "Hi @alice"` stores the body as a raw string. The platform's mention parser runs on read/parse and creates backlinks in the recipient's inbox (subject to notification prefs). Round-trips correctly for plain Markdown.

For web-UI-created docs with embedded `@mention` nodes, `--markdown` returns the raw markup ref string — round-trip won't work. Use `huly ws tx` to manipulate these directly.

### ControlledDocument workflow (full lifecycle)

The platform has a ControlledDocument / e-signature / training workflow. The CLI surfaces NONE of it. Behaviors that exist server-side:

- **State transitions**: Author → Reviewer → Approver e-signatures are enforced in that order. **Author must sign before Reviewer/Approver can sign.**
- **Effective version → archives older Effective versions** of the same template.
- **`DocumentMeta.title`** is rewritten to `"<code> <title>"` on `--state effective`.
- **`TrainingRequest`** auto-created per trainee if `documents.mixin.DocumentTraining` is enabled.
- **After a review**, the doc must be re-reviewed before it can be approved again (`OnDocTitleChanged`/`OnDocHasBecomeEffective`).
- **Inline comments must be resolved before approval.**

The CLI cannot trigger any of this. If the user asks for a ControlledDocument workflow:

> "ControlledDocument state transitions (Draft → In Review → Effective, e-signatures, training) are not exposed by the CLI. You'll need to advance states through the web UI; I can read the doc, snapshot it, and bulk-manage inline comments there."

### Default Drive ("Records") is pre-created

Every new workspace gets a `Records` Drive (Document workspace). The first document you create lives under it.

### Backlinks panel

The paper-clip icon in the UI shows every `@mention` pointing at the doc. CLI has no command to query backlinks directly; if needed, query `activity:class:UserMentionInfo` via `huly ws findAll`.

### Drawing board, Mermaid diagrams, highlights, notes

Slash commands in the web UI editor. The CLI stores raw Markdown — none of these round-trip.

---

## Common task recipes

### Create a wiki-style document with nested children

```bash
# 1. Confirm or create teamspace
huly teamspace list --json | jq -r '.[].name'
# If "Engineering" missing, create it first
# huly teamspace create --name "Engineering" --type public

# 2. Create root
ROOT=$(huly document create \
  --title "Engineering handbook" \
  --teamspace "Engineering" \
  --body $'# Welcome\nThis handbook covers…')
echo "$ROOT"

# 3. Create child (use --parent by title or by _id from $ROOT)
huly document create \
  --title "Onboarding" \
  --teamspace "Engineering" \
  --parent "$ROOT" \
  --body $'## Day 1\n…\n\n## Week 1\n…'
```

### Targeted edit on a doc body

```bash
# Preview the current body
huly document get <ref> --markdown

# Edit a single line (must appear exactly once)
huly document update <ref> --old-text "TODO: rotate keys" --new-text "DONE: rotated keys 2026-07-02"

# Or all occurrences
huly document update <ref> --old-text "acme.com" --new-text "acme.io" --replace-all
```

### Find docs without a teamspace (orphans)

```bash
huly document list --json | jq -r '.[] | select(.space == null) | ._id'
```

Then reparent via `huly ws updateDoc` (advanced; confirm with the user first — see "Move / reparent" above).

### Snapshot history of a doc

```bash
# List snapshot titles + ids
huly document snapshots <ref> --json | jq -r '.[] | "\(._id)\t\(.title)"'

# Get a specific snapshot's body as markdown
huly document snapshot <ref> --snapshot-id <sid> --markdown
```

### Audit who last edited a doc

```bash
huly document get <ref> --json | jq '{modifiedBy, modifiedOn, _id}'
# Or full tx history:
huly ws findAll '["core:class:Tx",{"objectId":"<doc-id>"}]' --json \
  | jq '[.[] | {by: .modifiedBy, on: .modifiedOn, ops: .attributes}]'
```

---

## Gotchas

- **`--archived` flag value:** there is no `--archived false`. Pass `--archived` (presence = true) to archive. **Unarchive is only available via raw `huly ws updateDoc` to clear `archived`**; confirm with the user first. The CLI help text doesn't mention this asymmetry.
- **`document update` cannot `--parent`.** Reparent only via `huly ws`; confirm with the user first (see "Move / reparent" above).
- **`document update` `--body` vs `--old-text`/`--new-text`** are mutually exclusive. Pick one strategy.
- **Inline comments cannot be created, replied to, or resolved via the CLI.** Only listed.
- **Resolving an inline thread DELETES all replies.** Don't write "important" content there.
- **`--content-search`** is best-effort regex on the body field. For real fulltext, use `huly ws queryAll`.
- **Teamspace `--type`** is free-text despite help text implying an enum. Pass any string.
- **Auto-creating a `General` teamspace** happens once per workspace. Don't try to "disable" it — just create your own with the right name and reuse.
- **No controlled-document state transitions on CLI.** Web UI only.
- **No training-request management on CLI.** Web UI only.
- **CLI-created docs store raw strings**, not `MarkupContent`. Rich-text features (mentions as actual nodes, embeds) don't survive the round-trip.
- **Newlines in `--body` are auto-stripped.** The CLI's `normalizeMarkupInput` strips newlines (and adjacent whitespace) before the prosemirror parser runs, so `<h1>Title</h1>\n<p>Body</p>` round-trips cleanly into one heading and one paragraph with no phantom empty paragraphs. (Earlier versions warned against embedded `\n`; that restriction is now lifted.)
- **Nested HTML must be properly nested, not flat.** A nested list needs `<li>...<ul><li>...</li></ul></li>`, not `<li>...</li><ul><li>...</li></ul>`. The prosemirror parser validates structure and silently drops malformed siblings — same applies to blockquotes in lists, code blocks in table cells, etc.
- **`card delete` MinIO cleanup is best-effort.** Before `removeDoc`, the CLI writes an empty markup via `updateMarkup` to clear the ydoc. Old JSON snapshots may persist on disk until garbage-collected server-side. (Requires server-side Issue 4 fix to fully clean.)
