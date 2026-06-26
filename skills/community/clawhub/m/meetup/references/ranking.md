# Ranking and Selection

Load this file when the user wants the best option, a shortlist, or when many event candidates are available.

## Goal

Pick the events the user is most likely to actually care about, not the events that merely exist.

## Ranking order

Apply these criteria in order:

1. **Scope fit**
   - Exact OpenClaw relevance beats general AI relevance when the user asked for OpenClaw.
   - AI/agent relevance beats generic tech relevance when the user asked for broader AI/agent events.

2. **Geographic fit**
   - Same city beats nearby city.
   - Nearby city beats region-wide result.
   - Region-wide result beats national result for a local query.

3. **Time relevance**
   - Upcoming soon beats upcoming far in the future for normal discovery.
   - Do not over-favor “tomorrow” if the event is a weak thematic fit.

4. **Evidence quality**
   - Dedicated event page beats vague listing.
   - Clear venue/date/RSVP beats thin metadata.

5. **User usefulness**
   - Beginner-friendly local meetup may beat a more prestigious but less relevant event.
   - If the user asked for hackathons, hackathons beat talks.

## Suggested labels for internal reasoning

Use simple internal buckets while ranking:

- **A-match** — strong fit, strong evidence, local or clearly worth travel
- **B-match** — relevant but slightly broader, farther away, or less certain
- **C-match** — technically related but weak fit or weak evidence

Normally show only A and B matches.
Do not show C matches unless the user explicitly asks for everything.

## Best-pick logic

When the user asks “which one should I pick?” or clearly wants a recommendation:

Pick the event that best balances:

- topic fit
- practical distance
- date usefulness
- confidence in event quality

Then explain the pick in 2–3 short bullets.

## Distance guidance

Do not fake precision.

- If you can estimate roughly, use “roughly X km away”.
- If you only know the city relationship, say “in your city” or “near your area”.
- If distance is not reliable, omit it.

## Tie-breakers

If two events are close in score:

- prefer the one with clearer details
- prefer the one with stronger OpenClaw/AI-agent relevance
- prefer the one that is easier to attend locally

## What not to optimize for

- hype
- social proof you cannot verify
- vague claims about popularity
- exact attendance counts unless directly shown on a reliable event page
