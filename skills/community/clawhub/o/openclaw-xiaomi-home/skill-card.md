## Description: <br>
Control Xiaomi/Mijia smart home devices through Home Assistant using natural language to manage lights, climate, locks, fans, sensors, covers, vacuums, and XiaoAI announcements. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[canmaxfire](https://clawhub.ai/user/canmaxfire) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to connect OpenClaw-style agents to a local Home Assistant instance and control Xiaomi/Mijia smart-home devices with plain-language requests. It is suited for device status checks, lighting and climate control, lock operations, routines, and local voice announcements. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad AI-driven control over physical smart-home devices, including locks and whole-home actions, can cause unsafe or unintended device changes. <br>
Mitigation: Review proposed actions before execution and require explicit confirmation for unlock, lock, whole-home, appliance, or automation-changing commands. <br>
Risk: The skill requires a sensitive Home Assistant long-lived access token. <br>
Mitigation: Use a dedicated least-privilege token if possible, store it only in the local environment file, protect the host account, and rotate the token if exposure is suspected. <br>
Risk: The MCP server and service persistence can expand local attack surface if exposed beyond localhost or enabled without review. <br>
Mitigation: Bind the MCP server strictly to localhost, keep bearer-token authentication enabled, and verify Docker or LaunchAgent persistence before enabling it. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/canmaxfire/openclaw-xiaomi-home) <br>
- [Home Assistant API Notes](artifact/references/api-notes.md) <br>
- [Automation Templates](artifact/references/automations.md) <br>
- [Device Support Reference](artifact/references/device-support.md) <br>
- [Detailed Installation Guide](artifact/references/installation.md) <br>
- [Home Assistant](https://www.home-assistant.io/) <br>
- [ha_xiaomi_home](https://github.com/nickoowen/ha-xiaomi-home) <br>
- [OpenClaw](https://openclaw.ai/) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, API calls, guidance] <br>
**Output Format:** [Markdown guidance, shell commands, configuration snippets, and JSON-RPC tool results returned as text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a local Home Assistant instance, Xiaomi/Mijia devices, and a Home Assistant long-lived access token.] <br>

## Skill Version(s): <br>
1.2.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
