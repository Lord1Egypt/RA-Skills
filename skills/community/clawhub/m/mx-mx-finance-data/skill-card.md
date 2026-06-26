## Description: <br>
Mx Finance Data lets agents use Eastmoney Miaoxiang financial data APIs to answer natural-language financial data queries across A-shares, Hong Kong and U.S. stocks, funds, bonds, indexes, sectors, companies, and issuers, producing structured Excel data and a text description. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[akiry09](https://clawhub.ai/user/akiry09) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, analysts, researchers, and agent builders use this skill to retrieve structured financial market, company, valuation, quote, and statement data from Eastmoney using natural-language questions. It is intended for data retrieval and review workflows such as investment research, market monitoring, strategy backtesting, industry analysis, credit research, financial statement review, and asset allocation support, not for subjective investment advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on an Eastmoney API key and sends user query text to the Eastmoney service. <br>
Mitigation: Confirm the Eastmoney service is trusted for the intended data use, keep EM_API_KEY out of prompts, logs, shared files, and committed shell profiles, and rotate or revoke the key if exposure is suspected. <br>
Risk: The skill installs and runs Python dependencies and writes result files locally. <br>
Mitigation: Install dependencies in a virtual environment and review generated Excel and text files before sharing or using them downstream. <br>
Risk: Queries above the supported entity quota are truncated to the first five financial entities. <br>
Mitigation: Split larger requests into smaller batches and check the description file for quota or truncation notes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/akiry09/mx-mx-finance-data) <br>
- [Eastmoney Miaoxiang API key registration](https://ai.eastmoney.com/mxClaw) <br>
- [Eastmoney searchData API endpoint](https://ai-saas.eastmoney.com/proxy/b/mcp/tool/searchData) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Text, Shell commands, Configuration instructions] <br>
**Output Format:** [Excel workbook (.xlsx), text description (.txt), and command-line status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires EM_API_KEY and Python dependencies httpx, pandas, and openpyxl; writes results under a local miaoxiang/mx_finance_data directory and processes at most five financial entities per query.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
