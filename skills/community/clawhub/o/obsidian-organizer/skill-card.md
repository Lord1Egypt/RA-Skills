## Description:

Organize and standardize Obsidian vaults for reliability and long-term maintainability.

This skill is ready for commercial/non-commercial use.

## Publisher:

[asimons81](https://clawhub.ai/user/asimons81)

### License/Terms of Use:


## Use Case:

External Obsidian users and developers use this skill to organize vault folder structure, enforce deterministic note naming, migrate messy vaults, reduce duplicate or ambiguous notes, and run repeatable audit-and-fix workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Applying proposed renames can change Markdown filenames and affect Obsidian links.

Mitigation: Back up the vault, run the audit in dry-run mode, review the proposed renames, and use --apply only after confirmation.

Risk: Bulk organization can move notes into an unsuitable folder or leave link integrity uncertain.

Mitigation: Propose moves before applying them, keep folder depth shallow, and pause for user review when link integrity is uncertain.

## Reference(s):

- [Folder Structure Standard](references/folder-structure.md)
- [File Naming Rules](references/naming-rules.md)
- [Migration Checklist](references/migration-checklist.md)
- [Obsidian Organizer on ClawHub](https://clawhub.ai/asimons81/skills/obsidian-organizer)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration instructions]

**Output Format:** [Markdown guidance with checklist steps and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose file moves and Markdown file renames; dry-run review and user confirmation are expected before applying changes.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
