## Description:

OC Backup helps OpenClaw users back up key configuration files, workspace data, custom skills, memory, cron data, and device settings with full or category-specific backup modes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[neverland83](https://clawhub.ai/user/neverland83)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw users and developers use this skill to create local backups of critical OpenClaw configuration, data, and custom skill files before upgrades, major edits, or scheduled maintenance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Backups may contain API keys, tokens, private memory, device credentials, and custom skill source in plaintext.

Mitigation: Store backup archives in a private encrypted location and avoid shared or synced folders unless the backup is encrypted.

Risk: A default full backup can include more sensitive OpenClaw data than a specific maintenance task requires.

Mitigation: Use category-specific backup options or dry-run previews when secrets, memory, device data, or custom skill source are not needed.

Risk: Retention cleanup can remove older backup directories from the selected output location.

Mitigation: Run cleanup with dry-run first and confirm the output directory and retention period before deleting old backups.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/neverland83/skills/oc-backup)
- [Backup File List](references/FILE_LIST.md)
- [Recovery Guide Template](references/RECOVERY_GUIDE_TEMPLATE.md)
- [Configuration Example](config/config.example.json)

## Skill Output:

**Output Type(s):** [Files, JSON, Markdown, Shell commands, Guidance]

**Output Format:** [CLI text or JSON plus tar.gz backup archives, JSON manifests, and Markdown recovery guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports full or category-specific backup modes, dry-run previews, custom output directories, and retention-based cleanup.]

## Skill Version(s):

1.1.0 (source: evidence release metadata, SKILL.md, and scripts/backup.js; artifact/package.json reports 1.0.2)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
