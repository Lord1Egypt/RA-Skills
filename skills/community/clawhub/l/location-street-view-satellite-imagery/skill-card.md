## Description:

Gets geocodes, reverse geocodes, and Street View or satellite imagery for addresses or coordinates through AgentPMT-hosted tool calls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agentpmt](https://clawhub.ai/user/agentpmt)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to add location lookup, visual site inspection, property assessment, travel preview, and geographic validation workflows to agents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles precise addresses or coordinates through AgentPMT-hosted remote calls.

Mitigation: Send only the minimum location data needed for the task and avoid submitting sensitive locations unless the user has approved that disclosure.

Risk: Generated image links are hosted and retained for 7 days.

Mitigation: Treat signed URLs as sensitive output, share them only with intended recipients, and avoid relying on them after expiration.

Risk: The security evidence notes mutable remote instructions and unpinned setup commands.

Mitigation: Prefer OpenClaw or pinned, reviewed skill versions for setup, and do not let live instructions override normal agent safety rules or broaden the requested task.

## Reference(s):

- [AgentPMT marketplace page](https://www.agentpmt.com/marketplace/location-street-view-satellite-imagery)
- [ClawHub skill page](https://clawhub.ai/agentpmt/skills/location-street-view-satellite-imagery)
- [Action schema](artifact/schema.md)
- [AgentPMT account MCP/REST setup](https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, JSON, API Calls]

**Output Format:** [Markdown instructions with JSON request and response shapes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Remote tool responses can include signed image URLs, base64 image data, geocoding metadata, and Street View availability details.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
