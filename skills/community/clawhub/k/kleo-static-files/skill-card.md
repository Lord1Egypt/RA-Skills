## Description:

Host static files on subdomains with optional authentication, file uploads, quota management, and automatic SSL via Caddy.

This skill is ready for commercial/non-commercial use.

## Publisher:

[awaaate](https://clawhub.ai/user/awaaate)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to create static sites, upload files or directories, configure optional basic authentication, and manage hosted content through the `sf` CLI or API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installer path asks users to run an unverified internet script with root privileges.

Mitigation: Download, inspect, and verify a pinned release before installation, especially on production or sensitive hosts.

Risk: The service installation creates a persistent host service with broad system privileges.

Mitigation: Run the service under a dedicated low-privilege account and lock down environment file permissions.

Risk: Clean deploy and delete operations can remove hosted sites or files.

Mitigation: Require explicit backups or confirmation before delete, clean-deploy, or uninstall operations.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/awaaate/skills/kleo-static-files)
- [Installation Guide](references/install.md)
- [Bun Runtime](https://bun.sh)
- [Caddy Web Server](https://caddyserver.com)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with inline bash commands, API endpoint tables, and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes commands that can create, overwrite, delete, and publish files through an external static hosting service.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
