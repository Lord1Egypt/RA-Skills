## Description:

Xiaomi Home Control lets agents control Xiaomi/Mijia smart-home devices through Home Assistant using natural-language requests for lights, climate, locks, sensors, fans, curtains, vacuums, and XiaoAI announcements.

This skill is ready for commercial/non-commercial use.

## Publisher:

[canmaxfire](https://clawhub.ai/user/canmaxfire)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to connect OpenClaw-style agents to Home Assistant so they can inspect and control local Xiaomi/Mijia smart-home devices with natural-language requests.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Smart-home commands can affect locks, climate, lights, covers, vacuums, and announcements.

Mitigation: Review sensitive tool calls before execution and restrict Home Assistant access to only the entities the agent should control.

Risk: The skill requires a Home Assistant long-lived access token stored in a local .env file.

Mitigation: Use a least-privilege token where possible, keep the .env file out of version control, protect local file permissions, and rotate the token if exposed.

Risk: The MCP server exposes home-control actions over HTTP and the security evidence flags under-scoped network binding.

Mitigation: Bind the server explicitly to loopback, keep it behind local firewall rules, and avoid exposing the port to a LAN or the internet.

Risk: The Docker configuration uses privileged or host-network Home Assistant deployment patterns.

Mitigation: Avoid privileged or host-network Docker unless required for the user's setup, and document any capability or network exposure that remains enabled.

Risk: The setup flow can install persistent startup through a LaunchAgent.

Mitigation: Review the LaunchAgent contents and uninstall procedure before enabling persistent startup.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/canmaxfire/skills/openclaw-xiaomi-home)
- [Home Assistant API Notes](artifact/references/api-notes.md)
- [Automation Templates](artifact/references/automations.md)
- [Device Support Reference](artifact/references/device-support.md)
- [Detailed Installation Guide](artifact/references/installation.md)
- [Home Assistant](https://www.home-assistant.io/)
- [ha_xiaomi_home](https://github.com/nickoowen/ha-xiaomi-home)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, API calls, guidance]

**Output Format:** [Markdown guidance with inline shell commands, configuration snippets, and JSON-RPC/Home Assistant API examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local smart-home control guidance and tool-call instructions; actions depend on the user's Home Assistant entities, token, and network configuration.]

## Skill Version(s):

1.2.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
