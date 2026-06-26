---
name: ics-generator
description: Generates Google Calendar‑compatible .ics files from structured event data.
---

# ics‑generator

## When to use
When you need to convert a schedule, study plan, or task list into an **iCalendar (.ics)** file that can be imported into Google Calendar or any other iCalendar‑compatible client.

## Workflow Overview
1. **Collect structured events** – each event must contain:
   - `summary` (string)  
   - `description` (string, optional)  
   - `start` (ISO‑8601 date/time or JS `Date`)  
   - `end`   (ISO‑8601 date/time or JS `Date`)  
   - `colorId` (Google Calendar colour ID, optional)  

2. **Chunking / sequential dates**  
   - **First chunk** – supply the intended start date (e.g., `2026‑05‑31T09:00:00Z`).  
   - **Subsequent chunks** – pass the **last date of the previous chunk** (via the `lastDate` field). The skill will automatically shift the next chunk’s start date forward by one day, guaranteeing a clean “one‑day‑gap” between chunks.

3. **Run the skill** – invoke the `run` function exported by `index.js` with the event array and optional `lastDate`.

## Implementation Notes
| Feature | Details |
|---------|---------|
| **Google‑Calendar compatibility** | Automatically injects the required headers:<br>`PRODID:-//Google Inc//Google Calendar 70.6//EN` <br>`CALSCALE:GREGORIAN` |
| **UTC enforcement** | All start/end times are normalized to **UTC** and formatted as `YYYYMMDDTHHMMSSZ`. Google Calendar accepts this exact format without further conversion. |
| **Unique identifiers** | Each event receives a UUID‑v4‑derived UID (`event-<uuid>`) so calendar clients can correctly sync updates. |
| **Color handling** | If a `colorId` is supplied, it’s added as `X‑GOOGLE‑CALENDAR‑COLOR:<id>` inside the VEVENT block. |
| **Output** | Returns a complete `.ics` string wrapped in `BEGIN:VCALENDAR … END:VCALENDAR`. Every `VEVENT` ends with `END:VEVENT` and the final block ends with `END:VCALENDAR`. |
| **Dependencies** | Node ≥ 20 (for `crypto.randomUUID()`). No external npm packages—pure JavaScript plus Node’s built‑in `crypto` module. |
| **License** | MIT – free to copy, modify, and share. |

### Why the specific `PRODID` / `CALSCALE`?
From community feedback, Google Calendar only imported the generated file **when** those exact values were present. A generic `PRODID` caused the “Unable to launch event” error; `CALSCALE:GREGORIAN` tells Google Calendar which calendar system to assume (Gregorian), which is required for proper time‑zone handling.