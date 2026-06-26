# Future Poke Recipe Seed

This offline bundle is intentionally not published as a live Poke recipe yet because it does not have a public Matrix Mate MCP URL.

## Future recipe basics

- Name: `Matrix Mate Travel Audit`
- Description: `Parse ITA Matrix itinerary links, audit fare rules, and summarize traveler-safe trip details with Matrix Mate.`
- Integration type: MCP
- Integration target: future hosted Matrix Mate MCP URL
- Auth model: anonymous read-only if the hosted surface is public

## Suggested onboarding prompts

- What route or itinerary are you trying to audit?
- Do you already have an ITA Matrix itinerary link, or should I search Matrix first?
- Is your priority traveler safety, fare rules, or premium-cabin optimization?

## First-turn guidance

Prefer this opening behavior:

1. Confirm whether the user already has a Matrix itinerary link.
2. If not, offer a browser-assisted Matrix search.
3. Once a link exists, parse it with Matrix Mate.
4. If verification fails, request manual ITA JSON plus fare rules instead of improvising.

## Publish constraint

Do not publish this recipe until a stable hosted MCP endpoint exists and the live recipe has been tested end-to-end in Poke Kitchen.
