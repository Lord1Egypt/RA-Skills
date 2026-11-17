## Description:

Bower is an automatic Google Drive organizer that scans Drive structure and file contents, builds a personalized preference profile, proposes and applies non-destructive moves, renames, and description updates, and never deletes files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[indigokarasu](https://clawhub.ai/user/indigokarasu)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use Bower to clean up, monitor, and maintain Google Drive organization with reviewable proposals for moves, renames, and description updates. It is intended for Drive organization workflows, not web research, general document analysis, or deletion.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad Google Drive access could expose or modify large amounts of user content.

Mitigation: Confirm the exact Drive scopes before installation, limit access to the minimum workable scope, and require visible review before bulk moves, renames, or description writes.

Risk: Scheduled scans and automatic application paths could change Drive organization without timely user review.

Mitigation: Disable or constrain scheduled jobs and automatic apply behavior until review, rollback, and audit logs are confirmed.

Risk: Chronicle/MemPalace ingestion and profile-building flows may store content summaries or preference signals beyond the immediate Drive organization task.

Mitigation: Review and disable those ingestion flows unless desired, and confirm storage location, retention, and deletion controls.

Risk: Self-update or external profile-script execution can alter behavior after installation.

Mitigation: Remove or disable self-update and external profile-script execution paths before deployment unless they are explicitly required and reviewed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/indigokarasu/skills/ocas-bower)
- [README](README.md)
- [Command reference](references/command_reference.md)
- [Decision invariants](references/decision-invariants.md)
- [Analysis schema](references/analysis_schema.md)
- [Organization rules](references/organization_rules.md)
- [Domain logic](references/domains.md)
- [Light scan triage](references/light-scan-triage.md)
- [MCP Drive tooling](references/mcp-drive-tooling.md)
- [Recovery behavior specification](references/spec-ocas-recovery.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with command names, JSON status summaries, and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce reviewable Drive organization proposals, health summaries, and audit-oriented status notes; applying changes requires Drive access and explicit scope.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter and changelog report 1.5.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
