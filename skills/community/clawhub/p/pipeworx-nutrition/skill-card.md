## Description:

Nutrition MCP wraps the Open Food Facts API for product search and lookup without an API key.

This skill is ready for commercial/non-commercial use.

## Publisher:

[brucegutman](https://clawhub.ai/user/brucegutman)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to connect an agent to the Pipeworx Nutrition MCP for Open Food Facts product search and product lookup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Product lookup queries are routed through the Pipeworx remote MCP service.

Mitigation: Install only when that routing is acceptable for the intended use case.

Risk: The documented connection uses an unpinned npm MCP bridge package.

Mitigation: Pin mcp-remote to a reviewed version and run the agent with normal least-privilege sandboxing.

## Reference(s):

- [Pipeworx Nutrition](https://pipeworx.io/packs/nutrition)
- [Pipeworx](https://pipeworx.io)
- [ClawHub Skill Page](https://clawhub.ai/brucegutman/skills/pipeworx-nutrition)

## Skill Output:

**Output Type(s):** [Text, JSON, Configuration]

**Output Format:** [MCP tool responses and JSON connection configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Provides product search and product lookup through a disclosed remote MCP service.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
