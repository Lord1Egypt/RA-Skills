## Description:

Connects an agent to a Pipeworx-hosted wger exercise database for exercise, muscle, equipment, and workout routine lookup.

This skill is ready for commercial/non-commercial use.

## Publisher:

[brucegutman](https://clawhub.ai/user/brucegutman)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, fitness application builders, and agents use this skill to browse exercises, retrieve exercise details, list muscles and equipment, and assemble workout guidance from wger data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Exercise lookup requests are sent to an external Pipeworx-hosted wger MCP endpoint.

Mitigation: Avoid sending private health details beyond what is needed for exercise lookup unless the user is comfortable with that service handling them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/brucegutman/skills/pipeworx-wger)
- [Pipeworx wger MCP endpoint](https://gateway.pipeworx.io/wger/mcp)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON configuration and optional curl examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Exercise queries are sent to the disclosed Pipeworx-hosted wger MCP endpoint.]

## Skill Version(s):

1.0.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
