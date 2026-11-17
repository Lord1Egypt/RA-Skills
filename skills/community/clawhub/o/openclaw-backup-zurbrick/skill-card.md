## Description:

Encrypted backup and restore for OpenClaw agents that creates operational archives plus optional age-encrypted secrets for local recovery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zurbrick](https://clawhub.ai/user/zurbrick)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw operators use this skill to create, verify, restore, schedule, and optionally upload OpenClaw backup sets while separating operational data from encrypted secrets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The backup workflow can read broad OpenClaw workspace data and move archive material to GitHub.

Mitigation: Review archive contents before upload, keep repositories private, and treat operational archives as private unless the operator has verified their contents.

Risk: Optional secrets handling can include credentials and authentication profiles.

Mitigation: Include secrets only with explicit operator intent, require age encryption, and avoid pushing secrets unless the operator has a documented reason.

Risk: Restore operations can replace ~/.openclaw and run restored health-check code.

Mitigation: Verify checksums, run restore dry-runs first, and restore only from backup sets the operator trusts.

Risk: Scheduled verification and retention workflows can create recurring jobs and delete old backup sets.

Mitigation: Confirm cron settings and retention policy before enabling scheduled cleanup.

## Reference(s):

- [Restore Guide](references/restore-guide.md)
- [What to Back Up](references/what-to-backup.md)
- [Retention Policy](references/retention-policy.md)
- [Workflows](references/workflows.md)
- [ClawHub Skill Page](https://clawhub.ai/zurbrick/skills/openclaw-backup-zurbrick)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash commands and references to bundled shell scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill guides users through scripts that can create backup archives, manifests, encrypted secrets archives, cron jobs, verification reports, restore dry-runs, and GitHub uploads.]

## Skill Version(s):

1.1.0 (source: server release metadata and changelog, released 2026-03-19)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
