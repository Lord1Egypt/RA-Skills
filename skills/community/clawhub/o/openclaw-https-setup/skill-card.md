## Description:

Automate HTTPS setup for OpenClaw Gateway on a VPS by configuring Nginx as a reverse proxy, obtaining TLS certificates, and redirecting HTTP traffic to HTTPS.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nanue1](https://clawhub.ai/user/nanue1)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to expose a running OpenClaw Gateway service through a custom domain with HTTPS on a VPS. It provides setup guidance and helper automation for Nginx, Certbot, SELinux networking, reverse proxy headers, and certificate renewal.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The helper script makes privileged Nginx and Certbot changes using unvalidated domain and email inputs.

Mitigation: Review the script before use, validate domain and email values, quote variable expansions, and run it only with trusted inputs.

Risk: Certificate renewal is configured by manually appending a crontab entry.

Mitigation: Prefer the platform Certbot renewal timer or review the existing crontab before adding renewal automation.

Risk: The setup changes web server, firewall-adjacent, SELinux, and certificate state on a VPS.

Mitigation: Apply it first in a controlled environment, back up existing Nginx configuration, and test Nginx configuration before reload.

## Reference(s):


## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with bash commands, Nginx configuration, and shell-script guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose privileged VPS administration commands for Nginx, Certbot, SELinux, systemd, and certificate renewal.]

## Skill Version(s):

1.0.0 (source: server release evidence and artifact META.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
