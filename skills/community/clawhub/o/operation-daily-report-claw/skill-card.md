## Description:

运营数据日报虾 automates multi-platform operations data collection, normalization, anomaly detection, Markdown report generation, and Feishu delivery for Douyin, Xiaohongshu, WeChat Channels, Bilibili, and Weibo.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tujinsama](https://clawhub.ai/user/tujinsama)

### License/Terms of Use:

MIT-0

## Use Case:

Operations teams, content teams, and supporting developers use this skill to gather creator-platform metrics, generate daily, weekly, or monthly Markdown reports, detect unusual performance changes, and optionally deliver results to Feishu.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles live analytics credentials and session cookies for creator platforms.

Mitigation: Use scoped official APIs where available, store secrets outside source control, and replace Bash .env sourcing with a safe dotenv parser before deployment.

Risk: Automated Feishu delivery and cron execution can expose business metrics or run with excessive privilege.

Mitigation: Confirm recipients before enabling sends and run scheduled jobs under a low-privilege account with reviewed environment variables.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tujinsama/skills/operation-daily-report-claw)
- [Publisher profile](https://clawhub.ai/user/tujinsama)
- [Anomaly rules](artifact/references/anomaly-rules.md)
- [Platform API guide](artifact/references/platform-api-guide.md)
- [Report templates](artifact/references/report-templates.md)
- [Douyin Open Platform](https://open.douyin.com/)
- [Xiaohongshu Creator Center](https://creator.xiaohongshu.com/)
- [WeCom developer platform](https://work.weixin.qq.com/)
- [Bilibili Creator Center](https://member.bilibili.com/)
- [Weibo Open Platform](https://open.weibo.com/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown reports, JSON data files, shell commands, cron snippets, and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can write raw platform data under data/raw and report files under data/reports when the bundled scripts are run.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
