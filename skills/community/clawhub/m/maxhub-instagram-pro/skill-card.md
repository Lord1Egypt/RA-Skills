## Description:

通过 MaxHub API 查询和分析 Instagram 的公开或用户授权数据，涵盖帖子、Reels、Stories、评论、用户资料、搜索与话题。

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiewxx](https://clawhub.ai/user/xiewxx)

### License/Terms of Use:

MIT-0

## Use Case:

社媒运营人员、研究者和内容分析团队可用它查询 Instagram 公开或经授权的内容与账户数据，并生成内容互动、受众和趋势分析。请按适用的用户授权和数据保护要求使用。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Identifiers, search terms, URLs, API keys, and optional cookies or tokens are sent to the third-party MaxHub service.

Mitigation: Use only authorized inputs, minimize personal data, keep credentials out of logs and prompts, and avoid providing cookies or tokens unless required and authorized.

Risk: The security review flags consent recordkeeping and broad request triggers as areas requiring care.

Mitigation: Confirm the user's authority and purpose, document consent where personal data is involved, and keep requests within the stated scope.

Risk: The security review notes an unpinned installer command.

Mitigation: Verify the installation source and selected version before running the installer.

## Reference(s):

- [Server-resolved source repository and skill path](https://github.com/XieWxx/maxhub-api-skills/tree/main/maxhub-instagram)
- [MaxHub API](https://www.aconfig.cn)
- [Instagram Graph API documentation](https://developers.facebook.com/docs/instagram-api)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Analysis]

**Output Format:** [Text or structured Markdown/JSON summaries and reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Query results depend on the MaxHub API response; the skill does not produce local files.]

## Skill Version(s):

0.1.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
