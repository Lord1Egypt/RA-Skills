---
name: honeybook
description: This skill should be used when the user asks about HoneyBook client-portal data. Triggers on phrases like "check HoneyBook", "sign contract", "pay invoice", "HoneyBook vendors", "unsigned contracts", "open invoices", "message the planner", "reply to my vendor", "next meeting with the planner", or any request involving wedding-vendor contracts, invoices, brochures, proposals, payments, messages, meetings or tasks via HoneyBook.
---

# honeybook-mcp

MCP server for HoneyBook's client portal — contracts, invoices, questionnaires, messages, meetings, tasks and payments across multiple wedding vendors, with magic-link session capture, in-portal messaging, and deep-link fallback for signing and paying.

## Tools

- `use_magic_link` — Capture a portal session from a vendor magic-link URL (`/app/link/resolve/…`)
- `use_flow_link` — Capture a questionnaire credential from a flow link (`/flow/<flowId>?hash=…`)
- `list_active_sessions` — Show active credentials, split into `portalSessions` and `flowCredentials`
- `get_flow(flow_id?, view?)` — Read one questionnaire (flow) and its answers (two calls: public `/minimal` for the vendor company id, then `/client/flow/<id>/active?ctxc=…`)
- `list_workspace_files` — All files one vendor has shared (filter by type)
- `get_workspace_file(file_id, section?)` — Full detail for one file. Takes `section`, **not** `view` — see below
- `get_workspace` — Workspace detail + status flags
- `list_payment_methods` — Saved payment methods
- `sign_contract` — Deep link to sign in portal (asks the user to confirm first)
- `pay_invoice` — Deep link to pay in portal (asks the user to confirm first)
- `list_projects` — Your projects (HoneyBook "events") with a vendor, each with the `workspace_id` the tools below take
- `get_project(project_id, view?)` — Project details: date, time, location, guests, custom fields, people (name/email/phone/role)
- `list_messages` — Messages in a workspace (`kind=activity` for the activity log, `kind=all` for both): compact cards, newest first; never marks anything seen
- `get_message` — One message in full (`format=text` default, `markdown` to keep lists and links, or the raw `html`) with attachments and delivery status
- `send_message` — Send a new message (`subject` + `body`) or reply (`reply_to_message_id`, subject inherited) through the portal; `format=markdown` sends a Markdown body as formatted HTML; asks the user to confirm first
- `mark_messages_seen` — Mark feed items seen, the way opening the Activity tab does
- `list_meetings` — Meetings the vendor scheduled (consultations, Zoom calls): time, join link, password; rescheduled meetings show their latest time
- `list_tasks` — Tasks assigned to you with today/this-week/overdue counts and task groups
- `list_notes` — Notes the vendor shared (meeting notes, AI recaps)
- `list_attachments` — Loose images, files and bookmarks (not contracts/invoices — those are workspace files)
- `list_payments(workspace_id, view?)` — Every payment on every file in a workspace, with paid/unpaid totals; `workspace_id` also takes a project name as listed in its schema; `view="brief"` answers one line per payment

## Response shape (`view`)

Only **two** tools here take the fleet's `view` parameter: `get_project` and
`get_flow`. Both honour `compact | raw`, and **`compact` is the default** — you
get the cheap shape without asking for it. There is no `full` rung on either:
`raw` already IS every field HoneyBook sent, so a third value would silently
alias to one of the other two.

`list_payments` takes a different `view`: `full` (the default, the payment
schedule with totals) or `brief` (one plain-text line per payment). `brief` is
the context-groups answer shape, not a fleet rung — see "In context groups".

The two compact rungs are **not the same kind of thing**, and the difference
decides which one you can trust to be complete:

- **`get_project` compact is a field projection.** It keeps `_id`, `name`,
  `type`, `date`/`end_date`, `time_start`/`time_end`, `timezone`, `location`,
  `venue_name`, `guests`, `budget`, `details`, `project_dates`, non-empty
  `custom_fields`, `image_url`, `last_activity_date`, and a de-duplicated
  `people[]` (`_id`, `name`, `email`, `phone`, `role`, `job_title`, `company`).
  Everything else is dropped — `view: "raw"` returns the untrimmed `/details`
  response, which embeds the **vendor's entire account**. Ask for it only when
  you need a field the list above does not name.
- **`get_flow` compact is a byte ceiling, not a projection.** No field is
  pruned. Under 200,000 bytes the questionnaire comes back whole and `compact`
  and `raw` differ only in indentation. Over it, compact replaces the flow with
  `truncated: { bytes, limit, topLevelKeys, hint }` — its own table of contents
  instead of its content. So on a large questionnaire the compact rung returns
  no questions at all; that is the signal to re-call with `view: "raw"`. (A real
  `/active` payload measured 96,246 bytes, comfortably under the ceiling, so the
  ordinary case is the whole thing.)

**`get_workspace_file` does not take `view`. It takes `section`** —
`summary` (default) | `pricing` | `agreement` | `payments` | `all` | `raw` —
and that is a different question, deliberately kept. `view` asks *how much of
the whole record to keep*; `section` asks *which part of it to expand*: line
items and tax/svc detail (`pricing`), contract HTML and signatures
(`agreement`), the full payment schedule (`payments`). `all` is the whole file
with the vendor-side heavy fields pruned — `vendor_emails` alone measured
~1.3 MB on one real proposal — and `raw` keeps even those.

**The surprise worth knowing:** passing `view:` to `get_workspace_file` does not
error. The unknown key is stripped during validation, the call succeeds, and you
get the `summary` section — the default you would have got anyway. Nothing tells
you the argument was ignored. Use the `section` name.

Every other tool has no shape parameter, for one of two reasons:

- **Its output is already narrow, with no fatter rung to ask for.**
  `list_projects`, `list_messages`, `list_meetings`, `list_payments`,
  `list_tasks` and `list_active_sessions` return hand-built rows rather than the
  upstream payload. `list_messages` in particular returns compact cards with a
  240-character `preview` and **no body** — `get_message` is the way to the full
  text, not a `view` value.
- **It does not return a record at all.** `sign_contract`, `pay_invoice`,
  `use_magic_link` and `use_flow_link` answer with prose, a deep link, or a
  capture receipt.

One last mechanical note: `raw` comes back **indented**, while `compact` is
minified. That is deliberate — `raw` is the rung a person reads when a payload
is not what they expected, and indentation is most of what makes an unfamiliar
shape legible.

## Workflows

- **First time** → user pastes magic-link URL from vendor email → `use_magic_link` → session captured
- **"Fill in / read the vendor's questionnaire"** → user pastes the `/flow/<id>?hash=…` link → `use_flow_link` → `get_flow`
- **"What contracts haven't I signed?"** → `list_workspace_files` with `file_type=agreement`, filter by `is_file_accepted=false`
- **"Summarize my HB status with Silk Veil"** → `get_workspace` (status flags) + `list_workspace_files`
- **"Send me a link to sign the photographer's contract"** → `list_workspace_files` → `sign_contract` (confirm when prompted)
- **"Which invoices are overdue?"** → `list_workspace_files` with `file_type=invoice`, sort by due date
- **"What did the planner send me?" / "Read me the latest checklist"** → `list_projects` → `list_messages` → `get_message`
- **"Reply to Ivy and ask about the rehearsal"** → `list_messages` (find the message) → `send_message` with `reply_to_message_id` → show the user the preview → once they approve, re-run with the same arguments plus the returned `confirmToken` (on a client that shows a confirmation prompt, the prompt replaces these two steps, unless the server sets `MCP_CONFIRM_ELICITATION=off`)
- **"When is my next Zoom with the planner?"** → `list_meetings`; the join link and password are in the row
- **"What have I paid and what's left?"** → `list_payments` (`totals.paid` / `totals.unpaid`); to pay one, `pay_invoice`
- **"Do I have anything to do?"** → `list_tasks` (`counts.overdue`, `counts.today`)

## In context groups

On an mcp-host that groups tools by context, this server is in the **money**
group. Its one canonical read is `list_payments` for **what's due**: the subject
is the project (`workspace_id`), whose schema lists your projects by name —
listed once at start from every captured portal session, so a fresh install or
a lapsed session publishes no names and the tool still takes a workspace id —
and `view: "brief"` answers `<file>: <payment> (<amount>) — <ISO date | no date>
— <paid|pending|overdue|unpaid>` per payment, inside the untrusted-data
envelope as `data: string[]` (the titles are the vendor's text), or the single
note line `-- none` when there is no payment. Nothing here is canonical for what's new or
what's on: `list_messages` (new) and `list_meetings` (on) carry those intents
but need a workspace and are read on request. A compound ask looks like "what
do I still owe the vendors, and anything due at school?" — the money group
answers the payments, the school group the rest. Reads go straight to
api.honeybook.com from the saved session, so the browser only has to be open
to capture one (`use_magic_link`); a missing or lapsed session is answered as
"run `use_magic_link` again", not "needs your browser open".

## Notes

- Each vendor = separate session keyed by portal origin (e.g. `https://acme.hbportal.co`)
- Sessions cached in `~/.honeybook-mcp/sessions.json` (mode 0600)
- **Two credential kinds, not interchangeable.** A portal session reads workspaces/files/invoices; a flow credential is HoneyBook's "weak auth", scoped to ONE questionnaire, cached separately in `~/.honeybook-mcp/flows.json`. A portal tool refuses a flow credential by name rather than failing upstream
- The flow storage key contains the flow id, so the ContextMint Bridge extension asks to re-approve the scope once per new questionnaire
- Write tools (`sign_contract`, `pay_invoice`) return deep links in v2
- Session expires → re-run `use_magic_link` with a fresh URL from the vendor's email
- `send_message` goes out as a real HoneyBook email to everyone in the workspace (the vendor and any co-clients). Always show the user the preview and get their explicit approval before passing the `confirmToken` back — never reuse or invent a token
- `list_messages` / `get_message` read the same feed the Activity tab renders and do not mark items seen; `unseen_count` counts messages from other people you have not opened
