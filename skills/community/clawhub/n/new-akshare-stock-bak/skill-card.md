## Description: <br>
A-share quantitative data analysis helper that uses AkShare to retrieve A-share quotes, historical prices, financial data, sector information, fund flows, IPO data, margin data, and related stock-analysis material. <br>

This skill is for research and development only. <br>

## Publisher: <br>
[make453](https://clawhub.ai/user/make453) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers can use this skill to query A-share market data, inspect financial indicators, and generate informational stock-analysis reports from AkShare or baostock data. Its outputs are for research and reference only, not professional financial advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Market data and generated buy, sell, position-size, stop-loss, or target-price guidance can be stale, unavailable, or misleading. <br>
Mitigation: Verify market data independently and do not rely on the skill output as professional financial advice. <br>
Risk: AkShare or baostock interfaces may fail when upstream websites change or network access is unavailable. <br>
Mitigation: Run in a trusted local environment, add exception handling and retries, and confirm important results against another data source. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/make453/new-akshare-stock-bak) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with Python and shell snippets; included scripts may emit JSON or plain-text analysis reports.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May require network access to AkShare or baostock data sources; market data and analysis should be independently verified.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
