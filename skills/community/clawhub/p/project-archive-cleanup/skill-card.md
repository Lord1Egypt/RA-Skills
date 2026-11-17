## Description:

Archive-clean finished, long-idle project directories — retain planning documents and result artifacts, strip execution traces (one-off scripts, import intermediates, scrape snapshots, console logs, superseded versions, byte-identical duplicates). Use when asked to clean up project leftovers, reduce process noise, or archive completed work. Always read-only scan first, then a two-phase backup-and-delete with batching for the safe-delete threshold.

This skill is ready for commercial/non-commercial use.

## Publisher:

[haiyangchenbj](https://clawhub.ai/user/haiyangchenbj)

### License/Terms of Use:

MIT-0

## Use Case:

Workspace owners and project teams use this skill to review completed, long-idle project directories, preserve planning and result files, and prepare an auditable archive cleanup. It helps identify process traces and duplicates while documenting backups and items that need sign-off.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence flags cleanup guidance that may work around a deletion safety limit, creating a risk of excessive deletion; the scan was partial and some references were unresolved.

Mitigation: Review every proposed deletion and its references before applying, preserve the applicable deletion limit, and verify backups before removing files.

## Reference(s):

- [ClawHub release](https://clawhub.ai/haiyangchenbj/skills/project-archive-cleanup)

## Skill Output:

**Output Type(s):** [Analysis, Guidance, Markdown, Shell commands]

**Output Format:** [Markdown cleanup plans and reports with shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include file classifications, backup and verification steps, and items requiring sign-off.]

## Skill Version(s):

1.0.0 (source: frontmatter; confirmed by release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
