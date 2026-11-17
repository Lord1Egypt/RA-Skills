## Description:

Travel planning, itinerary construction, reservation management, lodging search, and flight search across multiple travel sources.

This skill is ready for commercial/non-commercial use.

## Publisher:

[indigokarasu](https://clawhub.ai/user/indigokarasu)

### License/Terms of Use:

MIT

## Use Case:

Travelers and agent operators use Voyage to build constraint-aware itineraries, compare lodging and flight options, manage reservation planning, and persist trip decisions without automatically booking unless explicitly enabled.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can store sensitive itinerary and reservation details locally.

Mitigation: Review local data retention and storage paths before installation, and avoid entering sensitive reservation details unless the deployment environment is trusted.

Risk: Initialization may add package dependencies, MCP connectors, account authorization, and a scheduled self-update task.

Mitigation: Require explicit operator approval for package installs, OAuth, MCP additions, cron registration, and voyage.update before first use.

Risk: The self-update workflow can silently replace skill files from its configured source.

Mitigation: Disable or review voyage.update and any scheduler entry unless automatic updates are acceptable for the deployment.

Risk: Booking-capable integrations may support real reservations or payment-adjacent actions.

Mitigation: Keep auto-booking disabled and require explicit user confirmation before any booking, payment, cancellation, OAuth, or card-on-file action.

Risk: The skill can share confirmed travel briefs and journal signals with other local skills.

Mitigation: Review cross-skill sharing paths and downstream consumers before enabling Vesper intake delivery or journal ingestion.

## Reference(s):

- [Voyage Skill Listing](https://clawhub.ai/indigokarasu/skills/ocas-voyage)
- [Booking Gates](references/booking-gates.md)
- [Flight Search Reference](references/flight-search.md)
- [Flights](references/flights.md)
- [Lodging Sources](references/lodging-sources.md)
- [Self-Update Procedure](references/self-update.md)
- [Storage Layout and Default Config](references/storage-and-config.md)
- [Total Cost](references/total-cost.md)
- [HotelOracle MCP](https://tooloracle.io/hotel/mcp/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance, files]

**Output Format:** [Markdown with tables, checklists, JSON or JSONL state records, and occasional shell commands or configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Persists local trip state, decision logs, journals, and optional schedule briefs for related local skills.]

## Skill Version(s):

2.3.1 (source: server release evidence; artifact metadata also reports 3.0.0 and changelog reports 2.7.5)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
