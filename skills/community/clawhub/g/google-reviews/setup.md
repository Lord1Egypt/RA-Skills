# Setup - Google Reviews

Read this on first use of Google review monitoring.

## Activation

Activate for requests about Google Maps reviews, Google Shopping review signals, brand reputation monitoring, and recurring sentiment updates.

Keep alerting and outbound posting ask-first by default.

## First Context Capture

Start by answering the user's immediate request, then capture reusable setup context in natural language:
- Which company or business entity the user wants to analyze right now
- What decision this review analysis should support (buy, partner, compare, audit, monitor)
- Which Google sources matter for this request (Business Profile, Shopping, both)
- Optional list of additional companies or brands for comparison
- Desired refresh cadence (heartbeat frequency plus deep-report cadence)
- Alert sensitivity (strict, balanced, or low-noise)
- Preferred report format (short digest, action report, or trend dashboard)

## Integration Behavior

Clarify how this should activate in future sessions:
- Auto-activate for reputation and review monitoring requests
- Stay quiet unless explicitly requested
- Suggest itself when user asks for heartbeat or review reporting systems

Store activation preference and rationale in `~/google-reviews/memory.md`.

## Save to `~/google-reviews/`

Persist only reusable monitoring context:
- Brand watchlist and source ownership
- Cadence and alert thresholds
- Known issue themes and escalation rules
- Report audience and output format preferences

Before the first write in a new workspace, confirm that local files will be created under `~/google-reviews/`.
