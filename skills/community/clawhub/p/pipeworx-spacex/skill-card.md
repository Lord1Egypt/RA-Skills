## Description:

Access real-time and historical SpaceX data on launches, rockets, crew, and Starlink satellites with detailed status and media links.

This skill is ready for commercial/non-commercial use.

## Publisher:

[brucegutman](https://clawhub.ai/user/brucegutman)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to configure and call a Pipeworx-hosted MCP endpoint for SpaceX launch, rocket, crew, and Starlink data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: SpaceX tool requests are sent to the disclosed Pipeworx-hosted MCP endpoint.

Mitigation: Do not pass sensitive personal, account, or confidential data into this connector unless the service is trusted for that data.

## Reference(s):

- [Pipeworx SpaceX skill page](https://clawhub.ai/brucegutman/skills/pipeworx-spacex)
- [SpaceX MCP endpoint](https://gateway.pipeworx.io/spacex/mcp)
- [Source skill instructions](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration]

**Output Format:** [Markdown instructions with JSON configuration and bash examples; MCP tool calls return JSON data.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Remote MCP connector for SpaceX launch, rocket, crew, and Starlink data.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
