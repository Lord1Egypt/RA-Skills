## Description:

当用户需要做好看视频选题、短视频内容方向规划或竞品角度复盘时使用。基于用户提供的主题或视频链接，整理相关作品、标题角度与评论反馈，输出带样本依据的选题清单。来自 SocialDataX 社媒数据助手。

This skill is ready for commercial/non-commercial use.

## Publisher:

[devinchen2014](https://clawhub.ai/user/devinchen2014)

### License/Terms of Use:

MIT-0

## Use Case:

内容创作者和营销人员可根据主题、受众或好看视频链接，整理相关作品与评论样本，制定短视频选题、内容角度和参考标题。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: CLI 使用可变的 @latest 包版本，未来版本变化可能带来供应链风险，并接触执行环境中的凭证。

Mitigation: 执行前核对并固定可信的包版本；仅在需要时配置凭证，并避免在不可信环境运行。

Risk: 主题和视频链接会发送给 SocialDataX，证据中未提供隐私说明。

Mitigation: 调用前避免提交敏感主题或不适合向第三方服务披露的视频链接。

Risk: 扫描证据不完整：Skillspector 无法解析三个本地引用。

Mitigation: 部署前人工审阅无法解析的引用和完整技能内容；不要将另一项扫描的干净结果视为已消除该限制。

## Reference(s):

- [好看视频选题分析 on ClawHub](https://clawhub.ai/devinchen2014/skills/haokan-topic-analysis)
- [SocialDataX API Key and skill access](https://socialdatax.com/ai?from=clawhub)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Guidance]

**Output Format:** [Markdown选题清单，附样本作品链接或 ID]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [可包含候选选题、目标受众、内容角度、参考标题、优先级、理由及样本依据；注明样本数量和缺失信息。]

## Skill Version(s):

0.1.6 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
