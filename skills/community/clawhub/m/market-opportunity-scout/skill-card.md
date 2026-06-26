## Description: <br>
市场机会侦察兵自动监控 A/H 股市场异动、财经新闻和热点板块，并生成结构化投资机会简报。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yoriko233](https://clawhub.ai/user/yoriko233) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External investors, traders, and finance professionals use this skill to generate Markdown market briefs covering A/H share index movement, highlighted sectors, unusual stocks, finance news, and opportunity notes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill makes public market-data network requests during report generation. <br>
Mitigation: Install and run it only in environments where outbound public market-data requests are acceptable. <br>
Risk: Manual dependency installation may introduce supply-chain or version drift risk. <br>
Mitigation: Review and pin Python dependencies such as akshare and pandas before recurring use. <br>
Risk: A cron entry can create recurring local execution. <br>
Mitigation: Add the cron entry only when recurring reports are intended and review the command path and output destination first. <br>
Risk: Market reports may be delayed or incomplete and are not investment advice. <br>
Mitigation: Treat generated opportunity notes as research inputs and confirm market data before acting on them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yoriko233/market-opportunity-scout) <br>
- [Publisher profile](https://clawhub.ai/user/yoriko233) <br>
- [Support issues](https://github.com/yoriko233/market-opportunity-scout/issues) <br>
- [Eastmoney public market data endpoint](https://push2.eastmoney.com/api/qt/stock/get?secid=1.000001&fields=f43,f44,f170) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown market report and command-line guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports include market overview, hot sectors, unusual stocks, finance news, opportunity notes, and a financial-risk disclaimer.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
