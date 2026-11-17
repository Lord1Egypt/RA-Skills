## Description:

Analyzes public Zhihu content and user data through the MaxHub API, including questions, answers, articles, comments, search, trending content, and user profiles.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiewxx](https://clawhub.ai/user/xiewxx)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers, content teams, and marketers can use the skill to explore Zhihu questions and discussions, study creator profiles, track topics, and prepare content or market insights.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan marks the skill suspicious because reported installation and upgrade actions, local records asserting legal confirmation, and broad search triggers do not align with its stated read-only Zhihu analysis purpose; the available results do not establish malicious intent.

Mitigation: Review installation and upgrade steps and the handling of local compliance records before use. Require the user's explicit review before any action that writes records, asserts legal confirmation, or performs a non-read-only operation; keep searches scoped to the user's request.

Risk: Queries and credentials are sent to the external MaxHub service, and returned Zhihu posts, answers, and comments can contain personal information.

Mitigation: Use only authorized data, minimize personal data in queries, keep the API key and any optional cookies or tokens out of logs and prompts, and review what will be sent to https://www.aconfig.cn.

## Reference(s):

- [Server-resolved source repository and skill path](https://github.com/XieWxx/maxhub-api-skills/tree/main/maxhub-zhihu)
- [知乎数据助手 on ClawHub](https://clawhub.ai/xiewxx/skills/maxhub-zhihu-pro)
- [MaxHub API service](https://www.aconfig.cn)
- [Zhihu Open Platform](https://open.zhihu.com)
- [Data usage policy](artifact/DATA_USAGE_POLICY.md)
- [Query recipes index](artifact/references/recipes/_index.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Analysis, Guidance]

**Output Format:** [Concise summaries and reports based on Zhihu API results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Content and detail depend on the selected query and endpoint.]

## Skill Version(s):

0.1.0 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
