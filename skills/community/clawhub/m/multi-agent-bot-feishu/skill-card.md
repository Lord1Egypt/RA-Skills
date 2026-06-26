## Description: <br>
Guides OpenClaw users through creating additional agents and binding each one to a Feishu bot or group chat by editing ~/.openclaw/openclaw.json. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Richardcoder849](https://clawhub.ai/user/Richardcoder849) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw operators use this skill to configure separate agents for different Feishu bots, group chats, or business lines. It helps route messages, separate conversation memory, and apply per-chat or per-user access controls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The setup requires editing ~/.openclaw/openclaw.json, which can break existing OpenClaw routing if changed incorrectly. <br>
Mitigation: Back up the configuration file before making changes and verify agent, account, and binding identifiers before restarting OpenClaw. <br>
Risk: Feishu appSecret values and bot credentials are sensitive and may be exposed through configuration files, chats, logs, screenshots, or support requests. <br>
Mitigation: Use least-privilege Feishu bots, restrict access to the configuration file, and redact appSecret values from shared material. <br>
Risk: Using open access policies can expose bots or group chats to unintended users. <br>
Mitigation: Prefer allowlists and review dmPolicy, allowFrom, groupPolicy, and groupAllowFrom settings for each bot or group. <br>


## Reference(s): <br>
- [config-template.json](references/config-template.json) <br>
- [Feishu multiple bot configuration guide](https://docs.openclaw.ai/docs/feishu/multiple-bots) <br>
- [OpenClaw documentation](https://docs.openclaw.ai) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with JSON configuration examples and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the user to edit OpenClaw configuration, create a workspace directory, and restart the OpenClaw gateway.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact changelog top entry is 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
