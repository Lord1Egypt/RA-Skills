## Description: <br>
The skill helps an agent control Home Assistant smart-home devices and query device states using the MCP protocol. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[al-one](https://clawhub.ai/user/al-one) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to let an agent query Home Assistant state and issue smart-home control commands through an MCP server. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can let an agent change smart-home device state through Home Assistant. <br>
Mitigation: Review commands before execution and restrict use to intended devices and services. <br>
Risk: Home Assistant credentials may grant broad access to connected devices. <br>
Mitigation: Use a dedicated, least-privileged access token where possible and keep HASS_ACCESS_TOKEN out of shared logs and files. <br>
Risk: Commands involving safety-relevant devices can create physical-world effects. <br>
Mitigation: Use extra review for locks, alarms, heaters, garage doors, appliances, and similar devices before allowing changes. <br>


## Reference(s): <br>
- [Home Assistant MCP Integration](https://home-assistant.io/integrations/mcp) <br>
- [Home Assistant MCP Setup Redirect](https://my.home-assistant.io/redirect/config_flow_start?domain=mcp) <br>
- [mcporter Call Syntax](https://github.com/steipete/mcporter/raw/refs/heads/main/docs/call-syntax.md) <br>
- [mcporter CLI Reference](https://github.com/steipete/mcporter/raw/refs/heads/main/docs/cli-reference.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/al-one/mcp-hass) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May call Home Assistant tools that query or change smart-home device state when configured with Home Assistant credentials.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
