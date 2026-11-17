## Description:

Backs up and restores local Docker volumes for self-hosted Langfuse deployments, including Postgres and MinIO data, with optional ClickHouse coverage and retention pruning.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nissan](https://clawhub.ai/user/nissan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to back up, prune, and restore data for self-hosted Langfuse deployments running in Docker. It is intended for local operational workflows around Postgres, MinIO, and optional related Langfuse storage services.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Restore operations can overwrite the current Langfuse database and MinIO data.

Mitigation: Test restores on disposable data first, confirm the selected backup date, and stop Langfuse services before restoring production data.

Risk: Backup and restore scripts use a mutable container image for file copy operations.

Mitigation: Pin or pre-vet the container image before operational use.

Risk: Weakly validated backup dates, database names, and backup contents can lead to restoring the wrong data or accepting incomplete backups.

Mitigation: Validate backup dates and database names, require manifests or hashes, and verify them before restore.

Risk: Local backup files may contain sensitive Langfuse data.

Mitigation: Restrict backup directory permissions and store backups only in approved local or secured storage locations.

## Reference(s):

- [Langfuse Backup on ClawHub](https://clawhub.ai/nissan/skills/langfuse-backup)
- [Publisher profile](https://clawhub.ai/user/nissan)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and executable shell scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Docker and operates on local Docker volumes and local backup directories.]

## Skill Version(s):

1.0.2 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
