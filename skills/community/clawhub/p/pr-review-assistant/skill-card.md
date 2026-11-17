## Description:

Automated pull request review providing detailed feedback on correctness, security, performance, maintainability, testing, and best practices.

This skill is ready for commercial/non-commercial use.

## Publisher:

[charlie-morrison](https://clawhub.ai/user/charlie-morrison)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to collect pull request or local branch diffs and guide an AI reviewer toward structured feedback on quality, security, performance, maintainability, testing, and best practices.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Repository diffs or GitHub PR diffs may be shown to the reviewing agent.

Mitigation: Use the skill only in repositories and GitHub contexts where that code access is intended.

Risk: Large changes can be truncated by the helper's file and diff limits, leaving some changed code outside the review data.

Mitigation: Use focused review settings and inspect any omitted files separately when reviewing broad pull requests.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/charlie-morrison/skills/pr-review-assistant)
- [Publisher profile](https://clawhub.ai/user/charlie-morrison)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown review data or JSON diff summary for agent review]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can focus review categories, select staged changes or a GitHub PR, and cap the number of changed files included.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
