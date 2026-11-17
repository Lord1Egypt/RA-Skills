## Description:

Top 100 meme templates from Imgflip - names, dimensions, and image URLs ready for captioning.

This skill is ready for commercial/non-commercial use.

## Publisher:

[brucegutman](https://clawhub.ai/user/brucegutman)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to retrieve popular Imgflip meme template metadata for meme generators, social content tools, random template selection, and meme-format reference workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documented MCP setup runs an unpinned npm package with automatic confirmation.

Mitigation: Pin mcp-remote to a reviewed version before installation and review changes before upgrading.

Risk: Installing the MCP setup in an agent environment with sensitive files, environment variables, or credentials could increase exposure if the remote tooling is compromised or misconfigured.

Mitigation: Run the skill in a least-privilege environment without access to sensitive files, environment variables, or credentials.

## Reference(s):

- [Pipeworx Imgflip homepage](https://pipeworx.io/packs/imgflip)
- [Pipeworx Imgflip MCP endpoint](https://gateway.pipeworx.io/imgflip/mcp)
- [ClawHub skill page](https://clawhub.ai/brucegutman/skills/pipeworx-imgflip)
- [Publisher profile](https://clawhub.ai/user/brucegutman)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration]

**Output Format:** [Markdown instructions with bash and JSON examples; tool responses are JSON meme-template metadata.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns template id, name, image URL, width, height, and box count for the top 100 Imgflip meme templates.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
