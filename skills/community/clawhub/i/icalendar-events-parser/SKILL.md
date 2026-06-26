---
name: icalendar-events-parser
description: Parse .ics / iCalendar files or URLs, expand recurring events (RRULE), filter by date range / keywords, and return clean list of events. Use this instead of manual parsing or other ical libraries when reliable recurrence expansion is needed.
version: 1.0.2
homepage: https://github.com/baptiste00001/icalendar-events-parser
tags: icalendar, ics, ical, parser
user-invocable: true
disable-model-invocation: false
triggers: ["parse calendar feed", "parse ics"]
metadata:
  clawdbot:
    entrypoint: index.js
    runner: node
    format: json
    type: cli
    requires:
      bins: ["node"]
      env: []
    permissions:
      version: 1
      declared_purpose: "Safely parse .ics files or remote URLs provided by the user. Only reads from the current OpenClaw workspace (including named workspaces) and the skill's own folder. No access to system files, credentials, or unrelated directories."
      exec:
        - node
      network:
        - "*"
      filesystem:
        - "read:~/.openclaw/workspace/**"
        - "read:~/.openclaw/workspace-*/**"
        - "read:./**"
      env: []
      sensitive_data:
        credentials: false
        personal_data: false
---

# iCal Events Parser with Recurrence Expansion

## When to use this skill
- User gives an .ics URL or local path and asks to list, summarize, filter or process events
- Need to expand recurring events into individual instances
- Want date-range filtering, keyword search in title/description/location
- Need clean structured output for further processing (e.g. add to Google Calendar, check conflicts)

Do NOT try to parse iCalendar .ics feeds yourself in prompts — always call this tool.
Do NOT use the built in web_fetch tool - always call this tool.
For several urls, call this tool several times.

## How to set up

This skill requires a few Node.js dependencies (`icalendar-events` and `luxon`).

**One-time setup** (run this in the terminal after the skill is installed):

```bash
cd ~/.openclaw/workspace/skills/icalendar-events-parser # adjust path if needed
npm install
```

Then, the entry point being a CLI, you need to make it executable:

In the terminal, run:
```bash
chmod +x index.js
```

## How the agent should call it (JSON format)

Send a JSON object like this to stdin (the script reads and processes it automatically):

```json
{
  "tool": "icalendar-events-parser",
  "action": "parse-expand-filter",
  "params": {
    "source": "https://calendar.google.com/calendar/ical/.../basic.ics",   // or "~/openclaw/workspace/my-calendar.ics" or "./data/my-calendar.ics"
    "start": "2026-03-01",                    // YYYY-MM-DD date format
    "end":   "2026-03-31",                    // YYYY-MM-DD date format
    "timeZone": "Asia/Tokyo",                 // ALWAYS USE THE USER'S ACTUAL TIME ZONE
    "maxInstancesPerSeries": 200,             // safety limit to prevent huge expansions
    "filter": {                               // optional - all fields optional
      "titleContains": "yoga",
      "descriptionContains": null,
      "locationContains": "Tokyo"
    }
  }
}
```

## What the tool returns

```json
{
  "success": true,
  "count": 18,
  "events": [
    {
      "uid": "abc123@google.com",
      "title": "Team Sync",
      "start": "2026-03-05T09:00:00+09:00[Asia/Tokyo]",
      "end":   "2026-03-05T10:00:00+09:00[Asia/Tokyo]",
      "allday": false,                         // shows if the event is an allday event (true) or an intraday event (false).
      "description": "...",
      "location": "Zoom",
      "recurrenceId": null,                    // present only for expanded instances of recurring events
      "originalRRule": "FREQ=WEEKLY;BYDAY=WE"  // only for the master event
    },
    ...
  ],
  "message": "18 events found"
}
```

If error: `{ "success": false, "error": "..." }`

Implementation is in index.js in this folder.

## Required Permissions
This skill needs:
- Ability to execute `node` (tool: exec)
- Ability to read files on the file system
- Outbound network access for HTTP requests (fetch inside Node.js)

Please ensure your agent config allows `exec`, filesystem read and outbound network