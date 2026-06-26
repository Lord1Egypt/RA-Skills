## Description: <br>
High-performance Zulip bridge skill that enables messaging, stream monitoring, and administrative actions on Zulip servers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[niyazmft](https://clawhub.ai/user/niyazmft) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to connect an OpenClaw agent to Zulip so it can send and receive messages, monitor streams, manage selected stream and user actions, and respond with Zulip context. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The plugin requires Zulip bot credentials. <br>
Mitigation: Install only from a trusted publisher, use a least-privileged Zulip bot, and protect API keys in environment or host configuration. <br>
Risk: Sensitive administrative-style Zulip actions may be callable by host or agent configuration. <br>
Mitigation: Leave enableAdminActions disabled unless explicitly needed and review any configuration that can call message actions directly by name. <br>
Risk: The artifact includes source-install workaround guidance that bypasses scanner concerns. <br>
Mitigation: Prefer the ClawHub install path and avoid the source-install scanner-bypass workaround. <br>


## Reference(s): <br>
- [OpenClaw Zulip ClawHub page](https://clawhub.ai/niyazmft/openclaw-zulip-bridge) <br>
- [OpenClaw Zulip channel docs](https://docs.openclaw.ai/channels/zulip) <br>
- [Artifact README](artifact/README.md) <br>
- [Artifact skill instructions](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown and plain text guidance for Zulip messaging, monitoring, setup, and selected administrative actions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Zulip bot credentials and OpenClaw channel-plugin configuration.] <br>

## Skill Version(s): <br>
2026.5.1 (source: server release evidence, package.json, openclaw.plugin.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
