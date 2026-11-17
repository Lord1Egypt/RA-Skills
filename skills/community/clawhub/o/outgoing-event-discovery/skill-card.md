## Description:

Find and book real-world things to do, including restaurants, bars, concerts, comedy, museums, events, and activities, through Outgoing natural-language search.

This skill is ready for commercial/non-commercial use.

## Publisher:

[outgoing](https://clawhub.ai/user/outgoing)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to discover real-world venues and events in cities worldwide, route occasion-specific plans to companion skills, and book eligible activities after confirming details and cost.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Searches, city hints, and stable external user identifiers are sent to Outgoing.

Mitigation: Install only when this third-party data sharing is acceptable and avoid including unnecessary sensitive details in prompts.

Risk: Booking with a real payment token can create an actual purchase.

Mitigation: Use dry-run payment tokens during testing and provide a real payment token only after confirming the exact tickets, quantity, and total cost.

Risk: Venue details, accessibility details, prices, and availability can be incorrect if the agent adds information not returned by the API.

Mitigation: Present only API-returned details and ask users to confirm important accessibility, venue, price, and availability details before relying on them.

## Reference(s):

- [Outgoing Developer Docs](https://www.outgoing.world/developers)
- [Outgoing API Reference](https://www.outgoing.world/llms.txt)
- [Outgoing Full API Reference](https://www.outgoing.world/llms-full.txt)
- [AAuth MCP OpenClaw Package](https://www.npmjs.com/package/@aauth/mcp-openclaw)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown guidance with inline curl examples and API response summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an Outgoing API key or AAuth key and an external user identifier for API calls.]

## Skill Version(s):

0.1.8 (source: server release metadata; artifact frontmatter reports 0.1.7)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
