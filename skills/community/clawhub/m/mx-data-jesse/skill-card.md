## Description:

Queries Eastmoney financial data for market prices, financial metrics, and entity relationships.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jessecq1995](https://clawhub.ai/user/jessecq1995)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to query timely financial market, company, and relationship data through natural-language requests and save structured results for analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Query text is sent to Eastmoney's API.

Mitigation: Use only when the user trusts Eastmoney with the query and avoid submitting secrets or highly confidential research text.

Risk: Generated Excel files are local data exports that may contain untrusted returned content.

Mitigation: Treat generated spreadsheets as untrusted files and inspect or scan them before opening in spreadsheet software.

Risk: Broad financial data requests can produce large local outputs and excessive context for downstream agents.

Mitigation: Narrow queries by security, metric, and date range before requesting large historical datasets.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jessecq1995/skills/mx-data-jesse)
- [Eastmoney Mx homepage](https://marketing.dfcfs.com/views/finskillshub/indexIoMv0EzE)

## Skill Output:

**Output Type(s):** [text, markdown, files, json, configuration]

**Output Format:** [Markdown terminal preview plus Excel, text, and raw JSON files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires MX_APIKEY; writes query-named result files to a local output directory.]

## Skill Version(s):

1.0.5 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
