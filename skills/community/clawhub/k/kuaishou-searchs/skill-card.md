## Description:

快手作品搜索工具，可按关键词、博主主页或视频链接获取快手公开作品、互动指标和评论数据，用于内容选题、竞品监控、KOL筛选和评论洞察。

This skill is ready for commercial/non-commercial use.

## Publisher:

[why20261](https://clawhub.ai/user/why20261)

### License/Terms of Use:

MIT

## Use Case:

External users, content teams, marketers, analysts, and agents use this skill to retrieve structured public Kuaishou video, profile, and comment data for research, reporting, and operational analysis. It requires a GUAIKEI_API_TOKEN and does not support private, hidden, login-gated, posting, or engagement actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends Kuaishou keywords, profile URLs, video URLs, request limits, and GUAIKEI_API_TOKEN to guaikei.com.

Mitigation: Use it only when that data sharing is acceptable, avoid sensitive inputs, and provide a token with the minimum practical scope.

Risk: Returned public video, profile, and comment data is saved locally in logs.

Mitigation: Review retention needs and delete generated log files when the data is no longer needed.

Risk: The skill depends on a third-party API service for results and availability.

Mitigation: Confirm the service terms and retry or pause workflows when API errors, rate limits, or outages are returned.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/why20261/skills/kuaishou-searchs)
- [Server-resolved source repository](https://github.com/why20261/kuaishou-searchs)
- [Guaikei API service](https://www.guaikei.com)
- [Options reference](references/options.md)
- [Changelog](references/changelog.md)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with CLI commands and structured JSON command results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Successful commands return status, request metadata, runtime metadata, and result data; command results are also saved under logs/.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
