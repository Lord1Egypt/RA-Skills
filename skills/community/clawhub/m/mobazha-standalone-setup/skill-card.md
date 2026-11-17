## Description:

Deploy a self-hosted Mobazha store on any Linux VPS using Docker.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fengzie](https://clawhub.ai/user/fengzie)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to install and manage a standalone Mobazha store on a Linux VPS with Docker, optional domain-based TLS, privacy overlays, and post-install verification.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill guides users to run an unverified remote installer as root on a VPS.

Mitigation: Review the installer source before execution, proceed only if the user trusts the source, and prefer a pinned, checksum- or signature-verified installer.

Risk: The installed system enables persistent automatic updates, which can change services after deployment.

Mitigation: Audit the updater and understand how to disable or control it before using the store for real store or payment data.

Risk: First admin setup without a domain may occur over plain HTTP.

Mitigation: Use a domain with HTTPS or a secure SSH tunnel for initial setup and avoid entering sensitive data over an unsecured connection.

Risk: The workflow may require SSH credentials or root access to a user-provided VPS.

Mitigation: Ask for explicit user confirmation before connecting, avoid storing or logging credentials, and recommend rotating default SSH passwords after setup.

## Reference(s):

- [Mobazha self-host guide](https://mobazha.org/self-host)
- [Standalone installer flags reference](references/install-flags.md)
- [Mobazha standalone installer](https://get.mobazha.org/standalone)
- [ClawHub skill page](https://clawhub.ai/fengzie/skills/mobazha-standalone-setup)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash commands and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include SSH, Docker Compose, systemd, domain, TLS, backup, and troubleshooting commands for a user-provided VPS.]

## Skill Version(s):

0.2.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
