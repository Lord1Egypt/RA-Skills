## Description:

MySQL Master-Slave Setup & Troubleshooting SOP. Covers replication setup, Percona XtraBackup large-volume migration, replica lag investigation, and cross-cloud database acceleration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[freepengyang](https://clawhub.ai/user/freepengyang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and database operators use this skill as an operations SOP for MySQL replication setup, large-volume migration with Percona XtraBackup, replica lag triage, memory investigation, and cross-server migration checkpoints.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Copy-pasteable credential examples can expose database passwords or encourage weak static secrets.

Mitigation: Replace example passwords with managed secrets, rotate any credentials copied during testing, and restrict replication accounts to specific trusted hosts.

Risk: Destructive restore commands can remove a MySQL data directory or target the wrong host.

Mitigation: Confirm target host, database name, datadir, and backup validity before execution, and take tested snapshots or backups before any restore.

Risk: Replication and migration steps can cause production outage or data loss if run outside a controlled maintenance process.

Mitigation: Run only during approved maintenance windows with rollback plans, validated backups, pinned packages, and experienced database operators.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/freepengyang/skills/ops-mysql-master-slave)
- [ClawHub publisher profile](https://clawhub.ai/user/freepengyang)
- [Percona repository package](https://repo.percona.com/yum/percona-release-latest.noarch.rpm)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown SOP with Bash, SQL, and INI code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes operational checklists and command cheatsheets; commands require operator validation before use.]

## Skill Version(s):

1.0.2 (source: server release evidence; artifact frontmatter reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
