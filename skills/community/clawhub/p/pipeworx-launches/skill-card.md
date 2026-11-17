## Description:

Launches MCP wraps the Launch Library 2 API for free, unauthenticated launch data access.

This skill is ready for commercial/non-commercial use.

## Publisher:

[brucegutman](https://clawhub.ai/user/brucegutman)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to connect an agent to Pipeworx launch-data MCP tools for upcoming, past, specific, and searched space launches.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup uses an unpinned npm-based MCP bridge that can run code from the local account.

Mitigation: Pin mcp-remote to a reviewed version and run the MCP server in a restricted environment without unnecessary access to sensitive files or credentials.

## Reference(s):

- [Pipeworx Launches](https://pipeworx.io/packs/launches)
- [ClawHub skill page](https://clawhub.ai/brucegutman/skills/pipeworx-launches)

## Skill Output:

**Output Type(s):** [text, configuration]

**Output Format:** [Text responses from MCP tool calls and JSON MCP server configuration.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Launch data is accessed through a Pipeworx MCP endpoint; no API key is described in the artifact.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
