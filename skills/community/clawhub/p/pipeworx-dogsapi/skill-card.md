## Description:

Detailed dog breed encyclopedia — weight ranges, life spans, temperament, and breed groups from dogapi.dog.

This skill is ready for commercial/non-commercial use.

## Publisher:

[brucegutman](https://clawhub.ai/user/brucegutman)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to retrieve dog breed attributes, breed groups, hypoallergenic status, temperament details, and random dog facts for pet-focused agents, comparison tools, adoption platforms, and content workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The MCP setup uses mcp-remote@latest, which can auto-download an unpinned npm package.

Mitigation: Review and pin the mcp-remote package version before use, or use the direct curl/API endpoint in a restricted environment.

Risk: Running the MCP bridge with broad local access could expose sensitive files or environment variables to software and services the user has not reviewed.

Mitigation: Run the bridge only in a constrained environment and avoid granting access to sensitive files or environment variables unless the package and service operator are trusted.

## Reference(s):

- [Pipeworx DogsAPI homepage](https://pipeworx.io/packs/dogsapi)
- [Pipeworx DogsAPI MCP endpoint](https://gateway.pipeworx.io/dogsapi/mcp)

## Skill Output:

**Output Type(s):** [text, JSON, configuration, shell commands]

**Output Format:** [Markdown guidance with JSON MCP configuration and bash examples; tool calls return structured dog breed and fact data.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl for direct examples; MCP setup uses a remote service endpoint.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
