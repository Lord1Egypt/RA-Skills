## Description:

Implements GitHub or GitLab issues via parallel subagents with review gates between task batches

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to retrieve GitHub, GitLab, or Bitbucket issues, plan and implement changes with parallel subagents, and review work before preparing one consolidated pull request.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Completion guidance describes posting tooling feedback to an unrelated external repository without user approval.

Mitigation: Review the feedback step and obtain user approval before posting; skip it when approval is not given.

## Reference(s):

- [Skill homepage](https://github.com/athola/claude-night-market/tree/master/plugins/sanctum)
- [ClawHub skill page](https://clawhub.ai/athola/skills/nm-sanctum-do-issue)

## Skill Output:

**Output Type(s):** [Code, Markdown, Shell commands, Guidance]

**Output Format:** [Code changes with Markdown task plans and inline forge CLI commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Accepts one or more issue numbers or issue URLs; consolidates completed work into one pull request.]

## Skill Version(s):

1.10.3 (source: frontmatter, server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
