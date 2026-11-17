---
name: review-inbox
description: >-
  Work an app's customer reviews through MetaRun: triage what needs a reply,
  draft and post public responses, mine reviews for product and keyword
  signal, and turn the best quotes into social-proof screenshot slides.
  Trigger phrases: "check my reviews", "reply to reviews", "what are users
  complaining about", "answer the 1-star reviews", "mine my reviews".
metadata:
  openclaw:
    homepage: https://metarun.dev/agents
    primaryEnv: METARUN_TOKEN
    envVars:
      - name: METARUN_TOKEN
        required: false
        description: MetaRun personal access token (Settings, MCP). Not needed after `npx metarun login`, which stores it in ~/.metarun/config.json.
    requires:
      anyBins:
        - npx
---

# Review inbox: triage, reply, and mine the signal

You are working customer reviews through MetaRun. Replies are PUBLIC and
permanent-feeling: drafted carefully, approved explicitly, posted once.

## Ground rules

- Tools run over MetaRun's MCP server or `npx metarun run <tool> '<json>'`.
  Fetch unfamiliar schemas with `npx metarun tools <tool-name> --json`.
- Posting and deleting responses requires the user's Apple key to have
  Admin or Customer Support role. If those tools fail on authorization,
  say so; do not retry blindly.
- A reply is an outward action. Never post without showing the exact text
  and getting a clear yes. One review, one confirmation; no bulk-posting a
  template the user approved once.

## The mission

### 1. Read the room

- `apple_list_reviews` -> recent reviews with ratings and territories.
  Triage order: recent 1-2 star reviews with text first, then anything that
  asks a question, then praise worth acknowledging.
- `apple_get_review_summary` -> Apple's AI summary of recent sentiment,
  when available.
- Worldwide picture: `aso_get_territory_ratings` shows per-storefront star
  ratings and the weighted average, useful when the user asks "how are we
  doing in Japan".

### 2. Reply

- Draft replies in the app's voice: specific to the complaint, no corporate
  boilerplate, no promises the user has not made, never defensive. If a fix
  shipped or is coming, say which version.
- `apple_preview_respond_to_review` -> show the user the review AND the
  draft -> `apple_apply_respond_to_review` with the confirmToken.
- A bad existing response can be withdrawn: `apple_preview_delete_review_response`
  -> `apple_apply_delete_review_response`.

### 3. Mine the signal

- `aso_mine_reviews` extracts praise themes, complaint themes, and keyword
  candidates users actually type, without an LLM pass. Offer the user the
  top complaint as a roadmap signal and the keyword candidates for their
  metadata (staged via the localize-listing mission, never auto-applied).

### 4. Turn praise into assets (optional)

- A five-star quote can become a social-proof screenshot slide:
  `studio_add_review_slide` places it in a Screenshot Studio project. Offer
  this when a review is short, vivid, and specific.

## Beyond this mission

TestFlight crash and screenshot feedback are separate reads: discover with
`npx metarun tools testflight`. The wider surface: `npx metarun tools <filter>`.
