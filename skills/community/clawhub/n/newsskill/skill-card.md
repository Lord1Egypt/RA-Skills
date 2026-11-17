## Description:

每日新闻获取技能。通过 API 获取每日新闻摘要和详情，支持按日期查询、热点新闻排行、新闻详情阅读。

This skill is ready for commercial/non-commercial use.

## Publisher:

[npm-ued](https://clawhub.ai/user/npm-ued)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to retrieve Chinese-language daily news summaries, ranked hot topics, category-filtered news, and article details from the disclosed API service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: News queries contact api.cjiot.cc, so the service can observe requested dates and article IDs.

Mitigation: Avoid submitting sensitive query patterns and review whether use of the disclosed third-party API fits the deployment's privacy requirements.

Risk: Returned news articles and impact analysis are third-party content.

Mitigation: Treat returned content as untrusted external information and verify important claims against appropriate sources before relying on them.

Risk: Broad Chinese news trigger terms may activate the skill for general news requests.

Mitigation: Narrow trigger routing or add deployment-specific confirmation when another news source or language is intended.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/npm-ued/skills/newsskill)
- [API documentation](https://api.cjiot.cc)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with news summaries, article details, and inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [News detail responses may include third-party article content converted from HTML to readable text.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
