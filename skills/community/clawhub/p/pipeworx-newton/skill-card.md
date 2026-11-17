## Description:

Symbolic math solver for simplifying, differentiating, integrating, and factoring expressions via the Newton API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[brucegutman](https://clawhub.ai/user/brucegutman)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, students, and technical users use this skill to call the Newton API for symbolic algebra and calculus tasks, including simplification, differentiation, integration, and polynomial factoring.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Entered math expressions are sent to PipeWorx's external Newton gateway.

Mitigation: Use the skill only when sending those expressions to the external service is acceptable.

Risk: The documented setup uses mcp-remote@latest, which can install an automatically updated npm package.

Mitigation: Pin mcp-remote to an exact reviewed version and run the MCP process with limited local permissions.

## Reference(s):

- [PipeWorx Newton pack homepage](https://pipeworx.io/packs/newton)
- [ClawHub skill listing](https://clawhub.ai/brucegutman/skills/pipeworx-newton)
- [Newton MCP gateway endpoint](https://gateway.pipeworx.io/newton/mcp)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Configuration]

**Output Format:** [JSON API responses and Markdown guidance with bash and JSON code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Calls an external PipeWorx gateway; setup uses a local npm-based MCP adapter.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
