## Description:

Folder Organizer helps agents scan folders, design organization rules, classify files with IRK, PARA, and time-based models, generate plans and reports, and execute confirmed file operations with logging.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bojahng](https://clawhub.ai/user/bojahng)

### License/Terms of Use:

MIT-0

## Use Case:

Individuals, teams, and developers use this skill to organize downloads, personal archives, workspaces, disks, and mixed file collections. It supports read-only inventory, classification, rule design, plan generation, user-reviewed execution, rollback planning, and folder documentation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The execution path can move, rename, copy, archive, or back up local files when apply mode is used.

Mitigation: Use the skill only on explicit user-selected folders, inspect the dry-run output and validated plan first, keep backups, and avoid apply mode until the user confirms each material change.

Risk: A user-supplied log path may be removed before a new execution log is written.

Mitigation: Write logs to a dedicated report directory and do not pass an existing important file as the log target.

Risk: The package interface and main documentation are Chinese-only, which can hide operational assumptions from reviewers who do not read Chinese.

Mitigation: Require a reviewer or operator who can read the package language, or translate the workflow, safety guidance, and generated plans before installation or execution.

## Reference(s):

- [Folder Rules](references/folder-rules.md)
- [Output Templates](references/output-templates.md)
- [Taxonomy Patterns](references/taxonomy-patterns.md)
- [Tooling Design](references/tooling-design.md)
- [Workflow](references/workflow.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown reports, JSON plans, CSV move lists, JSONL logs, shell commands, and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports are expected to stay in a dedicated organize_report directory by default; execution should remain dry-run until the user explicitly confirms apply mode.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
