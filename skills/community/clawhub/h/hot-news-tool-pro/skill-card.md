## Description:

企业级新闻聚合工具，支持50+新闻源监控、定时更新、关键词告警、舆情分析与多渠道推送，适合品牌与行业情报。

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

External business, brand, market research, public relations, and industry analysis users use this skill to configure agents for multi-source news monitoring, scheduled collection, keyword alerts, sentiment and trend analysis, and report-oriented outputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Agents may create scheduled monitoring jobs or recurring polling loops.

Mitigation: Require explicit approval for cron expressions, polling intervals, target sources, retention paths, and stop conditions before enabling recurring work.

Risk: Agents may send alert content to email, webhook, or IM destinations.

Mitigation: Use only approved destinations and trusted SMTP or webhook credentials, store secrets outside generated files, and test notifications with non-sensitive content.

Risk: Agents may start a local API service or write report, configuration, archive, and export files.

Mitigation: Bind services to approved interfaces and ports, restrict access where possible, and confine written artifacts to reviewed workspace paths.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/hot-news-tool-pro)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guidance with bash, YAML, JSON, and Python snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide agents to create local configuration, report, archive, export, alert, and API service artifacts.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
