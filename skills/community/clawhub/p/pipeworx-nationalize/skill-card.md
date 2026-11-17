## Description:

Nationalize MCP provides nationality prediction from a first name using nationalize.io without requiring an API key.

This skill is ready for commercial/non-commercial use.

## Publisher:

[b-gutman](https://clawhub.ai/user/b-gutman)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users connect this MCP skill when they need an agent to estimate likely nationalities from one name or a batch of names.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Name queries are sent to an external Pipeworx/nationalize service.

Mitigation: Avoid sending sensitive personal data unless the external service is approved for the intended use.

Risk: The documented setup runs mcp-remote@latest through npx.

Mitigation: Prefer a pinned and reviewed mcp-remote version, and run the MCP bridge with least privilege or in a sandbox.

## Reference(s):

- [Pipeworx Nationalize pack](https://pipeworx.io/packs/nationalize)
- [ClawHub skill page](https://clawhub.ai/b-gutman/skills/pipeworx-nationalize)

## Skill Output:

**Output Type(s):** [text, configuration, API calls]

**Output Format:** [MCP tool responses and JSON connection configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No API key is documented; queries are sent to an external Pipeworx nationalize gateway.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
