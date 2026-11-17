## Description:

Random dog photos by breed -- 120+ breeds with sub-breeds from the Dog CEO API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[brucegutman](https://clawhub.ai/user/brucegutman)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to retrieve random or breed-specific dog image URLs, list supported breeds and sub-breeds, and add reference or placeholder dog photos to agent workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The MCP setup runs a mutable npm package through npx and mcp-remote, increasing local execution risk for a simple image lookup skill.

Mitigation: Review before installing, prefer a pinned and reviewed mcp-remote version, and run the skill in a constrained environment.

Risk: Requests are routed through Pipeworx, so prompts or tool arguments may be sent to a third-party service.

Mitigation: Avoid sending secrets, credentials, personal data, or sensitive prompts through this skill.

## Reference(s):

- [Pipeworx Dog CEO homepage](https://pipeworx.io/packs/dogceo)
- [Pipeworx Dog CEO MCP endpoint](https://gateway.pipeworx.io/dogceo/mcp)

## Skill Output:

**Output Type(s):** [text, configuration]

**Output Format:** [URLs, breed lists, and MCP configuration JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl for direct examples; MCP setup uses a remote Pipeworx endpoint.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
