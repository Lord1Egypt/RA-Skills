## Description:

Discover valuable GitHub issues with smart positive-label detection and analyze bug fix feasibility.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linux2010](https://clawhub.ai/user/linux2010)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and open source contributors use this skill to find promising GitHub issues, prioritize maintainer-labeled opportunities, and evaluate whether a bug fix or feature contribution is worth pursuing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may query GitHub and inspect repository context while evaluating issues.

Mitigation: Use it in repositories where GitHub CLI access and local code review are acceptable, and review the repositories and issues being queried.

Risk: The skill may suggest account-changing contribution actions such as commenting on an issue, creating a branch, or preparing pull request work.

Mitigation: Review and approve proposed comments, branch creation, commits, and pull request actions before allowing execution.

Risk: Issue rankings and feasibility assessments may be incomplete or misleading when labels, issue descriptions, or project activity signals are stale.

Mitigation: Confirm maintainer intent, issue status, existing pull requests, and project health before investing significant implementation work.

## Reference(s):

- [Issue Evaluation Criteria](references/evaluation-criteria.md)
- [Issue Analysis Report Template](references/analysis-template.md)
- [Issue Finder on ClawHub](https://clawhub.ai/linux2010/skills/issue-finder)
- [Publisher Profile](https://clawhub.ai/user/linux2010)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown guidance with inline shell commands and optional local markdown reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May query GitHub through the GitHub CLI and may write a local markdown analysis report when requested.]

## Skill Version(s):

1.6.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
