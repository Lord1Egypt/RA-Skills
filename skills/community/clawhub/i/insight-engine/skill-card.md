## Description:

Insight Engine turns operational logs and metrics into Python-computed statistics, LLM-interpreted insights, and Notion-ready daily, weekly, or monthly reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nissan](https://clawhub.ai/user/nissan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to generate operational insight reports from AI system logs, Langfuse traces, gateway usage, git activity, and control-plane signals. It is suited for recurring daily, weekly, and monthly analysis workflows that need cited, data-backed conclusions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Operational logs, local memory excerpts, or other sensitive data may be sent to configured model services or network endpoints.

Mitigation: Review the generated data packet before live runs, use dry-run or data-only mode for inspection, and keep Langfuse and Ollama endpoints local or HTTPS-trusted.

Risk: Recurring cron execution can repeatedly write reports to Notion and transmit analysis requests without manual review.

Mitigation: Use dedicated low-privilege Notion credentials and enable scheduled runs only after validating the report content and destination workspace.

## Reference(s):

- [Insight Engine Architecture Reference](references/architecture.md)
- [Daily Insight Analyst Prompt](scripts/prompts/daily_analyst.md)
- [Weekly Insight Analyst Prompt](scripts/prompts/weekly_analyst.md)
- [Monthly Insight Analyst Prompt](scripts/prompts/monthly_analyst.md)
- [ClawHub Skill Page](https://clawhub.ai/nissan/skills/insight-engine)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown reports, Notion page content, shell commands, and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports daily, weekly, monthly, dry-run, and data-only modes.]

## Skill Version(s):

1.0.4 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
