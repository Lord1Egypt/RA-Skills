## Description:

Define, measure, and enforce web performance budgets for bundle sizes, asset counts, image weights, third-party scripts, CI failures, and build trends.

This skill is ready for commercial/non-commercial use.

## Publisher:

[charlie-morrison](https://clawhub.ai/user/charlie-morrison)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to measure static web build outputs, define performance budgets, enforce those budgets in CI, track asset-size trends, audit third-party scripts, and identify optimization actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Budget and trend workflows can modify repository files such as performance budget configuration and history.

Mitigation: Review proposed file changes before committing them, and confirm that budget thresholds match the project's performance goals.

Risk: The CI example can post a pull request comment when wired into GitHub Actions.

Mitigation: Review CI permissions and PR-comment behavior before enabling the workflow in a repository.

## Reference(s):

- [Performance Budget Enforcer ClawHub Page](https://clawhub.ai/charlie-morrison/skills/performance-budget-enforcer)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with shell commands, JSON configuration examples, CI snippets, status reports, and optional machine-readable JSON or GitHub annotation formats.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update .perfbudget.json and .perfbudget-history.json when the agent applies the budget or trend workflows.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
