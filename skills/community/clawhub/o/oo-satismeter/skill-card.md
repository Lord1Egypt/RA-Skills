## Description:

SatisMeter (satismeter.com). Use this skill for ANY SatisMeter request — searching and reading data. Whenever a task involves SatisMeter, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and teams use the skill to retrieve SatisMeter project, survey, response, and survey statistics data through an OOMOL-connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup directs the agent to run remote installer payloads that have not been independently verified.

Mitigation: Review setup first, require approval before any downloaded installer runs, and use a pinned, independently verified CLI release.

Risk: The OOMOL connector brokers access to SatisMeter responses through the connected account.

Mitigation: Check the connector's bundled-skill installation behavior and confirm that this account access is appropriate before connecting it.

## Reference(s):

- [SatisMeter homepage](https://satismeter.com)
- [SatisMeter API documentation](https://app.satismeter.com/apidoc)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [JSON, Text, Guidance]

**Output Format:** [JSON connector responses and concise natural-language summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only SatisMeter project, survey, response, and statistics data]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
