## Description:

Access detailed information on Rick and Morty characters, locations, and episodes across all show seasons using specific IDs or searches.

This skill is ready for commercial/non-commercial use.

## Publisher:

[brucegutman](https://clawhub.ai/user/brucegutman)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users can configure a Rick and Morty lookup helper to search characters or retrieve character, location, and episode details by ID.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Queries are sent to a third-party Pipeworx gateway endpoint.

Mitigation: Use the skill for public Rick and Morty lookups and avoid sending sensitive or private data in tool arguments unless the service has been independently trusted.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/brucegutman/skills/pipeworx-rickmorty)
- [Pipeworx Rick and Morty MCP endpoint](https://gateway.pipeworx.io/rickmorty/mcp)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash and JSON configuration blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Queries are sent to a third-party Pipeworx gateway endpoint for Rick and Morty lookup results.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
