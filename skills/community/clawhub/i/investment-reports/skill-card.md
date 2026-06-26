## Description: <br>
Investage Temp helps track an investment portfolio with valuation, technical, and sentiment analysis, then generates weighted daily reports and email summaries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[arbiger](https://clawhub.ai/user/arbiger) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and individual investors can use this skill to set up a Python and PostgreSQL workflow for portfolio tracking, stock scoring, and daily investment-report generation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Portfolio reports may be sent to hardcoded external email recipients. <br>
Mitigation: Replace the hardcoded precaster email addresses and GOG account before running the reporter, then preview the generated report and verify recipients. <br>
Risk: The scripts may use hardcoded local database account details and scheduled email automation. <br>
Mitigation: Replace the PostgreSQL user and related configuration, verify where portfolio data is stored and sent, and enable the cron job only after review. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/arbiger/investment-reports) <br>
- [Polymarket markets API](https://clobgateway.poly.market/markets) <br>
- [Polymarket gamma markets API](https://gamma.poly.market/markets) <br>
- [Reddit search API](https://www.reddit.com/search.json?q={self.ticker}&sort=hot&limit=20) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with inline shell commands and generated HTML email reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs can use local PostgreSQL data, market data APIs, sentiment sources, and gog email sending when the bundled scripts are executed.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
