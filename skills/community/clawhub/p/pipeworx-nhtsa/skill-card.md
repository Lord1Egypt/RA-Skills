## Description:

Decode VINs and look up vehicle makes/models via the NHTSA Vehicle Product Information Catalog.

This skill is ready for commercial/non-commercial use.

## Publisher:

[brucegutman](https://clawhub.ai/user/brucegutman)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and automotive workflows use this skill to decode VINs, browse registered vehicle makes, look up models by make and year, and verify vehicle details from records such as bills of sale or registration documents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documented setup runs a mutable npm package with local user permissions.

Mitigation: Use a pinned mcp-remote version, review the local MCP bridge before installation, and run it in a restricted environment.

Risk: VIN or vehicle lookup inputs are sent to Pipeworx for processing.

Mitigation: Avoid submitting sensitive or unnecessary vehicle information unless the user accepts that data flow.

Risk: The local process could access unrelated project files, credentials, or environment variables if launched broadly.

Mitigation: Run the MCP bridge from a minimal workspace with only required environment variables exposed.

## Reference(s):

- [Pipeworx NHTSA Pack](https://pipeworx.io/packs/nhtsa)
- [Pipeworx NHTSA MCP Endpoint](https://gateway.pipeworx.io/nhtsa/mcp)
- [ClawHub Skill Page](https://clawhub.ai/brucegutman/skills/pipeworx-nhtsa)
- [Publisher Profile](https://clawhub.ai/user/brucegutman)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, API calls, Text]

**Output Format:** [Markdown with inline bash and JSON code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill guides agent use of remote vehicle lookup tools that return structured vehicle attributes.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
