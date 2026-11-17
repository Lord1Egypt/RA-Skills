## Description:

Microlink MCP wraps the Microlink API with no API key required on the free tier.

This skill is ready for commercial/non-commercial use.

## Publisher:

[b-gutman](https://clawhub.ai/user/b-gutman)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to connect to Pipeworx Microlink MCP tools for retrieving web page metadata and taking screenshots through Microlink.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The connection example uses a mutable npm package version for mcp-remote.

Mitigation: Review before installing and prefer a pinned mcp-remote version.

Risk: URL-based work is sent to a third-party remote service with limited disclosure.

Mitigation: Avoid confidential, internal, or token-bearing URLs and use a sandboxed low-privilege MCP environment.

## Reference(s):

- [Pipeworx Microlink Pack](https://pipeworx.io/packs/microlink)
- [ClawHub Skill Page](https://clawhub.ai/b-gutman/skills/pipeworx-microlink)

## Skill Output:

**Output Type(s):** [API Calls, Configuration, Text, Files]

**Output Format:** [MCP tool responses and JSON connection configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Tool outputs may include page metadata and screenshots for submitted URLs.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
