## Description:

舆情情绪分析专业版 helps agents run portfolio-scale news and market sentiment monitoring workflows with batch stock scans, custom weighting, report export, trend comparison, and sentiment alerts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

External developers, analysts, and enterprise risk teams use this skill to direct an agent through command-line sentiment scans across portfolios, generate JSON, CSV, or HTML reports, compare sector or historical trends, and configure alerts. It is an investment research aid and does not provide investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks agents to run command-line scripts and scheduled or watch-mode jobs.

Mitigation: Review the exact commands before execution, avoid broad automatic invocation, and confirm how to stop scheduled jobs before enabling recurring monitoring.

Risk: The skill may contact financial/news APIs and notification services, including email or webhook destinations.

Mitigation: Confirm API endpoints, credentials, SMTP settings, webhook URLs, and recipient lists before use, and keep credentials out of skill files and generated reports.

Risk: The skill can read stock lists and configuration files and write report or log files containing analysis outputs.

Mitigation: Run it in a controlled workspace, inspect output paths, and review generated reports for sensitive data before sharing.

Risk: Sentiment outputs can be incomplete, stale, or misleading for investment and risk decisions.

Mitigation: Treat outputs as research support only and require human review against trusted market data before taking action.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/news-sentiment-tool-pro)
- [Detailed examples](references/detail.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Markdown, JSON, CSV, HTML]

**Output Format:** [Markdown guidance with shell command examples and generated report files in text, JSON, CSV, or HTML formats]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May read stock lists and configuration files, write report files, call financial or news APIs, and send email or webhook notifications when configured.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
