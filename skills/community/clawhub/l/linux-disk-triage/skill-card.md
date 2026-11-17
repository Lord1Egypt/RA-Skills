## Description:

Linux磁盘告警清理与根分区扩容分析。Use when 磁盘告警、需腾空间、问如何扩大根分区。

This skill is ready for commercial/non-commercial use.

## Publisher:

[peterliu-512](https://clawhub.ai/user/peterliu-512)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations engineers use this skill to triage Linux disk usage alerts, identify safe cleanup candidates, and compare low-risk data migration against higher-risk partition expansion plans.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill includes destructive disk cleanup commands and system configuration edits.

Mitigation: Review exact command targets, confirm backups, and approve each deletion, partition change, Docker prune, and /etc write before execution.

Risk: Partition expansion and data migration guidance can cause data loss if applied to the wrong layout.

Mitigation: Verify df, lsblk, filesystem type, partition order, and backup status before following any expansion plan.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/peterliu-512/skills/linux-disk-triage)
- [data-dir-migration-softlink-pattern.md](references/data-dir-migration-softlink-pattern.md)
- [diREDACTED-SECRET.md](references/diREDACTED-SECRET.md)
- [home-partition-cleanup-case-20260829.md](references/home-partition-cleanup-case-20260829.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands are intended for human review before execution, especially destructive cleanup, partition changes, and system configuration edits.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
