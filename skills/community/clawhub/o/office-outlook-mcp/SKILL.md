---
name: outlook-fpx
description: Read and act on the user's Outlook / Microsoft 365 mailbox — mail, folders, calendar, contacts, tasks — via the Outlook REST API, using a bearer token lifted from their signed-in browser tab. Use when asked about their Outlook email, calendar or meetings.
---

# Outlook (Microsoft 365) access

Talks to `https://outlook.office.com/api/v2.0` with a bearer token captured
from the signed-in Outlook Web tab. **The browser is needed only to mint the
token** (~25h lifetime) — every actual request is a plain server-side `curl`.

## Setup (once)

```sh
npm i -g @fetchproxy/cli                      # provides `fpx`
fpx profile add outlook --domain outlook.cloud.microsoft
fpx profile declare outlook \
  --capture-header authorization@outlook.cloud.microsoft \
  --allow-download
```

Declare **one** host, the one your signed-in Outlook tab is on. A tenant still
on the legacy app uses `outlook.office.com` in both lines and exports
`OUTLOOK_CAPTURE_HOST=outlook.office.com`. Don't declare both: the bridge opens a
background tab for every declared domain with no tab open, and because a
signed-in `outlook.office.com` tab redirects to `outlook.cloud.microsoft`, it
opens another one on every capture.

Declare **all** scopes before the first pairing — widening them later forces the
user to re-approve. The first `fpx` call prints a 6-digit pair code to approve in
the ContextMint Bridge extension popup; the grant then persists.

Requires the **ContextMint Bridge** extension, from
https://github.com/nullnet-app/contextmint-bridge/releases (Chrome: load the
chrome zip unpacked; Safari is not available yet — it will ship inside the
ContextMint app, which has no public download — so use Chrome for now). It is the fetchproxy extension under its new name,
same maintainer, with public source — build it yourself or verify a release zip
against its `.sha256` (`shasum -a 256 -c <zip>.sha256`). The extension and `fpx`
are compatible by **fetchproxy protocol number** (currently protocol 4), not by
matching package versions. Keep the bridge and `fpx` current — a mismatch fails
with an error naming both protocol numbers.

## Use

```sh
source references/outlook-env.sh
outlook_token_refresh        # once per ~25h; needs an open, signed-in Outlook tab
outlook_get '/me' | jq .
```

- `outlook_get <path> [curl args]` — GET, body on stdout
- `outlook_get_text <path>` — same plus `Prefer: outlook.body-content-type="text"`; **use this for anything you will read** (measured 9.4× smaller than HTML)
- `outlook_post <path> <json>` / `outlook_patch <path> <json>`
- `outlook_token_expiry` — prints time remaining, never the token

Paths are relative to `/api/v2.0`. Exit code **4** means non-2xx; a **401**
prints `run: outlook_token_refresh`.

Common starting points — full verified set, including calendar, contacts, tasks
and write payloads, in **`references/api-recipes.md`**:

```sh
outlook_get '/me/mailfolders/inbox?$select=UnreadItemCount,TotalItemCount'
outlook_get '/me/mailfolders/inbox/messages?$top=20&$orderby=ReceivedDateTime%20desc&$select=Id,Subject,From,ReceivedDateTime,IsRead'
outlook_get '/me/calendarview?startDateTime=2026-09-20T00:00:00Z&endDateTime=2026-09-27T00:00:00Z&$select=Subject,Start,End,Location'
```

## Rules that bite

- **Fields are PascalCase** (`ReceivedDateTime`, `IsRead`). This is the Outlook
  REST API, *not* Graph — a camelCase Graph snippet silently returns nothing.
- **Always pass `$select`.** The default projection is ~40 fields per message
  including the full body.
- **`$search` and `$filter` cannot be combined.**
- **`/me/events` does not expand recurring series** — use `/me/calendarview`
  with a start/end window for "what's on my schedule".
- **`Prefer: outlook.timezone` takes Windows zone names** (`Eastern Standard
  Time`), not IANA (`America/New_York`).
- **`@odata.nextLink` is an absolute URL** — pass it to `curl -K ~/.outlook-fpx/curlrc`
  directly, not to `outlook_get`, which would prefix the base again.
- **`/owa/0/service.svc` is not this API** and returns 500. Use `/api/v2.0`.
- **A 2xx is not proof a write persisted** — re-read the resource to confirm.
- Never name a shell local `path` or `status`: in zsh `path` is tied to `PATH`
  (assigning it wipes `PATH` mid-function) and `status` is read-only. Both are
  harmless in bash, so this only breaks for zsh users.

## In context groups

When the office-outlook-mcp server is hosted on mcp-host, its tools join the
**work** group (`_meta.mint.domain: "work"`). The group's canonical reads,
each answered with `view: "brief"` (one line per item,
`title — <ISO date | no date> — <status>`, returned inside the
untrusted-content envelope as `data: string[]` because the text is other
people's; a line starting `-- ` is a note — `-- none` answers an empty page,
and a final `-- more` says Outlook has another page, so re-ask without
`brief` for the `nextLink`; a title starting `-- ` or `\` is escaped with one
leading `\`). `brief` is additive: on
`outlook_list_events` and `outlook_list_tasks` it joins the existing
`compact | full | raw` values, and `outlook_list_unread_messages` takes a
new optional `view` whose only value is `brief`:

- **what's new** → `outlook_list_unread_messages` (unread mail in the inbox,
  newest first; status `unread` or the meeting-message kind).
- **what's on** → `outlook_list_events`, with the asked range filled into
  `start`/`end` (status `cancelled` or your response).
- **what's due** → `outlook_list_tasks` (status the task's own).

None takes a subject: one signed-in mailbox, nothing to fan out over. A
compound ask — "what's on my calendar tomorrow, and anything new at work?" —
is one `whats-on` call over tomorrow plus one `whats-new` call, merged with
the other work-group sources. The server reaches Outlook with a bearer token
lifted from the browser; while that token is missing or expired and no
signed-in Outlook tab is open, the group answers that Outlook needs your
browser open rather than reading nothing.

## Privacy

This reads the user's real mailbox. Surface only what was asked for; do not dump
message bodies, recipients or attachments into the transcript incidentally. The
token lives in `~/.outlook-fpx/curlrc` (0600, its own directory — deliberately
not shared with any MCP's state) and is passed to `curl` via `-K` so it never
appears in `argv` or `ps` output.
