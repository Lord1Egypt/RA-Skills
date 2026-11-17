# Outlook REST v2.0 — verified request shapes

Every endpoint and header below was executed live against a real TransUnion
M365 mailbox on 2026-09-20 and returned the status shown. Nothing here is
inferred from documentation.

Base: `https://outlook.office.com/api/v2.0`
Auth: `Authorization: Bearer <token>` (see SKILL.md for capture)

> **Fields are PascalCase.** This is the Outlook REST API, not Microsoft Graph.
> `ReceivedDateTime`, `IsRead`, `BodyPreview` — not `receivedDateTime`. Copying a
> Graph snippet here silently returns nothing useful.

---

## Identity

```sh
outlook_get '/me' | jq '{EmailAddress, DisplayName, Alias, MailboxGuid}'
```
Returns `Id, EmailAddress, DisplayName, Alias, MailboxGuid`. Cheapest liveness check.

---

## Mail

### Folders

```sh
outlook_get '/me/mailfolders?$top=50' | jq -r '.value[] | "\(.UnreadItemCount)/\(.TotalItemCount)\t\(.DisplayName)"'
```

Item keys: `Id, DisplayName, ParentFolderId, ChildFolderCount, UnreadItemCount,
TotalItemCount, SizeInBytes, IsHidden`.

Well-known names usable in place of an id — all verified present:
`inbox`, `drafts`, `sentitems`, `deleteditems`, `archive`, `junkemail`,
`outbox`, `clutter`.

```sh
outlook_get '/me/mailfolders/inbox?$select=UnreadItemCount,TotalItemCount' | jq .
```

### Listing messages

Always pass `$select` — the default projection returns ~40 fields per message
including full `Body`, which is enormous on a 13k-message folder.

```sh
outlook_get '/me/mailfolders/inbox/messages?$top=20&$orderby=ReceivedDateTime%20desc&$select=Id,Subject,From,ReceivedDateTime,IsRead,HasAttachments' \
  | jq -r '.value[] | "\(.ReceivedDateTime)  \(if .IsRead then " " else "•" end)  \(.From.EmailAddress.Name // "?")\t\(.Subject)"'
```

Unread only:
```sh
outlook_get '/me/mailfolders/inbox/messages?$filter=IsRead%20eq%20false&$top=25&$select=Id,Subject,From,ReceivedDateTime'
```

Full-text search (`$search` and `$filter` cannot be combined):
```sh
outlook_get '/me/messages?$search=%22quarterly%20report%22&$top=10&$select=Id,Subject,From,ReceivedDateTime'
```

Verified query options: `$top`, `$skip`, `$select`, `$filter`, `$orderby`,
`$search`, `$count`. Paging: follow `@odata.nextLink` (absolute URL — pass it to
`curl` directly, not through `outlook_get`, which prefixes the base).

### Reading one message

```sh
outlook_get_text "/me/messages/$ID" | jq '{Subject, From, ReceivedDateTime, Body: .Body.Content}'
```

`outlook_get_text` sends `Prefer: outlook.body-content-type="text"`. Measured on
a real message: **7,299 bytes HTML → 775 bytes text (9.4×)**; across a 5-message
collection 37,638 → 12,828 bytes. Use it for anything an agent will read.

Without the header the API returns whatever the message was authored in, so a
collection comes back with a *mix* of `HTML` and `Text` — the `Prefer` header
normalises all of them to `Text`.

### Attachments

```sh
outlook_get "/me/messages/$ID/attachments?\$select=Id,Name,Size,ContentType" \
  | jq -r '.value[] | "\(.Size)\t\(.ContentType)\t\(.Name)"'
```
Item keys: `@odata.type, @odata.mediaContentType, Id, Name, ContentType, Size`.
Content bytes come back base64 in `ContentBytes` when `$select` does not exclude
it; omit `$select` to get it, and expect the response to be ~1.37× the file size.

---

## Calendar

```sh
# events in a window — expands recurrences, which /me/events does NOT
outlook_get '/me/calendarview?startDateTime=2026-09-20T00:00:00Z&endDateTime=2026-09-27T00:00:00Z&$select=Subject,Start,End,Location,Organizer&$orderby=Start/DateTime' \
  -H 'Prefer: outlook.timezone="Eastern Standard Time"' \
  | jq -r '.value[] | "\(.Start.DateTime)  \(.Subject)"'
```

`Prefer: outlook.timezone="<Windows tz name>"` is verified — `Start.TimeZone`
comes back as the requested zone instead of UTC. Note it takes **Windows**
zone names (`Eastern Standard Time`), not IANA (`America/New_York`).

`/me/calendars` lists calendars; `/me/events` lists events **without** expanding
recurring series, so prefer `/me/calendarview` for "what's on my schedule".

---

## Contacts, tasks, people

```sh
outlook_get '/me/contacts?$top=20&$select=DisplayName,EmailAddresses,CompanyName'
outlook_get '/me/tasks?$top=20&$select=Subject,Status,DueDateTime'
outlook_get '/me/people?$top=20&$select=DisplayName,ScoredEmailAddresses'   # relevance-ranked
outlook_get '/me/MailboxSettings'                                            # tz, working hours, auto-reply
```

---

## Writes

All four routes were confirmed to exist and be authorised by POSTing a
deliberately invalid body and receiving **400** (`UnableToDeserializePostBody` /
`RequestBodyRead`) rather than 401/403/404. **The payloads below are shapes, not
executed calls** — no mail was sent and nothing was mutated during the build.
Verify the body of any write by re-reading the resource afterwards; a 2xx is not
proof it persisted.

```sh
# send mail
outlook_post '/me/sendmail' '{
  "Message": {
    "Subject": "…",
    "Body": {"ContentType": "Text", "Content": "…"},
    "ToRecipients": [{"EmailAddress": {"Address": "someone@example.com"}}]
  },
  "SaveToSentItems": true
}'

# mark read  /  move  /  create draft  /  create event
outlook_patch "/me/messages/$ID" '{"IsRead": true}'
outlook_post  "/me/messages/$ID/move" '{"DestinationId": "archive"}'
outlook_post  '/me/messages' '{"Subject":"…","Body":{"ContentType":"Text","Content":"…"},"ToRecipients":[…]}'
outlook_post  '/me/events'   '{"Subject":"…","Start":{"DateTime":"2026-09-22T15:00:00","TimeZone":"Eastern Standard Time"},"End":{…}}'
```

Send only to `@example.com` when testing.

---

## Errors

| Signal | Meaning |
|---|---|
| `401`, **empty body**, `WWW-Authenticate: Bearer client_id="00000002-0000-0ff1-ce00-000000000000"` | token expired or revoked → `outlook_token_refresh` |
| `400` + `error.code` (`UnableToDeserializePostBody`, `RequestBodyRead`) | route exists, payload is wrong |
| `404` | wrong id or path — *not* an auth problem |
| `500` on `/owa/0/service.svc` | that is the OWA internal endpoint; it is **not** part of this API. Use `/api/v2.0`. |

`outlook_get` returns rc `4` for any non-2xx and prints the status to stderr.
