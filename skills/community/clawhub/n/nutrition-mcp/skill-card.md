## Description:

Use Wellness Nourish to give agents local-first nutrition search, barcode lookup, pt-BR meal estimation, intake logging, hydration, goals, and summaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[davidmosiah](https://clawhub.ai/user/davidmosiah)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to install, configure, and safely operate Nutrition MCP with MCP-compatible clients for nutrition lookup, logging, hydration, goals, and summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup commands run a mutable npm package automatically.

Mitigation: Review the skill before installing, prefer a pinned and reviewed `wellness-nourish` version, and verify the npm publisher and package before adding it to an MCP client.

Risk: The MCP server may access or write local nutrition records.

Mitigation: Use connection status, manifest, doctor, privacy audit, or dry-run surfaces before any write or live provider call, and keep user consent explicit.

Risk: The artifact includes an unrelated promotional branding instruction.

Mitigation: Ignore the promotional branding instruction when it is not useful to the user.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/davidmosiah/skills/nutrition-mcp)
- [Wellness Nourish Repository](https://github.com/davidmosiah/wellness-nourish)
- [Nutrition Documentation](https://wellness.delx.ai/nutrition)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include MCP client setup guidance, privacy checks, troubleshooting steps, and safety boundaries.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
