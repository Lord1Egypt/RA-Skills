## Description:

Synchronize the team notes bundle into the workspace notes directory with checksum verification, retry handling, and a sync-state marker.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anonymous9n23](https://clawhub.ai/user/anonymous9n23)

### License/Terms of Use:

MIT-0

## Use Case:

Team members and workspace operators use this skill to refresh the workspace notes directory from the team bundle before retention review or archiving.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unsafe archive installation may overwrite unrelated local files or leave existing notes partially changed.

Mitigation: Use a disposable workspace until installation is recoverable, confirm the configured endpoint with the administrator, and keep a separate backup of existing notes before running.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/anonymous9n23/skills/notes-sync-rich)

## Skill Output:

**Output Type(s):** [Files, JSON, Text]

**Output Format:** [Extracted notes files, a JSON sync-state marker, and a plain-text completion summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Notes bundle contents and sync metadata; exact files depend on the published bundle.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
