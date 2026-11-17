## Description:

Provides access to World Bank economic indicators and macroeconomic data, including GDP, inflation, poverty, trade, and development metrics through a pay-per-use API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ntriq-gh](https://clawhub.ai/user/ntriq-gh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and researchers use this skill to retrieve World Bank economic indicators for investment research, country risk modeling, and academic data collection.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill describes the data API as free while access is pay-per-use.

Mitigation: Review the access terms before use and treat each directed API call as a $0.01 USDC micropayment.

Risk: The skill relies on an external endpoint for economic data retrieval.

Mitigation: Use the endpoint only in workflows where external service calls are acceptable and verify returned data before relying on it for decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ntriq-gh/skills/ntriq-world-bank-economic-indicators)
- [ntriq homepage](https://x402.ntriq.co.kr)
- [World Bank economics API endpoint](https://x402.ntriq.co.kr/world-bank-econ)
- [Service catalog](https://x402.ntriq.co.kr/services)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, JSON]

**Output Format:** [Markdown instructions with endpoint examples and JSON response structure]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The API accepts country codes, World Bank indicator codes, optional year ranges, and pagination settings.]

## Skill Version(s):

1.0.0 (source: artifact frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
