## Description:

Analyze GitHub pull requests for security risks and determine if a PR is safe to merge.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nerdvana-labs](https://clawhub.ai/user/nerdvana-labs)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to assess GitHub pull requests before merge by checking for exposed secrets, unusually large changes, sensitive file edits, and other risk signals.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Private repository analysis may send a GitHub token to an external service.

Mitigation: Use public repositories when possible, or provide only a narrowly scoped, short-lived, read-only token after independently trusting the service owner and credential handling.

## Reference(s):

- [API Reference](artifact/references/api.md)
- [PR Risk Analyzer API Endpoint](https://pr-risk-analyzer.onrender.com/analyze-pr)
- [ClawHub Skill Page](https://clawhub.ai/nerdvana-labs/skills/pr-risk-analyzer)

## Skill Output:

**Output Type(s):** [Analysis, Guidance]

**Output Format:** [Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes a risk level, key issues, summary, and merge recommendation.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
