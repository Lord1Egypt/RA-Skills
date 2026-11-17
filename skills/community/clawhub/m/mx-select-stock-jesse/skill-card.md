## Description:

An Eastmoney data-based stock-screening tool that filters stocks by market indicators, financial indicators, and other user-provided conditions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jessecq1995](https://clawhub.ai/user/jessecq1995)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to submit natural-language stock-screening queries to Eastmoney's Miaoxiang API and receive filtered stock, company, sector, index, fund, or ETF results for review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Stock-screening query text is sent to Eastmoney's Miaoxiang API using MX_APIKEY.

Mitigation: Keep sensitive information out of queries and install only when this network use is acceptable.

Risk: Generated CSV, description, and raw JSON files are retained in the output directory.

Mitigation: Review the output directory and remove retained result files when they are no longer needed.

Risk: Generated CSV values should be treated as untrusted data.

Mitigation: Open generated CSVs with spreadsheet formula execution disabled or sanitize untrusted values first.

## Reference(s):

- [Eastmoney Miaoxiang homepage](https://marketing.dfcfs.com/views/finskillshub/indexuNdYscEA)
- [ClawHub skill page](https://clawhub.ai/jessecq1995/skills/mx-select-stock-jesse)

## Skill Output:

**Output Type(s):** [text, csv, json, files]

**Output Format:** [Terminal status text plus saved CSV, description text, and raw JSON files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires MX_APIKEY and writes results under the configured output directory.]

## Skill Version(s):

1.0.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
