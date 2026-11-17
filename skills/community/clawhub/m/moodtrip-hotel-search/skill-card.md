## Description:

Search, compare, evaluate, and hand off hotel bookings through the MoodTrip.ai MCP server using real-time hotel inventory, pricing, semantic search, reviews, and booking links.

This skill is ready for commercial/non-commercial use.

## Publisher:

[adiny](https://clawhub.ai/user/adiny)

### License/Terms of Use:

MIT-0

## Use Case:

External users and travel-planning agents use this skill to find, compare, and evaluate hotels, then hand off the final booking through a MoodTrip booking link.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installation can add a persistent MCP server configuration.

Mitigation: Require explicit user or administrator confirmation before editing MCP configuration or restarting a gateway.

Risk: The bundled MCP bridge runs an unpinned npx package.

Mitigation: Pin the bridge dependency version and review it before deployment.

Risk: Hotel search inputs are sent to MoodTrip.ai.

Mitigation: Avoid sending personal identifiers or payment information; use only destination, dates, guest counts, and lodging preferences needed for search.

## Reference(s):

- [MoodTrip Hotel Search on ClawHub](https://clawhub.ai/adiny/skills/moodtrip-hotel-search)
- [MoodTrip Hotel Search GitHub repository](https://github.com/adiny/moodtrip-hotel-search)
- [MoodTrip MCP server endpoint](https://api.moodtrip.ai/api/mcp-http)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with hotel search results, comparisons, setup guidance, and booking links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs can include MCP tool calls and link-based booking handoff; reservations are completed on the MoodTrip website.]

## Skill Version(s):

1.0.19 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
