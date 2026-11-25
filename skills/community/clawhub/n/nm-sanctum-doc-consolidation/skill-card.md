## Description:

Merges ephemeral report and analysis artifacts into permanent documentation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to identify valuable information in temporary reports, create a consolidation plan, and merge approved findings into permanent documentation. It can also summarize the resulting changes and remove source reports after a successful merge.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Rollback may undo earlier documentation consolidations, and some referenced paths were unavailable for review, leaving the security assessment incomplete.

Mitigation: Review rollback behavior and confirm affected documentation and referenced paths are present before execution.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/athola/skills/nm-sanctum-doc-consolidation)
- [Project homepage](https://github.com/athola/claude-night-market/tree/master/plugins/sanctum)

## Skill Output:

**Output Type(s):** [Analysis, Guidance, Markdown, Files]

**Output Format:** [Markdown consolidation plans, documentation updates, and execution summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Execution may create or update documentation and delete source reports after successful merges.]

## Skill Version(s):

1.10.4 (source: server-resolved ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
