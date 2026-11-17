## Description:

Restores OpenClaw data from plain or encrypted backups with checksum verification, current-state backup, and service restart guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[halaoluan](https://clawhub.ai/user/halaoluan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to recover or migrate OpenClaw state from backup archives after crashes, reinstalls, accidental deletion, failed upgrades, or device changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Restoring a backup can replace persistent OpenClaw memory, configuration, sessions, credentials, and installed skills.

Mitigation: Review the backup source and archive contents before restoring, and keep the automatic pre-restore backup until the restored environment has been verified.

Risk: A backup from an untrusted source can introduce unsafe or unwanted OpenClaw state before the service is restarted.

Mitigation: Use only trusted backups, verify checksums when available, inspect archive contents first, and run post-restore checks before normal use.

Risk: Disaster-recovery instructions include a curl-to-shell installer pattern.

Mitigation: Prefer pinned official installers and review install commands before execution.

Risk: Providing backup passwords through shell environment variables can expose secrets through shell history, process environments, or local tooling.

Mitigation: Enter backup passwords interactively where possible and avoid storing them in persistent shell configuration.

## Reference(s):

- [OpenClaw Restore README](README.md)
- [OpenClaw Restore FAQ](FAQ.md)
- [OpenClaw documentation](https://docs.openclaw.ai)
- [OpenClaw disaster recovery guide](https://docs.openclaw.ai/guides/disaster-recovery)
- [OpenClaw Backup companion skill](https://github.com/halaoluan/openclaw-backup)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and recovery instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance may include restore script selection, backup path handling, checksum verification, decryption steps, and post-restore checks.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
