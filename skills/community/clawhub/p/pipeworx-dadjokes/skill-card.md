## Description:

The finest dad jokes on the internet - random, searchable, and groan-worthy from icanhazdadjoke.com.

This skill is ready for commercial/non-commercial use.

## Publisher:

[brucegutman](https://clawhub.ai/user/brucegutman)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to fetch random, searchable, or ID-specific dad jokes for chatbots, conversation responses, and Slack or Discord bots.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup runs a remote MCP bridge through npm using an unpinned mcp-remote package.

Mitigation: Pin mcp-remote to a reviewed exact version, run the MCP process with least privilege, and avoid exposing sensitive environment variables.

## Reference(s):

- [Pipeworx Dadjokes Homepage](https://pipeworx.io/packs/dadjokes)
- [Pipeworx Dadjokes MCP Endpoint](https://gateway.pipeworx.io/dadjokes/mcp)
- [ClawHub Skill Page](https://clawhub.ai/brucegutman/skills/pipeworx-dadjokes)

## Skill Output:

**Output Type(s):** [Text, JSON, API Calls, Shell commands, Configuration]

**Output Format:** [Text jokes, JSON tool responses, and Markdown with inline bash and JSON code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl for the documented example and an MCP client configuration that launches mcp-remote.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
