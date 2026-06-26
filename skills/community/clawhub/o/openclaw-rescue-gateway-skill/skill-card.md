## Description: <br>
Configures a stable, maintainable OpenClaw rescue gateway with a second Discord bot, an independent port and launchd label, separated gateway lifecycle controls, and default full command execution without approval. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cchaojiejes](https://clawhub.ai/user/cchaojiejes) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators who already run an OpenClaw gateway use this skill to configure a separate rescue gateway for Discord access, independent launchd management, and emergency operation when the primary gateway is unavailable. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill instructs users to create a persistent Discord-controlled rescue gateway with full command execution and approvals disabled. <br>
Mitigation: Install only when a break-glass OpenClaw rescue gateway is intentionally needed; keep execution approvals enabled unless there is a specific emergency reason. <br>
Risk: Discord access to the rescue gateway can expose powerful operations to unintended users or channels. <br>
Mitigation: Restrict the rescue Discord bot to trusted servers, channels, and users, and verify the independent launchd service can be stopped or unloaded after use. <br>
Risk: Copying authentication profiles into the rescue agent can duplicate sensitive provider credentials. <br>
Mitigation: Use separate scoped rescue credentials where possible and protect copied credential files with restrictive file permissions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cchaojiejes/openclaw-rescue-gateway-skill) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, configuration, shell commands] <br>
**Output Format:** [Markdown with JSON configuration snippets and shell command blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes OpenClaw profile settings, macOS launchd service guidance, diagnostic commands, and credential-copying steps.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
