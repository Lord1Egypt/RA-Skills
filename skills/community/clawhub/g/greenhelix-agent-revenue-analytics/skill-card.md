## Description:

Provides a revenue analytics guide for AI agent services, covering attribution, customer lifetime value, cohorts, churn prediction, price elasticity, competitive intelligence, and webhook-driven dashboards.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mirni](https://clawhub.ai/user/mirni)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and agent-service publishers use this guide to design revenue measurement workflows for AI agent commerce. It helps agents produce implementation guidance and code examples for revenue attribution, LTV analysis, cohort retention, churn risk, pricing optimization, and revenue dashboards.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The guide references GreenHelix credentials and live billing, revenue, customer, and webhook data.

Mitigation: Use the GreenHelix sandbox or a least-privilege token first, and avoid production billing or customer data until endpoints and webhook destinations are verified.

Risk: The guide includes implementation examples that depend on GreenHelix APIs and the greenhelix-trading package.

Mitigation: Review the code and package source/version, pin dependencies, and validate API behavior before running examples in a production environment.

Risk: The security summary says credential, dependency, and endpoint risks are under-disclosed.

Mitigation: Document required credentials, dependency versions, target endpoints, and data access boundaries before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mirni/skills/greenhelix-agent-revenue-analytics)
- [Publisher profile](https://clawhub.ai/user/mirni)
- [GreenHelix sandbox](https://sandbox.greenhelix.net)
- [GreenHelix API endpoint](https://api.greenhelix.net/v1)
- [GreenHelix developer documentation](https://api.greenhelix.net/docs)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guide with Python code examples, shell commands, and configuration notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [References GREENHELIX_API_KEY and GreenHelix sandbox/API endpoints; the artifact is a non-executable guide.]

## Skill Version(s):

1.3.1 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
