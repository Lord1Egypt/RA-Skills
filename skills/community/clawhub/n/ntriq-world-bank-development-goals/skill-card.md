## Description:

Provides a pay-per-use API description for tracking UN Sustainable Development Goals progress by country, region, or globally using World Bank data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ntriq-gh](https://clawhub.ai/user/ntriq-gh)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can use this skill to understand how to query SDG indicators for impact investment reporting, development program monitoring, and emerging-market sustainability scoring.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill calls a third-party API and may involve x402 USDC payment authorization.

Mitigation: Verify endpoint pricing, payment authorization scope, and expected call volume before using it at scale.

Risk: The API response depends on external data availability and may affect reporting or scoring decisions.

Mitigation: Review returned indicators, years, and trends against the underlying World Bank data before using results in formal decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ntriq-gh/skills/ntriq-world-bank-development-goals)
- [ntriq x402 homepage](https://x402.ntriq.co.kr)
- [World Bank Goals API endpoint](https://x402.ntriq.co.kr/world-bank-goals)
- [Service catalog](https://x402.ntriq.co.kr/services)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, text]

**Output Format:** [Markdown with parameter tables, JSON examples, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Describes optional API parameters for country codes, SDG goals, indicators, and year ranges.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
