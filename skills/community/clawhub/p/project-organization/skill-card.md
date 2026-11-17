## Description:

Helps agents organize long-lived, multi-phase projects with structured folders, project scaffolding, file handoff, auditing, version control, and recoverable deletion.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tomuiv](https://clawhub.ai/user/tomuiv)

### License/Terms of Use:

MIT No Attribution

## Use Case:

Developers and other users managing long-lived projects use this skill to create and maintain project hierarchies, route incoming files, audit structure, and recover files moved to trash. It is not intended for one-off temporary tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Trash purges and automatic buffer expiry can remove files that are still needed.

Mitigation: Review status and dry-run results, keep backups, and confirm files are safely stored before purging or relying on buffer cleanup.

Risk: Project setup initializes Git and records persistent changes and logs.

Mitigation: Review the target directory and commit state before running setup or making changes.

Risk: OpenCode project-link repair may change project records or remote sync state.

Mitigation: Inspect status and dry-run output before repair, and avoid remote hub cleanup unless the sync setup is understood.

## Reference(s):

- [Project organization operations manual](references/ops-manual.md)
- [ClawHub skill page](https://clawhub.ai/tomuiv/skills/project-organization)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration instructions]

**Output Format:** [Markdown with shell commands and file-organization guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can guide creation of project folders, indexes, and operation logs.]

## Skill Version(s):

2.6.3 (source: skill frontmatter and ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
