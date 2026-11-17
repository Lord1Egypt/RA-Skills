## Description:

Linear 工具箱专业版 helps teams manage cross-team Linear boards, bulk issue operations, project health analysis, automation workflows, and permission audit workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, project leads, and operations teams use this skill to inspect Linear work across teams, produce project health summaries, configure workflow automation, and prepare bulk task changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad bulk edits, deletes, exports, or automation changes in Linear could affect many issues or teams if the scope is wrong.

Mitigation: Require explicit human confirmation for bulk actions, show the target team and issue count before execution, and keep rollback information for approved changes.

Risk: Over-privileged Linear credentials could expose or modify workspace data beyond the intended team scope.

Mitigation: Use a least-privilege Linear API key and verify role-based access before cross-team board, audit, or automation workflows are enabled.

Risk: Scheduled automation can repeatedly apply incorrect status changes or notifications if rules are misconfigured.

Mitigation: Use dry runs or manual review for new automation rules before enabling scheduled execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/linear-toolkit-pro)
- [Publisher profile](https://clawhub.ai/user/thcjp)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown, JSON examples, shell command examples, configuration snippets, and structured guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Linear board summaries, project health metrics, automation rule examples, execution logs, and error details.]

## Skill Version(s):

1.0.0 (source: server evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
