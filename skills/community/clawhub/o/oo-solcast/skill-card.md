## Description:

Solcast (solcast.com). Use this skill for ANY Solcast request — searching and reading data. Whenever a task involves Solcast, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and analysts can use this skill to retrieve Solcast irradiance and weather forecasts, historical estimates, and live estimated actuals for a location. They provide a latitude and longitude and receive the matching Solcast data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: CLI setup may execute unverified remote code without clear user approval.

Mitigation: Review and approve CLI installation separately, prefer a verified release, and check which additional agent skills it installs.

Risk: Connecting Solcast entrusts OOMOL with access to the account's API credentials.

Mitigation: Connect only if comfortable entrusting those credentials to OOMOL, and review the connection and account permissions.

## Reference(s):

- [Solcast API documentation](https://docs.solcast.com.au/)
- [Solcast](https://solcast.com)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)
- [oo CLI installation guide](https://cli.oomol.com/install-guide.md)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Shell commands, Guidance]

**Output Format:** [Solcast data returned as JSON, with shell commands and concise text guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses latitude and longitude; forecast data covers up to 14 days, historical estimates are available from 2007 through 7 days ago, and live estimated actuals cover the past 7 days.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
