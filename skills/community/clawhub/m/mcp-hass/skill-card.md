## Description:

Controls Home Assistant smart-home devices and queries their states through the Model Context Protocol.

This skill is ready for commercial/non-commercial use.

## Publisher:

[al-one](https://clawhub.ai/user/al-one)

### License/Terms of Use:


## Use Case:

External users and smart-home operators use this skill to let an agent inspect Home Assistant state and issue device-control commands through an MCP server.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill gives an agent real smart-home control through Home Assistant.

Mitigation: Use a dedicated revocable token with the least permissions available, and avoid broad agent prompts for safety-sensitive devices.

Risk: Home Assistant access can expose credentials or commands if transport is weak.

Mitigation: Use HTTPS or a trusted encrypted tunnel for Home Assistant.

Risk: The documented npx fallback can execute an unpinned package.

Mitigation: Prefer a pinned or otherwise verified mcporter installation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/al-one/skills/mcp-hass)
- [Home Assistant Model Context Protocol integration](https://home-assistant.io/integrations/mcp)
- [Home Assistant MCP setup link](https://my.home-assistant.io/redirect/config_flow_start?domain=mcp)
- [mcporter call syntax](https://github.com/steipete/mcporter/raw/refs/heads/main/docs/call-syntax.md)
- [mcporter CLI reference](https://github.com/steipete/mcporter/raw/refs/heads/main/docs/cli-reference.md)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires HASS_BASE_URL, HASS_ACCESS_TOKEN, and either mcporter or npx.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
