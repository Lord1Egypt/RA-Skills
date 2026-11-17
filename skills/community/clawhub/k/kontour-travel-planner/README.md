# kontour-travel-planner

AI agent skill for world-class travel planning using a 9-dimension progressive planning model.

## Install

```bash
npx skills add kontour-travel-planner
```

Or browse on a supported skill marketplace.

## What This Skill Does

Transforms any AI agent into a travel planning consultant using a structured methodology:

- **9 weighted dimensions** — dates, destination, budget, duration, travelers, interests, accommodation, transport, constraints
- **4-stage conversation flow** — Discover → Develop → Refine → Confirm
- **Guided discovery** — one high-impact question per turn, concrete options, conflict detection
- **Structured output** — trip context JSON, candidate scoring explanations, output polish with owner-tagged next actions, day-by-day itinerary, budget breakdown, Google Maps export
- **Reference data** — 200 destinations, 500 airports, airlines, activities, budget benchmarks (no API needed)

## Reference Data

Ground truth files in `references/`:

| File | Contents |
|------|----------|
| `destinations.json` | 200 global destinations with coordinates, costs, best months |
| `airports.json` | 500 airports with IATA codes and coordinates |
| `airlines.json` | Major airlines with alliances, hubs, regions |
| `activities.json` | Activity types with durations, cost tiers |
| `budget-benchmarks.json` | Daily cost benchmarks by destination tier |
| `booking-integrations.json` | Integration roadmap for booking providers |
| `embed-snippets.json` | Optional static CTA/template examples |

## Constraint Capture Smoke Test

The planner extracts operator-visible constraint details from natural-language requests, including budget caps, trip pace, neighborhood/base preference, opening-hours sensitivity, food preference, and weather sensitivity. Run the offline regression check with:

```bash
./scripts/test-plan-constraints.sh
```

## Candidate Scoring Explanations

When the request includes a known destination, `scripts/plan.sh` now emits `suggested_places` with ranked highlights and concise `why_chosen` factors. Each explanation references at least two concrete scoring factors such as destination fit, thematic fit, budget fit, hours sensitivity, or weather screening, so operators can see why a place entered the first-pass plan.

## Day-Plan Continuity

For known destinations with enough ranked highlights, `scripts/plan.sh` emits `day_plan_continuity`: a morning/afternoon/evening sequencing scaffold with zones, continuity reasons, and transition rationale. This gives operators a compact first pass that reduces avoidable backtracking before a full itinerary or route export is finalized.

## Risk + Fallback Warnings

When constraints make a first-pass plan fragile, `scripts/plan.sh` emits `risk_fallbacks` instead of failing bluntly. The warnings currently cover closed-venue/opening-hours risk, weather mismatch, sparse-area destinations outside bundled references, and over-constrained budget caps, with each warning naming the nearest viable alternative and the action to take before finalizing.

## Destination Comparison Support

When a request asks to compare 2-3 options, `scripts/plan.sh` emits `destination_comparison` with per-option budget benchmarks, best months, fit factors, tradeoffs, a decision matrix, best-for bullets, watch-outs, an operator summary, and a clear `recommended_option`. If the user names a month or season, the comparison highlights matching or risky timing so operators can explain the decision before committing to a destination-specific itinerary.

## Compact Presentation Markdown

For output polish, `output_polish.presentation_markdown` provides a ready-to-adapt Markdown draft with four compact sections: Recommendation, Why this fits, Watch-outs, and Next step. It preserves the structured JSON fields while giving operators a user-visible response scaffold with clear rationale and the single next action. `output_polish.decision_badges` also exposes compact readiness, next-owner, fallback-count, and decision-mode labels so UIs and operators can scan the plan state without parsing the full rationale. `output_polish.handoff_brief` adds a copy-ready operator transfer note with the decision, rationale bullets, watch-out, next action owner, and evidence drivers for smoother planning handoffs. `output_polish.shareable_summary` emits a plain-language, decision-first text block that can be pasted into chat or trip notes without exposing raw JSON. `output_polish.validation_summary` gives operators a go/no-go checklist with pass criteria and fallback actions before expanding or presenting the plan. `output_polish.finalization_gate` adds an explicit blocked/ready signal with user/operator blocking checks so provisional offline plans are not presented as final too early. `output_polish.live_validation_prompt_pack` provides copy-ready user/operator validation prompts before treating offline recommendations as final. `output_polish.assumption_ledger` adds a short operator-visible list of provisional assumptions, missing inputs, and live-validation caveats that should be labeled before a plan is shown as final. `output_polish.decision_snapshot_table` adds a compact five-row table for dashboards and chat cards: focus, readiness, primary evidence, watch-out, and next action. `output_polish.evidence_trace_card` adds a compact source-field audit trail so operators can see which structured evidence supports the recommendation. `output_polish.user_response_choices` adds copy-ready example traveler responses for the highest-priority clarification or confirmation so chat UIs can present concrete next-step choices. `output_polish.send_decision_card` adds a single send/hold call with the safest send form, primary blocker, and a copy-ready operator instruction so provisional plans are not over-sent as final. `output_polish.outbound_send_packet` adds the exact traveler-facing message to send now, plus send/hold status, hold-until condition, and a do-not-add guard so operators can paste one outbound reply without inventing a final itinerary too early. `output_polish.reply_intake_card` adds accepted traveler replies, the next operator move if they answer, and a still-do-not guard so the inbound answer is not treated as a go-ahead to send a fake final itinerary. `output_polish.followup_send_packet` adds the copy-ready traveler follow-up after that answer, with send/hold status and a still-do-not guard so acknowledgement is not treated as a final itinerary. `output_polish.unclear_reply_packet` adds the copy-ready traveler retry when the inbound answer is unclear, so operators can ask once more without treating a vague reply as a go-ahead for a final itinerary. `output_polish.two_turn_send_script` now includes that unclear-retry branch beside the happy-path follow-up. `output_polish.no_reply_nudge_packet` adds the copy-ready reminder when the traveler stays silent after the outbound question, so operators can nudge once without treating silence as a go-ahead for a final itinerary. `output_polish.post_nudge_hold_packet` adds the operator-only hold after that one reminder, so a second nudge or continued silence is not treated as a go-ahead for a final itinerary.

## Scripts

- `scripts/plan.sh` — Get structured trip context from natural language
- `scripts/export-gmaps.sh` — Export itinerary to Google Maps links and KML
- `scripts/gen-airports.py` — Generate airport reference data

## Marketplace privacy policy

- Do not disclose staging, preview, Pages, or deployment hostnames in marketplace text.
- Keep install and usage examples product-neutral and avoid personal/operator identifiers.
- Add approved public URLs only when the operator provides them in the current publishing context.

## License

MIT
