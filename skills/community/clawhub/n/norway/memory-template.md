# Memory Template - Norway

Create `~/norway/memory.md` with this structure:

```markdown
# Norway Trip Memory

## Status
status: ongoing
version: 1.0.0
last: YYYY-MM-DD
integration: pending | complete | paused | never_ask

## Trip Snapshot
- Dates:
- Duration:
- Arrival and departure airports:
- Travelers:
- Kids:
- Mobility notes:

## Route Direction
- Main corridor: [Oslo-west / Bergen-fjords / Stavanger-southwest / Trondheim-central / Lofoten / Tromso-Arctic / Svalbard]
- Confirmed bases:
- Open route questions:
- Ferry tolerance: [low / medium / high]
- Driving comfort: [none / summer only / winter-capable]

## Preferences
- Trip style:
- Budget:
- Pace:
- Food priorities:
- Outdoor priorities:
- Scenic-route priorities:
- Aurora priorities:

## Conditions
- Cold tolerance:
- Rain tolerance:
- Snow-driving confidence:
- Hike difficulty target:
- Must-see places:
- Must-avoid:

## Bookings and Deadlines
| Item | Needed by | Status | Notes |
|------|-----------|--------|-------|
| Entry docs | | | |
| Flights | | | |
| Rail or ferries | | | |
| Hotels | | | |
| Car rental | | | |
| Activities or tours | | | |

## Working Plan
- Current route draft:
- Backup plan:
- High-risk links:

## Notes
- Durable observations only.
```

## Status Values

| Value | Meaning | Behavior |
|-------|---------|----------|
| `ongoing` | still learning trip shape | ask only high-impact follow-ups |
| `complete` | core context is stable | act quickly from saved defaults |
| `paused` | memory use paused | do not expand without need |
| `never_ask` | no setup prompts wanted | avoid future setup questions |

## Key Principles

- Save route logic and logistics constraints, not casual travel chatter.
- Preserve season, corridor, and driving confidence because they determine almost every Norway plan.
- Keep changing details in the bookings table, not scattered notes.
- Replace old guesses once dates, flights, ferries, or car plans become fixed.
