## Description:

Automatically collects, filters, evaluates, and records pharmaceutical system bidding opportunities from Chinese procurement websites for bid and sales teams.

This skill is ready for commercial/non-commercial use.

## Publisher:

[elliotlaw](https://clawhub.ai/user/elliotlaw)

### License/Terms of Use:

MIT

## Use Case:

Sales, bid operations, and healthcare procurement teams use this skill to monitor pharmaceutical system tenders, screen deadlines and budgets, record structured opportunity data, and generate bidding recommendations.

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: WeCom secrets may be exposed in logs.

Mitigation: Review and fix secret logging before installation, and keep WeCom tokens and secrets out of logs and committed configuration.

Risk: Business data may be sent automatically to WeChat Work destinations.

Mitigation: Use least-privilege WeCom credentials, restrict webhook destinations to approved endpoints, and add a dry-run or approval step before records or notifications are sent.

Risk: The release includes both an in-process scheduler and a supplied crontab.

Mitigation: Choose one scheduler model during deployment to avoid duplicate automated runs.

## Reference(s):

- [ClawHub skill release page](https://clawhub.ai/elliotlaw/skills/pharmaceutical-bidding)
- [Skill overview](artifact/SKILL.md)
- [Release README](artifact/README.md)
- [WeChat Work setup guide](artifact/WECHAT_SETUP.md)
- [WeChat Work developer documentation](https://developer.work.weixin.qq.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Configuration, Guidance]

**Output Format:** [Markdown notifications, structured WeChat Work table records, and concise bidding recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can run on a daily schedule when configured and may send records or notifications automatically.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
