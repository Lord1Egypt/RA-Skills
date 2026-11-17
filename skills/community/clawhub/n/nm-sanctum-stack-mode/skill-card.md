## Description:

Detects shared stack membership and iterates a command across all PRs in base-to-tip order.

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill in pull request review or fix workflows to resolve a stack of dependent PRs, run the workflow from base to tip, and prepare a consolidated root-PR summary.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security assessment reports that unauthenticated PR comments can steer workflow targets.

Mitigation: Review PR-comment input and verify the selected PR targets before workflows act on or comment on them.

Risk: The security assessment reports that the promised base-to-tip PR ordering is not enforced.

Mitigation: Check the resolved PR list and dependency order before starting iteration.

## Reference(s):

- [Project homepage (skill metadata)](https://github.com/athola/claude-night-market/tree/master/plugins/sanctum)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Markdown]

**Output Format:** [Markdown guidance with shell command examples and PR summary tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Provides workflow guidance and a consolidated stack summary format.]

## Skill Version(s):

1.10.3 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
