## Description:

Geographic utilities for geocoding, reverse geocoding, country information, timezone lookup, and sunrise/sunset times.

This skill is ready for commercial/non-commercial use.

## Publisher:

[b-gutman](https://clawhub.ai/user/b-gutman)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and agents use this skill to convert place names and coordinates, retrieve country details, check local timezones, and calculate daylight information for a specific location and date.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documented MCP setup runs mcp-remote through npx with an unpinned latest package.

Mitigation: Pin mcp-remote to a reviewed exact version, use a lockfile or managed install, and run the MCP server with minimal filesystem and credential access.

Risk: The skill can process sensitive addresses, coordinates, or site locations through an external service.

Mitigation: Avoid sending sensitive home addresses, private coordinates, or confidential site locations unless the Pipeworx service is approved for the use case.

## Reference(s):

- [Pipeworx Geo homepage](https://pipeworx.io/packs/geo)
- [Pipeworx Geo ClawHub listing](https://clawhub.ai/b-gutman/skills/pipeworx-geo)
- [Publisher profile](https://clawhub.ai/user/b-gutman)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash and JSON code blocks; tool responses are JSON-compatible location data.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl and connects to the Pipeworx Geo MCP gateway; no API keys are documented.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
