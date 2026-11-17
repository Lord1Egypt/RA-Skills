## Description:

Helps users post a PowPop departure invitation and find potential travel companions; it requires a connected PowPop MCP server.

This skill is ready for commercial/non-commercial use.

## Publisher:

[durenzidu](https://clawhub.ai/user/durenzidu)

### License/Terms of Use:

MIT-0

## Use Case:

Travelers using PowPop can create a departure invitation and discover potential companions through nearby-origin, nearby-destination, and destination-mention searches. They review and approve a post before publication and can request recurring monitoring.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A public itinerary reveals the user's departure location, destination, and travel dates.

Mitigation: Review the draft before publishing and share only details you are comfortable making public.

Risk: Trip and candidate details remain in the local orders state file, and daily monitoring can continue until canceled.

Mitigation: Authorize the PowPop connection deliberately, protect the local state file, and cancel monitoring when finished.

## Reference(s):

- [PowPop MCP server](https://global.powpow.online/api/mcp)
- [PowPop Depart on ClawHub](https://clawhub.ai/durenzidu/skills/powpop-depart)
- [Publisher profile: durenzidu](https://clawhub.ai/user/durenzidu)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Chinese text and Markdown, including invitation drafts, candidate summaries, and itinerary guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an authenticated PowPop MCP connection; publication and recurring monitoring require explicit user approval.]

## Skill Version(s):

1.1.1 (source: frontmatter, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
