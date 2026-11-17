## Description:

Global biodiversity data - search species, retrieve taxonomy, and find georeferenced occurrence records via GBIF.

This skill is ready for commercial/non-commercial use.

## Publisher:

[b-gutman](https://clawhub.ai/user/b-gutman)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and researchers use this skill to search species, retrieve taxonomic details, and query georeferenced GBIF occurrence records for ecology, conservation, education, and biodiversity dashboard workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The MCP configuration runs mcp-remote@latest through npx, which can change over time.

Mitigation: Pin mcp-remote to a reviewed exact version before installation or deployment.

Risk: The skill depends on a remote Pipeworx-hosted GBIF endpoint and local execution of an MCP bridge.

Mitigation: Run the MCP bridge in a restricted environment and avoid exposing unnecessary files, credentials, or environment variables.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/b-gutman/skills/pipeworx-gbif)
- [Pipeworx GBIF pack](https://pipeworx.io/packs/gbif)
- [Pipeworx GBIF MCP endpoint](https://gateway.pipeworx.io/gbif/mcp)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with JSON configuration and inline bash examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide an agent to configure an MCP server and call Pipeworx-hosted GBIF tools.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
