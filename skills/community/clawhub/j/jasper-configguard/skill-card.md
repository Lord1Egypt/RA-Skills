## Description:

Jasper ConfigGuard helps agents and developers apply OpenClaw configuration changes with backups, health checks, dry-run previews, and automatic rollback on failure.

This skill is ready for commercial/non-commercial use.

## Publisher:

[emberdesire](https://clawhub.ai/user/emberdesire)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent operators use this skill to safely patch, validate, diff, back up, restore, and health-check OpenClaw gateway configuration. It is intended for workflows where configuration changes may restart a live gateway and need rollback protection.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can change and restart a live OpenClaw gateway, and the security summary warns that flaws could expose, corrupt, or misapply configuration.

Mitigation: Review carefully before production use, test changes in staging, pin a reviewed package version, and keep an independent backup outside the tool-managed backup directory.

Risk: Configuration files and backups under ~/.openclaw may contain sensitive operational details.

Mitigation: Restrict permissions on ~/.openclaw and its backups, and avoid granting broad filesystem access to agents using this tool.

Risk: Untrusted patch files or backup IDs could cause unexpected configuration changes or restores.

Mitigation: Only pass trusted patch files and backup IDs, and use dry-run and diff commands before applying changes.

## Reference(s):

- [Jasper ConfigGuard on ClawHub](https://clawhub.ai/emberdesire/skills/jasper-configguard)
- [OpenClaw](https://openclaw.ai)
- [Jasper ConfigGuard Product Page](https://exohaven.online/products/jasper-configguard)

## Skill Output:

**Output Type(s):** [shell commands, configuration, code, guidance]

**Output Format:** [Markdown with inline bash and JavaScript examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces OpenClaw configuration patches, dry-run diffs, backup and restore commands, validation checks, and health-check guidance.]

## Skill Version(s):

1.0.0 (source: frontmatter and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
