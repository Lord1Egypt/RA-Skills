## Description: <br>
OpenClaw Reference gives agents structured guidance for OpenClaw plugins, extensions, configuration, boot and provisioning, channels, model providers, CLI commands, and current development context. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tenequm](https://clawhub.ai/user/tenequm) <br>

### License/Terms of Use: <br>
Apache 2.0 <br>


## Use Case: <br>
Developers and engineers use this skill when working on OpenClaw code, building plugins or extensions, configuring instances, provisioning gateways, designing agent onboarding flows, or debugging configuration, plugin, channel, model, and CLI behavior. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The reference includes commands and workflows that can bypass plugin security scans, install or update plugins, change credentials or authentication, start persistent services, reset state, or enable wallet and payment flows. <br>
Mitigation: Do not let an agent run those commands automatically; require explicit human review and approval before applying commands that affect security, credentials, persistent services, state, wallets, or purchases. <br>
Risk: The skill is documentation-only and may provide operational guidance that is incorrect, stale, or unsuitable for a specific OpenClaw deployment. <br>
Mitigation: Review generated guidance against the target OpenClaw version, local configuration, and current issue context before deployment or production changes. <br>


## Reference(s): <br>
- [OpenClaw Boot & Provisioning](references/boot-provisioning.md) <br>
- [OpenClaw Channels & Extensions](references/channels-extensions.md) <br>
- [OpenClaw CLI Commands](references/cli-commands.md) <br>
- [OpenClaw Configuration](references/configuration.md) <br>
- [OpenClaw GitHub Context](references/github-context.md) <br>
- [OpenClaw Models & Providers](references/models-providers.md) <br>
- [OpenClaw Plugin System](references/plugin-system.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with code blocks, shell commands, and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only reference output; does not include executable skill code.] <br>

## Skill Version(s): <br>
2026.4.8 (source: server release and SKILL.md metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
