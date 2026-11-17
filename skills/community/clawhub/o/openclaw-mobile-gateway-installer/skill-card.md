## Description:

Installs and manages OpenClaw mobile gateway as a system service. Invoke when users need one-command deploy, start, stop, upgrade, or uninstall.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jason141123-sys](https://clawhub.ai/user/jason141123-sys)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to install, upgrade, check, restart, and uninstall an OpenClaw mobile gateway backed by a systemd service. It is intended for environments where a mobile APK needs a gateway endpoint for OpenClaw administration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installed gateway can expose administrative OpenClaw functions and secrets if reachable from untrusted networks.

Mitigation: Install only in a tightly controlled environment, do not expose port 4800 to untrusted networks, and place the service behind authentication, TLS, and firewall rules.

Risk: The installer creates an autostarting systemd service and writes service configuration containing sensitive OpenClaw and provider credentials.

Mitigation: Review the install and uninstall scripts before use, protect configured credentials, and rotate credentials if the service has already been reachable.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jason141123-sys/skills/openclaw-mobile-gateway-installer)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands and configuration values]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill may direct users to run installer, health-check, service-management, and uninstall commands.]

## Skill Version(s):

1.0.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
