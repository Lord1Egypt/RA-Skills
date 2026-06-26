## Description: <br>
Trend Radar generates weekly technology and market trend reports from web search results. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mupengi-bot](https://clawhub.ai/user/mupengi-bot) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, founders, and market researchers use this skill to monitor AI, SaaS, Korean startup, and OpenClaw ecosystem trends and produce weekly summary reports with highlights, category statistics, and follow-up keywords. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Web-based trend reports may include outdated, incomplete, or misleading market information. <br>
Mitigation: Review cited sources and important claims before using a report for business, product, or investment decisions. <br>
Risk: Optional weekly cron execution and saved report files can retain local research history longer than intended. <br>
Mitigation: Enable the cron example only when scheduled reports are desired, and periodically review or delete saved reports and event files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mupengi-bot/mupeng-trend-radar) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, JSON, Shell commands, Configuration] <br>
**Output Format:** [Markdown report with optional JSON event records and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports are saved under memory/research/trend-YYYY-WXX.md; optional event records use events/trend-update-YYYY-MM-DD.json.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
