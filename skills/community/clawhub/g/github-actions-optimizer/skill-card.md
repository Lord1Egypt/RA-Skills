## Description:

Optimize GitHub Actions workflows for speed, cost, security, and reliability -- analyze run times, cache strategies, job parallelism, and runner selection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[charlie-morrison](https://clawhub.ai/user/charlie-morrison)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and DevOps engineers use this skill to review GitHub Actions workflows and run history for speed, cost, security, and reliability improvements.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Suggested workflow changes may affect CI behavior, cost, or security posture if applied without review.

Mitigation: Review proposed workflow edits and run them in a branch or pull request before merging.

Risk: The skill may inspect workflow files and GitHub Actions run metadata through the GitHub CLI when available.

Mitigation: Use a GitHub account or token with the minimum repository permissions needed for workflow review.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/charlie-morrison/skills/github-actions-optimizer)
- [Publisher profile](https://clawhub.ai/user/charlie-morrison)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown report with recommendations, workflow snippets, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference local workflow files and GitHub Actions run metadata when available.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
