# Preparation Signal Rules

Used by: `sands.brief` (morning mode)

Flag an event as `prep_required: true` when ANY of these conditions are true.

---

## Title Keywords (case-insensitive)

review, prep, preparation, presentation, briefing, interview, pitch, demo,
proposal, debrief, kickoff, onboarding, performance, evaluation, assessment,
report, workshop, panel, keynote

## Attendee Signals

- At least one external attendee (email domain differs from user's primary domain)
- 3 or more total attendees

## Conference / Call Signals

- Event has a Google Meet, Zoom, Teams, or Webex link
- Title contains: call, sync, standup — AND has at least one external attendee

## Location Signals

- Event has a location and a travel block was inserted before it
- Event location has not appeared in the user's calendar in the past 30 days

---

## Do NOT Flag as Prep-Required

- Solo events: gym, workout, personal errands, focus time, lunch (no attendees)
- Recurring events where the same title appears >= 3 times in the last 30 days
  AND has no external attendees

---

## Output Format Per Prep Item

```
📋 [Event title] at [HH:MM]
   Why: [one-line reason]
   Suggested prep: [one actionable line]
```

Examples:
```
📋 Client Pitch at 10:00
   Why: External attendees, "pitch" in title
   Suggested prep: Review deck and confirm attendee list

📋 Dentist at 14:30
   Why: New location, no prior calendar history
   Suggested prep: Confirm address and allow travel time
```
