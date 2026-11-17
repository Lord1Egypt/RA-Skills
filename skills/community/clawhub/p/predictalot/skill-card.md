## Description:

Helps agents forecast time series and train or query tabular prediction models through a user-configured, self-hosted predictalot service.

This skill is ready for commercial/non-commercial use.

## Publisher:

[psyb0t](https://clawhub.ai/user/psyb0t)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and analysts use this skill to request forecasts, uncertainty bands, and sample paths from a trusted predictalot endpoint, or to train and query tabular prediction models on their own features.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Forecasting and training data are sent to the configured service.

Mitigation: Use only an endpoint you control and trust; do not send proprietary data to an untrusted URL.

Risk: A publicly reachable service can expose forecasting and model-management operations.

Mitigation: Keep the service bound to localhost unless protected by TLS, a strong bearer token, and network access controls.

Risk: An unpinned Docker image can change between deployments.

Mitigation: Pin the image to a reviewed version or digest before production use.

Risk: Deleting a stored tabular model is irreversible.

Mitigation: Verify the model ID and obtain explicit confirmation before deletion.

## Reference(s):

- [predictalot on ClawHub](https://clawhub.ai/psyb0t/skills/predictalot)
- [Setup and security guidance](references/setup.md)
- [Model Context Protocol documentation](https://modelcontextprotocol.io)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance]

**Output Format:** [Markdown guidance, shell commands, and JSON forecast responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Forecasts may include quantile bands or sample paths; tabular predictions depend on the selected mode.]

## Skill Version(s):

1.2.2 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
