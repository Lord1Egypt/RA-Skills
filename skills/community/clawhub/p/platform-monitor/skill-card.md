## Description:

全平台状态监控助手。监控AI平台可达性、关键词变化、响应时间、竞品动态，支持飞书/微信/钉钉通知、定时巡检、健康度评分。

This skill is ready for commercial/non-commercial use.

## Publisher:

[laozhang-tou](https://clawhub.ai/user/laozhang-tou)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to check AI platform and product availability, response time, keyword changes, announcements, competitor status changes, and scheduled monitoring reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The tool can make repeated network requests to configured URLs.

Mitigation: Review monitored URLs before use and avoid private, internal, or token-bearing URLs.

Risk: Installer scripts can persist scheduled checks through cron or Windows scheduled tasks.

Mitigation: Inspect scheduled task settings after installation and disable automatic checks when they are not needed.

Risk: The scanner classified the release as suspicious because broad URL fetching and opt-out scheduled execution need review.

Mitigation: Install only after reviewing the security guidance, dependency state, and intended monitoring scope.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/laozhang-tou/skills/platform-monitor)
- [Skill instructions](artifact/SKILL.md)
- [Platform Monitor README](artifact/scripts/README.md)
- [Coze manifest](artifact/coze_manifest.json)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON monitoring results and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Monitoring results may include platform status, response time, alerts, summaries, trend analysis, and exported CSV content.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
