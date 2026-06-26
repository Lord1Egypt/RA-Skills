# Source Strategy

Load this file when the user asks for real event discovery, broader coverage, or when the first search pass is weak.

## Goal

Find a small set of real, future events with the highest chance of being relevant to the user's location and scope.

## Search order

### Pass 1 — OpenClaw-first

Use this when the user asks for OpenClaw events, community events, or does not specify broader scope.

Start with the tightest likely sources:

- official or community Luma pages tied to OpenClaw
- event pages that clearly mention OpenClaw in the title or description
- targeted web search for OpenClaw + city/country if direct source discovery is thin

Example search patterns:

- `OpenClaw meetup {city}`
- `OpenClaw event {city}`
- `site:luma.com OpenClaw {city}`
- `site:luma.com OpenClaw {country}`
- `site:eventbrite.com OpenClaw {city}`
- `site:meetup.com OpenClaw {city}`

### Pass 2 — AI/agent-adjacent

Use this when:

- the user explicitly wants broader AI/agent/tech events
- OpenClaw-only search is too sparse
- the user asks for alternatives or more options

Example search patterns:

- `AI agents meetup {city}`
- `LLM meetup {city}`
- `agent engineering event {city}`
- `AI hackathon {city}`
- `site:luma.com AI agents {city}`
- `site:meetup.com LLM meetup {city}`
- `site:eventbrite.com AI meetup {city}`

### Pass 3 — Fallback discovery

Use this only if the first two passes are weak.

- broader web search
- alternate city/metro wording
- country-level search if local search is empty

Example:

- `{city} AI meetup`
- `{region} AI event`
- `{country} OpenClaw event`

## Token discipline

- Start with 1–2 tight queries.
- Do not shotgun ten queries immediately.
- Stop expanding when you already have 2–3 strong matches.
- Prefer event pages over listicles, SEO spam, or vague community pages.

## Good result signals

Prefer items with:

- exact date and time
- exact city or venue
- dedicated event page
- registration or RSVP link
- clear topic fit to OpenClaw, AI agents, LLMs, or relevant tech communities

## Weak result signals

Down-rank or discard items with:

- no date
- no location
- generic newsletter or landing page with no concrete event
- duplicate aggregator copies of the same event
- stale pages for already-past events

## When to stop

Stop searching when one of these is true:

- you found 3 strong matches for a normal request
- you found 5 strong matches for a broad request
- every further result is clearly worse than the shortlist

## Direct request vs background check

### Direct request

Always return something useful:

- a shortlist, or
- a clear “nothing strong found” with the best next step

### Background/scheduled check

If nothing clearly relevant is found, return nothing.
