# Setup — New Zealand Travel Guide

When the user first brings up New Zealand travel:

## 1. Create Memory

```bash
mkdir -p ~/new-zealand
```

Create `~/new-zealand/memory.md` from `memory-template.md`.

## 2. Gather the Route Inputs That Actually Matter

Ask naturally:
- Which month are they going?
- How many full days do they have on the ground?
- North Island, South Island, or undecided?
- Rental car, campervan, domestic flights, or mixed?
- Are they outdoors-first, food-first, family-first, or city-plus-nature?
- Any mobility, motion-sickness, hiking, dietary, or budget constraints?

## 3. Save the Important Friction Points

Track:
- arrival city and departure city
- ferry needs
- tolerance for long drives
- weather-sensitive priorities
- already-booked anchors

## 4. Returning Users

If `~/new-zealand/memory.md` exists:
1. Read it silently
2. Reuse known route and style preferences
3. Ask what changed since last plan
4. Update memory with new constraints

## Quick Start Responses

**"I am going to Queenstown"**
→ Ask: season, nights, ski vs hiking vs wineries
→ Then: use `queenstown.md`, `accommodation.md`, `seasonality.md`

**"Planning New Zealand road trip"**
→ Ask: days, island choice, driver confidence
→ Then: use `regions.md`, `transport.md`, `itineraries.md`

**"I want Milford Sound"**
→ Ask: where they will base, whether they can add weather buffer
→ Then: use `fiordland-southland.md`, `experiences.md`, `transport.md`

## Important Notes

- New Zealand is easy to underestimate and hard to rush well.
- Weather, road pace, and daylight matter more than many first-timers expect.
- Fewer bases usually produce a much better trip.
- Ferry, flight, and alpine days need explicit slack.
