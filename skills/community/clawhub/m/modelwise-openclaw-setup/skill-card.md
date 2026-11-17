## Description:

Guides agents through installing, configuring, running, and checking OpenClaw on Windows, macOS, and Linux.

This skill is ready for commercial/non-commercial use.

## Publisher:

[deerleo](https://clawhub.ai/user/deerleo)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to set up OpenClaw, configure model providers and messaging channels, start the gateway, and verify an installation across Windows, macOS, and Linux.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Gateway or messaging-channel settings may expose the assistant to untrusted users when bound broadly or configured with open wildcard access.

Mitigation: Bind the gateway to 127.0.0.1 unless LAN access is intentional, and use Telegram pairing or an explicit allowlist instead of open wildcard access.

Risk: Installer and update commands may run unpinned or pipe-to-shell package installation steps.

Mitigation: Avoid pipe-to-shell installers when possible, review commands before execution, and pin package versions for repeatable setup.

Risk: Troubleshooting reset commands can delete local OpenClaw data.

Mitigation: Run reset commands only after creating a complete backup outside ~/.openclaw.

## Reference(s):

- [OpenClaw Configuration Reference](references/configuration-reference.md)
- [Telegram Bot Setup Guide](examples/telegram-setup.md)
- [OpenClaw Documentation](https://docs.openclaw.ai)
- [OpenClaw GitHub Repository](https://github.com/openclaw/openclaw)
- [OpenClaw Website](https://openclaw.ai)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, code]

**Output Format:** [Markdown with inline shell commands and JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference local OpenClaw configuration paths, credential names, and messaging-channel settings.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
