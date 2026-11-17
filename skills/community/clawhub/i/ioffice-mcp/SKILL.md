---
name: ioffice-mcp
description: Access iOffice workspace and facility data via MCP. Use when the user asks about iOffice buildings, floors, spaces, reservations, visitors, maintenance requests, moves, or mail. Triggers on phrases like "book a room in iOffice", "check who's visiting today", "file a maintenance request", "log a package", "schedule a move", or any request involving workplace management in iOffice. Requires ioffice-mcp installed and the ioffice server registered (see Setup below).
---

# ioffice-mcp

MCP server for iOffice — natural-language workspace and facility management via the iOffice API.

- **npm:** [npmjs.com/package/ioffice-mcp](https://www.npmjs.com/package/ioffice-mcp)
- **Source:** [github.com/chrischall/ioffice-mcp](https://github.com/chrischall/ioffice-mcp)

## Setup

### Option A — npx (recommended)

Add to `.mcp.json` in your project or `~/.claude/mcp.json`:

```json
{
  "mcpServers": {
    "ioffice": {
      "command": "npx",
      "args": ["-y", "ioffice-mcp"],
      "env": {
        "IOFFICE_HOST": "your-tenant.ioffice.com",
        "IOFFICE_TOKEN": "your-token-here"
      }
    }
  }
}
```

### Option B — from source

```bash
git clone https://github.com/chrischall/ioffice-mcp
cd ioffice-mcp
npm install && npm run build
```

Then add to `.mcp.json`:

```json
{
  "mcpServers": {
    "ioffice": {
      "command": "node",
      "args": ["/path/to/ioffice-mcp/dist/index.js"],
      "env": {
        "IOFFICE_HOST": "your-tenant.ioffice.com",
        "IOFFICE_TOKEN": "your-token-here"
      }
    }
  }
}
```

Or use a `.env` file in the project directory with `IOFFICE_HOST` and `IOFFICE_TOKEN`.

## Authentication

Token auth (preferred) — set `IOFFICE_TOKEN`. Alternatively, set `IOFFICE_USERNAME` + `IOFFICE_PASSWORD`. If both are present, the token takes precedence.

## Tools

### Buildings
| Tool | Description |
|------|-------------|
| `io_list_buildings(view?)` | List buildings with optional search, pagination, and sorting |
| `io_get_building(id, view?)` | Get a single building by ID |
| `io_create_building(name, address1?, city?, ...)` | Create a new building |
| `io_update_building(id, ...)` | Update a building — only provide fields to change |
| `io_delete_building(id)` | Delete a building |

### Floors
| Tool | Description |
|------|-------------|
| `io_list_floors(buildingId?, view?)` | List floors, optionally filtered by building |
| `io_get_floor(id, view?)` | Get a single floor by ID |
| `io_create_floor(name, buildingId, ...)` | Create a floor within a building |
| `io_update_floor(id, ...)` | Update a floor |
| `io_delete_floor(id)` | Delete a floor |

### Spaces
| Tool | Description |
|------|-------------|
| `io_list_spaces(floorId?, view?)` | List spaces/rooms, optionally filtered by floor |
| `io_get_space(id, view?)` | Get a single space by ID |
| `io_create_space(name, floorId, capacity?, ...)` | Create a space on a floor |
| `io_update_space(id, ...)` | Update a space |
| `io_delete_space(id)` | Delete a space |

### Users
| Tool | Description |
|------|-------------|
| `io_list_users(search?, view?)` | List users with optional search |
| `io_get_user(id, view?)` | Get a single user by ID |
| `io_create_user(firstName, lastName, email, ...)` | Create a new user |
| `io_update_user(id, ...)` | Update a user |
| `io_delete_user(id)` | Delete a user |

### Reservations
| Tool | Description |
|------|-------------|
| `io_list_reservations(spaceId?, userId?, startDate?, endDate?, view?)` | List reservations with optional filters |
| `io_get_reservation(id, view?)` | Get a single reservation by ID |
| `io_create_reservation(title, spaceId, startDate, endDate, ...)` | Reserve a space |
| `io_update_reservation(id, ...)` | Update a reservation |
| `io_delete_reservation(id)` | Cancel/delete a reservation |
| `io_checkin_reservation(id)` | Check in to a reservation, confirming room usage |
| `io_checkout_reservation(id)` | Check out early, releasing the room |

### Visitors
| Tool | Description |
|------|-------------|
| `io_list_visitors(buildingId?, startDate?, endDate?, view?)` | List visitors with optional filters |
| `io_get_visitor(id, view?)` | Get a single visitor record by ID |
| `io_create_visitor(firstName, lastName, hostId?, expectedArrival?, ...)` | Pre-register a visitor |
| `io_update_visitor(id, ...)` | Update a visitor record |
| `io_checkin_visitor(id)` | Check in a visitor upon arrival |
| `io_checkout_visitor(id)` | Check out a visitor upon departure |

### Maintenance Requests
| Tool | Description |
|------|-------------|
| `io_list_maintenance_requests(status?, spaceId?, buildingId?, view?)` | List maintenance requests |
| `io_get_maintenance_request(id, view?)` | Get a single maintenance request |
| `io_create_maintenance_request(title, spaceId?, buildingId?, ...)` | File a new maintenance request |
| `io_update_maintenance_request(id, ...)` | Update a maintenance request |
| `io_accept_maintenance_request(id)` | Accept a pending request (pending → accepted) |
| `io_start_maintenance_request(id)` | Start work (accepted → in-progress) |
| `io_complete_maintenance_request(id, resolution?)` | Mark as complete |
| `io_archive_maintenance_request(id)` | Archive a completed request |

### Moves
| Tool | Description |
|------|-------------|
| `io_list_moves(status?, buildingId?, view?)` | List move requests |
| `io_get_move(id, view?)` | Get a single move request |
| `io_create_move(name, fromSpaceId?, toSpaceId?, scheduledDate?, ...)` | Create a move request |
| `io_update_move(id, ...)` | Update a move request |
| `io_approve_move(id, notes?)` | Approve a move request |
| `io_cancel_move(id, reason?)` | Cancel a move request |

### Mail
| Tool | Description |
|------|-------------|
| `io_list_mail(status?, recipientId?, buildingId?, view?)` | List mail items (packages and letters) |
| `io_get_mail(id, view?)` | Get a single mail item |
| `io_create_mail(recipientId, buildingId, carrier?, trackingNumber?, ...)` | Log a received mail item |
| `io_deliver_mail(id, deliveredDate?, signature?)` | Mark a mail item as delivered |
| `io_return_mail(id, reason?)` | Mark a mail item as returned to sender |

### Health

| Tool | Purpose |
|---|---|
| `io_healthcheck()` | Is this connector working? Reports which credential resolved, whether iOffice accepted it, and what to fix. Start here when any other tool fails — an empty result from a list tool can mean "no data" or "never authenticated", and this separates them. |

## Response shape (`view`)

The 18 read tools — every `io_list_*` and `io_get_*` across the nine resource
groups — take `view: "compact" | "full"`, and **`compact` is the default**: the
parameter is optional, and omitting it gives you the slim shape without asking
for it.

**Compact strips media; it does not project fields.** No hand-written field
list exists here, deliberately. Every read tool hands back iOffice's payload
verbatim, and the repo has no schema, no captured fixture and no live tenant —
so nothing in it could honestly say which of iOffice's fields matter. Stripping
is subtractive and cannot lose a field nobody knew about; an invented field list
would return records with holes in them that read like a verified answer.

Two rules do the stripping, and the second one is the one that will catch you
out:

- **A media-named key goes, whatever it holds** — `avatar`, `picture`, `photo`,
  `thumbnail`, `image`, `icon`, `banner`, `logo`, with an optional qualifier
  (`primary_photo_url`, `coverImage`), an optional `Url`/`Uri`/`Link`/`Src`
  suffix, and plurals. The match is anchored at the *start* of the key, so
  `hasThumbnail: false` and `thumbnailWidth: 200` survive — they are facts about
  a record, not the picture.
- **Any value that is an image URL goes, whatever the key is called** — an
  `http(s)` URL whose *path* ends in `.png`, `.jpg`, `.gif`, `.webp`, `.svg`,
  `.avif`, `.bmp` or `.ico`.

**The surprise, and it matters most on exactly this server: whether your floor
plan survives compact is decided by the file extension, not by the field name.**
`floorPlanUrl` is not a media key, so rule one leaves it alone — but a plan
served as `…/plans/3.png` is dropped by rule two, while the same plan as
`…/plans/3.pdf`, or behind a signed extension-less URL, comes back. The same
goes for `attachmentUrl` and `documentUrl`. If a read comes back without the
image you expected, that is why — ask for `full`.

The strip removes the **key**, recursing through nested objects and arrays, so
on compact `"imageUrl" in space` is `false` rather than null. Everything it does
not remove is byte-identical to `full`.

Pass `view: "full"` when you want the pictures themselves — a visitor badge
photo, a user avatar, a space's floor plan image.

There is **no `raw` rung**: `full` already *is* iOffice's payload untouched, so a
third value could only silently alias one of the other two. `view: "raw"` is a
schema validation error, not a quiet downgrade to compact.

Two of the reads — `io_list_reservations` and `io_list_mail` — also take
`view: "brief"` (see "In context groups" below).

The other 35 tools take no `view`, for two different reasons:

- **The 34 write and action tools** — `io_create_*`, `io_update_*`,
  `io_delete_*`, and the state transitions (check in/out, accept/start/
  complete/archive, approve/cancel, deliver/return) — answer with a receipt, or,
  on a client that cannot show a confirmation prompt (or on any client when the
  server sets `MCP_CONFIRM_ELICITATION=off`), with a preview and a
  `confirmToken` on the first call (nothing is written until the call is
  repeated with that token; an update, delete, cancel or return reads its target
  first so the preview names the record, and an unknown id fails there). There is nothing to strip and every field is load-bearing.
- **`io_healthcheck`** is read-only, but its output is its own verdict — which
  credential resolved, whether iOffice accepted it, what to fix — rather than an
  iOffice record.

## In context groups

This server is a member of the **work** group (mcp-host context groups). Every
tool except `io_healthcheck` carries a `_meta.mint` hint — inert to any other
client.

- **What's on at work** → `io_list_reservations` (canonical `whats-on`): room
  and desk bookings over `startDate`/`endDate`.
- **Anything new at work** → `io_list_mail` (canonical `whats-new`): mail and
  packages logged at the mailroom over `startDate`/`endDate`.
- **What's due** → nothing here answers it: iOffice records carry no due
  dates a person is chasing, so the group asks the other work members.
- **No subjects.** iOffice's listable sets (buildings, floors, spaces, the
  tenant's user directory) are the organisation's, not the person's, so no
  argument publishes a subject enum.

`io_list_visitors` is a non-canonical `whats-on` read; every other read is a
`lookup` and every write is a `change`.

The canonical reads answer `view: "brief"` with one line per item —
`title — <ISO date | no date> — <status>`, at most 120 characters (the whole
line is cut, title first, then the status if it alone would overflow) — inside the
same untrusted-data envelope as every other read (`data` is the list of
lines), because titles are written by other people. A line starting `-- ` is a
note, not an item (an item whose own title starts `-- ` or `\` is escaped
with one more leading `\`, as `\-- …` or `\\…`): `-- none` for an empty
page, `-- N of M shown` when iOffice states a total, `-- more` for a full
page without one, and `-- error: …` when the payload is in a shape the brief view does not read (ask with
`view: "full"`). The field names a line reads are a best reading of iOffice's
payload, not a verified shape; a missing field falls back to the record id,
`no date` or `no status` rather than dropping the item.

A compound ask looks like "what's on at work tomorrow — and any packages for
me?": the group calls `io_list_reservations` with tomorrow's range and
`io_list_mail`, each in `view: "brief"`, and merges the lines with the other
work members' answers.

## Workflows

**Book a meeting room:**
```
io_list_buildings → find building ID
io_list_floors(buildingId) → find floor ID
io_list_spaces(floorId) → pick a room
io_create_reservation(title, spaceId, startDate, endDate)
```

**Pre-register a visitor:**
```
io_list_users(search: "host name") → find hostId
io_create_visitor(firstName, lastName, hostId, buildingId, expectedArrival)
io_checkin_visitor(id) → when they arrive
io_checkout_visitor(id) → when they leave
```

**File and resolve a maintenance request:**
```
io_list_spaces(search: "room name") → find spaceId
io_create_maintenance_request(title, spaceId, buildingId)
io_accept_maintenance_request(id)
io_start_maintenance_request(id)
io_complete_maintenance_request(id, resolution: "Fixed the issue")
```

**Log and deliver a package:**
```
io_list_users(search: "recipient name") → find recipientId
io_create_mail(recipientId, buildingId, carrier: "FedEx", trackingNumber: "...")
io_deliver_mail(id) → when delivered to recipient
```

**Schedule and approve a move:**
```
io_list_spaces → find fromSpaceId and toSpaceId
io_create_move(name, fromSpaceId, toSpaceId, scheduledDate)
io_approve_move(id, notes: "Approved")
```

## Notes

- All dates use ISO 8601 format (e.g. `2026-03-21T09:00:00`)
- All list tools support `search`, `limit` (default 50, max 100), `startAt`, `orderBy`, and `orderByType`
- All `io_list_*` and `io_get_*` tools accept `view` — see [Response shape](#response-shape-view)
- `io_list_floors(buildingId)` and `io_list_spaces(floorId)` use nested API paths when an ID is provided
- Building → Floor → Space is the physical location hierarchy

## Acknowledgement of Terms

By using this MCP server, you acknowledge and agree to the following:

**1. This server accesses your own iOffice / Eptura Workplace tenant.** Auth happens via your own credentials, scoped to the tenant your employer has provisioned for you. It does not — and cannot — access anyone else's organization's data.

**2. [Eptura's Acceptable Use Policy](https://eptura.com/terms/acceptable-use-policy/) governs your use of this server**, just as it governs your direct use of iOffice. (iOffice rebranded to Eptura Workplace in 2023.) The clauses most relevant here:

> Customers may not use any robot, spider, site search/retrieval application or other manual or automatic device to retrieve, index, "scrape," "data mine" or otherwise gather Service content.

And: customers must "identify and authenticate all Users," may not resell or sublicense, must "promptly deactivate access to terminated personnel."

You are agreeing to those terms — read by the maintainer 2026-05-23 — every time you invoke a tool in this server.

**3. Eptura's contract is with your employer, not you.** iOffice / Eptura Workplace is typically licensed by an organization, not by individual employees. Your use of this server is *also* subject to your employer's separate IT/security/acceptable-use policies, which may restrict automation in ways the Eptura AUP doesn't. **Check with your employer's IT before using this server.** Using it without authorization may violate your employment agreement even if Eptura itself doesn't notice.

**4. Personal, single-employee use only.** This project is not affiliated with, endorsed by, sponsored by, or in partnership with Eptura, Inc. It is a personal automation tool for an individual authenticated user to drive their own workplace bookings (reservations, visitors, work orders). Do not use it to bulk-extract floor plans, employee directories, or other workspace data, and do not build a competing workplace product on top of it.

**5. You accept full responsibility** for any consequences of using this server in connection with your iOffice account — rate limiting, session revocation, tenant suspension, your employer's IT calling you, or any other enforcement action. If Eptura or your employer objects to your use, stop using this server.

This section is the maintainer's good-faith summary of the terms — it is not legal advice and does not modify or supersede Eptura's actual AUP, Master Subscription Agreement, or your employer's policies.
