## Description:

UK national carbon intensity data — real-time, historical, and generation mix from the Carbon Intensity API

This skill is ready for commercial/non-commercial use.

## Publisher:

[brucegutman](https://clawhub.ai/user/brucegutman)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, sustainability teams, smart home systems, and researchers use this skill to retrieve current and historical UK grid carbon intensity and generation mix data for operational decisions, dashboards, and analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup uses `npx` with an unpinned `mcp-remote@latest` package, creating supply-chain risk.

Mitigation: Pin `mcp-remote` to a trusted exact version or install it through a controlled package-management process before deployment.

Risk: Requests go through Pipeworx's gateway rather than directly to the public Carbon Intensity API.

Mitigation: Review the gateway endpoint and data-routing requirements before using the skill in sensitive or regulated environments.

## Reference(s):

- [Pipeworx Carbon Pack](https://pipeworx.io/packs/carbon)
- [Pipeworx Carbon MCP Gateway](https://gateway.pipeworx.io/carbon/mcp)
- [ClawHub Skill Page](https://clawhub.ai/brucegutman/skills/pipeworx-carbon)
- [Publisher Profile](https://clawhub.ai/user/brucegutman)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with JSON and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide an agent to call the Pipeworx carbon MCP gateway for carbon intensity and generation mix data.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
