---
name: gogcli-mcp-gmail
description: Use when the user asks to read, organize, draft, forward, autoreply, or otherwise work with Gmail in depth. Triggers for requests involving threads, labels, drafts, attachments, bulk archive/trash/mark-read operations, forwarding messages, or any Gmail operation beyond simple search/get/send. Includes auth and Gmail tools only.
---

# gogcli-mcp-gmail

Extended Gmail MCP server via [gogcli](https://github.com/openclaw/gogcli) — 62 tools: 8 auth + 4 base Gmail + 49 extra dedicated Gmail tools + `gog_upload_slots`.

- **Source:** [github.com/chrischall/gogcli-mcp](https://github.com/chrischall/gogcli-mcp)

## Requirements

- [gogcli](https://github.com/openclaw/gogcli) installed and authenticated
- Node.js 22 or later

## Setup

```json
{
  "mcpServers": {
    "gogcli-gmail": {
      "command": "npx",
      "args": ["-y", "gogcli-mcp-gmail"],
      "env": {
        "GOG_ACCOUNT": "you@gmail.com"
      }
    }
  }
}
```

## Extra Gmail Tools

### Read
| Tool | What it does |
|------|-------------|
| `gog_gmail_raw` | Raw Gmail API JSON for a message |
| `gog_gmail_attachment` | Download an attachment by `attachmentIndex` (or legacy `attachmentId`) and deliver its contents — inline when within `inlineMaxBytes` (3 MiB default, 10 MiB max — larger values are clamped), else a server-side file path — use `url`/`drive` when hosted (`deliver`: auto/inline/drive/url/off). `deliver="url"` gives a signed link `curl` can fetch with no credential, for an hour — hosted deployments only |
| `gog_gmail_url` | Print web URLs for threads |
| `gog_gmail_history` | List history events since a historyId |
| `gog_gmail_messages_search` | Search individual messages, not threads — one row per message |

### Threads
| Tool | What it does |
|------|-------------|
| `gog_gmail_thread_get` | Get a thread with all messages |
| `gog_gmail_thread_modify` | Modify labels on a thread |
| `gog_gmail_thread_attachments` | List all attachments in a thread (fetch each with `gog_gmail_attachment`) |

### Labels
| Tool | What it does |
|------|-------------|
| `gog_gmail_labels_list` | List all labels |
| `gog_gmail_labels_get` | Get a label's details and counts |
| `gog_gmail_labels_create` | Create a new label |
| `gog_gmail_labels_rename` | Rename a label |
| `gog_gmail_labels_delete` | Delete a label |
| `gog_gmail_labels_modify` | Modify labels on one or more threads |
| `gog_gmail_labels_style` | Change a label's color or visibility |

### Bulk operations
| Tool | What it does |
|------|-------------|
| `gog_gmail_archive` | Archive by IDs or query |
| `gog_gmail_mark_read` | Mark read by IDs or query |
| `gog_gmail_mark_unread` | Mark unread by IDs or query |
| `gog_gmail_trash` | Trash by IDs or query |
| `gog_gmail_message_modify` | Modify labels on a single message |
| `gog_gmail_batch_delete` | Permanently delete multiple messages |
| `gog_gmail_batch_modify` | Modify labels on multiple messages |

### Drafts
| Tool | What it does |
|------|-------------|
| `gog_gmail_drafts_list` | List drafts (+ free `origin`/`rootsOwnThread`; `enrich` adds recipients, `hasRecipients`, `isReply`) |
| `gog_gmail_drafts_get` | Get a draft, decoded (`format` text/html/both; `raw` for MIME JSON) |
| `gog_gmail_drafts_create` | Create a draft |
| `gog_gmail_drafts_update` | Update a draft — whole `body`, or `replace`/`append`/`prepend` on the stored text (HTML part generated); `bodyFormat: markdown`; `replyToThreadId` re-threads it in place (same id) + `threadingVerification`; `forkSiblingDraftId` blocks a body overwrite that would drop the other copy's text |
| `gog_gmail_drafts_delete` | Delete a draft |
| `gog_gmail_drafts_send` | Send a draft after the user confirms a preview of it (404 → `DRAFT_FORKED`, or `GOOGLE_404_NOT_THE_DRAFT` if the draft is still listed) |
| `gog_gmail_drafts_copy_to` | Send a "DRAFT: " review copy of a stored draft to someone else; the draft is untouched and the body is never passed or echoed in full |
| `gog_gmail_drafts_diff` | Diff two drafts (body divergence, threading loss, fork verdict) |
| `gog_gmail_drafts_reply` | Save a reply as a draft — inherited recipients, subject and quote; never sends |
| `gog_gmail_drafts_reply_all` | Save a reply-all as a draft; never sends |
| `gog_gmail_drafts_forward` | Save a forward as a draft; recipients optional, so it can be staged without any |

A draft edited in a mail client is replaced, not updated: the old id 404s. `drafts_update` / `drafts_send` answer that
404 with a `DRAFT_FORKED` report (what happened, the drafts that exist, what to do) instead of a bare `notFound`, at a
bounded cost of ≤2 extra gog calls. It never names a replacement — the 404'd draft cannot be fetched, so no lineage
signal can exist; use `drafts_diff` on a named pair for that. The 404 is attributed first: `replyToThreadId` and
`replyToMessageId` resolve their own entities and 404 identically, so if the draft id is still in the listing the answer
is `GOOGLE_404_NOT_THE_DRAFT` — no fork claimed, reply target named. That listing is capped at 20, so `listingEvidence`
says what it can carry: only a `complete-listing` (the window came back short, i.e. it covered the folder) claims the
draft is gone; `capped-listing` and `listing-unavailable` say in words that they establish nothing. A reply target, when
one was passed, is echoed and explained first.

`drafts_diff` confirms a pairing only on a link from the candidate **to the original** (its `Message-Id` in the
candidate's `In-Reply-To`/`References`) or on agreement over text **neither draft quoted and neither client generated**
— the salutation, closing formula, name and signature block are excluded alongside quoting, because a client writes them
identically on every message (`Hi Jennifer,` + `Thanks,` + `Chris` + `Sent from my iPhone` is 4 lines and 43 characters
of pure apparatus). A shared reply root is corroboration only — every reply in a thread has one — and `none` means no
evidence was found, not "unrelated". To adopt the survivor back onto the thread, call
`drafts_update` with `replyToThreadId`: same draft id, gog resolves the reply headers, `threadingVerification` reports
whether it worked. It rewrites the whole body, so diff and merge first.

gog requires a body on every update, so there is no header-only edit and every adoption overwrites the body. Pass
`forkSiblingDraftId` (the other copy's id) and the update reads that draft first — one extra gog call, zero when the param
is absent — and refuses to write (`DRAFT_CONTENT_LOSS`, nothing changed) if your body drops a line the sibling holds,
naming the lines; `acceptContentLoss: true` overrides, and `contentLossCheck.written` then reports whether the write it
authorised actually succeeded — a failed write says so and says nothing was saved. A check that could not run refuses too
(`DRAFT_CONTENT_LOSS_UNCHECKED`). It compares text only and never claims one draft replaced another — that is
`drafts_diff`'s job.

### Write
| Tool | What it does |
|------|-------------|
| `gog_gmail_import` | Import an RFC822/EML message into the mailbox (keeps its headers/date; does not send) |
| `gog_gmail_forward` | Forward a message |
| `gog_gmail_reply` | Reply to the original sender |
| `gog_gmail_reply_all` | Reply to sender plus every To/Cc recipient |
| `gog_gmail_autoreply` | Reply once to all messages matching a query |

### Settings
| Tool | What it does |
|------|-------------|
| `gog_gmail_vacation_get` | Get the vacation responder settings |
| `gog_gmail_vacation_update` | Enable/disable the vacation responder |
| `gog_gmail_filters_list` | List all filters |
| `gog_gmail_filters_get` | Get a filter by ID |
| `gog_gmail_filters_create` | Create a filter |
| `gog_gmail_filters_delete` | Delete a filter |
| `gog_gmail_sendas_list` | List send-as aliases |
| `gog_gmail_sendas_get` | Get one send-as alias |
| `gog_gmail_sendas_create` | Create a send-as alias |
| `gog_gmail_sendas_update` | Update a send-as alias |
| `gog_gmail_sendas_delete` | Delete a send-as alias |
| `gog_gmail_sendas_verify` | Resend an alias verification email |

Plus 8 auth tools and 4 base Gmail tools (search, get, send, run). Use `gog_gmail_run` for the settings with no dedicated tool (`delegates`, `forwarding`, `watch`) and email tracking (`track`).

## Files on a hosted deployment

When this server is hosted (remote), it cannot read paths on your machine. Call
`gog_upload_slots` with `files: [{filename}]`, PUT each file to its `uploadUrl`
with the slot's `curl` command, then pass the returned `blobKeys` to the drafts tools (`gog_gmail_drafts_create`, `_update`, `_reply`, `_reply_all`), `gog_gmail_import`, and the base send/reply tools.
Files up to 25 MiB; each is deleted from the upload store after the call succeeds
and kept if it fails. On a local install, pass a path as before.
