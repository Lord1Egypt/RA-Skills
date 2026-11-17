## Description:

Comprehensive security hardening and installation guide for OpenClaw (formerly Clawdbot/Moltbot), including server hardening, agent installation, and Tailscale/firewall configuration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kime541200](https://clawhub.ai/user/kime541200)

### License/Terms of Use:


## Use Case:

External developers and server operators use this skill to have an agent guide secure setup of a self-hosted OpenClaw instance, including SSH hardening, UFW/Fail2ban setup, Tailscale access, owner allowlisting, and verification checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks an agent to make server-wide SSH, firewall, service, VPN, IPv6, and npm configuration changes that could disrupt access or system behavior.

Mitigation: Review each sudo command before execution, verify key-based non-root SSH access in a second session, and keep console or provider recovery access available.

Risk: The workflow includes unverified install commands such as a curl-to-shell Tailscale installer and a global OpenClaw npm install.

Mitigation: Prefer signed package-manager installation steps where possible, review installer contents before running them, and pin and verify the OpenClaw npm package.

Risk: Firewall and VPN rule changes can unintentionally expose services or block intended administration paths.

Mitigation: Confirm UFW, listening socket, Tailscale, and OpenClaw health checks after changes and before ending the setup session.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kime541200/skills/openclaw-server-secure-skill)
- [Tailscale install script](https://tailscale.com/install.sh)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash and JSON code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes privileged Linux server commands that require user review before execution.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
