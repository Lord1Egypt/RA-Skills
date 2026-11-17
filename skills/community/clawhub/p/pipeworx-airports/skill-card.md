## Description:

Airports MCP — wraps AirportGap API (free, no auth required)

This skill is ready for commercial/non-commercial use.

## Publisher:

[brucegutman](https://clawhub.ai/user/brucegutman)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to query airport information through the Pipeworx Airports MCP gateway and receive JSON-RPC responses from AirportGap-backed tools.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The MCP client setup uses an automatic install of an unpinned mcp-remote package.

Mitigation: Review the MCP client setup before installing and pin mcp-remote to an exact reviewed version.

Risk: Airport query data is routed through a third-party gateway.

Mitigation: Do not send secrets, credentials, private identifiers, or confidential business data through the gateway; run the client with limited filesystem and environment access.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/brucegutman/skills/pipeworx-airports)
- [Pipeworx airports homepage](https://pipeworx.io/packs/airports)
- [Pipeworx homepage](https://pipeworx.io)
- [Pipeworx airports MCP endpoint](https://gateway.pipeworx.io/airports/mcp)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, JSON]

**Output Format:** [Markdown guidance with bash and JSON configuration examples; gateway calls return JSON-RPC responses.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl for direct examples. Anonymous use is rate limited; the MCP client setup should be reviewed before installation.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
