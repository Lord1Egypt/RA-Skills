## Description:

Use this skill to search and read Token Metrics data for requests involving Token Metrics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and analysts use the skill to retrieve Token Metrics prices, OHLCV histories, token listings, market-cap rankings, and trading signals through a connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: CLI setup may execute changing remote code and may add other agent skills during startup.

Mitigation: Review setup commands, prefer a verified oo CLI release, and decide whether to allow additional skills; set OO_SKILLS_SYNC_DISABLED=1 to disable startup synchronization.

Risk: The connected service uses OOMOL-managed credentials and requests may incur charges.

Mitigation: Use the intended connected account and review OOMOL billing and the Token Metrics plan before repeated requests.

## Reference(s):

- [Token Metrics API reference](https://developers.tokenmetrics.com/reference)
- [Token Metrics homepage](https://www.tokenmetrics.com/)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [JSON, Market data, Shell commands, Guidance]

**Output Format:** [JSON market data and Markdown guidance with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returned fields and records depend on the selected Token Metrics action.]

## Skill Version(s):

1.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
