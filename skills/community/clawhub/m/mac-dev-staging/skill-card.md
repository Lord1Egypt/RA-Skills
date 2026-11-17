## Description:

Turn a macOS machine into a local PHP/MariaDB staging server using the stock macOS Apache, Homebrew PHP 8.5, MariaDB, built-in SFTP, npm tooling, a local dev gateway surface, and optional nginx.

This skill is ready for commercial/non-commercial use.

## Publisher:

[matthewxmurphy](https://clawhub.ai/user/matthewxmurphy)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to configure a Mac as a repeatable local PHP staging node for Joomla, WordPress, CodeIgniter, Laravel, or similar apps. It helps detect the existing stack, install or verify Homebrew services, render Apache configuration, verify SFTP, check ports, and keep receipts for staging actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can change a Mac's local server posture by enabling services, remote access, and local staging endpoints.

Mitigation: Review the planned Apache, MariaDB, nginx, SSH/SFTP, and gateway changes before execution; keep services local or limited to trusted networks.

Risk: Remote Login and SFTP can broaden access to the Mac if enabled for broad users or exposed outside trusted networks.

Mitigation: Use a dedicated staging user, prefer SFTP-only workflows when possible, and limit SSH/SFTP to trusted LAN or VPN access.

Risk: Generated Apache virtual host configuration uses operator-provided hostnames and paths.

Mitigation: Avoid untrusted input to the vhost renderer and inspect generated snippets before installing them with sudo.

Risk: Global npm tooling installs mutable packages that can change over time.

Mitigation: Consider pinning versions or installing project-local tooling for workflows that need reproducible builds.

## Reference(s):

- [Mac Dev Staging ClawHub skill page](https://clawhub.ai/matthewxmurphy/skills/mac-dev-staging)
- [Stock macOS Apache Layout](references/apache-layout.md)
- [SFTP on macOS](references/sftp-on-macos.md)
- [nginx and NPM](references/nginx-and-npm.md)
- [Controller Surface](references/controller-surface.md)
- [Gateway Coexistence](references/gateway-coexistence.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and generated configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce local JSONL receipt files when the receipt helper is used.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
