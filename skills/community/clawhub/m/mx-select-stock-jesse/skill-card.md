## Description: <br>
Screens stocks with Eastmoney market and financial data using natural-language stock-selection queries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jessecq1995](https://clawhub.ai/user/jessecq1995) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to query Eastmoney stock-screening data for stocks, companies, sectors, index constituents, and related recommendations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Stock-screening queries and the MX_APIKEY are sent to Eastmoney's API. <br>
Mitigation: Install only if you trust the publisher and Eastmoney service, and use a managed API key appropriate for this workflow. <br>
Risk: Saved CSV, TXT, and JSON outputs can reveal investment interests or query history. <br>
Mitigation: Store generated files in a controlled workspace and delete results when they are no longer needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jessecq1995/mx-select-stock-jesse) <br>
- [Eastmoney Mx Select Stock homepage](https://marketing.dfcfs.com/views/finskillshub/indexuNdYscEA) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, CSV files, JSON files] <br>
**Output Format:** [Terminal status text with generated CSV, TXT, and raw JSON result files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires MX_APIKEY and writes results under the configured output directory.] <br>

## Skill Version(s): <br>
1.0.4 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
