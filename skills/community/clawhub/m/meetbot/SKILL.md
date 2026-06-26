---
name: meetbot
description: Schedule and book meetings using the Meet.bot MCP server (mcp.meet.bot). Use when the user wants to check calendar availability, find open time slots, book a meeting with a guest, get a shareable booking link, or list their Meet.bot scheduling pages. Requires a Meet.bot API key as a Bearer token.
---

# Meet.bot

Connect to the Meet.bot MCP server at `https://mcp.meet.bot` using a Bearer token.

## Auth
Every tool call requires `Authorization: Bearer <api-key>` in the HTTP header. If not configured, the server returns a clear error explaining this. Ask the user for their Meet.bot API key before proceeding.

## Tools

| Tool | Purpose |
|------|---------|
| `get_scheduling_pages` | List all the user's scheduling pages |
| `get_page_info` | Get details about a specific page by URL |
| `get_available_slots` | Find open time slots for a page |
| `book_meeting` | Book a slot (requires page, guest_email, guest_name, start) |
| `health_check` | Verify the API key is valid |

## Workflows

### Check availability
1. `get_scheduling_pages` to list pages (or use URL directly if known)
2. `get_available_slots` with the page URL, date range, and user's timezone
3. Present slots in readable local time — not raw ISO strings

### Book a meeting
1. Confirm page URL, guest name, guest email, and start time with the user
2. `book_meeting` — start time must be ISO 8601 (e.g. `2026-03-10T14:00:00Z`)
3. Confirm the booking details back to the user

### Share a booking link
1. `get_available_slots` with `booking_link: true`
2. Return the first 3–5 `booking_link` URLs for the guest to self-select

## Tips
- Pages with "archived" in the URL are inactive — skip them
- Always confirm before calling `book_meeting` — bookings cannot be cancelled via this server
- `get_available_slots` supports `count`, `start`, `end` (YYYY-MM-DD), and `timezone` (IANA)
