## Description:

File organization and batch operations for workspace management, including file moves, batch renaming, directory structures, type-based grouping, cleanup, scaffolding, and project layout restructuring.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dougchambes](https://clawhub.ai/user/dougchambes)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and workspace maintainers use this skill to organize files, plan batch moves or renames, create standard project structures, and clean up scattered workspace content.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Batch move or rename examples can reorganize many files if run from the wrong directory.

Mitigation: Review generated commands, run a dry run first, and restrict operations to a specific target directory.

Risk: Delete or broad cleanup operations can permanently remove files.

Mitigation: Require explicit confirmation before delete or broad move operations, and prefer recoverable deletion tools when available.

Risk: Project restructuring can be difficult to undo after files are moved.

Mitigation: Create a backup or clean git checkpoint before restructuring.

## Reference(s):

- [File Organization Patterns](artifact/references/patterns.md)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with inline shell commands and directory-structure examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes dry-run, backup, workspace-boundary, and confirmation guidance for broad file operations.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
