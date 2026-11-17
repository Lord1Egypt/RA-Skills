## Description:

Mx Finance Data lets agents answer natural-language requests for Eastmoney financial data across A-shares, Hong Kong and US stocks, funds, ETFs, bonds, indices, and related entities, returning structured market, valuation, company, and financial statement data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[akiry09](https://clawhub.ai/user/akiry09)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and analysts use this skill to retrieve structured financial data for investment research, trading review, market monitoring, industry analysis, credit research, audit support, and asset allocation workflows. It is intended for data retrieval and file generation, not subjective investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A programmatic caller could override the API endpoint and receive the configured Eastmoney API key.

Mitigation: Run the skill in a constrained environment, do not expose endpoint override parameters to users, and restrict outbound traffic to the documented Eastmoney endpoint.

Risk: Untrusted API data is written to XLSX files without formula neutralization.

Mitigation: Treat generated spreadsheets as untrusted external data and review them with spreadsheet protections enabled before sharing or opening in high-trust environments.

Risk: Queries covering more than five financial entities are truncated.

Mitigation: Split larger requests into smaller queries and review the TXT description file for quota truncation notes.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/akiry09/skills/mx-mx-finance-data)
- [Eastmoney MX service](https://ai.eastmoney.com/mxClaw)
- [Eastmoney searchData endpoint](https://ai-saas.eastmoney.com/proxy/b/mcp/tool/searchData)

## Skill Output:

**Output Type(s):** [files, text]

**Output Format:** [XLSX workbook, TXT description file, and CLI text summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires EM_API_KEY and Python dependencies httpx, pandas, and openpyxl; each query handles at most five financial entities and notes quota truncation in the description file.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
