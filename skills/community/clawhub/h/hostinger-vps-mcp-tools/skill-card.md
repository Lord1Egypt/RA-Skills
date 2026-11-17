## Description:

Set up Hostinger VPS servers as AI virtual employees with GUI and Koda (OpenClaw). Use when deploying new VPS instances, setting up remote desktops, installing Koda/OpenClaw, or configuring AI agent workstations. Handles Ubuntu server setup, GUI (XFCE + VNC/XRDP), Docker, and Koda deployment.

This skill is ready for commercial/non-commercial use.

## Publisher:

[maverick-software](https://clawhub.ai/user/maverick-software)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to provision and configure Hostinger VPS instances as AI agent workstations with remote desktop, Docker, OpenClaw/Koda deployment, identity setup, and post-deployment hardening guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unsafe root-level deployment defaults could expose or compromise a VPS.

Mitigation: Review and harden scripts before real use, avoid root SSH key login, and remove passwordless full sudo and Docker access from the runtime account.

Risk: Public XRDP or webchat exposure could make remote access and agent services reachable from the internet.

Mitigation: Avoid public exposure by default; place access behind VPN, Cloudflare Tunnel, HTTPS, or firewall rules, and validate all ports, domains, and keys.

Risk: Unpinned or unverified installers can introduce supply-chain uncertainty during server setup.

Mitigation: Pin and verify installers before execution on production infrastructure.

Risk: Hostinger and integration tokens grant sensitive infrastructure access.

Mitigation: Store tokens as secrets, limit file permissions, avoid plaintext configuration, and rotate any token that may have been exposed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/maverick-software/skills/hostinger-vps-mcp-tools)
- [Hostinger API documentation](https://developers.hostinger.com/)
- [Hostinger API authentication](https://developers.hostinger.com/#description/authentication)
- [Hostinger official MCP server](https://github.com/hostinger/api-mcp-server)
- [Hostinger API tokens](https://hpanel.hostinger.com/api-tokens)
- [hostinger-backend.ts](references/hostinger-backend.ts)
- [hostinger-controller.ts](references/hostinger-controller.ts)
- [hostinger-views.ts](references/hostinger-views.ts)
- [Hostinger VPS Notes](references/hostinger-notes.md)
- [Identity setup](references/identity-setup.md)
- [Security options](references/security-options.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with bash commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces deployment steps and scripts that require operator review before execution on infrastructure.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
