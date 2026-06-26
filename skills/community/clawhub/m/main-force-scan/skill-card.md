## Description: <br>
Scans Chinese A-share main-board stocks for volume-price patterns that may indicate accumulation, then produces a ranked candidate report for review. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[2459762052-spec](https://clawhub.ai/user/2459762052-spec) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Market-research users or agent operators use this skill to run post-market or intraday scans of Shanghai and Shenzhen main-board stocks and review a Top 20 markdown report of candidates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The scan contacts Eastmoney public endpoints and depends on their availability and data quality. <br>
Mitigation: Run only where that network access is acceptable and verify unusual results against another market-data source. <br>
Risk: The bundled script uses fixed local OpenClaw output paths and may need to be run as Python despite the shell-style usage example. <br>
Mitigation: Review and adjust the output paths for the target environment, then execute it with Python or an environment that honors the shebang. <br>
Risk: Candidate rankings can be inaccurate and are not financial advice. <br>
Mitigation: Treat the report as informational research only and require independent review before making trading decisions. <br>


## Reference(s): <br>
- [主力建仓前兆 - 详细参考](references/methodology.md) <br>
- [Eastmoney Finance](https://finance.eastmoney.com/) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, text, shell commands, guidance] <br>
**Output Format:** [Markdown report with terminal status text and shell command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes a dated local scan report from public Eastmoney market data.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
