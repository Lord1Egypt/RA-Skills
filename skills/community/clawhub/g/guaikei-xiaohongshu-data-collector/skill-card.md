## Description:

获取小红书公开笔记、评论和博主作品数据，帮助内容创作者、营销团队和分析人员做关键词调研、竞品监控、KOL 筛选和互动质量分析。

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT

## Use Case:

External users, developers, marketers, and analysts use this skill to run command-line Xiaohongshu public-data searches, retrieve note details and comments, monitor creator posts, and prepare structured results for downstream analysis or reporting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends Xiaohongshu query targets to a third-party Guaikei API service.

Mitigation: Install and run it only when that data flow is acceptable for the user's workspace and authorization requirements.

Risk: The skill requires a third-party GUAIKEI_API_TOKEN.

Mitigation: Store the token outside source control, limit access to the runtime environment, and rotate it if exposure is suspected.

Risk: Command results are saved locally and may include Xiaohongshu URLs or collected public-data results.

Mitigation: Keep the workspace private, avoid committing logs/, and delete or redact logs before sharing the workspace.

## Reference(s):

- [完整参数说明](references/options.md)
- [技能更新日志](references/changelog.md)
- [Guaikei API Website](https://www.guaikei.com)
- [ClawHub Skill Page](https://clawhub.ai/engheng-art/skills/guaikei-xiaohongshu-data-collector)

## Skill Output:

**Output Type(s):** [JSON, Shell commands, Configuration, Guidance]

**Output Format:** [JSON command output with concise Markdown usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js 16.14.0+ and GUAIKEI_API_TOKEN; command results may be saved under logs/.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata; artifact metadata reports 1.1.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
