## Description:

行业情报助手用于监控行业和竞品动态，通过 Tavily 搜索抓取资讯、生成结构化情报简报，并支持企业微信、飞书、钉钉等渠道推送。

This skill is ready for commercial/non-commercial use.

## Publisher:

[xuyongliang-eccom](https://clawhub.ai/user/xuyongliang-eccom)

### License/Terms of Use:

MIT-0

## Use Case:

Business, operations, and market-intelligence users can use this skill to collect current industry news, monitor competitors, generate daily or weekly briefings, and schedule report delivery to internal channels.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The scheduling helper can execute user-controlled shell input and create persistent cron tasks.

Mitigation: Review the skill before installation, use it only in an isolated environment, and avoid the scheduling script until shell execution is fixed.

Risk: API keys and delivery targets could be exposed or misdirected during search, report generation, or scheduled delivery.

Mitigation: Prefer TAVILY_API_KEY over command-line key arguments, avoid --break-system-packages, and confirm all recipients before sending or scheduling reports.

## Reference(s):

- [行业情报助手 — 快速上手指南](references/intro.md)
- [Tavily](https://tavily.com)
- [ClawHub skill page](https://clawhub.ai/xuyongliang-eccom/skills/industry-intel-assistant)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown reports, JSON search results, and command-line instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated reports include titles, summaries, source links, dates, and keyword metadata.]

## Skill Version(s):

1.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
