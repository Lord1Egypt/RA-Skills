## Description:

当用户提供红果剧名、剧集链接或 series_id，需要短剧口碑复盘、剧情争议分析、角色反馈整理或多部剧观众评价对比时使用。来自社媒数据助手 SocialDataX。

This skill is ready for commercial/non-commercial use.

## Publisher:

[devinchen2014](https://clawhub.ai/user/devinchen2014)

### License/Terms of Use:

MIT-0

## Use Case:

外部用户可提交红果短剧名称、分享链接或 series_id，获取基于观众评论样本的口碑主题、剧情争议与角色反馈整理，并在有限样本范围内比较多部剧集。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill repeatedly runs an unpinned latest CLI version, which can change without review and may access credentials; the security scan was partial, so its evidence is incomplete.

Mitigation: Pin and review the CLI version before use, and review the unresolved local references because the scan is incomplete.

## Reference(s):


## Skill Output:

**Output Type(s):** [Analysis, Markdown]

**Output Format:** [Markdown report with sample scope, audience themes, comment evidence, and review suggestions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Covers 1–3 dramas by default, up to 2 pages and 20 main reviews per drama, and at most one page of replies for one core dispute; includes up to 3 review suggestions.]

## Skill Version(s):

1.0.3 (source: server-resolved ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
