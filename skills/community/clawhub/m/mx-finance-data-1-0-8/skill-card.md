## Description: <br>
Mx Finance Data queries Eastmoney financial data from natural-language requests and returns structured market, company, valuation, and financial-statement results for A-shares, Hong Kong and US stocks, funds, bonds, indexes, sectors, and related entities. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhouhuihui008](https://clawhub.ai/user/zhouhuihui008) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, analysts, and agent workflows use this skill to retrieve structured financial data for investment research, strategy review, market monitoring, industry analysis, credit research, financial statement review, and asset-allocation support. The skill is for data retrieval and file generation, not subjective investment advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires an Eastmoney EM_API_KEY for authenticated data access. <br>
Mitigation: Use a revocable key, keep it in the environment only, and avoid hardcoding or writing it into prompts, logs, code, or output files. <br>
Risk: Financial queries may reveal confidential client positions, trading strategies, or research intent to the Eastmoney service. <br>
Mitigation: Avoid submitting confidential client or strategy details unless the deployment policy permits that disclosure. <br>
Risk: The Python dependencies are specified without pinned versions. <br>
Mitigation: Install dependencies in a virtual environment and review or pin package versions before controlled deployment. <br>
Risk: Returned financial data may be incomplete, quota-truncated, delayed, or unsuitable for direct trading decisions. <br>
Mitigation: Review the generated TXT description for truncation notices and validate material results against approved data sources before investment, audit, or compliance use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zhouhuihui008/mx-finance-data-1-0-8) <br>
- [Eastmoney MxClaw service](https://ai.eastmoney.com/mxClaw) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Text] <br>
**Output Format:** [XLSX workbook plus TXT description and CLI status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are written under the working directory in miaoxiang/mx_finance_data. A single query is limited to the first 5 financial entities and first 3 core indicators when requests exceed the service quota.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and changelog; artifact _meta.json lists 1.0.8) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
