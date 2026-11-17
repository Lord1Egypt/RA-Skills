## Description:

Fetch construction material prices from open APIs. Track price trends, regional variations, and update cost databases.

This skill is ready for commercial/non-commercial use.

## Publisher:

[datadrivenconstruction](https://clawhub.ai/user/datadrivenconstruction)

### License/Terms of Use:

MIT

## Use Case:

Developers, estimators, and construction cost teams use this skill to fetch construction material price data, analyze trends and regional factors, and prepare updates for cost databases from user-provided project or pricing data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: FRED API keys may be exposed if full request URLs or parameters are logged.

Mitigation: Use a limited API key and avoid logging full URLs or request parameters that include credentials.

Risk: Generated price updates may change business cost records based on incomplete or stale market data.

Mitigation: Validate price updates against trusted sources and back up cost datasets before applying changes.

Risk: Network requests to FRED may fail, return incomplete data, or be unavailable in some environments.

Mitigation: Handle empty or failed API responses explicitly and document when estimates rely on fallback or user-provided data.

## Reference(s):

- [Data Driven Construction](https://datadrivenconstruction.io)
- [FRED API Documentation](https://fred.stlouisfed.org/docs/api/)
- [Price Api on ClawHub](https://clawhub.ai/datadrivenconstruction/skills/price-api)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown with structured tables and Python code or configuration guidance when relevant]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May describe optional exports to Excel, CSV, or JSON based on user-provided data.]

## Skill Version(s):

2.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
