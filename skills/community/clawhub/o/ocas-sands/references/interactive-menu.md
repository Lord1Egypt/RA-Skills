# Interactive Menu

When invoked interactively (via `/` command), present a two-level menu using the `clarify` tool so the user can pick which function to run.

**Level 1 — Category selection** (max 4 choices):

```python
result = clarify(
    question="What would you like to do?",
    choices=[
        "Events — query, create, modify, or delete calendar events",
        "Schedule — find free slots, detect conflicts, calculate travel time",
        "Briefings — generate morning/evening briefings",
        "Status — show system status",
    ]
)
```

**Level 2 — Action selection** based on Level 1 choice:

- **Events** → clarify with choices: "calendar.query — Query calendar events", "event.create — Create a calendar event", "event.modify — Modify an event", "event.delete — Delete an event"
- **Schedule** → clarify with choices: "schedule.free — Find free time slots", "schedule.conflicts — Detect scheduling conflicts", "logistics.travel — Calculate travel time"
- **Briefings** → run "briefing.generate — Generate briefing" directly (single action — no sub-menu needed)
- **Status** → run "status — Show system status" directly (single action — no sub-menu needed)

After the user selects an action, execute it following the relevant procedure in this skill. Loop back to the menu after each action completes, until the user chooses to exit or sends `/stop`.

### Response parsing

Match the user's response against the full choice string. Extract the action key by splitting on `" — "` and taking the first segment. If the response doesn't match any known choice (user typed free-form via "Other"), match key prefixes case-insensitively. Re-present the current menu level on no match.

### Platform adaptation

On CLI, choices are navigable with arrow keys. On messaging platforms, choices render as a numbered list. The two-level hierarchy ensures no more than 4 options appear at any level on any platform.
