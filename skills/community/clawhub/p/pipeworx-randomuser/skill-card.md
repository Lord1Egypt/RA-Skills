## Description:

Generates realistic synthetic user profiles with names, contact details, addresses, nationality, and profile picture URLs through a Pipeworx-hosted MCP service.

This skill is ready for commercial/non-commercial use.

## Publisher:

[brucegutman](https://clawhub.ai/user/brucegutman)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, QA teams, and agents use this skill to generate synthetic user profiles for testing, demos, and workflows that need realistic placeholder people data without using real personal data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated profiles look like personal data and could be confused with real people records.

Mitigation: Treat returned profiles as synthetic test data and avoid mixing them with real personal data.

Risk: Using the skill sends generation requests to a Pipeworx-hosted MCP endpoint.

Mitigation: Confirm the endpoint is acceptable for the deployment environment before installing or using the skill.

Risk: Profile picture URLs may cause clients to fetch images from third-party-hosted locations.

Mitigation: Review client image-fetch behavior and network policy before rendering returned profile photos.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/brucegutman/skills/pipeworx-randomuser)
- [Pipeworx randomuser MCP endpoint](https://gateway.pipeworx.io/randomuser/mcp)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with JSON examples and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Profiles may include personal-looking synthetic fields and profile picture URLs.]

## Skill Version(s):

1.0.0 (source: release evidence, created 2026-04-14)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
