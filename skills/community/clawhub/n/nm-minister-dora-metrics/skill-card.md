## Description:

Computes DORA delivery-performance metrics from git and GitHub API

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering managers use the skill to measure delivery performance from repository history and GitHub activity, then identify the weakest DORA metric as an improvement target.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review was incomplete because a local path referenced in SKILL.md was unavailable.

Mitigation: Review the missing referenced file and rescan the release before installation.

Risk: Incorrect production-branch or failure-label choices can skew DORA metrics and cohort comparisons.

Mitigation: Confirm the production branch and GitHub failure labels, and sample contributing issues before relying on the report.

## Reference(s):

- [Project homepage (metadata)](https://github.com/athola/claude-night-market/tree/master/plugins/minister)
- [Agentic Workflow Signals from DORA](modules/agentic-workflow-signals.md)
- [DORA Tier Thresholds](modules/thresholds.md)
- [kuva](https://github.com/Psy-Fer/kuva)

## Skill Output:

**Output Type(s):** [Analysis, Text, JSON]

**Output Format:** [Plain-text report or JSON payload]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Per-metric values and tiers, an overall tier, and the weakest-metric bottleneck.]

## Skill Version(s):

1.10.3 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
