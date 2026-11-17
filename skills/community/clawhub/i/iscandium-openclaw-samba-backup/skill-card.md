## Description:

Backs up OpenClaw data to a remote Samba server and can be triggered for immediate or scheduled backups.

This skill is ready for commercial/non-commercial use.

## Publisher:

[iscandium](https://clawhub.ai/user/iscandium)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw operators use this skill to configure and run backups from a local OpenClaw data directory to a remote Samba share, including optional cron-based automation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores administrator and Samba credentials in JSON configuration.

Mitigation: Do not place real local administrator passwords in the skill config; use protected secret storage and a dedicated backup account where possible.

Risk: The backup can run unattended with root-level mount, copy, and deletion operations.

Mitigation: Enable cron automation only after administrative review, with tightly scoped sudo rules or a root-owned helper.

Risk: Weak path controls could affect which local directory is copied or which remote backup folder is pruned.

Mitigation: Use a fixed mount point, validate source and destination paths, and confirm retention deletion behavior before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/iscandium/skills/iscandium-openclaw-samba-backup)
- [JSON Schema Draft 2020-12](https://json-schema.org/draft/2020-12/schema)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with shell commands and JSON configuration references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May run a backup script that mounts a Samba share, copies OpenClaw data, and prunes retained backups.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
