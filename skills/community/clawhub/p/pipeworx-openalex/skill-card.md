## Description:

OpenAlex MCP wraps the OpenAlex API for scholarly works, authors, institutions, and concepts without requiring an API key.

This skill is ready for commercial/non-commercial use.

## Publisher:

[brucegutman](https://clawhub.ai/user/brucegutman)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and researchers use this skill to connect an agent to the Pipeworx OpenAlex MCP server for scholarly work, author, institution, and concept lookup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup runs an unpinned npm connector through npx.

Mitigation: Use a pinned and reviewed mcp-remote version, and run the MCP process in a sandbox or container before deployment.

Risk: Scholarly queries are routed through a third-party Pipeworx gateway.

Mitigation: Avoid confidential or identifying research queries unless the gateway's privacy and security posture is acceptable.

## Reference(s):

- [Pipeworx OpenAlex Pack](https://pipeworx.io/packs/openalex)
- [Pipeworx](https://pipeworx.io)
- [ClawHub Skill Page](https://clawhub.ai/brucegutman/skills/pipeworx-openalex)

## Skill Output:

**Output Type(s):** [text, configuration, guidance]

**Output Format:** [Markdown guidance and JSON MCP server configuration; MCP tool responses provide scholarly lookup results.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No API key is required by the skill.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
