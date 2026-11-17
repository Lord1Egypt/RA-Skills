## Description:

Automates a GitHub pull request review workflow from structured code review through issue tracking, fix verification, merge gating, and summary reporting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zlszhonglongshen](https://clawhub.ai/user/zlszhonglongshen)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to coordinate GitHub pull request reviews, create Issues for blocking findings, generate CI quality gates, and report whether a PR is ready to merge.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create persistent GitHub Issues, comments, workflow files, or other repository changes.

Mitigation: Use least-privilege GitHub tokens and require explicit approval before any write operation.

Risk: The skill can participate in merge-related decisions without clear confirmation gates.

Mitigation: Require branch protection, passing CI, and human confirmation before merge-related actions are applied.

Risk: Automated review findings may be incomplete or inaccurate for large or complex pull requests.

Mitigation: Treat generated review output as decision support and require maintainers to review blocking findings and suggested fixes.

## Reference(s):

- [PR Review Factory Skill Page](https://clawhub.ai/zlszhonglongshen/skills/pr-review-factory)
- [Skill README](artifact/README.md)
- [Skill Definition](artifact/SKILL.md)
- [Workflow Definition](artifact/workflow.json)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown reports, JSON summaries, YAML workflow configuration, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce GitHub Issue content, pull request review summaries, and CI workflow configuration for repository write operations.]

## Skill Version(s):

1.0.0 (source: frontmatter, workflow.json, server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
