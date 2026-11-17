## Description:

行业雷达按行业与技术关键词采集多源 RSS 内容、筛选并归纳文章，生成结构化情报简报；未配置 LLM 时使用本地规则引擎。

This skill is ready for commercial/non-commercial use.

## Publisher:

[morningstar-lu](https://clawhub.ai/user/morningstar-lu)

### License/Terms of Use:

MIT-0

## Use Case:

行业分析师与开发者可组合行业词和技术词来整理多源 RSS 动态，并生成结构化情报简报或周报。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Default access settings could expose saved reports.

Mitigation: Use only an isolated local demo until browser origins are restricted and private credentials are configured before first startup; changing credential environment variables does not update an existing account.

Risk: Paid model requests or sensitive keywords could be sent to a third-party model service before its safeguards are confirmed.

Mitigation: Keep paid models and sensitive keywords disabled until the model HTTP client matches the documented safeguards.

Risk: Deleting a subscription or data may leave retained report files.

Mitigation: Manually remove retained report files when deleting data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/morningstar-lu/skills/industry-radar)
- [API reference](artifact/references/api-reference.md)
- [Architecture reference](artifact/references/architecture.md)
- [Configuration reference](artifact/references/config-reference.md)

## Skill Output:

**Output Type(s):** [Markdown, Text, JSON]

**Output Format:** [Structured industry intelligence briefings in Markdown; REST API responses in JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Briefings summarize collected articles and include source links. LLM summarization is optional; when enabled, article text and subscription keywords are sent to the configured third-party model service.]

## Skill Version(s):

1.1.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
