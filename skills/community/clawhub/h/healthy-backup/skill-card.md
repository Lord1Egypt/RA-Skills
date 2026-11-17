## Description:

Healthy Backup audits an OpenClaw rig before creating encrypted local or optional rclone-synced backups with tiered scope and retention.

This skill is ready for commercial/non-commercial use.

## Publisher:

[littlejakub](https://clawhub.ai/user/littlejakub)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw operators use this skill to configure and run health-gated encrypted backups, with dry-run auditing before scheduled execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Default migratable or full backups may contain unredacted OpenClaw configuration even though documentation says sensitive config is scrubbed.

Mitigation: Review, fix, or explicitly accept this issue before installing; rotate any credentials that may already have been stored in affected backups.

Risk: Optional rclone sync can move encrypted backup archives to a remote destination.

Mitigation: Keep rclone sync disabled unless the remote is trusted and configured for the intended storage boundary.

Risk: Optional crontab and npm collection can expose local system state in dependency manifests.

Mitigation: Leave crontab and npm collection disabled unless needed, and review dry-run output before scheduling backups.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/littlejakub/skills/healthy-backup)
- [Publisher profile: littlejakub](https://clawhub.ai/user/littlejakub)
- [rclone installer reference](https://rclone.org/install.sh)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Files, Guidance]

**Output Format:** [Markdown with inline shell commands and JSON configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create encrypted .tgz.gpg backup archives, health reports, checksum files, cron entries, and optional rclone sync output.]

## Skill Version(s):

1.2.5 (source: server release metadata and target metadata; artifact files report 1.3.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
