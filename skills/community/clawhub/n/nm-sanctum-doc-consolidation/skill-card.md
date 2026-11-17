## Description:

Merges ephemeral report and analysis artifacts into permanent documentation

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and documentation maintainers use this skill to identify valuable content in ephemeral Markdown reports, plan where it belongs, and merge it into permanent documentation after approval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Rollback may undo changes from earlier consolidations; the partial scan also left some local references unresolved.

Mitigation: Review rollback behavior before installing, especially where earlier documentation matters, and inspect the proposed plan before approving execution.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/athola/skills/nm-sanctum-doc-consolidation)
- [Project homepage](https://github.com/athola/claude-night-market/tree/master/plugins/sanctum)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Files, Shell commands, Guidance]

**Output Format:** [Markdown consolidation plans, documentation files, and execution summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update documentation and remove source report files after the user approves the consolidation plan.]

## Skill Version(s):

1.10.3 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
