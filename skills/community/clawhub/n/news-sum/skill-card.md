## Description:

新闻汇总与邮件投递技能。当用户要求"生成今日新闻汇总"、"把新闻发给邮箱"时触发。支持：(1) 接收用户指定主题，搜索生成新闻汇总；(2) 按用户要求投递到指定邮箱。

This skill is ready for commercial/non-commercial use.

## Publisher:

[liliangjie91](https://clawhub.ai/user/liliangjie91)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to generate structured daily news summaries for specified topics and optionally send the finished Markdown report to an email recipient.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The email step uses a shell command with generated HTML and recipient input.

Mitigation: Review and fix the email command before use, avoid shell interpolation of generated content, and require explicit confirmation before sending reports or attachments.

Risk: The skill relies on web searches and generated summaries for current news.

Mitigation: Review source links and generated analysis before relying on, archiving, or emailing the report.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/liliangjie91/skills/news-sum)
- [Editor prompt template](references/editor.md)
- [Journalist prompt template](references/journalist.md)
- [Final report format](references/format.md)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, guidance]

**Output Format:** [Markdown reports, JSON research files, rolling brief text, and an email-send shell command when delivery is requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Default topics are international affairs, economic finance, and technology AI; generated news reports target 7,000 to 10,000 Chinese characters.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
