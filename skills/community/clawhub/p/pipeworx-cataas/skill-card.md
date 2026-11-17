## Description:

Retrieve random cat images, find cats by specific tags, and list available cat tags using the Pipeworx cataas service.

This skill is ready for commercial/non-commercial use.

## Publisher:

[brucegutman](https://clawhub.ai/user/brucegutman)

### License/Terms of Use:

MIT-0

## Use Case:

Agents and developers use this skill to retrieve random or tag-filtered cat images and list available tags when a workflow needs lightweight cat-image content.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Requests for cat images and normal connection metadata go to a disclosed third-party MCP endpoint.

Mitigation: Avoid sending sensitive prompts or private data through this skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/brucegutman/skills/pipeworx-cataas)
- [Pipeworx cataas MCP endpoint](https://gateway.pipeworx.io/cataas/mcp)

## Skill Output:

**Output Type(s):** [text, configuration]

**Output Format:** [Text responses with image URLs, cat IDs, tags, and JSON MCP server configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Remote endpoint requests may disclose normal connection metadata and any prompt content sent through the skill.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
