## Description:

Provides live scores, standings, team and player info across major sports leagues including football, basketball, baseball, and hockey.

This skill is ready for commercial/non-commercial use.

## Publisher:

[brucegutman](https://clawhub.ai/user/brucegutman)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to retrieve sports scores, standings, fixtures, team details, and player information across major leagues through a remote MCP sports service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sports queries and normal connection metadata are sent to gateway.pipeworx.io.

Mitigation: Send only the sports lookup information needed for the task, and avoid including private or unrelated prompt content.

Risk: Remote MCP capabilities may change after installation.

Mitigation: Review newly advertised MCP tools or capability changes before approving use.

## Reference(s):

- [Pipeworx sports ClawHub listing](https://clawhub.ai/brucegutman/skills/pipeworx-sports)
- [brucegutman ClawHub publisher profile](https://clawhub.ai/user/brucegutman)
- [Sports MCP endpoint](https://gateway.pipeworx.io/sports/mcp)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON configuration and command examples; sports query results are returned as MCP tool responses.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses a disclosed remote endpoint at gateway.pipeworx.io for sports lookups.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
