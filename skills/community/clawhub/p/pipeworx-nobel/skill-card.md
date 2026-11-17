## Description:

Nobel Prize laureates and awards \u2014 search by name or category and browse prizes by year since 1901.

This skill is ready for commercial/non-commercial use.

## Publisher:

[brucegutman](https://clawhub.ai/user/brucegutman)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to retrieve Nobel Prize laureate and award data for educational tools, research, trivia, and content workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup uses an unpinned mcp-remote package from the latest tag with automatic approval.

Mitigation: Review the setup before installation, pin mcp-remote to a specific reviewed version where possible, and run the MCP client with only the files and environment variables it needs.

## Reference(s):

- [Pipeworx Nobel homepage](https://pipeworx.io/packs/nobel)
- [ClawHub skill page](https://clawhub.ai/brucegutman/skills/pipeworx-nobel)
- [Pipeworx Nobel MCP endpoint](https://gateway.pipeworx.io/nobel/mcp)

## Skill Output:

**Output Type(s):** [Text, JSON, Configuration]

**Output Format:** [Markdown guidance with JSON configuration and JSON tool responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl for examples and configures an MCP client to use the Pipeworx Nobel endpoint.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
