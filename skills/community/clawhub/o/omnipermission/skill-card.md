## Description: <br>
Human-in-the-loop: A free, extensible framework for intercepting tool calls via the OmniPersona mobile app. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tobiasyouki](https://clawhub.ai/user/tobiasyouki) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
OpenClaw users and developers use this plugin to require mobile approval before selected high-risk tool calls execute, especially for agents that can access external services or destructive operations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The approval key can be exposed through status output or local plugin state. <br>
Mitigation: Avoid sharing status output, restrict access to local plugin state, and rotate the OmniPersona key if it may have been exposed. <br>
Risk: The plugin is not a hard security boundary if the agent can run OpenClaw CLI commands that modify the blacklist or plugin settings. <br>
Mitigation: Use an isolated environment for sensitive workflows and keep configuration changes under direct user control. <br>
Risk: Approval requests depend on the external OmniPersona/OmniPermission backend and mobile prompt content. <br>
Mitigation: Install only when the backend is trusted and verify what the mobile prompt displays before relying on it for high-risk tools. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/tobiasyouki/omnipermission) <br>
- [Publisher profile](https://clawhub.ai/user/tobiasyouki) <br>
- [Project homepage](https://github.com/youkinetwork/OmniPermission) <br>
- [OmniPersona on the App Store](https://apps.apple.com/us/app/omnipersona/id6553972082) <br>
- [OmniPersona on Google Play](https://play.google.com/store/apps/details?id=ai.youki.omni.persona) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can block blacklisted OpenClaw tool calls pending mobile approval; stores selected tool blacklist and the OmniPersona key in local plugin state.] <br>

## Skill Version(s): <br>
1.0.2 (source: package.json, openclaw.plugin.json, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
