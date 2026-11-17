## Description:

Math.js MCP — wraps the mathjs.org API (free, no auth).

This skill is ready for commercial/non-commercial use.

## Publisher:

[b-gutman](https://clawhub.ai/user/b-gutman)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to connect an MCP server that evaluates math expressions and converts units through the Pipeworx-hosted Math.js integration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup uses an unpinned npm bridge.

Mitigation: Pin mcp-remote to an exact reviewed version or run the bridge in a sandboxed environment.

Risk: Requests are sent to a third-party gateway with limited privacy disclosure.

Mitigation: Avoid sending sensitive or regulated data unless Pipeworx's data handling is acceptable.

## Reference(s):

- [Pipeworx Math.js Pack](https://pipeworx.io/packs/mathjs)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown with MCP JSON configuration and tool-result text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Provides evaluate and convert_units tools through a third-party remote MCP gateway.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
