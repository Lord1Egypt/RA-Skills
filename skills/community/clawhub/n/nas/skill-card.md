## Description:

Configure, secure, and optimize network attached storage with proper backup strategy, remote access, and media serving.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:


## Use Case:

External users, developers, and home lab operators use this skill for NAS setup and administration guidance across backup planning, remote access, Docker applications, media organization, and security hardening.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: NAS administration guidance can affect storage availability, backup reliability, firewall exposure, and account access.

Mitigation: Apply changes deliberately to the user's own NAS environment, test backups before relying on them, and review network or account changes before deployment.

Risk: Remote access guidance can create exposure if services are published directly to the internet.

Mitigation: Prefer VPN or authenticated reverse proxy access, avoid exposing NAS administration ports publicly, and keep firewall rules limited to required services.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ivangdavila/skills/nas)
- [backup.md](artifact/backup.md)
- [security.md](artifact/security.md)
- [apps.md](artifact/apps.md)
- [media.md](artifact/media.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Configuration instructions, Shell commands]

**Output Format:** [Markdown guidance with checklists, tables, paths, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No executable code or tool calls are included in the artifact.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
