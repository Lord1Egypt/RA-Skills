## Description:

通过 MaxHub API 查询并分析抖音视频、用户、搜索、热榜、直播、创作者、星图及内容趋势数据。

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiewxx](https://clawhub.ai/user/xiewxx)

### License/Terms of Use:

MIT-0

## Use Case:

内容创作者、新媒体团队和市场分析人员可用它查询抖音公开内容与趋势，辅助选题、账号分析和达人评估。使用时应遵循适用的数据保护要求，并仅处理获准的数据。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review notes that API credentials, cookies, or user data may be sent to third-party services, and the skill documents transmission of request data to MaxHub.

Mitigation: Use only authorized data, minimize personal information, avoid other people's cookies or session credentials, and keep API keys out of prompts and logs.

Risk: The skill writes local compliance confirmation and audit records during its documented workflow.

Mitigation: Review the files and location before enabling the workflow, protect access to them, and remove records when they are no longer needed.

Risk: The security review flags an unpinned installer and possible messaging capability; its analysis is partial.

Mitigation: Verify the installer source and release version, and check the endpoint whitelist for the capabilities available in the installed release before use.

## Reference(s):

- [Server-resolved source repository](https://github.com/XieWxx/maxhub-api-skills/tree/main/maxhub-douyin)
- [MaxHub API service](https://www.aconfig.cn)
- [Douyin Open Platform](https://developer.open-douyin.com)
- [Endpoint whitelist](references/endpoints_whitelist.yaml)
- [Data usage policy](DATA_USAGE_POLICY.md)

## Skill Output:

**Output Type(s):** [text, analysis, JSON, Markdown, guidance]

**Output Format:** [Text or Markdown summaries based on JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May contain public content metrics, user-provided identifiers, comments, or audience insights; tailor detail to the user's authorized purpose.]

## Skill Version(s):

0.1.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
