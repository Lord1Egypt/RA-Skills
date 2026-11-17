## Description:

Use Xweather (xweather.com) to search and read weather data whenever a task involves Xweather.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users can retrieve Xweather forecasts, current observations, and place details through their connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: First-time setup can download and execute an installer without a prior review.

Mitigation: Use a reviewed, version-specific oo CLI installation and require approval before running any downloaded installer.

Risk: The oo CLI setup may synchronize additional skills and use OOMOL account permissions.

Mitigation: Review the CLI's skill-synchronization behavior and OOMOL account permissions before setup.

## Reference(s):

- [Xweather](https://www.xweather.com/)
- [Xweather API documentation](https://www.xweather.com/docs/weather-api/getting-started)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [JSON, Text, Shell commands]

**Output Format:** [JSON weather data with concise textual summaries; oo CLI commands are shown as shell commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Weather results depend on the connected Xweather account and service availability.]

## Skill Version(s):

1.0.4 (source: frontmatter, release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
