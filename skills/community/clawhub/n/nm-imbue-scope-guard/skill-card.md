## Description:

Scores feature worthiness and enforces branch-size limits against overengineering.

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use Scope Guard during brainstorming and planning to score proposed features against value, cost, backlog priority, and branch limits, then decide whether to implement, discuss, defer, or reject them.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Feature deferrals can involve publishing project reasoning or context to GitHub without clear approval.

Mitigation: Review the issue and Discussion content and obtain explicit approval before publishing project-specific context.

Risk: The security scan is partial because several referenced local paths were unresolved.

Mitigation: Resolve and review the referenced paths, especially their GitHub publishing behavior, before relying on the workflow.

## Reference(s):

- [Project homepage](https://github.com/athola/claude-night-market/tree/master/plugins/imbue)
- [ClawHub release page](https://clawhub.ai/athola/skills/nm-imbue-scope-guard)

## Skill Output:

**Output Type(s):** [Guidance, Analysis, Markdown, Shell commands]

**Output Format:** [Markdown guidance with scoring summaries and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Recommendations depend on project goals, backlog, and branch metrics.]

## Skill Version(s):

1.10.3 (source: release metadata, frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
