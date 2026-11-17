## Description:

查询货币供应量、汇率、利率和美元指数。

This skill is ready for commercial/non-commercial use.

## Publisher:

[arsars2234](https://clawhub.ai/user/arsars2234)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and analysts use this skill to query U.S. macroeconomic and financial datasets from a local FastAPI service, including money supply, exchange rates, interest rates, Treasury data, GDP components, PCE, CPI/PPI, and related banking tables.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill contacts a fixed internal HTTP service at 10.168.1.162:8000.

Mitigation: Install only in environments that expect and trust this internal service, and prefer HTTPS, authentication, explicit timeouts, and encoded parameters for production or financial decision workflows.

Risk: Query parameters may contain sensitive information.

Mitigation: Avoid sending sensitive query parameters and review requests before running the helper.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/arsars2234/skills/macro-data-api)
- [Publisher profile](https://clawhub.ai/user/arsars2234)
- [Macro data API base URL](http://10.168.1.162:8000)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, JSON, Guidance]

**Output Format:** [JSON responses and Markdown usage guidance with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports default latest-record queries, numeric limits, date-based queries, and JSON query parameters for an allowlisted set of endpoints.]

## Skill Version(s):

1.0.6 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
