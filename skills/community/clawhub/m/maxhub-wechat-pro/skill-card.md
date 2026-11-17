## Description:

Queries and analyzes public WeChat Official Account and Channels content through the MaxHub API, including articles, accounts, comments, engagement, video, livestream, and search data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiewxx](https://clawhub.ai/user/xiewxx)

### License/Terms of Use:

MIT-0

## Use Case:

Content researchers, analysts, and account teams use the skill to retrieve and summarize public WeChat content and engagement data for content research, account analysis, and monitoring. Use it only for authorized purposes and minimize personal data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Query details and supplied identifiers or credentials are sent to an external service.

Mitigation: Review each request, submit only information needed for an authorized purpose, and avoid sending secrets or personal data unless necessary and authorized.

Risk: The release guidance notes local confirmation logging and account-balance access, and the installer version is not pinned.

Mitigation: Review the logging behavior and balance access before use, and verify or pin the installer version before installation.

## Reference(s):

- [Server-resolved source repository](https://github.com/XieWxx/maxhub-api-skills/tree/main/maxhub-wechat)
- [ClawHub release](https://clawhub.ai/xiewxx/skills/maxhub-wechat-pro)
- [MaxHub API](https://www.aconfig.cn)
- [WeChat Open Platform](https://open.weixin.qq.com)
- [Data usage policy](artifact/DATA_USAGE_POLICY.md)
- [Compliance gate](artifact/COMPLIANCE_GATE.md)
- [Recipe index](artifact/references/recipes/_index.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Analysis, Guidance]

**Output Format:** [Text or Markdown summaries and analysis of retrieved WeChat data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include public article, account, comment, engagement, video, livestream, search, or API balance information.]

## Skill Version(s):

0.1.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
