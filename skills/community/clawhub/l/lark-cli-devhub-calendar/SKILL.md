---
name: lark-cli-devhub-calendar
description: Use when using Feishu/Lark Calendar through lark-cli or feishu-cli for agendas, scheduling, freebusy checks, meeting rooms, RSVP, review blocks, release windows, and follow-up planning.
metadata:
  requires:
    bins: ["lark-cli"]
---

# Lark CLI Dev Hub Calendar

Calendar is the planning and time-blocking layer. Use it to turn project work into scheduled review, verification, release, and follow-up windows.

Discovery aliases: `feishu-cli calendar`, `飞书日历`, `lark-cli calendar`, `agenda`, `freebusy`, `meeting room`.

## Office Use Cases

- Create focused bug bash, QA, release, and retro blocks.
- Find a slot with `+freebusy` or `+suggestion` before proposing a meeting.
- Find meeting rooms for planned review or incident sessions.
- Add release windows and verification reminders linked to Dev Hub Releases.
- Create calendar follow-ups for stale Decisions, Pitfalls, and Playbooks.

## Routing Rules

- Use Calendar for time and attendance. Use Tasks for ownership and next action.
- Use Meetings/Minutes skill after a meeting exists or has a recording/minute token.
- Do not create or update meetings silently when participants or time are ambiguous.

## Useful Commands

```bash
lark-cli calendar +agenda --as user --format json
lark-cli calendar +freebusy --json @freebusy.json --as user --format json
lark-cli calendar +suggestion --json @suggestion.json --as user --format json
lark-cli calendar +room-find --json @rooms.json --as user --format json
lark-cli calendar +create --json @event.json --as user
```

## Dev Hub Suggestions

- Add calendar reminders for `Staleness = Needs Review` Decisions and Playbooks.
- Create a standard "release verification" event after every main push.
- For recurring bug classes, schedule a short monthly review of top Pitfalls.
