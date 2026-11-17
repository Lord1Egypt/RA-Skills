## Description:

Mx Finance Data lets agents query Eastmoney financial datasets in natural language for equities, funds, bonds, quotes, company profiles, valuation metrics, and financial statements, returning structured spreadsheet results and a description file.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhouhuihui008](https://clawhub.ai/user/zhouhuihui008)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and finance workflows use this skill to fetch structured financial data for investment research, strategy review, market monitoring, industry analysis, credit research, financial statement review, and asset allocation support. The skill is for structured data retrieval and report generation, not subjective investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a locally configured EM_API_KEY for Eastmoney's API service.

Mitigation: Install and run it only when the Eastmoney API service is trusted, keep the key in an environment variable, and avoid exposing it in code, prompts, logs, or output files.

Risk: Generated spreadsheets contain remote financial data and may include content that spreadsheet applications process specially.

Mitigation: Open generated XLSX files with normal spreadsheet caution, especially around external links or formulas, and review outputs before using them in downstream analysis.

Risk: Requests exceeding the documented query limits are truncated to the first 5 entities and first 3 core indicators.

Mitigation: Keep prompts within the documented limits or split large requests into smaller queries, and check the description file for truncation notes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhouhuihui008/skills/mx-finance-data-1-0-8)
- [ClawHub publisher profile](https://clawhub.ai/user/zhouhuihui008)
- [Eastmoney MxClaw API key registration](https://ai.eastmoney.com/mxClaw)
- [Eastmoney searchData API endpoint](https://ai-saas.eastmoney.com/proxy/b/mcp/tool/searchData)

## Skill Output:

**Output Type(s):** [Files, Text]

**Output Format:** [XLSX spreadsheet and plain-text description file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires EM_API_KEY; writes outputs under ./miaoxiang/mx_finance_data; one request processes up to 5 entities and 3 core indicators.]

## Skill Version(s):

1.0.0 (source: server release metadata and changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
