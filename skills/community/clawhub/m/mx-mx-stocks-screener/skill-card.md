## Description: <br>
Mx Stocks Screener lets agents run natural-language screeners across A-shares, Hong Kong and U.S. stocks, ETFs, funds, convertible bonds, and sectors, returning a data description and CSV export. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[akiry09](https://clawhub.ai/user/akiry09) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to screen financial assets with natural-language criteria for cross-market monitoring, portfolio construction, and strategy backtesting. It uses the Eastmoney Miaoxiang service and requires an EM_API_KEY. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends natural-language financial screening requests to an external market-data service using EM_API_KEY. <br>
Mitigation: Install only if the Eastmoney/Miaoxiang service is trusted, keep EM_API_KEY out of prompts, logs, and repositories, and rotate the key if exposure is suspected. <br>
Risk: Generated CSV and description files may contain market data that is outdated, incomplete, or unsuitable for direct investment decisions. <br>
Mitigation: Review generated files before sharing or acting on them, and validate important results against an authoritative financial data source. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/akiry09/mx-mx-stocks-screener) <br>
- [Eastmoney Miaoxiang service](https://ai.eastmoney.com/mxClaw) <br>
- [Eastmoney screening API endpoint](https://ai-saas.eastmoney.com/proxy/b/mcp/tool/selectSecurity) <br>


## Skill Output: <br>
**Output Type(s):** [Text, CSV files, Shell commands, Configuration] <br>
**Output Format:** [CSV file, plain-text description file, and command-line status text with output paths and row count] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires EM_API_KEY; optional MX_STOCKS_SCREENER_OUTPUT_DIR controls where generated files are written.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
