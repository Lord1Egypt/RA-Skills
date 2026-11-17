## Description:

Item Management helps users record, organize, search, export, back up, and review personal inventory data through natural-language commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gmmg55](https://clawhub.ai/user/gmmg55)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to maintain a local personal inventory, including item records, expiry reminders, search, statistics, exports, and backup/restore workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Delete, restore, and export workflows can lose or expose personal inventory data.

Mitigation: Review before installing, keep backups before delete or restore operations, restore only trusted JSON backups, and treat generated CSV and HTML reports as sensitive files.

Risk: Cloud-backup setup may copy personal item details outside the user's machine.

Mitigation: Confirm the cloud destination before enabling backup and avoid syncing inventory backups to untrusted accounts or locations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gmmg55/skills/item-management)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, files]

**Output Format:** [Chinese Markdown responses with CLI command invocations and generated CSV, JSON, or HTML files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses local SQLite data and JSON backups in the user's data directory.]

## Skill Version(s):

1.2.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
