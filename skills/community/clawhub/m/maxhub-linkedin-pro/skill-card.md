## Description:

LinkedIn 职业社交公开数据查询 skill，通过 MaxHub API 查询公司、职位、人员资料、员工列表、帖子、评论、搜索和关联数据。

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiewxx](https://clawhub.ai/user/xiewxx)

### License/Terms of Use:

MIT-0

## Use Case:

B2B analysts, recruiters, and business teams can use authorized public LinkedIn data to research companies, job openings, professional profiles, posts, and comments, then prepare market or recruiting summaries. Keep personal occupational data to the minimum needed for the task.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review flags an unpinned installer.

Mitigation: Check the installer source and version, and pin a reviewed version before installation.

Risk: Query details are sent to the named third-party API service.

Mitigation: Send only authorized, necessary query data; keep API keys and other secrets out of prompts, logs, and responses.

Risk: The security review reports an automatic confirmation record and broad recipe triggers.

Mitigation: Check that any recorded legal confirmation reflects the user's explicit consent, and confirm the intended query when a trigger is broad or ambiguous.

Risk: Some references were unresolved or ambiguous, and scanner coverage is partial.

Mitigation: Review the relevant reference files and verify the selected query flow before relying on it.

## Reference(s):

- [Server-resolved source repository](https://github.com/XieWxx/maxhub-api-skills/tree/main/maxhub-linkedin)
- [ClawHub release](https://clawhub.ai/xiewxx/skills/maxhub-linkedin-pro)
- [MaxHub API service](https://www.aconfig.cn)
- [LinkedIn Developer Platform](https://developer.linkedin.com)
- [Recipe index](artifact/references/recipes/_index.md)
- [Parameter mapping guide](artifact/references/param-mappings.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Analysis]

**Output Format:** [Concise Chinese or English text and Markdown summaries, tables, and analysis]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May contain professional or other personal data returned by the API; minimize data and do not expose API keys, cookies, or tokens.]

## Skill Version(s):

0.1.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
