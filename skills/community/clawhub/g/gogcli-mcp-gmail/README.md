# gogcli-mcp-gmail

> [!WARNING]
> **AI-developed project.** This codebase was built and is actively maintained by [Claude Code](https://www.anthropic.com/claude). Review all code and tool permissions before use.

Extended Gmail [MCP](https://modelcontextprotocol.io) server via [gogcli](https://github.com/openclaw/gogcli). Includes auth tools plus 49 additional dedicated Gmail tools for threads, labels, drafts, attachments, forwarding, autoreply, and bulk operations.

## Requirements

- [gogcli](https://github.com/openclaw/gogcli) installed and authenticated
- Node.js 22+

```bash
brew install gogcli
gog auth add your@gmail.com --services gmail
```

## Installation

```bash
npm install -g gogcli-mcp-gmail
```

### Claude Desktop

Add to `~/Library/Application Support/Claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "gogcli-gmail": {
      "command": "gogcli-mcp-gmail",
      "env": {
        "GOG_ACCOUNT": "you@gmail.com"
      }
    }
  }
}
```

### Claude Code

```bash
claude mcp add gogcli-gmail -- gogcli-mcp-gmail
```

## Extra Gmail Tools (49)

Plus 8 auth tools and 4 base Gmail tools (search, get, send, run) — 61 in all.

### Read

| Tool | Description |
|------|-------------|
| `gog_gmail_raw` | Dump the raw Gmail API JSON for a message (lossless, for scripting) |
| `gog_gmail_attachment` | Download an attachment (by `attachmentIndex`, or the legacy opaque `attachmentId`) and deliver its contents — by default an image inline and anything else as a server-side file path (`deliver`: auto/inline/drive/url/off; `inline` forces bytes within `inlineMaxBytes`, 3 MiB by default and at most 10 MiB — a larger value is clamped, since the hosted runtime caps one result at 14 MiB; `drive` uploads to Google Drive). On a hosted deployment, where that path is unreadable, use `url` or `drive`. `deliver="url"` returns a **signed download link** — fetchable with `curl`, no credential and no Google session, valid for an hour, nothing written to your Drive and not blocked by `GOG_READONLY`; it needs the blob store a hosted deployment lends this server, so a local stdio install is told to use another mode |
| `gog_gmail_url` | Print Gmail web URLs for one or more threads |
| `gog_gmail_history` | List Gmail history events since a given historyId |
| `gog_gmail_messages_search` | Search individual messages rather than threads — one result per matching message |

### Threads

| Tool | Description |
|------|-------------|
| `gog_gmail_thread_get` | Get a thread with all messages, optionally with sanitized content and attachments |
| `gog_gmail_thread_modify` | Modify labels on all messages in a thread |
| `gog_gmail_thread_attachments` | List all attachments in a thread (fetch each with `gog_gmail_attachment`) |

### Labels

| Tool | Description |
|------|-------------|
| `gog_gmail_labels_list` | List all labels |
| `gog_gmail_labels_get` | Get label details and counts |
| `gog_gmail_labels_create` | Create a new label |
| `gog_gmail_labels_rename` | Rename a label |
| `gog_gmail_labels_delete` | Delete a label |
| `gog_gmail_labels_modify` | Modify labels on one or more threads |
| `gog_gmail_labels_style` | Change a user label's color or visibility |

### Bulk Operations

| Tool | Description |
|------|-------------|
| `gog_gmail_archive` | Archive messages by ID or by query |
| `gog_gmail_mark_read` | Mark messages as read by ID or by query |
| `gog_gmail_mark_unread` | Mark messages as unread by ID or by query |
| `gog_gmail_trash` | Move messages to trash by ID or by query |
| `gog_gmail_message_modify` | Modify labels on a single message |
| `gog_gmail_batch_delete` | Permanently delete multiple messages (irreversible) |
| `gog_gmail_batch_modify` | Modify labels on multiple messages at once |

### Drafts

| Tool | Description |
|------|-------------|
| `gog_gmail_drafts_list` | List drafts (free `origin` + `rootsOwnThread`; `enrich` adds subject/from/date, to/cc/bcc, `hasRecipients` and `isReply` for one extra call) |
| `gog_gmail_drafts_get` | Get a draft by ID, decoded by default (`format`: `text` / `html` / `both`, or `raw` for gog's base64 MIME JSON) |
| `gog_gmail_drafts_create` | Create a new draft (`bodyFormat: "markdown"` renders the HTML part from one markdown body) |
| `gog_gmail_drafts_update` | Update a draft — whole body, or patch the stored text with `replace` (exact, once) / `append` / `prepend`; the HTML part is generated from the text unless you pass one — and re-thread it in place with `replyToThreadId`, keeping the same id, with a `threadingVerification` block reporting what gog actually wrote. `forkSiblingDraftId` refuses the write when the new body would drop text the other copy still holds |
| `gog_gmail_drafts_delete` | Delete a draft |
| `gog_gmail_drafts_send` | Send an existing draft (a 404 comes back diagnosed — `DRAFT_FORKED`, or `GOOGLE_404_NOT_THE_DRAFT` when the draft is still listed) |
| `gog_gmail_drafts_copy_to` | Send a review copy of a stored draft (subject + body, prefixed `DRAFT: `) to other addresses without touching the draft; the prompt shows 300 characters, length and SHA-256, not the whole body. `appendText` and `includeQuotedFrom` add a note and the message being answered |
| `gog_gmail_drafts_diff` | Diff two named drafts — divergent body lines (with untruncated `onlyInACount`/`onlyInBCount`), threading loss, and a conservative fork verdict (2 gog calls) |
| `gog_gmail_drafts_reply` | Save a reply as a draft — inherited recipients, subject and quote; never sends |
| `gog_gmail_drafts_reply_all` | Save a reply-all as a draft; never sends |
| `gog_gmail_drafts_forward` | Save a forward as a draft; recipients optional, so it can be staged without any |

#### When a draft you created stops resolving

A draft edited in a real mail client is not updated in place: the client writes a **new** draft and abandons the
original, so the id you were given starts returning `Google API error (404 notFound)` — indistinguishable, at first
glance, from "someone deleted it".

`gog_gmail_drafts_update` and `gog_gmail_drafts_send` turn that 404 into a `DRAFT_FORKED` report: what happened, the
drafts that *do* exist (with the free `origin` / `rootsOwnThread` fields, plus subject/from/date), the other
explanations that produce the same 404 (deleted, already sent), and what to do next. It **names no replacement** — the
404'd draft can no longer be fetched, so there is nothing to establish lineage against, and without lineage no pairing
verdict is possible. Naming a pair and running `gog_gmail_drafts_diff` is the only path here that issues a fork verdict.

**"Not listed" is not "does not exist".** That listing is capped at 20 drafts by construction — it is a failure path and
must not grow with the mailbox — so the report states, under `listingEvidence`, what its own evidence can carry. Only a
listing that came back *short* of the window covered the whole Drafts folder and earns the sentence "draft X no longer
resolves" (`basis: complete-listing`, `establishesTheDraftIsGone: true`). A window that came back *full*
(`capped-listing`) or a listing that *failed* (`listing-unavailable`) says so in words and claims nothing about the
draft: on a mailbox with more than 20 drafts, absence of evidence must not become the fork story by default. Widen it
with `gog_gmail_drafts_list` before concluding anything. When the call named a reply target, that target is echoed on
the report and its explanation is listed **first** — the branch with the least evidence about the draft is the last one
that should stay silent about the leading alternative.

**The 404 is attributed, not assumed.** `gmail drafts update` resolves up to three Google entities — the draft, the
thread behind `replyToThreadId`, and the message behind `replyToMessageId` — and gog renders all three 404s with the
same string. The listing the report already pays for settles it: if the draft id is still listed, the answer is
`GOOGLE_404_NOT_THE_DRAFT`, which claims no fork, names the reply target as the remaining explanation, and tells you
not to go hunting for a replacement draft. `DRAFT_FORKED` is only used when the draft really has stopped resolving.

**What counts as lineage** (`gog_gmail_drafts_diff`): only a link from the candidate *to the original* — the original
draft's own `Message-Id` inside the candidate's `In-Reply-To`/`References`, or agreement on text **neither draft
quoted**. A **shared reply root is not lineage**: it links both drafts to a common *ancestor*, which every reply in a
thread has, so it is reported as corroboration and can raise the answer no higher than an explicitly weak `candidate`.
Quoted lines are excluded from the agreement metric because Apple Mail quotes on every reply — two unrelated replies
into one thread carry the same 30-line block, which scores 0.79 on a whole-body line metric while proving nothing.

**Client boilerplate is excluded for the same reason.** The salutation, the closing formula, the name under it and the
signature block are reproduced identically on every message a client composes, whatever the message says —
`Sent from my iPhone` is Apple Mail's own default. `Hi Jennifer,` + `Thanks,` + `Chris` + `Sent from my iPhone` is 4
lines and 43 characters, enough on its own to clear a line-and-character threshold, so counting it paired two genuinely
unrelated one-sentence notes as `confirmed` — and short confirmation plus a signature is the dominant shape of this
mailbox. `bodyAgreement` reports `quotedLinesIgnored` and `boilerplateLinesIgnored` separately so the arithmetic can be
redone. The divergence report still counts those lines: a merge that drops the signature really did drop it. The cost
of the tighter metric is that a genuine fork of a *one-sentence* note now comes back `candidate` rather than
`confirmed`, with `missing` naming the shortfall — the deliberate direction, since a missed fork costs a re-check and a
wrong one sends the wrong text to the wrong thread.

Cost is bounded and constant: **at most 2 extra gog invocations**, only on a call that already failed, never scaling
with the number of drafts. A non-404 failure spends nothing.

Once you know which draft survived, `gog_gmail_drafts_update` with `replyToThreadId` adopts it back onto the original
conversation **in one call, keeping its draft id** — gog resolves `In-Reply-To`/`References` from that thread's latest
message and reports them back under `threadingVerification` (`ok`, the effective headers, and a note). Two things that
block make that safe to rely on: an explicit reply target *replaces* the draft's stored lineage rather than merging with
it, and gog requires a body on every update, so the call **overwrites the whole body**. Diff first, merge by hand, then
write.

#### Guarding the merge: `forkSiblingDraftId`

Because gog requires a body on every update there is **no header-only edit**, so adopting a draft back onto its thread is
always a full body overwrite — the exact operation that destroys the paragraph living only in the other copy. In the
observed fork *neither* copy was a superset: the mail-client copy had lost a paragraph and the Gmail copy had gained
sentences.

The line-based comparison cuts the other way too: a paragraph re-wrapped at a different width no longer matches line
for line, so `none` means *no evidence was found*, never *proven unrelated*, and the notes say so.

Pass `forkSiblingDraftId` (the id of the other copy) and `gog_gmail_drafts_update` reads that draft **before** writing and
refuses the write — `DRAFT_CONTENT_LOSS`, nothing changed — if your body omits any line the sibling still holds, naming the
exact lines. Merge them in and retry, or pass `acceptContentLoss: true` to write anyway (the lines are still reported, and
the sibling itself is never touched). A check that cannot be *run* — sibling unfetchable, unparseable, or with no readable
body — refuses too, as `DRAFT_CONTENT_LOSS_UNCHECKED`: an unrun check is not a passed check.

An override reports the write that **actually happened**, never a predicted one: `contentLossCheck.written` is set from
the result, so a write that failed comes back saying it was attempted and saved nothing, and says the listed lines are
still in the sibling. Believing the opposite is the destructive case — a caller who thinks the merged body is stored may
delete or overwrite the copy that now holds the only version of those lines.

It **makes no fork claim**. You name the sibling; nothing searches for it, identical bodies would not prove a pairing and
divergent ones would not disprove one. `contentLossCheck.forkClaim` is always `null` and points at
`gog_gmail_drafts_diff`, which is the only tool here that weighs identity, lineage and ordering.

**Cost:** opt-in, exactly **one** extra gog invocation (a `drafts get` on the id you named — never a scan, never scaling
with the mailbox), and **zero** when the param is absent. A refusal spends that one call and skips the write entirely.

### Write

| Tool | Description |
|------|-------------|
| `gog_gmail_import` | Import an RFC822/EML message into the mailbox, keeping its original headers and date (does not send) |
| `gog_gmail_forward` | Forward a message to new recipients (with optional note) |
| `gog_gmail_reply` | Reply to a message (original sender only) |
| `gog_gmail_reply_all` | Reply to every participant (sender plus all To/Cc recipients) |
| `gog_gmail_autoreply` | Reply once to all messages matching a query (with dedupe label) |

### Settings

| Tool | Description |
|------|-------------|
| `gog_gmail_vacation_get` | Get the vacation responder (auto-reply) settings |
| `gog_gmail_vacation_update` | Enable or disable the vacation responder, with optional start/end and audience limits |
| `gog_gmail_filters_list` | List all Gmail filters |
| `gog_gmail_filters_get` | Get a filter's criteria and actions by ID |
| `gog_gmail_filters_create` | Create a filter from match criteria plus one or more actions |
| `gog_gmail_filters_delete` | Delete a filter by ID |
| `gog_gmail_sendas_list` | List all send-as aliases |
| `gog_gmail_sendas_get` | Get one send-as alias by address |
| `gog_gmail_sendas_create` | Create a send-as alias (usually needs verification before use) |
| `gog_gmail_sendas_update` | Update an alias (display name, reply-to, signature, default) |
| `gog_gmail_sendas_delete` | Delete a send-as alias |
| `gog_gmail_sendas_verify` | Resend the verification email for a pending alias |

Email tracking (`track`) and the remaining admin settings (`delegates`, `forwarding`, `watch`) have no dedicated tool — reach them through the base `gog_gmail_run` escape hatch.

## Files on a hosted deployment

When this server is hosted (remote), it cannot read paths on your machine. Call
`gog_upload_slots` with `files: [{filename}]`, PUT each file to its `uploadUrl`
with the slot's `curl` command, then pass the returned `blobKeys` to the drafts tools (`gog_gmail_drafts_create`, `_update`, `_reply`, `_reply_all`), `gog_gmail_import`, and the base send/reply tools.
Files up to 25 MiB; each is deleted from the upload store after the call succeeds
and kept if it fails. On a local install, pass a path as before.

## License

MIT
