## Description:

Install, configure, run, and troubleshoot a Windows WeChat desktop automation and BHMailer/OpenClaw mail bridge bundle, including File Transfer Assistant workflows, plugin config, sidecar setup, and operations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yjli-new](https://clawhub.ai/user/yjli-new)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to install, configure, run, and troubleshoot a Windows-local WeChat desktop bridge that connects OpenClaw group commands with BHMailer-backed mail queries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive WeChat and mail operations may be exposed more broadly than users expect.

Mitigation: Bind the plugin to localhost or a protected private interface, and use HTTPS or HMAC for any non-local traffic.

Risk: Default shared secrets may allow unauthorized sidecar or admin access if left unchanged.

Mitigation: Change default shared secrets before installation and keep plugin and sidecar secrets matched through local configuration or environment variables.

Risk: Raw WeChat text retention and optional remote VLM processing can increase privacy exposure.

Mitigation: Decide whether raw WeChat text should be retained, disable remote VLM unless explicitly approved, and approve the exact VLM endpoint before use.

Risk: Bundled dependency versions may need updates before production use.

Mitigation: Review and update bundled dependencies during deployment hardening.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/yjli-new/skills/openclaw-wechat-mail-bridge-windows)
- [ClawHub Publisher Profile](https://clawhub.ai/user/yjli-new)
- [Project Homepage](https://github.com/YJLi-new/OPENCLAW-SKILLS/tree/main/wechat-mail-bridge-skill/clawhub-openclaw-wechat-mail-bridge-windows)
- [Windows Quick Install](references/install-windows.md)
- [Config Reference](references/config.md)
- [Sidecar Config Reference](references/sidecar-config.md)
- [Operations](references/operations.md)
- [Release Notes](references/release-notes.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown with inline shell commands and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May direct the agent to inspect bundled TypeScript and Python source when deeper implementation detail is requested.]

## Skill Version(s):

0.1.2 (source: ClawHub release evidence and references/release-notes.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
