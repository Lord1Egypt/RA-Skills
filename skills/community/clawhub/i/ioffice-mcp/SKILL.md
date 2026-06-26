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
| `io_list_buildings` | List buildings with optional search, pagination, and sorting |
| `io_get_building(id)` | Get a single building by ID |
| `io_create_building(name, address1?, city?, ...)` | Create a new building |
| `io_update_building(id, ...)` | Update a building — only provide fields to change |
| `io_delete_building(id)` | Delete a building |

### Floors
| Tool | Description |
|------|-------------|
| `io_list_floors(buildingId?)` | List floors, optionally filtered by building |
| `io_get_floor(id)` | Get a single floor by ID |
| `io_create_floor(name, buildingId, ...)` | Create a floor within a building |
| `io_update_floor(id, ...)` | Update a floor |
| `io_delete_floor(id)` | Delete a floor |

### Spaces
| Tool | Description |
|------|-------------|
| `io_list_spaces(floorId?)` | List spaces/rooms, optionally filtered by floor |
| `io_get_space(id)` | Get a single space by ID |
| `io_create_space(name, floorId, capacity?, ...)` | Create a space on a floor |
| `io_update_space(id, ...)` | Update a space |
| `io_delete_space(id)` | Delete a space |

### Users
| Tool | Description |
|------|-------------|
| `io_list_users(search?)` | List users with optional search |
| `io_get_user(id)` | Get a single user by ID |
| `io_create_user(firstName, lastName, email, ...)` | Create a new user |
| `io_update_user(id, ...)` | Update a user |
| `io_delete_user(id)` | Delete a user |

### Reservations
| Tool | Description |
|------|-------------|
| `io_list_reservations(spaceId?, userId?, startDate?, endDate?)` | List reservations with optional filters |
| `io_get_reservation(id)` | Get a single reservation by ID |
| `io_create_reservation(title, spaceId, startDate, endDate, ...)` | Reserve a space |
| `io_update_reservation(id, ...)` | Update a reservation |
| `io_delete_reservation(id)` | Cancel/delete a reservation |
| `io_checkin_reservation(id)` | Check in to a reservation, confirming room usage |
| `io_checkout_reservation(id)` | Check out early, releasing the room |

### Visitors
| Tool | Description |
|------|-------------|
| `io_list_visitors(buildingId?, startDate?, endDate?)` | List visitors with optional filters |
| `io_get_visitor(id)` | Get a single visitor record by ID |
| `io_create_visitor(firstName, lastName, hostId?, expectedArrival?, ...)` | Pre-register a visitor |
| `io_update_visitor(id, ...)` | Update a visitor record |
| `io_checkin_visitor(id)` | Check in a visitor upon arrival |
| `io_checkout_visitor(id)` | Check out a visitor upon departure |

### Maintenance Requests
| Tool | Description |
|------|-------------|
| `io_list_maintenance_requests(status?, spaceId?, buildingId?)` | List maintenance requests |
| `io_get_maintenance_request(id)` | Get a single maintenance request |
| `io_create_maintenance_request(title, spaceId?, buildingId?, ...)` | File a new maintenance request |
| `io_update_maintenance_request(id, ...)` | Update a maintenance request |
| `io_accept_maintenance_request(id)` | Accept a pending request (pending → accepted) |
| `io_start_maintenance_request(id)` | Start work (accepted → in-progress) |
| `io_complete_maintenance_request(id, resolution?)` | Mark as complete |
| `io_archive_maintenance_request(id)` | Archive a completed request |

### Moves
| Tool | Description |
|------|-------------|
| `io_list_moves(status?, buildingId?)` | List move requests |
| `io_get_move(id)` | Get a single move request |
| `io_create_move(name, fromSpaceId?, toSpaceId?, scheduledDate?, ...)` | Create a move request |
| `io_update_move(id, ...)` | Update a move request |
| `io_approve_move(id, notes?)` | Approve a move request |
| `io_cancel_move(id, reason?)` | Cancel a move request |

### Mail
| Tool | Description |
|------|-------------|
| `io_list_mail(status?, recipientId?, buildingId?)` | List mail items (packages and letters) |
| `io_get_mail(id)` | Get a single mail item |
| `io_create_mail(recipientId, buildingId, carrier?, trackingNumber?, ...)` | Log a received mail item |
| `io_deliver_mail(id, deliveredDate?, signature?)` | Mark a mail item as delivered |
| `io_return_mail(id, reason?)` | Mark a mail item as returned to sender |

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
